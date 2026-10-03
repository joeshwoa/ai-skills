# Production hand-off — from approved script to video

Render the hand-off files once the user approves the script:
```bash
bash scripts/rs.sh render <project>/spec.json --out <project>/out --formats pdf,docx,teleprompter,production,srt
```
- `*_for_production.txt` — labelled plain text (scene headings, `Name: line`, `Visual:`, `SFX:`,
  `Text:`, `VO:`) that flow-studio-director's `script_breakdown.py` reads without guessing.
- `*_teleprompter.txt` — only the talent's lines, scene by scene, `[Pause]` marks kept.
- `*_captions_ESTIMATED.srt` — planning only; real captions are timed from the recording.

Pick the route by production level (ask if unclear):

## A. Real shoot (talent on camera, phone or studio)
Give the team: the PDF (editor + talent colours), the teleprompter file, a shot list from the
Visual lines. After the shoot → **creative-studio**:
- `video_edit` (timeline JSON → MP4 + editable .kdenlive) for the cut,
- `video_captions` (Arabic default Tajawal; burned or .srt) timed from the real speech,
- `audio_clean` / `audio_master` / `audio_music` / `audio_sfx` for sound,
- `motion_*` for lower thirds, logo reveal, end frame,
- `design_create` with the cover text for the cover/thumbnail (`ig_story`, `leave_bottom` for captions).
See `skills/creative-studio/SKILL.md` (brand kit first).

## B. AI-generated video (no shoot)
→ **flow-studio-director**. Hand it `*_for_production.txt` (or the DOCX/PDF) as the client script:
```bash
python3 skills/flow-studio-director/scripts/script_breakdown.py <project>/out/<name>_for_production.txt \
    --out <project>/flow/breakdown --target-seconds <target> --ratio 9:16
```
Then follow its gates (cast → storyboard → rough cut → final). Characters speak natively in the
clip; tell it the dialect (e.g. Egyptian Arabic) and the talent's look.

## C. Faceless (voice-over + B-roll / screens / text)
→ **creative-studio**: `audio_voiceover` (Egyptian Arabic and other Edge voices, or Piper offline)
from the VO lines, screen recordings or `ai_generate_image/video` for B-roll, `video_edit`,
`video_captions`, `motion_kinetic_text` for text-only reels.

## D. Other languages / markets
For a version in another language: re-run this skill's step 5 with the target dialect
(transcreation — new hooks, local examples), not a word-for-word translation of the script.
For subtitles on an already-finished video → **premium-subtitle-localization** (it verifies the
source transcript against the audio, then adapts culturally).

## E. Something no skill covers
(e.g. scheduling posts, pulling analytics from an account) — use skill-router Part 2: search for the
user's own tool or a vetted skill, or build one, then add a line here linking it.
