# Long-form video — minutes, not seconds

YouTube videos, explainers, course lessons, webinars, podcasts/interviews, brand films and
documentaries. Set `brief.content_type: "long_form"`. The validator then gives the hook 10 s
(not 3), widens the runtime tolerance, asks for chapters, flags scenes that run > 3 minutes without
a change, warns about greetings as openers, and checks titles/thumbnails in the posting pack. The
PDF shows an estimated timecode on every scene and the chapter list for the description.

## Packaging first (YouTube)
Decide the **title + thumbnail before writing** — they are the promise the video must keep.
- 3–5 `title_options`: ≤ ~60–70 characters, the searched phrase early, a curiosity gap or a clear
  outcome; no clickbait the video doesn't pay off.
- 2–3 `thumbnail_concepts`: one face with a clear emotion, 2–4 words max (not the title repeated),
  one visual idea, high contrast, readable at phone size.
- The first 30 s confirm the title's promise — viewers who clicked for X and don't see X leave.

## Structure (explainer / essay / tutorial)
| Part | Time | Job |
|---|---|---|
| Cold open | 0–15 s | the most striking moment or result, then the question |
| Promise | 15–45 s | what they'll know/have by the end, why trust you (one line) |
| Chapters | 3–6 sections | one idea each; re-hook at the start of every chapter ("but here's what nobody tells you…") |
| Demo / proof | inside chapters | show, don't tell — screen recordings, real examples |
| Payoff | last 10–15% | the answer/result promised at the start |
| CTA + end screen | last 20 s | one action (subscribe, next video, link); end screen 5–20 s |

Retention devices: open loops ("I'll show you the one exception at the end"), pattern changes every
20–40 s (angle, B-roll, graphic, location), stakes and contrast, cutting every "um", no long intros,
no "before we start, subscribe". Put the CTA after value, not before it.

## Course lesson / training video (e.g. Neo AI programmes)
Hook (why this matters) → learning objectives (2–3, measurable: "build", "compare", "write") →
concept → worked example (screen recording, step by step) → "your turn" exercise → recap (3
points) → next lesson. 6–15 min per lesson; one objective per video beats one long video.
Add `brief.learning_objectives`. Keep facts and tool names current — check them live.

## Webinar / live session
Run-of-show with times: welcome + promise (2 min) → agenda → teaching blocks with interaction
prompts every ~10 min (poll, question, chat prompt) → Q&A → offer → close. Script the opening,
transitions, offer and close word-for-word; bullet the rest.

## Podcast / interview
Answers aren't scripted — **questions, order, timing and follow-ups are**. Use `question` blocks
(host) with `duration_sec` per segment. Research the guest (real, cited), open with the best clip,
ask open questions ("how did…", "what happened when…"), plan 2 follow-ups per key question, end
with a rapid-fire round and where to find the guest. Plan 3–5 short clips for reels from the start.

## Brand film / documentary
Real people, real places. Story arc: world → challenge → turn → what's next. Interview bites carry
the story; narration only where needed; observational footage; music builds to the turn. Put the
creative idea, look and sound in `sections` (like the founder-statement template).

## Writing long scripts aloud
- Spoken rhythm still rules: short sentences, contrast, concrete examples.
- Signpost: "أولاً… تانيًا… تالتًا" / "first… second… finally" — viewers can't re-read.
- Repeat the key idea at the end of each chapter in one line.
- Mark demos with B-roll lines so the editor knows what's on screen while you talk.
- Long scripts for a talent who doesn't memorise: render `--formats teleprompter`.

## Chapters
Set `"chapter": "Name"` on the scene that starts each section. YouTube needs ≥ 3 chapters, the first at
00:00, each ≥ 10 s — the renderer forces the first to 00:00. Timecodes are estimates from speaking
rate and `duration_sec`; re-time them from the final edit before publishing.

## Repurposing
Every long video should yield 3–6 reels/shorts: mark the strongest moments in `editor_notes`, then
run reels mode on each (new hook, 15–45 s, vertical reframe).
