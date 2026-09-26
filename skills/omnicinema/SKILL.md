---
name: omnicinema
description: Make brand and media assets with the user's omnicinema-mcp engine — logos (with reversed + icon variants), vector illustrations, app/web UI mockups, background music in a genre (WAV + editable MIDI), sound effects, voiceover, and short videos from a one-line idea (screenplay → stock footage or storyboard animatic → narration, captions, soundtrack → rendered MP4). Works fully offline and free; stock footage and AI photos/voices/music use the user's own API keys. Use for "make me a logo", "design a mockup of my app screen", "I need background music / a beat / a sound effect", "turn this script into a voiceover", "make a quick promo/animatic/storyboard video", or anything about OmniCinema. For real AI-generated film shots in Google Flow use flow-studio-director instead.
---

# OmniCinema

The user's own MCP server (github.com/joeshwoa/omnicinema-mcp), run as a
one-shot command — no MCP registration. `scripts/mcp_cli.mjs` starts the real
server, calls one tool, prints the result, exits.

## What it really makes

| Asset | Offline (free, default) | With the user's keys |
|---|---|---|
| Logo / vector art / UI mockup | Professional flat SVG + PNG (logos also `-reversed` and `-icon`) | same — no key needed |
| Photo / texture | a clearly labelled placeholder, **not a photo** | Replicate / Hugging Face image model (`generative: true`, costs quota) |
| Soundtrack | composed + synthesized stereo WAV (~−14 LUFS) + multi-track MIDI — a good demo, not a studio recording | MusicGen on Replicate/HF |
| Sound effect | 13 procedural recipes (whoosh, rain, thunder, wind, ocean, impact, riser, click, ding, beep, fire, footsteps, heartbeat) | real CC recordings from Freesound |
| Voiceover | system TTS (macOS `say`, flite, espeak-ng) — intelligible, robotic | natural voice via `HF_TTS_MODEL` |
| Video | screenplay + storyboard **animatic** (drawn frames, Ken Burns motion, captions, dissolves, VO, music) rendered to MP4 | real stock b-roll from Pexels/Pixabay/Unsplash (free keys); generative clips via Replicate/fal/HF |

Say which column the user is getting. Never call an animatic "footage" or a
placeholder "a photo".

## Setup (once, and after upgrades)

```bash
bash skills/omnicinema/scripts/bootstrap.sh                 # clone/update + build (Node ≥ 18.17)
bash skills/omnicinema/scripts/bootstrap.sh --with-render   # make sure the Remotion renderer is installed (usually already is; ffmpeg renders without it)
bash skills/omnicinema/scripts/bootstrap.sh --check         # installed? which media tools exist?
```
Needs `ffmpeg` for audio/video; `rsvg-convert` (librsvg) for PNG exports;
a TTS engine (`say` on macOS, or espeak-ng/flite) for voiceover.
Outputs go to `$CINEMA_ROOT` (`assets/`, `projects/`, `output/`). First use
picks `/Volumes/PortableSSD/omnicinema-mcp` when that drive is mounted, else
`~/AI-Projects/omnicinema`, and remembers it in
`~/.config/ai-skills/omnicinema.root` — quota counters and the IPC token
live there too, so it must not flip between drives. Tell the user the exact
file paths. Output files are named from the `subject`: a second call with
the same subject OVERWRITES the first — copy/rename each result (e.g.
`sofra_logo_emblem.svg`) before the next variation.

Paths below are relative to this skill's folder (the folder holding this
SKILL.md — in this repo `skills/omnicinema/`; adjust if installed elsewhere).

**API keys** (optional) go in `~/.cache/ai-skills/omnicinema-mcp/.env`
(copy `.env.example` there; git-ignored). The user edits that file
themselves — never ask them to paste keys into chat, never write keys
anywhere else. `list_providers` shows what is configured.

## Calling tools

```bash
bash skills/omnicinema/scripts/call.sh <tool> '<json>'     # readable result + file paths + next steps
bash skills/omnicinema/scripts/call.sh <tool> @args.json    # args from a file (long scripts, quotes, Arabic)
bash skills/omnicinema/scripts/call.sh --json <tool> ...     # raw MCP result
bash skills/omnicinema/scripts/call.sh --list                # every tool + arguments
```
Full catalog: `references/tools.md`. Recipes and style vocabulary:
`references/workflows.md`.

## How to work

1. **Pin down the request** (ask briefly, in the user's language, only what's
   missing): what it's for and where it will be used (sizes/ratio: 9:16 reel,
   16:9, 1:1), brand name/colours/mood, length (music/video), language of any
   spoken text, and whether they want to spend API quota or stay free.
2. **Write tool inputs in English** with the engine's vocabulary
   (`references/workflows.md`): the rule-based designers and screenplay
   engine read English keywords. Spoken text (`narration`, voiceover
   `script`) can be any language the TTS engine speaks — but offline TTS
   voices are English-first; for Arabic narration recommend the generative
   voice, or flow-studio-director's voice pipeline, and say why.
3. **Preview cheap first:** `consult_personas` for the design brief of a
   logo/music/voice; `run_cinema_pipeline` with `"dry_run": true` for videos
   (screenplay, shot list, providers, cost/network). Show it; adjust the
   prompt until the plan is right; then produce.
4. **Money gates:** `generative: true`, `approveOverBudget: true`,
   `enrich: true` (one Anthropic API call to polish a screenplay),
   `install_dependencies consent:true`, `approve_suggestion approve:true`
   only after the user explicitly agrees in chat to that specific spend or
   install. `check_limits` before a generative batch. Free stock APIs run
   automatically when their keys exist — pass `"stock": false` to stay
   fully offline.
5. **Check every output before presenting it:**
   `bash skills/omnicinema/scripts/check_media.sh <files…>` — then actually
   LOOK at the PNG previews (`*.check.png`) and video contact sheets
   (`*.contact.png`) with your image viewer. Fix and re-run anything that is
   off (wrong colours, cut text, silence, clipping, wrong ratio) before
   showing it. Read the tool's "Notes" too: an unmatched sound effect comes
   back as a generic impact WITH a warning — don't hand that over as the
   sound they asked for. Report real numbers (duration, LUFS, size).
6. **Hand over:** the files (paths), what each is, which column of the table
   above it came from, and the next improvement (e.g. "add a free Pexels key
   for real footage").

## Other jobs

- **Re-cut a video:** edit `montage-order.json` or replace clip files in the
  project folder, then `compile_montage`. For hands-on editing use
  `workflow_mode: "interactive_montage"`.
- **Serve assets to devuniverse / other local tools:**
  `bash skills/omnicinema/scripts/ipc.sh start` (localhost only, bearer
  token in `$CINEMA_ROOT/data`), `ipc.sh status`, `ipc.sh stop` when done.
  Never print the token. (The MCP tools `ipc_start`/`ipc_stop` die with the
  one-shot call — don't use them through `call.sh`.)
- **Find new video/AI providers:** `discover_providers` only queues
  candidates for review; nothing is installed or enabled automatically.

## Rules

- Offline first; spend only with explicit consent; say what is synthetic.
- Rights: no real people's likeness or voice, no existing logos, characters or
  songs — offer an original. Stock results carry attribution in
  `attributions.txt`; keep it with the delivery.
- Never present an output you haven't checked with `check_media.sh` and
  looked at.
