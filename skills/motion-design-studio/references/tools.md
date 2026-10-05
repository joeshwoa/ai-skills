# motion-design-studio — tool reference

Generated from studio-mcp (`call.sh help <tool>` shows the same). Flags: **N** internet · **$** may spend (needs OK) · **I** installs (needs OK).

## motion (18)

### `motion_3d` [N]

Real-time 3D motion graphics (three.js/WebGL, studio lighting with HDR-style reflections, soft
shadows, ACES tone mapping) rendered frame-exactly: 3D extruded titles, 3D logos, product
turntables, device mockups, particle fields and abstract loops. Fast (seconds per second of video
at 1080p) — use motion_blender instead for photoreal glass/caustics/real depth of field. Returns
MP4 (or alpha MOV/WebM), a timecoded contact sheet and key frames.

preset: title (text — any language: shaped with HarfBuzz so Arabic joins correctly, then extruded)
| logo (an SVG, or brand=<slug>'s logo, extruded + bevelled) | product (model=<.glb> turntable on a
shadow catcher) | device (phone|laptop mockup; screen=<image or video> plays on the display) |
particles (depth field of glowing points flying toward the camera) | abstract (glossy glass/chrome
shapes orbiting). material: plastic | metal | chrome | gold | glass | matte | clay | neon | satin.
camera: orbit | push-in | dolly | crane | static | turntable. animation: rise | spin-in | flip |
drop | zoom-through | turntable | float. depth: extrusion (world units, ~0.35 default).
background: CSS colour/gradient ('' = brand-tinted studio gradient); transparent=true for alpha.
bloom 0–1.5 = glow on bright parts (opaque only). motion_blur=6 → sub-frame motion blur.
options = extra scene settings (fov, orbit_degrees, exposure, count, side_color, …).

Arguments: `preset: str = 'title'`; `text: str = ''`; `logo: str = ''`; `model: str = ''`; `screen: str = ''`; `device: str = 'phone'`; `material: str = ''`; `camera: str = ''`; `animation: str = ''`; `duration: float = 5.0`; `size: str = '1920x1080'`; `fps: int = 30`; `transparent: bool = False`; `background: str = ''`; `color: str = ''`; `accent: str = ''`; `depth: float = 0`; `bloom: float = 0`; `motion_blur: int = 0`; `font: str = ''`; `weight: int = 800`; `brand: str = ''`; `options: dict = {}`; `formats: list[str] = []`; `project: str = ''`; `out: str = ''`

### `motion_blender` [N]

Physically based 3D motion graphics in Blender (headless): 3D title (any language — text is
shaped with HarfBuzz into outlines first, so Arabic joins correctly), 3D logo from SVG, product
turntable from a .glb, abstract glass/chrome loop — on a curved studio cyclorama with area lights,
real depth of field and motion blur. Returns the video, a timecoded contact sheet + key frames AND
the editable .blend master. Slow (minutes); for fast real-time 3D use motion_3d (three.js).

engine_name: EEVEE (fast raster, good for most titles) | CYCLES (path traced: glass, caustics,
soft GI — slowest). quality: draft (½ res, 16 samples) | preview (¾ res, 32) | final (full, 128).
material: metal | chrome | gold | glass | plastic | matte | clay | neon | satin. camera: push-in |
orbit | dolly | static. animation: rise | spin-in | flip | turntable. transparent=true → alpha
(shadow catcher in Cycles). If Blender is not installed and fallback=true, the same preset is
rendered with three.js instead and the result says FALLBACK clearly (no .blend then).

Arguments: `preset: str = 'title'`; `text: str = ''`; `logo: str = ''`; `model: str = ''`; `material: str = ''`; `engine_name: str = 'EEVEE'`; `quality: str = 'preview'`; `camera: str = ''`; `animation: str = ''`; `duration: float = 4.0`; `size: str = '1920x1080'`; `fps: int = 30`; `transparent: bool = False`; `dof: bool = True`; `motion_blur: bool = True`; `color: str = ''`; `accent: str = ''`; `background: str = ''`; `depth: float = 0.35`; `font: str = ''`; `weight: int = 800`; `brand: str = ''`; `fallback: bool = True`; `timeout: int = 3600`; `formats: list[str] = []`; `project: str = ''`; `out: str = ''`

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

### `motion_compose`

The pro motion-graphics engine (After Effects-style comp → video): write a JSON scene spec (or
pick a ready template) and get a frame-exact MP4 / ProRes 4444 / WebM-alpha, a timecoded contact
sheet + key frames to LOOK at, the standalone GSAP HTML and the spec JSON (editable masters).

spec = {size, fps, background, colors, post:{grain, vignette, light_leaks, letterbox, glow, chroma,
motion_blur}, camera, markers:{name: s}, scenes:[{duration, background, camera, transition:{type,
duration}, layers:[…]}]} (or top-level layers for one scene). Layer: {type: text|shape|image|video|
svg|lottie|icon|chart|counter|3d|group, id, x, y (or below|above: '<id of an earlier layer>' + gap — stacks on the
MEASURED height, so wrapped/Arabic headlines never collide with the line under them), anchor, w, h, scale, rotation, opacity, z, blend, in,
out, enter, exit, animate:[{preset, at, duration, ease, stagger, …}], keyframes:[{t,x,y,scale,
rotation,opacity,ease}], tweens:[raw GSAP]} + type props (text: text with *emphasis*, font head|
body|<Google family>, weight, size, color, align, rtl auto, bg, glow, shadow, stroke; shape: shape
rect|circle|ring|line|star|polygon|heart|triangle|arrow|path, fill (colour or gradient), radius;
image/video: src, fit, radius; svg: src or svg markup ('brand:logo'); lottie: src .json/.lottie,
speed, loop, recolor; chart: chart bar|hbar|line|area|pie|donut, data [{label,value}]; 3d: scene
{preset title|logo|product|particles|abstract|device, …}). Colours accept brand tokens (primary,
accent, background, text, muted). Presets: fade slide rise drop scale zoom pop blur elastic bounce
flip spin swing wipe iris block split-chars/words/lines (style rise|fade|pop|blur|rotate|punch)
typewriter scramble highlight underline shine glitch draw morph motion-path counter + loops wiggle
float parallax pulse kenburns shake; any preset takes -out for exits. Transitions: crossfade dip
wipe slide push zoom blur iris whip shape glitch. Arabic text is shaped by Chromium and never split
into letters. template=<name> + fields={…} builds a ready spec (see motion_templates);
preview=true renders 12 stills only (fast iteration). motion_blur=8 → real sub-frame motion blur
(8× render time). Full reference: docs/motion.md.

Arguments: `spec: dict = {}`; `template: str = ''`; `fields: dict = {}`; `size: str = ''`; `fps: int = 0`; `transparent: bool = False`; `brand: str = ''`; `colors: dict = {}`; `fonts: dict = {}`; `formats: list[str] = []`; `motion_blur: int = 0`; `preview: bool = False`; `project: str = ''`; `out: str = ''`

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

### `motion_lottie` [N]

Render a Lottie animation (.json Bodymovin or .lottie dotLottie, e.g. from LottieFiles or an
After Effects export) frame-exactly to MP4 / ProRes 4444 / WebM alpha / GIF, with optional brand
recolouring and retiming. Returns the video, a timecoded contact sheet, key frames, and data
(native fps/size/length, colours used, features such as expressions/effects that lottie-web may
not fully support).

size: '' = the animation's own size (capped at 1920) | 1080x1080 | 9:16 …; fit contain|cover.
speed: 0.5 = half speed; loops: play N times; duration (s) overrides the length (loops forever).
recolor_map {"#FF0000": "#00AA88", …} (nearest colour within tolerance) or recolor_mode brand
(uses brand=<slug> colours on the most used colours) | mono:#hex (every colour → a shade of #hex).
transparent=true → alpha (.mov + .webm); background: colour behind it otherwise (brand background
or white). fps: 0 = the animation's own fps. To use a Lottie as a LAYER in a bigger composition use
motion_compose with {"type": "lottie", "src": …}.

Arguments: `src: str`; `size: str = ''`; `fit: str = 'contain'`; `speed: float = 1.0`; `loops: int = 1`; `duration: float = 0`; `recolor_map: dict = {}`; `recolor_mode: str = ''`; `transparent: bool = False`; `background: str = ''`; `padding: int = 0`; `fps: int = 0`; `brand: str = ''`; `formats: list[str] = []`; `project: str = ''`; `out: str = ''`

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

### `motion_plan`

Router for motion graphics: describe the job in plain words (+ optional assets, size, duration,
needs_alpha, needs_3d, photoreal, arabic, brand) and get the best engine with the reasons, the
exact next tool call (args filled in), a ready spec skeleton/template, and the alternatives.
Engines: motion_compose (HTML+GSAP: 2D typography/infographics/UI/logo/transitions — default),
motion_lottie (designer .json/.lottie files), motion_3d (three.js real-time 3D), motion_blender
(photoreal Blender, slow), motion_remotion (existing React projects, licence-gated). Call this
first when unsure; it costs nothing and renders nothing.

Arguments: `brief: str`; `assets: list[str] = []`; `size: str = ''`; `duration: float = 0`; `needs_alpha: bool = False`; `needs_3d: bool = False`; `photoreal: bool = False`; `arabic: bool = False`; `brand: str = ''`

### `motion_remotion` [NI]

Render a composition of an EXISTING Remotion (React) project with `npx remotion render` — for
teams that already build videos in React or batch-render data-driven templates (pass input
props as props={…}). Returns the video + a contact sheet. For new motion graphics prefer
motion_compose (no Node, no licence question).

licence_ok=true is REQUIRED: confirm the user's organisation has ≤ 3 people or holds a Remotion
company licence (remotion.dev/docs/license). install=true runs `npm install` when node_modules is
missing (downloads packages). codec: h264 | h265 | vp9 | prores; transparent=true → ProRes 4444
(or VP9 with alpha when codec=vp9). frames: '0-89' to render a range. entry: the entry file if
Remotion cannot find it (e.g. src/index.ts). · INSTALLS software — only with the user's explicit OK

Arguments: `project_dir: str`; `composition: str`; `licence_ok: bool = False`; `install: bool = False`; `props: dict = {}`; `entry: str = ''`; `codec: str = 'h264'`; `transparent: bool = False`; `frames: str = ''`; `scale: float = 1.0`; `timeout: int = 3600`; `project: str = ''`; `out: str = ''`

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
