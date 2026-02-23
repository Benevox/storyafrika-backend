"""
API views for User models.
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, WriterApplication, Bookmark
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    WriterProfileSerializer,
    WriterApplicationSerializer,
    BookmarkSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User management."""

    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Filter queryset based on permissions."""
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(is_active=True)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Get current user's profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """Register a new user."""
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """Login user with email and password."""
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'error': 'Email and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response(
                {'error': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })


class WriterViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for browsing writer profiles."""

    queryset = User.objects.filter(is_writer=True, is_active=True)
    serializer_class = WriterProfileSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'username'


class WriterApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for Writer Applications."""

    queryset = WriterApplication.objects.all()
    serializer_class = WriterApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter based on permissions."""
        user = self.request.user
        if user.is_editor or user.is_staff:
            return WriterApplication.objects.all()
        return WriterApplication.objects.filter(user=user)

    def perform_create(self, serializer):
        """Create application for current user."""
        serializer.save(user=self.request.user)


class BookmarkViewSet(viewsets.ModelViewSet):
    """ViewSet for user bookmarks."""

    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only current user's bookmarks."""
        return Bookmark.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create bookmark for current user."""
        serializer.save(user=self.request.user)
