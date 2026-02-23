"""
Application configuration for StoryAfrika backend.
"""
from django.apps import AppConfig


class StoryAfrikaConfig(AppConfig):
    """Main application config for StoryAfrika."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'storyafrika_backend'

    def ready(self):
        """Import admin customizations when app is ready."""
        from . import admin  # noqa: F401
