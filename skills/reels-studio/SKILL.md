---
name: reels-studio
description: A full video content team (strategist, audience analyst, trend researcher, idea lead, hook writer, scriptwriter, dialect specialist, director, editor, copywriter, media buyer, growth analyst, brand/legal reviewer) that writes shoot-ready video scripts for reels/TikTok/Shorts, ads (Meta, TikTok, YouTube skippable/bumper, TV) with cutdowns and ad copy, and long-form video (YouTube explainers, course lessons, webinars, podcasts, brand films) in ANY language or dialect — Egyptian Arabic as people speak it, Gulf, Levantine, MSA, English… Locks scope and audience first, researches live dated trends, scores ideas and hooks, validates, renders PDF + DOCX in the house style (Neo AI built in) with teleprompter, captions draft and a production hand-off. Use for any request to write, plan or fix a reel, ad, commercial, YouTube video, lesson or podcast script — "اكتب سكريبت ريل/إعلان/فيديو يوتيوب", "عايز أفكار ريلز", "make an ad for X", "write hooks", "what's trending", "content calendar".
---

# Reels Studio — reels, ads and long-form video scripts

One content team for every video length. It never jumps straight to a script: scope and audience
are locked first, trends are checked live and dated, ideas and hooks are generated in volume and
scored, the script is written in the exact language/dialect of the audience, checked by a
validator, rendered in the house script format, and handed to production.

Three content types (set `brief.content_type`) share one workflow and one renderer:
| Type | What | Extra rules (validator) | Read |
|---|---|---|---|
| `reel` (default) | Reels, TikTok, Shorts, Spotlight, LinkedIn video — 7–90 s | hook ≤ 3 s, runtime ±10/25% | `hooks.md`, `platforms.md` |
| `ad` | paid video in any slot: Meta, TikTok, YouTube skippable / non-skippable / bumper, Shorts ads, Snapchat, LinkedIn, TV/CTV/cinema | hook ≤ 3 s, brand in first 5 s, CTA required, slot can't overrun, cutdowns fit their slots, placement limits, ad copy lengths, personal-attribute policy | `ads.md` |
| `long_form` | YouTube videos, explainers, course lessons, webinars, podcasts/interviews, brand films, documentaries | hook ≤ 10 s, no greeting openers, chapters (≥ 3, from 00:00), no 3-min monologue scenes, titles ≤ 100 chars + thumbnail concepts | `long-form.md` |

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
| Strategist | content type, scope, goal, funnel stage, success metric | `intake-scope-audience.md` |
| Audience analyst | persona, awareness stage, language/dialect, objections | `intake-scope-audience.md` |
| Trend researcher | live, dated trends, sounds, formats, news, occasions | `trends-research.md` |
| Idea lead | angles, idea board, series, campaigns | `ideation.md` |
| Hook writer | 3-layer hooks, 5–10 variants | `hooks.md` |
| Scriptwriter + dialect specialist | the words, in the audience's real spoken language | `scriptwriting.md`, `languages-dialects.md`, `long-form.md` |
| Director | visuals, shots, B-roll, ratios, performance notes | `scriptwriting.md` |
| Editor | pacing, cuts, SFX, captions, safe zones, cutdowns | `platforms.md`, `ads.md` |
| Copywriter | cover/thumbnail text, caption, titles, ad copy, hashtags | `posting-pack.md` |
| Media buyer (ads) | placements, testing matrix, KPIs | `ads.md` |
| Researcher / fact-checker (long-form) | sources for every claim, guest research | `long-form.md` |
| Growth analyst | A/B hooks, posting time, metrics to read, iteration | `posting-pack.md` |
| Brand & legal reviewer | claims, rights, consent, ad policy, brand voice, final QA | `review-checklist.md` |
| Producer | hand-off to video/voice/subtitle skills | `production-handoff.md` |

If the AI tool can run sub-agents in parallel, run the Trend researcher and Audience analyst
together, and run the Reviewer as an independent agent that did not write the script. Otherwise
play the roles in order — but never skip one.

## Workflow (gates — don't skip)

**0. Pick the mode.** *Quick* — the user already gave the idea, audience and goal (e.g. "write a
reel saying X for our diploma, same style as these"): go to step 4 after confirming anything
missing in one short message. *Full* — topic or business only: run every step.
*Series/calendar/campaign* — steps 1–3 once, then 4–8 per piece. *Ad set* — one master + cutdowns
+ hook variants. *Long video* — packaging (titles/thumbnail) before the script.

**1. Brief — content type, scope & audience (Strategist + Audience analyst).** Use the question bank in
`references/intake-scope-audience.md`: numbered multiple choice, a RECOMMENDED option each, max 6
questions, pre-fill what's known (brand files, earlier scripts, memory). Lock: content type,
platform(s)/placements, audience (who, where, what they know, the dialect they speak), awareness
stage, goal + one metric, format, length/slot, talent/voice, CTA, scope, deadline, brand rules.
Ads add: placements, ratios, offer facts, brand name. Long-form adds: chapters plan, learning
objectives (lessons), guest (interviews). If the user supplied reference scripts or videos, read them
fully first and copy their structure, tone and document style — the user's own examples beat every
default here. **Do not write a script before this is confirmed.**

**2. Trend scan (Trend researcher).** Search live (web search / browser — TikTok Creative Center,
Instagram & YouTube trending, Google Trends, X, news, the region's occasion calendar, competitors'
outlier videos and their ad libraries) per `references/trends-research.md`. Every trend gets a source
and a `checked` date; anything you couldn't verify today is labelled "unverified" — never present
memory as current. Note audio rights for business accounts. Skip only when the piece isn't
trend-based, and say so.

**3. Ideas (Idea lead).** 8–15 ideas across different angles and formats (`references/ideation.md`),
scored with `scripts/score_ideas.py` → show the top 3–5 as a board with a recommendation.
For long-form, score title + thumbnail concepts together with the idea. User picks (or "you decide").

**4. Hooks (Hook writer).** 5–10 hooks from different hook types in `references/hooks.md`, each as
spoken line + on-screen text + opening visual. Pick the strongest; keep 2–3 as alternates in
`posting.alt_hooks` (ads: 3+, recorded as separate openings).

**5. Script (Scriptwriter, dialect specialist, Director, Editor).**
```bash
bash scripts/rs.sh new --list        # reels, ads and long-form templates
bash scripts/rs.sh new --template ad_pas_master --language ar-EG --brand neoai --out <project>/spec.json
```
Fill every `{{…}}` (schema: `references/spec-schema.md`). Write how the audience speaks
(`references/languages-dialects.md`): Egyptian Arabic is ده/دي/مش/إزاي/عشان/هـ, with English
industry terms kept in English and prefixed الـ when that's how the audience talks — not MSA.
Every scene: what we see (blue, for the editor) and what is said (red, for the talent). One idea
per scene; pattern change every few seconds (reels/ads) or every 20–40 s (long-form); CTA matches
the goal; length fits the target at the language's speaking rate. Ads: write the master so scenes
can stand alone, then define `cutdowns`. Long-form: mark `chapter` on section-opening scenes.

**6. Validate.**
```bash
bash scripts/rs.sh validate <project>/spec.json            # errors must be 0
bash scripts/rs.sh validate <project>/spec.json --strict   # before final delivery: warnings fixed or accepted with the user
```
Then run `references/review-checklist.md` as the Reviewer (a human-judgement pass the script
can't do: is it actually interesting, true, on-brand, legal, policy-safe for ads?).

**7. Render.**
```bash
bash scripts/rs.sh render <project>/spec.json --out <project>/out --formats pdf,docx,teleprompter,production,srt
```
Open the PDF pages as images and look at them before showing the user (alignment, colours,
Arabic shaping, nothing cut off). Deliver PDF + DOCX (the default), say where they are. Long-form
scripts show estimated timecodes and YouTube chapters; ads show the CUTDOWNS and ad copy.
The SRT and timecodes are estimates — real captions/chapters are timed from the edit.

**8. Review round with the user.** Present: the chosen hook + alternates, the script file,
estimated runtime, the posting pack (or ad copy / titles + thumbnails), open micro-choices. Apply
edits to the spec and re-render; never hand-edit the PDF.

**9. Production hand-off (Producer)** — only when the user wants the video made:
`references/production-handoff.md` → flow-studio-director (AI-generated video/ads, reads
`*_for_production.txt`), video-post-studio (shoot edit, captions, colour, sound, ratio exports;
motion-design-studio for graphics, stock-library for b-roll), creative-studio (voice-over incl. Egyptian
Arabic, thumbnails), premium-subtitle-localization (other-language subtitles). If a needed
capability exists in no skill, build it with skill-router's procedure and connect it here.

**10. Learn.** After publishing, ask for the numbers (reels: hold, watch %, shares/saves; ads: hook
rate, hold rate, CTR, CPA/CPL; long-form: CTR on the thumbnail, average view duration, retention
dips) and log what worked to the brand file's `notes` and a usage report (skill-router Part 1 point 6).

## House style (Neo AI and others)
`brands/neoai.json` reproduces the team's existing scripts: A4, Cairo, right-aligned, black
headers, **blue = for the editor** (Visual, SFX, B-roll, on-screen text, supers, notes), **dark red =
what the talent says**, `FOR EDITOR / FOR TALENT` legend, scene headers `SCENE 01 — NAME`, `Pause.`
lines, `END FRAME`, `EDITOR NOTES`. `color_mode: "mono"` gives the all-blue variant (REEL 03/04).
Founder/brand-film briefs (location, camera, wardrobe, music, editing) go in `sections` before the
script. New client → copy `brands/default.json` to `brands/<slug>.json` and change only what
differs (`references/brand-styles.md`); if the client sends their own script format, match it.

## Honest limits
- Trends move daily; the skill researches live but can't see private platform analytics or
  guarantee reach. Algorithm notes are signals reported by the platforms, not secrets.
- Platform slot lengths, character limits and ad policies change — the references say "verify";
  the validator's numbers are as of 2026.
- Speaking-rate runtimes and timecodes are estimates (±15%); time the real read before locking edits.
- The dialect check flags common MSA words in Egyptian scripts; it doesn't judge naturalness —
  a native read-through does. For other dialects the specialist role does it by hand.
- The ad-policy check is a heuristic; the platforms' own review decides.
- No fake testimonials, invented statistics, impersonation or unlicensed music — the reviewer
  blocks them (`references/review-checklist.md`).
