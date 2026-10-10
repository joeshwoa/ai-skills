# video-post-studio — tool reference

Generated from studio-mcp (`call.sh help <tool>` shows the same). Flags: **N** internet · **$** may spend (needs OK) · **I** installs (needs OK).

## video (34)

### `video_auto_color`

One-click colour correction (the 'balance' pass before a look): white balance from near-neutral
pixels (grey-world on low-saturation midtones, guarded by the brightest neutrals), exposure to a
healthy mid-grey, and contrast by setting black/white points (0.5 / 99.5 percentiles) — measured on
`samples` frames, written as a .cube LUT and applied with ffmpeg. strength 0–1. Returns the corrected
MP4 (apply=false: LUT only), the .cube, a before/after sheet and the measured gains in data. For a
look on top use video_grade (or a timeline grade) after this.

Arguments: `path: str`; `strength: float = 1.0`; `white_balance: bool = True`; `exposure: bool = True`; `contrast: bool = True`; `samples: int = 8`; `apply: bool = True`; `project: str = ''`; `out: str = ''`

### `video_auto_edit` N

Make a video from a brief — the whole edit planned and assembled automatically, then rendered AND
left fully editable. brief = {script: "text to voice" | voiceover: "vo.wav" | talking_head: "cam.mp4",
footage: ["a.mp4", …] | "folder", style: reel | ad | promo | youtube | documentary, size ("9:16"
default for reel/ad), duration (montage length without voice), music: "song.mp3" | "stock:<query>" |
"generate" (default) | "none", music_genre, broll: stock | footage | both, broll_queries: ["English
query per shot/sentence", …] (needed for Arabic scripts; stock APIs index English), topic: fallback
query, captions: style | false, voice (audio_voiceover id), brand, title: "hook" | {text, subtitle},
lower_thirds: [{name, role, at}], cta: "follow" | {kind, handle, text}, grade: preset, transitions:
cut | mixed | dissolve, language}. Pacing per style (reel 1.4–2.8 s shots cut on the beat … documentary
4–8 s), b-roll per phrase from own footage (shot detection + quality ranking + filename keywords) and/or
free stock in the right orientation (licences kept), music ducked under the voice. Writes the timeline
JSON (tweak + re-render with video_edit), MP4 + .kdenlive, EDIT-REPORT.md (shot list: time, words,
source, licence/attribution) and a storyboard sheet + QC table to LOOK at. render=false: plan only.

Arguments: `brief: dict | str`; `project: str = ''`; `out: str = ''`; `render: bool = True`

### `video_beats`

Tempo and beat/downbeat times of a song (or a video's soundtrack) for cutting to music. Returns
data {tempo (BPM), beats [s], downbeats [s] (bar starts, assuming `meter` beats per bar), confidence,
regularity, method}, a plot to LOOK at (waveform + blue beat lines + red downbeats), beats.json and an
Audacity label track (.txt). bpm_hint: nudge toward a known tempo (fixes half/double-time picks).
start/duration: analyse part of the file. method: auto (librosa if installed, else numpy spectral
flux + dynamic programming) | numpy | librosa. Use the beats with video_cut_to_beats or a timeline's
"cut_to_beats".

Arguments: `path: str`; `bpm_hint: float = 0.0`; `start: float = 0.0`; `duration: float = 0.0`; `meter: int = 4`; `method: str = 'auto'`; `project: str = ''`; `out: str = ''`

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

### `video_color_match`

Match a clip's colour to a reference (another camera, the hero shot, a still/frame grab you like):
Reinhard colour transfer in CIELAB — mean and spread of lightness and both colour axes — measured on
`samples` frames of each, baked into a 33³ .cube LUT (reuse it in Resolve/Premiere/Kdenlive or
video_grade lut=…) and applied with ffmpeg. reference: video or image; reference_time: use one frame of
a reference video (s). strength 0–1 blends toward the original. preserve_luminance: match colour only
(keep the clip's exposure/contrast). Returns the graded MP4 (apply=false: LUT only), the .cube and a
before | after | reference sheet to LOOK at, with measured LAB distances in data.

Arguments: `path: str`; `reference: str`; `strength: float = 1.0`; `reference_time: float = -1.0`; `samples: int = 8`; `preserve_luminance: bool = False`; `apply: bool = True`; `project: str = ''`; `out: str = ''`

### `video_concat`

Join clips in order into one video (any mix of sizes/fps/codecs — they are conformed to `size`/
`fps`, default the first clip's). transition between every pair: cut | dissolve | dip | dip_white |
wipe_left | slide_left | zoom | iris … (transition_duration seconds, audio crossfades under it).
fit: auto | cover | contain | blur (for clips of another aspect ratio). Also writes a .kdenlive.

Arguments: `paths: list[str]`; `transition: str = 'cut'`; `transition_duration: float = 0.5`; `size: str = ''`; `fps: float = 0`; `fit: str = 'auto'`; `project: str = ''`; `out: str = ''`

### `video_cut_to_beats`

Cut a montage to music: each clip lasts `every` beats (1 = every beat, 2, 4 = every bar; or a
pattern like [4,2,2] that repeats) so every cut lands exactly on a beat; the song starts on its first
downbeat (align: downbeat | beat | start). clips: paths or timeline clip dicts ({"src","in"} — "out"/
"duration" are replaced; images get Ken Burns). Clips too short for their span take fewer beats.
transition: cut (default) or dissolve/zoom/… (starts on the beat). max_duration: stop after N s.
Renders MP4 + .kdenlive; data.cut_to_beats lists every cut time; also writes the timeline JSON.

Arguments: `clips: list`; `music: str`; `every: int | list = 2`; `align: str = 'downbeat'`; `size: str = ''`; `transition: str = 'cut'`; `max_duration: float = 0.0`; `music_volume_db: float = 0.0`; `grade: str = ''`; `captions: bool = False`; `project: str = ''`; `out: str = ''`

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

projects: the same edit as EDITABLE projects in one portable folder "<name> — Project/" next to the
MP4 — all (default) | none | comma list of premiere, aftereffects, resolve, fcpx, capcut, avid, kdenlive,
otio, edl. Graphics are rebuilt as live text/shape layers, captions as live text, grades as .cube LUTs,
plus stems, fonts and OPEN-IN.md. project_media: copy (default, hard-links on the same disk) |
reference. host_map: "local_prefix=host_prefix" when the studio runs in a VM/container and the apps
see the files elsewhere (e.g. "/sessions/x/mnt/SSD=/Volumes/PortableSSD"). mogrts: the After Effects
builder also exports each graphic as a .mogrt for Premiere.

Arguments: `timeline: dict | str`; `brand: str = ''`; `kdenlive: bool = True`; `project: str = ''`; `out: str = ''`; `name: str = 'edit'`; `projects: str = 'all'`; `project_media: str = 'copy'`; `host_map: str = ''`; `mogrts: bool = False`

### `video_export`

Deliver a finished video to a platform spec: reels | tiktok | shorts (1080x1920) | youtube
(1080p) | youtube_4k | linkedin | linkedin_square | instagram_feed (1080x1350) | x | whatsapp |
prores (ProRes 422 HQ master .mov) | prores4444 | gif | webm | master. Sets size, fps, H.264
high profile + bitrate cap, AAC 48 kHz, faststart, and masters loudness to the platform target
(-14 LUFS, true peak -1). fit when the aspect ratio differs: auto (smart face-tracking reframe) |
track | blur | pad | crop. Warns about platform length limits (trim_to_limit=true cuts to fit).

Arguments: `path: str`; `preset: str = 'youtube'`; `fit: str = 'auto'`; `loudness: bool = True`; `trim_to_limit: bool = False`; `project: str = ''`; `out: str = ''`

### `video_export_interchange`

Export a video_edit timeline (dict / JSON / .json path — e.g. the one video_auto_edit or
video_transcript_edit wrote) for a professional NLE: format fcpxml (Final Cut Pro 10.5+, DaVinci
Resolve: File › Import › Timeline), otio (OpenTimelineIO — Resolve 18+, Kdenlive 23+, Premiere/Avid
via OTIO adapters), edl (CMX3600 — Premiere: File › Import; Resolve: Import Timeline; V1 + its audio)
or all. Each file is re-read and checked (time math, every media path exists; opentimelineio strict
load when installed). Carries cuts, dissolves, speed, overlays on V2+, music on A2+; not grades,
position/scale, captions (import the .srt) or ducking. Returns the files + a track-layout preview.

Arguments: `timeline: dict | str`; `format: str = 'all'`; `name: str = 'edit'`; `project: str = ''`; `out: str = ''`

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

### `video_project_apps`

Which professional editing/motion apps are installed on this Mac (Premiere, After Effects, Final Cut,
Resolve free/Studio, CapCut, Kdenlive, Shotcut) — so the AI knows which projects it can open for you.

Arguments: 

### `video_project_open`

Open a project package (the '<name> — Project' folder video_edit writes) in one app on this Mac and
build the native project there:
  premiere      opens Premiere with the edit's XML (all tracks, transitions, motion, levels) — save as .prproj
  aftereffects  runs Projects/AfterEffects/build_project.jsx inside After Effects → saves the native .aep
                (needs AE › Settings › Scripting & Expressions › 'Allow Scripts to Write Files')
  fcpx          imports the FCPXML into Final Cut Pro (library + project)
  resolve       Resolve Studio: runs build_resolve.py (timeline, LUTs, subtitles); free: opens Resolve and the guide
  capcut        adds the draft to CapCut's project list (CapCut must be closed) and opens CapCut
  kdenlive | shotcut  opens the .kdenlive / .mlt
Nothing in the user's existing projects is changed.

Arguments: `package: str`; `app: str`; `save: bool = True`

### `video_project_relink`

After moving a project package (another disk, another Mac): rewrite the media and font paths inside
every project file to the folder's new location.

Arguments: `package: str`

### `video_qc`

Delivery QC report before a video goes out — a PASS/WARN/FAIL table image (LOOK at it) + data.checks:
black frames, frozen/static picture, flash/strobe risk (luminance flashes per second, whole frame and
quadrants, vs the 3-per-second ITU-R BT.1702/WCAG limit), letterbox/pillarbox bars, audio clipping,
loudness (integrated LUFS, LRA, true peak vs the platform target), silence gaps, A/V stream alignment
(start/duration sanity — not lip-sync), resolution / fps / codec / pixel format / faststart vs the
platform, caption safe zone (renders the .ass beside the file, or captions=<.ass>, and checks text stays
out of the platform UI zones), duration and file-size limits. platform: reels | tiktok | shorts |
youtube | linkedin | instagram_feed | x | whatsapp | broadcast | '' (generic). Also a timeline strip
marking where each problem is.

Arguments: `path: str`; `platform: str = ''`; `captions: str = ''`; `project: str = ''`; `out: str = ''`

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

### `video_scene_detect`

Find the shots in a video (cut detection) and measure each one — the assistant-editor pass before
cutting. Returns a labelled shot-list contact sheet (LOOK at it: shot number, in/out timecodes,
duration, flags SOFT / SHAKY / EXPOSURE, FACE badge) and data.shots [{n, start, end, duration, thumb,
motion (0–100 frame difference), shake (% of frame width of hand-held jitter), camera_move, sharpness
(Laplacian variance at 640 px: <40 soft, >150 crisp), blurry, brightness/contrast/clip_low/clip_high,
has_face/faces (OpenCV when installed), audio_db/audio_peak_db}].

threshold: scene-change sensitivity 0.15 (catches soft cuts, more false hits) … 0.3 (default) … 0.5
(only hard cuts). min_scene: shortest shot in seconds (suppresses flashes). method: auto (ffmpeg-style
scene score in numpy) | pyscenedetect (if installed). Dissolves/fades may be missed — lower threshold.
Feed shots to video_edit clips ({"src", "in": start, "out": end}) or to video_select_takes.

Arguments: `path: str`; `threshold: float = 0.3`; `min_scene: float = 0.6`; `method: str = 'auto'`; `analysis_fps: float = 0.0`; `thumbs: bool = True`; `project: str = ''`; `out: str = ''`

### `video_select_takes`

Pick the good footage from a pile: analyse every clip (or every shot inside each clip when
per_shot=true) for sharpness, stability (hand-held jitter), exposure, faces, audio level and motion,
rank them and return the top `count` with reasons — plus a ranked contact sheet to LOOK at and
ready-to-paste timeline clips ({"src","in","out"}) in data.picks.

paths: video files, and/or folder: every video in it. want: best | sharp | stable | faces | talking
(faces + clean audio) | audio | action (more motion) | calm (less motion) | broll (sharp, steady, no
faces needed). min_duration: shots shorter than this score low. data.ranked has every unit.

Arguments: `paths: list[str] = []`; `folder: str = ''`; `want: str = 'best'`; `count: int = 6`; `per_shot: bool = True`; `min_duration: float = 1.0`; `threshold: float = 0.3`; `project: str = ''`; `out: str = ''`

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

### `video_transcript`

Readable, INDEXED transcript of a video/audio for text-based editing: one sentence per line with
its timecode and word-index range ([00:12.30 | w45–w61] …), pauses ≥ 0.6 s shown as ⏸, likely fillers
in {braces}. Writes .md (read it) + .json (words with index/start/end — pass it as transcript= to
video_transcript_edit so Whisper does not run twice). verbatim=true prompts Whisper to keep
um/uh/يعني (it tends to drop them). language: auto | en | ar | egyptian.

Arguments: `path: str`; `language: str = 'auto'`; `model: str = 'auto'`; `speed: str = 'accurate'`; `verbatim: bool = True`; `allow_download: bool = False`; `project: str = ''`; `out: str = ''`

### `video_transcript_edit`

Edit a talking video by its transcript (Descript-style). Cut what you remove from the text:
remove=["exact words to cut", [i0, i1], {"start": 12.0, "end": 15.5}] and/or keep only some parts
(keep=[…] in the ORDER you want them — reorders the story). Word indices come from video_transcript
(pass its .json as transcript= so Whisper does not run again). remove_fillers: English um/uh/er/hmm
always, 'like / you know / I mean / basically…' only when standalone (pause or comma on both sides);
Egyptian/MSA Arabic امم/ممم/فـ always, 'يعني / آه / بص / يعني إيه / إيه ده / طب' only when standalone —
filler_mode safe (hesitation sounds only) | standard | aggressive. remove_silences shortens every pause
to max_pause s. remove_repeats drops stutters ('I I think'). remove_unlabelled also cuts voiced gaps
Whisper did not transcribe (often 'um'). Cut points snap to the quietest 10 ms; audio crossfades
(crossfade_ms, 10–20) at every cut. captions: '' or a style (reels/clean/bold…) to burn captions from
the edited words. dry_run: only the plan. verify: re-transcribe the result (fast model) and warn if a
cut word is still audible (Whisper word times are ±0.1 s). Returns MP4 + .kdenlive + timeline .json + cut list (.md/
.json, source timecodes) + CMX3600 .edl + a transcript image with every cut struck through (LOOK).

Arguments: `path: str`; `keep: list = []`; `remove: list = []`; `remove_fillers: bool = True`; `filler_mode: str = 'standard'`; `remove_silences: bool = True`; `max_pause: float = 0.35`; `remove_repeats: bool = False`; `remove_unlabelled: bool = False`; `language: str = 'auto'`; `transcript: str = ''`; `captions: str = ''`; `crossfade_ms: float = 15.0`; `model: str = 'auto'`; `speed: str = 'accurate'`; `allow_download: bool = False`; `dry_run: bool = False`; `verify: bool = True`; `project: str = ''`; `out: str = ''`

### `video_trim`

Cut one section out of a video (start → end, or start + duration). mode: accurate (re-encode,
frame-exact, default) | fast (stream copy, instant and lossless but snaps to the keyframe before
`start`). Returns the clip + contact sheet.

Arguments: `path: str`; `start: float = 0.0`; `end: float = 0.0`; `duration: float = 0.0`; `mode: str = 'accurate'`; `project: str = ''`; `out: str = ''`

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

### `audio_library_search` N

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

### `audio_voiceover` N

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

### `audio_voices` N

Voice catalogue for audio_voiceover: lists Edge neural voices (online, free) and/or Piper voices
(offline) for a language ('ar', 'ar-EG', 'en', 'en-GB', 'all'), with gender, accent and personality.
samples=N renders the first N voices reading sample_text and one 'audition' file with all of them
back to back (a 1 s beep between voices, in list order) so the user can pick by ear.
Returns data.voices [{id, gender, locale, engine, sample}].

Arguments: `language: str = 'ar'`; `gender: str = ''`; `engine: str = 'edge'`; `samples: int = 0`; `sample_text: str = ''`; `project: str = ''`; `out: str = ''`
