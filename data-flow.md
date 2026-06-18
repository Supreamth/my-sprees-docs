# E2E Data Flow · Project Start → Tracker

End-to-end data flow diagram ตั้งแต่กรอก Project Start Form บน GitHub Pages จนถึง Issue บน GitHub และ row ใน AI Project Tracker dashboard

ดู interactive diagram (SVG) ที่: https://supreamth.github.io/my-sprees-docs/data-flow/

## ภาพรวม

Pipeline นี้เชื่อม static form บน GitHub Pages เข้ากับ AI Project Tracker dashboard โดยไม่ต้องมี backend hosting ใช้ `repository_dispatch` + GitHub Action + cron importer เป็น 4 ชั้นหลัก ข้อมูลทุกชั้น idempotent — รันซ้ำได้ไม่ซ้ำ row

| Endpoint | Event type | Target repo | Tracker |
|---|---|---|---|
| `/dispatches` | `project-start-intake` | `Supreamth/my-sprees` | `http://127.0.0.1:8765` |

## 4 ชั้นหลักของ Pipeline

### Layer 1 — Form (Browser)
- Project Start Form บน GitHub Pages — static HTML + JS
- 23 fields · 6 หมวด (Identity / Problem / Goal / Workflow / Data / Acceptance)
- 9 critical บังคับกรอก — client-side validate block dispatch
- `sessionStorage` เก็บ PAT (clear ตอนปิด tab)
- `fetch()` POST → `api.github.com/repos/.../dispatches`
- route selector เลือก Discovery / PRD / UX / Architecture / Delivery / Planning / Implementation

### Layer 2 — Dispatch (GitHub API)
- `event_type` = `project-start-intake`
- `client_payload` ≤ 10 KB (brief markdown + route + requester + ts)
- Rate limit: 5000 dispatches / repo / hour
- PAT scope: `contents:read` + `metadata:read` เท่านั้น
- Fire-and-forget — ไม่รู้ผลจาก form ต้องรอ Action สร้าง Issue แล้วเช็คที่ issue list

### Layer 3 — Action Receiver
- ไฟล์: `Supreamth/my-sprees/.github/workflows/project-start-intake.yml`
- Trigger: `repository_dispatch: [project-start-intake]`
- Permissions: `issues: write`, `contents: read`
- Parse `client_payload` → ดึง `Project name:` ด้วย regex
- Create Issue: title = `Project Start: <name>`
- Labels: `[project-start, project-start:<route>]`
- Post comment พร้อมคำสั่ง ingest แบบ manual

### Layer 4 — Tracker (Host + SQLite)
- Cron: `*/5 * * * *` — ยังไม่ได้ติดตั้ง (ทำ manual ได้)
- CLI: `ai_tracker.cli ingest-issues --label project-start`
- Source: `gh issue list --label project-start --state open --json`
- Idempotency: `external_source='github_issue'` + `external_id=str(number)`
- Server: `ai_tracker.server` port 8765 + Bearer auth
- Tunnel: `tracker.sprees.net` via Cloudflare (pending login)

## Payload contract

| Field | Type | ตัวอย่าง | กฎ |
|---|---|---|---|
| `event_type` | string | `project-start-intake` | ตรงกับ `on.repository_dispatch.types` |
| `client_payload.route` | string | `Architecture` | ใช้เป็น suffix ของ label `project-start:<route>` |
| `client_payload.brief_markdown` | string | 9 critical + เพิ่มเติม | ≤ 10 KB — first line ต้องขึ้นต้นด้วย `- Project name: ...` |
| `client_payload.requester` | string | `supreamth` | GitHub username (ไม่มี space) — ถ้าใส่จะ assign issue ให้ |
| `client_payload.submitted_at` | ISO 8601 | `2026-06-18T07:30:00Z` | audit trail ใน issue body |

Issue body ที่ Action สร้าง:

```
Project Start: <name ที่ parse จาก brief>

<full brief_markdown>

---
> Submitted via Project Start Form · 2026-06-18T07:30:00Z
> Route: **Architecture**
> Requester: `supreamth`

> After ~5 min, this issue is imported into the AI Project Tracker dashboard:
> http://127.0.0.1:8765
```

## Verification probes

| # | ชั้น | คำสั่ง | ผลที่คาดหวัง |
|---|---|---|---|
| 1 | Form HTML | `curl -s https://supreamth.github.io/my-sprees-docs/project-start/ \| grep -E 'id="(generate\|executeBtn)"'` | เจอทั้ง 2 id |
| 2 | Dispatch endpoint | `gh api repos/Supreamth/my-sprees/dispatches -X POST --input /dev/null` | HTTP 422 (auth + URL ถูก) |
| 3 | Workflow exists | `gh workflow list --repo Supreamth/my-sprees \| grep project-start-intake` | เจอ 1 entry |
| 4 | Last dispatch run | `gh run list --workflow project-start-intake.yml --repo Supreamth/my-sprees --limit 1` | conclusion = success |
| 5 | Issue created | `gh issue list --repo Supreamth/my-sprees --label project-start --state open` | เห็น issue ใหม่พร้อม label |
| 6 | Tracker server | `curl -H "Authorization: Bearer change...en" http://127.0.0.1:8765/api/health` | HTTP 200 |
| 7 | Manual ingest | `cd /root/ai-project-tracker && PYTHONPATH=src python3 -m ai_tracker.cli ingest-issues --label project-start --target-repo Supreamth/my-sprees --db data/tracker.db` | imported=1, skipped=0 |
| 8 | Re-run idempotent | (รันคำสั่งเดิมซ้ำ) | imported=0, skipped=1 |

## สถานะปัจจุบัน

| ชั้น | ที่อยู่ | สถานะ |
|---|---|---|
| Form HTML | `supreamth.github.io/my-sprees-docs/project-start/` | live |
| Action receiver | `Supreamth/my-sprees/.github/workflows/project-start-intake.yml` | deployed (commit `ca6568d`) |
| Tracker server | `127.0.0.1:8765` (PID 97891) | running |
| Tracker CLI | `/root/ai-project-tracker/src/ai_tracker/cli.py` | working — `ingest-issues` subcommand พร้อม |
| Cron loop | `/etc/cron.d/ai-tracker-intake` | pending — รัน manual ได้ |
| Cloudflare tunnel | `tracker.sprees.net` | pending login — รอ user click Authorize |

## ขั้นต่อไป

1. ติดตั้ง cron ingest-issues — เพิ่ม `/etc/cron.d/ai-tracker-intake` เพื่อ poll ทุก 5 นาทีอัตโนมัติ (ตอนนี้ต้องรัน manual)
2. Authorize cloudflared — เปิด callback URL แล้ว click Authorize เพื่อสร้าง `tracker.sprees.net` แบบ public
3. รัน E2E test ครบรอบ ตาม verification probes #1-#8 เพื่อยืนยันว่าทุกชั้นต่อกันจริง
4. Trigger จริงจากฟอร์ม — กรอกฟอร์มบน Pages → Execute → ดู issue ใหม่ → ดู row ใน dashboard ภายใน 5 นาที
5. Update status page — เมื่อ pipeline live ครบ ให้แก้ `system-status/` ให้บอกว่า "intake loop: closed"

## ดูเพิ่ม

- https://supreamth.github.io/my-sprees-docs/ — System Map (index)
- https://supreamth.github.io/my-sprees-docs/project-start/ — Project Start Form
- https://supreamth.github.io/my-sprees-docs/company-playbook/ — Company Playbook
- https://github.com/Supreamth/my-sprees/blob/main/.github/workflows/project-start-intake.yml — workflow.yml