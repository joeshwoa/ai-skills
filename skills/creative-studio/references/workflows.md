# Team recipes

Each recipe is the order a real agency would work in, with the tools and the arguments that
matter. Always pass `brand=<slug>` (once a kit exists) and one `project=<name>` per job, and
LOOK at every preview before moving on.

## 1. New business → brand kit → launch pack

1. `brand_create` — `name`, `name_ar`, `brief` (what, where, for whom, 3 mood words),
   `sector`, `audience`, `personality`, `tagline`, `tagline_ar`, `concepts: 4`.
   Look at `concepts.png`, `palette.png`, `typography.png`. Present the 4 concepts; the user picks.
2. `brand_choose_logo {"brand": slug, "concept": "c2"}` — optional tweaks: `wordmark_font`,
   `case`, `tracking`, `mark`, `dot`. Fresh ideas: `brand_logo_concepts {"brand", "count": 4, "marks": [...], "variation": "b"}`.
3. `brand_apply {"brand": slug}` — starter set (social post, story, cover, business card,
   letterhead, email signature). `brand_guidelines {"brand": slug}` — PDF book.
4. Launch content: `design_create` per piece (see 2), a `motion_logo_reveal` sting, a reel (see 4).

Colour from the client? `base_color: "#…"`. Colour-blind/contrast check: `design_contrast`.

## 2. Social media design

- One post: `design_create {"template", "size", "brand", "project", "content": {...}}`.
  Templates (see `design_catalog`): headline, photo, split, quote, stat, list, event, offer,
  editorial, thumbnail, banner, poster, flyer, business_card, certificate, menu, infographic,
  letterhead, avatar. Each lists its fields; `field*` = required (a warning names any missing one).
- Content markup: `*word*` highlight colour, `==word==` marker, `\n` line break. Arabic text flips
  the layout to RTL automatically; set `"lang": "ar"` to be explicit.
- Sizes: `ig_square`, `ig_portrait`, `ig_story`, `youtube_thumbnail`, `linkedin_cover`, `a4`, …
  or `"1200x628"`; several comma-separated = one design exported at each size.
- Carousel: `design_carousel {"slides": [{template, …}, …], "size": "ig_portrait"}` (page counter,
  swipe hint, consistent chrome).
- Same design at other sizes later: `design_resize {"master": "<…>.design", "sizes": "ig_story,x_post"}`.
- A product photo with no background: `photo_remove_background` first, then `content.image`.
- Hand edits: the `.design` folder is plain HTML/CSS — edit `index.html`, re-export with
  `design_render_html`.

## 3. Photo work (Photoshop jobs)

- Portrait retouch: `photo_retouch` (skin smoothing, eyes, blemish heal) → `photo_look` or
  `photo_apply_lut` → `photo_compare` for a before/after sheet.
- Product shot: `photo_remove_background` → `photo_replace_background` (`background` = colour,
  gradient or image; `shadow`, `match_light`) → `photo_canvas` (ratio, padding, colour) →
  `photo_mockup` (phone/laptop/poster frames).
- Low-res image: `photo_upscale` (Real-ESRGAN) or `ai_upscale` (ComfyUI when installed).
- Layered master for a designer: `photo_compose_layers {"spec": {...layers...}, "psd": true, "xcf": true}`
  (see `call.sh help photo_compose_layers` for the layer spec) → `open_in_app` opens it in GIMP.
- Batch (a folder of photos): `photo_batch {"folder", "tool_name": "photo_look", "args": {...}}`.

## 4. Short-form video (reel / TikTok / Shorts)

1. Voiceover: write the script (Egyptian dialect for social), `audio_voiceover {"text", "voice":
   "auto" (ar-EG), "project"}` → WAV + `.srt` aligned to the voice.
2. Visuals: stills from `design_create` at **`ig_story` with `"leave_bottom": 0.26`** (room for
   captions), B-roll clips, `motion_title_card`, `motion_logo_reveal {"brand", "size": "1080x1920"}`
   (portrait uses the stacked logo).
3. Edit: `video_edit {"timeline": {...}, "brand", "project", "name"}`:
   ```json
   {"size": "9:16", "fps": 30,
    "clips": [{"image": "post.png", "duration": 8, "ken_burns": "in"},
              {"src": "broll.mp4", "in": 2, "out": 6, "transition": {"type": "dissolve", "duration": 0.5}},
              {"src": "logo_reveal.mp4", "transition": "dip"}],
    "overlays": [{"type": "lower_third", "at": 1, "duration": 4, "title": "…"}],
    "audio": [{"src": "vo.wav", "at": 0.4}, {"src": "music.wav", "duck": true, "volume_db": -8, "loop": true}],
    "captions": {"auto": true, "style": "reels", "position": "bottom"},
    "fade_out": 0.5, "loudness": "social"}
   ```
   `video_timeline_example` prints a full commented example.
4. Look at the contact sheet AND the `-kdenlive-check.png`. Read warnings (audio cut, transition
   shortened, clip aspect).
5. Deliver MP4 + `.kdenlive` + `.srt`. Other platforms: `video_export` (presets) or
   `video_reframe` (face-following 16:9 → 9:16).

## 5. Long video / YouTube / talking head

`video_remove_silence` (jump cuts) → `video_captions` (clean style, burned or `.srt` only) →
`video_grade` → `audio_clean` + `audio_master` on the dialogue → chapters/titles with
`motion_title_card` overlays → `video_thumbnail` + `design_create {"template": "thumbnail"}`.

## 6. Audio jobs

- Podcast clean-up: `audio_clean {"preset": "podcast"}` → `audio_master {"target": "podcast"}`.
- Music bed: `audio_music` (procedural, offline — also writes a MIDI you can open in a DAW) or
  `audio_library_search` (free-licence tracks; always pass the licence/credit on).
- SFX: `audio_sfx` (whoosh, pop, ding, riser…). Stems: `audio_separate_stems` (Demucs).
- Hand edits: `audio_audacity` drives an open Audacity; `open_in_app` opens a WAV in it.

## 7. Vector / print

- Logo from a sketch or bitmap: `vector_trace` → `vector_optimize` → `vector_recolor` to brand.
- Compose: `vector_compose` (shapes, text, images → SVG); `vector_text_to_outlines` before sending
  to print; `vector_boolean` (union/difference/intersection with Inkscape).
- Export: `vector_export` → PDF/EPS/PNG, favicon/app-icon sets.
- Print design: `design_create` at `a4`/`a3`/`business_card` → PDF with 3 mm bleed + crop-marks PDF.

## 8. AI images and video

1. `ai_backends` — what works now and which route each task takes (with speed on a 16 GB Mac).
2. `ai_prompt_enhance {"idea", "target": "flux"}` → `ai_generate_image {"prompt", "size", "count"}`.
3. Edit: `ai_edit_image` (img2img / inpaint with `mask_box` / outpaint `expand_to: "9:16"`),
   `ai_upscale`.
4. Local models (optional, big): `comfyui_setup` (dry run lists bundles, GB and licences) →
   user agrees → `confirm: true` → `comfyui_start`. On Apple Silicon `mflux_setup` is the fastest
   image path. Everything goes to STUDIO_HOME/models on the SSD.
5. Video: short abstract/product loops locally (LTX-Video/Wan, minutes per clip); anything with
   people talking, characters, Arabic speech or cinematic story → `ai_generate_video` writes a
   hand-off brief for **flow-studio-director** (Google Flow, Veo 3.1).
6. Paid APIs only via `ai_generate_image_byok` with the user's own key, dry run first.

## Quality checklist before delivering

- Previews looked at; no text overflow or clipped words (fit report ok).
- Contrast: body text ≥ 4.5:1 (`design_check` / palette pairs).
- Arabic: reads right-to-left, joined letters, no boxes, dialect as agreed; captions proofread.
- Video: no black frames, audio not cut, loudness ≈ −14 LUFS social / −16 podcast, captions inside
  the safe zone and not on top of on-screen text.
- Files named and grouped under `projects/<name>/`; editable masters included; licences for AI
  output and library music passed on.
