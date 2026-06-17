# System Status

หน้านี้แสดงสถานะการเชื่อมต่อทั้งหมดในระบบ: GitHub, GitHub Pages, AI Models, Model Credit & Usage และ external APIs

ดูเวอร์ชัน HTML: https://supreamth.github.io/my-sprees-docs/system-status/

## Snapshot ล่าสุด

Last updated: 2026-06-17 13:25 UTC+7 (added Model Credit & Usage function)

| Summary | Count |
|---|---:|
| Total connections | 13 |
| Healthy | 12 |
| Degraded / Unvalidated | 1 |
| Down | 0 |

## AI Models

| Connection | Provider | Status | Last check | Note |
|---|---|---|---|---|
| MiniMax-M3 | minimax-oauth | PASS 5/5 | 2026-06-16 20:25 | validated earlier; see Model Validation Log |
| OpenAI GPT-5.5 | openai-codex | PASS 5/5 | 2026-06-16 20:44 | validated in current session: skills, session search, honesty, memory injection, failure recovery. Current model access works via subscription/OAuth provider; direct `OPENAI_API_KEY` env is not set. |
| Other models (Anthropic, Gemini, DeepSeek, Grok) | mixed | UNVALIDATED | — | mentioned in routing table but not yet validated in this profile |

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
| OpenRouter | `OPENROUTER_API_KEY` → `/api/v1/credits` | READY | credit/usage/remaining |
| DeepSeek | `DEEPSEEK_API_KEY` → `/user/balance` | READY | balance by currency |
| OpenAI API | `OPENAI_ADMIN_KEY` หรือ `OPENAI_API_KEY` → costs endpoint | KEY-DEPENDENT | Codex/OAuth subscription อาจไม่มี billing API |
| Anthropic, Gemini, xAI/Grok, MiniMax OAuth | provider console / admin API | MANUAL | ต้องเช็คผ่าน portal หรือเพิ่ม admin API ภายหลัง |

### Latest safe run

| Provider | Status | Credit remaining | Usage | Note |
|---|---|---:|---:|---|
| Hermes local usage | OK | — | available via `hermes insights --days 30` | verified 2026-06-17 13:28 UTC+7 |
| OpenRouter | MISSING_KEY | — | — | `OPENROUTER_API_KEY` not set in this runtime |
| OpenAI API | MISSING_KEY | — | — | Current OpenAI access is Codex/OAuth; billing API key not set |
| DeepSeek | MISSING_KEY | — | — | `DEEPSEEK_API_KEY` not set in this runtime |
| Anthropic, Gemini, xAI/Grok, MiniMax OAuth | MANUAL | — | — | ต้องเช็คผ่าน provider console หรือเพิ่ม admin API ในอนาคต |

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
