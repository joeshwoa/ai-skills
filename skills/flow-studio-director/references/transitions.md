# Transitions — designing every cut

Every shot in the plan has a `transition_in`. Most should be a **cut** —
a well-planned cut is invisible and keeps pace. A transition is a
storytelling choice, not decoration; each one must have a reason you can
state in one line.

## Three kinds — and why the difference matters

**Post transitions** — made in the edit by `assemble.py`, any time, free:
`dissolve`, `fade_black`, `fade_white`, `wipe_left/right/up/down`,
`slide_*`, `zoom_in`, `circle_open/close`, `pixelize`, `radial`, `whip`
(blur). They overlap the two clips, so they **eat time** (a 0.5 s dissolve
shortens the film by 0.5 s) and anything spoken under them is half-lost.

**In-camera transitions** — must be designed into the generation; they
cannot be added afterwards:
- `match_cut` — shape, motion or composition in the last frame of shot A
  repeats in the first frame of shot B (a round coffee cup → the round sun).
  Build it with keyframes: take A's approved `last.png`, compose B's start
  keyframe to match its geometry. Needs `keyframes.start`.
- `morph` — A transforms into B. Generate a bridging shot on frames mode
  with start frame = A's last frame and end frame = B's first frame
  (keyframe chain). Keep the two frames similar in layout and light or it
  warps.
- `whip_pan` — A ends with a fast whip in one direction, B starts with a
  whip in the same direction; the cut hides in the blur. Both prompts must
  say so ("final 0.4 s: the camera whips violently to screen-right, heavy
  motion blur" / "opens mid-whip from screen-left, settling on…").
  `assemble.py` adds a 0.25 s blur assist over the join.

**Sound transitions** — picture cuts hard, sound crosses the cut:
- `j_cut` — B's sound starts before B's picture (`audio_offset` 0.3–1 s)
  and A's sound stops at that moment. Pulls the viewer into the next
  scene; natural for dialogue scene changes ("we hear the market before we
  see it"). Needs B to have usable audio before its in-point — set B's
  `in` at least `audio_offset` later than its first frame.
- `l_cut` — A's sound continues over B's picture and B's own sound starts
  only when A's ends. A reaction shot while the line finishes; a line that
  lands over the next image. Needs A to have audio after its `out`.

`assemble.py` never plays both clips' sound at once on a J/L cut, and warns
when there isn't enough spare sound (the cut then has little or no effect —
fix the in/out points, don't ignore it).

## Choosing

| Situation | Use |
|---|---|
| Same scene, continuous time, new angle | cut (on action, mid-movement) |
| Same scene, reaction to a line | cut, or l_cut to keep the line running |
| New scene, same time flow, social pace | cut; j_cut if sound can lead |
| Time passes / dreamy / memory | dissolve 0.5–1 s |
| Start or end of the piece, chapter break | fade_black (0.5–1 s) |
| Flash, revelation, heavenly/clean brand look | fade_white |
| Energy, montage, sport, product reveal | whip_pan (in-camera) or a hard cut on the beat |
| Visual rhyme between two ideas | match_cut |
| Transformation is the point | morph |
| Playful / explainer / kids' content | wipe, slide, circle_open — sparingly, one family per piece |
| Serious drama | cuts and dissolves only; stylised wipes cheapen it |

Rules:
- **One transition vocabulary per piece.** Mixing wipes, zooms and
  circles looks like a template.
- **Never dissolve over dialogue** — `shot_plan.py` warns when a line
  starts or ends under a transition.
- Post transitions ≤ half the shorter of the two clips (enforced).
- The first shot opens with `cut`, `fade_black` or `fade_white` only.
- In-camera transitions go on the shot card's routing line and in BOTH
  prompts — the outgoing and the incoming shot.
- Match the transition to the audio: a whip needs a whoosh, a hard cut on
  the music beat needs the beat marked in the edit.

## In plan.json

```json
"transition_in": {"type": "dissolve", "duration": 0.6}
"transition_in": {"type": "j_cut", "audio_offset": 0.5}
"transition_in": {"type": "whip_pan"}
"transition_in": {"type": "match_cut"}
```
The same objects go into `edit.json` clips for `assemble.py`; the
animatic (`animatic.py`) previews them, so the client sees the transitions
before anything is generated.
