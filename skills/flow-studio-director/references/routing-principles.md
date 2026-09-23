# Routing — deciding, per shot, how it gets made

Platform-neutral principles. The Flow-specific model facts and prices are
in `platforms/google-flow/flow-guide.md`; this file is the reasoning.

Never choose one method for the whole project. Every shot gets its own
decision, printed on its routing card with a one-line reason.

---

## 1. Does this shot need an image first?

Images are cheap or free (Nano Banana showed 0 credits on Flow Pro);
video is not. So the default is: **solve everything you can in an image,
then pay for motion once.** But an image is wasted when it constrains
something that should stay free.

Make a keyframe image when **any** of these is true:

- A recognizable character appears and must look like their reference
  (lock identity in the still, not by hoping the video model gets it).
- The composition is specific: exact framing, a product placement, a
  layout the next shot must cut against.
- The shot uses first+last frames (both frames are images by definition).
- There is legible text or a logo in frame (use the strongest image model;
  video models garble text).
- It is the first frame after a hard cut into a new scene — establish the
  look once, reuse it.
- You want to test a look cheaply before spending on motion.

Skip the image when:

- The shot is atmosphere / establishing with nothing to lock (sky, sea,
  crowd, abstract motion) — text-to-video on the cheapest tier.
- Identity is carried by ingredients/references and the framing is loose.
- The motion is organic and unpredictable (water, fire, fabric, animals,
  crowds) and a fixed end frame would fight it.
- It is an extension of the previous clip (the previous clip IS the frame).

## 2. Frames or ingredients?

**Frames control geometry. Ingredients control identity.**

| This shot's priority | Route |
|---|---|
| Must end on an exact frame the next shot starts from | first + last frames |
| A specific camera move (push to close-up, 180° arc, crane down) | first + last frames |
| Match cut / precise transition | first + last frames |
| Same character, different location or time | ingredients |
| Product must match real packaging | ingredients (product refs) |
| Natural performance, talking, reacting | ingredients (+ voice asset) |
| Organic motion — hair, water, crowd, cloth, animals | ingredients or text |
| No clear idea what the last frame should be | ingredients / first frame only — a bad end frame is worse than none |
| Edit existing footage | video-to-video edit |
| Pure establishing / mood | text-to-video, cheapest tier |

**Hybrid (default for character work with a controlled move):** generate
both keyframes in the image model *from the character references*, so
identity is locked in the stills, then hand the two stills to
first+last. Identity from references, geometry from frames, no conflict.

**Before using first+last, check the frames are bridgeable:**
- subject in a similar position in both (no jump across the room in 8 s),
- lighting direction and colour temperature identical,
- the change is ONE action, not three.
If any fails: move the end frame closer, split into two shots, or switch
to ingredients and accept free motion.

## 3. Length

- Pick the shortest length that holds the beat. On social, 2–4 s on
  screen per shot is normal; generate 4–6 s and trim.
- Dialogue decides length: words ÷ pace + ~1 s of air. Never lengthen a
  clip to fit words — shorten the line or split it across shots.
- A clip that will be extended must be generated at the extendable length
  and must end on stillness.

## 4. Model tier

- Draft / test / on screen under 2 s → cheapest tier or low resolution.
- Normal production shot → mid tier.
- Hero shot, opening frame, product beauty, anything the thumbnail uses
  → top tier — but only when it will be seen at full size. Never pay for
  top tier on a shot cropped to 9:16 and shown for two seconds.
- Talking characters with saved voices → the model that accepts voice
  assets as ingredients.

## 5. Getting from one beat to the next

| What changes between beats | Method | Why |
|---|---|---|
| Nothing — the same motion needs more time | extend | cheapest, no seam |
| Camera angle / framing, same moment | new shot, keyframe-chained | extend cannot re-frame |
| Same character, new place or time | new shot, ingredients | identity without the room |
| Everything | new shot, hard cut | carrying continuity would waste credits |
| Hero shot that must look its best | keyframe chain on a higher tier | extend forces the cheap tier |
| Dialogue longer than the clip | split the line across shots | never extend to fit words |
| The audience should feel a cut | new shot | extending kills rhythm |

Keyframe chaining uses the approved previous clip's last frame
(`qc_clip.py` writes it as `last.png`) as the next start frame.

Extension cautions: it inherits every flaw of the base clip, quality
drifts along a chain (three maximum, then rebuild from a fresh keyframe),
and it only joins cleanly when the base clip ends on stillness
(`qc_clip.py` reports `ends_on_stillness`).

## 6. Outputs per generation

x1 by default. x2–x3 only for a hero shot whose prompt is already
proven — choosing the best of three is cheaper than three rounds of
rewording. Never multiply outputs on an untested prompt.

## 7. The routing card (print one per shot)

```
▸ ROUTING — S03 (8s, 9:16)
KEYFRAMES: start + end, Nano Banana Pro (0 cr) — text on screen, must land on exact frame
METHOD: first+last frames · MODEL: Veo 3.1 Fast · 720p · x1 · 20 cr (live price checked)
WHY: push-in must end on the frame S04 extends from; Quality would be 100 cr for a 2 s on-screen moment
CONTINUITY FROM S02: keyframe chain (S02 last.png → S03 start)
ENDS ON STILLNESS: yes (S04 extends it)
FALLBACK: move end frame closer, or Omni first-frame-only with a slower push (12 cr)
```
