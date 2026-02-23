"""
Taxonomy models for StoryAfrika.
Organizing stories by Country, Category, Theme, and Era per PRD requirements.
"""
from django.db import models
from django.utils.text import slugify
import uuid


class Country(models.Model):
    """
    Countries for story organization.

    PRD Requirements:
    - Country-based exploration
    - Country pages with curated list of stories
    - Cultural overview (not political/economic data)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    # Cultural context (not political/economic)
    cultural_overview = models.TextField(
        blank=True,
        help_text="Brief cultural context about this country (2-3 paragraphs)"
    )

    # Display
    flag_emoji = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'countries'
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def published_stories_count(self):
        """Return count of published stories from this country."""
        return self.stories.filter(status='published').count()


class Category(models.Model):
    """
    Content pillars/categories for stories.

    PRD Content Pillars:
    1. Stories of Life - Personal experiences, memories, everyday African life
    2. Culture and Traditions - Rituals, customs, languages, food, identity
    3. History and Memory - Historical narratives, forgotten figures, collective memory
    4. Journeys and Lessons - Growth, struggle, learning, transformation
    5. Creative Voices - Fiction, poetry, artistic expression in African contexts
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    description = models.TextField(
        help_text="What types of stories belong in this category"
    )

    # Display order
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def published_stories_count(self):
        """Return count of published stories in this category."""
        return self.stories.filter(status='published').count()


class Theme(models.Model):
    """
    Themes for cross-cutting story organization.

    Examples: Family, Identity, Migration, Youth, Elders, Resilience, Loss, Joy, etc.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'themes'
        verbose_name = 'Theme'
        verbose_name_plural = 'Themes'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def published_stories_count(self):
        """Return count of published stories with this theme."""
        return self.stories.filter(status='published').count()


class Era(models.Model):
    """
    Light time-period tagging for historical context.

    PRD Requirement: "Light era or time-period tagging"
    Examples: Pre-Colonial, Colonial Era, Post-Independence, 1960s-1980s, Contemporary, etc.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    description = models.TextField(
        blank=True,
        help_text="Brief description of this time period"
    )

    # Optional year range for sorting
    start_year = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'eras'
        verbose_name = 'Era'
        verbose_name_plural = 'Eras'
        ordering = ['start_year', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def published_stories_count(self):
        """Return count of published stories from this era."""
        return self.stories.filter(status='published').count()
