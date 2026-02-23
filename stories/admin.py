"""
Django admin configuration for Story models.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Story, ReadingSession


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    """Admin interface for Stories."""

    list_display = [
        'title',
        'author',
        'status',
        'category',
        'country',
        'reading_time_minutes',
        'is_featured',
        'published_at'
    ]
    list_filter = [
        'status',
        'category',
        'country',
        'is_featured',
        'created_at',
        'published_at'
    ]
    search_fields = ['title', 'content', 'author__full_name', 'author__email']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = [
        'word_count',
        'reading_time_minutes',
        'content_html',
        'created_at',
        'updated_at',
        'published_at'
    ]
    filter_horizontal = ['themes']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Story Details', {
            'fields': ('title', 'slug', 'author', 'excerpt')
        }),
        ('Content', {
            'fields': ('content', 'content_html'),
            'classes': ('wide',)
        }),
        ('Taxonomy', {
            'fields': ('category', 'country', 'themes', 'era')
        }),
        ('Media', {
            'fields': ('hero_image', 'hero_image_caption')
        }),
        ('Publishing', {
            'fields': ('status', 'is_featured', 'featured_at')
        }),
        ('Metrics', {
            'fields': ('word_count', 'reading_time_minutes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        qs = super().get_queryset(request)
        return qs.select_related('author', 'category', 'country', 'era')

    actions = ['publish_stories', 'unpublish_stories', 'feature_stories', 'unfeature_stories']

    def publish_stories(self, request, queryset):
        """Bulk action to publish stories."""
        count = queryset.filter(status='approved').update(status='published')
        self.message_user(request, f'{count} stories published successfully.')
    publish_stories.short_description = "Publish selected stories"

    def unpublish_stories(self, request, queryset):
        """Bulk action to unpublish stories."""
        count = queryset.filter(status='published').update(status='draft')
        self.message_user(request, f'{count} stories unpublished.')
    unpublish_stories.short_description = "Unpublish selected stories"

    def feature_stories(self, request, queryset):
        """Bulk action to feature stories on homepage."""
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} stories featured.')
    feature_stories.short_description = "Feature selected stories"

    def unfeature_stories(self, request, queryset):
        """Bulk action to unfeature stories."""
        count = queryset.update(is_featured=False)
        self.message_user(request, f'{count} stories unfeatured.')
    unfeature_stories.short_description = "Unfeature selected stories"


@admin.register(ReadingSession)
class ReadingSessionAdmin(admin.ModelAdmin):
    """Admin interface for Reading Sessions (Analytics)."""

    list_display = [
        'story',
        'user',
        'started_at',
        'completed_reading',
        'time_spent_minutes'
    ]
    list_filter = ['completed_reading', 'started_at']
    search_fields = ['story__title', 'user__email', 'session_id']
    readonly_fields = ['started_at']
    date_hierarchy = 'started_at'

    def time_spent_minutes(self, obj):
        """Display time spent in minutes."""
        return f"{obj.time_spent_seconds // 60} min"
    time_spent_minutes.short_description = "Time Spent"

    def get_queryset(self, request):
        """Optimize queryset."""
        qs = super().get_queryset(request)
        return qs.select_related('story', 'user')
