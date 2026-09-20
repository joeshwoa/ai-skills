---
name: devuniverse
description: Scaffold a production-grade Flutter + Supabase/Firebase/Node project via a 27-persona virtual engineering agency that debates the stack, generates a 3D deep-scroll spatial UI module, syncs Figma wireframes, runs a compliance/security audit, and drafts Terms/Privacy docs — by running the real devuniverse-mcp server as a one-shot local command, no MCP client registration required. Use for "scaffold a new app", "start a Flutter project", "generate the 3D spatial canvas module", or anything about the DevUniverse agency.
---

# DevUniverse (skill form)

This is the real `devuniverse-mcp` server (github.com/joeshwoa/devuniverse-mcp)
— every capability, unmodified — reached without registering it as an MCP
server anywhere. Same mechanism as the `omnicinema` skill in this repo:
`scripts/mcp_cli.mjs` starts the real server fresh, does the MCP handshake,
calls exactly one tool, prints the JSON result, and exits.

## Workflow

1. **First use only — bootstrap it:**
   ```bash
   bash skills/devuniverse/scripts/bootstrap.sh
   ```
   Clones (or updates) `devuniverse-mcp` into
   `~/.cache/ai-skills/devuniverse-mcp` and builds it (this one builds
   clean from a fresh clone — verified). Safe to re-run any time.

2. **Read `references/tools.md`** for the full tool catalog (every tool's
   exact name and JSON argument shape, extracted from the real
   `src/server.ts`).

3. **Call a tool:**
   ```bash
   bash skills/devuniverse/scripts/call.sh <tool_name> '<json-args>'
   ```
   Examples:
   ```bash
   bash skills/devuniverse/scripts/call.sh get_agency_roster '{}'
   bash skills/devuniverse/scripts/call.sh init_dev_universe '{"project_type":"flutter_spatial_app","description":"a meditation app with a 3D deep-scroll journey through calming rooms"}'
   bash skills/devuniverse/scripts/call.sh generate_spatial_module '{"project_dir":"projects/<slug>","depth_layers":5}'
   bash skills/devuniverse/scripts/call.sh audit_compliance '{"project_dir":"projects/<slug>"}'
   ```
   The result prints as JSON; the human-readable report is in
   `.content[0].text`.

4. **`init_dev_universe` is the real starting point** for a new project —
   it runs the full agency debate, scaffold, Figma sync, compliance
   audit, and asset watcher in one call, and writes everything under
   `projects/<slug>/` inside the devuniverse-mcp cache dir (change
   working directory with `AI_SKILLS_CACHE_DIR` if you want the cache,
   and therefore generated projects, somewhere else).

5. **Anything that clones/installs/runs code on the user's machine**
   (`provision_omnicinema` with `confirm:true`) needs the user's explicit
   go-ahead in conversation first — the tool itself only gates on the
   flag, so the confirming has to happen before you pass it.

6. **Compliance docs are drafts, not legal advice** — `generate_compliance_docs`
   says so in its own output; don't present them to the user as final.

## Linking to the omnicinema skill

`init_dev_universe` with `use_omnicinema:true` (and `provision_omnicinema`,
`omnicinema_status`, `generate_media_asset`) bridge to a linked OmniCinema
install. If the `omnicinema` skill in this same repo is bootstrapped too,
point devuniverse at it however its own detection expects (see
`omnicinema_status`'s output for the exact search paths/overrides it
checks) rather than guessing a path.
