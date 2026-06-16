# System Status

หน้านี้แสดงสถานะการเชื่อมต่อทั้งหมดในระบบ: GitHub, GitHub Pages, AI Models และ external APIs

ดูเวอร์ชัน HTML: https://supreamth.github.io/my-sprees-docs/system-status/

## Trigger command

พิมพ์คำสั่งใดคำสั่งหนึ่งนี้เพื่อให้ผมอัปเดต:

- `update status`
- `refresh status`
- `check connections`

## Behavior เมื่อ trigger

1. ผมรัน health check จริงด้วย `curl` หรือ tool ที่เหมาะสม — GitHub API, Pages, external endpoints
2. ตรวจ SSH key, gh CLI, local repo status, GitHub Actions latest run
3. ตรวจ Model Validation Log ล่าสุดเพื่อ update สถานะ model
4. Update ตารางในหน้า + เปลี่ยน "Last updated" timestamp
5. Commit + push ไป my-sprees-docs
6. Verify Pages อัปเดตแล้ว

## Status legend

| Badge | Meaning | Action |
|---|---|---|
| OK / 200 | reachable + working as expected | no action |
| DEGRADED / WARN | reachable but with limitation (e.g. fallback only) or unvalidated | consider improving or validating |
| DOWN / FAIL | unreachable or broken | block dependent work until fixed |

## Operating rules

1. Update status ก่อนเริ่ม session งานใหม่ — ใช้เวลา 1-2 นาที
2. ถ้าเจอ DOWN → หยุดงานที่ depend on connection นั้น จนกว่าจะ resolve
3. ถ้าเจอ DEGRADED → ทำงานได้แต่ต้องระวัง fallback path
4. ถ้า model ใหม่ถูก deploy → update Models section + Model Validation Log พร้อมกัน

## Anti-pattern

อย่า trust status เก่าเกิน 24 ชั่วโมง — ถ้าไม่แน่ใจ ให้ refresh ก่อนเริ่มงาน
