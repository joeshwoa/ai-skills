---
name: reels-studio
description: A full short-form video content team (strategist, audience analyst, trend researcher, idea lead, hook writer, scriptwriter, dialect specialist, director, editor, copywriter, growth analyst, brand/legal reviewer) that turns a topic, product or "we need reels" into shoot-ready reel scripts in ANY language or dialect — Egyptian Arabic as people really speak it, Gulf, Levantine, Maghrebi, MSA, English, French… Locks scope and audience first, researches live dated trends, scores ideas, writes hook variants, then a validated scene-by-scene script for the editor and talent plus a posting pack, rendered as PDF + DOCX in the user's house style (Neo AI built in), with teleprompter text, draft captions and a production hand-off. Use for any request to write, plan, brainstorm or fix a Reel, TikTok, YouTube Short or other short vertical video — "اكتب سكريبت ريل", "عايز أفكار ريلز", "make a reel about X", "what's trending", "write hooks", "reels content calendar" — even when no platform is named.
---

# Reels Studio

A whole short-form content team in one skill. It never jumps straight to a script: scope and
audience are locked first, trends are checked live and dated, ideas and hooks are generated in
volume and scored, the script is written in the exact language/dialect of the audience, checked
by a validator, rendered in the house script format, and handed to production.

Paths below are relative to this skill's folder (`skills/reels-studio/` in the ai-skills repo).

## Setup (once)
```bash
bash scripts/setup.sh            # python-docx if missing, reports which PDF engine exists
bash scripts/setup.sh --fonts    # optional: install Cairo so the DOCX shows the house font
bash scripts/selftest.sh         # proves everything works here
```
PDF needs one of: Google Chrome/Chromium/Edge/Brave, Playwright Chromium, or LibreOffice.

## The team (read `references/team.md` for each role's checklist)
| Role | Owns | Reference |
|---|---|---|
| Strategist | scope, goal, funnel stage, success metric | `intake-scope-audience.md` |
| Audience analyst | persona, awareness stage, language/dialect, objections | `intake-scope-audience.md` |
| Trend researcher | live, dated trends, sounds, formats, news, occasions | `trends-research.md` |
| Idea lead | angles, idea board, series | `ideation.md` |
| Hook writer | 3-layer hooks, 5–10 variants | `hooks.md` |
| Scriptwriter + dialect specialist | the words, in the audience's real spoken language | `scriptwriting.md`, `languages-dialects.md` |
| Director | visuals, shots, B-roll, performance notes | `scriptwriting.md` |
| Editor | pacing, cuts, SFX, captions, safe zones | `platforms.md` |
| Copywriter | cover text, caption, hashtags, first comment | `posting-pack.md` |
| Growth analyst | A/B hooks, posting time, metrics to watch, iteration | `posting-pack.md` |
| Brand & legal reviewer | claims, rights, consent, brand voice, final QA | `review-checklist.md` |
| Producer | hand-off to video/voice/subtitle skills | `production-handoff.md` |

If the AI tool can run sub-agents in parallel, run the Trend researcher and Audience analyst
together, and run the Reviewer as an independent agent that did not write the script. Otherwise
play the roles in order — but never skip one.

## Workflow (gates — don't skip)

**0. Pick the mode.** *Quick* — the user already gave the idea, audience and goal (e.g. "write a
reel saying X for our diploma, same style as these"): go to step 4 after confirming anything
missing in one short message. *Full* — topic or business only: run every step. *Series/calendar* —
steps 1–3 once, then 4–8 per episode.

**1. Brief — scope & audience (Strategist + Audience analyst).** Use the question bank in
`references/intake-scope-audience.md`: numbered multiple choice, a RECOMMENDED option each, max 6
questions, pre-fill what's known (brand files, earlier scripts, memory). Lock: platform(s),
audience (who, where, what they know, the dialect they speak), awareness stage, goal + one metric,
format, length, talent/voice, CTA, scope (one reel / series / campaign), deadline, brand rules.
If the user supplied reference scripts or videos, read them fully first and copy their structure,
tone and document style — the user's own examples beat every default here. Write the answers
into the spec's `brief`. **Do not write a script before this is confirmed.**

**2. Trend scan (Trend researcher).** Search live (web search / browser — TikTok Creative Center,
Instagram & YouTube trending, Google Trends, X, news, the region's occasion calendar) per
`references/trends-research.md`. Every trend gets a source and a `checked` date; anything you
couldn't verify today is labelled "unverified" — never present memory as current. Note audio
rights for business accounts. Skip only in Quick mode when the user's idea is not trend-based,
and say so.

**3. Ideas (Idea lead).** 8–15 ideas across different angles and formats (`references/ideation.md`),
scored with `scripts/score_ideas.py` → show the top 3–5 as a board with a recommendation.
User picks (or "you decide").

**4. Hooks (Hook writer).** For the chosen idea write 5–10 hooks from different hook types in
`references/hooks.md`, each as spoken line + on-screen text + opening visual. Pick the strongest
for the script; keep 2–3 as A/B alternates in `posting.alt_hooks`.

**5. Script (Scriptwriter, dialect specialist, Director, Editor).**
```bash
bash scripts/rs.sh new --list
bash scripts/rs.sh new --template talking_head --language ar-EG --brand neoai --out <project>/spec.json
```
Fill every `{{…}}` (schema: `references/spec-schema.md`). Write how the audience speaks
(`references/languages-dialects.md`): Egyptian Arabic is ده/دي/مش/إزاي/عشان/هـ, with English
industry terms kept in English and prefixed الـ when that's how the audience talks — not MSA.
Every scene: what we see (blue, for the editor) and what is said (red, for the talent). Hook
lands in the first 3 s; one idea per scene; pattern change every few seconds; CTA matches the
goal; length fits the target at the language's speaking rate.

**6. Validate.**
```bash
bash scripts/rs.sh validate <project>/spec.json            # errors must be 0
bash scripts/rs.sh validate <project>/spec.json --strict   # before final delivery: warnings fixed or accepted with the user
```
Then run `references/review-checklist.md` as the Reviewer (a human-judgement pass the script
can't do: is it actually interesting, true, on-brand, legal?).

**7. Render.**
```bash
bash scripts/rs.sh render <project>/spec.json --out <project>/out --formats pdf,docx,teleprompter,srt
```
Open the PDF pages as images and look at them before showing the user (alignment, colours,
Arabic shaping, nothing cut off). Deliver PDF + DOCX (the default), say where they are.
The SRT is an estimate for planning only — real captions are timed from the recording.

**8. Review round with the user.** Present: the chosen hook + 2 alternates, the script file,
estimated runtime, the posting pack, open micro-choices. Apply edits to the spec and re-render;
never hand-edit the PDF.

**9. Production hand-off (Producer)** — only when the user wants the video made:
`references/production-handoff.md` → flow-studio-director (AI-generated video, reads the script
PDF/DOCX), creative-studio (voice-over incl. Egyptian Arabic, captions, edit, cover, thumbnails),
premium-subtitle-localization (other-language versions). If a needed capability exists in no
skill, build it with skill-router's procedure and connect it here.

**10. Learn.** After posting, ask for the numbers (views, 3-s hold, average watch time, completion,
shares/sends, saves, follows, link clicks) and log what worked to the brand file's notes and a
usage report (skill-router Part 1 point 6).

## House style (Neo AI and others)
`brands/neoai.json` reproduces the team's existing scripts: A4, Cairo, right-aligned, black
headers, **blue = for the editor** (Visual, SFX, B-roll, on-screen text, notes), **dark red = what
the talent says**, `FOR EDITOR / FOR TALENT` legend, scene headers `SCENE 01 — NAME`, `Pause.`
lines, `END FRAME`, `EDITOR NOTES`. `color_mode: "mono"` gives the all-blue variant (REEL 03/04).
Founder-style briefs (location, camera, wardrobe, music, editing) go in `sections` before the
script. New client → copy `brands/default.json` to `brands/<slug>.json` and change only what
differs (`references/brand-styles.md`); if the client sends their own script format, match it.

## Honest limits
- Trends move daily; the skill researches live but can't see private platform analytics or
  guarantee reach. Algorithm notes are signals reported by the platforms, not secrets.
- Speaking-rate runtimes are estimates (±15%); time the real read before locking edits.
- The dialect check flags common MSA words in Egyptian scripts; it doesn't judge naturalness —
  a native read-through does. For other dialects the specialist role does it by hand.
- No fake testimonials, invented statistics, impersonation or unlicensed music — the reviewer
  blocks them (`references/review-checklist.md`).
