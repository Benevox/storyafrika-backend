"""
Serializers for Taxonomy models.
"""
from rest_framework import serializers
from .models import Country, Category, Theme, Era


class CountrySerializer(serializers.ModelSerializer):
    """Serializer for Country model."""

    published_stories_count = serializers.ReadOnlyField()

    class Meta:
        model = Country
        fields = [
            'id',
            'name',
            'slug',
            'cultural_overview',
            'flag_emoji',
            'is_active',
            'published_stories_count',
        ]
        read_only_fields = ['id', 'slug']


class CountryListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for country lists."""

    published_stories_count = serializers.ReadOnlyField()

    class Meta:
        model = Country
        fields = [
            'id',
            'name',
            'slug',
            'flag_emoji',
            'published_stories_count',
        ]
        read_only_fields = ['id', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""

    published_stories_count = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'order',
            'is_active',
            'published_stories_count',
        ]
        read_only_fields = ['id', 'slug']


class CategoryListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for category lists."""

    published_stories_count = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'published_stories_count',
        ]
        read_only_fields = ['id', 'slug']


class ThemeSerializer(serializers.ModelSerializer):
    """Serializer for Theme model."""

    published_stories_count = serializers.ReadOnlyField()

    class Meta:
        model = Theme
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'is_active',
            'published_stories_count',
        ]
        read_only_fields = ['id', 'slug']


class ThemeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for theme lists."""

    class Meta:
        model = Theme
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']


class EraSerializer(serializers.ModelSerializer):
    """Serializer for Era model."""

    published_stories_count = serializers.ReadOnlyField()

    class Meta:
        model = Era
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'start_year',
            'end_year',
            'is_active',
            'published_stories_count',
        ]
        read_only_fields = ['id', 'slug']


class EraListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for era lists."""

    class Meta:
        model = Era
        fields = ['id', 'name', 'slug', 'start_year', 'end_year']
        read_only_fields = ['id', 'slug']
