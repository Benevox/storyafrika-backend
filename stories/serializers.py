"""
Serializers for Story models.
"""
from rest_framework import serializers
from .models import Story, ReadingSession
from users.serializers import WriterProfileSerializer
from taxonomy.serializers import (
    CountryListSerializer,
    CategoryListSerializer,
    ThemeListSerializer,
    EraListSerializer
)


class StoryListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for story lists."""

    author = WriterProfileSerializer(read_only=True)
    category = CategoryListSerializer(read_only=True)
    country = CountryListSerializer(read_only=True)

    class Meta:
        model = Story
        fields = [
            'id',
            'title',
            'slug',
            'excerpt',
            'author',
            'category',
            'country',
            'hero_image',
            'status',
            'published_at',
            'reading_time_minutes',
        ]
        read_only_fields = ['id', 'slug', 'published_at', 'reading_time_minutes']


class StoryDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for individual story view."""

    author = WriterProfileSerializer(read_only=True)
    category = CategoryListSerializer(read_only=True)
    country = CountryListSerializer(read_only=True)
    themes = ThemeListSerializer(many=True, read_only=True)
    era = EraListSerializer(read_only=True)

    class Meta:
        model = Story
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'content_html',
            'excerpt',
            'author',
            'category',
            'country',
            'themes',
            'era',
            'hero_image',
            'hero_image_caption',
            'status',
            'is_featured',
            'created_at',
            'updated_at',
            'published_at',
            'word_count',
            'reading_time_minutes',
        ]
        read_only_fields = [
            'id',
            'slug',
            'content_html',
            'created_at',
            'updated_at',
            'published_at',
            'word_count',
            'reading_time_minutes',
        ]


class StoryCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating stories."""

    themes_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Story
        fields = [
            'title',
            'content',
            'excerpt',
            'category',
            'country',
            'themes_ids',
            'era',
            'hero_image',
            'hero_image_caption',
        ]

    def create(self, validated_data):
        """Create story with themes."""
        themes_ids = validated_data.pop('themes_ids', [])
        story = Story.objects.create(**validated_data)

        if themes_ids:
            story.themes.set(themes_ids)

        return story

    def update(self, instance, validated_data):
        """Update story with themes."""
        themes_ids = validated_data.pop('themes_ids', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if themes_ids is not None:
            instance.themes.set(themes_ids)

        instance.save()
        return instance


class StorySubmitSerializer(serializers.Serializer):
    """Serializer for submitting a story for review."""

    story_id = serializers.UUIDField()

    def validate_story_id(self, value):
        """Validate that story exists and belongs to user."""
        try:
            story = Story.objects.get(id=value)
        except Story.DoesNotExist:
            raise serializers.ValidationError("Story not found.")

        # Check if user owns the story (will be added in view)
        return value


class ReadingSessionSerializer(serializers.ModelSerializer):
    """Serializer for Reading Sessions (internal analytics)."""

    class Meta:
        model = ReadingSession
        fields = [
            'id',
            'story',
            'started_at',
            'completed_reading',
            'time_spent_seconds',
        ]
        read_only_fields = ['id', 'started_at']
