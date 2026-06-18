# Project Start Form

แบบฟอร์มแยกสำหรับเริ่มต้น Project ให้ requester กรอกข้อมูลให้ชัดเจนก่อนเข้าสู่ Discovery, PRD, UX, Architecture หรือ Development

## Purpose

ใช้เป็นด่านแรกของทุก project request เพื่อให้บริษัทไม่เริ่มจากคำสั่งกว้างๆ เช่น “ทำระบบ”, “ทำ dashboard”, “ทำ AI” แต่เริ่มจาก:

- ปัญหาคืออะไร
- ใครเจอปัญหา
- มีหลักฐานอะไร
- impact คืออะไร
- goal และ success metrics คืออะไร
- MVP scope และ non-goals คืออะไร
- risk/security/compliance คืออะไร
- acceptance criteria คืออะไร

## Rule

No brief, no build.

ถ้า Project Start Brief ยังไม่ชัด ห้ามเริ่ม implementation ให้ส่งกลับไป Discovery, PRD หรือ Architecture ตามข้อมูลที่ขาด

## Critical fields

1. Project name
2. Business owner
3. Problem
4. User / customer
5. Evidence
6. Impact / cost
7. Goal
8. MVP scope
9. Non-goals
10. Acceptance criteria

## Output

ระบบจะ generate `Project Start Brief` เป็น Markdown สำหรับส่งต่อให้ Founder/PM/AI/team review

## Routing

Requester เลือก next phase ได้:

- Discovery
- PRD
- UX Design
- Architecture
- Delivery Planning
- Implementation

แต่ถ้าช่อง critical ยังว่าง ระบบจะ block และ highlight ช่องที่ขาด — ต้องกรอกให้ครบก่อนจึงจะ Execute ได้

## Execute Flow

เมื่อ critical fields ครบ ปุ่ม **Execute → \<Route\>** จะปรากฏใต้ brief output การไหลของข้อมูลมี 3 ขั้น:

1. **Browser → GitHub API**  
   ฟอร์มทำ `POST https://api.github.com/repos/Supreamth/my-sprees/dispatches` พร้อม `event_type: project-start-intake` และ `client_payload` ที่มี brief markdown, route, requester, และ timestamp

2. **GitHub Action → Issue**  
   Workflow `project-start-intake.yml` ใน `Supreamth/my-sprees` รับ event แล้วสร้าง Issue:
   - Title: `Project Start: <projectName>`
   - Body: brief markdown ทั้งหมด
   - Labels: `project-start` และ `project-start:<route>` เช่น `project-start:Implementation`
   - Assignee: requester (ถ้าเป็น GitHub username ที่ไม่มี space)

3. **AI Project Tracker → Dashboard**  
   Cron บนเครื่อง host รัน `ingest-issues` command ทุก ~5 นาที:
   ```bash
   PYTHONPATH=src python3 -m ai_tracker.cli ingest-issues \
     --label project-start \
     --target-repo Supreamth/my-sprees \
     --db data/tracker.db
   ```
   Issue ถูก import เป็น project + first task ใน SQLite แล้วแสดงใน dashboard ที่ http://127.0.0.1:8765

Brief ที่ submit ผ่านฟอร์มนี้จะ land ใน `Supreamth/my-sprees` Issues พร้อม label `project-start:<route>` และ `/root/ai-project-tracker` จะ poll และ import เข้า dashboard โดยอัตโนมัติ

## Live status (2026-06-18)

**Pipeline**: end-to-end verified, public HTTPS dashboard live.

- Form: https://supreamth.github.io/my-sprees-docs/project-start/
- Action: https://github.com/Supreamth/my-sprees/blob/main/.github/workflows/project-start-intake.yml
- Dashboard: https://tracker.sprees.net (auth: `Authorization: Bearer *** change-this-token`)
- Test artifact: https://github.com/Supreamth/my-sprees/issues/35 (Issue) → tracker project #4

**Owner**: Founder / PM
**Runbook**: see `project-start/README.md` §4-6 for full pipeline + verification + infra details
