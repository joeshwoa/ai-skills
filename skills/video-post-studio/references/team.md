# The post team — one checklist per role

Each role signs its part before the next starts. In a single-agent run, play them in this order
and write one line per role in the delivery note ("Colorist: matched 7 shots to S03, look
film_fuji 0.6").

## Post producer
- Brief locked: platform(s) + ratio(s), length, goal, CTA, audience language/dialect, tone,
  brand kit, music feel, must-haves, deadline, deliverables (per platform MP4, SRT, project file).
- Treatment (one paragraph) + deliverables list approved by the client.
- Tracks approvals: treatment → rough cut → picture lock → final. Revisions batched per round.
- Owns honesty in the delivery note: what's approximate, licences, what couldn't be done.

## Assistant editor (ingest & logging)
- `video_probe` every source: fps, rotation, variable frame rate, codec, audio channels.
  Mixed fps → note it (the timeline conforms to the project fps).
- Long clips → `video_scene_detect` (shots + sharpness/motion/exposure/faces/audio).
  A pile of clips → `video_select_takes` (`want`: best | sharp | stable | faces | talking | audio |
  action | calm | broll). Keep the shot sheets.
- Speech → `video_transcript` (indexed words, pauses, likely fillers).
- Flags: shaky (→ `video_stabilize`), dark/colour cast (→ colorist), bad audio (→ `audio_clean`),
  vertical vs horizontal footage (→ framing plan: `video_reframe` or blurred fill).

## Story / transcript editor
- Hook: the strongest line in the first 1.5 s (reels/ads) or 10 s (long-form).
- Structure: hook → 3–5 beats → payoff/CTA. Cut everything that doesn't serve the goal.
- Removals: fillers (English um/uh/like/you know; Egyptian يعني/آه/اممم/بص/إيه ده — only standalone),
  false starts, repeats, long pauses. `video_transcript_edit` with `dry_run=true` first to see the
  cut list; then render. Never change the meaning of what someone said.
- Read the verify report: "audible remnant" → nudge that cut or keep the word.

## Editor
- Spine first (dialogue/VO or the music), then picture.
- Shot length by style; cut on action, on a beat, or on a breath — never inside a word.
- J/L cuts for dialogue scenes (sound leads/trails the picture) to hide edits.
- B-roll covers jump cuts and illustrates the words said over it (literal first, then metaphor).
- Transitions only with a reason: cut (default), dissolve (time passes), dip (chapter), whip/zoom
  (energy, reels), shape wipes from motion-design-studio for branded pieces.
- Music: cut to the beat; end on a musical ending, not mid-phrase (trim music from the end
  backwards or use a fade on a downbeat).
- Keep the timeline JSON as the source of truth; render with `video_edit` after every change.

## Colorist
1. Balance each shot (`video_auto_color`): neutral whites, exposure, black/white points.
2. Match all shots to the hero shot (`video_color_match`, strength 0.6–1.0) → .cube per shot.
3. One look for the piece (timeline `grade` / `video_grade`), subtle (0.4–0.7 strength).
- Skin tones natural; brand colours not shifted; no clipped highlights on faces.
- LOOK at before/after/reference sheets for every matched shot.

## Sound editor & mixer
- Dialogue: `audio_clean` (podcast/voice presets), no clicks at cuts (10–30 ms crossfades), room
  tone under jump cuts if needed.
- Music: ducked under speech (10–12 dB), up in the gaps; fades in/out.
- SFX: whoosh on fast transitions, pop/tick on text hits, riser before the reveal — sparingly.
- Levels: dialogue −16…−14 LUFS short-term, peaks ≤ −1 dBTP; master to the platform target.

## Music supervisor
- Mood/tempo from the brief (calm 70–90 BPM, upbeat 100–125, energetic 125–150).
- Sources: own track, `stock_search kind=music commercial=true` (licence kept, credit added), or
  `audio_music` (procedural bed, also writes MIDI). No copyrighted songs without a licence.

## Graphics (with motion-design-studio)
- Title/hook card, lower thirds for every new speaker, chapter titles (long-form), CTA end card.
- Brand colours/fonts (`brand=<slug>`); Arabic supers right-aligned; safe zones per platform.
- Text on screen ≤ 7 words at a time on reels; readable for ≥ 1.5 s.

## Captions & localisation
- Captions on by default for social (most viewing is muted).
- Exact words from the script when there is one; otherwise transcribe and proofread.
- Styles: reels (word highlight), bold, karaoke, clean, boxed. Max 2 lines; safe zone above UI.
- Other languages → premium-subtitle-localization, then burn or ship as SRT.

## Finishing / QC
- `video_qc platform=<target>`; every FAIL fixed; WARNs explained to the client.
- Watch the full contact sheet; check the first and last second (no black flash, no cut-off audio).
- Check the Kdenlive check preview when delivering the project file.

## Delivery & archive
- `video_export` per platform; thumbnail; `.srt`; `stock_credits` → credits.txt in the description.
- Editable masters: `.kdenlive`; FCPXML/OTIO/EDL via `video_export_interchange` for Resolve/Premiere/FCP.
- Everything for the job under `STUDIO_HOME/projects/<project>/` — tell the client where.
