---
name: omnicinema
description: Generate cinematic video (multi-scene screenplay + footage + Remotion render), design assets (logos, vector art, textures, UI mockups), voiceover, music, and SFX — by running the real omnicinema-mcp server as a one-shot local command, with no MCP client registration required. Use for "make a video / short film / trailer", "generate a logo / design asset", "generate voiceover / music / sound effect", or anything about the OmniCinema pipeline.
---

# OmniCinema (skill form)

This is the real `omnicinema-mcp` server (github.com/joeshwoa/omnicinema-mcp)
— every capability, unmodified — reached without registering it as an MCP
server anywhere. `scripts/mcp_cli.mjs` is a small generic MCP stdio client:
it starts the real server fresh, does the MCP handshake, calls exactly one
tool, prints the JSON result, and exits. No long-lived server process, no
editing Claude/Cursor's MCP config — just a shell command, like any other
skill script. Because it talks nothing but the protocol to the real,
unmodified server code, there is no duplicated logic to drift out of sync.

## Workflow

1. **First use only — bootstrap it:**
   ```bash
   bash skills/omnicinema/scripts/bootstrap.sh
   ```
   Clones (or updates) `omnicinema-mcp` into `~/.cache/ai-skills/omnicinema-mcp`
   and builds it. Safe to re-run any time to pick up upstream changes.

   > **Known upstream issue:** as of the last check, a fresh clone of
   > omnicinema-mcp fails to build (`Cannot find module '../assets/...'`)
   > because the repo's own `.gitignore` has a bare `assets/` rule that
   > also swallows `src/assets/` real source files — they were never
   > committed. `bootstrap.sh` detects this and prints the exact one-line
   > fix (anchor the gitignore rule to `/assets/`, then `git add -f
   > src/assets`) for the repo owner to push upstream. This is a bug in
   > omnicinema-mcp itself, not in this skill — nothing here needs to
   > change once it's fixed.

2. **Read `references/tools.md`** for the full tool catalog (every tool's
   exact name and JSON argument shape, extracted from the real
   `src/server.ts` — nothing paraphrased or guessed).

3. **Call a tool:**
   ```bash
   bash skills/omnicinema/scripts/call.sh <tool_name> '<json-args>'
   ```
   Examples:
   ```bash
   bash skills/omnicinema/scripts/call.sh list_providers '{}'
   bash skills/omnicinema/scripts/call.sh consult_personas '{"assetKind":"logo","subject":"a fox reading a book","style":"minimalist"}'
   bash skills/omnicinema/scripts/call.sh generate_image '{"assetKind":"logo","subject":"a fox reading a book"}'
   bash skills/omnicinema/scripts/call.sh run_cinema_pipeline '{"prompt":"a lonely lighthouse keeper watches a storm roll in","style":"noir","sceneCount":4}'
   ```
   The result prints as JSON; the human-readable summary is in
   `.content[0].text`.

4. **For anything that costs money or calls a real external API**
   (`generative:true` on any generate_* tool, `install_dependencies` with
   `consent:true`, `approve_suggestion` with `approve:true`), tell the
   user exactly what will run/cost before passing that flag — these tools
   are explicit-flag-gated by design specifically so no confirmation UI is
   needed, but that means the confirming has to happen in conversation
   instead.

5. **Without any provider keys configured**, everything still works using
   local placeholders and offline synthesis (vector art renders as real
   SVG, music/voiceover/SFX synthesize locally) — good enough to preview
   structure, timing, and layout before spending on generative APIs. See
   `references/tools.md`'s last section for how to add keys.

## Honesty

- `discover_providers` / `approve_suggestion` never auto-integrate
  anything; a new provider still needs a human-reviewed adapter.
- Budget guards on generate_* tools are real — an over-quota call halts
  with a cost breakdown rather than silently spending; only proceed past
  that with the user's explicit go-ahead.
- `ipc_start` only lives for the one-shot process here (see
  `references/tools.md`) — it's not useful as a persistent local API
  through this skill's call path.
