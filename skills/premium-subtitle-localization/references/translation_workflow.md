# Translation workflow — the virtual expert team

This is the core of the skill. A subtitle translated word-for-word is
*wrong* even when every word is correct — jokes die, idioms turn to
nonsense, and register (formal/casual, who's mocking whom) gets lost.
This document is what makes the difference between that and a
translation that actually lands for a target-language audience.

**Who does this work:** the agent running this skill (Claude, Cursor, an
GPT-based agent, whatever is executing the SKILL.md steps) — not a
translation library. `deep-translator`/Google-Translate-style tools do
literal, statistical translation, which is precisely the failure mode
this workflow exists to avoid. Scripts in this skill only ever handle
mechanics (parsing, batching, timing, file I/O); every line of actual
translated text comes from the agent's own language understanding.

**If your environment can spawn independent sub-agents** (e.g. Claude
Code's Task tool, or any multi-agent orchestration the host supports),
run passes 2–4 below as separate sub-agent calls so each one is a fresh
read with no anchoring bias toward the previous pass's phrasing — hand
each sub-agent the batch JSON plus this file and one clear instruction
for its own pass. **If your environment is a single agent with no
sub-agent capability**, do all four passes yourself, sequentially, but
treat each pass as a genuine, critical re-read of the previous pass's
output — not a rubber stamp. Say explicitly (in your own reasoning) what
you're checking for in each pass; don't silently merge them into one
step, or the discipline this structure is for gets lost.

## Inputs you need before starting

- Source SRT (from Step 1 of SKILL.md) and the work-order JSON from
  `batch_for_translation.py` (cues grouped into batches with context).
- **Genre/tone** — comedy, drama, documentary, technical/corporate,
  children's content. This changes the priority order below: comedy
  prioritizes "the joke lands" over literal accuracy; a documentary
  prioritizes factual accuracy over any adaptation; corporate/technical
  content prioritizes terminology consistency. Ask the user if it's not
  obvious from the content itself (see SKILL.md Step 0).
- **Source and target language/culture.** Not just the language — *which*
  culture's register and references. Russian-in-Russia and
  Russian-in-a-diaspora-community can want different levels of
  localization; ask if it matters and isn't obvious.

## The four passes, per batch

Work through each batch from `batch_for_translation.py`'s output in
order (batches carry a little dialogue *before* and *after* their real
target lines — read all of it for context; only translate the lines
listed under `"translate"`).

### Pass 1 — Literal draft (understand, don't polish yet)

For each line, work out its exact denotative meaning: who is speaking,
to whom, what is literally being said, and what (if anything) is
implied — sarcasm, a double meaning, a reference to something said
earlier in the context window. Do not try to make this sound good yet;
the point is to nail down *what the line actually means* before
touching *how to say it*, so cultural adaptation later doesn't
accidentally drift from the source's intent.

### Pass 2 — Meaning-preserving rewrite ("translation expert")

Rewrite the literal draft into the target language so the **meaning and
intent survive**, even where the literal words wouldn't. This is
ordinary professional translation: correct grammar, correct register
(is this character rude, formal, flirting, scared?), correct handling of
things that don't map 1:1 (a source pun that doesn't exist in the target
language gets a *different device* that produces the same effect, not a
literal non-joke). Preserve each character's voice consistently — if
someone speaks bluntly in the source, they should still sound blunt, not
suddenly polite because the target language's polite register was
easier to write.

### Pass 3 — Cultural adaptation ("localization expert")

This is where culture-bound content gets handled — idioms, slang,
region-specific references (a local celebrity, a food, a religious or
national holiday, a brand only known in one country), wordplay that only
works in the source language's sounds/spelling.

Rules, in priority order:

1. **Prefer a target-culture equivalent that produces the same effect**
   over either a literal translation (which won't land) or a footnote
   (subtitles have no footnotes). "He's about as useful as a chocolate
   teapot" → find the target language's own idiom for "useless," not a
   literal chocolate teapot.
2. **When no equivalent exists and the reference matters to the joke or
   plot**, add the *smallest possible* clarifying hint woven into the
   line itself — a few words, not a clause, and never breaking the
   subtitle's time budget (see `subtitle_standards.md` for the
   reading-speed limits this is bound by). This is not a translator's
   note in brackets; it reads as a natural part of the line. Example
   pattern: a source line naming a specific local dish that means
   "comfort food" to the source audience can become "[target dish that
   means comfort food]" or, if no clean equivalent exists, a short
   generic phrase like "his mom's cooking" — something a target-culture
   viewer parses instantly, without ever feeling like a translator
   interrupted the scene to explain something.
3. **When a reference is decorative and losing it changes nothing**
   (a throwaway brand mention, a name-drop that isn't a plot point),
   it's fine to substitute a generic/neutral equivalent rather than
   force an explanation — don't let a minor reference cost the joke's
   timing.
4. **Never invent meaning the source didn't have.** Adaptation changes
   *how* something is said, not *what happened* — don't add jokes,
   opinions, or plot details that aren't implied by the source line.
5. Log every non-trivial adaptation as a `note` on that cue (the `note`
   field `apply_translation.py` collects into a sidecar file) — e.g.
   `"source pun on X (لعبة على المعنى) has no Russian equivalent; used a
   different pun on Y that produces the same laugh in the same beat"`.
   This is what a reviewer (Pass 5 / the QA checklist) checks against —
   without notes, nobody can tell "meaning preserved differently" from
   "meaning lost".

### Pass 4 — Fluency and timing polish ("editor")

Read the batch straight through, in the target language only, as if you
were a target-language viewer who never saw the source. Fix anything
that reads as translated rather than written: unnatural word order,
over-formal phrasing where the scene is casual, a joke's punchline
landing on the wrong word for the sentence's natural rhythm. For comedy
specifically, punchlines should land at (or very near) the end of the
line/cue, matching where the original placed its punch — timing is part
of what makes a joke work, and subtitle cues are the one place a
translator controls timing precisely (each cue has a fixed duration from
the source; see `subtitle_standards.md`).

Then check length against the cue's `duration_ms` (given in the batch
JSON) using the reading-speed limits in `subtitle_standards.md` — if the
natural target-language phrasing is unavoidably longer than the time
allows (common going into e.g. German or Russian from a terser source
language), tighten wording rather than let `validate_srt.py` catch it
later; don't just accept an overlong line and hope.

## After all batches: assemble and hand to QA

Collect every cue's final text into the flat JSON
`apply_translation.py` expects (`[{"index": N, "text": "...", "note":
"..."}]`), run it to produce the real SRT, then run `validate_srt.py`
(mechanical checks) and go through `qa_review_checklist.md` (the
judgment-based review pass) before merging into the video.
