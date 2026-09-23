# Script analysis — reading the client's script before anything else

A finished video can only be as right as the reading of the script it
came from. Most "the client didn't like it" outcomes trace back to an
assumption made in the first hour: who the characters are, what a line
meant, how long it runs, what the product must look like. So the script is
analysed twice, mechanically and then editorially, and the client signs off
on our interpretation before any character or shot exists (gate `script`).

## Pass 1 — mechanical (script_breakdown.py)

```bash
python3 scripts/script_breakdown.py client_script.docx --out breakdown \
    --target-seconds 60 --ratio 9:16
```

Gives facts, not opinions: scenes (location, INT/EXT, time of day),
characters (lines, words, scenes, ages and first descriptions found in
the action lines), every line with word count and spoken seconds,
narration (V.O.), off-screen lines (O.S.), SFX, music and on-screen text
cues, transitions written in the script, production risks per scene
(crowds, fast action, text in frame, hands, fluids, animals, mirrors,
device screens), runtime estimate vs target, name typos, dialect mixing,
and a first list of client questions. Also writes `plan_skeleton.json` —
a first cut of the shot list with every line fitted into clip-sized
windows. The skeleton is a starting point, never a plan: every shot in it
is marked `routing_reviewed: false` until the director routes it.

If the parser misreads the format (it prints what it found), fix the
input — convert to one `Name: line` per line — rather than trusting a bad
breakdown.

## Pass 2 — editorial (the agent, reading as director + writer)

Work through these in order and write the answers down; they become the
**Script interpretation** the client approves.

1. **Purpose.** What must the viewer know, feel or do at the end? One
   sentence. If the script doesn't make it clear, that's question #1.
2. **Audience & platform.** Who watches, where, with sound or muted,
   vertical or horizontal. Does the script's pacing fit (a 60 s ad with a
   15 s intro fails on Reels)?
3. **Structure.** Hook (first 1.5 s) → setup → turn → payoff → CTA. Mark
   where each happens. Missing hook or CTA → propose one, don't silently add.
4. **Every line's intent.** For each line: what it says, what it means
   (subtext), what the performance should be. Jokes: where the laugh is and
   what makes it land. Flag any line whose meaning is ambiguous.
5. **Characters.** Who they are, their relationship, their arc across the
   piece, how each speaks (dialect, register, pace). Anything the script
   says about looks, age, wardrobe is binding; everything else is a
   proposal the client must approve.
6. **World.** Each location as it must look; props that matter; brand
   and product requirements (exact packaging, colours, logo usage).
7. **Continuity map.** What must stay the same across scenes (wardrobe,
   props in hand, time of day, weather) and what deliberately changes.
8. **Sound.** Which lines are on-screen dialogue (native generation) and
   which are narration (external voice-over); SFX and music cues; places
   where silence matters.
9. **On-screen text.** Every title, super, CTA, price — exact wording,
   language, where and how long. Made in post or in a keyframe, never by
   the video model.
10. **Runtime.** Estimated vs target. If over: propose specific cuts
    (which lines, which shots) — never speed up dialogue to fit.
11. **Feasibility with AI video.** For each risk the breakdown flagged:
    how we will shoot around it (framing, splitting, post), or what we
    need to tell the client up front (e.g. "a crowd will read as a soft
    background, not individual faces").
12. **Rights and sensitivities.** Real people, brands, music, children,
    religious or political content, claims that need substantiation.

## The questions for the client

Merge the breakdown's questions with the editorial ones. Group them, keep
them answerable in one line each, offer a recommended answer for each
("Scene 3 time of day? — recommended: golden hour, it matches the product
warmth"). Never ask what the script already answers.

## The sign-off document (gate `script`)

Send the client one short document:
- the logline and purpose as we understood them,
- scene-by-scene summary with runtime,
- the cast list with our proposed look for each character,
- narration/voice decisions, on-screen text list,
- anything we will change or cut and why, known AI limits,
- the questions (with recommended answers).

When the client confirms (or answers), record it:
`project_state.py gate script approve --by user --note "client confirmed v2"`.
Only now does character building start.
