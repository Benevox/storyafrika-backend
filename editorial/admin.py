"""
Django admin configuration for Editorial models.
"""
from django.contrib import admin
from django.utils import timezone
from .models import (
    StoryReview,
    StoryRevision,
    FeaturedStory,
    EditorialNote,
    ContentGuideline
)


@admin.register(StoryReview)
class StoryReviewAdmin(admin.ModelAdmin):
    """Admin interface for Story Reviews."""

    list_display = [
        'story',
        'reviewer',
        'status',
        'created_at',
        'completed_at',
        'checks_passed'
    ]
    list_filter = ['status', 'created_at', 'completed_at']
    search_fields = ['story__title', 'reviewer__full_name', 'feedback']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Review Info', {
            'fields': ('story', 'reviewer', 'status')
        }),
        ('Feedback', {
            'fields': ('feedback',),
            'classes': ('wide',)
        }),
        ('Editorial Checklist', {
            'fields': (
                'meets_editorial_standards',
                'cultural_sensitivity_check',
                'originality_check',
                'completeness_check'
            )
        }),
        ('Internal Notes', {
            'fields': ('internal_notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )

    def checks_passed(self, obj):
        """Show if all checks passed."""
        all_passed = all([
            obj.meets_editorial_standards,
            obj.cultural_sensitivity_check,
            obj.originality_check,
            obj.completeness_check
        ])
        return '✓' if all_passed else '✗'
    checks_passed.short_description = 'All Checks'

    def save_model(self, request, obj, form, change):
        """Auto-set reviewer if not set."""
        if not obj.reviewer:
            obj.reviewer = request.user
        super().save_model(request, obj, form, change)

    actions = ['approve_reviews', 'request_revisions']

    def approve_reviews(self, request, queryset):
        """Bulk approve reviews and stories."""
        count = 0
        for review in queryset:
            if all([
                review.meets_editorial_standards,
                review.cultural_sensitivity_check,
                review.originality_check,
                review.completeness_check
            ]):
                review.status = 'approved'
                review.completed_at = timezone.now()
                review.story.status = 'approved'
                review.story.save()
                review.save()
                count += 1
        self.message_user(request, f'{count} reviews approved.')
    approve_reviews.short_description = "Approve selected reviews (with checks)"

    def request_revisions(self, request, queryset):
        """Bulk request revisions."""
        count = queryset.update(status='needs_revision')
        self.message_user(request, f'{count} stories marked for revision.')
    request_revisions.short_description = "Request revisions for selected"


@admin.register(StoryRevision)
class StoryRevisionAdmin(admin.ModelAdmin):
    """Admin interface for Story Revisions."""

    list_display = ['story', 'revised_by', 'created_at', 'short_notes']
    list_filter = ['created_at']
    search_fields = ['story__title', 'revision_notes', 'title', 'content']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Revision Info', {
            'fields': ('story', 'review', 'revised_by')
        }),
        ('Snapshot', {
            'fields': ('title', 'content'),
            'classes': ('wide',)
        }),
        ('Notes', {
            'fields': ('revision_notes',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def short_notes(self, obj):
        """Show truncated revision notes."""
        return obj.revision_notes[:50] + '...' if len(obj.revision_notes) > 50 else obj.revision_notes
    short_notes.short_description = 'Notes'


@admin.register(FeaturedStory)
class FeaturedStoryAdmin(admin.ModelAdmin):
    """Admin interface for Featured Stories (Homepage Curation)."""

    list_display = [
        'story',
        'position',
        'featured_by',
        'is_active',
        'start_date',
        'end_date',
        'is_currently_active'
    ]
    list_filter = ['is_active', 'start_date', 'end_date']
    list_editable = ['position', 'is_active']
    search_fields = ['story__title', 'custom_headline']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'

    fieldsets = (
        ('Story', {
            'fields': ('story', 'featured_by', 'position')
        }),
        ('Customization', {
            'fields': ('custom_headline',)
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-set featured_by if not set."""
        if not obj.featured_by:
            obj.featured_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """Optimize queryset."""
        qs = super().get_queryset(request)
        return qs.select_related('story', 'featured_by')


@admin.register(EditorialNote)
class EditorialNoteAdmin(admin.ModelAdmin):
    """Admin interface for Editorial Notes (Internal Communication)."""

    list_display = ['short_note', 'author', 'story', 'is_urgent', 'created_at']
    list_filter = ['is_urgent', 'created_at']
    search_fields = ['note', 'story__title', 'author__full_name']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {
            'fields': ('story', 'author', 'is_urgent')
        }),
        ('Note', {
            'fields': ('note',),
            'classes': ('wide',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def short_note(self, obj):
        """Show truncated note."""
        return obj.note[:80] + '...' if len(obj.note) > 80 else obj.note
    short_note.short_description = 'Note'

    def save_model(self, request, obj, form, change):
        """Auto-set author if not set."""
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(ContentGuideline)
class ContentGuidelineAdmin(admin.ModelAdmin):
    """Admin interface for Content Guidelines."""

    list_display = ['title', 'order', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'order', 'is_active')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('wide',)
        }),
        ('Examples', {
            'fields': ('good_examples', 'bad_examples')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-set created_by if not set."""
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
