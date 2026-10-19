# Strategy and planning
Purpose: decide what to run, where, how often and why, then review it every quarter. Decision rules, not theory.
Last updated: 2026-10-19

Platform facts (limits, formats, API) live in `platforms/<slug>.md`; this file only decides how to use them. Cadence numbers here are heuristics unless a platform file says official.

## 1. Account audit checklist (run before planning anything)
Score each line: ok / fix / missing. Fix before posting more.
1. Ownership: who is admin on each account, is the owner's login (not the agency's) the root, is two-factor on, are old staff removed. See the "handing over access" case in `platforms/instagram.md` section 10.
2. Handles: same or near-same handle everywhere; Latin handle exists where the platform forces it (Telegram, see `platforms/telegram.md` section 11).
3. Account type: professional/business/creator where the platform needs it for analytics and API (`platforms/instagram.md` section 1).
4. Bio and link: one sentence on what the brand does, for whom, and the one action wanted; link goes to a page that matches the bio; UTM on every link (see `analytics-and-reporting.md` section 6).
5. Verification and official-account marks: apply only where the platform file lists a real eligibility path.
6. Contact paths: WhatsApp or DM, phone, email, support hours stated in the bio or a pinned post.
7. Content inventory: last 30 posts tagged by pillar, format, result; note top 5 and bottom 5 and why (hypothesis, not certainty).
8. Audience: language/dialect mix, city split, device, active hours from the platform's own insights.
9. Community health: unanswered comments and DMs, average first-reply time, number of unresolved complaints.
10. Risk: past strikes/restrictions, copyrighted music in old posts, any undisclosed paid posts, open giveaways with no rules page. Route findings to `compliance-and-ethics.md`.
11. Tools: which schedulers/bots have account access; remove any unofficial tool (`platforms/*.md` section 8 "Forbidden").
12. Competitors/peers: 3 to 5 accounts; note format mix and cadence only, never copy content.

## 2. Goals to metrics map
Pick one primary goal per quarter per account. More than one primary goal means none.
| Goal | Primary metric | Supporting metrics | Typical formats | Stop-doing signal |
|---|---|---|---|---|
| Awareness | non-follower reach or views | follower growth, shares, saves | short video, collaborations, search-friendly content | reach flat for 6 weeks with 3 format tests |
| Engagement/community | meaningful comments, replies, shares per 1,000 reach | return commenters, member posts | questions, polls, UGC, live | engagement only from giveaways |
| Traffic | tracked clicks (UTM) and landing-page sessions | click-through per post, bounce | link-friendly posts, Pins, Stories links, GBP posts | clicks high but landing conversion near zero |
| Leads | form fills, DM conversations opened, WhatsApp starts | qualified rate, cost per lead (time) | lead magnets, comment-to-DM flows, Click-to-chat | leads never qualified by sales |
| Sales | attributed orders/revenue (see attribution limits) | assisted conversions, repeat rate | proof, demos, offers, live selling | revenue only on discount days |
| Support/retention | first-reply time, resolved rate, sentiment | repeat contacts, review rating | pinned FAQs, fast replies, Stories Q&A | rising complaint volume on same issue |
Exact metric names per platform: `platforms/<slug>.md` section 9. Definitions: `analytics-and-reporting.md`.

## 3. Audience and pillar design
Audience, in one paragraph per segment: who, what they want to do after seeing the post, what stops them, where they already spend time (use the platform files' Egypt notes and `egypt-mena-playbook.md` for the mix), which dialect they read.
Pillars: choose 3 to 5. A pillar is a repeatable promise to the audience, not a topic.
- Test each pillar: can you name 20 posts for it, can you measure it, does it map to the goal in section 2?
- Standard set to start from (adapt): Educate (teach one thing), Proof (results, cases, reviews with permission), Behind the scenes (people, process), Offer (product, price, deadline), Community (questions, UGC, replies).
- Ratio default (heuristic): 40 educate/entertain, 20 proof, 20 community, 10 behind the scenes, 10 offer. Move 10 points toward offer only when the goal is sales and the audience is warm.
- One idea per post. Same idea may be adapted across platforms (`content-craft.md` section 4), never pasted unchanged.
- Voice: write 5 do/don't lines (formal or casual, humour allowed, emoji use, dialect, words never used). Save them in the reply library (`../templates/reply-library.md`).

## 4. Cadence by account size and team capacity
Heuristics, not platform rules. Official numeric cadence rarely exists; check each platform file section 4 for what it says.
| Team capacity | Platforms | Weekly output | Rule |
|---|---|---|---|
| 1 person, under 10 h/week | 1 primary + 1 owned channel (WhatsApp/Telegram/GBP) | 3 posts + daily Stories or 1 check | Quality over volume; batch on one day |
| 1 person, 10 to 20 h | 2 primary + GBP/owned | 6 to 8 posts total | One idea becomes 2 formats |
| 2 to 3 people | 3 to 4 platforms | 10 to 15 posts | Named owner per platform; weekly review |
| Agency/team with approvals | 4+ platforms | calendar-driven | Approval SLA 24 h; kill switch owner |
Account size adjustments:
- Under 1,000 followers: reach comes from discovery formats (short video, search, collaborations); spend 60% of time on discovery formats and 40% on replying/commenting on others' relevant posts (by hand, never automated).
- 1,000 to 20,000: keep the best-performing pillar at 40% of output; add one series that repeats weekly.
- Above 20,000: add community roles (moderators, FAQ owner) and a monthly experiment.
Cut rule: if you cannot reply to comments and DMs within the targets in `community-management.md` section 1, reduce posting before reducing replies.
Hard ceilings for scheduled output (API caps, daily limits): never plan above them; run `scripts/limits_check.py` and `scripts/calendar_gen.py`.

## 5. Funnel mapping per platform
Use each file's section 4 funnel list; this table only says which job each platform does by default.
| Platform | Default job | Link-out behaviour | Detail |
|---|---|---|---|
| Facebook | reach + local + Groups + Messenger service | links reduce reach per Meta advice | `platforms/facebook.md` |
| Instagram | awareness (Reels) + consideration (carousels) + DM conversion | no clickable links in captions | `platforms/instagram.md` |
| TikTok | top-of-funnel discovery | profile link | `platforms/tiktok.md` |
| YouTube | search + education + Shorts feeder | description links | `platforms/youtube.md` |
| LinkedIn | B2B trust, recruiting | links allowed, native content preferred | `platforms/linkedin.md` |
| X | real-time voice, public support | links allowed | `platforms/x-twitter.md` |
| Threads | conversation, repurposed text | limited | `platforms/threads.md` |
| Reddit | research, honest Q&A, niche | read the subreddit rules | `platforms/reddit.md` |
| Snapchat | young mobile attention | low link use | `platforms/snapchat.md` |
| Pinterest | evergreen discovery to site | link-out is the point | `platforms/pinterest.md` |
| Google Business Profile | local intent, reviews | calls, directions, website | `platforms/google-business-profile.md` |
| WhatsApp | opted-in conversion and service | chat is the destination | `platforms/whatsapp.md` |
| Telegram | owned broadcast + community | links in posts | `platforms/telegram.md` |
| Discord / DM hand-offs | community, support | invite links | `platforms/messaging-and-community-channels.md` |

## 6. Channel selection and what to skip
Decision rules, in order:
1. Go where the audience already is (Egypt mix: `egypt-mena-playbook.md`, figures are ad reach, not users).
2. Pick the channel your team can reply on. An unattended channel hurts more than a missing one.
3. B2B with a named buyer title: LinkedIn first. Local walk-in business: Google Business Profile and Facebook first. Young consumer product: TikTok/Instagram/Snapchat. Evergreen visual (food, home, fashion, weddings): Pinterest in addition. Developer or niche expert community: Reddit/Discord/X.
4. Add one platform at a time; give it 12 weeks and a defined test before judging.
Skip or defer when:
- the platform's API/automation path is closed and your plan depends on automation (see `automation-recipes.md`);
- the audience is not there and you have no reason to expect it (X and Reddit for a mass-market Egyptian retail brand, per the Egypt figures in their platform files);
- you would have to repost the same file everywhere; repurposing is allowed, copy-paste is not;
- compliance load is high and nobody owns it (financial, health, children's products), until `compliance-and-ethics.md` is applied.

## 7. 30-day launch plan for a new account
Week 0 (days 1 to 3): audit (section 1), pillars (section 3), handle/bio/link, UTM sheet, reply library, approval owner, brand-safety list, tracking sheet.
Week 1 (days 4 to 10): publish 4 to 6 anchor posts per platform (who we are, the problem, proof placeholder, how to buy/contact, FAQ). Follow and engage with 10 relevant accounts per day by hand. Set up pinned post and highlights/collections.
Week 2 (days 11 to 17): start the weekly series; test 2 hooks and 2 formats; reply to every comment within the targets; ask 3 existing customers for permission to use their words.
Week 3 (days 18 to 24): add one collaboration or UGC prompt; run a small, rules-compliant community action (not a giveaway unless `compliance-and-ethics.md` section 4 is done); check first-week insights.
Week 4 (days 25 to 30): review: top 3 posts, bottom 3, reply speed, clicks; keep, kill, and test lists; set next month's calendar with `scripts/calendar_gen.py`; fill `../templates/monthly-report.md`.
Targets for day 30 are relative to the account's own baseline; invent no benchmark.

## 8. Quarterly review
Run once per quarter, 2 hours, with the owner.
1. Goal result vs target (primary metric only first).
2. Pillar table: output share vs result share; cut the bottom pillar or fix its format.
3. Platform table: hours spent vs primary metric; drop or pause one platform if its result is under half of the average and no test is running.
4. Format table: which formats earned reach, which earned action.
5. Community: first-reply time, unresolved items, top 5 recurring questions (turn them into content).
6. Risk log: strikes, restrictions, near misses, crisis drills (`crisis-playbook.md`).
7. Platform file freshness: any platform file with `Last verified` older than 90 days gets re-checked before decisions on money or account safety.
8. Output: 3 decisions (keep / stop / start) with owner and date. No more than 3.

## 9. Pillar worksheet (fill one row per pillar)
| Pillar | Promise to the audience | Goal it serves | 3 example posts | Best formats | Metric | Owner |
|---|---|---|---|---|---|---|
| Educate | "You will learn one useful thing" | awareness | how-to, myth vs fact, checklist | carousel, short video | saves, shares | |
| Proof | "It works, here is evidence" | leads/sales | case, before/after with permission, review | video, image, GBP post | clicks, DMs | |
| Community | "You are heard" | engagement/support | question, poll, reply video, UGC | Stories, replies, live | comments per reach | |
Rules: a result claim needs proof on file; a customer story needs written permission (`compliance-and-ethics.md` section 5).

## 10. Change rules (when to adjust the plan mid-quarter)
- Change a format only after 6 comparable posts; one viral or dead post is noise.
- Change timing only with 4 weeks of the account's own insights; until then slots from `scripts/calendar_gen.py` are placeholders.
- Pause a platform immediately on: restriction notice, API/policy change that breaks the workflow, crisis (see `crisis-playbook.md`), or a missing owner for replies.
- Add volume only after reply targets were met for 4 straight weeks.
- Seasonal peaks (Ramadan, Eid, White Friday, back-to-school): plan 6 to 8 weeks ahead, freeze offers and legal copy 2 weeks ahead, and keep a normal-day reserve post. Calendar logic: `egypt-mena-playbook.md` section 5.

## 11. Sources
- Platform files linked above (each carries its own sources and `Last verified` date).
- Cadence and ratios in sections 3 and 4 are practitioner heuristics (unsourced) unless a platform file says otherwise.
