# The team — who does what

A real video content team (reels, ads, long-form), mapped to roles the AI plays (or runs as parallel sub-agents).
Each role has inputs, outputs and a "done when" check. Hand-offs are written, not implied:
every role's output lands in the project folder or the spec.

Project folder layout (one per reel or series):
```
<project>/
  brief.md          strategist + audience analyst (also mirrored in spec.brief)
  trends.md         trend researcher — every item dated + sourced
  ideas.json        idea lead (scored with scripts/score_ideas.py) → ideas.md board
  hooks.md          hook writer — 5–10 variants, chosen one marked
  spec.json         the script (scriptwriter, dialect specialist, director, editor, copywriter)
  review.md         reviewer's findings and how each was resolved
  out/              rendered PDF, DOCX, teleprompter, draft SRT
```

---

## 1. Strategist (Head of content)
**Input:** the request, brand file, any reference scripts/videos, past performance.
**Decides:** the job of this reel — goal (awareness / engagement / followers / consideration /
leads / conversions / retention), ONE primary metric, funnel stage, scope (one reel, a series of N,
or a campaign with phases like teaser → launch → proof → urgency), deadline, budget/production
level (phone + talent, studio, AI-generated, faceless).
**Done when:** you can state in one sentence "This reel makes <audience> <feel/do X> so that
<metric> moves", and the user agreed.

## 2. Audience analyst
**Input:** brief, brand, comments/DMs/FAQs if the user has them.
**Produces:** a persona card — who (role, age band, city/country), what they already know,
awareness stage (unaware → problem-aware → solution-aware → product-aware → most-aware), the pain
and the desire in their own words, objections, where they scroll and when, and the **language
they actually speak** (dialect, how much English mixing, formality, Franco/Arabizi in comments).
**Done when:** the persona has at least 3 phrases written the way that audience says them.

## 3. Trend researcher
**Input:** brief, persona, platforms, region, date.
**Produces:** `trends.md` — formats, sounds, memes, news, occasions, competitor reels that are
working *now*, each with source link, date checked, lifecycle stage (emerging / peaking / dying),
fit score for this brand, and rights note for audio. Follow `trends-research.md`.
**Done when:** every item has a date and a source; nothing from memory is presented as current.

## 4. Idea lead (Creative director)
**Input:** brief, persona, trends, content pillars.
**Produces:** 8–15 ideas across angles and formats (`ideation.md`), scored → board of top 3–5 with
a recommendation and why. For series: the series spine, episode list, recurring format/opening.
**Done when:** the user picked one (or delegated).

## 5. Hook writer
**Input:** chosen idea, persona phrases.
**Produces:** 5–10 hooks from ≥4 different hook types (`hooks.md`), each = spoken line + on-screen
text + first visual, ≤ ~3 s to say. Marks the pick and 2–3 A/B alternates.
**Done when:** the first line would stop *this* persona mid-scroll — read it aloud in their dialect.

## 6. Scriptwriter
**Input:** idea, hook, persona, template, brand voice.
**Produces:** the spoken words scene by scene (`scriptwriting.md`): hook → setup/tension → value
beats → payoff → CTA, one idea per scene, short lines, pauses where the talent needs them.
**Done when:** it reads aloud naturally within the target time and every scene earns its seconds.

## 7. Dialect & localization specialist
**Input:** the draft, persona language notes.
**Produces:** the script in the audience's real spoken variety (`languages-dialects.md`) — not a
translation: idioms, rhythm, code-switching and spelling the way that audience writes. For
multi-market campaigns: one adapted version per market (transcreation), not one translation.
**Done when:** no textbook phrasing left; validator dialect warnings resolved or justified.

## 8. Director
**Input:** script, production level, location/talent.
**Produces:** the blue lines — framing, camera movement, B-roll, props, performance notes, visual
pattern changes every 2–4 s, the visual hook, end frame. Founder/executive pieces: full production
brief (location, light, camera, wardrobe, performance) in `sections`.
**Done when:** an editor and a camera operator could shoot it without asking you anything.

## 9. Editor
**Input:** script + director notes, platform specs.
**Produces:** `editor_notes` — cut rhythm, SFX (only on key moments), music bed and its build,
captions style and position (inside safe zones), on-screen text timing (readable: ~0.3 s/word +
0.5 s), transitions, loop ending if used, export specs.
**Done when:** notes cover pace, sound, captions, safe zones and the end frame.

## 10. Copywriter
**Input:** final script.
**Produces:** `posting` — cover text (3–5 words, readable as a thumbnail), caption (hook first
line, value, CTA; keywords people search for), hashtags (few and specific), first comment,
platform title for Shorts (`posting-pack.md`).
**Done when:** caption works for someone who hasn't watched the video.

## 11. Growth analyst
**Input:** posting pack, account history if available.
**Produces:** A/B plan (alternate hooks, trial reels where available), posting time (from the
account's own insights first, else general guidance), the 2–3 metrics to read after 24 h / 7 days
and what each result means for the next reel.
**Done when:** there is a decision rule ("if 3-s hold < X, change the hook, keep the body").

## 11b. Media buyer (ads)
**Input:** brief, placements, budget, past ad results.
**Produces:** placement list and ratios, the slot lengths to cut for, the testing matrix (hooks ×
bodies × CTAs), KPIs (hook rate, hold rate, CTR, CPA/CPL, ROAS) and when to kill or scale a variant
(`ads.md`).
**Done when:** every cutdown maps to a placement and every variant has a reason to exist.

## 11c. Researcher / fact-checker (long-form, ads with claims)
**Input:** script draft.
**Produces:** a source (link + date) for every fact, number, quote and product claim; guest research
for interviews; flags anything unverifiable for removal.
**Done when:** no line states something the team can't show a source for.

## 12. Brand & legal reviewer (independent)
**Input:** spec, rendered PDF, brand file.
**Produces:** `review.md` from `review-checklist.md` — truth of claims, consent, rights (music,
footage, logos, people), platform policy, brand voice, dialect naturalness, accessibility, and
"is it actually interesting?".
**Done when:** every finding is fixed or explicitly accepted by the user.

## 13. Producer
**Input:** approved script.
**Produces:** the hand-off to production skills (`production-handoff.md`) and the shoot list.

---

## Running roles as sub-agents (when the tool supports it)
Give each sub-agent: the brief, the persona, the relevant reference file, and an exact output
format. Good parallel splits: (trend researcher ∥ audience analyst ∥ researcher for long-form) → idea lead → (hook writer ∥
director's visual-hook options) → scriptwriter → (dialect specialist ∥ copywriter) → reviewer.
The reviewer must not be the agent that wrote the script.
