# creative-studio — tool reference

Generated from studio-mcp (`studio help <tool>` shows the same). Flags: **N** uses the internet · **$** may spend money (needs the user's OK) · **I** installs something (needs the user's OK).

## system (3)

### `open_in_app`

Open a file the studio made in the free desktop app that edits it, so the user can take over
by hand: .psd/.xcf → GIMP, .svg/.pdf → Inkscape, .kra → Krita, .kdenlive/.mlt → Kdenlive,
.blend → Blender, .aup3/.wav → Audacity. app='auto' picks by extension.

Arguments: `path: str`; `app: str = 'auto'`

### `studio_doctor`

Start here. Lists every free tool the studio can drive, whether it is installed, what it is
for, and the exact install command for the missing ones. Also shows STUDIO_HOME (where outputs
and AI models are kept).

Arguments: 

### `studio_install` [NI]

Install the free tools for a department: core, design, photo, video, audio, ai, apps (or one
dependency name from studio_doctor). With confirm=false it only lists what WOULD be installed
and the download sizes — show that to the user; call again with confirm=true only after they agree.
Python packages go into this studio's own environment; apps via Homebrew (macOS) or apt (Linux). · INSTALLS software — only with the user's explicit OK

Arguments: `group: str = 'core'`; `confirm: bool = False`

## brand (9)

### `brand_apply` [N]

Apply a brand: generate a ready-to-post starter set in the brand's colours, fonts and logo —
social avatar, Instagram post + story + quote templates, LinkedIn/X/Facebook/YouTube covers, website
share image, print-ready business card (front/back PDF with bleed + crop marks), A4 letterhead PDF,
and an email signature (HTML + preview). Every item is an editable design master.
contact: {"name", "title", "name_ar", "title_ar", "phone", "email", "website", "address", "handle"}.
assets: subset of avatar, post, story, quote, linkedin_cover, x_header, fb_cover, youtube_banner,
og_image, business_card, letterhead, email_signature (default all). logo_url: public URL of the logo
for the email signature (email clients can't embed local files). Returns files + a contact sheet.

Arguments: `brand: str`; `contact: dict | str = ''`; `assets: list | str = ''`; `logo_url: str = ''`; `project: str = ''`

### `brand_choose_logo` [N]

Build the full logo suite for one concept (and optionally tweak it): horizontal + stacked lockups,
icon, wordmark (+ Arabic wordmark), monogram — each in colour, reversed, mono black, mono white —
plus app icon, favicon.svg/.ico and PNG sizes (16/32/48/180/192/512). Returns the suite sheet to LOOK at.
Tweaks: wordmark_font (Google family), case (title|upper|lower), tracking (em, e.g. 0.1), mark (kind),
dot ('yes'/'no' accent full stop).

Arguments: `brand: str`; `concept: str = 'c1'`; `wordmark_font: str = ''`; `case: str = ''`; `tracking: float = -99`; `mark: str = ''`; `dot: str = ''`

### `brand_create` [N]

Create a complete brand kit from a brief: colour palette (harmony + tints + WCAG-checked text
pairs), Arabic+Latin type pairing, 3–6 logo concepts (geometric mark + outlined wordmark, Arabic name
shaped correctly) with the full SVG/PNG/ICO suite for one of them, and starter voice & tone notes.
Saved to STUDIO_HOME/brands/<slug>/brand.json so every design tool can use brand=<slug>.
Returns previews to LOOK at: concept sheet, palette, typography, logo suite.

personality: e.g. "modern, friendly, trustworthy". base_color: optional hex/name (else derived from
sector/personality). The brief is read whole-word into a sector (coffee, food, tech, finance, health,
wellness, eco, education, kids, property, travel, luxury, heritage, sport, creative, logistics,
community) → a curated palette for that category (varied per brand name), fitting type pairings and
subject marks (e.g. coffee → cup, bean, arch; finance → shield, bars). Pass sector= to force it. harmony: auto | complementary | analogous | triadic | split | tetradic | monochrome.
font_pair: modern, corporate, friendly, playful, luxury, editorial, heritage, bold, geometric, creative,
news, egypt-classic (see design_catalog pairs). choose: concept built into the suite (change later with
brand_choose_logo). Logos are typographic/geometric — honest starting points a designer would refine.

Arguments: `name: str`; `brief: str = ''`; `sector: str = ''`; `audience: str = ''`; `personality: list | str = ''`; `name_ar: str = ''`; `tagline: str = ''`; `tagline_ar: str = ''`; `base_color: str = ''`; `harmony: str = 'auto'`; `font_pair: str = ''`; `concepts: int = 4`; `choose: str = 'c1'`; `overwrite: bool = False`

### `brand_guidelines` [N]

Brand guidelines book as a multi-page vector PDF (A4 landscape): cover, contents, essence, voice &
tone, logo, clear space & minimum sizes, variations, misuse, colour (HEX/RGB/CMYK), measured WCAG pairs,
Arabic + Latin typography, applications (renders a few branded assets when applications=true), back
cover. Returns the PDF, page PNGs and a contact sheet to LOOK at.

Arguments: `brand: str`; `applications: bool = True`; `project: str = ''`

### `brand_logo_concepts` [N]

Generate a fresh set of logo concepts for a saved brand (keeps the current chosen logo until you
call brand_choose_logo). marks: optional list — lettermarks monogram_circle, monogram_square,
monogram_letter, letter_split, hexagon, shield; geometry quarters, orbit, stack, petals, arch, spark,
chevrons, leaf, wave, star8, sun; subject marks cup, bean, bowl, drop, roof, book, bars, bolt, heart,
plus, pyramid, bubble, pin, sprout. Default: picked from the brief's sector.
fonts: optional Latin families to try for the wordmark. variation: any text → different random seed.
Returns the concept sheet to LOOK at.

Arguments: `brand: str`; `count: int = 4`; `marks: list | str = ''`; `fonts: list | str = ''`; `variation: str = ''`

### `brand_palette`

Colour palette generator: from a base colour (hex/name) or a brief ('organic juice bar, fresh,
friendly'), build primary/secondary/accent + tinted neutrals, 50–900 ramps and WCAG-checked text pairs
(contrast ratio + AA/AAA). harmony: auto | complementary | analogous | triadic | split | tetradic |
monochrome. With brand + apply=true it replaces that kit's colours (logos are rebuilt); colors
{"accent": "#..."} overrides individual roles. Returns a palette sheet to LOOK at.

Arguments: `base_color: str = ''`; `brief: str = ''`; `harmony: str = 'auto'`; `brand: str = ''`; `apply: bool = False`; `colors: dict | str = ''`

### `brand_show`

List saved brand kits (no argument) or show one kit: colours, fonts, voice, logo files and previews.

Arguments: `brand: str = ''`

### `brand_type_pairing` [N]

Typography pairing for Arabic + Latin: pick a curated pair by mood words ('luxury, calm') or id, or
set families yourself (any Google font). Renders a bilingual specimen (headline + body in both scripts)
to LOOK at. With brand + apply=true it updates the kit (logos keep their wordmark font until
brand_choose_logo).

Arguments: `moods: list | str = ''`; `pair: str = ''`; `head: str = ''`; `body: str = ''`; `head_ar: str = ''`; `body_ar: str = ''`; `head_weight: int = 0`; `brand: str = ''`; `apply: bool = False`

### `brand_update`

Edit a saved brand kit: changes = {"tagline": "...", "tagline_ar": "...", "name_ar": "...",
"colors": {"accent": "#FF6B4A"}, "fonts": {"head": "Sora"}, "voice": {...}, "personality": [...],
"audience": "...", "brief": "..."}. Colour changes rebuild the logo suite. Returns the updated kit.

Arguments: `brand: str`; `changes: dict | str`

## design (8)

### `design_carousel` [N]

Multi-slide carousel (Instagram / LinkedIn) with one consistent look: shared header/logo, page
counter, progress dots and a swipe hint. Returns one PNG per slide + a PDF (LinkedIn document post),
an editable master and a contact sheet to LOOK at.

slides: [{"template": "headline", "headline": "..."}, {"template": "list", "headline": "...", "items": [...]},
{"template": "stat", "stat": "73%", "label": "..."}, {"template": "quote", ...}, {"template": "headline",
"headline": "Follow for more", "cta": "Save this post", "mode": "accent"}]. Any design template works per slide;
per-slide "mode" varies the background. 3–10 slides read best; keep ≤ 25 words per slide.

Arguments: `slides: list | str`; `size: str = 'ig_portrait'`; `brand: str = ''`; `style: str = ''`; `mode: str = ''`; `handle: str = ''`; `colors: dict | str = ''`; `fonts: dict | str = ''`; `formats: str = 'png,pdf'`; `name: str = ''`; `project: str = ''`; `out: str = ''`

### `design_catalog`

List what the design department can make: templates (with their content fields and best sizes),
size presets (with platform safe zones), colour styles and Arabic+Latin font pairings.
what: all | templates | sizes | styles | pairs.

Arguments: `what: str = 'all'`

### `design_check`

QC any finished image or design master before publishing: size vs the platform preset, WCAG
contrast of text (masters only), text outside safe zones, and a preview with the platform's safe zone
and UI overlays drawn on top so you can LOOK at what the app will cover. path: PNG/JPG or .design folder.

Arguments: `path: str`; `size: str = ''`; `show_safe_zone: bool = True`

### `design_contrast`

WCAG 2.x contrast ratio of two colours (hex or name) with AA/AAA grades for normal and large text,
plus the nearest passing variant of the foreground if it fails. Fast — no rendering.

Arguments: `foreground: str`; `background: str`

### `design_create` [N]

Make a finished, agency-quality design from a professional template + a JSON content spec —
social posts, stories, thumbnails, banners, posters, flyers, business cards, certificates, menus,
infographics, letterheads. Returns exported files (PNG/JPG/WebP/PDF/SVG), an editable master folder
and a preview to LOOK at, plus measured QC (text fit, WCAG contrast, safe zones).

template: see design_catalog (headline, photo, split, quote, stat, list, event, offer, editorial,
thumbnail, banner, poster, flyer, business_card, certificate, menu, infographic, letterhead, avatar).
content: {"headline": "Grow *faster*", "eyebrow": "...", "subhead": "...", "cta": "...", "image": "path|url",
"handle": "@you", "lang": "auto|ar|en", "leave_bottom": 0.3 (keep the lower 30% empty — for reels
that get burned-in captions), ...} — *word* = highlight colour, ==word== = marker, \n = break.
Arabic content flips the layout to RTL automatically. size: preset (ig_square, ig_portrait, ig_story,
youtube_thumbnail, linkedin_cover, a4, a3, business_card…), 'WxH' px or 'WxHmm'; several comma-separated
= one design exported at each size. brand: saved brand kit slug (brand_create) — applies its colours,
fonts and logo. style (no brand): studio, midnight, electric, sunset, mint, mono, nile, rose.
mode: light | dark | brand | accent | ink (background choice). formats: png,jpg,webp,pdf,svg ('auto' =
png for screen; pdf+png for print). Print sizes get 3 mm bleed + a crop-marks PDF; cmyk=true converts
with Ghostscript when installed. Fonts are Google Fonts downloaded once and cached.

Arguments: `template: str = 'headline'`; `content: dict | str = ''`; `size: str = ''`; `brand: str = ''`; `style: str = ''`; `mode: str = ''`; `colors: dict | str = ''`; `fonts: dict | str = ''`; `formats: str = 'auto'`; `bleed_mm: float = -1`; `crop_marks: bool = True`; `cmyk: bool = False`; `name: str = ''`; `project: str = ''`; `out: str = ''`

### `design_fonts` [N]

Search Google Fonts (free, OFL) and optionally render a specimen PNG of one family so you can
LOOK before choosing. query filters by name/category/notes ('kufi', 'serif', 'display'); arabic=true
lists only Arabic-capable families (curated best ones first). specimen='Cairo' downloads it (cached in
STUDIO_HOME/cache/fonts) and renders weights with Arabic + Latin sample text (sample overrides).

Arguments: `query: str = ''`; `arabic: bool = False`; `specimen: str = ''`; `sample: str = ''`; `project: str = ''`; `out: str = ''`

### `design_render_html` [N]

Power tool: render ANY HTML/CSS you write (a string or a path to an .html file / master folder) with
headless Chromium to PNG/JPG/WebP/PDF/SVG — pixel-exact, real web typography, Arabic shaping and RTL.
Returns files, a preview to LOOK at and QC (overflow, contrast, missing fonts/images).

Conventions (all optional): wrap each page/artboard in <section class="page"> (sized by the tool to
`size`); fonts: ["Cairo", "Inter:400,800"] → downloaded once and embedded as @font-face; use them by
name in CSS. brand: a kit slug → CSS variables --primary --secondary --accent --ink --paper and families
'sf-head'/'sf-body'. Text fitting: put text in a [data-fit-box] container with fixed size and give text
elements data-fit data-max="120" data-min="40" (px). A full-size .page gets var(--u) = 1% of the short side.
sizes: comma list to render the same responsive HTML at several sizes. Print: size 'a4' etc. →
vector PDF with bleed_mm bleed (design to the bleed-inclusive page).

Arguments: `html: str`; `size: str = '1080x1080'`; `sizes: str = ''`; `formats: str = 'png'`; `fonts: list | str = ''`; `brand: str = ''`; `pages: int = 0`; `name: str = ''`; `project: str = ''`; `out: str = ''`; `bleed_mm: float = 0`

### `design_resize` [N]

Export set: re-flow an existing design master (a .design folder made by design_create /
design_carousel) to other size presets — the template re-lays out for each aspect ratio (not a crop).
Returns files for every size and previews to LOOK at. For hand-written HTML masters use
design_render_html with sizes instead.

Arguments: `master: str`; `sizes: str = 'ig_square,ig_portrait,ig_story'`; `formats: str = 'auto'`; `project: str = ''`; `out: str = ''`

## photo (20)

### `photo_adjust`

Lightroom-style manual adjustments in one pass (all default 0 = unchanged). Ranges: exposure_stops
−3…+3; contrast/highlights/shadows/whites/blacks/saturation/vibrance/clarity −1…+1; temperature
−1 cool…+1 warm; tint −1 green…+1 magenta; curves {'rgb':[[0,0],[64,50],[192,210],[255,255]],
'r':…,'g':…,'b':…} (0–255 points, smooth monotone); sharpen 0…2; denoise 0…1 (OpenCV NL-means);
vignette −1…+1; grain 0…1; fade 0…1 (matte blacks). Returns the image + before/after preview and
clipping stats.

Arguments: `image: str`; `exposure_stops: float = 0.0`; `contrast_amount: float = 0.0`; `highlights: float = 0.0`; `shadows: float = 0.0`; `whites: float = 0.0`; `blacks: float = 0.0`; `saturation_amount: float = 0.0`; `vibrance_amount: float = 0.0`; `temperature_amount: float = 0.0`; `tint: float = 0.0`; `curves: dict = {}`; `clarity_amount: float = 0.0`; `sharpen_amount: float = 0.0`; `denoise_strength: float = 0.0`; `vignette_amount: float = 0.0`; `grain_amount: float = 0.0`; `fade_amount: float = 0.0`; `format: str = ''`; `quality: int = 92`; `project: str = ''`; `out: str = ''`

### `photo_apply_lut`

Apply a 3D .cube LUT (from Resolve, a LUT pack, or photo_look export_cube) with trilinear
interpolation; strength 0…1 blends with the original. Before/after preview.

Arguments: `image: str`; `lut: str`; `strength: float = 1.0`; `format: str = ''`; `quality: int = 92`; `project: str = ''`; `out: str = ''`

### `photo_auto_enhance`

One-click enhance: neutralises colour casts (robust grey-world white balance), sets black/white
points from the histogram, adds local contrast (CLAHE on lightness) when the photo is flat, a touch of
vibrance and output sharpening. strength 0…1.5 scales everything. Before/after preview + stats.

Arguments: `image: str`; `strength: float = 1.0`; `white_balance: bool = True`; `local_contrast: bool = True`; `format: str = ''`; `quality: int = 92`; `project: str = ''`; `out: str = ''`

### `photo_batch`

Run any single-image photo tool over every image in a folder (e.g. tool_name='photo_resize',
args={'width':1080,'height':1350,'mode':'fill'}; or photo_convert, photo_adjust, photo_look,
photo_remove_background, photo_apply_lut, photo_upscale …). `pattern` filters files ('*.jpg').
Outputs go to one folder; returns every file plus a contact sheet of the results.

Arguments: `folder: str`; `tool_name: str`; `args: dict = {}`; `pattern: str = '*'`; `project: str = ''`; `out: str = ''`

### `photo_canvas`

Extend the canvas without scaling the photo: to width×height, to an aspect ratio ('1:1', '9:16'),
or by `padding` px on every side. color: any colour, 'transparent', or 'blur' (blurred extension of
the photo — good for putting landscape photos into stories). anchor: center/top/bottom/left/right/
top-left…

Arguments: `image: str`; `width: int = 0`; `height: int = 0`; `ratio: str = ''`; `padding: int = 0`; `color: str = '#ffffff'`; `anchor: str = 'center'`; `format: str = ''`; `quality: int = 92`; `project: str = ''`; `out: str = ''`

### `photo_collage`

Collage / grid of photos: layout 'grid' (auto rows×cols for the canvas ratio, last row centred),
'hero' (one big image + a row below), 'mosaic' (big left + stacked right column). Images come from
`images` (paths, in order) or a `folder`. Each cell is filled with a subject-aware crop (faces kept),
with gap, rounded corners, background colour and optional captions (Arabic works). Returns the
collage + preview.

Arguments: `images: list[str] = []`; `folder: str = ''`; `width: int = 2000`; `height: int = 2000`; `layout: str = 'grid'`; `gap: int = 16`; `radius: int = 0`; `background: str = '#ffffff'`; `smart_crop: bool = True`; `captions: list[str] = []`; `caption_color: str = '#ffffff'`; `format: str = 'jpg'`; `quality: int = 92`; `project: str = ''`; `out: str = ''`

### `photo_compare`

Before/after comparison image for portfolios and client approval: mode 'side_by_side', 'stacked'
(vertical), or 'split' (one frame, left = before, right = after, divider with a handle at `split`
0…1). Labels can be Arabic. `after` is resized to `before` when sizes differ.

Arguments: `before: str`; `after: str`; `mode: str = 'side_by_side'`; `labels: list[str] = ['Before', 'After']`; `split: float = 0.5`; `width: int = 0`; `format: str = 'jpg'`; `quality: int = 92`; `project: str = ''`; `out: str = ''`

### `photo_compose_layers` [N]

The 'Photoshop file' deliverable: build a layered design from a JSON spec (photos, cut-outs, text
incl. Arabic/RTL with any Google/system font, shapes, gradients, blend modes, opacity, drop shadows as
separate layers) and write (1) an editable layered PSD (opens in Photoshop/Photopea/GIMP/Krita/
Affinity — pixel layers with names, positions, blend modes, opacity; text as pixels), (2) a GIMP XCF
where text layers are LIVE editable GIMP text (needs GIMP, 2.10 or 3.x), (3) flattened PNG (and JPG).
Returns files + the flattened preview + a layers sheet; with verify, GIMP re-renders the XCF and the
difference to our PNG is reported. spec is a dict or a path to a .json file (format below). Fonts
missing locally are fetched free from Google Fonts.

SPEC format:
{
"width": 1080, "height": 1350, "background": "#0f172a" | "linear:#0f172a,#1e3a8a,90" | "/path/photo.jpg" | "transparent",
"layers": [   // bottom → top
{"type": "image", "name": "Photo", "src": "/path/a.jpg", "x": 0, "y": 0, "width": 1080, "height": 900,
"fit": "cover|contain|stretch", "radius": 24, "remove_background": false, "rotate": 0},
{"type": "shape", "name": "Card", "shape": "rect|ellipse|polygon|line", "x": 60, "y": 980, "width": 960, "height": 300,
"radius": 32, "fill": "#ffffff" | {"type":"linear","colors":["#f59e0b","#ef4444"],"angle":0}, "stroke": {"color":"#000","width":2},
"points": [[x,y],…] (polygon/line), "line_width": 6},
{"type": "text", "name": "Headline", "text": "عرض خاص النهارده بس", "font": "Cairo", "weight": 800, "size": 96,
"color": "#ffffff", "x": 80, "y": 1000, "width": 920, "align": "right|left|center", "direction": "auto|rtl|ltr",
"line_height": 1.25, "letter_spacing": 0, "stroke": {"color": "#000", "width": 3}},
{"type": "fill", "name": "Tint", "fill": "#000000" | gradient, "opacity": 0.3, "blend": "multiply"}
]
// every layer: "opacity" 0–1, "blend" (normal multiply screen overlay soft_light hard_light darken lighten
// difference exclusion color_dodge color_burn add hue saturation color luminosity), "visible",
// "shadow": true | {"color":"#000","dx":0,"dy":12,"blur":24,"opacity":0.4,"spread":0}  (becomes its own layer)
}

Arguments: `spec: dict`; `name: str = 'composition'`; `psd: bool = True`; `xcf: bool = True`; `png: bool = True`; `jpg: bool = False`; `verify: bool = True`; `project: str = ''`; `out: str = ''`

### `photo_convert`

Convert to PNG / JPG / WebP / AVIF / TIFF / GIF (quality 1–100; 100 = lossless for WebP),
optionally limit the long side (max_side px), strip or keep EXIF, and flatten transparency onto
`background` for JPEG. Colour profiles are converted to sRGB for web formats. Reports the size
saving.

Arguments: `image: str`; `format: str = 'webp'`; `quality: int = 88`; `max_side: int = 0`; `strip_metadata: bool = True`; `background: str = '#ffffff'`; `project: str = ''`; `out: str = ''`

### `photo_crop`

Exact crop. Either box=[left, top, right, bottom] in pixels, or margins to cut from each side
(left/top/right/bottom px). trim=true removes uniform borders / transparent edges automatically.

Arguments: `image: str`; `left: int = 0`; `top: int = 0`; `right: int = 0`; `bottom: int = 0`; `box: list[int] = []`; `trim: bool = False`; `format: str = ''`; `quality: int = 92`; `project: str = ''`; `out: str = ''`

### `photo_info`

Inspect an image before editing: size, megapixels, mode, alpha, DPI, format, EXIF camera/date,
colour profile, exposure stats (clipping, brightness, contrast) and detected faces. Returns the
numbers in data and a preview PNG to look at.

Arguments: `image: str`

### `photo_look`

Film / cinematic colour grade presets: teal_orange, film_portra, film_fuji, kodachrome,
bleach_bypass, noir, bw_soft, vintage_warm, moody_matte, cross_process, golden_hour, clean_bright,
blockbuster_cool, sepia. strength 0…1 blends with the original; optional grain/vignette.
export_cube=true also writes the look as a 33³ .cube LUT (use it in Resolve, Premiere, Kdenlive,
ffmpeg lut3d or photo_apply_lut); with no image it only writes the .cube. look='all' renders a
contact sheet of every look on your image so the user can pick.

Arguments: `image: str = ''`; `look: str = 'teal_orange'`; `strength: float = 1.0`; `grain_amount: float = 0.0`; `vignette_amount: float = 0.0`; `export_cube: bool = False`; `format: str = ''`; `quality: int = 92`; `project: str = ''`; `out: str = ''`

### `photo_mockup`

Place a design on a surface. Built-in generated scenes (no stock photos needed): scene='phone'
(tilted modern smartphone on a soft backdrop — screens, app shots, stories), 'poster' (framed print on
a wall), 'cards' (business cards on a dark desk, back colour picked from the design). Or corner-pin
into YOUR photo: photo=path + corners=[[x,y] TL, TR, BR, BL] of the screen/poster/box face; surface=
'print' multiplies the photo's lighting and texture into the design, 'screen' keeps it emissive with
a faint glare; lighting 0…1 sets how much. fit: cover | contain | stretch. background='#top,#bottom'
recolours scene backdrops. Returns the mockup + preview.

Arguments: `design: str`; `scene: str = 'phone'`; `photo: str = ''`; `corners: list[list[float]] = []`; `fit: str = 'cover'`; `surface: str = 'print'`; `lighting: float = 0.8`; `width: int = 1600`; `height: int = 1200`; `background: str = ''`; `format: str = 'jpg'`; `quality: int = 92`; `project: str = ''`; `out: str = ''`

### `photo_remove_background`

Remove the background → transparent PNG (local AI, no upload). model: isnet-general-use (best,
default), u2net, u2net_human_seg (people), isnet-anime (art), silueta/u2netp (small, fast); the
model (5–180 MB) downloads once from Hugging Face into STUDIO_HOME/models/rembg. edges: 'soft'
(guided-filter refinement keeps hair), 'hard' (crisp product edges), 'matting' (pymatting, slow),
'raw'. clean_fringe removes old-background colour on edges. shadow: none | contact | drop | both.
crop_to_subject trims to the subject (+padding px). Also saves the mask (subject cut-out). Preview on
a checkerboard.

Arguments: `image: str`; `model: str = 'isnet-general-use'`; `edges: str = 'soft'`; `clean_fringe: bool = True`; `shadow: str = 'none'`; `crop_to_subject: bool = False`; `padding: int = 0`; `save_mask: bool = True`; `project: str = ''`; `out: str = ''`

### `photo_replace_background`

Put the subject on a new background: a colour ('#f5efe6'), a gradient ('linear:#1e3a8a,#60a5fa,90'
or 'radial:#fff,#d1d5db'), or a photo path. Works on photos (removes the background first) or on
transparent PNG cut-outs. width/height set the canvas (default: original size); subject_scale is the
subject's max share of the canvas; position center|bottom|left|right; shadow contact|drop|both|none;
blur_background (px) for photo backgrounds; match_light nudges the subject's colour toward the scene
and adds a subtle light wrap. Returns the composite + before/after preview.

Arguments: `image: str`; `background: str = '#f2f2f2'`; `width: int = 0`; `height: int = 0`; `subject_scale: float = 0.85`; `position: str = 'center'`; `shadow: str = 'contact'`; `blur_background: float = 0.0`; `match_light: bool = True`; `model: str = 'isnet-general-use'`; `format: str = 'jpg'`; `quality: int = 92`; `project: str = ''`; `out: str = ''`

### `photo_resize`

Resize a photo. mode: 'fit' (inside width×height, keeps ratio), 'fill' (cover the exact size and
crop — crop='smart' keeps faces/subject, or center/top/bottom/left/right), 'pad' (fit then pad to
exact size with pad_color, 'blur' for a blurred-photo fill, or 'transparent'), 'exact' (stretch).
Or give scale (e.g. 0.5) or long_edge (px). High-quality Lanczos; upscaling >2× warns (use
photo_upscale). Returns the resized file + preview.

Arguments: `image: str`; `width: int = 0`; `height: int = 0`; `mode: str = 'fit'`; `scale: float = 0.0`; `long_edge: int = 0`; `crop: str = 'smart'`; `pad_color: str = '#ffffff'`; `format: str = ''`; `quality: int = 92`; `project: str = ''`; `out: str = ''`

### `photo_retouch`

Remove objects, blemishes, dust, wires or text by painting a mask — offline OpenCV inpainting
method 'auto' (default: diffusion for tiny spots, content-aware patch copy + Poisson seamless
blending for larger areas), 'patch', 'telea' or 'ns' (pure diffusion), with grain matching so the patch doesn't look plastic. Give `mask` (white =
remove, any size — it is scaled) or `regions`: [{'type':'circle','x':..,'y':..,'r':..},
{'type':'rect','x','y','w','h'}, {'type':'polygon','points':[[x,y],…]}, {'type':'stroke','points':…,
'width':..}]. Best for small/medium areas on textured backgrounds; for big objects or areas that need
new content (a person, a building), use the ai department's generative inpaint instead. Returns
the result + before/after preview with the mask outlined.

Arguments: `image: str`; `mask: str = ''`; `regions: list[dict] = []`; `method: str = 'auto'`; `grow: int = 4`; `match_grain: bool = True`; `format: str = ''`; `quality: int = 92`; `project: str = ''`; `out: str = ''`

### `photo_rotate`

Rotate (degrees, counter-clockwise positive) and/or flip ('horizontal' | 'vertical').
expand=true keeps the whole image (corners filled with `fill`: 'auto' = transparent for PNG, white
for JPEG, 'crop' = crop to the largest clean rectangle). auto_straighten=true detects the horizon /
dominant lines (OpenCV) and levels them.

Arguments: `image: str`; `angle: float = 0.0`; `flip: str = ''`; `expand: bool = True`; `fill: str = 'auto'`; `auto_straighten: bool = False`; `format: str = ''`; `quality: int = 92`; `project: str = ''`; `out: str = ''`

### `photo_smart_crop`

Subject-aware crop to any aspect ratio ('1:1', '4:5', '9:16', '16:9', 'story', 2.39 …). Finds faces
(kept whole, eyes near the upper third) and the visually important region (saliency); with
use_subject_mask=true it also uses the AI background-removal mask (slower, best for products).
zoom>1 crops tighter. width>0 also resizes. Returns the crop and a preview showing the chosen box.

Arguments: `image: str`; `ratio: str = '1:1'`; `zoom: float = 1.0`; `use_subject_mask: bool = False`; `width: int = 0`; `format: str = ''`; `quality: int = 92`; `project: str = ''`; `out: str = ''`

### `photo_upscale`

Enlarge a photo 2×/3×/4× with AI super-resolution, offline: Real-ESRGAN 'realesr-general-x4v3'
(compact GAN model, BSD-3, 5 MB ONNX fetched once from Hugging Face) run tiled on CPU (CoreML on
Mac when available). It restores edges and texture and removes JPEG blocking — it does invent fine
detail, so check faces/text in the preview. model='lanczos' = classic resampling + light sharpening
(no AI). detail_blend 0…1 mixes some Lanczos back in for a more natural look. Transparent images keep
their alpha (upscaled with Lanczos).

Arguments: `image: str`; `scale: int = 4`; `model: str = 'realesr-general-x4v3'`; `detail_blend: float = 0.0`; `format: str = ''`; `quality: int = 92`; `project: str = ''`; `out: str = ''`

## vector (8)

### `vector_boolean`

Boolean path operations via Inkscape: union, difference (bottom minus top), intersection,
exclusion, division, cut, combine. ids = the objects to combine (see vector_info top_level_ids; order
in the file decides top/bottom); empty = every top-level shape. The result keeps the bottom object's
fill/stroke. Returns the new SVG + before/after preview.

Arguments: `svg: str`; `operation: str = 'union'`; `ids: list[str] = []`; `project: str = ''`; `out: str = ''`

### `vector_compose` [N]

Illustrator-style vector artwork from a JSON spec (shapes, paths, gradients, groups, drop shadows,
text incl. Arabic RTL with Google/system fonts) → clean hand-editable SVG (opens in Inkscape/
Illustrator/Figma), vector PDF (print), PNG (png_scale × size). outline_text=true also writes a
print-safe copy with text converted to outlines (Inkscape). Returns files + preview.

SPEC format:
{
"width": 1000, "height": 1000, "background": "#ffffff" | {"type":"linear","colors":["#0f172a","#1e3a8a"],"angle":90} | null,
"elements": [   // painted in order (first = back)
{"type":"rect","id":"card","x":100,"y":100,"width":800,"height":500,"rx":40,"fill":"#fff","stroke":"#111","stroke_width":4},
{"type":"circle","cx":500,"cy":500,"r":200,"fill":{"type":"radial","colors":["#fde68a","#f59e0b"]}},
{"type":"ellipse","cx":..,"cy":..,"rx":..,"ry":..}, {"type":"line","x1":..,"y1":..,"x2":..,"y2":..,"stroke":"#000","stroke_width":6,"linecap":"round"},
{"type":"polygon"|"polyline","points":[[x,y],…]}, {"type":"path","d":"M10 10 C …Z","fill":"#e11d48"},
{"type":"text","text":"مرحبا بيك","x":500,"y":520,"font":"Cairo","weight":700,"size":96,"fill":"#111",
"anchor":"start|middle|end","direction":"auto|rtl|ltr","letter_spacing":0,"line_height":1.2 (for \n lines)},
{"type":"image","href":"/path/photo.png","x":0,"y":0,"width":300,"height":300}   (embedded),
{"type":"group","id":"logo","transform":"translate(100 50) rotate(-8)","elements":[…]}
]
// any element: "id", "opacity", "transform", "fill"/"stroke" as colour or gradient dict
// ({"type":"linear"|"radial","colors":[…],"stops":[0,1],"angle":deg}), "stroke_width", "linejoin",
// "shadow": {"dx":0,"dy":8,"blur":12,"color":"#000","opacity":0.3}, "class"
}

Arguments: `spec: dict`; `name: str = 'vector'`; `pdf: bool = True`; `png: bool = True`; `png_scale: float = 2.0`; `outline_text: bool = False`; `project: str = ''`; `out: str = ''`

### `vector_export`

Export an SVG. formats: pdf (vector, print), eps (vector, legacy print — Inkscape), png (at `dpi`
or `width` px), svg (plain copy). sizes=[…] writes square PNGs at each size. preset:
'icons' → PNG set 16…1024; 'favicon' → favicon.ico (16/32/48), favicon-16/32.png,
apple-touch-icon 180 (opaque), android-chrome 192/512, icon.svg, site.webmanifest + HTML snippet;
'app_icon' → iOS AppIcon.appiconset (1024 + legacy sizes, Contents.json, no alpha) and Android
mipmap-*/ic_launcher(.png/_round) + 512 Play Store icon. padding (0…0.3 of the side), background
colour and corner_radius (0…0.5) shape the icon tile. text_to_path outlines fonts in PDF/EPS.

Arguments: `svg: str`; `formats: list[str] = ['pdf', 'png']`; `dpi: int = 300`; `width: int = 0`; `sizes: list[int] = []`; `preset: str = ''`; `padding: float = 0.0`; `background: str = ''`; `corner_radius: float = 0.0`; `text_to_path: bool = False`; `name: str = ''`; `project: str = ''`; `out: str = ''`

### `vector_info`

Inspect an SVG before editing: size/viewBox, element counts, top-level ids (for vector_boolean),
colours used (for vector_recolor), fonts and whether text is live, embedded rasters, file size.
Returns numbers + a preview.

Arguments: `svg: str`

### `vector_optimize`

Clean and shrink an SVG for web/apps: removes editor junk (Inkscape/Illustrator/Figma/Sketch
namespaces, metadata, comments), unused defs and ids, empty groups, rounds coordinates to
`precision` decimals and collapses whitespace. Verifies the render is visually identical and reports
the size saving.

Arguments: `svg: str`; `precision: int = 2`; `keep_ids: bool = False`; `keep_metadata: bool = False`; `project: str = ''`; `out: str = ''`

### `vector_recolor`

Recolour an SVG (fills, strokes, gradient stops, CSS) to a brand palette. mapping={'#old':'#new'}
for exact swaps; or palette=['#0f172a','#f59e0b',…] with method 'luminance' (darkest source colour →
darkest palette colour… keeps contrast/hierarchy, best for logos & icons) or 'nearest' (closest
perceptual colour in CIE Lab). Returns recoloured SVG, the mapping used, and before/after preview.

Arguments: `svg: str`; `palette: list[str] = []`; `mapping: dict = {}`; `method: str = 'luminance'`; `project: str = ''`; `out: str = ''`

### `vector_text_to_outlines`

Convert all live text to vector outlines (paths) with Inkscape — the print-safe version to send to
printers/sign makers so fonts can't go missing. Checks that no <text> remains and that the render is
visually unchanged. Keep the original SVG as the editable master.

Arguments: `svg: str`; `project: str = ''`; `out: str = ''`

### `vector_trace`

Trace a raster (logo photo, scan, sketch, icon, illustration) into a clean vector SVG with vtracer.
colors = how many flat colours to keep (2–16; the image is first quantised with k-means so shapes come
out clean); black_and_white=true traces a single ink colour (sketches, signatures; `threshold`).
preset: logo (smooth curves, default) | illustration | sharp (straight edges) | pixel (pixel art) |
photo (posterised look). remove_background keys out a flat border colour. smooth (0–2) denoises
before tracing. Returns SVG + side-by-side (source vs vector) preview, path count and fidelity.

Arguments: `image: str`; `colors: int = 6`; `preset: str = 'logo'`; `remove_background: bool = True`; `max_side: int = 1600`; `smooth: float = 1.0`; `black_and_white: bool = False`; `threshold: int = 128`; `project: str = ''`; `out: str = ''`

## video (20)

### `video_broll`

Insert B-roll over a main video (A-roll): inserts=[{"src": "b.mp4", "at": 5.0, "duration": 3,
"in": 0}] — the main picture is covered for that time while the main AUDIO keeps playing (the
classic cutaway). fade: soft edge in seconds (0 = hard cut). Set "volume_db" on an insert to mix
its own sound in. Returns MP4 + .kdenlive + contact sheet.

Arguments: `path: str`; `inserts: list[dict]`; `fade: float = 0.2`; `keep_audio: bool = True`; `project: str = ''`; `out: str = ''`

### `video_captions`

Auto-captions burned into the video + a clean .srt (upload it to YouTube/LinkedIn) + the styled
.ass. Speech is transcribed with audio_transcribe (word timestamps) unless srt= or words= is given.
style: reels (big bold words, the spoken word gets an accent box, pop-in — Reels/TikTok/Shorts) |
bold (spoken word turns accent-coloured) | karaoke (words fill with colour as spoken) | clean
(sentence subtitles, soft shadow — YouTube/LinkedIn) | boxed (white on a dark box) | auto (reels
for vertical, clean for landscape). Arabic is shaped and ordered right-to-left (Egyptian dialect:
dialect='egyptian'). position: auto | bottom | lower | middle | top. accent: highlight colour
(default brand accent or yellow). Also writes a .kdenlive with the captions as a subtitle filter.

Arguments: `path: str`; `style: str = 'auto'`; `language: str = 'auto'`; `srt: str = ''`; `words: list = []`; `position: str = 'auto'`; `accent: str = ''`; `words_per_chunk: int = 0`; `uppercase: bool | None = None`; `size: float = 1.0`; `model: str = 'auto'`; `dialect: str = ''`; `allow_download: bool = False`; `brand: str = ''`; `project: str = ''`; `out: str = ''`

### `video_concat`

Join clips in order into one video (any mix of sizes/fps/codecs — they are conformed to `size`/
`fps`, default the first clip's). transition between every pair: cut | dissolve | dip | dip_white |
wipe_left | slide_left | zoom | iris … (transition_duration seconds, audio crossfades under it).
fit: auto | cover | contain | blur (for clips of another aspect ratio). Also writes a .kdenlive.

Arguments: `paths: list[str]`; `transition: str = 'cut'`; `transition_duration: float = 0.5`; `size: str = ''`; `fps: float = 0`; `fit: str = 'auto'`; `project: str = ''`; `out: str = ''`

### `video_edit`

The editor: render a JSON timeline to MP4 AND write the same edit as an editable Kdenlive
project (.kdenlive, checked by rendering it headless with melt). Use for anything multi-clip:
cuts, transitions (dissolve, dip, dip_white, wipe_*, slide_*, push, zoom, iris, blur…), J/L cuts,
speed changes, stills with Ken Burns, colour cards, full-frame title cards, overlays (motion
lower thirds/titles/CTAs rendered with the motion department, logos, alpha graphics, B-roll,
picture-in-picture), music with automatic ducking, auto-captions, a programme grade and loudness.

timeline = {"size": "1920x1080"|"9:16", "fps": 30, "clips": [{"src", "in", "out", "speed", "transition":
{"type","duration"}, "j_cut", "l_cut", "grade", "fit", "zoom"} | {"image", "duration", "ken_burns"} |
{"color", "duration"} | {"title", "subtitle", "duration", "style"}], "overlays": [{"type": lower_third|
title|cta|kinetic|counter|motion|shape_wipe|overlay|image|broll|pip, "at", "duration", …}], "audio":
[{"src", "at", "volume_db", "duck", "fade_in", "fade_out", "loop"}], "captions": {"auto": true,
"style": reels|bold|karaoke|clean|boxed, "position": auto|bottom|lower|center|top, "font", "font_ar"
(Arabic defaults to Tajawal — it renders right in the MP4 AND in Kdenlive)}, "extend_to_audio": true
(a voiceover longer than the picture holds the last still), "grade": "teal_orange", "fade_in", "fade_out", "loudness":
"youtube"} (a dict, JSON string or .json path; relative paths resolve next to the .json).
brand: brand kit slug for titles/lower thirds/captions. Returns MP4, .kdenlive, .srt/.ass when
captioned, a contact sheet and the melt check preview — LOOK at both.

Arguments: `timeline: dict | str`; `brand: str = ''`; `kdenlive: bool = True`; `project: str = ''`; `out: str = ''`; `name: str = 'edit'`

### `video_export`

Deliver a finished video to a platform spec: reels | tiktok | shorts (1080x1920) | youtube
(1080p) | youtube_4k | linkedin | linkedin_square | instagram_feed (1080x1350) | x | whatsapp |
prores (ProRes 422 HQ master .mov) | prores4444 | gif | webm | master. Sets size, fps, H.264
high profile + bitrate cap, AAC 48 kHz, faststart, and masters loudness to the platform target
(-14 LUFS, true peak -1). fit when the aspect ratio differs: auto (smart face-tracking reframe) |
track | blur | pad | crop. Warns about platform length limits (trim_to_limit=true cuts to fit).

Arguments: `path: str`; `preset: str = 'youtube'`; `fit: str = 'auto'`; `loudness: bool = True`; `trim_to_limit: bool = False`; `project: str = ''`; `out: str = ''`

### `video_grade`

Colour-grade a video: a named look (teal_orange, film_portra, film_fuji, kodachrome, bleach_bypass,
noir, bw_soft, vintage_warm, moody_matte, cross_process, golden_hour, clean_bright, blockbuster_cool,
sepia — the SAME looks as photo_look, via its .cube export) or any .cube LUT (Resolve/LUT packs),
blended by strength 0–1, plus manual exposure (stops-ish, ±1), contrast/saturation (−1…+1),
temperature (−1 cool … +1 warm), vibrance, vignette 0–1. Returns the graded MP4, a BEFORE/AFTER
sheet and a .kdenlive with the LUT as an effect.

Arguments: `path: str`; `preset: str = ''`; `lut: str = ''`; `strength: float = 1.0`; `exposure: float = 0.0`; `contrast: float = 0.0`; `saturation: float = 0.0`; `temperature: float = 0.0`; `vibrance: float = 0.0`; `vignette: float = 0.0`; `project: str = ''`; `out: str = ''`

### `video_loudness`

Normalise a video's audio to a platform loudness target and report the MEASURED result: youtube/
streaming/reels/tiktok (-14 LUFS), podcast/apple (-16), broadcast/ebu (-23), atsc (-24) or a number.
True-peak limited (default -1 dBTP). The picture is stream-copied (no re-encode).

Arguments: `path: str`; `target: str = 'youtube'`; `true_peak: float = -1.0`; `project: str = ''`; `out: str = ''`

### `video_music`

Add a music bed under a video with automatic ducking: the music dips duck_db whenever someone
speaks and swells in the gaps (audio_mix), fades in/out, loops short tracks with crossfades and
masters the result to `target` (-14 LUFS streaming, 'podcast' -16, 'broadcast' -23). The picture
is copied untouched. Returns the MP4 + a .kdenlive with the ducking as volume keyframes.

Arguments: `path: str`; `music: str`; `duck_db: float = 10.0`; `music_level_db: float = -18.0`; `fade_in: float = 1.0`; `fade_out: float = 2.5`; `loop: bool = True`; `target: str = 'streaming'`; `project: str = ''`; `out: str = ''`

### `video_overlay`

Put a graphic on top of a video: an alpha video from the motion department (.mov ProRes 4444 /
.webm VP9 alpha — lower thirds, titles, CTAs, transitions), a PNG logo/watermark or any image.
at/duration in seconds (duration 0 = the overlay's own length, images: to the end). position:
center | top-left | top-right | bottom-left | bottom-right | top | bottom | left | right (used when
width < 1: width = fraction of the frame width). Audio of the base video is kept.

Arguments: `path: str`; `overlay: str`; `at: float = 0.0`; `duration: float = 0.0`; `position: str = 'center'`; `width: float = 0.0`; `opacity: float = 1.0`; `fade: float = 0.0`; `project: str = ''`; `out: str = ''`

### `video_pip`

Picture-in-picture: `inset` (webcam, reaction, product shot) in a corner of `path` with rounded
corners, a thin border and a soft shadow. width = fraction of the frame width (0.3); position
top-left | top-right | bottom-left | bottom-right; duration 0 = as long as the inset lasts.
inset_audio_db: mix the inset's own sound at this gain (default: muted).

Arguments: `path: str`; `inset: str`; `at: float = 0.0`; `duration: float = 0.0`; `position: str = 'bottom-right'`; `width: float = 0.3`; `radius: int = 24`; `border: str = '#FFFFFF'`; `inset_audio_db: float | None = None`; `project: str = ''`; `out: str = ''`

### `video_probe`

Inspect a video before editing: duration, resolution, fps, codecs, rotation, alpha, audio
(codec/rate/channels + measured loudness), bitrate, and a timestamped contact sheet to LOOK at.
Returns data.info with everything ffprobe knows that matters for editing.

Arguments: `path: str`; `sheet: bool = True`; `project: str = ''`; `out: str = ''`

### `video_reframe`

Smart reframe a landscape video for Reels/TikTok/Shorts (9:16), square (1:1) or feed (4:5) — the
crop FOLLOWS the speaker's face (OpenCV YuNet; falls back to the most salient region when no face)
like a camera operator: holds still inside a dead zone, eases into moves, re-frames instantly at
scene cuts. mode: track (default) | center (static centre crop) | blur (whole frame over a blurred
fill, for wide group shots). size: output size (default 1080-wide). deadzone: 0–0.3 of the crop
width; smoothness: seconds of easing. Returns MP4, a tracking plot + contact sheet to LOOK at and
a .kdenlive with the same moves as Transform keyframes.

Arguments: `path: str`; `aspect: str = '9:16'`; `mode: str = 'track'`; `size: str = ''`; `deadzone: float = 0.1`; `smoothness: float = 0.5`; `project: str = ''`; `out: str = ''`

### `video_remove_silence`

Cut dead air out of a talking video (jump-cut edit): every pause longer than max_pause seconds
is shortened to max_pause, leading/trailing silence trimmed to keep_edges. Uses audio_trim_silence's
speech detection (threshold_db relative to the loudest speech; raise to -35 for noisy rooms), then
cuts the picture at the same points with click-free audio. jump_zoom: e.g. 1.12 alternates a
punch-in on every other segment so jump cuts feel intentional. Returns MP4 + .kdenlive (every cut
editable) + data.segments (kept source ranges) + seconds removed.

Arguments: `path: str`; `max_pause: float = 0.35`; `threshold_db: float = -42.0`; `keep_edges: float = 0.12`; `jump_zoom: float = 1.0`; `project: str = ''`; `out: str = ''`

### `video_render_project`

Render a Kdenlive/Shotcut/MLT project (.kdenlive, .mlt) to MP4 headless with melt — e.g. after the
user fine-tuned a studio edit by hand in Kdenlive. size: WxH (default the project's own). Returns
the MP4, measured, with a contact sheet.

Arguments: `project_file: str`; `size: str = ''`; `preset: str = 'youtube'`; `project: str = ''`; `out: str = ''`

### `video_speed`

Change playback speed: constant (speed=2 → twice as fast, 0.5 → slow motion) or speed RAMPS —
ramps=[{"start": 3, "end": 6, "speed": 4, "ease": 0.4}] (source seconds; eased in and out so it
feels like a real ramp). preset: 'ramp_middle' (fast through the middle third). audio: auto (pitch-
preserved time-stretch for 0.5–2×, muted beyond) | keep | mute. Also writes a .kdenlive.

Arguments: `path: str`; `speed: float = 0.0`; `ramps: list[dict] = []`; `preset: str = ''`; `audio: str = 'auto'`; `project: str = ''`; `out: str = ''`

### `video_split`

Split a video into parts: at given times (at=[12.5, 40]), every N seconds (every=60), or at
detected scene cuts (scenes=true, threshold 0.2 sensitive … 0.5 strict). Parts are frame-accurate
re-encodes. Returns the parts, their ranges in data.parts and a contact sheet of first frames.

Arguments: `path: str`; `at: list[float] = []`; `every: float = 0.0`; `scenes: bool = False`; `threshold: float = 0.35`; `project: str = ''`; `out: str = ''`

### `video_stabilize`

Stabilise shaky handheld footage (two-pass vid.stab: motion analysis, then smooth camera path).
smoothing: frames of smoothing each side (10 subtle … 40 gimbal-like); tripod=true locks the
frame completely; zoom: extra % zoom to hide moving borders (0 = automatic optimal zoom).
Falls back to ffmpeg's simpler 'deshake' when vid.stab isn't compiled in. Returns MP4 + a
before/after sheet + measured shake reduction.

Arguments: `path: str`; `smoothing: int = 20`; `zoom: float = 0.0`; `tripod: bool = False`; `project: str = ''`; `out: str = ''`

### `video_thumbnail`

Pick the best frames of a video for a thumbnail/cover: scores ~60 candidate frames for
sharpness, exposure, colourfulness and faces (bigger face = better), keeps the top `count` spread
across the video, saves them full-resolution + a comparison sheet. With title= it also designs a
finished YouTube thumbnail from the best frame (design_create 'thumbnail' template, brand-aware,
Arabic ok). Returns frames, the designed thumbnail and previews to LOOK at.

Arguments: `path: str`; `count: int = 3`; `title: str = ''`; `brand: str = ''`; `template: str = 'thumbnail'`; `project: str = ''`; `out: str = ''`

### `video_timeline_example`

Example timelines for video_edit (copy, change the paths, render): kind = full (every feature) |
talking_head (cuts + lower third + captions + music) | reel (9:16 with hook title, B-roll, captions) |
slideshow (photos with Ken Burns and dissolves).

Arguments: `kind: str = 'full'`

### `video_trim`

Cut one section out of a video (start → end, or start + duration). mode: accurate (re-encode,
frame-exact, default) | fast (stream copy, instant and lossless but snaps to the keyframe before
`start`). Returns the clip + contact sheet.

Arguments: `path: str`; `start: float = 0.0`; `end: float = 0.0`; `duration: float = 0.0`; `mode: str = 'accurate'`; `project: str = ''`; `out: str = ''`

## motion (12)

### `motion_captions`

Animated social captions as a transparent overlay (ProRes 4444 .mov + VP9 .webm) timed to an
.srt file, a segments list [{start, end, text}] or word timings words=[{word,start,end}] (e.g.
audio_transcribe's data.words — exact timing). Words are grouped into short chunks and the spoken
word is highlighted; without word timings they are estimated by length within each subtitle
(approximate — reported in warnings).

style: pop (chunk pops in, current word gets an accent box — reels style) | karaoke (words fill
with the accent colour as spoken) | clean (sentence fades in, subtle). Arabic chunks read RTL.
For burned captions directly on a video (faster, libass), use video_captions instead.

Arguments: `srt: str = ''`; `segments: list = []`; `words: list = []`; `style: str = 'pop'`; `size: str = '1080x1920'`; `fps: int = 30`; `words_per_chunk: int = 3`; `position: str = 'auto'`; `brand: str = ''`; `colors: dict = {}`; `fonts: dict = {}`; `formats: list[str] = []`; `project: str = ''`; `out: str = ''`

### `motion_countdown`

Countdown from `start` to 1 (one second per number) with number transitions, optionally
ending on end_text (e.g. "GO" / "يلا"). style: ring (progress ring sweeps each second) | bold
(huge numbers slam in with a flash). digits: latin | arabic (٥ ٤ ٣). Returns MP4 (or alpha) +
contact sheet.

Arguments: `start: int = 5`; `end_text: str = ''`; `style: str = 'ring'`; `size: str = '1920x1080'`; `fps: int = 30`; `digits: str = 'latin'`; `transparent: bool = False`; `brand: str = ''`; `colors: dict = {}`; `fonts: dict = {}`; `formats: list[str] = []`; `project: str = ''`; `out: str = ''`

### `motion_counter`

Animated number counter(s): counts up to `value` with prefix/suffix ("$", "%", "K+") and a
label, plus an underline progress bar. For a stat row pass items=[{value,label,prefix,suffix}]
(up to 4). digits: latin | arabic (٠١٢٣…). Returns MP4 (or alpha) + contact sheet.

Arguments: `value: float = 0`; `label: str = ''`; `prefix: str = ''`; `suffix: str = ''`; `decimals: int = 0`; `items: list = []`; `digits: str = 'latin'`; `duration: float = 4.0`; `size: str = '1920x1080'`; `fps: int = 30`; `transparent: bool = False`; `brand: str = ''`; `colors: dict = {}`; `fonts: dict = {}`; `formats: list[str] = []`; `project: str = ''`; `out: str = ''`

### `motion_cta`

Call-to-action overlay with alpha: subscribe (button + cursor click → 'Subscribed', bell and
like pop), follow (avatar/handle card whose + turns into ✓), link ("link in bio" pill with
bouncing arrow). text overrides the button label (Arabic ok, e.g. "اشترك"). With brand= the
brand icon is used as the avatar. Returns MOV/WebM alpha + contact sheet + HTML.

Arguments: `kind: str = 'subscribe'`; `text: str = ''`; `handle: str = ''`; `position: str = 'auto'`; `duration: float = 4.0`; `size: str = '1920x1080'`; `fps: int = 30`; `brand: str = ''`; `colors: dict = {}`; `fonts: dict = {}`; `formats: list[str] = []`; `project: str = ''`; `out: str = ''`

### `motion_infographic`

Animated infographic from data=[{label, value}] (≤ 8 rows): kind bars (horizontal bars grow
with counting values) | columns (vertical) | donut (segments draw in with a legend and total).
Labels may be Arabic. Values are drawn to scale — this is a real chart, not decoration.
Returns MP4 (or alpha) + contact sheet + HTML.

Arguments: `data: list`; `title: str = ''`; `kind: str = 'bars'`; `unit: str = ''`; `duration: float = 6.0`; `size: str = '1920x1080'`; `fps: int = 30`; `transparent: bool = False`; `digits: str = 'latin'`; `brand: str = ''`; `colors: dict = {}`; `fonts: dict = {}`; `formats: list[str] = []`; `project: str = ''`; `out: str = ''`

### `motion_kinetic_text`

Kinetic typography from text (Arabic or English): phrases separated by new lines or '|' become
beats; words animate in on a rhythm; *asterisk* words are emphasised in the accent colour with a
highlight. Duration is automatic from the word count unless given. Returns MP4 (or alpha),
contact sheet, HTML source.

style: punch (one phrase at a time, words punch in, centred — reels/promo energy) | stack (lines
stack up big and bold, earlier lines dim — explainer/manifesto) | type (typewriter with caret;
Arabic types word by word so letters stay joined). brand: saved brand kit slug.

Arguments: `text: str`; `style: str = 'punch'`; `size: str = '1920x1080'`; `fps: int = 30`; `duration: float = 0`; `transparent: bool = False`; `brand: str = ''`; `colors: dict = {}`; `fonts: dict = {}`; `formats: list[str] = []`; `project: str = ''`; `out: str = ''`

### `motion_logo_reveal`

Logo reveal / sting from an SVG (or PNG) logo — or a brand kit's own logo with brand=<slug>
(logo may then be omitted; the tagline defaults to the brand's). Returns the MP4 (or alpha
MOV/WebM), contact sheet and HTML source.

style: draw (SVG outlines draw on, then fills fade in — needs an SVG with paths/shapes) |
pop (spring scale-in with ring burst and particles) | mask (circular iris reveal, ring and a light
sweep across the logo). The logo holds on the last frame (fade_out=true fades it to the
background instead). tagline appears under the logo (Arabic ok).

Arguments: `logo: str = ''`; `tagline: str = ''`; `style: str = 'draw'`; `duration: float = 4.5`; `size: str = '1920x1080'`; `fps: int = 30`; `transparent: bool = False`; `fade_out: bool = False`; `brand: str = ''`; `colors: dict = {}`; `fonts: dict = {}`; `formats: list[str] = []`; `project: str = ''`; `out: str = ''`

### `motion_lower_third`

Lower-third name/role super with alpha, ready to overlay on an interview or talking head.
Returns ProRes 4444 .mov + VP9 .webm (both with transparency), a contact sheet (shown over a
checkerboard) and the HTML source.

style: modern (accent bar + wiping name/role panels — broadcast) | glass (rounded translucent card
with initials badge, or `photo` as the badge) | line (minimal text with a drawn accent line).
position: auto (left for Latin, right for Arabic) | left | right | center. Sits inside the
title-safe area (higher on 9:16 to clear platform UI). Arabic names/roles are shaped correctly.
brand: saved brand kit slug.

Arguments: `name: str`; `role: str = ''`; `style: str = 'modern'`; `position: str = 'auto'`; `duration: float = 6.0`; `size: str = '1920x1080'`; `fps: int = 30`; `photo: str = ''`; `brand: str = ''`; `colors: dict = {}`; `fonts: dict = {}`; `formats: list[str] = []`; `project: str = ''`; `out: str = ''`

### `motion_render_html`

Power tool: render ANY HTML animation (a file path or an HTML string) frame-exactly to video.
CSS animations/transitions, element.animate(), GSAP timelines, requestAnimationFrame/canvas
loops, setTimeout sequences and <video> elements are all driven by a virtual clock, so the
output never drops or stutters. duration: seconds (0 = window.__duration if the page sets it,
else the natural end of its animations). transparent=true keeps the page background see-through
(set html/body background: transparent) → ProRes 4444 / WebM alpha. Returns files + contact sheet.

Page hooks (optional): window.__duration = seconds; window.__ready = Promise to await (e.g. data
loading); window.__onseek = async (t) => {...} called every frame with the time in seconds.
workers>1 renders chunks in parallel pages — only for pages whose look depends purely on time
(not on state accumulated frame by frame). grain: 0–20 film grain added at encode time.

Arguments: `html: str`; `duration: float = 0`; `size: str = '1920x1080'`; `fps: int = 30`; `transparent: bool = False`; `formats: list[str] = []`; `wait_ms: int = 0`; `workers: int = 1`; `grain: float = 0`; `project: str = ''`; `out: str = ''`

### `motion_templates`

List the motion templates, their styles and what each is for (quick catalog for choosing).

Arguments: 

### `motion_title_card`

Animated title card / opener: headline revealed word by word through masks, kicker label,
accent bar, subtitle, animated gradient backdrop with film grain, and a clean outro. Returns the
MP4 (or MOV/WebM with alpha when transparent=true), a contact sheet to LOOK at, and the editable
HTML source.

style: bold (default, left-aligned editorial) | minimal (centered, letter-by-letter blur-in for
Latin, word-level for Arabic) | split (colour panels wipe across, then the title). Wrap a word in
*asterisks* to colour it with the primary colour. Arabic/English both work (RTL detected).
size: 1920x1080 | 9:16 | 1:1 | 4:5 | 4k | WxH. colors: {primary, accent, background, text, muted}.
fonts: {head, body, head_ar, body_ar} Google Fonts families, or a mood/pairing word ("luxury").
brand: saved brand kit slug (colours + fonts).

Arguments: `title: str`; `subtitle: str = ''`; `kicker: str = ''`; `style: str = 'bold'`; `align: str = 'auto'`; `duration: float = 5.0`; `size: str = '1920x1080'`; `fps: int = 30`; `transparent: bool = False`; `brand: str = ''`; `colors: dict = {}`; `fonts: dict = {}`; `formats: list[str] = []`; `project: str = ''`; `out: str = ''`

### `motion_transition`

Shape-wipe transition as an alpha overlay: the shapes fully cover the frame at the midpoint,
so cut from clip A to clip B exactly at data.cut_at. shape: diagonal (skewed colour panels
sweep across) | circle (iris grows and closes) | bars (staggered vertical bars) | split (halves
close and open). Returns MOV/WebM alpha + contact sheet; data.cut_at = the cut time in seconds.

Arguments: `shape: str = 'diagonal'`; `duration: float = 1.2`; `size: str = '1920x1080'`; `fps: int = 30`; `brand: str = ''`; `colors: dict = {}`; `formats: list[str] = []`; `project: str = ''`; `out: str = ''`

## audio (16)

### `audio_analyze`

Measure and SEE any audio (or a video's audio): duration, integrated loudness (LUFS), true peak,
silence %, clipping, stereo phase, noise floor, spectral balance, plus a waveform+spectrogram PNG to
look at. Pass target (e.g. 'podcast', '-14') to get a pass/fail against it. Use before and after
every audio operation you are unsure about.

Arguments: `path: str`; `target: str = ''`; `project: str = ''`; `out: str = ''`

### `audio_audacity`

Drive a running Audacity (free Audition replacement) through mod-script-pipe so the user can
watch/continue by hand. action: status (is Audacity reachable?) | open (import `path` into a new
project window) | run (send raw scripting `commands`, e.g. ["SelectAll:", "Normalize: PeakLevel=-1",
"Compressor: Threshold=-18 Ratio=3"]) | process (open `path`, run `commands` on all audio, export
to `export`, close the project). launch=true starts Audacity first if it is installed.
Scripting reference: https://manual.audacityteam.org/man/scripting_reference.html.
If the pipe is missing, the result explains how to enable mod-script-pipe (one-time setting).

Arguments: `action: str = 'status'`; `path: str = ''`; `commands: list[str] = []`; `export: str = ''`; `launch: bool = False`; `timeout: float = 120.0`

### `audio_clean`

'Studio voice' clean-up of a spoken recording (audio or the audio of a video): high-pass,
noise reduction, EQ (mud cut, presence, air), de-ess, expander (pushes down room tone and
reverb tails between words), compression and loudness normalisation. Returns the cleaned file,
a before/after waveform+spectrogram PNG, and measured loudness.

preset: podcast (natural, -16 LUFS) | reel (punchy, -14 LUFS) | phone (rescue a phone/laptop
recording: stronger denoise, band-limited, -16) | light (minimal) | music (just HP + loudness).
denoise: override strength 0..1 (-1 = preset). declick: remove mouth clicks/crackle.
target_lufs: override the loudness target (0 = preset). Honest limits: real de-reverberation of
speech needs ML (not free/offline here) — this reduces room tone between words, not echo on words;
heavy denoise (≥0.9) can sound watery.

Arguments: `path: str`; `preset: str = 'podcast'`; `denoise: float = -1.0`; `declick: bool = False`; `target_lufs: float = 0.0`; `format: str = 'wav'`; `project: str = ''`; `out: str = ''`

### `audio_convert`

Convert audio (or extract the audio of a video) to wav | mp3 | m4a | aac | flac | ogg | opus | aiff,
optionally changing sample rate (e.g. 48000 for video, 44100 for music) and channels (1/2).
bitrate like '192k' (defaults: mp3/m4a 192k, opus 128k). Returns the new file, measured.

Arguments: `path: str`; `format: str = 'mp3'`; `sample_rate: int = 0`; `channels: int = 0`; `bitrate: str = ''`; `project: str = ''`; `out: str = ''`

### `audio_join`

Join audio files in order into one file, with an optional equal-power crossfade (seconds) or a
silent gap between them. Returns the joined file and data.offsets (start time of each input in the
result — useful for chapters/captions).

Arguments: `paths: list[str]`; `crossfade: float = 0.0`; `gap: float = 0.0`; `format: str = 'wav'`; `project: str = ''`; `out: str = ''`

### `audio_library_search` [N]

Search FREE-licensed recorded music and sound effects and optionally download the top results
with an attribution/licence file. kind: any | music | sfx. source: auto (Freesound if a key is set,
plus Openverse) | openverse (no key; aggregates Freesound, Jamendo, Wikimedia… CC-licensed) |
freesound (needs a free API key in FREESOUND_API_KEY or STUDIO_HOME/keys.json). commercial=true
keeps only licences that allow commercial use (CC0 / CC BY — attribution still required for BY).
download=N saves the first N (Freesound gives its HQ MP3 preview without OAuth; originals need
OAuth login). Pixabay Music/SFX has NO public audio API, so it cannot be searched here — the user
can browse pixabay.com/music by hand. Returns data.results with licence + attribution for each.

Arguments: `query: str`; `kind: str = 'any'`; `source: str = 'auto'`; `commercial: bool = True`; `limit: int = 10`; `download: int = 0`; `min_duration: float = 0.0`; `max_duration: float = 0.0`; `project: str = ''`; `out: str = ''`

### `audio_master`

Master/normalise a finished mix or voice to a loudness target with a true-peak ceiling, and
report the MEASURED result. target: streaming/youtube/reels (-14 LUFS) | podcast/apple/voiceover
(-16) | broadcast/ebu (-23) | atsc (-24) | or a number like '-18'. true_peak: ceiling in dBTP
(-1 default; -2 for lossy delivery safety). glue: gentle 1.5:1 bus compression before limiting.
Returns the mastered file + preview; data.metrics has lufs/true_peak as measured by ffmpeg ebur128.

Arguments: `path: str`; `target: str = 'streaming'`; `true_peak: float = -1.0`; `glue: bool = True`; `format: str = 'wav'`; `project: str = ''`; `out: str = ''`

### `audio_mix`

Mix a voice (voiceover/podcast) over a music bed with automatic ducking: the music dips by
duck_db whenever the voice speaks and swells back in the gaps, with a music-only intro/outro,
fades, looping of short music (crossfaded) and final mastering to `target` (-14 streaming default).
music_level_db: music loudness UNDER the voice relative to the voice (-18 ≈ clear speech; -12 more
music). attack/release: ducking speed in seconds. Returns the mix, a stem-annotated preview and
measured loudness; data.duck_regions lists when the music is ducked.

Arguments: `voice: str`; `music: str`; `duck_db: float = 10.0`; `music_level_db: float = -18.0`; `intro: float = 2.0`; `outro: float = 3.0`; `fade_in: float = 1.5`; `fade_out: float = 3.0`; `loop_music: bool = True`; `attack: float = 0.12`; `release: float = 0.6`; `target: str = 'streaming'`; `format: str = 'wav'`; `project: str = ''`; `out: str = ''`

### `audio_music`

Generate an original, royalty-free music bed offline (no AI model, no internet): WAV + editable
multi-track MIDI. genre: lofi (jazzy 7th chords, swung boom-bap, vinyl) | cinematic (strings, piano
ostinato, build → climax → resolve, trailer booms) | corporate (bright plucks, claps, bell hook,
I–V–vi–IV) | oriental (Arabic maqam melody on a plucked oud, qanun tremolos, ney, tonic drone and
darbuka/riq). maqam: hijaz | hijazkar | kurd | nahawand | bayati | rast | saba | nikriz (bayati/rast/
saba use exact quarter tones). rhythm (oriental): maqsum | baladi | saidi | malfuf. key e.g. 'D'
(oriental: tonic, default D), bpm 0 = genre default, seed = variation (same seed → same piece).
Ends musically (± a bar); fit=true fades out at exactly `duration`. Honest level: tasteful synthetic
demo/library quality — good for reels/explainers under a voice, not a substitute for a composer.

Arguments: `genre: str = 'lofi'`; `duration: float = 60.0`; `bpm: float = 0.0`; `key: str = ''`; `maqam: str = 'hijaz'`; `rhythm: str = 'maqsum'`; `seed: int = 0`; `loudness: float = -14.0`; `fit: bool = False`; `project: str = ''`; `out: str = ''`

### `audio_separate_stems`

Split a song or mix into stems: vocals + accompaniment (stems='two', default) or vocals, drums,
bass, other (stems='four'). Use to remove music under speech, make karaoke/instrumental beds, or
rescue dialogue. method: auto (Demucs if installed) | demucs (Meta's htdemucs — near
commercial quality; CPU ≈ 0.5–1.5x realtime, ~80 MB model on first use) | center (no install, stereo
only, crude: works for centre-panned vocals, leaks bass/kick). Returns one file per stem + a preview.

Arguments: `path: str`; `method: str = 'auto'`; `stems: str = 'two'`; `model: str = 'htdemucs'`; `format: str = 'wav'`; `project: str = ''`; `out: str = ''`

### `audio_sfx`

Generate a sound effect offline (original, royalty-free): whoosh | riser | downlifter | impact |
pop | click | ding | success | error | glitch | typing | tick | shutter. duration 0 = natural
length (risers/typing/ticks stretch to any duration). variations=N renders N takes with different
seeds (pick by ear). Returns WAV file(s) + preview. For recorded/realistic effects (rain, door,
crowd…) use audio_library_search (Freesound/Openverse).

Arguments: `kind: str = 'whoosh'`; `duration: float = 0.0`; `variations: int = 1`; `seed: int = 0`; `loudness: float = -16.0`; `project: str = ''`; `out: str = ''`

### `audio_transcribe`

Transcribe speech (audio OR video file) to text with word-level timestamps: SRT + VTT + TXT +
JSON (segments, words, per-word probability). Use for captions, subtitles, transcripts, finding
cut points. Returns files and data {srt, vtt, txt, json, language, words:[{word,start,end,probability}],
confidence, flagged_segments}. Output is Whisper's text verbatim — NOTHING is guessed or 'repaired';
uncertain words/segments are flagged for human review instead.

language: 'auto' | 'ar' | 'en' | any Whisper code. model: 'auto' (best cached: large-v3) |
large-v3 | large-v3-turbo | medium | small | base | base.en … ; speed='fast' prefers lighter models
(base.en for English). dialect='egyptian' biases spelling toward Egyptian colloquial (prompt only;
it never changes words that were not said). prompt: domain context; hotwords: names/terms to favour.
max_chars_per_line 42 (use 40 for Arabic reels), max_lines 2. engine: auto | faster-whisper | mlx
(mlx-whisper on Apple Silicon, much faster there). allow_download: permit fetching a missing model.

Arguments: `path: str`; `language: str = 'auto'`; `model: str = 'auto'`; `speed: str = 'accurate'`; `formats: list[str] = ['srt', 'vtt', 'txt', 'json']`; `max_chars_per_line: int = 42`; `max_lines: int = 2`; `dialect: str = ''`; `prompt: str = ''`; `hotwords: str = ''`; `vad: bool = True`; `engine: str = 'auto'`; `allow_download: bool = False`; `project: str = ''`; `out: str = ''`

### `audio_transcribe_models`

List Whisper models for audio_transcribe: which are already downloaded (cached), their size,
and the speed/accuracy trade-off, plus whether the fast Apple-Silicon engine (mlx-whisper) is
available. Use before choosing `model=` or before asking the user to allow a download.

Arguments: 

### `audio_trim_silence`

Tighten a recording: shortens every pause longer than max_pause seconds down to max_pause
(jump-cut style, with 15 ms crossfades so there are no clicks) and trims leading/trailing silence
to keep_edges seconds. threshold_db is relative to the loudest part (-42 default; raise to -35 for
noisy rooms). Returns the tightened file and data.cuts [{start,end}] in ORIGINAL time plus an
edit list mapping — use it to cut matching video.

Arguments: `path: str`; `max_pause: float = 0.45`; `threshold_db: float = -42.0`; `keep_edges: float = 0.15`; `format: str = 'wav'`; `project: str = ''`; `out: str = ''`

### `audio_voiceover` [N]

Text → natural voiceover (Egyptian/Saudi/Gulf Arabic, many English accents) with captions
aligned to the voice. Long scripts are chunked by sentence/paragraph, synthesised, stitched with
natural pauses and loudness-normalised. Returns the audio (WAV 48 kHz by default), an SRT and a
words JSON (data: audio, srt, json, words, duration, voice, lufs).

voice: 'auto' (Egyptian female for Arabic text, US multilingual female for English), an Edge
voice id (ar-EG-SalmaNeural, ar-EG-ShakirNeural, ar-SA-HamedNeural, en-US-AndrewMultilingualNeural…),
an alias (egyptian-female, egyptian-male, saudi-male, british-female, narrator-male…) or a Piper
voice (ar_JO-kareem-medium, en_US-lessac-medium). rate '-10%'..'+30%', pitch '-5Hz'..'+5Hz'.
engine: auto (edge online, Piper offline fallback) | edge | piper. pause_ms: silence between
paragraphs. loudness: LUFS target (-16 voiceover/podcast, -14 reels; 0 = leave as is).
Tip: write numbers/abbreviations the way they should be SAID (Egyptian: 'تلاتين' not '30').

Arguments: `text: str = ''`; `script_path: str = ''`; `voice: str = 'auto'`; `rate: str = '+0%'`; `pitch: str = '+0Hz'`; `volume: str = '+0%'`; `engine: str = 'auto'`; `pause_ms: int = 350`; `loudness: float = -16.0`; `format: str = 'wav'`; `max_chars_per_line: int = 42`; `allow_download: bool = False`; `project: str = ''`; `out: str = ''`

### `audio_voices` [N]

Voice catalogue for audio_voiceover: lists Edge neural voices (online, free) and/or Piper voices
(offline) for a language ('ar', 'ar-EG', 'en', 'en-GB', 'all'), with gender, accent and personality.
samples=N renders the first N voices reading sample_text and one 'audition' file with all of them
back to back (a 1 s beep between voices, in list order) so the user can pick by ear.
Returns data.voices [{id, gender, locale, engine, sample}].

Arguments: `language: str = 'ar'`; `gender: str = ''`; `engine: str = 'edge'`; `samples: int = 0`; `sample_text: str = ''`; `project: str = ''`; `out: str = ''`

## ai (14)

### `ai_backends` [N]

Which AI backends are usable right now, what the automatic router will pick for each task (and why), installed
models with licences, and honest speed expectations on a 16 GB Apple-Silicon Mac. Start here before generating.

Arguments: `check_network: bool = True`

### `ai_edit_image`

Edit an existing image with AI (local, free). mode:
'img2img' — restyle/re-imagine the whole picture (strength 0.2 subtle … 0.8 heavy; default 0.6);
'inpaint' — repaint only the WHITE area of `mask` (PNG) or of `mask_box` [x, y, w, h] in image pixels, e.g. remove
an object or change a garment (default strength 0.9; untouched pixels are copied back exactly);
'outpaint' — extend the canvas: expand_to='9:16'/'16:9'/'story'… or expand_px [left, top, right, bottom]; the
original pixels are kept at full resolution and only the new border is generated.
Needs ComfyUI (comfyui_setup/comfyui_start); img2img can also run on mflux on the Mac. Prompt describes the
RESULT (for inpaint: what should appear in the masked area). Returns the edited PNG + sidecar JSON + a
before/after (and mask) preview sheet.

Arguments: `image: str`; `prompt: str`; `mode: str = 'img2img'`; `mask: str = ''`; `mask_box: list[int] = []`; `strength: float = -1.0`; `expand_to: str = ''`; `expand_px: list[int] = []`; `negative: str = ''`; `style: str = 'none'`; `seed: int = -1`; `backend: str = 'auto'`; `model: str = ''`; `project: str = ''`; `out: str = ''`

### `ai_generate_image` [N]

Generate images from an English prompt with the best FREE backend available, and say which one ran.
Router (backend='auto'): mflux on an Apple-Silicon Mac (fastest local) → ComfyUI if running with a model
(FLUX-schnell GGUF / SDXL-Lightning) → Hugging Face free tier if HF_TOKEN is set → Pollinations (free, no key,
draft quality + small watermark). size: preset (1:1, 4:5/1080x1350, 9:16/story, 16:9, youtube-thumbnail, og, a4…)
or 'WxH'; output is exactly that size (generated at the model's native ~1 MP, then cover-cropped).
count ≤ 8 (seeds seed, seed+1…). style/brand_colors shape the prompt (see ai_prompt_enhance); enhance=false sends
your prompt verbatim. model: ComfyUI bundle id (flux-schnell-q4, sdxl-lightning…), mflux id (schnell-q4,
z-image-turbo) or HF repo. Returns PNGs (prompt/seed embedded) + sidecar JSON each (prompt, seed, backend, model,
licence) + a labelled contact sheet to LOOK at. Paid providers are never used here (see ai_generate_image_byok).

Arguments: `prompt: str`; `negative: str = ''`; `size: str = '1:1'`; `count: int = 1`; `seed: int = -1`; `style: str = 'none'`; `brand_colors: list[str] = []`; `backend: str = 'auto'`; `model: str = ''`; `steps: int = 0`; `enhance: bool = True`; `no_text: bool = False`; `project: str = ''`; `out: str = ''`

### `ai_generate_image_byok` [N$]

PAID, optional: generate with the user's OWN key at fal (FAL_KEY), Replicate (REPLICATE_API_TOKEN) or OpenAI
(OPENAI_API_KEY). Only when the user explicitly wants a paid provider. confirm=false returns the price estimate
and does nothing; call again with confirm=true after the user agrees. Same outputs as ai_generate_image. · SPENDS: may use paid credits/quota — only with the user's explicit OK

Arguments: `prompt: str`; `provider: str = 'fal'`; `size: str = '1:1'`; `count: int = 1`; `seed: int = -1`; `style: str = 'none'`; `brand_colors: list[str] = []`; `model: str = ''`; `confirm: bool = False`; `project: str = ''`; `out: str = ''`

### `ai_generate_video`

Text→video or image→video (`image` = first frame). Routing:
• cinematic video with characters, dialogue, speech, Arabic lines, storytelling or sound → HAND-OFF to the
flow-studio-director skill (Google Flow, Veo 3.1): returns a ready brief, generates nothing here;
• silent b-roll, loops, product/atmosphere shots → local ComfyUI, free: LTX-Video 2B distilled (fastest,
≈3–10 min per 4 s on a 16 GB Mac), Wan 2.1 1.3B (t2v) or Wan 2.2 5B GGUF (best, slow; quality='standard').
route: auto | comfyui | flow. model: ltxv-2b | wan21-1.3b | wan22-5b-q4. Local output: H.264 MP4 at the model's
native size (same aspect as `size`), poster frame, sidecar JSON and a contact sheet to LOOK at. Long renders:
wait=false (or a timeout) returns a prompt_id — fetch later with comfyui_collect.

Arguments: `prompt: str`; `image: str = ''`; `duration: float = 4.0`; `size: str = '16:9'`; `route: str = 'auto'`; `model: str = ''`; `seed: int = -1`; `quality: str = 'draft'`; `style: str = 'cinematic'`; `camera: str = ''`; `negative: str = ''`; `audio: str = ''`; `dialogue: str = ''`; `wait: bool = True`; `timeout_min: int = 60`; `project: str = ''`; `out: str = ''`

### `ai_prompt_enhance`

Turn a short English idea into a strong, model-specific prompt (deterministic templates, no LLM).
target: flux | sdxl | pollinations | hf | mflux (images), ltxv | wan (local video), veo (Google Flow brief with
camera + AUDIO/dialogue). style: one of the studio presets (photoreal, cinematic, product, editorial, food,
flat-vector, 3d-render, poster, social-ad, islamic-geometric, egyptian-heritage …). brand_colors: hex or names
(hex is translated to colour words models understand). Returns prompt + negative + notes in data.
Arabic ideas: there is no offline translator — YOU (the agent) should write the idea in English; keep Arabic copy
for text overlays done by the design tools.

Arguments: `idea: str`; `target: str = 'flux'`; `style: str = 'none'`; `brand_colors: list[str] = []`; `size: str = '1:1'`; `negative: str = ''`; `camera: str = ''`; `audio: str = ''`; `dialogue: str = ''`; `duration: float = 4.0`; `no_text: bool = False`

### `ai_upscale`

Enlarge an image with an AI upscaler that invents plausible fine detail (2×–4×; up to 8× with a final resample).
Router: ComfyUI + Real-ESRGAN x4plus (BSD, commercial OK; or model='ultrasharp-4x' — crisper but NON-commercial)
→ mflux SeedVR2 on the Mac → plain Lanczos + unsharp as a clearly-labelled non-AI fallback.
Returns the upscaled PNG + sidecar JSON + a 100%-crop detail comparison to LOOK at.

Arguments: `image: str`; `scale: float = 2.0`; `model: str = ''`; `backend: str = 'auto'`; `project: str = ''`; `out: str = ''`

### `comfyui_collect`

Fetch the result of a long ComfyUI job started with wait=false or that timed out (ai_generate_video,
comfyui_run_workflow): waits for it, downloads, assembles video, writes sidecar + previews.

Arguments: `prompt_id: str`; `wait: bool = True`; `timeout_min: int = 60`

### `comfyui_run_workflow`

Run ANY ComfyUI workflow: a file exported with ComfyUI's 'Save (API)' or a studio template name (t2i, i2i,
inpaint, outpaint, upscale, video_ltxv_t2v, …). String values written as "$name" are replaced from `params`
(typed: numbers stay numbers); params named image/mask/start_image that are local file paths are uploaded
automatically. The workflow is validated against the live server first (missing nodes/models are named).
Returns every output image/video downloaded + a preview sheet.

Arguments: `workflow: str`; `params: dict = {}`; `wait: bool = True`; `timeout_min: int = 30`; `project: str = ''`; `out: str = ''`

### `comfyui_setup` [NI]

Install ComfyUI (free, local AI image/video server) into STUDIO_HOME/apps/ComfyUI with its own Python
environment (PyTorch with Apple Metal on the Mac), the needed custom nodes (ComfyUI-GGUF), and download the chosen
models from Hugging Face into STUDIO_HOME/models/comfyui (on the external SSD). models: any of
flux-schnell-q4 (10.8 GB, default), flux-schnell-q5, sdxl-lightning (6.9 GB), sdxl-turbo, realesrgan-x4 (67 MB),
ultrasharp-4x (non-commercial), ltxv-2b (video, 9.7 GB), wan21-1.3b, wan22-5b-q4 — shared files download once.
confirm=false (default) only returns the plan with sizes and LICENCES — show it to the user first. confirm=true
runs it in the background (resumable downloads); watch with comfyui_status. FLUX-dev is deliberately not offered
(non-commercial licence) — schnell is Apache-2.0. · INSTALLS software — only with the user's explicit OK

Arguments: `models: list[str] = ['flux-schnell-q4', 'realesrgan-x4']`; `custom_nodes: list[str] = []`; `confirm: bool = False`; `update: bool = False`; `background: bool = True`

### `comfyui_start`

Start the local ComfyUI server installed by comfyui_setup (background process, logs in STUDIO_HOME/logs).
lowvram=true trades speed for memory — use it on a 16 GB Mac for video or when you see out-of-memory errors.
Returns the URL; does nothing if it is already running.

Arguments: `port: int = 8188`; `lowvram: bool = False`; `wait_s: int = 90`

### `comfyui_status`

ComfyUI health: installed?, running (URL, device, memory, queue)?, which studio model bundles are present,
and the progress of a running comfyui_setup/mflux_setup download.

Arguments: 

### `comfyui_stop`

Stop the ComfyUI server the studio started (frees all its memory). free_only=true keeps it running but unloads
models from RAM — handy on a 16 GB Mac before switching to video/other apps.

Arguments: `free_only: bool = False`

### `mflux_setup` [NI]

Apple-Silicon only: install mflux (MLX-native FLUX, the fastest local image generator on a Mac) into the studio's
Python and pre-download a model into STUDIO_HOME/models/hf. model: schnell-q4 (≈9.6 GB, pre-quantised 4-bit,
Apache-2.0, default), schnell-q8 (≈13 GB), z-image-turbo (≈20 GB download, quantised to 4-bit at load, Apache-2.0,
excellent photorealism). confirm=false returns the plan and sizes only. · INSTALLS software — only with the user's explicit OK

Arguments: `model: str = 'schnell-q4'`; `confirm: bool = False`; `background: bool = True`
