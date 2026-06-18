# Setting Up the Project Start Intake Action

The Project Start Form dispatches a `repository_dispatch` event to **Supreamth/my-sprees** (a different repo from this docs site). You need to add a GitHub Actions workflow there to receive the event and create an Issue.

## Steps

1. **Copy `action-template.yml`** (from this same directory) to:
   ```
   Supreamth/my-sprees/.github/workflows/project-start-intake.yml
   ```

2. **Commit and push** that file to the `main` branch of `Supreamth/my-sprees`.

3. **Ensure the workflow has the right permissions.** The workflow uses `GITHUB_TOKEN` (automatic), which needs:
   - `issues: write`
   - `contents: read`

   These are the defaults for most repos. If your repo restricts default permissions, go to:
   `Settings → Actions → General → Workflow permissions` → set to "Read and write permissions".

4. **Set up a fine-grained PAT** for the form's Execute button:
   - Go to GitHub → Settings → Developer settings → Fine-grained personal access tokens
   - New token → Resource owner: `Supreamth` → Repository access: only `my-sprees`
   - Permissions: `Issues: Read and write`, `Contents: Read`, `Metadata: Read`
   - Copy the token and paste it in the **DEV ONLY** panel on the form (stored in `sessionStorage` only)

5. **Test**: Fill out the form → click "Generate Project Start Brief" → click "Execute → \<Route\>" → check `Supreamth/my-sprees/issues` for a new Issue with labels `project-start` and `project-start:<route>`.

## Pipeline overview

```
Browser form
  └─ POST /repos/Supreamth/my-sprees/dispatches  (repository_dispatch)
       └─ GitHub Action: project-start-intake.yml
            └─ Creates Issue with labels + body = brief markdown
                 └─ AI Project Tracker cron (ingest_issues command)
                      └─ SQLite DB → Dashboard at http://127.0.0.1:8765
```

## Troubleshooting

| Symptom | Likely cause |
|---------|--------------|
| 401 from dispatch | PAT missing or expired — re-enter in DEV ONLY panel |
| 404 from dispatch | PAT doesn't have access to `Supreamth/my-sprees`, or repo name is wrong |
| 422 from dispatch | Workflow file not yet pushed, or event_type mismatch |
| Issue not created | Check Actions tab in `Supreamth/my-sprees` for workflow run errors |
| Not in tracker | Cron hasn't fired yet, or `ingest_issues` command not set up — see tracker README |
