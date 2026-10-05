# Recipes (copy, change the paths, run)

All calls: `bash scripts/call.sh <tool> '<json>'` or `@file.json` (put Arabic and long briefs in a
file). Always pass one `project` per job; LOOK at every preview.

## EDIT 1 — talking head → clean social clip with captions
1. `video_transcript {"path": "cam.mp4", "language": "ar"}` → read the indexed transcript.
2. `video_transcript_edit {"path": "cam.mp4", "remove": ["word 12-30", "the bit about pricing"], "remove_fillers": true, "dry_run": true}`
   → read the cut list, then run again without `dry_run`.
3. `video_reframe {"path": "<edited>.mp4", "aspect": "9:16"}` (face-tracking) if the camera was horizontal.
4. `video_captions {"path": "<reframed>.mp4", "style": "reels", "language": "ar"}`.
5. `video_qc {"path": "<captioned>.mp4", "platform": "reels"}` → `video_export {"preset": "reels"}`.

## EDIT 2 — event / product footage pile → 30 s montage on music
1. `video_select_takes {"folder": "footage/", "want": "best", "count": 12}` → shot sheet.
2. `video_beats {"path": "track.mp3"}` → tempo, beat plot.
3. `video_cut_to_beats {"clips": [<ranked clips with in/out>], "music": "track.mp3", "every": [4,2,2], "size": "9:16", "max_duration": 30}`.
4. Titles/CTA overlays from motion-design-studio into the timeline; `video_edit` to re-render.
5. `video_auto_color` / `video_color_match` on mismatched shots; `video_qc`; export.

## EDIT 3 — interview / YouTube video (long-form)
1. `video_remove_silence` or `video_transcript_edit` (story order via `keep` list).
2. B-roll per topic: own footage (`video_scene_detect` on b-roll reels) + `stock_search` (stock-library).
3. Timeline: A-roll clips with `l_cut`/`j_cut`, b-roll overlays, lower thirds at each new speaker,
   chapter titles, music bed `duck: true`, `captions: {"style": "clean"}`, `loudness: "youtube"`.
4. `video_edit` → `video_qc platform=youtube` → `video_export youtube` + `video_thumbnail`.
5. Client edits in Resolve? `video_export_interchange {"timeline": "timeline.json", "format": "all"}`.

## MAKE 1 — reel/ad from a script (no footage)
Write the brief to a file (Arabic scripts need English `broll_queries`, one per sentence):
```json
{"brief": {"script": "…", "style": "reel", "size": "9:16", "broll": "stock",
  "broll_queries": ["coffee cup morning", "coffee beans roasting", "barista pouring latte", "coffee shop interior"],
  "topic": "coffee", "music": "generate", "music_genre": "lofi", "captions": "reels",
  "brand": "qahwa-house", "title": "بيت القهوة", "cta": {"kind": "follow", "handle": "@qahwahouse"},
  "language": "ar"},
 "project": "qahwa-reel"}
```
`video_auto_edit @brief.json` → LOOK at storyboard.png, sheet, QC table; read EDIT-REPORT.md
(shot list + licences). Improve `timeline.json` (swap weak b-roll with better `stock_search`
picks, adjust shot lengths, add motion overlays) → `video_edit` → QC → export → `stock_credits`.
Options: `voiceover: "vo.wav"` (own VO), `talking_head: "cam.mp4"` (speaker as A-roll),
`footage: "folder"` + `broll: "both"`, `music: "stock:<query>"`, `stock_people: "allow"` (only with
model releases), `render: false` to plan only.

## MAKE 2 — promo from a product photo + motion
1. Product shots: own photos or `stock_search kind=photo` (no other brands' logos).
2. motion-design-studio: `motion_compose template=social_promo` (or app_promo / stat_reveal).
3. Here: add music (`video_music`), SFX hits, captions if there's VO, QC, export per platform.

## MAKE 3 — YouTube explainer
reels-studio writes the long-form script (chapters) → `audio_voiceover` → `video_auto_edit`
with `style: "youtube"`, `size: "16:9"`, chapter titles as overlays → fine cut → chapters list in
the description (from the timeline) → `video_thumbnail` + design thumbnail.

## Fixing common problems
| Problem | Fix |
|---|---|
| Shaky phone footage | `video_stabilize` before cutting |
| Mixed white balance between cameras | `video_color_match` every shot to one reference |
| Voice too quiet vs music | timeline music `volume_db -18…-22`, `duck: true`, `duck_db 10–12` |
| Click at a cut | `audio_crossfade: 0.02` on that clip |
| Captions over on-screen text | design with `leave_bottom`, or `captions.position: "top"` for that piece |
| Horizontal footage in a vertical reel | `video_reframe` (faces) or blurred fill (default for stills) |
| Wrong/weak stock b-roll | `stock_search` with a more concrete English query (object + action + setting), pick by number |
| Stock shows a person / other brand | replace it — no model release, no third-party trademarks in ads |
| Kdenlive project letterboxes 16:9 clips | expected (the MP4 uses cover); adjust with Kdenlive's Transform effect or deliver FCPXML for Resolve |
