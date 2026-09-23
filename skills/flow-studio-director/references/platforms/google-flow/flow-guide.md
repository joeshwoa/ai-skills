# Google Flow — platform guide

Verified 2026-09-23 on a **Google AI Pro** account by reading the live
Flow UI (nothing was generated) plus Google's "Flow models & supported
features" help page. Machine-readable version:
`capabilities.json` (what `scripts/shot_plan.py` validates against).

**Prices and options change.** Flow shows the exact cost of the current
settings under the settings panel ("ستستهلك عملية الإنشاء N من الوحدات"
/ "This generation will use N credits"). Read it before every generation
and trust it over this file. If it disagrees with this file, update
`capabilities.json` and note the date.

---

## Models on Pro, and what each is for

| Model (UI name) | Modes | Lengths | Res | Extend | Credits (720p, x1) |
|---|---|---|---|---|---|
| **Omni 1.1 Flash** | text, frames (start / start+end), ingredients, **video edit** | 4 / 6 / 8 / **10 s** | 720p, 360p | no | 4s 7 · 6s 10 · 8s 12 · 10s 15 (360p 10s = 7) |
| **Veo 3.1 - Lite** | text, frames, ingredients | 8 s (UI) | 720p | **yes** | 8s 10 |
| **Veo 3.1 - Fast** | text, frames, ingredients | 8 s (UI) | 720p | no | 8s 20 |
| **Veo 3.1 - Quality** | text, frames (no ingredients) | 8 s (UI) | 720p | no | 8s 100 |
| Nano Banana 2 (image) | text, edit, refs | — | — | — | **0** |
| Nano Banana Pro (image) | text, edit, refs, best text rendering | — | — | — | **0** |
| Nano Banana 2 Lite (image) | drafts | — | — | — | 0 (expected) |

All video models produce native audio (dialogue, SFX, ambience).
Video ratios: 16:9, 9:16. Image ratios: 16:9, 4:3, 1:1, 3:4, 9:16.
Outputs per generation: x1–x4 (cost multiplies).
Google's help page lists 4/6/8 s for Veo text/frames; the Pro UI showed
no length picker for Veo (8 s fixed). If the picker appears, use it.

**What this means in practice (Pro):**
- Omni is the workhorse: cheapest per second, the only 10 s option, the
  only video-to-video editor, ingredients at every length, and saved
  voices/characters as ingredients. Default for dialogue and character
  shots.
- Omni 360p costs half of 720p at 10 s — use it to test performance,
  timing and blocking before paying for 720p.
- Veo Lite is the only way to extend a clip.
- Veo Fast for motion/physics-heavy shots where Omni struggles, and for
  first+last camera moves.
- Veo Quality (100) only for a hero shot seen at full size. Almost never
  on 9:16 social.
- Keyframes cost nothing, so lock composition and identity in images
  first, every time it matters (see `routing-principles.md` §1).
- Pro's monthly allowance (~1,000 credits reported, confirm in the
  account menu) is roughly 80 Omni 8s clips, or 10 Quality clips. Plan
  in those units.

---

## Flow features the skill uses

**Settings panel** (the chip in the prompt bar, e.g. "فيديو · 720p · 4ث · x1"):
Video/Image · Ingredients/Frames · ratio · model · resolution · length ·
outputs · live cost.

**Frames mode**: the prompt bar shows Start (بدء) and End (إنهاء) slots
with a swap button. Start only = first-frame; both = first+last.

**Ingredients mode**: add references with `+` → asset picker.

**Asset picker (`+`)** — categories: All, Images, Videos, **Voices**,
**Characters**, Avatar images, Uploads; search; "Add to prompt"; upload.
- **Characters** (sidebar: الشخصيات): saved identities (e.g. Hana,
  Omar). Register every recurring character here once; add it as an
  ingredient in every shot it appears in.
- **Voices** (الأصوات): the 30 Gemini voices (Achernar, Charon, Kore…)
  plus **custom voices** built from a base voice + a written
  "performance customization" (e.g. "speaking Egyptian Arabic, warm,
  optimistic"). Each voice has a preview with a 120-character sample
  line. This is how on-screen characters get a consistent voice with no
  external dubbing.

**Clip editor** (open a clip): version history with the exact prompt
used, download, share, favourite, delete, timeline with `+` to extend /
add the next clip, and an edit box ("describe how to change this video")
on Omni for video-to-video edits.

**Scenes** (المشاهد): sequence approved clips inside Flow.

**Agent mode** (الوكيل chip): Flow's own built-in agent. This skill does
not rely on it; it is a separate feature the user can choose.

**Tools** (الأدوات): upscale/other utilities — check what is offered and
its cost when needed.

---

## Prompt style that already works in this account

The user's existing clips use labelled blocks — keep this shape (and
extend it per `prompt-architecture.md`):

```
STYLE: 3D animated cartoon, Pixar style, high quality CGI.
CHARACTERS: A young girl speaking excitedly.
OPTICAL: Medium close-up shot, 50mm lens. ABSOLUTELY NO TEXT ON SCREEN.
GEOMETRY: Hana is standing in a dark, ancient stone room. A strong, glowing
green light (from an off-screen digital panel) illuminates her face.
LOCKS: [HANA_LOCK]: ... floral headband, white t-shirt with pink/yellow flowers, loose yellow trousers.
MOTION: [0-6s] Hana looks off-screen ... points at it and speaks with natural lip-sync.
AUDIO: [STRICTLY ONE GIRL VOICE ONLY]. A young girl speaks excitedly in Egyptian
Arabic: "بص يا عمر ظاهر إيه ع الشاشة..." SFX: Digital hum.
NEGATIVE: photorealism, boy character, multiple voices, text on screen.
```

---

## Watermarks, rights, disclosure

Flow output carries SynthID. Check the plan page for visible-watermark
and commercial-use terms before client delivery. Do not generate real,
identifiable people without consent, brand logos the user doesn't own,
or copyrighted characters; offer an original instead.
