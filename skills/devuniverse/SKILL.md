---
name: devuniverse
description: Scaffold a new Flutter app (optionally with a Supabase/Firebase backend, a Fastify service and a 3D deep-scroll journey) from a plain-language brief using the user's devuniverse-mcp "virtual agency" — a rule-based persona bench debates the stack, then it writes a project that compiles and passes its own tests, with ADRs, wireframes, a Figma plugin, RLS migrations or Firebase rules, and draft privacy/terms docs. Use for "start a new app", "scaffold a Flutter project", "set up an app with Supabase/Firebase", "add a 3D scroll journey to my app", "re-theme my app from these images", "audit my app before release", "generate privacy policy / terms for my app", or anything about DevUniverse.
---

# DevUniverse

The user's own MCP server (github.com/joeshwoa/devuniverse-mcp), run as a
one-shot command — no MCP registration. `scripts/mcp_cli.mjs` starts the real
server, calls one tool, prints the result, exits. Nothing is re-implemented
here, so the skill never drifts from the server.

**What it is:** 27 deterministic personas (rules, not LLMs) score the brief's
signals (accounts, offline, payments, teams, chat, search, GDPR, 3D…), vote,
and record dissent; the scaffold follows those rulings. Same brief → same
project. **What it is not:** a finished product. Payments are a stub
(`docs/PAYMENTS.md`), the offline write-queue has no server sync yet, there
are no golden or RLS-policy tests, and nothing is deployed. Say so when
you present a project.

## Setup (once, and after upgrades)

```bash
bash skills/devuniverse/scripts/bootstrap.sh          # clone/update + build into ~/.cache/ai-skills
bash skills/devuniverse/scripts/bootstrap.sh --check  # what's installed, which toolchains exist
```
Needs Node ≥ 20. Checking the generated app needs Flutter ≥ 3.44 (Dart 3.12).
Projects are written to `$DEVUNIVERSE_ROOT/projects/<slug>`. First use picks
`/Volumes/PortableSSD/devuniverse-mcp` when that drive is mounted, else
`~/AI-Projects/devuniverse`, and remembers it in
`~/.config/ai-skills/devuniverse.root` (so nothing splits if the drive is
unplugged later — you get a clear error instead). Set `DEVUNIVERSE_ROOT` for
one call to put a project elsewhere. Tell the user where it landed.

Paths below are relative to this skill's folder (the folder holding this
SKILL.md — in this repo `skills/devuniverse/`; adjust if installed elsewhere).

## Calling tools

```bash
bash skills/devuniverse/scripts/call.sh <tool> '<json>'   # readable report
bash skills/devuniverse/scripts/call.sh <tool> @args.json  # args from a file (long briefs, quotes, Arabic)
bash skills/devuniverse/scripts/call.sh --json <tool> ...   # raw MCP result
bash skills/devuniverse/scripts/call.sh --list              # every tool + arguments
```
Full catalog: `references/tools.md`. Recipes: `references/workflows.md`.

## New app — the workflow (follow in order)

1. **Get the brief right — it drives every decision.** If the request is
   thin, ask briefly (in the user's language): product name; who it's for;
   must-have features; offline?; payments/subscriptions?;
   teams/multi-tenant?; chat/realtime?; search?; 3D/immersive?; markets
   (GDPR/EU)?; backend preference (Supabase/Firebase)? Put the answers
   into the `description` as plain **English** words, even when the user
   writes in Arabic — the bench scores English keywords only (list in
   `references/workflows.md`), so an Arabic brief silently gets a bare app.
   Avoid words that trip signals by accident (§1 there: "company", "assets",
   "pricing", "live"…). Decisions the user has already made go in as
   **mandates**, not brief words: `"backend": "supabase"|"firebase"`,
   `"state_management": "riverpod"|"bloc"`, `"service": true|false` — the
   bench still argues, the ruling follows the user, and the transcript
   records both. Pick `project_type` from the table below. Pass `name`
   when the user has one.
2. **Plan first:** call `init_dev_universe` with `"dry_run": true`. Show the
   user the rulings table, the dependencies and the file count, and point out
   any decision that looks wrong for their case (e.g. Firebase when they
   want Supabase → re-run the dry run with `"backend": "supabase"`). Every
   app except `three_d_experience` gets accounts (sign-in, settings,
   delete-account); there is no "no backend" option. Wait for OK.
3. **Generate:** same call without `dry_run`.
4. **Prove it works:** `bash skills/devuniverse/scripts/verify_project.sh <project_dir>`
   — adds android/ios folders, `flutter pub get/analyze/test`, the Node
   service's install/tsc/test/build, the RLS check, and `audit_compliance`.
   Never tell the user it compiles or passes unless this printed PASS; list
   every NOT RUN line as unverified. Don't repeat the report's "watching
   app/assets/incoming" line — the watcher dies with the one-shot call; run
   `verify_assets` yourself after adding images. If something fails, read the log, fix
   the project (or report the server bug), and re-run.
5. **Hand over:** where it is, what was decided and why (one line each, from
   the rulings), what is real vs stub, the exact next commands from the
   tool's "Next steps", and what the user must supply (Supabase URL +
   publishable key via `--dart-define-from-file=.env`, or
   `flutterfire configure`; company details for the legal drafts).

| project_type | When |
|---|---|
| `flutter_app` | a mobile app (default) |
| `full_stack` | app + backend service / webhooks / integrations |
| `flutter_spatial_app` | app whose core experience is a 3D deep-scroll journey |
| `three_d_experience` | a 3D showcase with no accounts |
| `backend_api` | backend + Fastify service only, no Flutter app |
| `custom` | none of the above fits; the brief decides |

## Other jobs

- **Add the 3D journey to an existing devuniverse project:** `generate_spatial_module`
  with `project_dir` (it patches `pubspec.yaml`), then add the `GoRoute` it
  prints to `app/lib/router/app_router.dart` (otherwise the journey is
  unreachable), then `verify_project.sh`.
- **Re-theme from brand art:** copy images into `app/assets/incoming/`, call
  `verify_assets`, then `sync_figma` (tokens changed) and `verify_project.sh`.
  It themes from the LARGEST image in `incoming/` + `generated/` — move
  generated images aside first if the brand art is smaller.
  Show the new palette and the WCAG notes from `docs/ADAPTATION_REPORT.md`.
- **Legal drafts with real details:** `generate_compliance_docs` with
  company_name / contact_email / governing_law. Always say: drafts for a
  lawyer to review, not legal advice.
- **Before a release / after adding packages or permissions:** `audit_compliance`.
- **"Make it feel like this site/video":** `ingest_reference` (patterns only,
  never copies artwork); `apply_theme: true` only after the user agrees.
- **Figma:** `sync_figma` → SVG wireframes + a development plugin that builds
  editable frames (the Figma REST API cannot create designs).
- **Generated media (images/audio) for the app:** needs the omnicinema skill
  running as a service (`ipc.sh`) — see "Linking OmniCinema" in
  `references/workflows.md`, then `generate_media_asset` (`kind` image or
  audio; `texture` is only a labelled placeholder without an image API key).

## Rules

- Dry run before writing; verify before claiming.
- `provision_omnicinema` with `confirm: true` clones, installs and runs code:
  only after the user explicitly says yes in chat. Prefer the omnicinema
  skill's own `bootstrap.sh` + `scripts/ipc.sh` (see workflows).
- Never write real keys into the project; `.env` stays git-ignored
  (`.env.example` is the template).
- Compliance docs are drafts, audits are static scans — never "you are compliant".
- Don't hand-edit generated files to hide a server bug: fix the project and
  tell the user the server needs the same fix (and offer to make it in
  devuniverse-mcp).
