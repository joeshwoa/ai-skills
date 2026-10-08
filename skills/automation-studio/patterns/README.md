# Pattern library — tested n8n building blocks (easy → complex)

Every pattern is SDK code (`workflow.ts`) + the built JSON (`workflow.json`) + test cases (`cases.json`) + a
diagram (`diagram.svg`, `diagram.mmd`). All cases pass on n8n 2.42 with `autokit test` (cases marked
"network" call the real public API; skip them offline with `AUTOKIT_OFFLINE=1`).

Start from one: `bash scripts/auto.sh new list` · `bash scripts/auto.sh new 08 -o my-flow.ts`

| # | Pattern | Level | What it teaches | Credentials needed |
|---|---------|-------|-----------------|--------------------|
| 01 | webhook-lead-to-sheet | 1–2 | Webhook in, clean with Set, validate with IF (regex), write to Sheets, reply 200/400 with Respond to Webhook | Google Sheets |
| 02 | schedule-api-digest | 2 | Schedule (time of day), HTTP to a key-less public API with retries, Code summary that **fails loudly** on bad data, email | Gmail |
| 03 | form-switch-routing | 2 | n8n's hosted Form trigger, tidy fields, **Switch** with named outputs + fallback, Slack / Gmail / triage | Slack, Gmail |
| 04 | rss-filter-telegram | 2–3 | RSS, Filter by regex, **Remove Duplicates across executions** (never re-send), Limit, Telegram | Telegram bot |
| 05 | paginated-api-to-postgres | 3 | HTTP **built-in pagination** (`$pageCount`, complete expression), Split Out, typed mapping, Postgres **upsert** (re-runs never duplicate) | Postgres |
| 06 | batch-rate-limit | 3 | Reply 202 first, Split Out, **Loop Over Items** (batches of 10) + Wait, per-item errors don't stop the run, count results | Slack |
| 07 | error-alerts | 3 | ONE **error workflow** for all flows: classify AUTH / TRANSIENT / BUG, Telegram + email with a link to the failed run | Telegram, Gmail |
| 08 | idempotent-webhook | 4 | **Idempotency**: require a key, n8n remembers processed keys (2 outputs: new / seen) → 201 vs 200 duplicate vs 400 — proven over 2 runs | none |
| 09 | ai-support-agent | 4 | **AI Agent** + OpenAI model + per-customer memory + Code tool, input guardrails before AI cost, handoff flag | OpenAI |
| 10 | document-extraction | 4 | Download PDF → **Extract from File** (tested on a real PDF) → **Information Extractor** → Code re-checks the maths → Sheets or review | OpenAI, Google Sheets |
| 11 | human-approval | 5 | **Human in the loop**: Gmail *send and wait* with Approve/Decline (double confirm, 3-day timeout), auto-approve under a threshold | Gmail, Slack |
| 12 | orchestrator-subworkflow | 5 | **Sub-workflows**: typed inputs, called once per item, failures counted not fatal; `deploy` links `name:<sub-workflow>` to the real id | Slack |

Levels: 1 = one trigger, one action · 2 = transform + branch · 3 = loops, pagination, batching, error workflow ·
4 = idempotency, AI, documents, state · 5 = humans in the loop, sub-workflow architecture, multi-system orchestration.

Lessons these tests caught (they are also in `references/n8n-building.md`):
- With `caseSensitive: false`, n8n lower-cases the **value**, not your regex → write regexes in lower case.
- Remove Duplicates "seen in previous executions" does not dedupe inside one run; it has **two outputs** (kept / discarded).
- Respond to Webhook passes its input items on unchanged — chain work after it to reply first, process later.
- In SDK code use `expr('{{ … }}')` for expressions and double quotes in string arrays (`["id"]`); no TypeScript
  annotations, no arrow-function helpers, no `.map()` at the top level of the file.
