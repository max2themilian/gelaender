# Daily Workflow

This is the recommended daily development workflow for the Gelaender project.

## 1. Open Project

1. Open VS Code in `C:\dev\gelaender`.
2. Open a terminal in VS Code.

## 2. Activate Virtual Environment

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If activation worked, you usually see `(.venv)` in the prompt.

## 3. Start Backend (FastAPI)

```powershell
python -m uvicorn run:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```

What this gives you:

- API server at `http://127.0.0.1:8000`
- Auto-reload on code changes

## 4. Start Frontend (Second Terminal)

```powershell
Set-Location frontend
python -m http.server 5500
```

What this gives you:

- Frontend at `http://127.0.0.1:5500`

## 5. Daily Browser Checks

Open in Firefox:

1. `http://127.0.0.1:8000/health` (backend alive)
2. `http://127.0.0.1:8000/docs` (Swagger UI for API testing)
3. `http://127.0.0.1:5500` (frontend)

## 6. During Development

1. Edit code in VS Code.
2. Refresh browser tabs.
3. Test API endpoints in Swagger (`/docs`).
4. Watch terminal logs for errors.

## 7. Stop Services Cleanly

In each running terminal, press:

- `Ctrl + C`

## 8. When You Add Python Packages

```powershell
pip install <package-name>
```

Then update dependency tracking in a controlled way.

## Quick Understanding

- `venv` isolates project Python packages.
- FastAPI is the backend API runtime.
- Swagger (`/docs`) is interactive API documentation.
- Firefox is only the client to open URLs.

## 9. Agent Workflow (Professional Mode)

Use the custom agents as a pipeline, not randomly.

### 9.1 Agent Roles

1. `Architect Agent`

- Use before structural or scope decisions.
- Output: decision, trade-offs, and dependency order.

2. `Backend Build Agent`

- Use for API routes, schemas, validation, and service orchestration.

3. `Data Agent`

- Use for SQLAlchemy model evolution, migrations, and indexing decisions.

4. `Frontend Build Agent`

- Use for semantic pages, CSS system work, and JS integration.

5. `Design Agent`

- Use for visual direction, tokens, and accessibility-aware UI decisions.

6. `Security Review Agent`

- Use before merging larger backend or deployment-facing changes.
- Output must prioritize findings by severity.

7. `QA Release Agent`

- Use at checkpoint boundaries to verify pass/fail readiness.

### 9.2 Daily Agent Sequence

1. Architect check (only if structure changed)
2. Build agent for the active layer (backend/frontend/data)
3. Security review for sensitive changes
4. QA gate before commit

### 9.3 Quality Gates Before Commit

1. Import and syntax checks are clean.
2. Relevant endpoints return expected status codes.
3. No secret values are committed.
4. Docs are updated when behavior changes.
5. One clear commit message for one coherent change set.

### 9.4 Example Prompt Pattern

Use this structure for each agent call:

1. Goal
2. Scope (files/features affected)
3. Constraints (security, style, no overengineering)
4. Required output format

Short prompt template:

```text
Goal: <what we need done>
Scope: <which feature/files>
Constraints: keep modular, validate inputs, no secrets, minimal diff
Output: summary + changed files + verification steps
```

### 9.5 Current Project Rule

For Gelaender, default to this order for new backend work:

1. Architect Agent (if design choice exists)
2. Backend Build Agent
3. Data Agent (if models/migrations touched)
4. Security Review Agent
5. QA Release Agent

## 10. Local Google Calendar Test Flow

Use this flow to verify shows sync from public ICS locally without Google Cloud billing.

1. Ensure `.env` in workspace root contains:
   - `GOOGLE_CALENDAR_ICS_URL=https://calendar.google.com/calendar/ical/<calendar-id>/public/basic.ics`
2. Start backend from workspace root:

```powershell
Set-Location backend
.\scripts\run-local-api.ps1
```

3. In a second terminal, run contract validation:

```powershell
Set-Location backend
.\scripts\validate-tour-dates.ps1 -BaseUrl http://127.0.0.1:8000
```

4. Optional direct endpoint check:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/tour-dates | ConvertTo-Json -Depth 4
```

5. Success criteria:
   - Response is a non-empty array.
   - Events contain `event_name`, `date`, `city`, `venue_name`, `ticket_url`.
   - Ticket URL is taken from `tickets: <link>` in event description when present.
