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

## 4. Pipeline overview (live 2026-06-18)

The form is the first step of a four-stage pipeline:

1. **Browser form** (this page) — fills 22 fields, validates 10 critical ones, dispatches on Execute.
2. **GitHub Action** — `Supreamth/my-sprees/.github/workflows/project-start-intake.yml` (added 2026-06-18, commit `fba84d0`) listens for `repository_dispatch` event_type `project-start-intake` and creates an Issue with labels `project-start` + `project-start:<route>`.
3. **Issue** — the brief markdown is the Issue body. A bot comment tells reviewers how to import it.
4. **AI Project Tracker** — the `ingest-issues` CLI subcommand scans `Supreamth/my-sprees` for new `project-start`-labeled issues every ~5 min (cron) or on demand, and creates a project + initial task + `intake` trace event.

After ingestion, the project appears in the dashboard at:
https://tracker.sprees.net  (auth: `Authorization: Bearer *** change-this-token`)

## 5. End-to-end verification (2026-06-18)

| Stage | Evidence |
|-------|----------|
| Workflow deployed | https://github.com/Supreamth/my-sprees/blob/main/.github/workflows/project-start-intake.yml |
| Test Issue created | https://github.com/Supreamth/my-sprees/issues/35 (title "Project Start: [E2E TEST] Project Start Pipeline", labels `project-start` + `project-start:Discovery`) |
| Tracker ingested | Project #4 in `/api/dashboard` JSON: name="Project Start: [E2E TEST] Project Start Pipeline", status=active, description starts with "# Project Start Brief" |
| Tunnel live | https://tracker.sprees.net returns HTTP 200 with auth (14685 bytes, ~70ms via Cloudflare edge sin12/kul01) |

## 6. Live infra

- **Domain**: `sprees.net` NS moved from Hostinger parking to Cloudflare (2026-06-18)
- **Tunnel**: `mysprees-tracker` (UUID `0226fd55-77ce-412e-a0d8-fc7aed7d7616`) — 4 QUIC connections, all green
- **Service unit**: `/etc/systemd/system/cloudflared.service` — active + enabled, restart=on-failure
- **Auth token (placeholder)**: `change-this-token` — rotate before exposing to non-trusted users
