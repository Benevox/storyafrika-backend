# StoryAfrika Backend (Django)

This is the Django backend for StoryAfrika - a digital storytelling platform for African stories, culture, and history.

## Architecture

This backend is built according to the StoryAfrika Product Requirements Document (PRD) with the following key features:

- **Editorial Review System**: Story submission, review, and approval workflow
- **Taxonomy Organization**: Stories organized by Country, Category, Theme, and Era
- **No Social Engagement**: No likes, followers, or public engagement metrics
- **Archive-Quality**: Built for long-term preservation and cultural importance

## Tech Stack

- **Framework**: Django 5.0.1 (Django 5.x)
- **Database**: PostgreSQL (SQLite for development)
- **API**: Django REST Framework
- **Authentication**: Email + Google OAuth
- **Image Processing**: Pillow
- **Content Processing**: Markdown with sanitization

## Project Structure

```
project-root/
├── manage.py                 # Django entrypoint
├── storyafrika_backend/      # Main Django project
│   ├── settings.py           # Project settings (env-driven via python-decouple)
│   ├── urls.py               # URL routing (/admin, /api, media)
│   └── wsgi.py               # WSGI configuration
├── api/                      # API URL router
│   └── urls.py               # JWT auth, DRF routers, API docs
├── users/                    # User authentication and profiles
│   ├── models.py             # User, WriterApplication, Bookmark
│   └── admin.py              # Admin configuration
├── stories/                  # Core story functionality
│   ├── models.py             # Story, ReadingSession
│   └── admin.py              # Admin configuration
├── taxonomy/                 # Content organization
│   ├── models.py             # Country, Category, Theme, Era
│   ├── admin.py              # Admin configuration
│   └── management/
│       └── commands/
│           └── seed_data.py  # Initial data seeding
├── editorial/                # Editorial workflow
│   ├── models.py             # StoryReview, FeaturedStory, etc.
│   └── admin.py              # Admin configuration
├── requirements.txt          # Python dependencies
├── .env.example              # Example environment configuration
└── .github/
    └── workflows/            # CI workflows for dev/staging/main
```

## Setup Instructions

### 1. Install Dependencies

**Recommended:** Use **Python 3.12** (CI uses 3.12; `psycopg2-binary` has wheels and avoids build issues).

```bash
pip install -r requirements.txt
```

**If you're on Windows with Python 3.13:** `psycopg2-binary` has no wheel and may fail to build. Use SQLite for local dev instead:

```bash
pip install -r requirements-dev.txt
```

Then in `.env` leave `DB_NAME` (and other `DB_*`) unset or commented out so the app uses SQLite.

### 2. Configure Environment

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# For PostgreSQL (recommended for production)
DB_NAME=storyafrika_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# For Development (SQLite is used by default if DB_NAME is not set)
# Just comment out the DB_* variables above
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Seed Initial Data

Populate categories, countries, themes, and eras:

```bash
python manage.py seed_data
```

This creates:
- 5 Content Pillars (Categories)
- 41 African Countries
- 30 Themes
- 6 Historical Eras

### 5. Create Superuser (Editor)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account. This account will have:
- `is_staff=True` for Django admin access
- `is_editor=True` for editorial review privileges

### 6. Run Development Server

```bash
python manage.py runserver
```

The server will start at `http://localhost:8000`

Key URLs:
- Django Admin: `http://localhost:8000/admin/`
- API base: `http://localhost:8000/api/`
- API docs (Swagger UI): `http://localhost:8000/api/docs/`

## Key Models

### User Management

**User**
- Email-based authentication
- Writer/Editor roles
- Profile with biography and avatar
- No public follower counts

**WriterApplication**
- Writers must apply to contribute
- Requires writing sample and motivation
- Editor review and approval

**Bookmark**
- Private story bookmarking
- No public bookmark counts

### Content Organization

**Category** (Content Pillars)
1. Stories of Life
2. Culture and Traditions
3. History and Memory
4. Journeys and Lessons
5. Creative Voices

**Country**
- 41 African countries
- Cultural overview (no political/economic data)
- Flag emoji for display

**Theme**
- Cross-cutting themes (Family, Identity, Migration, etc.)
- 30 predefined themes

**Era**
- Light time-period tagging
- Pre-Colonial to Contemporary
- 6 historical periods

### Story Management

**Story**
- Markdown content with HTML conversion
- Status workflow: draft → submitted → in_review → approved → published
- Rich metadata: category, country, themes, era
- Auto-calculated reading time
- No likes or engagement counters

**ReadingSession**
- Internal analytics only
- Track time spent reading
- Measure completion rates
- Not publicly visible

### Editorial Workflow

**StoryReview**
- Editorial feedback and revision requests
- Checklist for editorial standards
- Internal notes for editors

**StoryRevision**
- Version history for stories
- Track all changes

**FeaturedStory**
- Editor-curated homepage
- Manual curation (no algorithms)
- Positioning control

**ContentGuideline**
- Editorial standards documentation
- Good and bad examples
- Internal reference for editors

## Django Admin

Access the admin interface at `http://localhost:8000/admin`

Key admin features:

### Story Management
- Bulk publish/unpublish stories
- Feature/unfeature for homepage
- Filter by status, category, country
- Preview reading time and word count

### Editorial Dashboard
- Review pending story submissions
- Approve stories with checklist
- Request revisions with feedback
- Feature stories on homepage

### Taxonomy Management
- Add/edit countries, categories, themes, eras
- Reorder categories
- Toggle active/inactive status

### User Management
- Approve writer applications
- Assign editor roles
- View bookmarks (private)

## API Endpoints (Coming Next)

The REST API will be built using Django REST Framework with endpoints for:

- `/api/stories/` - Story CRUD and listing
- `/api/countries/` - Country-based browsing
- `/api/categories/` - Category browsing
- `/api/auth/` - Authentication (email + OAuth)
- `/api/submit/` - Story submission
- `/api/bookmarks/` - Personal bookmarks

## Development Guidelines

### Editorial Standards (Built-in)

All content must:
- Be written with intention and care
- Respect cultural and personal dignity
- Offer depth, reflection, or insight
- Be original or properly cited
- Read as a complete story, not a social post

### Disallowed Content

- Breaking news or developing stories
- Political propaganda
- Clickbait or SEO-driven content
- Hate speech
- AI-generated content
- Promotional content

### Design Principles (PRD-Aligned)

- **Archive-quality, not social-media-quality**
- **Calm, editorial, authoritative**
- **No vanity metrics** (likes, followers, view counts)
- **Preservation-focused** - built for decades, not years
- **Cultural institution** - not a startup

## Database Schema

See models in:
- `users/models.py`
- `stories/models.py`
- `taxonomy/models.py`
- `editorial/models.py`

All models use UUIDs as primary keys for better scalability and data portability.

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users
python manage.py test stories
python manage.py test editorial
python manage.py test taxonomy
```

## Deployment

### Requirements

- Python 3.11+
- PostgreSQL 13+
- S3-compatible storage (for media files)

### Environment Variables

Set these in production:

```env
DEBUG=False
SECRET_KEY=<strong-random-key>
ALLOWED_HOSTS=api.storyafrika.com

DB_NAME=storyafrika_prod
DB_USER=storyafrika_user
DB_PASSWORD=<secure-password>
DB_HOST=<db-host>
DB_PORT=5432

USE_S3=True
AWS_ACCESS_KEY_ID=<key>
AWS_SECRET_ACCESS_KEY=<secret>
AWS_STORAGE_BUCKET_NAME=storyafrika-media
```

### Recommended Hosting

- **Backend**: Fly.io or Railway
- **Database**: Managed PostgreSQL (Fly.io, Railway, or AWS RDS)
- **Media Storage**: AWS S3 or compatible service

## Contributing

When making changes:

1. Follow PRD requirements strictly
2. Maintain editorial-first approach
3. Never add social engagement features
4. Prioritize long-term preservation
5. Write migrations for all model changes

## License

See main repository LICENSE file.

## Support

For questions or issues, please contact the StoryAfrika team.
