# Worked run: "Qahwa House" café launch (brief → brand → post → menu → voice → sting → reel)

A real end-to-end run of the studio (previews in `qahwa_house/`). Every call is shown as it was
made; `call.sh` = `bash scripts/call.sh`.

**Brief:** specialty coffee shop in Maadi, Cairo; warm, crafted, modern; young professionals;
bilingual (English + Egyptian Arabic); launch offer "first cup free".

## 1. Brand kit
```bash
call.sh brand_create '{"name":"Qahwa House","name_ar":"بيت القهوة","brief":"specialty coffee shop in Maadi, Cairo; warm, crafted, modern","sector":"coffee","audience":"young professionals","tagline":"Crafted in Cairo","tagline_ar":"معمولة في القاهرة","concepts":4}'
```
→ read as sector *coffee*, palette "terracotta roast" (#B5523B / #3A2419 / #E8B04B on cream),
type Fraunces + Work Sans / El Messiri + Tajawal, concepts: cup, bean, arch, "Q" monogram
(`1-logo-concepts.jpg`). The user chose c1 (cup): `call.sh brand_choose_logo '{"brand":"qahwa-house","concept":"c1"}'`.

## 2. Launch post (Arabic, story size, room for captions)
```bash
call.sh design_create '{"template":"offer","brand":"qahwa-house","size":"ig_story","project":"qahwa-launch","name":"opening-offer-story","content":{"eyebrow":"افتتاح المعادي","offer":"مجاناً","offer_label":"أول فنجان علينا","headline":"قهوة مختصة محمصة طازة كل أسبوع","cta":"شارع ٩، المعادي","lang":"ar","leave_bottom":0.26}}'
```
No product photo → the brand's cup sits in the offer disc (`3-offer-post.jpg` is the 4:5 version).
First attempt forgot `offer` and the tool warned: *template 'offer' expects 'offer'* — read warnings.

## 3. Menu (A4 print, bleed + crop marks)
```bash
call.sh design_create '{"template":"menu","brand":"qahwa-house","size":"a4","project":"qahwa-launch","content":{"headline":"Menu","sections":[{"title":"Espresso bar","items":[{"name":"Espresso","price":"55"},{"name":"Flat white","price":"85"}]},{"title":"Slow bar","items":[{"name":"V60 — Ethiopia Guji","price":"110"}]}]}}'
```

## 4. Egyptian voiceover
```bash
call.sh audio_voiceover '{"text":"أهلاً بيكم في بيت القهوة. قهوة مختصة، محمصة طازة كل أسبوع، في قلب المعادي. أول فنجان علينا!","voice":"auto","project":"qahwa-launch"}'
```
→ ar-EG-SalmaNeural, 10.9 s, −16.3 LUFS, `.srt` aligned to the voice.

## 5. Logo sting (portrait → stacked lockup)
```bash
call.sh motion_logo_reveal '{"brand":"qahwa-house","size":"1080x1920","duration":4,"project":"qahwa-launch"}'
```

## 6. The reel
`timeline.json`:
```json
{"size":"9:16","fps":30,
 "clips":[{"image":".../design/opening-offer-story-ig-story.png","duration":8,"ken_burns":"in"},
          {"src":".../motion/logo_reveal-qahwa-house-stacked-reversed.mp4","transition":{"type":"dissolve","duration":0.6}}],
 "audio":[{"src":".../audio/vo-ar-eg-salmaneural.wav","at":0.4}],
 "captions":{"auto":true,"style":"reels","position":"bottom"},
 "fade_out":0.5,"loudness":"social"}
```
```bash
call.sh video_edit '{"timeline":"timeline.json","brand":"qahwa-house","project":"qahwa-launch","name":"opening-reel"}'
```
→ 11.4 s 1080×1920 MP4 (−14 LUFS), `.srt`, `.ass`, `.kdenlive` (+ its melt check preview).
`5-reel-contact-sheet.jpg` shows the result. What the run taught (now built in): a 4:5 post in a
9:16 reel is placed whole on a blurred fill instead of being cropped; with the first 7 s still the
voiceover (11.25 s) ran past the picture — the edit warned *the audio is CUT*, so the still went
to 8 s; captions on a text-heavy design → design with `leave_bottom`.

## Deliver
`STUDIO_HOME/projects/qahwa-launch/` — design PNGs + `.design` masters, menu PDF + crop-marks PDF,
voiceover WAV + SRT, sting MP4, reel MP4 + `.kdenlive` + `.srt`; brand kit in
`STUDIO_HOME/brands/qahwa-house/` (logo suite SVG/PNG/ICO, brand.json). Offer
`brand_guidelines` and `brand_apply` next.
