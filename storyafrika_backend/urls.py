"""
URL configuration for StoryAfrika backend.

Routes:
- /admin/ - StoryAfrika Editorial Dashboard
- /api/ - REST API endpoints
- /api/docs/ - API documentation
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # StoryAfrika Editorial Admin
    path("admin/", admin.site.urls),

    # REST API
    path("api/", include("api.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
