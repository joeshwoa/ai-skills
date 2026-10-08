# Testing — prove it works before anyone relies on it

`auto.sh test flow.json flow.cases.json` runs each case in a throw-away local n8n (real engine, the same
version that will run in production when possible). No account, server or credentials needed.

## What happens per case
- The trigger is replaced by a Manual Trigger + a Code node **with the trigger's name** emitting the case's
  `trigger` items → `$json` and `$('Trigger name')` behave as in production.
- Nodes that need credentials or reach outside (app nodes, AI roots, Wait, Execute Workflow, send email, SSH,
  files …) become Code nodes with the same name returning the case's `mocks` (or passing items through).
  AI sub-nodes of mocked roots are removed.
- Respond to Webhook passes items through (like the real node) and its **status + body are captured** and
  shown on the node (`{"status": 201, "response": {...}}`).
- HTTP Request without credentials runs **live** unless mocked (`mock_http: true` or a mock for that node).
  Any node can be forced live with `"live": ["Node"]` (e.g. an AI node when the user has provided a key).
- `"runs": 2` executes the same sandbox twice and checks the last run → proves dedupe/idempotency.
- Everything else (IF, Switch, Set, Code, Merge, Loop, Split Out, Aggregate, Filter, Sort, Date & Time,
  Crypto, XML/HTML/Markdown, Extract from File, Remove Duplicates …) runs for real.

## cases.json
```json
{"cases": [{
  "name": "valid lead is saved and gets 200",
  "trigger": {"body": {"email": "A@B.co"}, "headers": {}, "query": {}},
  "mocks": {"Add to Leads sheet": [{"id": 1}], "Ask AI": [{"output": "positive"}]},
  "passthrough": ["Wait 1h"],
  "live": ["Get weather"], "mock_http": false,
  "env": {"API_BASE": "https://example.com"},
  "runs": 1,
  "expect": {"status": "success",
    "nodes": {"Clean lead": {"json": {"email": "a@b.co"}},
              "Valid email?": {"output": 0, "items": 1},
              "Reply 400": {"ran": false},
              "Summary": {"contains": "3 leads"},
              "Parse": {"error": "Unexpected API response"},
              "Rows": {"min_items": 10}}}
}]}
```
- `trigger`: object, list of objects, or `[{"json":…, "binary":…}]`. Webhook triggers produce
  `{headers, params, query, body}`; forms produce `{<Field label>: value, submittedAt}`; Error Trigger produces
  `{execution:{…}, workflow:{…}}`; Execute Workflow Trigger produces the declared inputs.
- Binary mocks: `{"json":{}, "binary":{"data":{"data":"<base64>","mimeType":"application/pdf","fileName":"x.pdf"}}}`
  (pattern 10 tests real PDF text extraction this way).
- `json` is a subset match on item 0 of the chosen output; `contains` searches all items' JSON text.

## The minimum test set (QA checklist)
1. Happy path end to end. 2. Every IF/Switch branch (one case each). 3. Invalid / missing input → the
error/400 path. 4. External failure: mock an error-shaped response (`[{"error":"timeout"}]`) and check the
flow fails loudly or routes to the failure path. 5. Empty list → nothing sent. 6. Duplicates (`runs: 2`).
7. Volume: 100–500 generated items (Python one-liner in the case file generator). 8. Arabic/Unicode text.

## Reading results
`✅/❌ case → status`, then per node `out [items per output]` + the first item, then each assertion with
`(got: …)` when it fails. `--json` for machine-readable output, `--keep` to keep the sandbox for debugging.
Offline machines: `AUTOKIT_OFFLINE=1` skips cases that use `live`.

## After deploy (live checks)
- Webhooks: `auto.sh trigger --target local --path orders --data '{"…"}' -H 'Idempotency-Key: k1'` → shows the
  HTTP reply and the per-node summary of the execution.
- Schedules/app triggers: `auto.sh executions --target T --id <workflowId> --limit 3`.
- Use test resources (a test sheet/channel/inbox) for the first live runs; switch to production after.

## Other platforms
- Node-RED: run the converted flow in Node-RED and call it with curl (same payloads as the n8n cases).
- Make: Make's scenario "Run once" with the same sample payload; check each module's bundle.
- Zapier/Power Automate/Pipedream/Activepieces: their editor's "Test step" per step with the case data.
