# Setup

## Local backend

1. Create and activate a Python virtual environment.
2. Install dependencies from backend/requirements.txt.
3. Run backend: python -m uvicorn run:app --reload --app-dir backend --host 127.0.0.1 --port 8000

## Local frontend

1. In a second terminal: Set-Location frontend
2. Run: python -m http.server 5500

## Day 2 migration bootstrap

1. Initialize Alembic once: python -m alembic init backend/alembic

## Google Calendar for Shows

1. Create a dedicated Google Calendar for shows.
2. Set calendar visibility to public.
3. In Google Calendar settings, copy the public ICS URL.
4. Put this value into .env:
   - GOOGLE_CALENDAR_ICS_URL
5. Restart backend and verify:
   - GET /api/tour-dates returns upcoming events from Google Calendar.

Optional (if you later have Google Cloud access):

- GOOGLE_CALENDAR_ID and GOOGLE_API_KEY can also be used.
