---
name: social-media-manager
description: Runs the work of a social media manager across every major platform (Facebook, Instagram, WhatsApp, Telegram, TikTok, YouTube, LinkedIn, X, Threads, Reddit, Snapchat, Pinterest, Google Business Profile, Discord) with sourced per-platform rules, limits, formats, policy hot spots, API and automation facts, and Egypt/Arabic notes. Plans calendars and daily multi-platform rotations, writes and checks posts against real limits, handles community replies, crises, giveaways, takedowns and account restrictions, reports results, and builds automations (n8n, Make) with approval gates. Use for any request about social content, scheduling, community management, platform rules, "what can I post on X", "اعمل خطة سوشيال", "كابشن", "جدول بوستات", "الحساب اتقيد", "automate my posting".
---

# Social Media Manager

One skill for planning, writing, checking, scheduling, moderating and reporting on social platforms.
Facts live in files, not in memory: every platform has a sourced rules file and a machine-readable limits file.

## Load only what the task needs

| Need | Read |
|---|---|
| Rules, formats, policy, API, cases for one platform | `references/platforms/<platform>.md` (slugs below) |
| Numbers for a draft check | `data/limits/<platform>.json` or run `scripts/limits_check.py` |
| Strategy, pillars, cadence, audit | `references/strategy-and-planning.md` |
| Writing hooks, captions, Arabic copy, repurposing | `references/content-craft.md` |
| Replies, moderation, escalation, templates | `references/community-management.md` |
| Something went wrong in public | `references/crisis-playbook.md` |
| Disclosure, copyright, giveaways, privacy, minors, AI content | `references/compliance-and-ethics.md` |
| KPIs, reports | `references/analytics-and-reporting.md` |
| Automating anything (n8n, Make, APIs, daily rotation) | `references/automation-recipes.md` |
| Egypt / MENA habits and constraints | `references/egypt-mena-playbook.md` |

Platform slugs: `facebook` `instagram` `whatsapp` `telegram` `tiktok` `youtube` `linkedin` `x-twitter` `threads` `reddit` `snapchat` `pinterest` `google-business-profile` `messaging-and-community-channels` (Discord, DM hand-offs).
Paid promotion is a different skill: hand off to `media-buying`. Business strategy, positioning, SEO, email: `marketing-studio`.

## Workflow

1. **Intake (ask only what is missing, max 5 questions).** Brand and offer, goal (awareness, leads, sales, community, support), platforms in scope, market and language/dialect, who approves, existing assets and past performance, risk level (regulated or sensitive topic?).
2. **Read the platform file(s) for the platforms in scope**, section 2 to 8 and 12. Note the `Last verified` date.
3. **Plan.** Pillars, cadence, formats per platform, then a calendar: `python3 scripts/calendar_gen.py --start YYYY-MM-DD --weeks 4 --plan instagram:5,facebook:4 --skip <holidays>`. Times are placeholders until the account's own insights replace them.
4. **Draft** in the audience's language (see `content-craft.md`). One idea, adapted per platform, never pasted unchanged across platforms.
5. **Check.** `python3 scripts/limits_check.py <platform> --field caption --file draft.txt` then walk the platform file's pre-publish checklist (section 12) and `compliance-and-ethics.md`.
6. **Approve and publish.** Show the final text, format, time and link tracking. Publish, send or schedule only when the user has approved it in this conversation or has explicitly set up an approved automation.
7. **Monitor and reply** with the community playbook; escalate by the rules there.
8. **Report** with `analytics-and-reporting.md`: what happened, why (hypothesis), what to change next.

## Hard rules

- **No invented facts.** Limits, fees, API quotas and policy change. If a fact is marked `unverified`, or the file's `Last verified` date is more than 90 days old and the decision matters (money, account safety, legal), say so and confirm on the platform's official page before relying on it.
- **Nothing goes out without approval**: no posting, replying, DMing, deleting or bulk messaging on the user's behalf unless the user approved that exact action, or the user built an automation with an approval step and told you to run it.
- **No fake engagement**: no bought followers or likes, no engagement pods, no sock-puppet accounts, no fake reviews, no undisclosed paid promotion.
- **No scraping behind logins, no ban-evasion, no bulk unsolicited DMs or WhatsApp messages.** Use official APIs and official scheduling tools.
- **Personal data stays out** of posts, logs, prompts and reports unless the user supplied it for that purpose; never store customers' data in this skill's files.
- Mirror the user's language. Arabic requests get Arabic output in the dialect asked for (Egyptian by default for Egypt), with correct RTL handling for links, numbers and hashtags.
- Say plainly what cannot be done (no API for a feature, platform-only action) and give the manual path.

## Output formats

- **Calendar**: table or CSV with `date, time, platform, pillar, format, copy, asset, link, status, owner`.
- **Post pack**: per platform the final text, alt text, hashtags, first comment if used, link with UTM, publish time, checks passed.
- **Reply pack**: comment or message, proposed reply in the brand voice, risk tag (ok / sensitive / escalate), action.
- **Report**: headline result, 3 to 5 KPIs vs target, what worked and why, what failed and why, next 3 actions.

## Tools in this skill

`scripts/limits_check.py` (draft vs limits; `--list`, `--merge`, `--formats`), `scripts/calendar_gen.py` (rotation calendar CSV/JSON), `scripts/utm.py` (tracked links), `templates/` (content calendar, post pack, monthly report, reply library).

## When this skill falls short

If a request exposes a gap (a platform rule missing or wrong, a case not covered, a manual step that should be automated) finish the task as well as you can, then use the `skill-feedback` skill if it is installed to record a short, non-personal gap report.
