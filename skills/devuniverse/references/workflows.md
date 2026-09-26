# DevUniverse — recipes and details

All commands assume `S=skills/devuniverse/scripts`.

## 1. What steers the debate (write these words into `description`, in English)

The bench scores the brief with whole-word keyword rules
(`src/agency/signals.ts` in devuniverse-mcp). A signal counts only if its
words appear — so translate the user's needs into these words, and keep
the accidental ones out.

| Signal | Trigger words | What it changes |
|---|---|---|
| Offline | offline, local-first, sync/syncing, airplane mode, poor connectivity | drift cache + write queue (Firestore cache on Firebase); pushes the vote toward Firebase |
| Realtime | real-time, chat, collaboration/collaborative, multiplayer, presence, live chat/updates/feed/scores/tracking/location/stream, live cursors | weighs the backend vote; "messages" in the privacy policy |
| Teams / B2B | multi-tenant, tenant(s), organization(s), team(s), workspace(s), B2B, SaaS, agency, company | strong push toward Supabase |
| Payments | payment(s), subscription(s), billing, Stripe, checkout, e-commerce, shop, marketplace, pricing | checkout screen stub + docs/PAYMENTS.md; favours the Fastify service |
| Compliance | GDPR, HIPAA, PCI, SOC2, compliance, audit / audit trail, regulated | privacy counsel favours Supabase (region-pinned hosting, RLS); GDPR/CCPA sections in the drafts |
| Search | search, full-text, discover/discovery, filter/filtering, faceted | pushes toward Supabase (Postgres full-text) |
| Notifications | notification(s), push, reminder(s), alert(s) | pushes toward Firebase (FCM); push is not wired into the app |
| Server work | webhook(s), integration(s), third-party API, cron, background job(s), worker(s), PDF generation, server-side | Fastify service with tests + Dockerfile (payments, heavy media and AI also favour it) |
| AI | AI, ML, LLM, GPT, Claude, embedding, recommendation, semantic | favours the service; AI-prompt section in the privacy drafts |
| Heavy media | video, audio, cinematic, film, render/rendering, asset(s), animation(s), gallery, portfolio, media, sound, music | favours the service; cinematic design lean; "media uploads" in the privacy drafts |
| 3D | 3D, three-d, spatial, immersive, parallax, depth effect/layers/scroll, z-axis, deep scroll, camera fly/dive/travel, tunnel, universe, galaxy, planet | spatial journey module |
| 3D models | glTF, GLB, mesh(es), 3D model, modeling, Blender, .obj, USDZ, skybox, texture(s) | model stage (model_viewer_plus) |
| Scale | million(s), high traffic, scale, viral, global launch | weighs infrastructure choices |
| Bloc | bloc, cubit, enterprise team, large team | Bloc instead of Riverpod (or use the mandate) |
| Lightweight 3D | lightweight, simple 3D, quick preview, minimal | lighter 3D choices |
| Lottie | lottie | Lottie instead of Rive for micro-interactions |
| Platforms | iOS/iPhone/iPad/App Store, Android/Play Store, web/browser/PWA, desktop/macOS | store checklist targets; none named → iOS + Android + web |

Always true, whatever the words: every project type except
`three_d_experience` gets accounts (auth screens, settings, sign-out,
delete-account). Every Supabase project gets the same migration: profiles,
organizations, organization_members, assets, audit_log — all with RLS and a
`delete_my_account()` function.

**Words to avoid** (they switch on a signal nobody asked for): company /
agency / teams (multi-tenant) · assets / sound / film / render / gallery
(heavy media → service) · pricing / shop (payments + service) · texture
(3D model stage) · planet / universe / tunnel (3D) · alert / reminder
(Firebase lean) · "minimal" (lightweight 3D). Rephrase: "a small business"
not "a company"; "images" not "assets".

**Mandates beat words.** When the user has decided, pass them instead of
hoping the words tip the vote:
`"backend": "supabase" | "firebase"`, `"state_management": "riverpod" |
"bloc"`, `"service": true | false`. The report marks those rows "client
mandate" and the transcript keeps the bench's own pick and arguments.

Name: pass `"name"`; otherwise it takes a quoted name, "called/named X", or a
short noun phrase from the brief.

Good brief (English, concrete, no accidental words):
> A recipe sharing app called "Sofra" for Egyptian home cooks. Cooks sign up,
> save favourite recipes offline, and search by ingredient. Launching in
> Egypt and the EU, so GDPR matters. iOS and Android.

## 2. New project, end to end

```bash
cat > /tmp/brief.json <<'JSON'
{"project_type":"flutter_app","name":"Sofra","backend":"supabase","dry_run":true,
 "description":"A recipe sharing app called \"Sofra\" for Egyptian home cooks. Users sign up, save favourite recipes offline, search by ingredient. GDPR matters. iOS and Android."}
JSON
bash $S/call.sh init_dev_universe @/tmp/brief.json          # plan: show the user
# after OK: same file with "dry_run": false
bash $S/call.sh init_dev_universe @/tmp/brief.json
bash $S/verify_project.sh <the "Project directory" the report printed>   # must end with PASS lines
```
A captured dry run is in `examples/dry_run_sofra.md`.

What to tell the user afterwards (short): location; the rulings that matter
to them (backend, state management, offline, service or not) with the
one-line reason from the transcript; verification results; stubs (payments,
offline sync to server, no golden/RLS-policy tests); what they must supply
(`.env` from `.env.example`: SUPABASE_URL + SUPABASE_PUBLISHABLE_KEY, or
`flutterfire configure`); the next commands (`flutter run` works in demo mode
with in-memory accounts before any backend exists).

## 3. Verify an existing project

```bash
bash $S/verify_project.sh <project_dir>                   # android+ios, all checks
bash $S/verify_project.sh <project_dir> --platforms web   # other targets
bash $S/verify_project.sh <project_dir> --no-platforms    # don't run flutter create
```
Not covered (say so): `docker build`, device/emulator runs, store builds,
running the migrations on a real Postgres (`cd backend && supabase init &&
supabase start && supabase db reset`), Firebase rules (emulator), live
Supabase/Firebase projects.

## 4. Add the 3D journey later

```bash
bash $S/call.sh generate_spatial_module '{"project_dir":"<dir>","project_name":"Sofra Journey","mesh_renderer":"model_viewer_plus","depth_layers":5}'
# then add the GoRoute the tool prints to app/lib/router/app_router.dart
bash $S/verify_project.sh <dir> --no-platforms
```
Without the route the journey compiles but can't be reached — check it.
`flutter_scene` needs Flutter's master channel — only if the user asks for it.

## 5. Re-theme from brand images

Copy the user's logo / key art into `<dir>/app/assets/incoming/`, then:
```bash
bash $S/call.sh verify_assets '{"project_dir":"<dir>"}'
bash $S/call.sh sync_figma '{"project_dir":"<dir>","mode":"all"}'
bash $S/verify_project.sh <dir> --no-platforms
```
Show the palette it derived and any contrast warnings in `docs/ADAPTATION_REPORT.md`.
The theme comes from the largest image across `incoming/` and `generated/`:
if the report names a generated image, move it out and run `verify_assets`
again. (The report's "watching incoming/" only lasts for that one call.)

## 6. Legal drafts and release audit

```bash
bash $S/call.sh generate_compliance_docs '{"project_dir":"<dir>","company_name":"…","contact_email":"…","governing_law":"Egypt"}'
bash $S/call.sh audit_compliance '{"project_dir":"<dir>"}'
```
Drafts for a lawyer; the audit is a static scan (secrets, http://, trackers,
Android permissions, iOS usage strings, missing policies) — not a certificate.

## 7. Linking OmniCinema (generated images/audio inside the app)

The omnicinema skill must be installed and its asset API running:
```bash
bash skills/omnicinema/scripts/bootstrap.sh
bash skills/omnicinema/scripts/ipc.sh start          # prints the exports below
export CINEMA_ROOT=… OMNICINEMA_PATHS=~/.cache/ai-skills/omnicinema-mcp OMNICINEMA_API_URL=http://127.0.0.1:8787
bash $S/call.sh omnicinema_status                    # expect CASE A
bash $S/call.sh generate_media_asset '{"project_dir":"<dir>","kind":"image","prompt":"calm teal waves background","file_name":"hero"}'
bash skills/omnicinema/scripts/ipc.sh stop           # when done
```
`kind`: image (offline vector art) or audio (soundtrack). `texture` without
an image API key is a labelled PHOTO PLACEHOLDER — don't ship it, and don't
let it re-theme the app. Video is refused (make it with omnicinema's
`run_cinema_pipeline`). The omnicinema MCP tools `ipc_start`/`ipc_stop`
don't persist through `call.sh` — always use `ipc.sh`. Files land in
`app/assets/generated/` with a provenance `manifest.json`; images re-tune the
theme. Soundtracks are large WAVs — convert to AAC/OGG before shipping.

## 8. Troubleshooting

| Symptom | Fix |
|---|---|
| `isn't installed yet` | run `bootstrap.sh` |
| offline/payments/teams missing from the rulings | the brief lacked the English words in §1 |
| a ruling the user doesn't want (e.g. Firebase) | pass the mandate (`"backend": "supabase"`) |
| surprise 3D / service / multi-tenant | an accidental word (§1 "Words to avoid") |
| `flutter analyze` errors in a fresh project | server bug: capture the log, report it, fix in devuniverse-mcp (it is the user's repo) |
| `pub get` fails on versions | Flutter older than 3.44 — `flutter upgrade` |
| CASE B from omnicinema_status | omnicinema not installed / env not exported (§7) |
| token rejected (401) | `CINEMA_ROOT` differs between ipc.sh and this shell |
| `Storage guard: refusing to write outside managed roots` | the project is outside `$DEVUNIVERSE_ROOT` — set it to the folder that contains `projects/` |
| "Output folder … is not available" | the remembered root is on an unmounted drive: mount it or set `DEVUNIVERSE_ROOT` |
