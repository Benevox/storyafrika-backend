# StoryAfrika API Testing Guide

This document lists all test scenarios for the StoryAfrika API. Run them in **Postman** to verify functionality. Each scenario specifies Method, URL, Headers, Body (where applicable), and Expected response.

**Assignees:** Tests are grouped by feature. Each scenario is assigned to **Zekeri** or **Alexin**. Both test complete feature areas.

| Feature | Zekeri | Alexin |
|---------|--------|--------|
| Auth & Users | Register, Login, Login invalid, Get me, Get me no token, Refresh, List users, List writers, Get writer | Register weak/mismatched, Login missing fields, Get me invalid token, Refresh invalid |
| Writer Applications | Create, List own, List as editor | Create missing fields, Non-editor scope |
| Stories | List (anon, writer), Create, Retrieve, Submit, Search, Related, Featured | List (editor), Pagination, Create non-writer, Retrieve invalid, Submit non-author/non-draft, Edit non-author, Search empty, Related empty, Featured date |
| Bookmarks | Create, List, Delete, Duplicate | Non-existent story, Scope check |
| Taxonomy | List all, Get country by slug | Inactive excluded, Invalid slug |
| Editorial | Featured, Guidelines | - |
| Reading Sessions | Create (auth, anon) | Anonymous without session |
| Admin | - | All smoke checks |

---

## 1. Introduction

### Testing with Postman

1. Start the Django server: `python manage.py runserver`
2. Use this doc as a checklist. Each scenario gives:
   - **Method** – HTTP verb (GET, POST, PUT, PATCH, DELETE)
   - **URL** – Full path (use `{{baseUrl}}` if you set it)
   - **Headers** – Content-Type, Authorization when needed
   - **Body** – Raw JSON for POST/PUT/PATCH
   - **Expected** – Status code and key response fields or error message

### Postman setup

1. Create an environment (e.g. "StoryAfrika Local").

2. Add variables:
   - `baseUrl` = `http://localhost:8000/api`
   - `access_token` = (leave empty; set from login/register response)
   - `refresh_token` = (leave empty; set from login/register response)

3. For requests that need auth, add header:
   - Key: `Authorization`
   - Value: `Bearer {{access_token}}`

4. For JSON bodies, add header:
   - Key: `Content-Type`
   - Value: `application/json`

### References

- [API_DOCUMENTATION.md](../API_DOCUMENTATION.md) – Full API reference
- Swagger UI: `http://localhost:8000/api/docs/`
- [README.md](../README.md) – Setup instructions

---

## 2. Test Data Prerequisites

### Seed taxonomy

```bash
python manage.py seed_data
```

Creates: 5 categories, 41 countries, 30 themes, 6 eras.

### Create test users

| User | Email | Role | Purpose |
|------|-------|------|---------|
| Editor | editor@storyafrika.test | Superuser, is_editor | Admin, approve/review |
| Writer | writer@storyafrika.test | is_writer=True | Create stories, submit |
| Plain user | user@storyafrika.test | Regular user | Bookmarks, apply to become writer |

Create via Django admin (`/admin/`) or `python manage.py createsuperuser` for editor, then promote others via admin.

### Create test data

- One **writer application** (pending) for user@storyafrika.test
- One **draft story** (author: writer)
- One **published story** (author: writer)
- One **featured story** (link to published story; create via admin)
- One **bookmark** (user bookmarks published story)

---

## 3. Authentication & Users

### Register

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/users/register/` |
| **Headers** | Content-Type: application/json |
| **Body** | `{"email": "newuser@storyafrika.test", "full_name": "New User", "password": "SecurePass123!", "password_confirm": "SecurePass123!"}` |
| **Expected** | 201 |
| **Response** | `user` (id, email, full_name, ...), `tokens` (refresh, access) |

**Django note:** Serializer validates password match and Django’s `validate_password` rules.

---

### Register – weak password

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/users/register/` |
| **Headers** | Content-Type: application/json |
| **Body** | `{"email": "new@test.com", "full_name": "New", "password": "123", "password_confirm": "123"}` |
| **Expected** | 400 |
| **Response** | `{"password": ["..."]}` (Django password validation errors) |

---

### Register – mismatched passwords

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/users/register/` |
| **Headers** | Content-Type: application/json |
| **Body** | `{"email": "new@test.com", "full_name": "New", "password": "SecurePass123!", "password_confirm": "DifferentPass123!"}` |
| **Expected** | 400 |
| **Response** | `{"password": ["Password fields didn't match."]}` |

---

### Login

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/users/login/` |
| **Headers** | Content-Type: application/json |
| **Body** | `{"email": "writer@storyafrika.test", "password": "<writer_password>"}` |
| **Expected** | 200 |
| **Response** | `user`, `tokens` (refresh, access) |

**Tip:** Save `tokens.access` and `tokens.refresh` to your Postman environment.

---

### Login – invalid credentials

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/users/login/` |
| **Headers** | Content-Type: application/json |
| **Body** | `{"email": "writer@storyafrika.test", "password": "wrongpassword"}` |
| **Expected** | 401 |
| **Response** | `{"error": "Invalid credentials."}` |

---

### Login – missing email

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/users/login/` |
| **Headers** | Content-Type: application/json |
| **Body** | `{"password": "somepass"}` |
| **Expected** | 400 |
| **Response** | `{"error": "Email and password are required."}` |

---

### Login – missing password

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/users/login/` |
| **Headers** | Content-Type: application/json |
| **Body** | `{"email": "user@example.com"}` |
| **Expected** | 400 |
| **Response** | `{"error": "Email and password are required."}` |

---

### Get current user (me)

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/users/me/` |
| **Headers** | Authorization: Bearer {{access_token}} |
| **Expected** | 200 |
| **Response** | User object (id, email, full_name, is_writer, is_editor, published_stories_count, ...) |

---

### Get me – no token

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/users/me/` |
| **Headers** | (none) |
| **Expected** | 401 |
| **Response** | `{"detail": "Authentication credentials were not provided."}` |

---

### Get me – invalid token

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/users/me/` |
| **Headers** | Authorization: Bearer invalid_token_here |
| **Expected** | 401 |
| **Response** | `{"detail": "Given token not valid for any token type", ...}` |

---

### Refresh access token

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/auth/token/refresh/` |
| **Headers** | Content-Type: application/json |
| **Body** | `{"refresh": "{{refresh_token}}"}` |
| **Expected** | 200 |
| **Response** | `{"access": "<new_access_token>"}` |

---

### Refresh – invalid token

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/auth/token/refresh/` |
| **Headers** | Content-Type: application/json |
| **Body** | `{"refresh": "invalid_refresh_token"}` |
| **Expected** | 401 |
| **Response** | `{"detail": "Token is invalid or expired", ...}` |

---

### List users (anonymous)

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/users/` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | Paginated list of active users. Staff see inactive users too. |

---

### List writers (public)

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/writers/` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | List of writers (full_name, username, biography, avatar, published_stories_count) |

---

### Get writer by username

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/writers/<username>/` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | Writer profile (id, full_name, username, biography, avatar, published_stories_count) |

Replace `<username>` with a real writer username (e.g. from seed data or admin).

---

## 4. Writer Applications

### Create writer application

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/writer-applications/` |
| **Headers** | Authorization: Bearer {{access_token}}, Content-Type: application/json |
| **Body** | `{"writing_sample": "A sample of my writing...", "motivation": "I want to share African stories."}` |
| **Expected** | 201 |
| **Response** | Application object (id, user, writing_sample, motivation, status: "pending", ...) |

**Django note:** `perform_create` ties the application to `request.user` automatically.

---

### Create application – missing required fields

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/writer-applications/` |
| **Headers** | Authorization: Bearer {{access_token}}, Content-Type: application/json |
| **Body** | `{}` |
| **Expected** | 400 |
| **Response** | `{"writing_sample": ["This field is required."], "motivation": ["This field is required."]}` |

---

### List own applications

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/writer-applications/` |
| **Headers** | Authorization: Bearer {{access_token}} |
| **Expected** | 200 |
| **Response** | List of applications for the current user only |

---

### List applications as editor

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/writer-applications/` |
| **Headers** | Authorization: Bearer {{access_token}} (editor token) |
| **Expected** | 200 |
| **Response** | List of all applications (from all users) |

---

### Non-editor sees only own applications

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/writer-applications/` |
| **Headers** | Authorization: Bearer {{access_token}} (plain user) |
| **Expected** | 200 |
| **Response** | List contains only this user's applications |

---

## 5. Stories

### List stories (anonymous – published only)

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/stories/` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | Paginated list; only `status: "published"` stories |

---

### List stories (writer – own + published)

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/stories/` |
| **Headers** | Authorization: Bearer {{access_token}} (writer token) |
| **Expected** | 200 |
| **Response** | List includes own stories (all statuses) plus all published stories |

---

### List stories (editor – all)

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/stories/` |
| **Headers** | Authorization: Bearer {{access_token}} (editor token) |
| **Expected** | 200 |
| **Response** | List includes draft, submitted, in_review, approved, published stories |

---

### List stories – pagination

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/stories/?page=2&page_size=5` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | Paginated object with `count`, `next`, `previous`, `results` (max 5 items) |

---

### Create story (writer)

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/stories/` |
| **Headers** | Authorization: Bearer {{access_token}}, Content-Type: application/json |
| **Body** | `{"title": "My Story", "content": "Story content in **Markdown**.", "excerpt": "Brief excerpt", "category": "<category_uuid>", "country": "<country_uuid>", "themes_ids": ["<theme_uuid>"], "era": "<era_uuid>"}` |
| **Expected** | 201 |
| **Response** | Story object (id, title, slug, status: "draft", ...) |

Replace `<category_uuid>`, `<country_uuid>`, etc. with IDs from `GET /api/categories/`, `GET /api/countries/` after seeding. `category` and `country` are required; `themes_ids` and `era` are optional.

**Django note:** `IsWriterOrReadOnly` – only writers can create. New stories start as `status: "draft"`.

---

### Create story – non-writer

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/stories/` |
| **Headers** | Authorization: Bearer {{access_token}} (plain user token) |
| **Body** | `{"title": "Story", "content": "Content", "category": "<uuid>", "country": "<uuid>"}` |
| **Expected** | 403 |
| **Response** | `{"detail": "You do not have permission to perform this action."}` |

---

### Retrieve story by slug

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/stories/<slug>/` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | Full story (content, content_html, author, category, country, themes, era, reading_time_minutes, ...) |

---

### Retrieve story – invalid slug

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/stories/non-existent-slug-12345/` |
| **Headers** | (none) |
| **Expected** | 404 |
| **Response** | `{"detail": "Not found."}` |

---

### Submit draft for review

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/stories/<slug>/submit/` |
| **Headers** | Authorization: Bearer {{access_token}} |
| **Expected** | 200 |
| **Response** | `{"message": "Story submitted for review.", "story": {...}}` with `status: "submitted"` |

Only the story author can submit. Story must be in `draft` status.

---

### Submit – non-author

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/stories/<other_user_slug>/submit/` |
| **Headers** | Authorization: Bearer {{access_token}} (different writer) |
| **Expected** | 403 |
| **Response** | `{"error": "You can only submit your own stories."}` |

---

### Submit – non-draft story

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/stories/<slug>/submit/` |
| **Headers** | Authorization: Bearer {{access_token}} |
| **Expected** | 400 |
| **Response** | `{"error": "Story is already submitted."}` (or "in_review", "approved", "published" depending on status) |

Use a story that is already `submitted` or `published`.

---

### Edit story – non-author

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | PUT |
| **URL** | `{{baseUrl}}/stories/<other_author_slug>/` |
| **Headers** | Authorization: Bearer {{access_token}} |
| **Body** | `{"title": "Hacked", "content": "...", "category": "<uuid>", "country": "<uuid>"}` |
| **Expected** | 403 |
| **Response** | `{"detail": "You do not have permission to perform this action."}` |

---

### Search stories

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/stories/search/?q=keyword` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | Paginated list of stories matching `q` in title, content, or excerpt |

---

### Search – empty query

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/stories/search/?q=` |
| **Headers** | (none) |
| **Expected** | 400 |
| **Response** | `{"error": "Please provide a search query."}` |

---

### Get related stories

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/stories/<slug>/related/` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | Array of up to 4 related stories (same category/country/themes) |

---

### Get related stories – none found

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/stories/<slug>/related/` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | `[]` (empty array if no related stories) |

---

### Get featured stories (via stories action)

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/stories/featured/` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | Array of story objects (currently active featured stories) |

---

### Featured stories – date window

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/stories/featured/` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | Only stories with `is_currently_active` true (within start_date/end_date, is_active) |

---

## 6. Bookmarks

### Create bookmark

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/bookmarks/` |
| **Headers** | Authorization: Bearer {{access_token}}, Content-Type: application/json |
| **Body** | `{"story": "<story_uuid>"}` |
| **Expected** | 201 |
| **Response** | Bookmark object (id, story, story_title, story_slug, created_at) |

---

### Create bookmark – non-existent story

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/bookmarks/` |
| **Headers** | Authorization: Bearer {{access_token}}, Content-Type: application/json |
| **Body** | `{"story": "00000000-0000-0000-0000-000000000000"}` |
| **Expected** | 400 or 404 |
| **Response** | Validation error (e.g. "Invalid pk" or "Story not found") |

---

### Create bookmark – duplicate

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/bookmarks/` |
| **Headers** | Authorization: Bearer {{access_token}}, Content-Type: application/json |
| **Body** | `{"story": "<already_bookmarked_story_uuid>"}` |
| **Expected** | 400 |
| **Response** | IntegrityError / validation error (Bookmark has `unique_together` on user + story) |

---

### List bookmarks

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/bookmarks/` |
| **Headers** | Authorization: Bearer {{access_token}} |
| **Expected** | 200 |
| **Response** | List of current user's bookmarks only |

---

### List bookmarks – scope check

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/bookmarks/` |
| **Headers** | Authorization: Bearer {{access_token}} |
| **Expected** | 200 |
| **Response** | List contains only bookmarks for this user; no other users' bookmarks |

---

### Delete bookmark

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | DELETE |
| **URL** | `{{baseUrl}}/bookmarks/<bookmark_id>/` |
| **Headers** | Authorization: Bearer {{access_token}} |
| **Expected** | 204 |

---

## 7. Taxonomy (Countries, Categories, Themes, Eras)

### List countries

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/countries/` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | List of active countries (id, name, slug, flag_emoji, published_stories_count) |

---

### List countries – inactive excluded

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/countries/` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | List excludes countries with `is_active=False` |

---

### Get country by slug

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/countries/<slug>/` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | Full country (cultural_overview, is_active, etc.) |

---

### Get country – invalid slug

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/countries/invalid-slug-xyz/` |
| **Headers** | (none) |
| **Expected** | 404 |
| **Response** | `{"detail": "Not found."}` |

---

### List categories

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/categories/` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | List of active categories (id, name, slug, description, published_stories_count) |

---

### List themes

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/themes/` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | List of active themes |

---

### List eras

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/eras/` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | List of active eras |

---

## 8. Editorial (Featured & Guidelines)

### Get featured stories (via editorial endpoint)

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/featured/` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | List of FeaturedStory objects (story, position, custom_headline, is_currently_active, ...) |

---

### Get content guidelines

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | GET |
| **URL** | `{{baseUrl}}/guidelines/` |
| **Headers** | (none) |
| **Expected** | 200 |
| **Response** | List of active guidelines (title, description, good_examples, bad_examples) |

---

## 9. Reading Sessions

### Create reading session (authenticated)

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/reading-sessions/` |
| **Headers** | Authorization: Bearer {{access_token}}, Content-Type: application/json |
| **Body** | `{"story": "<story_uuid>", "completed_reading": false, "time_spent_seconds": 0}` |
| **Expected** | 201 |
| **Response** | Reading session (id, story, started_at, completed_reading, time_spent_seconds) |

---

### Create reading session (anonymous)

**Assignee:** Zekeri

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/reading-sessions/` |
| **Headers** | Content-Type: application/json |
| **Body** | `{"story": "<story_uuid>", "completed_reading": false, "time_spent_seconds": 0}` |
| **Expected** | 201 |
| **Response** | Reading session with `session_id` (Django session key) |

**Django note:** The view creates a session if one doesn't exist, then stores `session_id` for anonymous users.

---

### Create reading session – anonymous without session

**Assignee:** Alexin

| Field | Value |
|-------|-------|
| **Method** | POST |
| **URL** | `{{baseUrl}}/reading-sessions/` |
| **Headers** | Content-Type: application/json (no cookies) |
| **Body** | `{"story": "<story_uuid>", "completed_reading": false, "time_spent_seconds": 0}` |
| **Expected** | 201 |
| **Response** | Reading session created; view creates session and stores session_id |

---

## 10. Admin UI (Smoke)

**Assignee:** Alexin

These are run in the Django admin (`/admin/`), not Postman. Brief smoke checks:

| Action | Steps | Expected |
|--------|-------|----------|
| Approve writer application | Admin > Writer applications > Select > Approve | Status changes to approved; user becomes writer |
| Publish story | Admin > Stories > Select > Change status to Published | Story visible to public |
| Feature story | Admin > Featured stories > Add > Select story, set position | Story appears in featured list |
| Add guideline | Admin > Content guidelines > Add | Guideline appears in API |

---

## 11. Error Handling Summary

| Endpoint | Condition | Expected Status | Response Shape |
|----------|-----------|-----------------|----------------|
| POST /users/login/ | Missing email/password | 400 | `{"error": "Email and password are required."}` |
| POST /users/login/ | Invalid credentials | 401 | `{"error": "Invalid credentials."}` |
| POST /users/register/ | Weak password | 400 | `{"password": ["..."]}` |
| POST /users/register/ | Password mismatch | 400 | `{"password": ["Password fields didn't match."]}` |
| GET /users/me/ | No token | 401 | `{"detail": "Authentication credentials were not provided."}` |
| GET /users/me/ | Invalid token | 401 | `{"detail": "Given token not valid for any token type", ...}` |
| POST /auth/token/refresh/ | Invalid refresh | 401 | `{"detail": "Token is invalid or expired", ...}` |
| POST /stories/ | Non-writer | 403 | `{"detail": "You do not have permission to perform this action."}` |
| POST /stories/{slug}/submit/ | Non-author | 403 | `{"error": "You can only submit your own stories."}` |
| POST /stories/{slug}/submit/ | Non-draft status | 400 | `{"error": "Story is already {status}."}` |
| PUT /stories/{slug}/ | Non-author | 403 | `{"detail": "You do not have permission to perform this action."}` |
| GET /stories/search/?q= | Empty q | 400 | `{"error": "Please provide a search query."}` |
| GET /stories/{slug}/ | Invalid slug | 404 | `{"detail": "Not found."}` |
| GET /countries/{slug}/ | Invalid slug | 404 | `{"detail": "Not found."}` |
| POST /writer-applications/ | Missing fields | 400 | `{"writing_sample": [...], "motivation": [...]}` |

---

## 12. Appendix

### Glossary

| Term | Meaning |
|------|---------|
| **draft** | Story status; not yet submitted for review |
| **submitted** | Story status; awaiting editorial review |
| **published** | Story status; visible to public |
| **writer** | User with `is_writer=True`; can create and submit stories |
| **editor** | User with `is_editor=True`; can review applications and stories |
| **slug** | URL-friendly identifier (e.g. `my-story-title`) |

### References

- [API_DOCUMENTATION.md](../API_DOCUMENTATION.md)
- Swagger UI: `http://localhost:8000/api/docs/`
- [README.md](../README.md)
