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
  not a single mechanical translate-and-burn-in step. Also verifies the
  source transcript against the actual audio before translating, so
  dialect/ASR errors are caught rather than silently rewritten into
  fluent invented dialogue.
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

There is a second, less obvious failure this skill is built to prevent.
Subtitles are judged by how they read, so every pressure in the pipeline
pushes toward output that reads well. On hard audio — colloquial
dialect, music under dialogue, overlapping speakers — automatic
transcription returns garbled text, and the instinctive response is to
tidy it into something fluent. That instinct is the single most damaging
thing you can do here: invented dialogue reads *better* than real
dialogue, so it passes every review by anyone without the audio open.
Accuracy to what was actually said outranks fluency at every step, and
Step 1.5 exists to enforce that mechanically rather than on good
intentions.

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
video, use that — skip transcription entirely. Note that a found file
carries no confidence data, so Step 1.5's automated triage cannot run on
it: spot-check a dozen cues spread across the film against the audio
before trusting it, and treat it as suspect if it looks machine-made
(uniform cue lengths, no punctuation, MSA phrasing over colloquial
speech). If it finds only other
formats (`.vtt`/`.ass`), convert with `ffmpeg -i in.vtt out.srt` first
(ffmpeg handles that natively).

If nothing usable exists, generate one from the audio:

```bash
pip install --break-system-packages -r scripts/requirements.txt   # mlx-whisper or faster-whisper
python3 scripts/transcribe.py "/path/to/movie.mp4" source.srt \
    --lang ar --dialect egyptian --keep-wav work/audio.wav
```

Keep `source.srt` as the untouched raw ASR — copy it to `source.raw.srt`
now. Step 1.5 needs the original to compare against, and `--keep-wav`
preserves the audio the re-listening step needs. Deleting either forces
every later fix to become a guess.

**Defaults that matter, and are not negotiable on dialect content:**

- `--model` defaults to `large-v3`. Smaller Whisper models do not degrade
  gracefully on colloquial film audio — they emit confident, fluent,
  phonetically-plausible nonsense. `small` here is not "faster with some
  errors", it is a transcript that is wrong in a way no later step can
  detect.
- `--dialect` primes the model for how people actually talk. Whisper's
  Arabic training is dominated by MSA/news, so without it the output
  drifts toward formal Arabic nobody in the film said. Supported:
  `egyptian`, `gulf`, `levantine`, `maghrebi` (see `transcribe.py` to add
  more).
- `--initial-prompt` with character names, place names and the film's
  recurring domain nouns measurably raises recognition of exactly those
  words. Use it whenever you know them.
- On Apple Silicon the `mlx` backend is picked automatically and runs on
  the GPU. That is what makes `large-v3` practical on a feature film
  instead of an overnight job.

## Step 1.5: verify the transcript against the audio — REQUIRED

**Do not translate an unverified transcript.** Everything downstream —
all four translation passes, the QA review, the final video — treats
`source.srt` as ground truth. If it isn't, none of that work can detect
the problem, because a translation faithful to a wrong source looks
exactly like a correct translation.

```bash
python3 scripts/asr_confidence.py source.srt --queue work/review_queue.json
```

This reads the `source.srt.asr.json` sidecar `transcribe.py` wrote and
flags every cue the model was unsure about. If more than ~25% of the
film is flagged, stop and fix the *transcription* (wrong dialect? wrong
model? missing prompt?) — re-running the whole film beats repairing
hundreds of cues by hand.

### The rule: a garbled cue has exactly three honest resolutions

When you meet a cue that reads as nonsense, you may:

1. **Re-transcribe that span from the audio** — the preferred move.
2. **Mark it unclear** (`[غير واضح]` / the target-language equivalent)
   and flag it for the user.
3. **Ask the user what is said there.**

You may **not** write what the line "probably" was, however obvious it
seems from the surrounding dialogue. That is fabrication, and it is the
single worst failure this skill can produce: invented dialogue comes out
*more* fluent than real dialogue, so it survives every review by anyone
who doesn't have the audio open. Reading well is not evidence.
`references/asr_accuracy_guide.md` has the full reasoning and a real
worked example of this going wrong.

Resolve the queue against the audio:

```bash
python3 scripts/retranscribe_spans.py work/review_queue.json --out work/candidates.json
# then set "chosen" per span (copy a candidate verbatim, or "" for unclear)
python3 scripts/retranscribe_spans.py --finalize work/candidates.json source.srt \
    --evidence work/evidence.json
```

Each span is re-decoded several times under different conditions. Where
independent decodes agree, that's strong evidence. Where they scatter,
the audio genuinely doesn't support a confident reading and the honest
answer is "unclear" — not the nicest-sounding option. `--finalize`
refuses any `chosen` value that no decode actually produced.

Then prove the transcript still matches what was heard:

```bash
python3 scripts/check_transcript_fidelity.py source.raw.srt source.srt \
    --evidence work/evidence.json --report work/drift.json
```

This must exit 0 before you translate anything. It fails on undocumented
rewriting and on cues that silently vanished. If it fails, fix the
transcript — do not raise the thresholds to make it pass.

Tell the user, in the Step 5 summary, how many cues were re-transcribed
and how many are marked unclear. Unclear cues are a normal, honest
outcome on hard audio; hiding them is not.

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

**Do not edit the source text during translation.** If a source cue
still looks wrong at this stage, that is a Step 1.5 problem: send it
back through `retranscribe_spans.py`, or mark it unclear. Quietly
"fixing" the Arabic (or any source language) while writing the target
line puts an unverified guess into the file at the one point where
nothing is checking the source any more — this is exactly how a past run
shipped a transcript with 81% of its cues altered away from what the
audio contained.

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

**Transcript fidelity (the guard against silent source edits)** — cheap,
and it catches the one failure the other two checks structurally cannot:

```bash
python3 scripts/check_transcript_fidelity.py source.raw.srt source.srt \
    --evidence work/evidence.json
```

Run it again here even though Step 1.5 already did: Step 2's four passes
are exactly where a source cue tends to get quietly "corrected" in
passing. A non-zero exit means the source drifted after it was verified.

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
were obtained (found vs. transcribed, and with which model/dialect), how
many cues, **how many cues were re-transcribed from audio and how many
remain marked unclear**, which cues (if any) got non-literal cultural
adaptations worth mentioning, and the `validate_srt.py` /
`check_transcript_fidelity.py` / review-pass outcomes. Report unclear
cues plainly — on hard audio they are the honest result, and a run that
claims none on difficult dialect audio is more suspicious than one that
reports thirty. Don't dump the full dialogue
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
