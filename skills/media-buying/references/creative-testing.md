# Creative testing
Purpose: plan, run and read creative tests so budget goes to ideas that win, without being fooled by noise.
Last updated: 2026-10-19

Creative specs, safe zones, text limits and platform fatigue rules are in `platforms/*.md` sections 6 and 9; policy limits are in section 8 of each file. Scripts: `scripts/ads_math.py test-size` and `abtest`, `scripts/naming.py`. Thresholds below are **heuristics** with reasons; platform files state their own where they exist. Scripting and production of the video/image assets belong to `reels-studio` and the creative skills; this file covers strategy, testing and reading results.

## 1. Concepts, variations, iterations
| Level | What changes | Example | Test it when |
|---|---|---|---|
| Concept | the core idea: angle, problem, promise, story, format | "price-comparison demo" vs "customer story" vs "founder explainer" | Early, and whenever results plateau; this is where large gains come from |
| Variation | execution of one concept: hook, first 3 seconds, voice, talent, opener | same story, three different hooks | After a concept shows promise |
| Iteration | small edits to a winner: CTA, caption, thumbnail, length, text overlay, music | same ad, shorter by 5 s | To squeeze a winner; expect smaller effects |

Rules:
- Delivery systems reward genuinely different creative; recolors and font swaps are treated as the same ad (`platforms/meta-ads.md` s6, s9). Do not count them as separate variants.
- Test concepts first, hooks second, details last. Reason: effect size shrinks down the list, and small effects need far more data to see (section 7).
- Keep a **concept library**: one row per concept with angle, evidence, status (testing, winner, fatigued, retired), result, and the file name (`templates/creative-brief.md`, `templates/test-log.md`).
- One variable per test. If you change the hook and the offer together, you learn nothing about either.

## 2. Anatomy: hook, body, CTA
- **Hook (first 1-3 seconds or the thumbnail plus first line)**: stops the scroll. Types: problem call-out, result, pattern interrupt, question, social proof, demonstration, curiosity gap. For sound-on video platforms (TikTok, Reels, Snap, Shorts) the hook is visual and verbal; for static it is the image plus headline.
- **Body**: proves the promise in order: problem -> mechanism/solution -> proof (demo, numbers you can substantiate, testimonial that is real and typical) -> objection handling (price, delivery, trust). Keep one message per ad.
- **CTA**: one clear action matching the objective ("Order now", "Send us a message on WhatsApp", "Book a visit"). Buttons must match the destination; misleading buttons are a rejection cause (`policy-and-account-health.md` s2).
- **Offer**: price, discount, bundle, guarantee, delivery terms. Offers change results more than wording; test them as concepts and keep the landing page consistent with the ad (policy risk otherwise).
- Metrics that map to each part: hook -> 3-second view rate (hook rate) and thumb-stop; body -> hold rate / ThruPlay / average watch time; CTA and offer -> CTR (link), landing page views, CVR, CPA. Definitions per platform in each file s10.

## 3. What to test first (order, heuristic)
1. **Offer and angle** (concept): what is the reason to buy now?
2. **Format**: UGC/creator video, product demo, static, carousel, motion graphic, founder talk.
3. **Hook**: 3-5 hooks on the winning concept.
4. **Proof and objection**: testimonial type, guarantee, delivery message, price anchor.
5. **CTA and landing page**: button text, page headline, form length, WhatsApp vs form.
6. **Audience** is a separate test; do not test audience and creative in the same cell. On Meta-style broad delivery, the creative is the targeting.

## 4. How many variants and how much budget
- Variants per test cell (heuristic): 3-5 distinct concepts in a testing ad set when the budget supports it; fewer is better than starved. Reason: each additional variant divides the same events; the platform file's own advice (3-5 creatives per ad set on most files) applies.
- Budget: `python3 scripts/ads_math.py test-size --cpa 100 --variants 3` returns the minimum total (per variant = CPA x events per variant; the script default is 50 events per variant, the same learning-exit scale the Meta file uses). Example: CPA 100 gives 5,000 per variant and 15,000 total for three. Currency is whatever you pass; nothing is converted.
- If the budget cannot reach that, do not pretend to run a CPA test. Options, in order:
  1. Test fewer variants (2).
  2. Optimize and judge on an upstream metric: cost per landing page view, add to cart or lead, hook rate, link CTR. Lower confidence; say so.
  3. Run sequentially (A then B) for the same period, accepting calendar noise (section 7).
  4. Accept directional learning only: pick by upstream metrics, then validate the winner in the real campaign.
- Platform floors: Google's file suggests at least about 10x target CPA per variant per week as a minimum for a directional CPA read (`platforms/google-ads.md` s9 rule 10); TikTok sets daily floors by funnel depth (`platforms/tiktok-ads.md` s5, s9). Those are minimums to see anything, not confirmation of a winner; use `test-size` for confidence.
- Where to run the test: an isolated testing campaign or ad set (so new ads do not reset a scaled ad set's learning; "what not to touch" lists are in the platform files s9). Graduate winners into the scaling campaign as new ads, not by editing live ads.

## 5. Duration and decision rules
- Run a cell for at least a full weekly cycle (7 days) so weekday effects average out, and until each variant has met its minimum spend/events from section 4. Heuristic: do not call a result before 3-4 days even if the numbers look decisive, because early delivery is volatile and learning is not complete (platform wait rules in s9 of each file).
- Do not stop early because a variant "wins" on day 2. Do stop early to cut: a variant with spend above 2-3x target CPA and zero conversions, after tracking is verified (rule in `platforms/meta-ads.md` s9 and `google-ads.md` s9).
- Decision ladder:
  1. Compare on the primary metric chosen **before** launch (write it in `templates/test-log.md`).
  2. Test the difference with `ads_math.py abtest --a-n <impressions or clicks A> --a-x <events A> --b-n <...> --b-x <...>`. Use impressions with clicks for CTR, clicks (or landing page views) with conversions for CVR. It is a two-proportion z-test; "p < 0.05" means likely real, otherwise treat as equal.
  3. If significant and the effect is large enough to matter economically: promote the winner, retire the loser, and record the learning.
  4. If not significant: either keep running (if the budget allows reaching the planned sample) or call it a tie and choose by cost/production effort.
  5. Re-validate the winner once in the live campaign (the test cell is not the production environment).
- Example: 10,000 impressions each, 100 vs 130 link clicks gives p = 0.047, borderline; a re-run or longer run is the sensible move, not a rollout across the account.
- Many comparisons raise false positives: if you compare five variants and pick the best, treat the p-value as optimistic and confirm the winner in a follow-up cell.

## 6. Fatigue signals and refresh cadence
Signals (from the platform files; see `meta-ads.md` s9, `tiktok-ads.md` s9, `google-ads.md` s9):
- Frequency rising, especially in a small audience; CTR or hook rate falling over about a week; CPM rising on a stable audience; CPA rising while landing page CVR is flat; negative comments rising; new-user share falling.
- Distinguish fatigue from tracking, audience, season or landing page problems before blaming creative (`optimization-playbook.md` s3).
Refresh cadence (**heuristic**, reasoning: fatigue speed depends on audience size, spend and format):
- High-spend or small audiences on short-video platforms: expect to add new creative weekly. Mid-spend: every 2-3 weeks. Low-spend broad audiences: monthly or when signals appear.
- Always keep a pipeline: at least 2 new concepts ready before the current best starts to decay; do not wait for the drop.
- Add new ads beside winners instead of editing winners (editing live ads re-triggers review and can reset learning; platform files s9).
- Ramadan and White Friday: refresh weekly and prepare spares because review queues and fatigue both speed up (`mena-and-egypt-notes.md` s7).
- Retire only clear losers; a fatigued winner can return after a rest or with a new hook.

## 7. Reading results without fooling yourself
- **Novelty effect**: a new ad often gets a delivery boost or curiosity clicks in the first days. Judge after the early period and re-check at day 7+.
- **Spend skew**: delivery systems give most spend to one ad early; the favored ad is not proven better, it was just given more chances, and low-spend ads have too few events to judge. Equalize spend (separate ad sets or a platform A/B tool) when a clean comparison matters, or compare on rates with enough sample per variant.
- **Small samples**: 3 conversions vs 5 is noise. Use the sample thresholds in section 4 and `abtest`.
- **Different audiences per ad**: when delivery chooses audiences, the same ad can look better simply because it reached easier people. Compare within the same ad set/campaign.
- **Day-of-week, paydays, events**: Egypt payday patterns and season events shift conversion rates; run both variants simultaneously, not one after the other.
- **Attribution lag**: recent conversions arrive later; compare mature windows (see `tracking-and-attribution.md` s4).
- **Surrogate metrics**: high CTR or view rate can come from curiosity bait that sells nothing. Always confirm with CVR/CPA or qualified leads. For COD, confirm with delivered orders (`tracking-and-attribution.md` s6).
- **Peeking and stopping on a good day**: set the end condition up front.
- **Survivorship**: log losers too; a concept's second test often regresses toward average.
- **Confounders**: price, stock, landing page edits or a promo during the test void the result. Log them.

## 8. UGC and creator creative
- Authentic, phone-shot, first-person content often fits short-video feeds (practitioner observation; no sourced benchmark). Treat it as a concept to test, not a guarantee.
- Briefing: problem, one promise, three must-say points, forbidden claims, 3 hook options to film, length, aspect ratios, language/dialect, deliverables with raw files, usage rights and duration (`templates/creative-brief.md`).
- Rights: contract for organic and paid usage, whitelisting/partnership access, exclusivity, disclosure language (`mena-and-egypt-notes.md` s9). Use the platform partnership tools (Meta partnership ads, TikTok Spark Ads; see platform files).
- Vet creators for audience country, authenticity and prior brand issues; require native analytics screenshots.
- Disclose paid partnerships clearly; do not fabricate testimonials or let creators claim results the product cannot substantiate (`policy-and-account-health.md` s2).
- AI-generated or significantly AI-edited media: some platforms require disclosure (TikTok in `tiktok-ads.md` s8); never use a public figure's likeness without permission.

## 9. Arabic and RTL cautions
(Full list: `mena-and-egypt-notes.md` s4; Meta specifics in `meta-ads.md` s6.)
- One dialect per ad: Egyptian Arabic for Egypt consumer ads, Khaleeji for Gulf consumer ads, MSA for formal, finance, health or multi-country copy. A native speaker approves every ad; machine translation reads formal and can change meaning.
- Mixed text direction: Arabic with Latin brand names, numbers, URLs or hashtags can reorder punctuation. Preview every placement on iOS and Android. Prefer Latin terms mid-sentence with Arabic punctuation inside the Arabic run.
- Numbers and currency: one numeral system per ad (Western or Arabic-Indic), a clear currency token (EGP / ج.م, SAR, AED) and prices identical to the landing page.
- Captions and overlays: use fonts with full Arabic shaping, readable size, and platform safe zones (Stories/Reels/TikTok UI covers top and bottom). Check auto-rendered Arabic text for broken letter joining; never ship it without a native review.
- Layout: mirror arrows, swipe direction and carousel order for RTL where the platform does not.
- Cultural: respectful treatment of religious references; avoid mixing sacred content with hard sell; dress and imagery norms vary by country.
- Keep Arabic and English versions as separate ads with separate IDs so results are not blended.

## 10. Naming and logging
- Use `scripts/naming.py` so reports can parse the ad name:
```
python3 scripts/naming.py build --level ad --brand acme --objective sales --platform meta --market eg --period 2026-11 --offer whiteFriday --audience broad --placement advplus --budgettype cbo --concept ugc-hook3 --format 9x16 --version v2
```
  returns `acme_sales_meta_eg_2026-11_whiteFriday|broad_advplus_cbo|ugc-hook3_9x16_v2`. The script rejects non-ASCII (transliterate Arabic). `python3 scripts/naming.py parse "<name>"` validates an existing name.
- Concept IDs: `<angle>-<hook#>` (for example `ugc-hook3`), format as ratio (`9x16`), version `v1`, `v2`.
- Every test gets a row in `templates/test-log.md`: hypothesis, variable, cells, primary metric, sample plan, start/end, result, decision, learning.
- Brief before production: `templates/creative-brief.md`. Review for policy risk (`policy-and-account-health.md` s2) and specs (platform file s6) before upload.

## 11. Test protocol (summary for an agent)
1. Hypothesis: "Changing X to Y will improve metric M by at least Z because R."
2. Choose cells (2-5) and the one variable. Confirm production readiness and policy check.
3. Size: `test-size`; decide the primary metric and end date before launch.
4. Launch in an isolated test ad set/campaign with identical audience, budget logic and landing page; no other changes.
5. Do not touch for the minimum duration (platform file s9 "what not to touch").
6. Read with `abtest` and the pitfalls list; write the decision and the learning in the test log.
7. Promote winners via new ads in the scaling campaign; queue the next test (the learning suggests it).
8. Get user approval before any launch or spend change (SKILL.md hard rule).

## Sources
- Platform files (dated 2026-10-19, with their own sources): `platforms/meta-ads.md` s6, s9, `platforms/tiktok-ads.md` s9, `platforms/google-ads.md` s9, plus `mena-and-egypt-notes.md` s4, s7, s9.
- Test-statistics approach: `scripts/ads_math.py abtest` implements a two-proportion z-test; no external benchmark is cited. Refresh cadence and variant counts are heuristics.
