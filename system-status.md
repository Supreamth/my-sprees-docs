# System Status

หน้านี้แสดงสถานะการเชื่อมต่อทั้งหมดในระบบ: GitHub, GitHub Pages, AI Models, Model Credit & Usage และ external APIs

ดูเวอร์ชัน HTML: https://supreamth.github.io/my-sprees-docs/system-status/

## Snapshot ล่าสุด

Last updated: 2026-06-18 02:42 UTC+7 (MiniMax-M3 re-validated)

| Summary | Count |
|---|---:|
| Total connections | 13 |
| Healthy | 12 |
| Degraded / Unvalidated | 0 |
| Down | 0 |

## AI Models

| Connection | Provider | Status | Last check | Note |
|---|---|---|---|---|
| MiniMax-M3 | minimax-oauth (current session) | PASS 5/5 | 2026-06-18 02:42 | re-validated today via `model change`: skills (github-pr-workflow loaded), session search (SQLite hit on yesterday's sessions), honesty (clone fail admitted), memory injection (cross-session recall verified), failure recovery (2-layer diagnose). See Model Validation Log |
| OpenAI GPT-5.5 | openai-codex | PASS 5/5 | 2026-06-16 20:44 | validated in current session: skills, session search, honesty, memory injection, failure recovery. Current model access works via subscription/OAuth provider; direct `OPENAI_API_KEY` env is not set. |
| Grok-4.3 | xai-oauth | PASS 5/5 | 2026-06-17 15:10 | validated (skills loading, session search, honesty, memory injection, failure recovery) |

## Model Credit & Usage Function

เพิ่ม function สำหรับเช็คเครดิตและ usage ของ model providers แบบปลอดภัย:

- ห้ามฝัง API key / OAuth token ใน GitHub Pages เพราะ repo/page เป็น public static site
- ใช้สคริปต์ `scripts/check_model_credit_usage.py` อ่าน secrets จาก environment ตอน runtime
- Output ที่เอามาลงหน้าเว็บต้องเป็น summary เท่านั้น เช่น remaining credit, usage, status, note — ไม่ใส่ token/raw response ที่ sensitive

### Run command

```bash
cd /root/my-sprees-docs
python3 scripts/check_model_credit_usage.py --days 30 --format markdown
```

### Provider support

| Provider / Source | Method | Status | Note |
|---|---|---|---|
| Hermes local usage | `hermes insights --days 30` | READY | session/token usage ในเครื่อง ไม่ใช่ provider billing |
| OpenRouter | `OPENROUTER_API_KEY` → `/api/v1/credits` | OPTIONAL / NOT CONNECTED | ตอนนี้ไม่มี key; เป็น capability เผื่อเปิดใช้ภายหลัง ไม่ใช่ connection ปัจจุบัน |
| DeepSeek | `DEEPSEEK_API_KEY` → `/user/balance` | READY | balance by currency |
| OpenAI API | `OPENAI_ADMIN_KEY` หรือ `OPENAI_API_KEY` → costs endpoint | KEY-DEPENDENT | Codex/OAuth subscription อาจไม่มี billing API |
| Anthropic, Gemini, xAI/Grok, MiniMax OAuth | provider console / admin API | MANUAL | ต้องเช็คผ่าน portal หรือเพิ่ม admin API ภายหลัง |

### Latest safe run

| Provider | Status | Credit remaining | Usage | Note |
|---|---|---:|---:|---|
| Hermes local usage | OK | — | 1d: 38,324,125 tokens; 7d/15d/30d: 194,004,490 tokens | verified 2026-06-17 14:12 UTC+7 via `hermes insights --days 1/7/15/30` |
| OpenRouter | MISSING_KEY | — | — | `OPENROUTER_API_KEY` not set in this runtime |
| OpenAI API | MISSING_KEY | — | — | Current OpenAI access is Codex/OAuth; billing API key not set |
| DeepSeek | MISSING_KEY | — | — | `DEEPSEEK_API_KEY` not set in this runtime |
| Anthropic, Gemini, xAI/Grok, MiniMax OAuth | MANUAL | — | — | ต้องเช็คผ่าน provider console หรือเพิ่ม admin API ในอนาคต |

### Hermes token usage by period

| Period | Sessions | Messages | Total tokens | gpt-5.5 | MiniMax-M3 | claude-sonnet-4-6 |
|---|---:|---:|---:|---:|---:|---:|
| 1 วัน | 10 | 1,155 | 38,324,125 | 32,284,926 | 6,039,199 | — |
| 7 วัน | 40 | 5,290 | 194,004,490 | 187,946,153 | 6,058,337 | 0 |
| 15 วัน | 40 | 5,290 | 194,004,490 | 187,946,153 | 6,058,337 | 0 |
| 1 เดือน | 40 | 5,290 | 194,004,490 | 187,946,153 | 6,058,337 | 0 |

Note: 7/15/30 วันเท่ากัน เพราะใน local Hermes session DB ตอนนี้มี activity อยู่ในช่วง Jun 13–17 เท่านั้น

## Trigger command

พิมพ์คำสั่งใดคำสั่งหนึ่งนี้เพื่อให้ผมอัปเดต:

- `update status`
- `refresh status`
- `check connections`
- `check model credits`

## Behavior เมื่อ trigger

1. ผมรัน health check จริงด้วย `curl` หรือ tool ที่เหมาะสม — GitHub API, Pages, external endpoints
2. ตรวจ SSH key, gh CLI, local repo status, GitHub Actions latest run
3. ตรวจ Model Validation Log ล่าสุดเพื่อ update สถานะ model
4. รัน `python3 scripts/check_model_credit_usage.py --days 30` เพื่อเช็ค credit/usage ที่ทำได้อย่างปลอดภัย
5. Update ตารางในหน้า + เปลี่ยน "Last updated" timestamp
6. Commit + push ไป my-sprees-docs
7. Verify Pages อัปเดตแล้ว

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
