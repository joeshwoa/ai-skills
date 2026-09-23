# Post-production and delivery

## Assembly

1. Collect each shot's **approved** take (`project_state.py show`).
2. Write `edit.json` (format in `scripts/assemble.py`): clip order with
   in/out trims, narration placements, music bed, platform.
3. `python3 scripts/assemble.py edit.json` — conforms size/fps across
   models, keeps native dialogue, ducks music under narration, normalises
   loudness to the platform target (verified −14.0 LUFS on test).
4. `python3 scripts/qc_clip.py final.mp4 --duration <total> --ratio <r> --expect-audio`
   and watch it end to end before calling it done.

Cutting rules: hard cuts on action by default; dissolves only for time
jumps; trim the first ~0.3 s of generated clips (models often ease in)
and any drift at the tail; 2–4 s per shot on social, longer holds for
emotion.

Colour: clips from Omni and Veo differ slightly — grade them to one look
(shared LUT + per-clip lift/gamma/gain) in the editor if the cut shows it.

Transitions are designed per cut (`transitions.md`) and rendered by
`assemble.py` (dissolves, fades, wipes, J/L cuts, whip assist). Mechanical
fixes to a single clip: `scripts/edit_clip.py` (`editing.md`).

## Captions

Burned-in for 9:16 social (most people watch muted), SRT for YouTube.
Arabic: ≤40 characters per line, 2 lines max, `HH:MM:SS,mmm`, UTF-8.
Captions come from the script text — never re-transcribed from the audio
(see the subtitle skill's lesson: ASR on dialect invents text). Generate
them with `scripts/captions.py` (maps each scripted line through the final
timeline, splits long lines evenly, writes .srt + a styled .ass for
burning).

## Delivery specs

| Platform | Ratio | Resolution | Loudness | Notes |
|---|---|---|---|---|
| Reels / TikTok / Shorts | 9:16 | 1080×1920 | −14 LUFS | keep text out of top ~250 px / bottom ~350 px; hook in 1.5 s |
| YouTube | 16:9 | 1920×1080+ | −14 LUFS | chapters if > 3 min |
| Instagram feed | 4:5 / 1:1 | 1080×1350 / 1080×1080 | −14 LUFS | 4:5 fills more screen |
| Facebook / LinkedIn | 1:1 / 16:9 | 1080×1080 / 1920×1080 | −14 LUFS | captions mandatory |
| Paid ad | 9:16 + 1:1 + 16:9 | as above | −14 LUFS | three reframes from one plan |
| Broadcast | 16:9 | 1920×1080 | −23 LUFS | check the channel's spec |

Flow renders 720p; the assembler scales to delivery size. If Flow offers
an upscale at download, compare its cost against the need (a 9:16 phone
view rarely needs it).

## Variants

Plan 16:9 and 9:16 up front if both are needed — composing for both in
the keyframes is far cheaper than regenerating. Cutdowns (6 s, 15 s) come
from the same approved takes.

## Publish checklist

- continuity across cuts, no drift in faces/wardrobe
- dialogue intelligible, right voices, no stray voices
- captions timed and spelled correctly, inside safe zones
- loudness at target, no clipping
- watermark / commercial terms checked for the user's plan
- AI-disclosure rules for ads or news where required
- rights: no real people without consent, no logos/music the user doesn't own
