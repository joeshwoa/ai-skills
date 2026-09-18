---
name: premium-subtitle-localization
description: >
  Add translated subtitles to a video — find or generate source-language
  subtitles, translate them with real cultural/comedic adaptation (never
  a flat literal translation), validate formatting and timing, and mux
  the result into the video without re-encoding. Use this whenever the
  user asks to subtitle, translate, localize, or dub (subtitle-only) a
  video/movie/show into another language, or gives a video file and a
  target language. Involves a "virtual expert team" of translation
  passes (literal draft, meaning-preserving rewrite, cultural adaptation,
  fluency/timing polish) plus automated QA and an agentic review pass —
  not a single mechanical translate-and-burn-in step.
---

# Premium Subtitle Localization

## Why this skill exists, and what it actually is

A subtitle pipeline built out of `ffmpeg` + a translation API is easy to
build and produces subtitles nobody enjoys reading: jokes die, idioms
turn literal and confusing, and the video gets needlessly re-encoded.
This skill is that same pipeline done properly — real audio/video
tooling for the mechanical parts (extraction, timing, muxing,
validation), and a structured, multi-pass **agentic** translation
process for the part that actually requires judgment: making the target
language line mean, and land, what the source line meant and landed.

Be upfront if asked: this skill does not do voice dubbing (replacing the
audio track with translated speech) — it produces subtitles only. It
also doesn't guarantee every joke survives; some genuinely don't
translate, and Pass 3 of the translation workflow documents the honest
fallback for those cases (see `references/cultural_adaptation_guide.md`).

## Step 0: figure out the job

If the request already gives you a video path, target language, and
it's obvious from context (e.g. "translate this movie to Russian
subtitles"), skip to Step 1. Otherwise ask briefly, covering only what's
actually unclear:

1. **Video file path.**
2. **Source language** (or "detect it") and **target language(s)** —
   this skill supports any pair; nothing is hardcoded to a specific
   language beyond the CPS/line-length tables in
   `references/subtitle_standards.md` (extend those tables for a
   language not yet listed).
3. **Genre/tone** — comedy, drama, documentary, corporate/technical,
   kids' content. This changes translation priorities (see
   `references/translation_workflow.md`) — comedy prioritizes the joke
   landing, documentary prioritizes factual precision.
4. **Output preference** — soft subtitles (a toggleable track, default;
   no re-encode, no quality loss) or burned-in/hardsub (only if the
   target platform can't do subtitle tracks — this re-encodes the
   video). Default to soft-sub unless told otherwise.

Keep this to one round of questions; use sensible defaults (soft-sub,
genre inferred from the filename/description if not stated) for
anything the user doesn't specify.

## Step 1: get source-language subtitles

```bash
python3 scripts/find_subtitles.py "/path/to/movie.mp4"
```

If it finds a matching-language `.srt` already sitting next to the
video, use that — skip transcription entirely. If it finds only other
formats (`.vtt`/`.ass`), convert with `ffmpeg -i in.vtt out.srt` first
(ffmpeg handles that natively).

If nothing usable exists, generate one from the audio:

```bash
pip install --break-system-packages -r scripts/requirements.txt   # faster-whisper, if not already installed
python3 scripts/transcribe.py "/path/to/movie.mp4" source.srt --lang ar --model small
```

Skim the result before trusting it — ASR mishears names/slang/overlapping
dialogue, and any mistake here propagates into every target language.
Fix obvious transcription errors directly in `source.srt` before
translating.

## Step 2: translate — the virtual expert team

**Read `references/translation_workflow.md` before doing any
translating** — this is the actual substance of the skill, not
boilerplate. It defines four passes (literal draft → meaning-preserving
rewrite → cultural adaptation → fluency/timing polish) that together
are how "language experts and translation experts" gets implemented:
either as separate sub-agent calls if your environment supports
spawning them, or as four genuinely distinct passes by the same agent.
Also read `references/cultural_adaptation_guide.md` for concrete
idiom/joke/reference-handling patterns.

Mechanically:

```bash
python3 scripts/batch_for_translation.py source.srt work_order.json --batch-size 25 --context 3
```

This produces a JSON work order grouping the dialogue into batches (with
a little surrounding context per batch so jokes/callbacks translate
coherently, not line-by-line blind). Work through
`translation_workflow.md`'s four passes for each batch, then collect
every cue's final text into a flat JSON file:

```json
[
  {"index": 1, "text": "translated line here", "note": "optional: explain any non-literal adaptation"},
  {"index": 2, "text": "..."}
]
```

`note` is how deliberate adaptations get logged for review — always add
one whenever a line isn't a close literal translation, so the QA pass
(Step 3) can tell "adapted on purpose" from "meaning drifted by
accident."

```bash
python3 scripts/apply_translation.py source.srt translations.json target.srt
```

This reassembles the translation into a real SRT using the *original*
cue timings (translation never invents new timing) and writes adaptation
notes to `target.srt.notes.json`.

## Step 3: validate — automated tests + agent review

Two different kinds of check, both required, neither optional:

**Automated ("the tester")** — formatting/timing rules, no judgment
involved:

```bash
python3 scripts/validate_srt.py target.srt --lang ru --source source.srt
```

Fix every reported error (exit code non-zero) before proceeding.
Warnings (reading speed, line length) are worth a look but aren't always
fixable without changing the meaning — use judgment, documented in
`references/subtitle_standards.md`.

**Agentic review ("the reviewer")** — meaning fidelity, adaptation
quality, character voice consistency, nothing invented. Follow
`references/qa_review_checklist.md` — spawn a fresh sub-agent for this
if your environment supports it (it should review, not have written,
the translation), otherwise switch mindset and do it yourself as a
skeptical editor. Report the outcome to the user either way (what was
checked, what if anything was flagged and fixed).

Loop back to Step 2 for any flagged cue, then re-run `validate_srt.py`,
before moving on.

## Step 4: merge into the video

```bash
# soft subtitles (default) — no re-encode, instant regardless of movie length
python3 scripts/merge_subtitles.py "/path/to/movie.mp4" target.srt "/path/to/movie.ru.mkv" --lang ru

# only if the target platform genuinely can't do subtitle tracks:
python3 scripts/merge_subtitles.py "/path/to/movie.mp4" target.srt "/path/to/movie.ru.burned.mp4" --burn-in
```

Then verify the output is actually correct — never just trust ffmpeg's
exit code:

```bash
python3 scripts/verify_output.py "/path/to/movie.mp4" "/path/to/movie.ru.mkv"
```

This checks the output file is playable, has video/audio/subtitle
streams intact, and its duration matches the original (a merge that
silently truncated the file is a real, catchable failure mode).

## Step 5: hand it over

Deliver the final video file and a short summary: how source subtitles
were obtained (found vs. transcribed), how many cues, which cues (if
any) got non-literal cultural adaptations worth mentioning, and the
`validate_srt.py` / review-pass outcome. Don't dump the full dialogue
into the chat — the summary is what's useful, the file speaks for
itself.

## Extending: another language pair, another genre

- Add a language to `CPS_BY_LANG` / `MAX_CHARS_PER_LINE_BY_LANG` in
  `scripts/validate_srt.py` before relying on its reading-speed/line
  checks for that language — the generic default is conservative but not
  tuned per-language.
- Genre-specific translation priorities live in
  `translation_workflow.md`'s "Inputs you need" section — add a new
  genre bullet there if a genre this skill hasn't handled before (e.g.
  courtroom drama, where precise legal terminology might outrank
  fluency) comes up.

## What this skill won't do

- **No voice dubbing.** Subtitles only — replacing the audio track with
  translated speech is a different (much harder) pipeline this doesn't
  attempt.
- **No guarantee every joke survives.** Some jokes are genuinely
  untranslatable; the honest fallback (translate straight, log it) is
  documented in `cultural_adaptation_guide.md` rather than pretending
  every line can be rescued.
- **No mechanical/API translation as the primary path.** A translation
  library can be useful for a rough first-pass draft on a very long
  file if truly needed, but the meaning-preserving/cultural-adaptation
  work always has to be the agent's own reasoning, per
  `translation_workflow.md` — that's the entire point of this skill
  over just calling `ffmpeg` and Google Translate directly.
