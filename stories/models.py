"""
Story models for StoryAfrika.
Core storytelling functionality aligned with PRD requirements.
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
import uuid
import markdown
import bleach


class Story(models.Model):
    """
    Core Story model for StoryAfrika.

    PRD Requirements:
    - Long-form storytelling
    - Clean HTML or Markdown output
    - Metadata: category, country, theme, era
    - No engagement metrics (likes, comments)
    - Reading time calculation
    """

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted for Review'),
        ('in_review', 'In Review'),
        ('needs_revision', 'Needs Revision'),
        ('approved', 'Approved'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    # Core fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    # Content
    content = models.TextField(
        help_text="Story content in Markdown format"
    )
    content_html = models.TextField(
        blank=True,
        help_text="Auto-generated HTML from Markdown"
    )

    # Summary/excerpt
    excerpt = models.TextField(
        max_length=500,
        blank=True,
        help_text="Brief excerpt or summary (auto-generated if empty)"
    )

    # Author
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='stories'
    )

    # Taxonomy (PRD requirement: Category, Country, Theme, Era)
    category = models.ForeignKey(
        'taxonomy.Category',
        on_delete=models.PROTECT,
        related_name='stories'
    )
    country = models.ForeignKey(
        'taxonomy.Country',
        on_delete=models.PROTECT,
        related_name='stories'
    )
    themes = models.ManyToManyField(
        'taxonomy.Theme',
        related_name='stories',
        blank=True
    )
    era = models.ForeignKey(
        'taxonomy.Era',
        on_delete=models.SET_NULL,
        related_name='stories',
        null=True,
        blank=True
    )

    # Media
    hero_image = models.ImageField(
        upload_to='story_images/',
        blank=True,
        null=True
    )
    hero_image_caption = models.CharField(max_length=255, blank=True)

    # Status and publishing
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    # Editor curation
    is_featured = models.BooleanField(
        default=False,
        help_text="Featured on homepage by editors"
    )
    featured_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    # Reading metrics (internal only, not public)
    word_count = models.IntegerField(default=0)
    reading_time_minutes = models.IntegerField(default=0)

    class Meta:
        db_table = 'stories'
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['country', 'status']),
            models.Index(fields=['author', 'status']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Generate slug from title
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Story.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Convert Markdown to HTML
        if self.content:
            # Convert markdown to HTML
            html = markdown.markdown(
                self.content,
                extensions=['extra', 'nl2br', 'sane_lists']
            )
            # Sanitize HTML (allow only safe tags)
            allowed_tags = [
                'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'blockquote', 'ul', 'ol', 'li', 'a', 'img', 'code', 'pre',
            ]
            allowed_attributes = {
                'a': ['href', 'title'],
                'img': ['src', 'alt', 'title'],
            }
            self.content_html = bleach.clean(
                html,
                tags=allowed_tags,
                attributes=allowed_attributes,
                strip=True
            )

            # Calculate word count
            self.word_count = len(self.content.split())

            # Calculate reading time (average 225 words per minute)
            self.reading_time_minutes = max(1, round(self.word_count / 225))

            # Generate excerpt if not provided
            if not self.excerpt:
                # Get first 150 words of plain text
                words = self.content.split()[:150]
                self.excerpt = ' '.join(words) + ('...' if len(words) == 150 else '')

        # Set published_at timestamp when first published
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def get_related_stories(self, limit=4):
        """
        Get related stories based on category, country, and themes.
        """
        related = Story.objects.filter(
            status='published'
        ).exclude(
            id=self.id
        )

        # Prioritize stories with same category and country
        same_category_country = related.filter(
            category=self.category,
            country=self.country
        )[:limit]

        if same_category_country.count() >= limit:
            return same_category_country

        # Fill with stories from same country
        same_country = related.filter(
            country=self.country
        ).exclude(
            id__in=[s.id for s in same_category_country]
        )[:limit - same_category_country.count()]

        return list(same_category_country) + list(same_country)


class ReadingSession(models.Model):
    """
    Track reading sessions for meaningful metrics.

    PRD Success Metrics:
    - Average time spent reading stories
    - Number of stories saved or bookmarked
    - Percentage of returning readers

    This data is INTERNAL ONLY - never shown publicly.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name='reading_sessions'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reading_sessions'
    )

    # Session data
    session_id = models.CharField(max_length=255)  # For anonymous users
    started_at = models.DateTimeField(auto_now_add=True)
    completed_reading = models.BooleanField(default=False)
    time_spent_seconds = models.IntegerField(default=0)

    class Meta:
        db_table = 'reading_sessions'
        verbose_name = 'Reading Session'
        verbose_name_plural = 'Reading Sessions'
        indexes = [
            models.Index(fields=['story', 'started_at']),
            models.Index(fields=['user', 'started_at']),
        ]

    def __str__(self):
        return f"Reading session for {self.story.title}"
