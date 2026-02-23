"""
Django admin configuration for User models.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, WriterApplication, Bookmark


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""

    list_display = ['email', 'full_name', 'is_writer', 'is_editor', 'is_staff', 'date_joined']
    list_filter = ['is_writer', 'is_editor', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'full_name', 'username']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'username', 'biography', 'avatar')}),
        ('Permissions', {'fields': ('is_writer', 'is_editor', 'is_active', 'is_staff', 'is_superuser')}),
        ('OAuth', {'fields': ('google_id',)}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'is_writer', 'is_editor'),
        }),
    )

    ordering = ['-date_joined']
    filter_horizontal = ()


@admin.register(WriterApplication)
class WriterApplicationAdmin(admin.ModelAdmin):
    """Admin interface for Writer Applications."""

    list_display = ['user', 'status', 'created_at', 'reviewed_by', 'reviewed_at']
    list_filter = ['status', 'created_at', 'reviewed_at']
    search_fields = ['user__email', 'user__full_name', 'motivation', 'writing_sample']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Application', {
            'fields': ('user', 'writing_sample', 'motivation')
        }),
        ('Review', {
            'fields': ('status', 'reviewed_by', 'review_notes', 'reviewed_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-approve writer status when application is approved."""
        if obj.status == 'approved' and obj.user:
            obj.user.is_writer = True
            obj.user.save()
        super().save_model(request, obj, form, change)


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    """Admin interface for Bookmarks."""

    list_display = ['user', 'story', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'story__title']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
