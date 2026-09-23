# From the client's script to the finished video — right the first time

"Right the first time" doesn't come from generating harder. It comes from
making every expensive step depend on a cheap, signed decision, and
checking every output before the next step builds on it. Five gates,
each a thing the client can say yes to in minutes:

| Gate | What the client approves | What it costs us to get there | Enforced by |
|---|---|---|---|
| 1 `script` | our reading of the script + answers to our questions | nothing | no characters/images before it |
| 2 `cast` | every character's look and voice | ~0 (images free; optional 7-credit voice test per lead) | no keyframes, no shots before it |
| 3 `storyboard` | the whole film as an animatic: every frame, order, timing, lines, transitions | 0 (keyframes free) | no video before it (user may waive for quick jobs) |
| 4 `rough_cut` | the assembled film at preview quality | the shots | only after every shot passes QC and is approved |
| 5 `final` | the finished master + deliverables | minutes | final QC must pass |

Everything paid for (video generations) happens between gates 3 and 4,
after the client has already seen and approved what each shot must look
like. Surprises at the end become rare because the end was previewed at
the start.

## Step by step

**0. Receive.** Script (any format), brief, brand assets, references,
deadline, deliverables (platforms, ratios, lengths), budget. Ask the
Round 1 intake questions (`intake.md`) that the brief doesn't answer.

**1. Analyse** (`script-analysis.md`): `script_breakdown.py`, then the
editorial pass. Send the interpretation + questions. → gate `script`.

**2. Cast** (`cast.md`): bible → sheets → expression sheets → consistency
test → Flow Characters + Voices → client approves each. → gate `cast`.

**3. Plan**: turn `plan_skeleton.json` into the real plan — route every
shot (`routing-principles.md`), set transitions (`transitions.md`), write
every prompt (`prompt-architecture.md`), price it (`shot_plan.py`, zero
errors), set autonomy mode and budget (`project_state.py init`).

**4. Storyboard**: generate every shot's keyframe(s) (free), build the
animatic, send it:
```bash
python3 scripts/animatic.py --plan plan.json --keyframes keyframes/ --out review/animatic.mp4
python3 scripts/animatic.py --plan plan.json --keyframes keyframes/ --out review/animatic_client.mp4 --no-labels
```
Client comments here are free to act on — redraw a keyframe, reorder,
cut a line. → gate `storyboard`.

**5. Produce**: shot by shot in the chosen autonomy mode; every take QC'd
(`qc.md`); fix in post before regenerating (`editing.md`); approved takes
logged in state.

**6. Rough cut**: `assemble.py edit.json --preview`, captions from the
script, watch it through, then send. Notes are sorted before acting
(see Revisions). → gate `rough_cut`.

**7. Final**: full-quality assemble with captions/logo, final QC (below),
deliverables, delivery note. → gate `final`.

## Final QC — the whole film, not just the clips

Run `qc_clip.py` on the master (length, ratio, audio, black/frozen frames),
then watch it **twice**: once for story and feel, once with this list.

- Hook works in the first 1.5 s, muted and unmuted
- Every scripted line present, in order, right character, right voice,
  right dialect, intelligible; no stray voices
- Captions match the audio word for word, are timed, inside safe zones,
  nothing on the platform UI areas
- Identity and wardrobe identical across every shot
- Continuity across cuts: props in hand, positions, light direction, time
  of day, screen direction
- Transitions as approved in the storyboard; no dialogue lost under them
- No generation artifacts: hands, faces in motion, warped lines, garbled
  text, flicker, extra people
- Brand: logo, colours, product exactly as in the brief; on-screen text
  spelled correctly
- Sound: loudness at target (−14 LUFS social), no clipping, music ducked
  under speech, no abrupt cuts in ambience
- Length within the brief; the end card/CTA holds long enough to read
- Deliverables: every ratio/length asked for, file names, captions files
- Rights: music licence, no real people/brands without clearance,
  watermark and AI-disclosure terms for the client's use

## Revisions — sort every note before touching anything

| Note type | Example | Action | Cost |
|---|---|---|---|
| Edit | "tighten the start", "swap shots 4 and 5", "bigger logo" | edit / re-assemble | 0 |
| Post fix | "warmer colour", "remove the flicker at 0:12" | `edit_clip.py` | 0 |
| Partial regenerate | "she should smile here", "wrong hand" | Omni edit or new take of that shot | that shot's credits |
| Script change | "change the line", "add a scene" | back to gate 1 for that part; re-plan, re-cast if new characters | new shots |
| Taste change against an approved gate | "actually make her older" | show which approval it changes and what it costs; agree first | may be large |

Send the sorted list back with the cost of each item before doing it.
Changes that contradict an approved gate are fine — but they are the
client's decision, made knowing the cost, not something discovered on the
invoice.

## Delivery package

- master video(s): `<project>_<ratio>_<length>_v<N>.mp4`
- captions: `.srt` (and burned version if requested)
- a thumbnail/still (best frame)
- short delivery note: what's included, versions, anything to know
  (watermark terms, AI-disclosure requirements, music licence)
- keep: plan.json, state.json, all approved takes, keyframes, character
  sheets — the next episode or revision starts from these.
