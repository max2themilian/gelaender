# Gelaender

Professional full-stack band website for Gelaender.

## Stack

- Frontend: HTML, CSS, JavaScript
- Backend: FastAPI (Python)
- Database: PostgreSQL

## Day 1 Status

- Workspace instructions and reusable agents are configured.
- Repository skeleton is in progress.

## Developer Workflow

- Daily runbook: [docs/daily-workflow.md](docs/daily-workflow.md)

## Local ICS Testing (No Google API Key)

Run from the workspace root in PowerShell.

1. Start backend with local development defaults and an ICS feed URL:

```powershell
cd backend
.\scripts\run-local-api.ps1 -IcsUrl "https://calendar.google.com/calendar/ical/<your-public-calendar-id>/public/basic.ics"
```

2. In a second PowerShell window, validate the API response contract:

```powershell
cd backend
.\scripts\validate-tour-dates.ps1 -BaseUrl "http://127.0.0.1:8000"
```

Notes:

- The backend route keeps the existing order: ICS first, then Google API key source, then static fallback data.
- This workflow does not require `GOOGLE_API_KEY`.
- For convenience, `run-local-api.ps1` sets process-local defaults when env values are missing.
