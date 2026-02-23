"""
Django admin configuration for Taxonomy models.
"""
from django.contrib import admin
from .models import Country, Category, Theme, Era


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """Admin interface for Countries."""

    list_display = ['name', 'flag_emoji', 'is_active', 'published_stories_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'cultural_overview']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'flag_emoji', 'is_active')
        }),
        ('Cultural Context', {
            'fields': ('cultural_overview',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Categories (Content Pillars)."""

    list_display = ['name', 'order', 'is_active', 'published_stories_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'order', 'is_active')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    """Admin interface for Themes."""

    list_display = ['name', 'is_active', 'published_stories_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'is_active')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Era)
class EraAdmin(admin.ModelAdmin):
    """Admin interface for Eras (Time Periods)."""

    list_display = ['name', 'start_year', 'end_year', 'is_active', 'published_stories_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    list_editable = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'is_active')
        }),
        ('Time Period', {
            'fields': ('start_year', 'end_year', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
