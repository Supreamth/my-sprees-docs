# Project Start Form — Quick Start

## 1. Open the form

Open `index.html` in a browser, or visit the live URL:
https://supreamth.github.io/my-sprees-docs/project-start/

## 2. Fill mandatory fields

Fields marked **\*** are critical. The form will not let you Execute until all of these are filled:

- Project name
- Business owner
- Problem
- User / customer (who experiences the problem)
- Evidence
- Impact / cost
- Project goal
- MVP scope
- Non-goals / out of scope
- Acceptance criteria

Select a **Requested next phase** (Discovery, PRD, UX Design, Architecture, Delivery Planning, or Implementation).

## 3. Set your PAT (one time per session)

Open the **DEV ONLY** panel at the top of the form and paste your fine-grained GitHub PAT.  
The token is stored in `sessionStorage` only — it clears when you close the tab.

See `action-instructions.md` for how to create the PAT.

## 4. Generate → Execute

Click **Generate Project Start Brief** — the form validates all critical fields and generates a Markdown brief.

Then click **Execute → \<Route\>** to dispatch the brief as a `repository_dispatch` event to `Supreamth/my-sprees`.

## 5. See the issue

A GitHub Action in `Supreamth/my-sprees` creates an Issue with:
- Title: `Project Start: <project name>`
- Body: the full brief markdown
- Labels: `project-start` and `project-start:<route>`

## 6. See it in the tracker

Within ~5 minutes the AI Project Tracker cron imports the Issue and it appears in the dashboard at:

```
http://127.0.0.1:8765
```

To import immediately:

```bash
cd /root/ai-project-tracker
PYTHONPATH=src python3 -m ai_tracker.cli ingest-issues \
  --label project-start \
  --target-repo Supreamth/my-sprees \
  --db data/tracker.db
```

## Files in this directory

| File | Purpose |
|------|---------|
| `index.html` | The Project Start Form (static, GitHub Pages) |
| `action-template.yml` | Copy this to `Supreamth/my-sprees/.github/workflows/project-start-intake.yml` |
| `action-instructions.md` | Step-by-step setup guide for the receiving Action |
| `README.md` | This file |
