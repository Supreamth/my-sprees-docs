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

แต่ถ้าช่อง critical ยังว่าง ระบบจะ mark ว่า Not ready for implementation
