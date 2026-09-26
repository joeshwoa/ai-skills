# omnicinema-mcp — tool catalog

Generated from the live server's tools/list (omnicinema-mcp 0.3.0, 173e627). Regenerate after upgrading: `bash scripts/call.sh --list` or `--json --list`. Descriptions are the server's own words.

## run_cinema_pipeline
Use when the user wants a short video from a one-line idea. Writes a multi-scene screenplay with shot-to-shot continuity, fills each shot with stock footage (Pexels/Pixabay/Unsplash, only if their keys are set) or an offline storyboard frame, optionally adds narration (offline system TTS + captions) and a soundtrack fitted to the cut, edits a frame-accurate timeline (hard cuts in a scene, dissolves between scenes) and renders an MP4 with Remotion or ffmpeg.
TIP: call with dry_run:true first — it returns the screenplay, shot list, provider choice and a cost/network estimate instantly without writing files, so you can show the user before producing.
Network/money: stock APIs are used automatically when keys exist (free; set stock:false to stay offline). generative:true calls paid-or-quota video APIs (budget-guarded; approveOverBudget:true to exceed). With no keys everything runs offline.
Returns: projectId, rendered MP4 path (if rendered), screenplay.md, timeline.json, attributions, warnings, next steps. interactive_montage pauses before the edit so a human can reorder/replace clips, then compile_montage finishes.

Arguments:
- `prompt` (required) — string: The video idea, e.g. 'a lone lighthouse keeper watching a storm roll in'.
- `dry_run` — boolean: true = plan only: screenplay, shot list, providers, cost estimate. No files, no network, no quota.
- `workflow_mode` — string one of fully_automated, interactive_montage (default "fully_automated"): fully_automated renders in one call; interactive_montage stops after gathering clips (then use compile_montage).
- `sceneCount` — integer: Number of scenes (default 3–5 from the prompt). Scenes follow a story arc.
- `shotsPerScene` — integer: Shots per scene (default 2): establishing → medium → close.
- `shotDurationSeconds` — number: Seconds per shot (default 4).
- `fps` — integer: Frames per second (default 30).
- `width` — integer: Frame width (default 1920). Use 1080 with height 1920 for vertical.
- `height` — integer: Frame height (default 1080).
- `style` — string: Visual style, e.g. 'noir', 'documentary', 'neon cyberpunk'. Also steers lighting.
- `prefer` — string one of video, image: Prefer motion b-roll ('video', default) or stills ('image') from stock.
- `stock` — boolean: Use stock APIs when keys are configured (default true). false = fully offline storyboard/animatic.
- `generative` — boolean: SPENDS QUOTA/MONEY: generate clips with your Replicate/fal/HF video model (default false).
- `approveOverBudget` — boolean: Only after the user agrees: proceed past the free-tier budget guard.
- `render` — boolean: Render the MP4 now (default true in fully_automated). Uses Remotion if installed, else ffmpeg.
- `narration` — string: Narration script. Spoken offline by the system TTS (say/flite/espeak-ng), captioned, locked to the timeline; the last shot is held if the narration runs long.
- `captions` — boolean: Burn narration captions into the video (default true).
- `soundtrack` — boolean: Add an offline-synthesized soundtrack fitted to the video length, ducked under narration.
- `musicStyle` — string: Soundtrack genre: 'lo-fi', 'cinematic orchestral', 'hip-hop', 'trap', 'rock', 'electronic', 'ambient'.
- `enrich` — boolean: SPENDS MONEY: true + ANTHROPIC_API_KEY polishes the screenplay prose with one Anthropic API call. Default false (offline template prose).

## compile_montage
Use after run_cinema_pipeline in interactive_montage mode, or to re-cut any project: rebuilds the timeline from the project folder (honoring an optional montage-order.json and any clip files you replaced), validates it (no gaps, no missing files) and renders the MP4. Offline; no network. Returns the MP4 path, validation warnings and next steps.

Arguments:
- `projectId` (required) — string: The projectId returned by run_cinema_pipeline.
- `render` — boolean: Render after compiling (default true).

## install_dependencies
Use when rendering fails because ffmpeg, Blender or the Remotion toolchain is missing. With consent:false (default) it only detects the OS and returns the exact commands it WOULD run — nothing is installed. Only call with consent:true after the user explicitly agrees; it then runs the package manager (may need sudo) and npm (network).

Arguments:
- `consent` — boolean (default false): true runs the install commands. Only set after explicit user approval.
- `targets` — array: Which dependencies (default all).

## list_providers
Use to answer 'what can this server do with my keys?'. Lists every catalogued provider (stock, generative video/image, audio) with whether its key/model env vars are set. Offline; reads tools-registry.json and env only.

Arguments:

## discover_providers
Use when the user asks to find new video/model tools. Searches the public Hugging Face Hub and GitHub Search APIs (network, no key needed; GITHUB_TOKEN optional) and QUEUES candidates in data/review-queue.json. Never installs, enables or runs anything. Returns the top candidates and the queue size.

Arguments:
- `query` (required) — string: Search term, e.g. 'text to video'.

## approve_suggestion
Use only after the user approves a discovered candidate. Adds it to tools-registry.json as DISABLED and unimplemented (a human must write an adapter and enable it). No network. Requires approve:true; otherwise does nothing.

Arguments:
- `suggestionId` (required) — string: The suggestion id from discover_providers.
- `approve` — boolean (default false): Must be true to make any change.

## consult_personas
Use before generating to show/tune the strategy. Runs the persona consultation (Director of Photography, Graphic Designer, Voice Director, Music Producer) for an asset kind and returns the compiled brief: positive/negative prompt, technical params (palette, lens, BPM/key/structure, pacing) and the debate transcript. Instant, offline, writes nothing.

Arguments:
- `assetKind` (required) — string one of cinematic-photo, logo, vector-art, texture, ui-mockup, voiceover, soundtrack, sfx: What to design.
- `subject` (required) — string: The subject/description.
- `style` — string: Style hint, e.g. 'noir', 'lo-fi', 'brutalist'.
- `aspectRatio` — string: e.g. '16:9', '1:1', '9:16'.

## generate_image
Use for logos, illustrations, app/web mockups, photos and textures.
- logo / vector-art / ui-mockup: designed OFFLINE as clean SVG (plus a PNG export when rsvg-convert or ffmpeg is installed). Logos come with -reversed (dark backgrounds) and -icon variants. Free, instant, no network.
- cinematic-photo / texture: need an image API. Without generative:true you get a clearly LABELLED placeholder, not a photo. generative:true calls Replicate/Hugging Face with your key (uses quota; budget-guarded → returns a halt with a cost breakdown; retry with approveOverBudget:true only if the user agrees).
Style words steer the result: palette ('vibrant', 'warm', 'earth', 'mono'), logo layout ('monogram', 'wordmark', 'horizontal', 'emblem'), type voice ('luxury', 'tech', 'playful'), 'sharp' corners. Returns file paths, size, license.

Arguments:
- `assetKind` (required) — string one of cinematic-photo, logo, vector-art, texture, ui-mockup: Type of visual asset.
- `subject` (required) — string: What to create, e.g. 'Nova Labs' (logo), 'fitness mobile app' (ui-mockup), 'mountain sunset'.
- `style` — string: Style keywords (see description).
- `aspectRatio` — string: e.g. '1:1', '16:9', '3:1' (wide logo lockup).
- `generative` — boolean: USES QUOTA: photo/texture via your image API key. Ignored for vector kinds.
- `approveOverBudget` — boolean: Only after the user agrees: proceed past the budget guard.

## generate_voiceover
Use to turn a script into spoken audio (WAV). Offline by default via the system TTS engine (macOS 'say', pico2wave, ffmpeg's flite, or espeak-ng): intelligible but synthetic-sounding, loudness-normalized to -16 LUFS. If no engine exists you get a timing placeholder TONE that is explicitly labelled NOT SPEECH. generative:true uses your Hugging Face TTS model (HF_TTS_MODEL; quota, budget-guarded) for a natural voice. Returns the WAV path and exact duration in ms.

Arguments:
- `subject` (required) — string: The narration text (or a topic if you also pass script).
- `script` — string: Explicit script (overrides subject as the spoken text).
- `style` — string: Delivery: 'dramatic' (slower, deeper), 'calm documentary', 'energetic'.
- `generative` — boolean: USES QUOTA: natural voice via HF_TTS_MODEL.
- `approveOverBudget` — boolean: Only after the user agrees: proceed past the budget guard.

## generate_soundtrack
Use for background music or a beat in a genre: hip-hop, trap/rap, cinematic orchestral, rock, lo-fi, electronic, ambient. Offline by default: the Music Producer plans tempo/key/structure/instruments and the engine composes and synthesizes a stereo WAV (voice-led chords, bass, drums, a melody, section dynamics, mastered to about -14 LUFS) plus an editable multi-track MIDI. It is a synthesized demo, not a studio recording. generative:true uses your MusicGen model on Replicate/HF (quota, budget-guarded). Returns WAV + MIDI paths, exact duration, and the arrangement.

Arguments:
- `subject` (required) — string: Theme/mood, e.g. 'rainy midnight city'.
- `style` — string: Genre, e.g. 'hip-hop', 'cinematic orchestral', 'lo-fi', 'electronic'.
- `durationSeconds` — number: Target length; the arrangement is re-flowed to fit (whole bars).
- `generative` — boolean: USES QUOTA: render via your MusicGen API model.
- `approveOverBudget` — boolean: Only after the user agrees: proceed past the budget guard.

## generate_sfx
Use for a sound effect or ambience. Offline by default: procedural synthesis matched to the request (whoosh, rain, thunder, wind, ocean, impact, riser, click, ding, beep, fire, footsteps, heartbeat). generative:true searches Freesound with your FREESOUND_API_KEY (network, CC-licensed results, budget-guarded). Returns the file path, exact duration and license.

Arguments:
- `subject` (required) — string: The effect, e.g. 'whoosh transition', 'rain ambience'.
- `style` — string: 
- `generative` — boolean: NETWORK: fetch a real recording from Freesound.
- `approveOverBudget` — boolean: Only after the user agrees: proceed past the budget guard.

## check_limits
Use before a generative run or when the user asks about remaining quota. Reports per-provider usage vs the budget guard's daily/weekly/monthly limits from data/usage-limits.json. Offline.

Arguments:
- `provider` — string: A single provider slug; omit for all tracked providers.

## ipc_start
Use when another local program needs to request assets from this engine over HTTP. Starts a server bound to 127.0.0.1 with a bearer token (stored in data/ipc-token.txt, mode 0600). Returns the URL and token. Stop it with ipc_stop.

Arguments:
- `port` — integer: Port (default OMNICINEMA_IPC_PORT or 8787; 0 = any free port).

## ipc_status
Use to check whether the local REST API is running and where. Offline.

Arguments:

## ipc_stop
Use to shut down the local REST API started by ipc_start.

Arguments:

