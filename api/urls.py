"""
API URL configuration for StoryAfrika.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# Import viewsets
from users.views import (
    UserViewSet,
    WriterViewSet,
    WriterApplicationViewSet,
    BookmarkViewSet,
)
from stories.views import StoryViewSet, ReadingSessionViewSet
from taxonomy.views import CountryViewSet, CategoryViewSet, ThemeViewSet, EraViewSet
from editorial.views import FeaturedStoryViewSet, ContentGuidelineViewSet

# Create router
router = DefaultRouter()

# User endpoints
router.register(r'users', UserViewSet, basename='user')
router.register(r'writers', WriterViewSet, basename='writer')
router.register(r'writer-applications', WriterApplicationViewSet, basename='writer-application')
router.register(r'bookmarks', BookmarkViewSet, basename='bookmark')

# Story endpoints
router.register(r'stories', StoryViewSet, basename='story')
router.register(r'reading-sessions', ReadingSessionViewSet, basename='reading-session')

# Taxonomy endpoints
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'themes', ThemeViewSet, basename='theme')
router.register(r'eras', EraViewSet, basename='era')

# Editorial endpoints
router.register(r'featured', FeaturedStoryViewSet, basename='featured')
router.register(r'guidelines', ContentGuidelineViewSet, basename='guideline')

urlpatterns = [
    # API Documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # JWT Authentication
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Router URLs
    path('', include(router.urls)),
]
