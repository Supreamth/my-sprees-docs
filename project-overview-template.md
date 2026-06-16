# Project Overview Page Template

ทุกครั้งที่เกิด Project ใหม่ ให้สร้าง Project Overview Page เป็นหน้า web/dashboard กลางของ project เพื่อให้ founder, PM, designer, engineer, reviewer และ AI model ทุกตัวเห็นสถานะเดียวกัน

## Purpose

Project Overview Page ใช้เป็น:

1. หน้าแรกสำหรับติดตาม project
2. single-page status dashboard สำหรับคนและ AI
3. จุดรวม link ไป Project Start Brief, PRD, architecture, context handoff, tasks และ decisions
4. ที่เก็บ next step task/prompt ที่สามารถ copy ไปสั่ง model ถัดไปได้ทันที
5. ลดการถามซ้ำว่า project อยู่ขั้นไหน ต้องทำอะไรต่อ ใครเป็น owner และ context ล่าสุดอยู่ที่ไหน

## Required page for every project

เมื่อมี project ใหม่ ให้สร้าง:

```text
docs/products/<project-slug>/index.html
docs/products/<project-slug>/overview.md
docs/products/<project-slug>/context/current-state.md
docs/products/<project-slug>/context/model-handoff.md
```

ถ้าใช้ public docs site ให้ link จาก project registry หรือ company docs home

## Project Overview Page sections

### 1. Project header

ต้องแสดง:
- Project name
- One-line summary
- Owner
- Current phase
- Current status
- Last updated
- Next gate

### 2. Snapshot cards

ควรมี cards:
- Phase
- Status
- Owner
- Priority
- Risk level
- Next action
- Latest artifact
- Model currently recommended

### 3. Process timeline

แสดง process ทั้งหมดและสถานะ:

- Project Start
- Discovery
- Problem Definition
- Requirements
- PRD
- UX
- Architecture
- Delivery Planning
- Implementation
- QA / Security
- Release
- Feedback

Status values:
- not started
- in progress
- blocked
- ready for review
- completed
- skipped with reason

### 4. Source of truth links

รวม link ไป:
- Project Start Brief
- Problem Clarification Brief
- PRD
- Requirements
- UX flows
- Architecture
- Data model
- API contract
- Threat model
- Delivery plan
- Test plan
- Release checklist
- Current state
- Decision log
- Model handoff packet

### 5. Current state

ต้องตอบได้:
- ตอนนี้ project อยู่ phase ไหน
- ทำอะไรเสร็จแล้ว
- กำลังทำอะไร
- blocked อะไร
- decision ล่าสุดคืออะไร
- verification ล่าสุดคืออะไร
- context freshness เป็นอย่างไร

### 6. Next step task / prompt

ต้องมี prompt ที่ copy ได้เสมอสำหรับ model ถัดไป

ควรมี 3 แบบ:

1. Human instruction
   - ภาษาสั้นๆ ที่คนใช้สั่งต่อได้
2. AI handoff prompt
   - prompt พร้อม role, objective, source files, do-not-do, expected output
3. Reviewer prompt
   - prompt สำหรับให้ model อีกตัวตรวจงาน

### 7. Open questions and blockers

แสดง:
- open questions
- owner ของแต่ละ question
- due date
- impact ถ้าไม่ตอบ
- blocker status

### 8. Decisions

แสดง decisions สำคัญ:
- accepted
- proposed
- superseded

แต่ละ decision ต้อง link ไป decision log

### 9. Risks

แสดง risk table:
- risk
- likelihood
- impact
- mitigation
- owner

### 10. Activity log

สรุป chronological:
- date
- event
- actor/model
- artifact/commit/PR link

## Project Overview Markdown template

```markdown
# <Project Name> Overview

Updated: YYYY-MM-DD HH:MM TZ
Owner:
Current phase:
Status:
Priority:

## One-line summary

## Current objective

## Snapshot
- Phase:
- Status:
- Owner:
- Next gate:
- Latest artifact:
- Recommended next model:

## Source of truth
- Project Start Brief:
- PRD:
- Requirements:
- Architecture:
- Current State:
- Model Handoff:
- Decision Log:

## Process timeline
| Phase | Status | Owner | Link | Notes |
|---|---|---|---|---|
| Project Start | completed | | | |
| Discovery | not started | | | |
| PRD | not started | | | |
| UX | not started | | | |
| Architecture | not started | | | |
| Delivery Planning | not started | | | |
| Implementation | not started | | | |
| QA/Security | not started | | | |
| Release | not started | | | |
| Feedback | not started | | | |

## Current state

## Completed

## In progress

## Blocked

## Open questions
| Question | Owner | Due | Impact | Status |
|---|---|---|---|---|

## Decisions
| Date | Decision | Status | Link |
|---|---|---|---|

## Risks
| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|

## Next step task / prompt

### Human instruction

### AI handoff prompt

### Reviewer prompt

## Activity log
| Date | Actor/model | Event | Link |
|---|---|---|---|
```

## Next step prompt template

```markdown
You are taking over this project as: [Role]

Read first:
- <Project overview URL>
- <Current state file>
- <Model handoff file>
- <Relevant source-of-truth docs>

Current objective:

Current phase:

Do this next:
1.
2.
3.

Do not do:
- Do not skip the current gate
- Do not invent missing requirements
- Do not overwrite source-of-truth decisions without updating decision log

Expected output:
- Summary
- Updated artifacts
- Decisions needed
- Verification performed
- Updated next-step prompt
```

## Rule

Every meaningful model run must either:

1. update the Project Overview Page, or
2. return a proposed update for the page

No project should continue without a visible next step and copyable next prompt.
