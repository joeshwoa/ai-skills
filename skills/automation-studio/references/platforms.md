# Other platforms — when, what converts, what to tell the user

Build and test in n8n first (the real engine runs the tests), then port. `auto.sh convert flow.json --to <p> -o out/`.

| | n8n | Make | Zapier | Power Automate | Pipedream | Activepieces | Node-RED |
|---|---|---|---|---|---|---|---|
| Model | nodes + items | modules + bundles, routers | linear steps + Paths | actions, conditions, scopes | code-first steps | pieces, branches | message flows |
| Self-host / free | yes (open source) | no / free tier | no / free tier | M365 licence | free tier | yes (open source) | yes (open source) |
| Pricing unit | executions (Cloud) | operations | tasks | runs / premium connectors | credits | tasks (cloud) | none |
| Webhook custom reply | yes | yes (Webhook response) | **no** | yes (premium) | yes (`$.respond`) | yes | yes |
| Code | JS / Python | limited (functions) | JS / Python steps | expressions only | Node / Python / Go / Bash | TypeScript | JS function nodes |
| AI agents | native (LangChain) | AI modules / agents | AI by Zapier, agents | Copilot / AI Builder | via code / AI steps | AI pieces | contrib nodes |
| Import from our converter | — | **blueprint JSON** | build guide | build guide | build guide | build guide | **flows.json (runs)** |

## Node-RED (`--to node-red`)
Output: `<name>.node-red.json` + `NODE_RED_NOTES.md`. Import: menu → Import → select file → Deploy.
- Webhook → `http in` + `http response`; Schedule → `inject` (interval or crontab); HTTP Request → `http request`
  wrapped by function nodes; Set / IF / Filter / Switch / Code / Split Out / Aggregate / Limit / Merge /
  Remove Duplicates (with flow context for "seen before") / Respond to Webhook → function nodes running a small
  **n8n-compatible runtime** (items, `$json`, `$('Node')`, `{{ }}` expressions, n8n condition operators).
- Loop Over Items → loop body runs once with all items (add a `delay` node in rate-limit mode if needed).
- App nodes (Sheets, Slack, AI …) → clearly marked TODO pass-through: install the matching `node-red-contrib-*`
  package or call the app's REST API with `http request`.
- Verified: patterns 01 and 08 return byte-identical responses in Node-RED 4 and n8n (incl. idempotency over 2 calls).

## Make.com (`--to make`)
Output: `<name>.make-blueprint.json` + `MAKE_GUIDE.md` (module table + what to finish by hand).
Import: Scenarios → Create a new scenario → ⋯ → **Import Blueprint** → Save.
- Core modules (validated with Make's own schema/module validators): Webhooks `gateway:CustomWebHook`,
  `gateway:WebhookRespond`; HTTP `http:ActionSendData` (v3); `util:SetVariables`, `util:FunctionSleep`;
  `builtin:BasicRouter` (+ filters per route, case-insensitive operators when n8n was), `builtin:BasicFeeder`
  (iterator), `builtin:BasicAggregator`.
- Expressions are translated to Make formulas: `$json.x` → `{{2.x}}` (the module that produced x),
  `.trim()` → `trim()`, `.toLowerCase()` → `lower()`, `a || "d"` → `ifempty(a; "d")`, `.replace(/re/g,"")` →
  `replace(…; /re/g; "")`, `Math.round` → `round`, `.length` → `length()`, `.includes` → `contains()`,
  `.slice` → `substring()`, `Number()` → `parseNumber(…; ".")`, comparisons/arithmetics, `$now` → `now`,
  `$execution.id` → `executionId`. Anything else is marked **⚠ TRANSLATE** and listed in the guide.
- App nodes become named placeholders with the exact Make module to use (e.g. `google-sheets:addRow (v2)`,
  `slack:CreateMessage (v4)`, `telegram:SendReplyMessage`, `google-email:ActionSendEmail (v2)`,
  `openai-gpt-3:CreateCompletion`). Forms/chat triggers → custom webhook (use Tally/Google Forms/Typeform).
- IF "else" → second route; set it as **fallback route** in Make. Schedules are a scenario setting.
- With the **Make connector** in this chat you can: validate blueprints (`validate_blueprint_schema`,
  `validate_module_configuration`), list app modules, and — only with the user's explicit OK — create the
  scenario (`scenarios_create`) and run it once (`scenarios_run`). The user's connections are made in Make's UI.

## Zapier (`--to zapier`)
Guide: trigger app/event, each action with field mappings, Filter/Paths for branches, Looping by Zapier,
Code by Zapier (ready-to-paste JS with an n8n-style `$input` shim). Limits to tell the user: no custom webhook
responses (Catch Hook replies 200 immediately), each action = a task (cost), polling triggers every 1–15 min
by plan, multi-step + Paths need paid plans.

## Microsoft Power Automate (`--to power-automate`)
Guide with Condition/Switch/Apply to each/Compose/Response; **no JavaScript** — logic is rebuilt with
expressions (`triggerBody()?['email']`, `toLower()`, `formatDateTime(utcNow(),'yyyy-MM-dd')`). HTTP and the
"When an HTTP request is received" trigger are **premium**. Best when the company lives in Microsoft 365.

## Pipedream (`--to pipedream`)
Guide + Node.js steps (`defineComponent({ async run({ steps, $ }) { … } })`), `$.respond()` for webhook
replies, `$.flow.exit()` to stop. Developer-friendly; connected accounts hold credentials.

## Activepieces (`--to activepieces`)
Guide with Branch/Router/Loop and Code pieces (TypeScript `export const code = async (inputs) => {…}`).
Open source, self-hostable with Docker — the closest alternative to n8n.

## Choosing (when the user asks)
- Non-technical team, simple app-to-app, budget OK → Zapier.
- Visual, complex branching, cheaper per operation → Make.
- Microsoft 365 company, SharePoint/Teams/Outlook → Power Automate.
- Developers, code-heavy, event sources → Pipedream.
- Own server / data control / AI agents / unlimited runs → **n8n** (or Activepieces).
- IoT, hardware, local LAN devices → Node-RED.
