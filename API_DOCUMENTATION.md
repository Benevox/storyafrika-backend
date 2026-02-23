# StoryAfrika REST API Documentation

Base URL: `http://localhost:8000/api/`

## Authentication

StoryAfrika uses JWT (JSON Web Tokens) for authentication.

### Register a new user

```http
POST /api/users/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "full_name": "John Doe",
  "password": "securepassword123",
  "password_confirm": "securepassword123"
}
```

**Response:**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    ...
  },
  "tokens": {
    "refresh": "refresh_token",
    "access": "access_token"
  }
}
```

### Login

```http
POST /api/users/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response:** Same as registration

### Get current user

```http
GET /api/users/me/
Authorization: Bearer <access_token>
```

### Refresh access token

```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "refresh_token"
}
```

---

## Stories

### List published stories

```http
GET /api/stories/
```

**Query Parameters:**
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20)

**Response:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/stories/?page=2",
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "title": "Story Title",
      "slug": "story-title",
      "excerpt": "Brief excerpt...",
      "author": {
        "id": "uuid",
        "full_name": "Author Name",
        ...
      },
      "category": {...},
      "country": {...},
      "hero_image": "url",
      "status": "published",
      "published_at": "2026-02-08T10:00:00Z",
      "reading_time_minutes": 5
    }
  ]
}
```

### Get story detail

```http
GET /api/stories/{slug}/
```

**Response:**
```json
{
  "id": "uuid",
  "title": "Story Title",
  "slug": "story-title",
  "content": "Full markdown content...",
  "content_html": "<p>Rendered HTML...</p>",
  "excerpt": "Brief excerpt...",
  "author": {...},
  "category": {...},
  "country": {...},
  "themes": [...],
  "era": {...},
  "hero_image": "url",
  "hero_image_caption": "Caption",
  "status": "published",
  "published_at": "2026-02-08T10:00:00Z",
  "word_count": 1200,
  "reading_time_minutes": 5
}
```

### Create a story (Writers only)

```http
POST /api/stories/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "My Story",
  "content": "Story content in **Markdown**...",
  "excerpt": "Optional excerpt",
  "category": "category-uuid",
  "country": "country-uuid",
  "themes_ids": ["theme-uuid-1", "theme-uuid-2"],
  "era": "era-uuid",
  "hero_image_caption": "Image caption"
}
```

### Update a story

```http
PUT /api/stories/{slug}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content...",
  ...
}
```

### Submit story for review

```http
POST /api/stories/{slug}/submit/
Authorization: Bearer <access_token>
```

### Get featured stories

```http
GET /api/stories/featured/
```

### Search stories

```http
GET /api/stories/search/?q=keyword
```

### Get related stories

```http
GET /api/stories/{slug}/related/
```

---

## Countries

### List all countries

```http
GET /api/countries/
```

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Nigeria",
    "slug": "nigeria",
    "flag_emoji": "🇳🇬",
    "published_stories_count": 42
  },
  ...
]
```

### Get country detail

```http
GET /api/countries/{slug}/
```

**Response:**
```json
{
  "id": "uuid",
  "name": "Nigeria",
  "slug": "nigeria",
  "cultural_overview": "Brief cultural context...",
  "flag_emoji": "🇳🇬",
  "is_active": true,
  "published_stories_count": 42
}
```

### Get stories by country

```http
GET /api/countries/{slug}/stories/
```

**Query Parameters:**
- `page` - Page number

---

## Categories (Content Pillars)

### List all categories

```http
GET /api/categories/
```

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Stories of Life",
    "slug": "stories-of-life",
    "description": "Personal experiences...",
    "published_stories_count": 28
  },
  ...
]
```

### Get category detail

```http
GET /api/categories/{slug}/
```

### Get stories by category

```http
GET /api/categories/{slug}/stories/
```

---

## Themes

### List all themes

```http
GET /api/themes/
```

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Family",
    "slug": "family"
  },
  ...
]
```

### Get stories by theme

```http
GET /api/themes/{slug}/stories/
```

---

## Eras

### List all eras

```http
GET /api/eras/
```

**Response:**
```json
[
  {
    "id": "uuid",
    "name": "Pre-Colonial",
    "slug": "pre-colonial",
    "start_year": null,
    "end_year": 1800
  },
  ...
]
```

### Get stories by era

```http
GET /api/eras/{slug}/stories/
```

---

## Writers

### List all writers

```http
GET /api/writers/
```

**Response:**
```json
[
  {
    "id": "uuid",
    "full_name": "Writer Name",
    "username": "writer_username",
    "biography": "Writer bio...",
    "avatar": "url",
    "date_joined": "2026-01-01T00:00:00Z",
    "published_stories_count": 5
  },
  ...
]
```

### Get writer profile

```http
GET /api/writers/{username}/
```

---

## Writer Applications

### Apply to become a writer

```http
POST /api/writer-applications/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "writing_sample": "Your writing sample (300-500 words)...",
  "motivation": "Why you want to write for StoryAfrika..."
}
```

### Get my applications

```http
GET /api/writer-applications/
Authorization: Bearer <access_token>
```

---

## Bookmarks

### List my bookmarks

```http
GET /api/bookmarks/
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "id": "uuid",
    "story": "story-uuid",
    "story_title": "Story Title",
    "story_slug": "story-slug",
    "created_at": "2026-02-08T10:00:00Z"
  },
  ...
]
```

### Add bookmark

```http
POST /api/bookmarks/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "story": "story-uuid"
}
```

### Remove bookmark

```http
DELETE /api/bookmarks/{id}/
Authorization: Bearer <access_token>
```

---

## Content Guidelines

### List editorial guidelines

```http
GET /api/guidelines/
```

**Response:**
```json
[
  {
    "id": "uuid",
    "title": "Guideline Title",
    "slug": "guideline-slug",
    "description": "Detailed explanation...",
    "good_examples": "Examples...",
    "bad_examples": "Counter-examples...",
    "is_active": true,
    "order": 1
  },
  ...
]
```

---

## Reading Sessions (Internal Analytics)

### Create reading session

```http
POST /api/reading-sessions/
Content-Type: application/json

{
  "story": "story-uuid",
  "completed_reading": false,
  "time_spent_seconds": 0
}
```

### Update reading session

```http
PATCH /api/reading-sessions/{id}/
Content-Type: application/json

{
  "completed_reading": true,
  "time_spent_seconds": 300
}
```

---

## Interactive API Documentation

Visit these URLs for interactive API exploration:

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. In production, consider adding rate limiting to prevent abuse.

---

## CORS

CORS is enabled for:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

Configure additional origins in `.env` file:
```
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

---

## Pagination

All list endpoints use pagination with:
- Default page size: 20
- Max page size: 100

Access next/previous pages:
```http
GET /api/stories/?page=2
```

---

## Filtering & Searching

### Search stories
```http
GET /api/stories/search/?q=keyword
```

### Filter by status (Editors only)
```http
GET /api/stories/?status=published
```

---

## Best Practices

1. **Always use HTTPS in production**
2. **Store JWT tokens securely** (not in localStorage)
3. **Refresh tokens before expiry** (60 minutes for access tokens)
4. **Handle 401 responses** by refreshing token or re-authenticating
5. **Respect pagination** - don't request all items at once
6. **Cache responses** where appropriate
7. **Include proper error handling**

---

## Example: Complete Registration + Story Creation Flow

```javascript
// 1. Register
const registerResponse = await fetch('http://localhost:8000/api/users/register/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'writer@example.com',
    full_name: 'Jane Writer',
    password: 'securepass123',
    password_confirm: 'securepass123'
  })
});
const { user, tokens } = await registerResponse.json();

// 2. Apply to become a writer
const applicationResponse = await fetch('http://localhost:8000/api/writer-applications/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${tokens.access}`
  },
  body: JSON.stringify({
    writing_sample: 'My writing sample...',
    motivation: 'I want to share African stories...'
  })
});

// (Wait for approval by editor)

// 3. Create a story
const storyResponse = await fetch('http://localhost:8000/api/stories/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${tokens.access}`
  },
  body: JSON.stringify({
    title: 'My First Story',
    content: 'Story content in **Markdown**...',
    category: 'category-uuid',
    country: 'country-uuid'
  })
});
const story = await storyResponse.json();

// 4. Submit for review
const submitResponse = await fetch(`http://localhost:8000/api/stories/${story.slug}/submit/`, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${tokens.access}` }
});
```

---

For more details, visit the interactive documentation at `/api/docs/`.
