# devuniverse-mcp — tool catalog

Generated from the live server's tools/list (devuniverse-mcp 6655a3a). Regenerate after upgrading: `bash scripts/call.sh --list` (summary) or `--json --list` (full schemas). Descriptions are the server's own words.

## init_dev_universe
Start here to create a new app project from a plain-language brief. The rule-based persona bench debates the stack (Supabase/Firebase, Riverpod/Bloc, offline layer, 3D renderer, service layer…), then the tool writes projects/<slug>/: a Flutter app wired to those rulings (auth screens, go_router, settings with account deletion, checkout stub when payments are mentioned, offline layer, 3D journey when spatial) that passes flutter analyze/test as generated; Supabase migrations with RLS or Firebase rules; an optional Fastify service with tests; ADRs, a meeting transcript, wireframes, and draft compliance docs. backend_api projects get no Flutter app. Returns the rulings, cross-examination results, and the exact commands to run next. Use dry_run: true first to show the user the plan without writing anything.

Arguments:
- `project_type` (required) — string one of flutter_app, flutter_spatial_app, full_stack, backend_api, three_d_experience, custom: flutter_app (mobile app) · flutter_spatial_app (app + 3D deep-scroll journey) · full_stack (app + backend) · backend_api (backend + service only, no Flutter app) · three_d_experience (3D showcase, no accounts) · custom.
- `description` (required) — string: Plain-language brief. Keywords steer the debate: accounts/sign-in, offline, chat/realtime, search, payments/subscriptions/Stripe, teams/multi-tenant, GDPR, 3D/glTF, webhooks/integrations, bloc.
- `name` — string: Product name. Omit to derive one from the brief (quoted name, 'called X', or a short noun phrase).
- `dry_run` — boolean (default false): Return the debate, rulings, and file list without writing anything to disk.
- `use_omnicinema` — boolean (default false): Route the media pipeline through the OmniCinema companion (detected/linked automatically).
- `style_preferences` — array: Manual design preferences blended by the synthesis engine, e.g. ["glassmorphism", "dark", "luxury"].
- `backend` — string one of supabase, firebase: Client mandate: use this backend whatever the bench prefers (its pick stays in the transcript).
- `state_management` — string one of riverpod, bloc: Client mandate for Flutter state management.
- `service` — boolean: Client mandate: true = add the Fastify service layer, false = no service.

## get_agency_roster
List the persona bench that debates every project (names, titles, focus areas). Read-only; use it to explain who argued what in a MEETING_TRANSCRIPT.md. Personas are deterministic rules, not LLM agents.

Arguments:

## generate_spatial_module
Add the 3D deep-scroll journey (scroll-driven Z-axis camera, parallax layers, starfield, snap rooms, reduced-motion fallback; optional glTF model stage and Rive HUD) to a project that init_dev_universe created without it, or emit it standalone. Writes lib/spatial/*.dart; when project_dir has an app/, it also adds the needed dependencies and asset folders to app/pubspec.yaml. Returns the files written and how to route to JourneyPage. Not needed for flutter_spatial_app projects — init already includes it.

Arguments:
- `project_dir` — string: Existing devuniverse project to write into (files land under app/). Omit to create a standalone module.
- `project_name` — string (default "Spatial Canvas"): Display name used inside the journey.
- `mesh_renderer` — string one of model_viewer_plus, flutter_scene: glTF stage: model_viewer_plus (stable Flutter) or flutter_scene (needs Flutter master).
- `rive` — boolean (default false): Include the Rive HUD overlay seam.
- `depth_layers` — integer (default 5): 

## verify_assets
Use after the user adds images to app/assets/incoming/ (or generated/): analyzes them (format, size, dominant palette) and re-derives the app theme tokens (colors, brightness, spacing, radii) in design-tokens.json and app/lib/theme/design_tokens.dart. Returns the new palette and changed files; details and WCAG contrast checks go to docs/ADAPTATION_REPORT.md.

Arguments:
- `project_dir` (required) — string: A generated devuniverse project directory.

## watch_assets
Start or stop automatic theme adaptation: while watching, any image dropped into app/assets/incoming/ re-runs verify_assets. init_dev_universe starts one per project for the life of this server process. Call without project_dir to list active watchers.

Arguments:
- `project_dir` — string: 
- `enabled` — boolean (default true): 

## omnicinema_status
Only relevant if the user has the optional OmniCinema media-generator companion. Detects it (OMNICINEMA_PATHS or default paths), checks its local IPC health, and returns CASE A (installed; IPC health reported) or CASE B (not installed: the repo pointer plus the CASE C offer to provision it), with next steps.

Arguments:

## provision_omnicinema
CASE C: "Would you like devuniverse-mcp to automatically clone, install dependencies, and link OmniCinema-MCP for 100% free cinematic assets? [y/N]" — with confirm: true this clones the pinned OMNICINEMA_REPO_URL, runs npm install + build, starts the IPC service detached (logged to data/logs/), and syncs the bearer token from data/ipc-token.txt. Refuses unpinned repository URLs.

Arguments:
- `confirm` (required) — boolean: Explicit consent to clone, install dependencies, and run the companion tool. Must be true.

## generate_media_asset
CASE A: request an image/texture/audio/video from the linked OmniCinema loopback API, save it into app/assets/generated/ with a provenance manifest entry, and re-adapt the theme to the new material. Requires omnicinema_status to report CASE A.

Arguments:
- `project_dir` (required) — string: 
- `kind` (required) — string one of image, texture, audio, video: 
- `prompt` (required) — string: What to generate, e.g. 'nebula background, deep violet, 4k'.
- `file_name` — string: 
- `adapt` — boolean (default true): Re-run theme adaptation after saving (images only).

## sync_figma
Regenerate the design artifacts for a project's screens (the same screens the app's router has): SVG wireframes in design/wireframes/ (drag into Figma), a Figma development plugin that rebuilds them as editable frames, and, in handoff mode, a comment on a Figma file (needs FIGMA_TOKEN). init_dev_universe already runs this once; use it again after verify_assets changes the tokens. The Figma REST API cannot create designs, so the plugin is the editable path.

Arguments:
- `project_dir` (required) — string: 
- `mode` — string one of wireframes, plugin, handoff, all (default "plugin"): 
- `figma_file_key` — string: Figma file key (from its URL) — required for handoff mode.

## ingest_reference
Use when the user shares a site or screen recording they want the app to feel like. Extracts patterns only — palette, fonts, tech/interaction fingerprint (three.js, GSAP, scroll-snap…), structure — and returns a rebuild plan mapped onto devuniverse modules; writes references/<source>/REPORT.md. Videos need ffmpeg. Never copies artwork or trade dress. apply_theme: true also blends the palette into the tokens.

Arguments:
- `project_dir` (required) — string: 
- `url` — string: Public page you have the right to study.
- `video_path` — string: Local video file demonstrating the desired interaction.
- `apply_theme` — boolean (default false): 

## scan_extension_marketplace
Maintenance tool, unrelated to a specific project: searches GitHub and Hugging Face for recently published MCP servers / dev packages and appends them to data/dev-review-queue.json as pending_human_review with risk flags (no license, low adoption, suspicious install scripts). Never installs anything. Returns counts and the queue path.

Arguments:
- `limit` — integer (default 20): 
- `sources` — array: 

## generate_compliance_docs
Regenerate compliance/PRIVACY_POLICY.md, TERMS_OF_SERVICE.md and STORE_COMPLIANCE_CHECKLIST.md for an existing project, e.g. to fill in company_name / contact_email / governing_law (init already writes drafts with placeholders). Content follows the project's data categories (accounts, payments, media…). Structured drafts for counsel review, not legal advice.

Arguments:
- `project_dir` (required) — string: 
- `company_name` — string: 
- `contact_email` — string: 
- `governing_law` — string: e.g. "Ireland" or "Delaware, USA"

## audit_compliance
Run before a release or after adding dependencies/platform folders: static scan of a project for committed credentials and .env files, plaintext http:// endpoints, tracker SDKs needing disclosure, sensitive Android permissions, empty iOS usage strings, and missing policy docs. Writes compliance/AUDIT_REPORT.md; returns the top findings and fails (isError) on any high-severity finding.

Arguments:
- `project_dir` (required) — string: 

