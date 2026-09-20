# devuniverse-mcp — full tool catalog

Every tool below is real, unmodified devuniverse-mcp functionality
(source: `joeshwoa/devuniverse-mcp`, `src/server.ts`). Call any of them
with:

```bash
bash scripts/call.sh <tool_name> '<json-args>'
```

## init_dev_universe

The unified entry point. Convenes the 27-senior virtual agency for a new
project: parses requirements, debates and votes the stack
(Supabase/Firebase/Node, Riverpod/Bloc, spatial 3D core, mesh renderer,
offline layer…), synthesizes a design language, generates the full
scaffold (Flutter app, backend, RLS migrations, Dockerfiles, CI,
Terms/Privacy docs), cross-examines every artifact, compiles Figma-ready
wireframes, runs the compliance audit, and starts the asset watcher.
Everything lands under `projects/<slug>/` with the full meeting
transcript.

| field | type | notes |
|---|---|---|
| `project_type` | enum, required | one of `flutter_app`, `flutter_spatial_app` (enables the deep-scroll 3D canvas), `full_stack`, `backend_api`, `three_d_experience`, `custom` |
| `description` | string, required, min 8 chars | plain-language brief; keywords steer the debate (3d, offline, chat, payments, multi-tenant, gdpr…) |
| `use_omnicinema` | boolean | route the media pipeline through the OmniCinema companion (default false) |
| `style_preferences` | array of strings | e.g. `["glassmorphism", "dark", "luxury"]` |

## get_agency_roster

List the 27 senior personas that debate every project: names, titles,
focus areas. No arguments.

## generate_spatial_module

Emit the immersive 3D deep-scroll Flutter module code (scroll-driven
Z-axis camera, Matrix4 perspective parallax layers, CustomPainter
starfield, snap-point rooms, reduced-motion fallback; optional
flutter_scene/flutter_cube mesh stage and Rive HUD).

| field | type | notes |
|---|---|---|
| `project_dir` | string | existing devuniverse project to write into (files land under `app/`); omit to create a standalone module |
| `project_name` | string | default "Spatial Canvas" |
| `mesh_renderer` | `"flutter_scene"` \| `"flutter_cube"` | optional |
| `rive` | boolean | include the Rive HUD overlay seam; default false |
| `depth_layers` | int 2–8 | default 5 |

## verify_assets

Analyze art in the project's asset drop zones (format, dimensions,
dominant palette) and re-derive design tokens (colors, brightness,
padding grid, radii). Writes `docs/ADAPTATION_REPORT.md` with WCAG
contrast verification.

| field | type | notes |
|---|---|---|
| `project_dir` | string, required | a generated devuniverse project directory |

## watch_assets

Start/stop the watcher on `app/assets/incoming` — any dropped image
re-runs verification and theme adaptation automatically. Call without
`project_dir` to list active watchers.

| field | type | notes |
|---|---|---|
| `project_dir` | string | omit to list active watchers |
| `enabled` | boolean | default true |

## omnicinema_status

Detect the OmniCinema companion on this machine (well-known SSD paths +
overrides), check its loopback IPC health, report CASE A/B/C state and
next steps. No arguments.

## provision_omnicinema

CASE C: auto-provision OmniCinema. With `confirm:true`, clones the
pinned OmniCinema repo, runs npm install + build, starts the IPC service
detached, and syncs the bearer token. Refuses unpinned repository URLs.
**Always get the user's explicit go-ahead before passing `confirm:true`**
— this clones and runs code on their machine.

| field | type | notes |
|---|---|---|
| `confirm` | boolean, required | must be `true` |

## generate_media_asset

CASE A: request an image/texture/audio/video from the linked OmniCinema
loopback API, save it into `app/assets/generated/` with a provenance
manifest entry, and re-adapt the theme to the new material.

| field | type | notes |
|---|---|---|
| `project_dir` | string, required | |
| `kind` | enum, required | `image` \| `texture` \| `audio` \| `video` |
| `prompt` | string, required, min 3 chars | e.g. "nebula background, deep violet, 4k" |
| `file_name` | string | optional |
| `adapt` | boolean | re-run theme adaptation after saving (images only); default true |

## sync_figma

Compile the roundtable's screen plan into design artifacts: SVG
wireframes, a generated Figma development plugin (auto-layout + tokens),
and an optional REST handoff comment (needs `FIGMA_TOKEN`). Note: the
Figma REST API cannot create designs — the plugin is the actual
editable-draft path.

| field | type | notes |
|---|---|---|
| `project_dir` | string, required | |
| `mode` | `"wireframes"` \| `"plugin"` \| `"handoff"` \| `"all"` | default `plugin` |
| `figma_file_key` | string | from the Figma file's URL; required for handoff mode |

## ingest_reference

Reverse-engineer the *patterns* (never the protected artwork/trade
dress) of a reference the user provides: palette, typography,
framework/interaction fingerprint (three.js, GSAP ScrollTrigger,
scroll-snap, WebGL…), structure, and a rebuild plan mapped onto
devuniverse modules. Videos get ffmpeg keyframe + palette analysis when
ffmpeg is present.

| field | type | notes |
|---|---|---|
| `project_dir` | string, required | |
| `url` | string | a public page the user has the right to study |
| `video_path` | string | local video demonstrating the desired interaction |
| `apply_theme` | boolean | blend the extracted palette into project tokens; default false |

## scan_extension_marketplace

Crawl GitHub and Hugging Face for recently published MCP servers / dev
packages, log them to `data/dev-review-queue.json` as
`pending_human_review` (risk flags: missing license, low adoption,
suspicious install patterns). Nothing is ever auto-installed.

| field | type | notes |
|---|---|---|
| `limit` | int 1–50 | default 20 |
| `sources` | array of `"github"` \| `"huggingface"` | optional |

## generate_compliance_docs

Draft a complete Terms of Service, GDPR/CCPA Privacy Policy, and store
compliance checklist from the project's actual data categories.
Documents carry a review-by-counsel banner — **structured drafts, not
legal advice**. Requires `init_dev_universe` to have run first
(`blueprint.json` with signals).

| field | type | notes |
|---|---|---|
| `project_dir` | string, required | |
| `company_name` / `contact_email` / `governing_law` | string | optional, e.g. governing_law: "Ireland" |

## audit_compliance

Static scan of a project for liabilities: committed credentials,
plaintext endpoints, undisclosed tracker SDKs, sensitive permissions,
missing policy documents. Writes `compliance/AUDIT_REPORT.md` with
severity-ranked findings.

| field | type | notes |
|---|---|---|
| `project_dir` | string, required | |

## Notes

- `init_dev_universe` with `use_omnicinema:true` bridges to the
  omnicinema skill in this same repo (`skills/omnicinema/`) when it's
  installed — bootstrap that one too if you want the media pipeline
  linked in.
- Every write-side tool resolves paths and refuses anything outside the
  project's own managed root (`assertInsideManagedRoots` in the real
  server) — that safety check is untouched by this wrapper.
