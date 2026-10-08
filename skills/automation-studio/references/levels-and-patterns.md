# Levels and patterns — from easy to complex

Pick the lowest level that fully solves the problem. Each level adds techniques on top of the previous.

| Level | Shape | Techniques | Tested patterns |
|---|---|---|---|
| 1 Simple | 1 trigger → 1–3 actions | app trigger / webhook / schedule, field mapping, Respond to Webhook | 01 |
| 2 Branching | transform + decisions | Set, IF, Switch (named outputs + fallback), Filter, Code for one-off logic, forms | 01, 02, 03, 04 |
| 3 Robust bulk | many items, unreliable APIs | Split Out, Loop Over Items (batches) + Wait, pagination, retries, continue-on-error, Aggregate, error workflow | 05, 06, 07 |
| 4 Stateful / intelligent | events repeat, unstructured data, AI | idempotency keys + dedupe across runs, upsert, Data Tables/DB, AI Agent + tools + memory, extractors, documents | 08, 09, 10 |
| 5 Systems | people, many workflows, scale | Wait / send-and-wait approvals, sub-workflows with typed inputs, orchestration, queue mode, versioned deploys | 11, 12 |

## Choosing building blocks
- **Trigger**: app trigger (polling or webhook) if the node exists → generic Webhook (+ auth) → Schedule (poll an API with "since last run" via dedupe or a stored cursor) → Form/Chat trigger for humans → Execute Workflow Trigger for sub-flows → Error Trigger for the error workflow → Manual for one-offs.
- **Many items**: n8n runs each node once per item automatically. Use Loop Over Items only when you need batching/pacing or per-item sub-steps that must finish before the next item.
- **Fan-out → fan-in**: parallel branches into Merge (append / combine by key / by position) with inputs 0..N-1.
- **Wait**: fixed time, until a date, or until a webhook call / form submit (approvals).
- **Errors**: node setting `onError: continueRegularOutput | continueErrorOutput` for expected per-item failures; workflow error workflow for the unexpected; Stop and Error to fail deliberately with a clear message.
- **State**: Remove Duplicates (seen keys, up to a history size), Data Tables (n8n built-in tables), Postgres/Supabase for real data, Redis for locks/counters, workflow static data only for small cursors.
- **AI**: Text Classifier / Sentiment / Information Extractor / Basic LLM Chain for single-shot tasks; Agent for tool use; vector store + embeddings for RAG; always validate model output.

## Common recipes (build from patterns)
| Need | Start from | Change |
|---|---|---|
| Website form → CRM + Slack | 01 or 03 | swap Sheets for HubSpot/Pipedrive/Zoho node, add Slack |
| Daily report from an API/DB | 02 | swap HTTP for Postgres/Sheets read, Code builds the table, email or Slack |
| New item in source X → copy to Y, never twice | 04 / 08 | dedupe on the source id; upsert in target |
| Sync two systems nightly | 05 | read changed since last run, upsert, report counts |
| Send bulk messages respecting limits | 06 | batch size = provider limit / minute, Wait between batches |
| Alert on every failure | 07 | set as error workflow everywhere |
| Payment/order webhook (Stripe, Paymob, Shopify) | 08 | verify signature in Code, idempotency on event id |
| WhatsApp/Telegram/website chatbot | 09 | Telegram/WhatsApp trigger or chat trigger, tools for your data |
| Invoices/CVs/forms from PDFs or email attachments | 10 | Gmail trigger with attachments, Extract from File, extractor schema |
| Approvals (expenses, leave, content) | 11 | Slack/Telegram/Gmail send-and-wait, timeouts, escalation |
| Many similar jobs per customer/product | 12 | orchestrator + sub-workflow, failures counted |
