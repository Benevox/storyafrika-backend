"""
API views for Taxonomy models.
"""
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Country, Category, Theme, Era
from .serializers import (
    CountrySerializer,
    CountryListSerializer,
    CategorySerializer,
    CategoryListSerializer,
    ThemeSerializer,
    ThemeListSerializer,
    EraSerializer,
    EraListSerializer,
)


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for browsing countries."""

    queryset = Country.objects.filter(is_active=True).order_by('name')
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def get_serializer_class(self):
        """Use detailed serializer for detail view."""
        if self.action == 'retrieve':
            return CountrySerializer
        return CountryListSerializer

    @action(detail=True, methods=['get'])
    def stories(self, request, slug=None):
        """Get published stories for a specific country."""
        country = self.get_object()
        stories = country.stories.filter(status='published').order_by('-published_at')

        # Import here to avoid circular dependency
        from stories.serializers import StoryListSerializer
        from rest_framework.pagination import PageNumberPagination

        paginator = PageNumberPagination()
        paginator.page_size = 20
        paginated_stories = paginator.paginate_queryset(stories, request)

        serializer = StoryListSerializer(paginated_stories, many=True)
        return paginator.get_paginated_response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for browsing categories (Content Pillars)."""

    queryset = Category.objects.filter(is_active=True).order_by('order', 'name')
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def get_serializer_class(self):
        """Use detailed serializer for detail view."""
        if self.action == 'retrieve':
            return CategorySerializer
        return CategoryListSerializer

    @action(detail=True, methods=['get'])
    def stories(self, request, slug=None):
        """Get published stories for a specific category."""
        category = self.get_object()
        stories = category.stories.filter(status='published').order_by('-published_at')

        # Import here to avoid circular dependency
        from stories.serializers import StoryListSerializer
        from rest_framework.pagination import PageNumberPagination

        paginator = PageNumberPagination()
        paginator.page_size = 20
        paginated_stories = paginator.paginate_queryset(stories, request)

        serializer = StoryListSerializer(paginated_stories, many=True)
        return paginator.get_paginated_response(serializer.data)


class ThemeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for browsing themes."""

    queryset = Theme.objects.filter(is_active=True).order_by('name')
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def get_serializer_class(self):
        """Use detailed serializer for detail view."""
        if self.action == 'retrieve':
            return ThemeSerializer
        return ThemeListSerializer

    @action(detail=True, methods=['get'])
    def stories(self, request, slug=None):
        """Get published stories with this theme."""
        theme = self.get_object()
        stories = theme.stories.filter(status='published').order_by('-published_at')

        # Import here to avoid circular dependency
        from stories.serializers import StoryListSerializer
        from rest_framework.pagination import PageNumberPagination

        paginator = PageNumberPagination()
        paginator.page_size = 20
        paginated_stories = paginator.paginate_queryset(stories, request)

        serializer = StoryListSerializer(paginated_stories, many=True)
        return paginator.get_paginated_response(serializer.data)


class EraViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for browsing historical eras."""

    queryset = Era.objects.filter(is_active=True).order_by('start_year')
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def get_serializer_class(self):
        """Use detailed serializer for detail view."""
        if self.action == 'retrieve':
            return EraSerializer
        return EraListSerializer

    @action(detail=True, methods=['get'])
    def stories(self, request, slug=None):
        """Get published stories from this era."""
        era = self.get_object()
        stories = era.stories.filter(status='published').order_by('-published_at')

        # Import here to avoid circular dependency
        from stories.serializers import StoryListSerializer
        from rest_framework.pagination import PageNumberPagination

        paginator = PageNumberPagination()
        paginator.page_size = 20
        paginated_stories = paginator.paginate_queryset(stories, request)

        serializer = StoryListSerializer(paginated_stories, many=True)
        return paginator.get_paginated_response(serializer.data)
