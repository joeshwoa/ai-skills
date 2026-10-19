# Content calendar template
Last updated: 2026-10-19

Copy this table into a Sheet, Notion or Airtable. One row per post per platform. Generate the skeleton with `python3 scripts/calendar_gen.py --start YYYY-MM-DD --weeks 4 --plan instagram:5,facebook:4 --skip <holidays>`; times are placeholders until account insights replace them. Limits: `data/limits/<platform>.json`; rules: `references/platforms/<platform>.md`.

| post_id | date | time | platform | pillar | format | copy | asset | link/UTM | status | owner | approvals |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20261101-instagram-1 | 2026-11-01 | 20:30 | instagram | educate | reel | (final caption) | reel-03.mp4 | https://example.com/p?utm_source=instagram&utm_medium=social&utm_campaign=theme-2026-11&utm_content=reel-03 | planned | name | approver, date |
| | | | | | | | | | | | |

Column rules:
- `post_id`: `YYYYMMDD-platform-slot`, unique, used as the idempotency key in automations (`references/automation-recipes.md` section 5).
- `time`: local audience time with timezone (Africa/Cairo for Egypt).
- `pillar`, `format`: from the strategy (`references/strategy-and-planning.md` sections 3 and 5).
- `copy`: final text only after limits check; keep alt text, hashtags and first comment in the post pack (`post-pack.md`).
- `link/UTM`: build with `python3 scripts/utm.py URL --source <platform> --medium social --campaign <theme-yyyy-mm> --content <format-nn>`.
- `status`: planned, generated, checked, approved, scheduled, published, failed, paused, needs-fix, expired.
- `owner`: the person answering comments and DMs after publishing.
- `approvals`: name, date, version or hash; required before `approved`. No approval, no publishing (SKILL.md hard rules, `references/compliance-and-ethics.md` section 11).
