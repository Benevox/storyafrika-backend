"""
API views for Editorial models.
"""
from rest_framework import viewsets, permissions
from .models import FeaturedStory, ContentGuideline
from .serializers import FeaturedStorySerializer, ContentGuidelineSerializer


class FeaturedStoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Featured Stories (public read-only)."""

    queryset = FeaturedStory.objects.filter(
        is_active=True,
        story__status='published'
    ).select_related('story').order_by('position')
    serializer_class = FeaturedStorySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Return only currently active featured stories."""
        queryset = super().get_queryset()
        return [f for f in queryset if f.is_currently_active]


class ContentGuidelineViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Content Guidelines (public read-only)."""

    queryset = ContentGuideline.objects.filter(is_active=True).order_by('order')
    serializer_class = ContentGuidelineSerializer
    permission_classes = [permissions.AllowAny]
