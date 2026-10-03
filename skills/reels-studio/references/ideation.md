# Ideation — from a topic to an idea board

## Content pillars (set once per brand)
3–5 recurring themes the account owns. For an AI-training brand, e.g.: (1) AI news decoded for
non-experts, (2) practical how-tos, (3) myths & mistakes, (4) student stories (real), (5) behind
the scenes / the people. Every idea belongs to a pillar; balance them across a month.

## The angle grid — run a topic through all of these
1. **Myth vs truth** — what does everyone believe that's wrong?
2. **Mistake** — what do beginners do that costs them?
3. **How-to in 30 s** — one concrete win they can try today.
4. **Comparison** — cheap vs expensive, old way vs new way, tool A vs tool B (fair, real test).
5. **Story** — a real moment (yours, a student's with consent) with a turn.
6. **News-jack** — what this week's news means for *them*.
7. **Hot take** — a defensible opinion with a reason.
8. **POV / relatable** — their daily frustration, played for recognition or laughs.
9. **Behind the scenes** — how the work/course/product is really made.
10. **FAQ** — a real question from comments/DMs answered in one reel.
11. **Challenge / experiment** — "I tried X for N days".
12. **Prediction** — where this is going and what to do now.
13. **Audience call-out** — "If you're a lawyer/teacher/marketer, AI changes this for you."
14. **Proof** — a demo, a result, numbers that are true and sourced.

Generate 8–15 ideas from different rows. Each idea: title, pillar, angle, format, hook (draft),
why it fits the persona, trend link (if any, dated), production effort.

## Scoring (0–5 each) — what each number means
- **hook** — 5: a stranger would stop; 3: interesting to followers; 1: needs explanation.
- **audience_fit** — 5: speaks to their exact pain in their words; 3: generally relevant; 1: wrong person.
- **shareability** — 5: they'd send it to a friend/colleague; 3: might save it; 1: neither.
- **trend_timing** — 5: rides something peaking this week or an occasion; 3: evergreen; 1: stale.
- **feasibility** — 5: shoot today with what we have; 3: needs a setup day; 1: needs budget we don't have.
- **brand_fit** — 5: only this brand could say it; 3: on-brand; 1: off-voice or risky.
- **originality** — 5: nobody in the niche has done it; 3: fresh twist; 1: copy of a common reel.

```bash
bash scripts/rs.sh score <project>/ideas.json --md <project>/ideas.md
```
Floors: audience_fit ≥ 3, brand_fit ≥ 2, feasibility ≥ 2 — below that the idea sinks regardless of
score. Show the top 3–5 to the user with one recommendation and why.

## Series design
- A name and a fixed opening ("AI in 30 seconds — episode 4"), same framing/sound cue.
- Each episode works alone; ends pointing to the next.
- Plan 6–10 titles before shooting 1; batch-shoot.

## Campaign design (example: an event or launch)
Phases with dates: teaser (curiosity, no details) → reveal (what/when) → why attend / why enrol
(value) → who it's for (call-outs per persona) → proof/people (founder, speakers, students) →
urgency (last seats, date) → day-of → recap. Different talents per phase is a strength — the
founder for vision, the COO for business value, an instructor for the practical angle, a host for
energy. Same end frame and CTA wording everywhere.
