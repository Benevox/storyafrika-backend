"""
User models for StoryAfrika.
Aligned with PRD requirements for writer profiles and authentication.
"""
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with admin privileges."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_editor', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for StoryAfrika.

    PRD Requirements:
    - Email authentication (primary)
    - Google OAuth support
    - Writer profiles with biography
    - No public follower counts or engagement metrics
    """

    # Core fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255)

    # Profile fields
    full_name = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=100, unique=True, null=True, blank=True)

    # Writer profile fields
    biography = models.TextField(
        blank=True,
        help_text="Short biography for writer profile (1-2 paragraphs)"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )

    # Role and permissions
    is_writer = models.BooleanField(
        default=False,
        help_text="Approved to submit stories"
    )
    is_editor = models.BooleanField(
        default=False,
        help_text="Can review and approve stories"
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # OAuth fields
    google_id = models.CharField(max_length=255, blank=True, null=True, unique=True)

    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email

    def get_display_name(self):
        """Return the best available display name."""
        return self.full_name or self.username or self.email.split('@')[0]

    @property
    def published_stories_count(self):
        """Return count of published stories."""
        return self.stories.filter(status='published').count()


class WriterApplication(models.Model):
    """
    Model for writer applications.

    PRD Requirement: Writers must apply or be invited to contribute.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='writer_application'
    )

    # Application details
    writing_sample = models.TextField(
        help_text="A sample of your writing (300-500 words)"
    )
    motivation = models.TextField(
        help_text="Why do you want to write for StoryAfrika?"
    )

    # Review
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_applications'
    )
    review_notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'writer_applications'
        verbose_name = 'Writer Application'
        verbose_name_plural = 'Writer Applications'
        ordering = ['-created_at']

    def __str__(self):
        return f"Application from {self.user.email} - {self.status}"


class Bookmark(models.Model):
    """
    Bookmark model for readers to save stories.

    PRD Requirement: Ability to save and bookmark stories (no public counters).
    This is PRIVATE - no public bookmark counts shown.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    story = models.ForeignKey(
        'stories.Story',
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bookmarks'
        verbose_name = 'Bookmark'
        verbose_name_plural = 'Bookmarks'
        unique_together = ['user', 'story']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} bookmarked {self.story.title}"
