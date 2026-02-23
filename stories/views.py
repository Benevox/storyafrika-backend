"""
API views for Story models.
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Story, ReadingSession
from .serializers import (
    StoryListSerializer,
    StoryDetailSerializer,
    StoryCreateSerializer,
    ReadingSessionSerializer,
)


class IsWriterOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow writers to create stories.
    """

    def has_permission(self, request, view):
        # Read permissions for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for authenticated writers
        return request.user.is_authenticated and request.user.is_writer


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit their own stories.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for story author
        return obj.author == request.user


class StoryViewSet(viewsets.ModelViewSet):
    """ViewSet for Story management."""

    permission_classes = [IsWriterOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        """
        Filter stories based on permissions.
        - Public: only published stories
        - Authors: own stories (all statuses)
        - Editors: all stories
        """
        user = self.request.user

        # Editors and staff see everything
        if user.is_authenticated and (user.is_editor or user.is_staff):
            return Story.objects.all().select_related(
                'author', 'category', 'country', 'era'
            ).prefetch_related('themes')

        # Authors see own stories + published stories
        if user.is_authenticated and user.is_writer:
            return Story.objects.filter(
                Q(status='published') | Q(author=user)
            ).select_related(
                'author', 'category', 'country', 'era'
            ).prefetch_related('themes')

        # Public sees only published stories
        return Story.objects.filter(status='published').select_related(
            'author', 'category', 'country', 'era'
        ).prefetch_related('themes')

    def get_serializer_class(self):
        """Use appropriate serializer based on action."""
        if self.action == 'retrieve':
            return StoryDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return StoryCreateSerializer
        return StoryListSerializer

    def perform_create(self, serializer):
        """Save the story with current user as author."""
        serializer.save(author=self.request.user, status='draft')

    @action(detail=True, methods=['post'])
    def submit(self, request, slug=None):
        """Submit a story for editorial review."""
        story = self.get_object()

        # Only author can submit
        if story.author != request.user:
            return Response(
                {'error': 'You can only submit your own stories.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Check if story is in draft status
        if story.status != 'draft':
            return Response(
                {'error': f'Story is already {story.status}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Change status to submitted
        story.status = 'submitted'
        story.save()

        # Create a review entry (will be done in editorial app)
        from editorial.models import StoryReview
        StoryReview.objects.create(story=story, status='pending')

        return Response({
            'message': 'Story submitted for review.',
            'story': StoryDetailSerializer(story).data
        })

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get currently featured stories."""
        from editorial.models import FeaturedStory

        featured = FeaturedStory.objects.filter(
            is_active=True,
            story__status='published'
        ).select_related('story').order_by('position')

        # Get stories from featured
        stories = [f.story for f in featured if f.is_currently_active]

        serializer = StoryListSerializer(stories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search stories by title and content."""
        query = request.query_params.get('q', '')

        if not query:
            return Response(
                {'error': 'Please provide a search query.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        stories = self.get_queryset().filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        )

        page = self.paginate_queryset(stories)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(stories, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def related(self, request, slug=None):
        """Get related stories."""
        story = self.get_object()
        related = story.get_related_stories(limit=4)

        serializer = StoryListSerializer(related, many=True)
        return Response(serializer.data)


class ReadingSessionViewSet(viewsets.ModelViewSet):
    """ViewSet for tracking reading sessions (internal analytics)."""

    queryset = ReadingSession.objects.all()
    serializer_class = ReadingSessionSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        """Create reading session."""
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            # For anonymous users, use session ID
            session_id = self.request.session.session_key
            if not session_id:
                self.request.session.create()
                session_id = self.request.session.session_key
            serializer.save(session_id=session_id)
