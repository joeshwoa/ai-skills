# OmniCinema — recipes, vocabulary, checks

All commands assume `S=skills/omnicinema/scripts`. Inputs in English (the
designers and screenplay engine are keyword-driven). Every recipe ends with
`check_media.sh` and looking at the preview.

## 1. Vocabulary the engines understand

**Colours (logos, art, mockups):** hex codes in `style` win
(`"style":"#0f766e #f59e0b luxury"`), then colour words, whole words (red, orange, amber,
gold, yellow, lime, green, emerald, olive, teal, turquoise, cyan, sky, blue,
navy, indigo, violet, purple, magenta, pink, rose, brown, coffee, beige,
cream, sand, black, charcoal, grey, silver, white), then moods: warm/sunset ·
earth/nature/eco · mono/minimal/noir · vibrant/playful/neon · else blue. With
NO style at all the default is "clean minimal" → a mono grey palette — always
pass colours or a mood.
For vector art, colour words in the subject count too ("teal waves").

**Logo layout:** monogram / initials / badge / crest / seal → monogram;
wordmark; horizontal (use `aspectRatio: "3:1"`); emblem. Without a layout
word it picks emblem or monogram (seeded by the name) — name the layout.
**Type voice:** luxury/elegant/premium/classic/serif/fashion → serif premium;
tech/mono/minimal/brutal/future → geometric tech; playful/fun/kids/friendly →
rounded playful. Note "monogram" contains "mono", which also selects the
tech type voice — add "luxury" or "playful" when that's wrong.
**Corners:** "sharp"/"brutal" → sharp.
Logo `subject` = the brand name (+ optional tagline words); keep it short.

**UI mockup screen** (from the subject): dashboard/analytics/admin/console ·
shop/store/cart/checkout/catalog · landing/homepage/website/SaaS/portfolio ·
app/mobile/iOS/Android/fitness/music/wallet → phone screens · sign-in/login →
auth · chat/inbox. Phone content is themed for fitness, finance and music;
other domains get a generic tasks layout — say so, it is a layout mockup,
not the user's real screens.

**Video look** (prompt + style): noir/detective · storm/rain/thunder ·
neon/cyberpunk · night/midnight/moon · dawn/sunrise · sunset/golden/warm/
desert · snow/winter/cold/icy · forest/nature/garden/morning · else cinematic.
**Video prompt shape:** `a <subject> <verb-ing> … in/at <setting> at <time>`,
e.g. "a street food vendor in Cairo opening his cart at dawn". Proper nouns
keep their capital letter. One subject per film works best.

**Music genre** (whole words, `style` first, then subject): hip hop/boom ·
trap/rap · orchestral/cinematic/epic/score · rock/metal/punk · lo-fi/chill/
jazzy · EDM/electronic/house/techno/synth · otherwise ambient score. Put the
genre in `style`; confirm with `--json` (`meta`/arrangement shows the genre). `durationSeconds` sets length
(re-flowed to whole bars).

**Sound effects (offline, whole words):** thunder · rain · ocean/waves ·
wind · whoosh/transition/swipe · riser/build/tension · impact/hit/boom/
explosion · ding/chime/success/coin · beep/alarm/countdown · click/tap/UI/
typing · fire/crackle · footsteps · heartbeat. Anything else (door knock,
glass breaking, train horn) renders a generic impact plus a warning — use
Freesound (`generative:true`, free key) for those.

**Voiceover delivery (`style`):** dramatic · calm documentary · energetic.

## 2. Brand kit (logo + variants + colours)

```bash
bash $S/call.sh consult_personas '{"assetKind":"logo","subject":"Sofra","style":"#0f766e #f59e0b warm playful"}'   # show the brief
A="${CINEMA_ROOT:-$(cat ~/.config/ai-skills/omnicinema.root)}/assets"   # where outputs land
bash $S/call.sh generate_image  '{"assetKind":"logo","subject":"Sofra","style":"#0f766e #f59e0b emblem playful"}'
for f in "$A"/sofra_logo*; do mv "$f" "${f/sofra_logo/sofra_logo_emblem}"; done   # keep it: the next call overwrites
bash $S/call.sh generate_image  '{"assetKind":"logo","subject":"Sofra","style":"#0f766e #f59e0b wordmark playful","aspectRatio":"3:1"}'
for f in "$A"/sofra_logo.* "$A"/sofra_logo-*; do mv "$f" "${f/sofra_logo/sofra_logo_wordmark}"; done
bash $S/check_media.sh "$A"/sofra_logo_*.svg
```
Deliver: main SVG + PNG, `-reversed` (dark backgrounds), `-icon` (app icon /
favicon; SVG only — export a PNG with `rsvg-convert -w 1024`), the hex
palette. Offer 2–3 layout options side by side rather than one. Text uses installed fonts (not outlined) — for print, convert text to
outlines in a vector editor.

## 3. App / web mockup

```bash
bash $S/call.sh generate_image '{"assetKind":"ui-mockup","subject":"Sofra recipe mobile app","style":"#0f766e #f59e0b"}'
```
Good for pitch decks and landing pages. For real app screens, build them
(devuniverse skill) and screenshot.

## 4. Music, SFX, voiceover

```bash
bash $S/call.sh generate_soundtrack '{"subject":"warm kitchen morning","style":"lo-fi","durationSeconds":30}'
bash $S/call.sh generate_sfx '{"subject":"soft UI click"}'
cat > /tmp/vo.json <<'JSON'
{"subject":"promo","script":"Before the city wakes, the fire is already lit.","style":"calm documentary"}
JSON
bash $S/call.sh generate_voiceover @/tmp/vo.json
bash $S/check_media.sh <the WAV paths from each tool's "Files:" list>
```
Targets: music ≈ −14 LUFS, VO ≈ −16 LUFS, peaks below −1 dBTP, no long
silences. The MIDI is editable in any DAW — offer it to musicians.
Offline VO is robotic; for a client-facing voice, use `generative:true`
(HF_TTS_MODEL, with consent) or record a human.

## 5. Video (animatic or stock b-roll)

```bash
cat > /tmp/film.json <<'JSON'
{"prompt":"a street food vendor in Cairo opening his cart at dawn",
 "sceneCount":3,"shotsPerScene":2,"shotDurationSeconds":3,"width":1080,"height":1920,
 "narration":"Before the city wakes, Amm Hassan lights the fire.",
 "soundtrack":true,"musicStyle":"ambient","dry_run":true}
JSON
bash $S/call.sh run_cinema_pipeline @/tmp/film.json      # plan: scenes, shots, stock queries, cost
# edit the prompt/params until the plan is right, then set "dry_run": false
bash $S/check_media.sh <the MP4 path the tool printed>   # then LOOK at <mp4>.contact.png
```
Sizes: 1080×1920 reels/shorts · 1920×1080 YouTube · 1080×1080 feed.
Without stock keys the result is an animatic (drawn frames) — ideal for
pitching or timing a script, not a final ad. With a free `PEXELS_API_KEY`
the same run pulls real b-roll (check `attributions.txt`). Re-cut: create `projects/<id>/montage-order.json` — a
JSON array of the `src` file names from `timeline.json`, in the new order
(missing ones are appended) — or swap clip files, then
`compile_montage {"projectId":"<id>"}`. The title card and first caption
stay at the start. For real AI film shots with
characters and dialogue, hand over to flow-studio-director.

## 6. Keys, quotas, providers

- Keys: `~/.cache/ai-skills/omnicinema-mcp/.env` (from `.env.example`),
  edited by the user. Free: Pexels, Pixabay, Unsplash, Freesound. Paid /
  quota: Replicate, fal, Hugging Face.
- `list_providers` — what's configured. `check_limits` — usage vs budget
  guard. A budget halt returns the cost breakdown: show it and ask.
- `discover_providers {"query":"text to video"}` queues candidates only;
  `approve_suggestion` adds a DISABLED entry that still needs a human-written
  adapter.

## 7. Serving assets to other tools

```bash
bash $S/ipc.sh start      # localhost API + token in $CINEMA_ROOT/data (prints the env for devuniverse)
bash $S/ipc.sh status
bash $S/ipc.sh stop
```
Endpoints: `GET /health`, `GET /schema`, `POST /generate` (asset bytes),
`POST /assets/image|audio` (JSON result). Bearer token required; never
print it into chat. `ipc.sh start` refuses if something already answers on
the port. The MCP tools `ipc_start`/`ipc_stop` only live for one `call.sh`
call — use `ipc.sh`.

## 8. Checks and what "good" means

`check_media.sh` flags: invalid/unrenderable SVG, unreadable images, audio
quieter than −30 LUFS, peaks above −0.5 dBTP, >60 % silence, video without
audio, >20 % black frames. Then look:
- logos: name spelled right, not clipped, readable at 64 px (icon), works on
  dark (reversed);
- art/mockups: colours match the brief, nothing overlapping or cut;
- video contact sheet: right ratio, captions inside the frame, titles
  readable, no blank shots, story order right.
Anything off → change the inputs (style words, colours, prompt shape) and
regenerate — it is free offline.

## 9. Troubleshooting

| Symptom | Fix |
|---|---|
| `isn't installed yet` | `bootstrap.sh` |
| no PNG next to an SVG | install librsvg (`brew install librsvg`) |
| voiceover is a beep "NOT SPEECH" | no TTS engine: macOS has `say`; else `brew install espeak-ng` |
| render fails | `bootstrap.sh --check`; ffmpeg missing → `install_dependencies` (consent) or `brew install ffmpeg` |
| wrong colours | put hex codes in `style` |
| odd scene headings | rephrase the prompt as `a <subject> <verb-ing> in <place> at <time>` |
| 401 from IPC | the caller's `CINEMA_ROOT` differs from `ipc.sh`'s |
