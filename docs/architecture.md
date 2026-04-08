# Architecture

## Current State

- Frontend: multi-page vanilla HTML/CSS/JS in `frontend/`
- Backend: FastAPI app in `backend/app/`
- Database: PostgreSQL target with Alembic migration scaffold initialized

## Backend API Layout

- App entry: `backend/app/main.py`
- Health endpoint: `/health`
- Tour endpoint: `/api/tour-dates`
- Social links endpoint: `/api/social-links`

## Backend Layering

- `routes/` for HTTP routers and endpoint registration
- `schemas/` for Pydantic response and request contracts
- `models/` for SQLAlchemy ORM entities
- `services/` reserved for business logic (next steps)

## Next Targets

- Keep website-only API surface minimal and read-only
- Move tour/content data to persistent storage when needed
- Add production deployment checks and monitoring baseline
