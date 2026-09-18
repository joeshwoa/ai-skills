# Subtitle technical standards

The numeric limits `validate_srt.py` checks, and why they exist — so
when the validator warns, you know whether to actually fix the line or
it's a defensible exception.

## Reading speed (characters per second, CPS)

The core constraint: a viewer has to read the line *and* watch the
scene, in the time the cue is on screen. Go too fast and the subtitle is
functionally decorative — nobody finishes reading it.

| Language | Recommended max CPS | Why |
|---|---|---|
| English | 20 | Netflix/BBC-style professional guideline |
| Arabic | 18 | Script + diacritics read slightly slower at speed |
| Russian, German | 18–19 | Longer average word length than English for the same meaning |
| French, Spanish, Italian, Portuguese, Turkish | 19 | |
| Japanese, Chinese, Korean | 6–7 (counted in *characters*, not phonemes) | Each character carries more meaning; a much lower character-count budget produces a similar actual reading time |

These are defaults in `validate_srt.py`'s `CPS_BY_LANG` — add a language
there if you're localizing into something not listed, rather than
silently reusing the generic default.

## Line length and count

- Max **2 lines** per cue. A third line usually means the cue should
  either be split into two cues (if the timing allows it) or the text
  tightened — three-line subtitles cover too much of the frame.
- Max **~42 characters per line** for Latin-script languages (Netflix's
  widely-used figure); Russian/German get slightly more room (44) since
  their words run longer for the same meaning; CJK gets much less
  (16–18) since each character is visually denser.

## Timing

- **Minimum duration ~700ms.** Below that, most viewers can't even
  register a short cue existed, regardless of reading speed math.
- **Minimum gap ~80ms between consecutive cues.** Cues that touch or
  overlap can flicker or fail to render as two distinct subtitles
  depending on the player; a small gap avoids that entirely.
- **Never invent new timing that isn't in the source SRT.** The cue
  start/end times come from the *original* dialogue's timing (or from
  transcription, if generated in Step 1) — translation must fit inside
  that window, not the other way around. If a target-language line
  genuinely cannot fit, tighten the wording (Pass 4 in
  `translation_workflow.md`); don't silently stretch the cue's duration,
  since that desyncs it from what's actually being said on screen.

## Cue count integrity

Every source cue produces exactly one translated cue, in the same
order, with the same timing. Never merge two source cues into one
translated cue (loses one speaker's line or one beat of timing) and
never split one source cue's text across two output cues (there's no
corresponding second source timing to give the split half). If a
target-language sentence structure genuinely wants a different split
than the source, use line breaks *within* the single cue's text, not a
new cue. `validate_srt.py --source original.srt` checks the cue count
matches exactly for this reason.
