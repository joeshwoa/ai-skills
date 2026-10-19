---
name: media-buying
description: Plans, launches, optimizes and reports paid media on Meta (Facebook/Instagram/WhatsApp), Google Ads (Search, Performance Max, Demand Gen), YouTube, TikTok, Snapchat, LinkedIn, X, Pinterest and Telegram Ads, with sourced per-platform rules, creative specs, policies, tracking and API facts, plus Egypt/MENA realities (payment, WhatsApp-first leads, cash-on-delivery, Ramadan and White Friday). Includes funnel and objective selection, budget and test sizing, creative testing, attribution and conversion tracking setup, optimization decision rules, account-health and ad-rejection recovery, and scripts for CPA/ROAS/break-even/COD math, A/B significance, scaling steps, UTM and naming. Use for any ads question, media plan, budget split, "ليه الإعلان مش بيصرف", rejected ad, disabled ad account, ROAS drop, scaling, reporting.
---

# Media Buying

A decision-rule skill for paid media. Platform facts are in sourced files; arithmetic is done by scripts; judgments follow written rules with their reasoning.

## Load only what the task needs

| Need | Read |
|---|---|
| Rules, specs, policy, tracking, API for one ad platform | `references/platforms/<platform>.md` |
| Choose objectives, structure the funnel, split budget | `references/funnel-and-objectives.md` |
| Pixel, CAPI, UTM, attribution, GA4 mismatch | `references/tracking-and-attribution.md` |
| Plan or read a creative test | `references/creative-testing.md` |
| Bids, budgets, learning phase, pacing | `references/bidding-and-budgets.md` |
| A campaign is under- or over-performing | `references/optimization-playbook.md` |
| Rejected ads, restricted or disabled account | `references/policy-and-account-health.md` |
| Weekly or monthly report | `references/reporting.md` |
| Egypt, KSA, UAE, payment, COD, seasonality | `references/mena-and-egypt-notes.md` |

Ad platform slugs: `meta-ads` `google-ads` `youtube-ads` `tiktok-ads` `snapchat-ads` `linkedin-ads` `x-ads` `pinterest-ads` `telegram-ads`.
Organic content is `social-media-manager`; video scripts and ad creatives scripts are `reels-studio`; strategy and positioning are `marketing-studio`.

## Workflow

1. **Intake**: product and unit economics (price, cost, margin), goal and the one conversion that matters, market, budget and period, existing tracking, existing assets, who owns the ad account, past results. Missing economics means you cannot set a target CPA: compute it (`scripts/ads_math.py breakeven`) or ask.
2. **Targets first.** Break-even CPA/ROAS from margin, adjusted for returns and cash-on-delivery delivery rate. Everything else is judged against this number, not against internet "benchmarks".
3. **Tracking before spend.** A campaign without a verified conversion event and consistent UTMs does not launch (`tracking-and-attribution.md`).
4. **Structure**: fewest campaigns that can each exit the learning phase on the budget available. Budget per variant comes from `scripts/ads_math.py test-size`, not from taste.
5. **Pre-launch checklist** of the platform file (section 13), then creative and policy review.
6. **Operate by rules**: wait out learning, change one thing at a time, cut and scale by the stated steps (`optimization-playbook.md`). Log every change with date and reason (`templates/test-log.md`).
7. **Report** in business terms: spend, revenue or leads, CPA/ROAS vs break-even, what changed, what is next.

## Hard rules

- **No invented benchmarks.** Never present a CPM/CTR/CPA/ROAS "industry average" as fact. If a platform file cites one, repeat its source and date; for Egypt and MENA say reliable benchmarks are scarce and use the account's own history.
- **Platform facts expire.** Check each file's `Last verified` date; items marked `unverified` are to be confirmed in the live ads manager or official help page before acting. Spec and policy rules change often.
- **Never spend money or change a live account without explicit approval** in this conversation: no launching, budget changes, pausing, or uploading creatives unless the user approved that action. Prepare the change list; let the user execute or approve.
- **Do not circumvent policy**: no cloaking, no account-swapping to dodge a ban, no restricted claims disguised, no fake testimonials. Fix the ad, the landing page or the process; appeal through official channels.
- **Do not enter or request payment details, passwords or access tokens** in chat. Use roles/partner access in the ad platform.
- **COD and WhatsApp funnels distort reports.** Platform ROAS counts orders placed; the business earns on delivered orders. Always show both (`ads_math.py cod`).
- Heuristics (scaling steps, budgets per variant, thresholds) are labelled as heuristics with their reasoning; platform rules are labelled with their source.

## Output formats

- **Media plan**: objective, target CPA/ROAS, structure, budget split by funnel stage and platform, audiences, creative plan, tracking plan, risks, calendar (`templates/media-plan.md`).
- **Change list** (for approval): what, where, why, expected effect, rollback condition.
- **Diagnosis**: symptom, ordered checks (tracking, delivery, creative, audience, landing page, economics), finding, fix.
- **Report**: `templates/weekly-report.md`.

## Tools in this skill

`scripts/ads_math.py` (metrics, breakeven, budget, test-size, abtest, scale, pacing, cod), `scripts/utm_builder.py`, `scripts/naming.py` (campaign naming that reports can parse), `templates/`.

## When this skill falls short

If you hit a gap (a missing platform rule, wrong number, uncovered case), finish the task as well as you can, then use the `skill-feedback` skill if installed to record a short non-personal gap report.
