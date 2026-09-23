# Changelog — flow-studio-director

## 2026-09-23 — v2 (client script to finished film)

- Five gates (script → cast → storyboard → rough_cut → final) enforced by
  `project_state.py` on keyframes, generation, takes and approvals; `--by`
  required, approvals carry the user's words; reopening cascades;
  `sync-plan` / `cast-remove` keep state in step with the plan.
- Characters before scenes: a character is built only through `cast-set`
  with real files (sheet, expressions, consistency test, Flow Character,
  voice); silent on-screen characters are found and cast.
- `script_breakdown.py`: docx/pdf/txt/fountain; scene headings with colons
  and on two lines; timecodes, notes and clock times never become
  characters; Arabic name-on-its-own-line cues; named V.O. keeps its
  speaker; similar names are asked, never merged (`--alias` after the
  answer).
- `animatic.py` storyboard, `edit_clip.py` mechanical fixes, transitions
  (post, in-camera, J/L sound cuts without double audio), `captions.py`
  timed from measured speech in the real clips, `selftest.py`
  (38 checks, incl. regressions for every bug found in two reviews).


## 2026-09-23 — v1

Built from the user's "Flow Studio Director" Gemini Gem instructions, used
as a statement of intent rather than copied, and rebuilt against the live
Google Flow UI on his Google AI Pro account.

- Platform facts verified in the live UI without generating: models on Pro
  (Omni 1.1 Flash, Veo 3.1 Lite/Fast/Quality, Nano Banana 2/Pro/2 Lite), real
  credit costs (Omni 7/10/12/15 for 4/6/8/10 s at 720p, 7 at 360p 10 s; Lite
  10; Fast 20; Quality 100; images 0), Flow Characters and Voices assets,
  selector map for automation.
- Removed VoxSync: on-screen dialogue is native to the video model using
  saved Flow voices; external TTS (Gemini TTS / ElevenLabs) only for an
  off-screen narrator.
- Added four autonomy modes enforced by `project_state.py`.
- Added mandatory QC of every take (`qc_clip.py`) with contact sheets.
- Added plan validation and pricing (`shot_plan.py`), assembly with loudness
  normalisation (`assemble.py`), narration generation (`voiceover.py`).
- Split craft from platform data so other platforms are a new folder.

Not yet exercised live: a real generation, waiting and download in Flow
(procedures P5–P9 in automation-kapture.md are marked "verify on first
run"), and live TTS calls (no API key in the build environment).
