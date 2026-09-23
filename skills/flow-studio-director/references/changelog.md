# Changelog — flow-studio-director

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
