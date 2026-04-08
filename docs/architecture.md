# Architecture

## Current State

- Frontend: multi-page vanilla HTML/CSS/JS in `frontend/`
- Backend: FastAPI app in `backend/app/`
- Database: PostgreSQL target with Alembic migration scaffold initialized

## Backend API Layout

- App entry: `backend/app/main.py`
- Health endpoint: `/health`
- Products endpoint: `/api/products`
- Tour endpoint: `/api/tour-dates`
- Social links endpoint: `/api/social-links`

## Backend Layering

- `routes/` for HTTP routers and endpoint registration
- `schemas/` for Pydantic response and request contracts
- `models/` for SQLAlchemy ORM entities
- `services/` reserved for business logic (next steps)

## Next Day 2 Targets

- Add order request/response schemas and order route skeleton
- Move hardcoded sample data into service layer stubs
- Create first autogenerate-ready migration from model metadata
