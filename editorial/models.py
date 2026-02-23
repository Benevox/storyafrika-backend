"""
Editorial workflow models for StoryAfrika.
Manages story submission, review, and revision process per PRD requirements.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class StoryReview(models.Model):
    """
    Editorial review for submitted stories.

    PRD Requirements:
    - Editorial feedback and revision support
    - Structured submission workflow
    - Editor-reviewed publishing workflow
    """

    REVIEW_STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('in_progress', 'In Progress'),
        ('approved', 'Approved'),
        ('needs_revision', 'Needs Revision'),
        ('rejected', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    story = models.ForeignKey(
        'stories.Story',
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='story_reviews'
    )

    # Review details
    status = models.CharField(
        max_length=20,
        choices=REVIEW_STATUS_CHOICES,
        default='pending'
    )

    # Editorial feedback
    feedback = models.TextField(
        blank=True,
        help_text="Detailed feedback for the writer"
    )

    # Editorial checklist
    meets_editorial_standards = models.BooleanField(
        default=False,
        help_text="Does the story meet StoryAfrika's editorial standards?"
    )
    cultural_sensitivity_check = models.BooleanField(
        default=False,
        help_text="Story respects cultural and personal dignity"
    )
    originality_check = models.BooleanField(
        default=False,
        help_text="Content is original or properly cited"
    )
    completeness_check = models.BooleanField(
        default=False,
        help_text="Story reads as complete, not a social post"
    )

    # Internal notes (not shared with writer)
    internal_notes = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'story_reviews'
        verbose_name = 'Story Review'
        verbose_name_plural = 'Story Reviews'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['story', 'status']),
            models.Index(fields=['reviewer', 'status']),
        ]

    def __str__(self):
        return f"Review of {self.story.title} by {self.reviewer}"

    def save(self, *args, **kwargs):
        # Set completed_at when review is finished
        if self.status in ['approved', 'needs_revision', 'rejected'] and not self.completed_at:
            self.completed_at = timezone.now()

        super().save(*args, **kwargs)


class StoryRevision(models.Model):
    """
    Track revisions made to stories during editorial process.

    Maintains history of changes for writer accountability and editorial transparency.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    story = models.ForeignKey(
        'stories.Story',
        on_delete=models.CASCADE,
        related_name='revisions'
    )

    review = models.ForeignKey(
        StoryReview,
        on_delete=models.CASCADE,
        related_name='revisions',
        null=True,
        blank=True
    )

    # Snapshot of content at revision time
    title = models.CharField(max_length=255)
    content = models.TextField()
    revision_notes = models.TextField(
        blank=True,
        help_text="Notes about what was changed in this revision"
    )

    # Metadata
    revised_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='story_revisions'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'story_revisions'
        verbose_name = 'Story Revision'
        verbose_name_plural = 'Story Revisions'
        ordering = ['-created_at']

    def __str__(self):
        return f"Revision of {self.story.title} at {self.created_at}"


class FeaturedStory(models.Model):
    """
    Editor-curated featured stories for homepage.

    PRD Requirements:
    - Curated homepage managed by editors
    - No algorithmic feeds
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    story = models.ForeignKey(
        'stories.Story',
        on_delete=models.CASCADE,
        related_name='featured_placements'
    )

    # Curation
    featured_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='featured_stories'
    )

    position = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )

    # Optional custom headline for featured placement
    custom_headline = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional custom headline for homepage"
    )

    # Active period
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Leave empty for indefinite featuring"
    )

    is_active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'featured_stories'
        verbose_name = 'Featured Story'
        verbose_name_plural = 'Featured Stories'
        ordering = ['position', '-created_at']
        indexes = [
            models.Index(fields=['is_active', 'position']),
        ]

    def __str__(self):
        return f"Featured: {self.story.title}"

    @property
    def is_currently_active(self):
        """Check if feature is currently active based on dates."""
        now = timezone.now()
        if not self.is_active:
            return False
        if self.start_date > now:
            return False
        if self.end_date and self.end_date < now:
            return False
        return True


class EditorialNote(models.Model):
    """
    Internal notes for editorial team coordination.

    Used for editor-to-editor communication about stories, writers, or editorial decisions.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    story = models.ForeignKey(
        'stories.Story',
        on_delete=models.CASCADE,
        related_name='editorial_notes',
        null=True,
        blank=True
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='editorial_notes_created'
    )

    note = models.TextField()

    # Priority for urgent items
    is_urgent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'editorial_notes'
        verbose_name = 'Editorial Note'
        verbose_name_plural = 'Editorial Notes'
        ordering = ['-created_at']

    def __str__(self):
        story_ref = f" - {self.story.title}" if self.story else ""
        return f"Editorial note by {self.author}{story_ref}"


class ContentGuideline(models.Model):
    """
    Editorial standards and content guidelines.

    PRD Editorial Standards:
    - Written with intention and care
    - Respects cultural and personal dignity
    - Offers depth, reflection, or insight
    - Original or properly cited
    - Complete story, not a social post
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    description = models.TextField(
        help_text="Detailed explanation of this guideline"
    )

    # Examples
    good_examples = models.TextField(
        blank=True,
        help_text="Examples of content that follows this guideline"
    )
    bad_examples = models.TextField(
        blank=True,
        help_text="Examples of content that violates this guideline"
    )

    # Metadata
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='guidelines_created'
    )

    class Meta:
        db_table = 'content_guidelines'
        verbose_name = 'Content Guideline'
        verbose_name_plural = 'Content Guidelines'
        ordering = ['order', 'title']

    def __str__(self):
        return self.title
