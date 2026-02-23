"""
Serializers for Editorial models.
"""
from rest_framework import serializers
from .models import StoryReview, FeaturedStory, ContentGuideline


class StoryReviewSerializer(serializers.ModelSerializer):
    """Serializer for Story Reviews."""

    reviewer_name = serializers.CharField(source='reviewer.full_name', read_only=True)
    story_title = serializers.CharField(source='story.title', read_only=True)

    class Meta:
        model = StoryReview
        fields = [
            'id',
            'story',
            'story_title',
            'reviewer',
            'reviewer_name',
            'status',
            'feedback',
            'meets_editorial_standards',
            'cultural_sensitivity_check',
            'originality_check',
            'completeness_check',
            'created_at',
            'updated_at',
            'completed_at',
        ]
        read_only_fields = [
            'id',
            'reviewer',
            'created_at',
            'updated_at',
            'completed_at',
        ]


class FeaturedStorySerializer(serializers.ModelSerializer):
    """Serializer for Featured Stories."""

    story_title = serializers.CharField(source='story.title', read_only=True)
    story_slug = serializers.CharField(source='story.slug', read_only=True)
    story_excerpt = serializers.CharField(source='story.excerpt', read_only=True)
    story_hero_image = serializers.ImageField(source='story.hero_image', read_only=True)
    author_name = serializers.CharField(source='story.author.full_name', read_only=True)

    class Meta:
        model = FeaturedStory
        fields = [
            'id',
            'story',
            'story_title',
            'story_slug',
            'story_excerpt',
            'story_hero_image',
            'author_name',
            'position',
            'custom_headline',
            'start_date',
            'end_date',
            'is_active',
            'is_currently_active',
        ]
        read_only_fields = ['id', 'is_currently_active']


class ContentGuidelineSerializer(serializers.ModelSerializer):
    """Serializer for Content Guidelines."""

    class Meta:
        model = ContentGuideline
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'good_examples',
            'bad_examples',
            'is_active',
            'order',
        ]
        read_only_fields = ['id', 'slug']
