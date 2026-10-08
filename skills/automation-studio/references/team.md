# The team — roles, what each one checks

One AI plays every role, in order. Each role has a short checklist; tick it mentally before moving on.

## 1. Automation consultant / business analyst (G1)
- What outcome, for whom, how often? What happens today by hand (steps, time spent, error rate)?
- Trigger: event in an app (webhook / app trigger), schedule, form, chat, email, file drop, manual, another workflow.
- Systems involved and **which accounts the user already has** (and plan: free/paid — features differ).
- Data: one sample of the real input (ask for it), required fields, what the output must look like.
- Volume: items per run, runs per day, peak; latency needed (seconds vs. next morning).
- Edge cases: duplicates, missing fields, wrong formats, very large inputs, the app being down.
- Who is alerted on failure and how. What is the "definition of done" (a test the user can run).
- ROI one-liner: hours saved per month × value; platform cost.

## 2. Process designer (G2)
- Plan JSON with clear verbs ("Create contact in HubSpot"), one decision per diamond, every branch ends.
- Mark manual/human steps, waits, and external systems; show error paths.
- Diagram → user sign-off. Changing a box now is free; after building it isn't.

## 3. Solutions architect
- Platform: n8n by default. Choose another only if the user asks or is already invested
  (`platforms.md`). Hosting: local Mac (dev, personal), n8n Cloud (zero ops), VPS/Docker (control, cost).
- Sync vs async: webhooks that do slow work reply **202 first** then process (patterns 06, 11).
- Split big flows into sub-workflows by responsibility (pattern 12); one error workflow for all (pattern 07).
- State: dedupe history (Remove Duplicates), Data Tables, or a real DB (Postgres) — never a Google Sheet as a database for >1k rows or concurrent writes.
- Limits: API rate limits, payload size, execution time; plan batching and retries.
- Cost: executions (n8n Cloud counts executions, not steps), Make operations, Zapier tasks, AI tokens.

## 4. Integration engineer
- For each system: node exists? (`auto.sh nodes`) → which resource/operation → auth type (OAuth2, API key,
  service account, bot token) → scopes. Otherwise HTTP Request with a predefined or generic credential.
- Pagination (`$pageCount`, next URL, cursor), rate limits (batch + Wait, `requestInterval`), timeouts,
  `retryOnFail` + `maxTries` + `waitBetweenTries` for flaky APIs.
- Webhooks: path, method, auth (header/basic/JWT), response mode (immediately / last node / Respond node),
  test URL vs production URL, signature verification (Stripe/GitHub/Meta) in a Code node or app trigger.

## 5. Workflow developer (G3)
- SDK code, exact node versions from the installed catalog, explicit expressions, named nodes.
- `$json` = current item from the immediate predecessor; reference anything else with `$('Node').item.json`
  (`nodeJson()` in SDK). Respect item linking (paired items).
- Code node only for real logic; always return `[{json:{…}}]` (all items) or `{json:{…}}` (each item).

## 6. AI engineer
- Agent only when tools/decisions are needed; for "classify/extract/summarise" use Text Classifier,
  Information Extractor, Basic LLM Chain (cheaper, deterministic).
- Model choice + temperature; structured output (parser or extractor schema); memory keyed per user/session.
- Guardrails: validate input before the model (cost), cap iterations, never let the model's numbers through
  unchecked (pattern 10), human handoff flag (pattern 09), log prompts/outputs for review.
- Cost: tokens × runs; batch; cache; smaller models for routing.

## 7. Data engineer
- Mapping table source → target with types; normalise (trim, lower-case emails, E.164 phones, ISO dates, cents).
- Idempotency: natural keys, upsert on a unique column, dedupe across runs.
- Validation with Filter/IF; bad records to a review path, not silently dropped.

## 8. QA / test engineer (G5)
- Cases: happy path, every IF/Switch branch, invalid input, empty list, external failure (mock an error item),
  duplicates (`"runs": 2`), large input (e.g. 500 items), unicode/Arabic text.
- Assert on the nodes that matter (outputs, item counts, exact fields, response status/body).
- Re-run all cases after every edit (regression). Live cases for key-less APIs.

## 9. Security & compliance
- Credentials only in n8n's credential store; least-privilege scopes; separate test/prod credentials.
- Webhook auth (header token / basic / JWT) for anything that changes data; never trust input.
- PII: minimise what you store; execution data retention (`EXECUTIONS_DATA_PRUNE`, save-on-error only).
- Self-host: HTTPS, strong owner password, 2FA, `N8N_ENCRYPTION_KEY` backed up, updates applied.

## 10. DevOps / platform engineer
- Install/upgrade (`setup_n8n.sh`, Docker), backups (`n8n export:workflow --all`, `export:credentials --all
  --decrypted` only to an encrypted location), queue mode with Redis + workers for volume, Postgres instead of
  SQLite for production. Details in `deploy-hosting.md`.

## 11. Monitoring & support
- Error workflow on every production flow; alerts with a link to the failed execution.
- Daily/weekly health: `auto.sh executions --target T`; failure rate; slow nodes.
- Runbook: common errors and the fix (expired OAuth → reconnect credential; 429 → lower batch; schema change).

## 12. Technical writer / trainer
- Handover (1 page): purpose, trigger, diagram, inputs/outputs, credentials used, how to pause/resume,
  alerts and what to do, how to change safely (edit → test → deploy), owner.
- Language: the user's (Arabic/English); screenshots or the HTML diagram for non-technical owners.
