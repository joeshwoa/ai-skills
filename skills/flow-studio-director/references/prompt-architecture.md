# Prompt architecture

Every prompt this skill writes is dense, specific and complete: a model
fills every gap you leave with an average guess, and average guesses are
what make AI video look like AI video. Aim for 150–350 words per video
prompt. Longer is not better past that — it dilutes; add precision, not
adjectives.

## Rules that apply to every prompt

1. **English for the prompt; the real language for anything spoken or
   written on screen.** Dialogue stays in its dialect, inside quotes.
2. **Labelled blocks**, always in the same order, so nothing is forgotten
   and a failed take can be fixed by editing one block.
3. **Lock strings are pasted verbatim** — character, wardrobe, location.
   Never paraphrase them between shots; paraphrase is how wardrobe drifts.
   A deliberate change gets a new version tag (`[HANA_LOCK v2]`).
4. **State-zero.** The clip starts *before* the action and ends *after*
   it settles. A door being opened starts with the door closed and a hand
   approaching. Nothing spawns or vanishes: it enters from off-screen or
   is revealed by camera movement.
5. **One action per shot.** Three actions in 8 s = three half-done actions.
6. **Physics, not adjectives.** "Key light from camera-left at 45°,
   3200 K, soft, falling off to deep shadow on the right cheek" beats
   "dramatic lighting".
7. **Say what you want instead of what you don't.** "An empty desert
   with no roads or buildings" works better than "no buildings". Keep a
   short NEGATIVE line anyway for the recurring failures (extra fingers,
   text on screen, extra voices).
8. **No subtitles, no captions, no on-screen text** unless text is the
   point — then use the image model (Nano Banana Pro) and put the exact
   string in quotes.
9. **Timestamps for anything with more than one beat** (`[0-2s]`,
   `[2-5s]`, `[5-8s]`) — models follow a timeline far better than a
   paragraph.
10. **If it will be extended, it ends on a hold**: "the final second is a
    still hold, no motion".

## Arabic (and any dialect) on screen

- Write dialogue exactly as it is spoken: Egyptian `إزيك، عايز، دلوقتي، بص`,
  not MSA. Never "correct" a character's dialect.
- Minimal tashkeel — only where two readings are spelled the same and the
  wrong one would be mispronounced (`مُصِرّ` vs `مِصْر`).
- State the dialect in words: "speaks in Egyptian Arabic (Cairene)".
- Pace: ~2.0–2.6 words/s. `shot_plan.py` enforces it.
- One or two speakers per clip. With two, give each line its speaker and
  timestamp, and say who is silent while the other talks.

---

## A. Character reference sheet (image, once per character)

```
Character reference sheet for [NAME], [style e.g. 3D Pixar-style CGI / photoreal].
Three views on one canvas, left to right: front, three-quarter, profile. Full body,
neutral standing pose, arms slightly away from the body. Plain light-grey seamless
background, soft even studio light from the front, no shadows on the backdrop.
IDENTITY: [age], [build], [height relative to others], [skin tone], [face shape,
eyes, nose, mouth], [hair: colour, length, texture, style], [marks].
WARDROBE [NAME_LOCK v1]: [every garment: colour name, fabric, fit, condition],
[accessories], [shoes].
Same person in all three views, identical clothing and proportions. No text, no labels.
```

Register the approved sheet as a Character in Flow.

## B. Keyframe image (start or end frame)

```
[STYLE line — identical in every keyframe of the project]
SHOT: [shot size], [lens mm], [camera height and tilt], [aperture / depth of field].
COMPOSITION: [subject position on the grid], [headroom], [eyeline / looking room],
[foreground / midground / background contents with screen sides].
CHARACTER: [NAME] — [pose, hands, gaze, expression at THIS instant].
[NAME_LOCK v1 — verbatim]
SET: [LOCATION_LOCK — verbatim], [props in frame and where].
LIGHT: key [source, side, angle, hardness, K]; fill [ratio]; rim [yes/no, colour];
practicals [list]; atmosphere [haze/dust/none].
FRAME STATE: this is the [first/last] frame — [exact state of the action].
No text, no watermark, no extra people.
```

Start and end frames of the same shot share the STYLE, SET and LIGHT
lines word for word; only pose/expression/camera position change.

## C. Video prompt (the main one)

```
STYLE: [identical project-wide style line + film look, e.g. "shot on 35mm, fine grain"]
CAST: [exact names present] — [count] people total. [Anyone NOT present if likely to be added.]
OPTICAL: [shot size], [lens], [aperture/DOF], [camera height/tilt], [camera move + speed],
[stabilisation: locked-off / dolly-smooth / subtle handheld].
GEOMETRY: [who is where: screen-left/right, fg/mg/bg, distances], [eyelines],
[180° line side], [entrances/exits and from where].
LIGHT: [key/fill/rim with direction + K], [practicals], [shadow direction], [atmosphere].
LOCKS: [NAME_LOCK vN verbatim] [LOCATION_LOCK verbatim] [PROP_LOCK verbatim]
MOTION:
[0-2s] state-zero — [the frame before the action starts]
[2-5s] [the one action, with weight, cause and follow-through]
[5-8s] [settle / reaction / end state]{; final second is a still hold if extending}
PERFORMANCE: [emotion, energy, micro-expressions, where eyes go]
AUDIO:
  DIALOGUE: [STRICTLY N VOICE(S)]. [NAME] speaks in [dialect], [delivery]:
    "[exact line]" ([start]-[end]s). [NAME2 stays silent / reacts].
    Natural lip-sync matching the words.
  SFX: [specific foley with surfaces and materials]
  AMBIENCE: [room tone / exterior bed]
  MUSIC: none (added in post)
NEGATIVE: [text on screen, subtitles, extra fingers, extra people, voice changes,
music, wardrobe changes — plus anything this shot is prone to]
```

For **ingredients** shots, open with what each reference is:
"Using the provided references — [HANA] (character), [HANA_VOICE]
(voice), [STONE_ROOM] (location) — …".

For **first+last frames** shots, describe the *transition*: "The camera
performs a slow 20% push-in from the start frame to the end frame while
Hana turns her head from screen-left to camera…". Do not re-describe
things the frames already fix; spend the words on motion and sound.

## D. Video-to-video edit (Omni)

Mostly a preservation list — the model changes whatever you do not pin:

```
CHANGE ONLY: [the single change, precisely].
KEEP IDENTICAL: faces and identity, wardrobe [LOCK verbatim], body positions and motion
paths, timing, camera framing and movement, lens and depth of field, background layout,
lighting direction and colour temperature, grade, all audio.
DO NOT: alter faces, change the number of people, add objects, add text, change the ratio,
re-time or re-stage anything.
```
Bundle all changes into one pass when possible; test on 4 s first; more
than three edit passes on one clip → regenerate instead.

## E. Extension (Veo Lite `+`)

Continue the exact motion, framing, light and audio; state what happens
in the new seconds; end on stillness again if another extension follows.
Never introduce a new location, new character or a camera re-frame in an
extension — that is a new shot.

## F. Custom voice (Flow Voices)

```
Base voice: [e.g. Achird — male, friendly, mid pitch]
Performance: [age], [dialect: "speaking Egyptian Arabic (Cairene)"], [energy],
[texture: warm / gravelly / breathy], [pace], [emotional default], [anything to avoid].
Sample line (≤120 chars, in dialect): "[a line this character would really say]"
```

---

## Worked example — the account's existing prompt, upgraded

Before (worked, but loose on light, timing and audio control):
> MOTION: [0-6s] Hana looks off-screen at the glowing green light with
> wide, surprised eyes. She points at it and speaks with natural lip-sync.

After:
```
STYLE: 3D animated feature film, Pixar-style CGI, soft subsurface skin, high detail.
CAST: Hana only — 1 person in frame. Omar is off-screen and silent.
OPTICAL: Medium close-up, 50mm, f/2.8 shallow depth of field, camera at Hana's eye level,
very slow push-in (about 10% over the clip), locked-off otherwise.
GEOMETRY: Hana centre-left, facing three-quarters to screen-right; the glowing panel is
off-screen right at her eye level; dark stone wall behind her, soft out of focus.
LIGHT: Key is the off-screen panel, screen-right, hard green (#39FF88), raking across her
face; faint warm fill from screen-left at 1/8 intensity; no rim; fine dust in the green beam.
LOCKS: [HANA_LOCK v1]: female, big brown eyes, wavy brown hair, floral headband,
white t-shirt with pink and yellow flowers, loose yellow trousers.
MOTION:
[0-1s] Hana looks down, neutral, still — the light has not caught her attention yet.
[1-2.5s] The green glow flickers on her cheek; she lifts her head and her eyes widen.
[2.5-7s] She raises her right hand and points screen-right, speaking.
[7-8s] She holds the point, mouth closed, eyes still on the panel — still hold.
PERFORMANCE: curious, excited, a little awed; eyebrows up on the question.
AUDIO:
  DIALOGUE: STRICTLY ONE GIRL'S VOICE. Hana speaks in Egyptian Arabic, excited, clear:
    "بص يا عمر، ظاهر إيه ع الشاشة؟" (2.6-4.8s) "ليه درجة حرارة الأرض بتعلى؟" (5.0-7.0s)
    Natural lip-sync matching the words.
  SFX: a low digital hum from screen-right; a soft fabric rustle as she raises her arm.
  AMBIENCE: quiet stone-room tone with a faint echo.
  MUSIC: none.
NEGATIVE: text or subtitles on screen, a second voice, a boy's voice, music, photorealism,
extra fingers, the panel appearing in frame.
```
