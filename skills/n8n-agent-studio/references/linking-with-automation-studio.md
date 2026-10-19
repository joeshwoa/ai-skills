# How n8n-agent-studio and automation-studio work together

| Need | Skill / command |
|---|---|
| Draw the process, pick triggers/nodes, build/test/deploy any n8n flow | automation-studio (`auto.sh …`) |
| Reach a system without an API; recipes; browser agent; MCP bridge; hosting browserd | n8n-agent-studio (`nx.sh …`) |
| `nx build/test/validate/deploy/creds/diagram/nodes/convert/pull/list/trigger/executions` | pass-through to automation-studio's engine — identical results |

Handoffs
- automation-studio meets "the app has no API" → switch to this skill: `nx probe` / `nx ladder`, then come back with a browserd HTTP node as just another step.
- This skill builds a flow → uses automation-studio's patterns for sinks (`patterns/01-webhook-lead-to-sheet`), error workflow, approval, AI support agent (`09`), credentials walkthroughs, platform converters (Make/Zapier… can call the same browserd URL through their HTTP modules).
- Same test file format (`cases.json`), same `selftest.sh` idea, same secrets file (`web_secrets` key added next to `n8n_api_keys`).

Local + published together (typical for Joshua)
1. Build & test on the Mac (A). 2. Move the n8n flow to a server/Cloud (B/C) only after tests pass; keep browserd where the logged-in sessions are. 3. Claude/Cursor connect to either through the MCP bridge (pattern 03) — a way to *operate* flows by chat.
4. Claude in Chrome / computer-use (as the operator) is the discovery tool during build (find the hidden API, draft the recipe), n8n+browserd is the unattended runtime.
