# QA review checklist — the reviewer agent pass

`validate_srt.py` is a mechanical tester: it catches formatting/timing
bugs but has no idea whether the translation is any good. This checklist
is the judgment-based pass the user asked for explicitly ("some agent
that check the work and results") — run it after `validate_srt.py`
passes, before merging into the video.

**If your environment can spawn an independent sub-agent, use a fresh
one for this pass** — it should not have written the translation, so it
reviews with no attachment to the previous phrasing choices. If you're a
single agent, deliberately switch mindset: read as a skeptical editor
checking someone else's work, not as the translator re-reading your own.

## What to check

Work through the translated SRT (all of it for a short piece; a
representative sample — every batch, a few cues from each — for a full
movie) against the *original* source SRT side by side:

1. **Meaning fidelity.** For each checked line: does the target line
   convey what the source line conveys? Not word-for-word — does a
   target-language viewer walk away believing the same thing happened,
   the same joke was made, the same emotional beat landed? Flag any line
   where the meaning was accidentally changed or lost (not deliberately
   adapted — see the `.notes.json` sidecar for deliberate adaptations,
   which is exactly what that file is for: telling you which
   differences from literal are on purpose).

2. **Adaptation notes check out.** For every cue with a `note` in the
   `.notes.json` sidecar, confirm the adaptation actually makes sense:
   does the substituted idiom/reference/joke actually produce the effect
   the note claims? A note that says "adapted the pun" but the resulting
   line isn't actually funny or clear is a failed adaptation, not a
   successful one — flag it for a re-pass.

3. **Character voice consistency.** Does each character sound like the
   same person across their lines — same register, same verbal habits —
   or does the translation's tone drift cue to cue in a way the source
   didn't?

4. **Nothing invented.** Scan for lines that assert something the source
   didn't (an added joke, an opinion, a plot detail) — adaptation changes
   phrasing, never facts.

5. **Reads naturally out loud.** Say a sample of lines to yourself (or
   simulate doing so) in the target language — stiff, "translated-sounding"
   phrasing that technically means the right thing still fails this
   check; flag it for a Pass-4 fluency fix.

6. **Comedy-specific (if genre is comedy):** do punchlines land at the
   end of their cue, matching the pacing the source had? A correctly
   translated joke that's phrased so the funny word isn't the last word
   often just doesn't read as funny — flag for a reword, not a re-translation.

## Output of this pass

Produce a short list: `cue #N: <issue> -> <suggested fix>` for anything
flagged. Anything flagged goes back through Pass 2–4 of
`translation_workflow.md` for just that cue (no need to redo the whole
batch), then re-run `validate_srt.py` before merging.

If nothing is flagged after checking a representative sample, say so
explicitly to the user ("reviewed N of M cues across every batch, no
meaning or fluency issues found") rather than silently proceeding —
this pass existing and finding nothing is still worth stating, the same
way premium-presentations reports a clean `validate_deck.py` run instead
of just moving on.
