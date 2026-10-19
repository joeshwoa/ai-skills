# What the improvement reports contain, and what they never do

Purpose: find where the skills fall short so they can be fixed for everyone. It is automatic and on by default so the library improves without anyone filing anything; it is disclosed here, in the README and in BOOTSTRAP.md, and it has a one-line opt-out.

## Sent
| Field | Values | Why |
|---|---|---|
| skill | folder name of the skill | which skill to fix |
| event | gap, failure, wrong_info, suggestion, new_skill_request, success_note | kind of problem |
| outcome | success, partial, failure | how the task ended |
| agent | claude, cursor, gemini, antigravity, windsurf, chatgpt, codex, copilot, other | which agent family has the issue |
| surface | cli, desktop, web, mobile, ide, api, other | where it runs |
| os | macos, windows, linux, ios, android, other, unknown | environment-specific bugs |
| skill_version | short git commit of the library | which version had the problem |
| tags | up to 5 from a fixed list | clustering |
| gap / suggestion | generic text, 300 / 500 characters max | what to improve |
| install_id | random UUID created on first use, stored locally, not derived from the person, device or account | de-duplicate and cap abuse |
| received_at | set by the server | ordering |

## Never sent
Names, emails, usernames or handles, phone numbers, IP addresses (the function does not read or store them), URLs and domains, file names and paths, prompts, conversation text, file contents, brand or client names, credentials or tokens, location, device identifiers, browsing history.
The sender redacts these patterns; the server rejects (does not store) any report that still matches them.

## Controls
- Opt out: `AI_SKILLS_TELEMETRY=off`, `DO_NOT_TRACK=1`, or create `~/.config/ai-skills/telemetry-off`.
- Preview: `scripts/report.py --dry-run ...` prints the exact payload.
- Reset identity: delete `~/.config/ai-skills/install-id`.
- Status: `scripts/report.py --status`.
- Deletion: reports are not linkable to a person; to remove reports from a given installation send its install ID to the maintainer.

## Storage and access
One database table; the public API keys cannot read or write it. Only the `ingest` function can insert, and only the maintainer can read. Raw reports are reviewed monthly and deleted after 12 months (maintainer commitment; aggregated counts may be kept).
Server code: `backend/ingest/index.ts`. Schema: `backend/migration.sql`.
