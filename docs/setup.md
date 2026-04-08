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
