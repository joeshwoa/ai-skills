# omnicinema-mcp — full tool catalog

Every tool below is real, unmodified omnicinema-mcp functionality (source:
`joeshwoa/omnicinema-mcp`, `src/server.ts`). Call any of them with:

```bash
bash scripts/call.sh <tool_name> '<json-args>'
```

Arguments are the exact same JSON shape the MCP tool takes — nothing has
been reinterpreted or simplified. Optional fields can be omitted.

## run_cinema_pipeline

Generate a multi-scene screenplay with shot-to-shot frame continuity,
acquire matching footage (official stock APIs, opt-in bring-your-own-key
generative providers, or generated placeholders), assemble a
frame-accurate Remotion timeline, validate it, and optionally render an
MP4. `workflow_mode:"interactive_montage"` pauses after asset acquisition
so a human can arrange clips before compiling.

| field | type | notes |
|---|---|---|
| `prompt` | string, required | the video concept |
| `workflow_mode` | `"fully_automated"` \| `"interactive_montage"` | default `fully_automated` |
| `sceneCount` | int 1–12 | default derived from the prompt |
| `shotsPerScene` | int 1–6 | default 2 |
| `shotDurationSeconds` | number 1–30 | default 4 |
| `fps` | int 1–120 | default 30 |
| `width` / `height` | int | default 1920×1080 |
| `style` | string | e.g. "noir", "documentary", "neon cyberpunk" |
| `prefer` | `"video"` \| `"image"` | motion b-roll vs. stills |
| `generative` | boolean | opt in to bring-your-own-key generative video |
| `render` | boolean | render the MP4 now (default true in fully_automated) |
| `narration` | string | optional voiceover script, locked to the timeline |
| `soundtrack` | boolean | add an offline-synthesized music bed |
| `musicStyle` | string | e.g. "lo-fi", "cinematic orchestral", "hip-hop" |

## compile_montage

Resume an interactive project: rebuild the timeline from the project
directory (honoring an optional `montage-order.json`), validate it, and
render.

| field | type | notes |
|---|---|---|
| `projectId` | string, required | from `run_cinema_pipeline` |
| `render` | boolean | default true |

## install_dependencies

Detect the host OS and install missing multimedia dependencies (Remotion,
ffmpeg, Blender). Requires explicit consent — `consent:false` only
previews the plan.

| field | type | notes |
|---|---|---|
| `consent` | boolean | must be `true` to actually install; default false |
| `targets` | array of `"remotion"` \| `"ffmpeg"` \| `"blender"` | default all |

## list_providers

List the curated asset/generative providers from `tools-registry.json`
with live configured status. No arguments.

## discover_providers

Scan official public catalogs (Hugging Face Hub, GitHub Search) for
candidate video tools and append them to `discovery-suggestions.json` for
human review. Never auto-integrates or executes anything found.

| field | type | notes |
|---|---|---|
| `query` | string, required | e.g. "text to video", "seedance" |

## approve_suggestion

Explicitly promote a reviewed discovery suggestion into
`tools-registry.json`. Added disabled and unimplemented — a human still
has to write an adapter and enable it.

| field | type | notes |
|---|---|---|
| `suggestionId` | string, required | from `discover_providers` |
| `approve` | boolean | must be `true`; default false |

## consult_personas

Run the multi-agent persona consultation for an asset kind and return the
compiled PromptBrief (positive/negative prompt, technical params, debate
transcript) WITHOUT generating anything. Use to preview/tune strategy.

| field | type | notes |
|---|---|---|
| `assetKind` | enum, required | `cinematic-photo` \| `logo` \| `vector-art` \| `texture` \| `ui-mockup` \| `voiceover` \| `soundtrack` \| `sfx` |
| `subject` | string, required | the subject/description |
| `style` | string | optional style hint |
| `aspectRatio` | string | e.g. "16:9", "1:1", "9:16" |

## generate_image

Create a cinematic photo, transparent logo, vector art, texture, or UI
mockup. Vector kinds render as real SVG offline; photoreal kinds use a
configured image API when `generative:true`, else a local placeholder.
Budget-guarded — an over-quota request halts with a cost breakdown; retry
with `approveOverBudget:true`.

| field | type | notes |
|---|---|---|
| `assetKind` | enum, required | `cinematic-photo` \| `logo` \| `vector-art` \| `texture` \| `ui-mockup` |
| `subject` | string, required | what to create |
| `style` / `aspectRatio` | string | optional |
| `generative` | boolean | use an official image API (needs a configured key) |
| `approveOverBudget` | boolean | proceed despite a budget-guard flag |

## generate_voiceover

Generate spoken narration. Uses a configured TTS API when
`generative:true`, else a local placeholder. Returns an exact millisecond
duration. Budget-guarded.

| field | type | notes |
|---|---|---|
| `subject` | string, required | topic, or the narration script itself |
| `script` | string | explicit script overriding subject |
| `style` | string | e.g. "dramatic", "calm documentary" |
| `generative` / `approveOverBudget` | boolean | optional |

## generate_soundtrack

Compose a full instrumental across genres. The Music Producer persona
plans BPM/key/structure/instrumentation. Renders via a configured
MusicGen API when `generative:true`, else deterministic local synthesis
(WAV + editable MIDI). Budget-guarded.

| field | type | notes |
|---|---|---|
| `subject` | string, required | theme/mood, e.g. "rainy midnight city" |
| `style` | string | genre, e.g. "hip-hop", "lo-fi" |
| `generative` / `approveOverBudget` | boolean | optional |

## generate_sfx

Produce a sound effect / ambience. Uses the Freesound API when
`generative:true`, else a local synthesized transient. Budget-guarded.

| field | type | notes |
|---|---|---|
| `subject` | string, required | e.g. "whoosh transition", "rain ambience" |
| `style` / `generative` / `approveOverBudget` | | optional |

## check_limits

Report per-provider free-tier usage (daily/weekly/monthly) from
`data/usage-limits.json`.

| field | type | notes |
|---|---|---|
| `provider` | string | omit for all tracked providers |

## ipc_start / ipc_status / ipc_stop

Start/check/stop the localhost-only REST API (bound to 127.0.0.1) so
another local tool can request assets programmatically. `ipc_start` takes
an optional `port` (defaults to `OMNICINEMA_IPC_PORT` or 8787); the other
two take no arguments. Note: because `call.sh` runs the server as a
one-shot process, an `ipc_start` call here starts the IPC server for the
lifetime of that single process only — it exits with the call. For a
persistent IPC server, run the omnicinema-mcp server directly
(`node <cache>/dist/index.js` under a real MCP client, or `npm start`).

## Provider keys (needed for anything with `generative:true`)

See `tools-registry.json` in the cache dir for the full list. Each
provider needs its own env vars (e.g. `PEXELS_API_KEY`,
`REPLICATE_API_TOKEN` + `REPLICATE_VIDEO_MODEL`, `FAL_API_KEY` +
`FAL_VIDEO_MODEL`, `HUGGINGFACE_API_TOKEN` + a model id,
`FREESOUND_API_KEY`, etc.). Put them in a `.env` file at the cache dir
root (`~/.cache/ai-skills/omnicinema-mcp/.env` by default) — never paste
real keys into chat or into this repo. Without any keys configured,
everything still works using local placeholders/synthesis; only
`generative:true` calls need them.
