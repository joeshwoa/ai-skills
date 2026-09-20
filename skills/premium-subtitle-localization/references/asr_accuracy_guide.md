# ASR accuracy on dialect film audio — and the fabrication trap

Read this before transcribing anything colloquial, and before "fixing"
any transcript that looks wrong.

## Why automatic transcription fails badly here

Whisper (and every comparable model) is trained overwhelmingly on clean,
read, *standard-register* speech. A feature film in a spoken dialect
violates all three at once:

- **Register.** Arabic ASR training is dominated by MSA — news, Quranic
  recitation, audiobooks. Almost nobody in a film speaks that way. The
  model maps colloquial phonetics onto the formal vocabulary it knows.
- **Acoustics.** Music under dialogue, room tone, shouting, crying,
  laughter, phone filters, crowd scenes.
- **Overlap.** Real conversation interrupts. Whisper assumes one speaker
  at a time and blends overlapping speech into one line.

The critical property is *how* it fails. It does not output "???" or low
gibberish you'd notice. It outputs **fluent, well-formed, confident text
that is phonetically adjacent to the truth and semantically unrelated.**

Real examples from a run of this skill on an Egyptian comedy:

| actually said | Whisper large-v3 emitted |
|---|---|
| خلّصني قوام | حصاني قوام |
| طلبة الثانوية العامة | طلس التنمية العامة |
| التوفيق والنجاح | التوفير والنجاح |
| مش متوترين | متوازنين |
| يا باشا | يا نبي |

Every one of those is a real Arabic word. Nothing in the text marks them
as errors. Spell-check passes. Grammar passes. Only the audio disagrees.

## The trap: repairing a transcript from context

Handed that table's right-hand column, an agent — or a person — will
reconstruct the left-hand column. The surrounding dialogue makes it
guessable: an exam-day scene, a mother at a door, a TV presenter. So
"طلس التنمية العامة" becomes "طلبة الثانوية العامة" and it is *correct*.

Then the next one is guessable too. And the next. And somewhere in there,
the guesses stop being recoveries and start being invention, with no
felt difference at the moment of writing, because the process feels
identical either way.

This is not hypothetical. A previous run of this skill shipped an Arabic
transcript in which, measured against the raw ASR it came from:

- **19%** of cues were unchanged
- **67%** were edited
- **14%** were rewritten past recognition
- **101 cues** had silently disappeared

— i.e. **81% of the delivered transcript had been altered away from what
the audio actually produced**, entirely in text space, with no
re-listening at any point. The Russian translation built on top of it was
then faithful, careful, four-pass... and downstream of fiction.

The user noticed immediately, because he could hear the film.

### Why every existing check missed it

- `validate_srt.py` checks formatting and timing. The cues were
  well-formed and correctly timed. **Pass.**
- `verify_output.py` checks the muxed file's streams and duration. All
  intact. **Pass.**
- The agentic QA pass compares the *translation* against the *source*.
  The translation was faithful to the source. The source was wrong.
  **Pass.**

Nothing in the pipeline compared anything to the audio. That is the hole
`check_transcript_fidelity.py` closes.

### Why fabrication is worse than garbled text

Garbled text is self-reporting: anyone who opens the file sees a problem
and can act on it. Invented text is silent. It reads *better* than a real
transcript — cleaner, more idiomatic, better punctuated — because it was
written rather than heard. It therefore survives every downstream review
by anyone who does not have the audio open, which is everyone.

A transcript that says `[غير واضح]` thirty times is more useful and more
honest than one that reads perfectly and is 14% invented.

## What to do instead

### If a lot of the film is flagged (>25%)

Don't repair cues. Fix the transcription and re-run:

- **Set `--dialect`.** The single highest-leverage flag. Priming the
  model with colloquial orthography pulls output away from MSA.
- **Use `--model large-v3`.** Not `small`, not `medium`. On this content
  smaller models don't lose accuracy gracefully, they lose it invisibly.
- **Use `--initial-prompt`** with character names, place names, and the
  film's recurring domain nouns. Whisper is far likelier to recognize a
  word it has just "seen" than to guess it from phonetics.
- **Check the backend.** On Apple Silicon, `mlx` runs on the GPU and is
  what makes `large-v3` practical on a feature-length film at all. If
  `transcribe.py` fell back to CPU `faster-whisper`, a full-quality run
  may be impractically slow — install `mlx-whisper` rather than dropping
  to a smaller model.

### If individual cues are flagged

Use `retranscribe_spans.py`. It cuts each span out with padding and
decodes it several times under different conditions (greedy vs. sampled,
with and without the dialect prompt).

- **Decodes agree** → strong evidence; adopt that reading.
- **Decodes scatter** → the audio does not support a confident
  transcript. Mark it unclear. This is a real result, not a failure to
  try hard enough.

The padding matters: Whisper decodes a 1.5-second fragment much worse
than the same words inside a 6-second window. The no-prompt pass matters
too — a reading that only appears *with* the prompt may be the prompt
talking, not the audio.

### The three legal moves, restated

For any cue you believe is wrong:

1. Re-transcribe that span from audio and adopt a reading the decoder
   actually produced.
2. Mark it unclear and surface it to the user.
3. Ask the user what is said there.

Writing what the line "probably" was is not on the list, no matter how
confident the inference or how obvious the context. If you find yourself
reasoning "this is clearly meant to be X" — that is the trap, and the
fact that it feels obvious is exactly what makes it dangerous.

## Honest limits

Even done correctly, dialect ASR on film audio is hard. A good run on
difficult material can still leave a few percent of cues unresolved.
That is the state of the technology, not a defect in the work, and
saying so plainly is part of delivering the job. What is *not*
acceptable is converting that uncertainty into confident invented text
because it produces a nicer-looking deliverable.
