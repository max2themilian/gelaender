# Daily Workflow

This is the recommended daily development workflow for the Gelaender project.

## 1. Open Project

1. Open VS Code in `C:\dev\gelaender`.
2. Open a terminal in VS Code.

## 2. Start Local Frontend Preview

```powershell
Set-Location frontend
python -m http.server 5500
```

What this gives you:

- Frontend at `http://127.0.0.1:5500`

## 3. Daily Browser Checks

Open in Firefox:

1. `http://127.0.0.1:5500`
2. `http://127.0.0.1:5500/music.html`
3. `http://127.0.0.1:5500/tour.html`
4. `http://127.0.0.1:5500/contact.html`

## 4. During Development

1. Edit code in VS Code.
2. Refresh browser tabs.
3. Verify embeds, links, and navigation.
4. Watch the browser console for CSP or embed errors.

## 5. Stop Preview Cleanly

In the running terminal, press `Ctrl + C`.

## 6. Agent Workflow

Use the custom agents as a pipeline, not randomly.

1. `Architect Agent` for structural or scope decisions.
2. `Frontend Build Agent` for pages, CSS, or JS changes.
3. `Design Agent` for visual direction and layout work.
4. `Security Review Agent` before release-sensitive changes.
5. `QA Release Agent` before pushing major edits live.

## 7. Quality Gates Before Commit

1. Local static preview works.
2. No secret values are committed.
3. Docs are updated when behavior changes.
4. One clear commit message for one coherent change set.
