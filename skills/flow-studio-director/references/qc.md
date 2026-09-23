# QC — checking every output

Nothing generated is accepted without QC. Not the first take, not the
fifth, not in autopilot. QC has two halves and both are required.

## 1. Measure (script)

```bash
python3 scripts/qc_clip.py take.mp4 --duration 8 --ratio 9:16 \
    --expect-speech --dialogue '[{"start":2.6,"end":4.8},{"start":5.0,"end":7.0}]'
```
Checks length, aspect ratio, audio track, near-silence, clipping, black
frames, frozen picture, whether sound exists under each scripted line,
sound outside the script, and whether the clip ends on stillness. Writes
`contact_sheet.png` (5 frames), `first.png`, `last.png`, `report.json`.

A FAIL here is final — do not "look past" a technical failure.

## 2. Look and listen (agent)

Open `contact_sheet.png` (and first/last) with the image-reading tool.
For audio, listen if the environment can play it; otherwise rely on the
sound-coverage numbers and ask the user to listen before approving any
dialogue shot. Mark each line PASS / MINOR / FAIL with the time:

| # | Check | Looking for |
|---|---|---|
| 1 | Identity | same face, age, build as the character sheet and earlier shots; no drift inside the clip |
| 2 | Wardrobe & props | lock string honoured in every frame |
| 3 | Anatomy | hands and fingers, limb count, people count, no melting in motion |
| 4 | Physics | weight, contact, occlusion, shadows on real surfaces, cloth and hair |
| 5 | Continuity | vs the previous approved shot: light direction and colour, position, eyeline, 180° line, props in hand |
| 6 | Camera | the move, framing and lens asked for |
| 7 | Dialogue | the scripted words (not paraphrased), right voice, right dialect, lips moving with speech, no extra voices |
| 8 | Text | no stray text/subtitles/garbled letters unless requested |
| 9 | Technical | flicker, warping, banding, artifacts |
| 10 | Intent | does the shot deliver its beat — would the director keep it? |

## 3. Verdict (one of four)

- **ACCEPT** — say so plainly; don't invent problems.
- **FIX IN POST** — trim, crop, speed-ramp, grade, cover a glitch with a
  cut. Default whenever it works: zero credits. Give the exact edit.
- **REGENERATE** — FAIL on identity, anatomy, dialogue or the core
  action. Always attach the **corrected prompt** and say exactly what
  changed and why. "Try again" alone is never a verdict.
- **CHANGE ROUTE** — the same failure twice means the route is wrong,
  not the wording: different model, different method (frames ↔
  ingredients), or split the shot. `project_state.py` stops automatic
  retakes at 2 failures in a row in per_shot and at 3 in autopilot.

**Logging the verdict** (the combined verdict of both halves — a clip that
passes `qc_clip.py` but fails the visual checklist is a FAIL):
ACCEPT → `PASS` · FIX IN POST → `CHECK` · REGENERATE / CHANGE ROUTE →
`FAIL` · generation errored, was blocked or timed out → `ERROR` (with the
credits actually charged). An x2–x4 generation is one take: log the
total credits, the chosen output as `--file`, the others in `--note`.

Close every QC pass with: extendable? (Veo 8s and ends on stillness),
cuts cleanly against the previous approved shot?, and credits spent vs
budget. Then log it (the take was opened with `start-take` right after
Generate): `project_state.py log-take <shot> --file ... --verdict PASS|CHECK|FAIL|ERROR`.

## Troubleshooting — symptom → cause → cheapest fix

| Symptom | Cause | Fix |
|---|---|---|
| Face drifts / identity changes | weak identity anchor | Character asset as ingredient, or lock identity in keyframes (hybrid) |
| Warp / teleport mid-clip | first and last frames too far apart | bring the end frame closer, or split the shot |
| Lighting jumps inside a clip | keyframes lit differently | regenerate the end frame with the start frame's LIGHT line verbatim |
| Wardrobe changes | lock paraphrased | paste the lock verbatim; add "wardrobe identical to reference" |
| Extra person / duplicate | vague cast | "CAST: X only — 1 person in frame" |
| Action starts mid-way | state-zero broken | rewrite [0-2s] as the moment before the action |
| Object pops in | spawning | enter from off-screen or reveal with the camera |
| Wrong words / paraphrased line | line too long for the window, or quotes missing | shorten to pace, quote it exactly, timestamp it |
| Second voice / voices swapped | too many speakers, no voice lock | 1–2 speakers, voice asset per character, "STRICTLY ONE VOICE", name the silent one |
| MSA instead of dialect | dialect not stated / MSA spelling | name the dialect, write dialect spelling, voice asset with dialect in its performance |
| Subtitles burned in | model added captions | "no subtitles, no on-screen text" in NEGATIVE |
| Music in the clip | not excluded | "MUSIC: none" |
| Stiff, robotic motion | over-constrained first+last | switch to ingredients, let motion run free |
| Garbled text in frame | text made by the video model | make it in the keyframe with Nano Banana Pro, exact string in quotes |
| Extension seam | base clip ended moving | regenerate the base to end on a hold, then extend |

Always try the cheapest retry first: fix the prompt, test at 360p or 4 s,
then pay for the full take.

## Whole-film QC

Clip QC is not film QC. Before delivery, run the final checklist in
`client-workflow.md` on the assembled master: every line present and
right, captions word-for-word, continuity across cuts, transitions as
approved, brand, loudness, deliverables, rights.
