# Company/Product Development Playbook

เอกสารมาตรฐานสำหรับบริษัทที่ใช้ AI เป็นส่วนหนึ่งของการค้นหาโอกาส ออกแบบผลิตภัณฑ์ วางระบบ พัฒนา ทดสอบ ปล่อย production และเรียนรู้จากลูกค้า โดยตั้งใจให้ใช้ได้จริงก่อนเริ่มสั่งให้เขียนระบบ

## หลักการสำคัญ

1. เริ่มจากปัญหาและลูกค้า ไม่ใช่ code
2. ทุก phase ต้องมี artifact ที่อ่าน ตรวจ และตัดสินใจได้
3. Model ที่เขียนงานไม่ควรเป็น model เดียวกับที่ approve งานตัวเอง
4. ใช้ AI เป็นทีมผู้ช่วยหลายบทบาท แต่ให้มนุษย์เป็น decision owner
5. Requirement สำคัญต้องมี acceptance criteria เสมอ
6. Release ต้องมี test, security, rollback และ monitoring ก่อน production

## AI model role taxonomy

| Role | ใช้กับงาน | Model ที่เหมาะ |
|---|---|---|
| Strategist | company thesis, market positioning, business model | strongest reasoning model |
| Researcher | market research, competitor, API/vendor scan | web/research-enabled model |
| Product Manager | PRD, requirements, roadmap, scope | long-context reasoning model |
| UX Designer | user flow, wireframe, copy, states | design/vision-capable model |
| Architect | architecture, data model, API contract, trade-offs | strong reasoning model |
| Builder | implementation, tests, refactor | coding-specialized model |
| Reviewer | spec compliance, code review, QA review | separate reasoning/coding model |
| Security Reviewer | threat model, auth, permissions, data risk | security-focused reasoning model |
| SRE/DevOps | CI/CD, deploy, rollback, monitoring | DevOps/SRE-capable model |
| Analyst | metrics, feedback, cohort, support synthesis | data-analysis + reasoning model |

## End-to-end process

### Phase 0: Company / Business Intent

Goal: นิยามว่าบริษัทนี้ควรมีอยู่ทำไม

Key questions:
- บริษัทแก้ปัญหาอะไร
- ลูกค้าคือใคร
- จะหาเงินจากอะไร
- ทำไมตอนนี้ถึงควรทำ
- ถ้าสำเร็จใน 12 เดือน หน้าตาเป็นยังไง

Artifacts:
- `company-thesis.md`
- `business-model.md`
- `initial-icp.md`
- `positioning.md`

Recommended model:
- Strongest reasoning model
- Optional: second reasoning model for critique

Human owner:
- Founder / CEO

Exit gate:
- อธิบาย company thesis ได้ใน 3-5 ประโยค
- มี ICP แรกที่ชัดพอจะไปสัมภาษณ์ได้

### Phase 1: Market & Customer Discovery

Goal: พิสูจน์ว่าปัญหามีอยู่จริงและมีคนยอมจ่าย

Activities:
- สัมภาษณ์ลูกค้า 10-30 ราย
- วิเคราะห์ competitors และ alternatives
- เก็บ current workflow และ pain points
- ประเมิน willingness to pay

Artifacts:
- `customer-interviews/`
- `competitor-matrix.md`
- `pain-point-ranking.md`
- `market-map.md`

Recommended model:
- Web/research model สำหรับ market/competitor
- Long-context model สำหรับสรุป interviews
- Reasoning model สำหรับหา pattern และ blind spots

Human owner:
- Founder / Product Lead

Exit gate:
- มี pain point ซ้ำจากลูกค้าหลายราย
- รู้ว่าเขาแก้ปัญหานี้ปัจจุบันอย่างไร
- มี hypothesis ว่าทำไม solution เราดีกว่าเดิม

### Phase 2: Problem Definition

Goal: นิยาม problem ให้คมก่อนคิด solution

Artifacts:
- `problem-statement.md`
- `target-user-segment.md`
- `current-workflow.md`
- `problem-validation-summary.md`

Recommended model:
- Strong reasoning model
- Use prompt: “challenge this problem statement; identify assumptions, weak evidence, and alternative explanations.”

Human owner:
- Founder / PM

Exit gate:
- problem statement ชัดใน 3 ประโยค
- แยก symptom, root cause และ desired outcome ได้

### Phase 3: Product Strategy

Goal: กำหนดว่าจะชนะด้วยอะไรและ MVP แรกคืออะไร

Artifacts:
- `product-strategy.md`
- `mvp-scope.md`
- `non-goals.md`
- `success-metrics.md`
- `pricing-hypothesis.md`

Recommended model:
- Reasoning model ระดับสูง
- Multi-model debate: proposer, critic, investor/customer/operator perspective

Human owner:
- Founder / Product Lead

Exit gate:
- MVP เล็กพอจะทำได้ แต่มีค่าพอจะทดสอบหรือขาย
- มี non-goals ชัดเจนเพื่อกัน scope creep

### Phase 4: Requirement Discovery

Goal: แปลงปัญหาและ strategy เป็น requirement ที่ตรวจได้

Requirement groups:
- Business requirements
- User requirements
- Functional requirements
- Non-functional requirements
- Compliance requirements
- Out of scope

Artifacts:
- `requirements.md`
- `user-stories.md`
- `acceptance-criteria.md`
- `assumptions-and-risks.md`

Recommended model:
- Long-context reasoning model
- Domain expert review ถ้าเป็น regulated industry

Human owner:
- PM / Domain Expert / Founder

Exit gate:
- ทุก requirement สำคัญมี acceptance criteria
- มี out-of-scope ที่ชัดเจน

### Phase 5: PRD

Goal: ทำเอกสารกลางที่ business, product, design, engineering, QA อ่านตรงกัน

PRD structure:
- Background
- Problem
- Goals
- Non-goals
- Target users
- User journeys
- Functional requirements
- Non-functional requirements
- UX requirements
- Analytics requirements
- Edge cases
- Acceptance criteria
- Rollout plan
- Open questions

Artifacts:
- `prd.md`

Recommended model:
- Draft: reasoning + writing model
- Critique: separate reasoning model
- Engineering summary: fast model ได้หลัง PRD approved

Human owner:
- PM

Exit gate:
- อ่านแล้วรู้ว่า build อะไร ไม่ build อะไร และเสร็จจริงวัดยังไง

### Phase 6: UX / Workflow Design

Goal: ออกแบบ flow ก่อนออกแบบ database/code

Artifacts:
- `user-flows.md`
- `wireframes/`
- `ux-spec.md`
- `states-and-errors.md`
- `copy-guidelines.md`

Recommended model:
- Design/vision-capable model
- Reasoning model สำหรับ edge states
- Optional HTML prototype model for clickable prototype

Human owner:
- Product Designer / PM

Exit gate:
- happy path, error path, empty/loading/success states ชัด
- permission/admin workflow ชัดถ้ามี

### Phase 7: Technical Discovery

Goal: ลด technical unknown ก่อน commit แผนใหญ่

Artifacts:
- `technical-discovery.md`
- `integration-inventory.md`
- `data-source-inventory.md`
- `spikes/`
- `security-assumptions.md`

Recommended model:
- Architect/reasoning model
- Research model สำหรับ third-party APIs/libraries
- Coding model สำหรับ proof-of-concept spike

Human owner:
- CTO / Tech Lead

Exit gate:
- unknown ใหญ่ถูกพิสูจน์ด้วย spike หรือมี mitigation plan

### Phase 8: Architecture & System Design

Goal: วางระบบให้ dev ทำต่อได้โดยไม่เดา

Artifacts:
- `architecture.md`
- `adrs/`
- `api-contract.md`
- `data-model.md`
- `sequence-diagrams.md`
- `threat-model.md`
- `observability-plan.md`
- `deployment-architecture.md`

Recommended model:
- Architect: strong reasoning model
- Security critique: security-focused model
- Scale/cost critique: separate reasoning model
- API/schema draft: coding-aware model

Human owner:
- CTO / Staff Engineer / Security Lead

Exit gate:
- architecture ผ่าน review
- auth, data, error handling, observability, deployment และ rollback ถูกคิดไว้แล้ว

### Phase 9: Delivery Planning

Goal: แตกงานให้ build ได้จริงเป็น issue/PR เล็กๆ

Artifacts:
- `delivery-plan.md`
- `milestones.md`
- GitHub issues / Linear tickets
- `implementation-plan.md`
- `test-plan.md`
- `release-plan.md`

Recommended model:
- Planning/reasoning model
- Coding-aware model สำหรับแตก technical tasks

Human owner:
- Tech Lead / Engineering Manager / PM

Exit gate:
- ไม่มี issue กว้างแบบ “build dashboard”
- ทุก issue มี context, goal, scope, non-goals, acceptance criteria, test plan

### Phase 10: Implementation

Goal: build แบบ controlled และตรวจได้

Process:
- Branch from main
- Write failing tests where practical
- Implement minimal code
- Run local verification
- Open small PR
- CI required
- Review by separate reviewer model + human
- Merge
- Post-merge verification

Artifacts:
- Code
- Tests
- PR
- Review notes
- CI result
- Changelog if needed

Recommended model:
- Builder: coding-specialized model
- Tests: coding/reasoning model
- Review: separate model, not the builder
- Debug: reasoning + coding model

Human owner:
- Engineer / Tech Lead

Exit gate:
- tests pass
- acceptance criteria covered
- review approved
- no known security blocker

### Phase 11: QA / Security / Compliance

Goal: พิสูจน์ว่าระบบพร้อมใช้งานจริง

QA coverage:
- Unit tests
- Integration tests
- E2E tests
- Regression tests
- Performance tests
- Accessibility tests
- Browser/device tests

Security coverage:
- Auth and permission checks
- Input validation
- Secrets scanning
- Dependency scanning
- Audit logs
- Threat model review

Compliance coverage:
- Data retention
- Consent
- Export/delete user data
- Audit trail
- Privacy policy impact

Artifacts:
- `qa-report.md`
- `security-review.md`
- `risk-register.md`
- `compliance-checklist.md`

Recommended model:
- QA reasoning model
- Security-focused model
- Coding model for automated tests
- Human expert for legal/compliance

Human owner:
- QA Lead / Security Lead / Legal

Exit gate:
- release readiness checklist ผ่าน
- known risks accepted by human owner

### Phase 12: Release / Operations

Goal: ปล่อยระบบโดยควบคุม risk

Artifacts:
- `release-checklist.md`
- `deployment-plan.md`
- `rollback-plan.md`
- `runbook.md`
- `monitoring-dashboard.md`
- `incident-playbook.md`

Recommended model:
- DevOps/SRE-capable model
- Reasoning model for release risk
- Fast model for release notes summary

Human owner:
- Tech Lead / SRE / Founder

Exit gate:
- deploy, monitoring, alert, rollback, incident owner ชัด

### Phase 13: Feedback Loop / Iteration

Goal: เรียนรู้หลัง release แล้วแปลงเป็น backlog ที่มีเหตุผล

Artifacts:
- `analytics-report.md`
- `customer-feedback-summary.md`
- `support-ticket-themes.md`
- `next-iteration-backlog.md`
- `post-release-review.md`

Recommended model:
- Data analysis model
- Long-context summarization model
- Reasoning model for prioritization

Human owner:
- PM / Founder / Growth / Support

Exit gate:
- next iteration ผูกกับ metric หรือ customer learning ไม่ใช่แค่ idea ใหม่

## Required templates for a lean AI-native company

Minimum docs:
1. `company-thesis.md`
2. `problem-statement.md`
3. `prd.md`
4. `user-flows.md`
5. `architecture.md`
6. `delivery-plan.md`
7. `test-plan.md`
8. `release-checklist.md`
9. `security-checklist.md`
10. `decision-log.md`

## Decision gates summary

| Gate | ต้องมีอะไรก่อนผ่าน |
|---|---|
| Start discovery | ICP draft + interview plan |
| Start PRD | validated problem + customer evidence |
| Start design | PRD draft + primary workflows |
| Start architecture | PRD + UX flow + technical constraints |
| Start implementation | approved PRD + architecture + acceptance criteria + test plan |
| Merge PR | tests + review + criteria coverage |
| Release production | QA + security + rollback + monitoring |
| Iterate | analytics/feedback + prioritized learning |

## Operating rules for AI usage

1. Separate maker and checker
   - Builder model writes
   - Reviewer model critiques
   - Human approves important decisions

2. Use model by task, not by habit
   - Strategy: strongest reasoning
   - Research: web-enabled
   - Requirements: long-context reasoning
   - UX: design/vision
   - Architecture: strong reasoning
   - Code: coding model
   - Security: security-focused
   - Analytics: data-analysis model

3. Never skip artifacts
   - If it is not written, it is not aligned

4. No production without rollback
   - Every release must have a way back or a containment plan

5. No requirement without acceptance criteria
   - If it cannot be tested or observed, it is not ready for implementation

6. Record decisions
   - Use ADRs and decision log to avoid re-litigating old choices

## First implementation recommendation

Before starting any real system, create a company docs repository with:

```text
docs/
  company-thesis.md
  problem-statement.md
  product-strategy.md
  prd.md
  requirements.md
  user-flows.md
  architecture.md
  delivery-plan.md
  test-plan.md
  release-checklist.md
  security-checklist.md
  decision-log.md
```

Then make every new product idea pass through this sequence:

```text
Idea → Discovery → Problem → Strategy → Requirements → PRD → UX → Architecture → Delivery Plan → Implementation → QA/Security → Release → Feedback
```

This playbook is intentionally lightweight enough for a startup, but strict enough to build real company-grade systems.
