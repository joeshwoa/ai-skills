---
name: creative-studio
description: A whole content-creation team for the AI, built only on free/open-source tools the AI drives itself — branding (logo concepts, palette, Arabic+Latin type, guidelines PDF), graphic design (social posts, carousels, stories, thumbnails, posters, flyers, menus, business cards, print PDFs with bleed), Photoshop-style photo work (retouch, looks, background removal, upscaling, layered PSD/XCF masters), Illustrator-style vector (SVG compose, trace, outline, icon sets), Premiere-style video editing (JSON timeline → MP4 + editable Kdenlive project, transitions, captions, reframing, grading), After-Effects-style motion graphics (titles, lower thirds, logo reveals, kinetic type), audio (Egyptian-Arabic voiceover, transcription/captions, clean-up, mastering, music beds, SFX) and AI image/video generation (local ComfyUI/mflux or free services). Use for any request to design, brand, edit, animate, voice, caption, retouch, generate or "make content" for a business or social media — in Arabic or English — even when no tool is named, and whenever the user wants a result they can also open and edit in GIMP, Inkscape, Kdenlive, Audacity or Blender.
---

# Creative Studio

The user's own MCP server **studio-mcp** (github.com/joeshwoa/studio-mcp) — 110 tools in
eight departments plus housekeeping. Every tool runs free software headlessly (Chromium,
ffmpeg, MLT, GIMP, Inkscape, Pillow/OpenCV, faster-whisper, edge-tts, ComfyUI…), returns
**file paths + preview images + measured facts** (sizes, loudness, contrast, text fit), and
where a free desktop app exists it also writes that app's editable file so a human can take over.

| Team role | Department | Key tools |
|---|---|---|
| Brand designer | `brand` | `brand_create`, `brand_logo_concepts`, `brand_choose_logo`, `brand_apply`, `brand_guidelines` |
| Graphic designer | `design` | `design_create`, `design_carousel`, `design_resize`, `design_catalog`, `design_check` |
| Photo editor (Photoshop) | `photo` | `photo_retouch`, `photo_look`, `photo_remove_background`, `photo_upscale`, `photo_compose_layers` (PSD+XCF), `photo_mockup` |
| Illustrator | `vector` | `vector_compose`, `vector_trace`, `vector_export` (PDF/EPS/icon sets), `vector_text_to_outlines`, `vector_boolean` |
| Video editor (Premiere) | `video` | `video_edit` (timeline → MP4 + .kdenlive), `video_captions`, `video_reframe`, `video_grade`, `video_remove_silence`, `video_export` |
| Motion designer (After Effects) | `motion` | `motion_title_card`, `motion_lower_third`, `motion_logo_reveal`, `motion_kinetic_text`, `motion_cta`, `motion_render_html` |
| Sound engineer (Audition) | `audio` | `audio_voiceover`, `audio_transcribe`, `audio_clean`, `audio_master`, `audio_mix`, `audio_music`, `audio_sfx` |
| AI artist (Midjourney/Runway) | `ai` | `ai_backends`, `ai_generate_image`, `ai_edit_image`, `ai_upscale`, `ai_generate_video`, `comfyui_setup` |
| Studio manager | `system` | `studio_doctor`, `studio_install`, `open_in_app` |

Full argument reference: `references/tools.md`. Team recipes: `references/workflows.md`.
Registering it as an MCP server in Claude/Cursor/Antigravity: `references/mcp-setup.md`.
A complete worked run (brief → brand → post → menu → voiceover → logo reveal → reel):
`examples/qahwa_house_launch.md`.

## Setup (once, and after upgrades)

```bash
bash scripts/bootstrap.sh           # Python env + studio-mcp + headless Chromium (~1.5 GB)
bash scripts/bootstrap.sh --check   # what is installed, what is missing (with install commands)
bash scripts/selftest.sh            # proves it works (temp folder); --full adds brand, voice, Whisper
```
Needs Python ≥ 3.10 and git (macOS: `brew install python@3.12`). The environment goes on the
external SSD (`/Volumes/PortableSSD/creative-studio/.venv`) when it is mounted, else
`~/.cache/ai-skills/creative-studio/venv`; remembered in `~/.config/ai-skills/creative-studio.venv`.
Outputs, brand kits and AI models live in **STUDIO_HOME** — first use picks
`/Volumes/PortableSSD/creative-studio` when mounted, else `~/AI-Projects/creative-studio`, and
remembers it (`~/.config/ai-skills/creative-studio.root`). Tell the user where files landed.

Desktop apps and AI models are **not** installed by bootstrap. `studio_doctor` lists them;
`studio_install {"group": "apps"}` (or core/design/photo/video/audio/ai) shows exactly what would
be installed and its size — show that to the user and only call again with `"confirm": true`
after they agree. Same for `comfyui_setup` / `mflux_setup` (GBs of models).

Paths are relative to this skill's folder (in the ai-skills repo: `skills/creative-studio/`).

## Calling tools

If the MCP server is registered, call the tools directly. Otherwise use the CLI:
```bash
bash scripts/call.sh list [dept]                   # catalogue
bash scripts/call.sh help design_create            # full description + arguments
bash scripts/call.sh design_create '{"template":"headline","size":"ig_square","brand":"qahwa-house","content":{"headline":"..."}}'
bash scripts/call.sh --json video_edit @timeline_args.json   # args from a file; machine-readable result
```
Put Arabic or long arguments in a JSON file and pass `@file` (no shell-quoting accidents).

## How the team works (follow this order)

1. **Brief first.** Business, audience, language (Arabic/English/bilingual, Egyptian dialect for
   social), platforms and sizes, deadline, tone. Ask only what you cannot infer.
2. **Brand before assets.** If there is no kit, `brand_create` (pass `sector` when you know it:
   coffee, food, tech, finance, health, wellness, eco, education, kids, property, travel, luxury,
   heritage, sport, creative, logistics, community). It reads the brief into a curated palette,
   type pairing and subject marks (cup/bean for coffee, shield/bars for finance…). **Show the user
   `concepts.png` and let them choose** (`brand_choose_logo`); refine with `brand_update` /
   `brand_logo_concepts`. Every other tool then takes `brand=<slug>`.
3. **Make the assets** with the department tools, always `brand=<slug>` and one `project=<name>`
   so everything for a job lands in `STUDIO_HOME/projects/<name>/<dept>/`.
4. **LOOK at every preview** the tool returns (Read the PNG) before showing the user. Fix what
   you see: overflow, clashes, crops, empty slots, wrong language direction. Read `warnings` —
   they are measured problems (text not fitting, WCAG fails, audio cut, missing required field).
5. **Deliver** the final files plus the editable masters (`.design` folder, `.psd/.xcf`, `.svg`,
   `.kdenlive`, `.srt`), say where they are, and offer `open_in_app` for hand edits.

## Rules that keep quality high

- **Consent:** tools flagged I (installs) or $ (spends) must be dry-run first and confirmed by the
  user. N tools use the internet (Google Fonts, edge-tts voices, Pollinations) — fine by default.
- **Reels with burned captions:** design the still at `ig_story` with `"leave_bottom": 0.26` so
  captions never sit on the design's text; `captions.position: "bottom"`. A still of another shape
  is placed whole on a blurred fill (never cropped) unless you pass `fit: "cover"`.
- **Voiceover length:** a VO longer than the picture holds the last still automatically; if the last
  clip is video you get a "the audio is CUT" warning — lengthen a clip or add an end card.
- **Arabic:** RTL layout is automatic from the text. Social copy in Egyptian dialect, formal in MSA.
  Voices: `audio_voices` (ar-EG Salma/Shakir…). Whisper's Egyptian transcription is good, not
  perfect — read the `.srt` (or pass `words`/`srt` you wrote from the script) before burning in.
- **Kdenlive:** every edit also writes a `.kdenlive` checked by rendering it with melt; Arabic
  captions go into it as a transparent video track (MLT mis-shapes Arabic subtitles).
- **AI generation:** `ai_backends` first. Local = mflux/ComfyUI on the Mac (models on the SSD);
  otherwise Pollinations (free, online). Cinematic video with characters/dialogue/Arabic speech
  is handed off to the **flow-studio-director** skill (Google Flow) — `ai_generate_video` writes
  that brief. Every result states model + licence + commercial-use verdict: pass it on.
- **Print:** print sizes get 3 mm bleed + crop-marks PDF; CMYK only if Ghostscript is installed —
  tell the user to proof with the printer's profile.
- **Honesty:** logos are geometric/typographic systems — strong starting points a designer (or the
  user) should choose and refine; check trademarks. Offline music is a procedural bed, not a
  composer. Say so when it matters.

## Related skills (pick the right one)

- **flow-studio-director** — cinematic AI film in Google Flow (characters, dialogue, Veo 3.1).
  The studio hands such videos over and then edits/captions/brands the returned clips.
- **omnicinema** — the user's omnicinema-mcp engine: one-prompt promo animatics and genre music
  with MIDI. Use the studio for brand kits, layouts, photo/vector work and real timeline editing.
- **premium-presentations** — slide decks; take the palette/fonts from `brand_show`.
- **premium-subtitle-localization** — translating/localising subtitles; the studio burns them in.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `studio-mcp is not installed yet` | `bash scripts/bootstrap.sh` |
| `environment … not available (external drive not mounted?)` | mount PortableSSD, or `bootstrap.sh --venv ~/somewhere` |
| `Chromium for Playwright is not installed` | re-run bootstrap (sets `PLAYWRIGHT_BROWSERS_PATH`); for MCP registration pass that env var |
| `X is not installed … Fix: brew install …` | show the user the command/size; `studio_install` with confirm after they agree |
| Fonts fail offline | the first render of each Google font needs internet; afterwards cached in STUDIO_HOME/cache |
| Brand read the wrong sector | pass `sector=` explicitly, or `base_color=` for the client's colour |
| AI image too slow / fails | `ai_backends` explains the route; `comfyui_status`; smaller size; `backend:"pollinations"` |
