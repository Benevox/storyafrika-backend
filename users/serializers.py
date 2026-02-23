"""
Serializers for User models.
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, WriterApplication, Bookmark


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    published_stories_count = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'full_name',
            'username',
            'biography',
            'avatar',
            'is_writer',
            'is_editor',
            'date_joined',
            'published_stories_count',
        ]
        read_only_fields = ['id', 'is_writer', 'is_editor', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'password_confirm']

    def validate(self, attrs):
        """Validate password confirmation."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs

    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ''),
        )
        return user


class WriterProfileSerializer(serializers.ModelSerializer):
    """Detailed serializer for writer profiles."""

    published_stories_count = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
            'username',
            'biography',
            'avatar',
            'date_joined',
            'published_stories_count',
        ]
        read_only_fields = ['id', 'date_joined']


class WriterApplicationSerializer(serializers.ModelSerializer):
    """Serializer for Writer Applications."""

    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = WriterApplication
        fields = [
            'id',
            'user',
            'user_email',
            'user_name',
            'writing_sample',
            'motivation',
            'status',
            'review_notes',
            'created_at',
            'updated_at',
            'reviewed_at',
        ]
        read_only_fields = [
            'id',
            'user',
            'status',
            'review_notes',
            'created_at',
            'updated_at',
            'reviewed_at',
        ]


class BookmarkSerializer(serializers.ModelSerializer):
    """Serializer for Bookmarks."""

    story_title = serializers.CharField(source='story.title', read_only=True)
    story_slug = serializers.CharField(source='story.slug', read_only=True)

    class Meta:
        model = Bookmark
        fields = [
            'id',
            'story',
            'story_title',
            'story_slug',
            'created_at',
        ]
        read_only_fields = ['id', 'user', 'created_at']
