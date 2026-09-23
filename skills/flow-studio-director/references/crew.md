# The crew

This skill works as a full production team. Each role below is a
checklist the agent runs, not a costume. On a small job the roles
collapse into one pass; on a long film each can be a separate sub-agent
(if the environment supports spawning them) whose output feeds the next.

The rule that makes a team better than one generalist: **every role signs
off on every shot.** A prompt is not finished until each role below has
contributed its line or said "nothing needed here".

---

## Pre-production

**Producer** — owns the budget and the plan.
- Converts the brief into shot count x length x model and prices it with
  `scripts/shot_plan.py` before anything is generated.
- Always puts the cheapest viable path beside the best-quality one.
- Sets the autonomy mode with the user and holds the spending brake
  (`scripts/project_state.py can-generate` before every generation).

**Content strategist** — owns *why anyone watches*.
- Platform, audience, goal, hook in the first 1.5 s, where the CTA lands.
- For MENA / Egyptian audiences: dialect, humour, references, seasonal
  context (Ramadan, exams, Eid, summer) that make it feel local.
- Researches what is working in the niche before inventing (see
  `ideation.md`).

**Screenwriter** — owns the words and the beats.
- One clear action per shot; a beat sheet before dialogue.
- Dialogue written to fit its window (2–2.6 words/s for Arabic, 2.3–3
  for English); shorter lines, more cuts, never a monologue in 8 s.
- Writes in the spoken dialect as it is actually spoken — never MSA
  "corrected" into a character who would not say it.

**Director** — owns the intent of every shot.
- What the audience should feel and know at the end of this shot, and
  why this shot exists at all. Cuts shots that do not earn their credits.
- Decides the continuity method per shot (see `routing-principles.md`).

**Casting & character designer** — owns identity.
- Builds each character's bible: age, build, relative height, skin tone,
  face structure, hair, marks, and an IMMUTABLE wardrobe line with colour
  names, fabric, fit, accessories, shoes.
- Produces reference sheets (front / three-quarter / profile, neutral
  light) as images first, then registers them in the platform (Flow:
  Characters) so every shot reuses the same identity.

**Voice director** — owns how each character sounds.
- Picks a base voice per character and writes its performance direction
  (dialect, age, energy, texture, pace). In Flow this becomes a saved
  voice asset (see `audio.md`).
- One voice per character for the whole project; changes only with a new
  lock version.

**Production designer** — owns the world.
- Locations described as fixed geometry: what is screen-left, screen-right,
  foreground, background; materials; era; clutter level.
- Props list with exact appearance; any prop that recurs gets a reference
  image.

**Costume** — enforces the wardrobe lock in every prompt, verbatim.

---

## Camera, light, motion

**Director of photography** — owns the frame.
- Shot size (ECU / CU / MCU / MS / MWS / WS / EWS), lens (focal length
  and what it does: 24 mm exaggerates space, 50 mm is neutral, 85 mm
  compresses and flatters faces), aperture / depth of field, camera
  height and tilt, composition (thirds, headroom, lead room, eyeline).
- One camera move per shot, named precisely (static, slow push-in,
  pull-out, dolly left, truck, pan, tilt, crane up, orbit/arc N degrees,
  handheld drift, whip pan) with its speed.
- Obeys the 180° line across shots unless a cross is deliberate.

**Gaffer (lighting)** — owns light as physics, not mood words.
- Key: source, direction (clock position or screen side), hardness,
  colour temperature in K. Fill ratio. Rim/back light. Practicals in
  frame. Shadow direction and softness. Atmosphere (haze, dust, rain).
- Keeps key direction and temperature consistent across every shot in a
  scene — the #1 cause of cuts that feel wrong.

**Movement / physics coordinator** — owns weight and cause.
- Every motion has a cause and a consequence: weight shift before a step,
  cloth drag, hair follow-through, liquid slosh, contact shadows.
- State-zero: the clip starts before the action begins and ends after
  it settles (see `prompt-architecture.md`).

**VFX supervisor** — owns anything injected, transformed or edited.
- Contact, occlusion and cast shadows for inserted objects; light match;
  what must stay untouched in a video-to-video edit.

---

## Sound

**Dialogue supervisor** — native, in-clip dialogue only (never dubbed
over characters). Speaker count per clip (1–2), exact lines in quotes,
delivery direction, lip-sync instruction, and what must NOT be heard
("one voice only", "no background chatter").

**Sound designer** — foley and ambience written into the video prompt:
footsteps on which surface, fabric, props, room tone, weather, city.

**Composer / music supervisor** — music is added in post, not generated
into dialogue shots (music baked into a clip cannot be edited, ducked or
changed later). Brief: genre, BPM, energy curve, where it hits.

**Narrator (voice-over)** — only for a voice the audience never sees.
Generated outside the video model (`scripts/voiceover.py`, see
`audio.md`).

---

## Post

**Editor** — cuts on action, 2–4 s rhythm for social, holds for emotion.
Assembles with `scripts/assemble.py`. Decides trims that save a
regeneration.

**Colourist** — matches clips from different models to one look before
anything else in post.

**Script supervisor (continuity)** — before every shot, checks against
the previous approved shot: wardrobe, props, hand holding what, position,
light direction, time of day, eyeline.

**QC supervisor** — checks every generated output, no exceptions:
`scripts/qc_clip.py` for the measurable half, then the visual checklist
in `qc.md` by actually looking at the frames. Gives a verdict, never a
compliment. A shot is not "done" until QC says PASS and the user (or the
autopilot rules) accepts it.

---

## How the roles show up in a shot card

Each shot card ends with a sign-off block so it is visible that nothing
was skipped:

```
SIGN-OFF  director ✓ intent | DP ✓ 85mm MCU push-in | gaffer ✓ key camera-left 3200K
          physics ✓ state-zero, ends on hold | costume ✓ [HANA_LOCK v1] | sound ✓ 1 voice + foley
          continuity ✓ vs S03 | producer ✓ 12 cr (Omni 8s) | QC plan ✓ speech 1.0–3.6s
```
