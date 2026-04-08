# Gelaender Project Guidelines

## Project Overview
This project is a professional band website for Gelaender with a vanilla multi-page frontend, a FastAPI backend, and a PostgreSQL database.

## Architecture
- Keep frontend code in frontend/
- Keep backend code in backend/
- Keep database scripts and seeds in database/
- Keep docs in docs/

## Frontend Conventions
- Use semantic HTML structure and accessible landmarks.
- Use modular CSS with tokens in variables.css.
- Use progressive enhancement JavaScript.
- Build mobile-first and preserve a restrained DDR-inspired visual language.

## Backend Conventions
- Use FastAPI with clear split across routes, schemas, models, and services.
- Use Pydantic validation for request and response contracts.
- Use SQLAlchemy ORM for DB interactions.
- Use Alembic for migrations.

## Security Rules
- Use Stripe hosted checkout only.
- Never store card data locally.
- Never commit secrets.
- Use environment variables for runtime configuration.
- Validate all mutable inputs server-side.

## Review Expectations
- Prioritize findings first: bugs, risks, regressions, and missing tests.
- If no findings exist, state that and mention residual risks.
