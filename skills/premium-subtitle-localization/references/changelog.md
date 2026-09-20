# Changelog — premium-subtitle-localization

## 2026-09-20 — transcript fidelity: stop ASR errors becoming invented dialogue

**Trigger:** real usage report. Arabic→Russian subtitling of an Egyptian
comedy. The user's report: the Arabic subtitles don't match the words
spoken in the film, so the Russian built on them can't be right either.

**Diagnosis.** Not a translation bug and not a tuning bug. Measuring the
shipped source transcript against the raw ASR it was derived from:
19% of cues unchanged, 67% edited, 14% rewritten past recognition, and
101 cues silently dropped — 81% of the delivered transcript altered away
from what the audio produced, all of it in text space with no
re-listening. The ASR output itself was genuinely garbled (Whisper
large-v3 on Egyptian colloquial + film audio emits fluent phonetic
nonsense), and the pipeline's response to garbled text was to make it
read well. Every existing check passed, because none of them compared
anything to the audio: `validate_srt.py` checks format/timing,
`verify_output.py` checks the container, and the agentic QA pass checks
the translation against a source it assumes is correct.

**Root cause:** the skill treated `source.srt` as ground truth, gave the
agent no evidence-based way to fix a garbled cue, and had no rule against
inferring one from context. Fluency pressure did the rest.

### Changed

- **`scripts/transcribe.py`** — rewritten. Backend auto-detection
  (`mlx_whisper` on Apple Silicon → `faster_whisper` elsewhere); default
  model raised from `small` to `large-v3`; `--dialect` priming for
  Egyptian/Gulf/Levantine/Maghrebi; `--initial-prompt` for names and
  domain nouns; `condition_on_previous_text=False` (stops one bad line
  biasing the next into a self-consistent fiction); temperature fallback;
  hallucination-boilerplate blocklist; word timestamps driving cue
  splitting; repeat collapsing. Now also writes a
  `<out.srt>.asr.json` sidecar with per-cue confidence.

### Added

- **`scripts/asr_confidence.py`** — triages a transcript from the sidecar,
  flags cues the model was unsure about, writes a review queue. Warns
  when >25% is flagged, since that means the transcription settings are
  wrong rather than a few lines being hard.
- **`scripts/retranscribe_spans.py`** — the legitimate repair path. Cuts
  each flagged span from the audio with padding, re-decodes it under
  several independent conditions, and reports whether they agree.
  `--finalize` applies chosen readings and writes an evidence file, and
  **refuses any chosen text that no decode actually produced**.
- **`scripts/check_transcript_fidelity.py`** — the gate. Diffs the edited
  transcript against the raw ASR, and fails on undocumented rewriting
  (>5%) or any silently dropped cue. Run in Step 1.5 and again in Step 3.
- **`references/asr_accuracy_guide.md`** — why dialect ASR fails this
  way, the fabrication trap, and the three legal moves for a garbled cue.

- **`SKILL.md`** — new **Step 1.5: verify the transcript against the
  audio (REQUIRED)**, with the explicit rule that a garbled cue may only
  be re-transcribed, marked unclear, or asked about — never guessed.
  Step 2 now forbids editing source text during translation; Step 3 adds
  a second fidelity check; Step 5 must report re-transcribed and unclear
  cue counts. Accuracy-over-fluency is stated in the intro.

**Verification.** The fidelity gate was run against the real failing run
and correctly fails it (133 undocumented rewrites, 101 dropped cues),
naming the invented lines. The confidence triage, the finalize accept
path, the unclear path, the evidence round-trip, and the refusal of
non-decoder-produced text were each tested end to end.

**Known limit.** The re-transcription loop could not be executed against
real audio from this environment (the device shell is a Linux VM;
`mlx_whisper` is Apple-Silicon-only). Its ffmpeg span-cutting, candidate
comparison, finalize/refusal logic and evidence round-trip are tested;
the live decode path runs first on the user's own machine.
