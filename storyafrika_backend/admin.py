"""
Custom Django Admin configuration for StoryAfrika.
Personalizes the admin interface with StoryAfrika branding.
"""
from django.contrib import admin

# Customize the default admin site
admin.site.site_header = 'StoryAfrika Editorial Dashboard'
admin.site.site_title = 'StoryAfrika Admin'
admin.site.index_title = 'Content Management & Editorial Workflow'
admin.site.site_url = None  # Disable "View site" link
