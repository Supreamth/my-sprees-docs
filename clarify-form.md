# Problem Clarification Form

แบบฟอร์ม prerequisite สำหรับถาม user ก่อนเริ่มสั่งพัฒนาระบบ เพื่อป้องกันการ build ผิดปัญหา ผิด user หรือผิด scope

## ควรออกแบบเป็น Web Form ไหม?

ควร โดยเฉพาะถ้าจะใช้ในบริษัทจริง เพราะ Web Form ช่วย:

1. Standardize intake ทุก request ด้วย schema เดียวกัน
2. ลด ambiguity ก่อนเข้า PRD/UX/Architecture
3. ทำให้ compare priority ระหว่าง request ได้ง่าย
4. ทำให้ AI และทีม dev ได้ context ที่ครบกว่า chat สั้นๆ
5. สร้าง audit trail ว่า request เริ่มจากปัญหาและ evidence อะไร

ข้อควรระวัง: อย่าถามเยอะเกินตั้งแต่แรก ควรแยกเป็น 2 stage

- Stage A: Intake 8-10 คำถาม สำหรับคัดกรอง idea
- Stage B: Deep Clarification 25-35 คำถาม สำหรับ request ที่จะเข้า delivery จริง

## Stage A: Intake Questions

1. ชื่อปัญหา/request คืออะไร?
2. ใครเป็น owner/requester?
3. ปัญหาที่พบคืออะไร? ห้ามเริ่มจาก solution
4. ใครคือ user ที่เจอปัญหานี้?
5. มีหลักฐานอะไรบ้าง เช่น interview, support ticket, metric, sales feedback, screenshot?
6. Impact ของปัญหาคืออะไร เสียเวลา/เงิน/โอกาสเท่าไหร่?
7. Urgency อยู่ระดับไหน?
8. ถ้าไม่แก้ตอนนี้จะเกิดอะไร?
9. ปัจจุบันแก้ปัญหานี้อย่างไร?
10. อยากให้ส่งต่อ phase ไหน: discovery, PRD, UX, architecture, delivery planning, implementation?

## Stage B: Deep Clarification Questions

### Problem

1. ปัญหานี้เกิดในสถานการณ์ไหน?
2. เกิดบ่อยแค่ไหน?
3. severity สูงสุดคืออะไร?
4. root cause ที่คิดว่าเป็นไปได้คืออะไร?
5. อะไรคือ symptom และอะไรคือ root problem?

### User / Customer

6. user หลักคือใคร?
7. buyer หรือ decision maker คือคนเดียวกับ user ไหม?
8. segment ไหนควรเริ่มก่อน?
9. ใครไม่ใช่ target user ใน version แรก?
10. user มี skill/context/constraint อะไร?

### Workflow

11. workflow ปัจจุบัน step-by-step เป็นอย่างไร?
12. จุดเจ็บที่สุดอยู่ขั้นตอนไหน?
13. มี handoff ระหว่างคน/ทีม/ระบบตรงไหน?
14. มี manual workaround อะไรอยู่?
15. ต้อง integrate กับเครื่องมืออะไรบ้าง?

### Desired Outcome

16. ถ้าแก้สำเร็จ user จะทำอะไรได้?
17. outcome ที่ดีต้องเร็วขึ้น ถูกลง แม่นขึ้น หรือเสี่ยงน้อยลงอย่างไร?
18. metric ไหนควรดีขึ้น?
19. user จะรู้ได้อย่างไรว่าระบบช่วยจริง?
20. business จะรู้ได้อย่างไรว่าคุ้ม?

### Scope

21. MVP ต้องมีอะไรบ้าง?
22. อะไรไม่ทำใน version แรก?
23. อะไรเป็น nice-to-have?
24. deadline หรือ milestone สำคัญคืออะไร?
25. budget/resource constraint คืออะไร?

### Acceptance Criteria

26. Given/When/Then หลักคืออะไร?
27. test case happy path คืออะไร?
28. edge cases สำคัญคืออะไร?
29. error state ที่ต้องรองรับคืออะไร?
30. Definition of Done คืออะไร?

### Risk / Security / Compliance

31. ข้อมูลมี PII/payment/health/financial data ไหม?
32. permission model ต้องเป็นอย่างไร?
33. audit log ต้องมีไหม?
34. data retention/delete/export ต้องมีไหม?
35. failure mode ที่รับไม่ได้คืออะไร?

## Gate Rules

| Gate | ต้องตอบได้ก่อนผ่าน | ถ้ายังตอบไม่ได้ |
|---|---|---|
| Discovery | ใครเจอปัญหาและ evidence คืออะไร | ไปสัมภาษณ์/เก็บ evidence เพิ่ม |
| PRD | goal, non-goal, user journey, acceptance criteria | ห้ามเริ่ม architecture |
| Architecture | data, integration, auth, scale, security constraints | ทำ technical discovery/spike ก่อน |
| Implementation | scope แตกเป็น issue เล็ก + test plan | แตก delivery plan ใหม่ |

## Output Template

```markdown
# Problem Clarification Brief

## Intake
- Title:
- Owner:
- Urgency:
- Recommended route:

## Problem

## User / Customer

## Evidence

## Impact

## Current workflow

## Pain point

## Desired outcome

## Success metrics

## MVP scope

## Non-goals

## Acceptance criteria

## Constraints / dependencies

## Data / security / compliance risks

## Integrations

## Unacceptable failure modes

## Readiness check
Ready / Not ready for implementation because...
```
