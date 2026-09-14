# Deck spec schema

A deck spec is one JSON file that both renderers (`build_deck.py` → editable
`.pptx`, `render_preview.py` → animated `.html`) read, so the two outputs
always match.

```json
{
  "meta_title": "Q3 Board Update",
  "theme": "onyx-gold",
  "transition": "fade",
  "footer": "Company Name · Confidential",
  "slides": [ ... ]
}
```

- `theme`: one of the ids in `scripts/themes.py` — 16 available: `onyx-gold`,
  `arctic-minimal`, `sunset-startup`, `sage-editorial`, `cobalt-tech`,
  `ivory-luxe`, `midnight-violet`, `crimson-editorial`, `mint-fresh`,
  `graphite-mono`, `blush-luxury`, `forest-corporate`, `azure-finance`,
  `amber-warmth`, `neon-pulse`, `slate-professional`. Render
  `scripts/themes.py`'s `build_theme_gallery_html()` to preview all of them
  before asking the user to pick.
- `transition`: `fade` | `push` | `wipe` | `cut`. Applied to every slide.

## Slide types

Each entry in `slides` is an object with a `type` plus type-specific fields.
There are **21 types** — mix several across one deck instead of leaning on
just `bullets`/`title`/`closing`; real variety between slides is what makes a
deck read as designed rather than templated.

**title** — opening slide.
`{"type":"title","kicker":"SERIES B","title":"Cominde","subtitle":"AI-native mobile apps, shipped in weeks not quarters"}`

**section** — big number + short title, used as a chapter divider.
`{"type":"section","number":"01","title":"The problem"}`

**bullets** — a titled list. Each bullet can be a plain string, or
`{"point": "...", "detail": "..."}` for a bold headline + smaller supporting
line (use this for "so what" explanations, not just raw facts).
`{"type":"bullets","title":"Why now","bullets":[{"point":"On-device models crossed the quality bar","detail":"Sub-1B models now match GPT-3.5-class output for narrow tasks"}]}`

**stats** — a row of KPI numbers.
`{"type":"stats","title":"Traction","stats":[{"value":"42%","label":"MoM revenue growth"},{"value":"180+","label":"Paying teams"}]}`

**quote** — a pull-quote slide (customer testimonial, mission statement).
`{"type":"quote","quote":"This cut our release cycle from 6 weeks to 4 days.","attribution":"Head of Product, Acme Co."}`

**table** — a data table.
`{"type":"table","title":"Pricing","headers":["Plan","Price","Seats"],"rows":[["Starter","$0","1"],["Team","$49/mo","10"]]}`

**closing** — final slide (thank-you / contact).
`{"type":"closing","title":"Let's talk","contact":"founders@cominde.dev"}`

**agenda** — a numbered outline/table-of-contents, airier than `bullets`.
`{"type":"agenda","title":"Agenda","items":["The problem","Our approach","Traction so far","Team","The ask"]}`

**two_column** — two independent plain-text lists side by side (problem/
solution, before/after, current-state/future-state).
`{"type":"two_column","title":"Old way vs new way","left_heading":"Manual counting","left_items":["3 days per cycle count","Aisles closed during counts"],"right_heading":"Aurora drones","right_items":["45 minutes per cycle count","Zero downtime"]}`

**comparison** — two labeled cards for a direct A/B, more visually distinct
than `two_column` (each side gets its own colored header strip and panel).
`{"type":"comparison","title":"Aurora vs. legacy RFID","left_label":"Legacy RFID","left_points":["$180k hardware install","6 month deployment"],"right_label":"Aurora","right_points":["$0 hardware install","2 week deployment"]}`

**timeline** — a horizontal chronological line with milestones (roadmap,
history, launch schedule).
`{"type":"timeline","title":"Roadmap","milestones":[{"label":"Q4 2026","text":"GA launch"},{"label":"Q1 2027","text":"EU expansion"}]}`

**process** — numbered circles for a how-it-works / step-by-step flow.
Distinct from `timeline`: steps, not dates.
`{"type":"process","title":"How it works","steps":[{"number":1,"label":"Deploy","detail":"Drones self-map the warehouse overnight"},{"number":2,"label":"Scan","detail":"Autonomous nightly inventory flights"}]}`

**big_statement** — one huge, unavoidable line (a milestone number, a
mission statement). Use sparingly, once or twice a deck.
`{"type":"big_statement","statement":"We cut inventory count time by 94%","support":"Measured across 12 pilot warehouses, Q2–Q3 2026"}`

**team** — a grid of people. Initials in a colored circle stand in for
headshots — this skill never fabricates photos of real people.
`{"type":"team","title":"Team","people":[{"name":"Dana Osei","role":"CEO, ex-Amazon Robotics"},{"name":"Marcus Lin","role":"CTO, ex-Boston Dynamics"}]}`

**feature** — text + bullets on the left, a stat callout panel on the
right. Reach for this when a slide "needs an image": a real number in a
styled panel reads as more premium than a stock photo, and this skill never
fabricates a fake one.
`{"type":"feature","title":"Built for scale","description":"Aurora's fleet manager coordinates up to 200 drones across a single site with zero manual routing.","bullets":["Auto-charging dock network","Collision-avoidance mesh"],"panel_label":"Fleet uptime","panel_value":"99.7%","panel_caption":"Trailing 90 days, all pilot sites"}`

**icon_grid** — a grid (up to ~6) of feature callouts, each with a glyph
circle, bold label, and short description. For "what we offer" / "key
capabilities" — reads as far less flat than a `bullets` list.
`{"type":"icon_grid","title":"Platform capabilities","items":[{"glyph":"AM","label":"Auto-mapping","description":"Drones self-map new warehouse layouts on first flight."}]}`

**pricing** — 2-4 pricing-tier cards side by side, one optionally
highlighted as the recommended plan (`"highlight": true`).
`{"type":"pricing","title":"Pricing","tiers":[{"name":"Growth","price":"$4,900","period":"mo","highlight":true,"features":["Up to 5 sites","Unlimited drones","Priority support"]}]}`

**faq** — a short Q&A list (keep to ~3-4 pairs so each answer has room to
breathe; the validator will flag it if the copy runs long).
`{"type":"faq","title":"Questions investors ask","items":[{"question":"What happens if a drone loses connectivity?","answer":"It completes a safe-return-to-dock routine and resumes on its next flight."}]}`

**chart_bar** — a real, native, editable bar chart (rectangles, not a
picture) for a small series of numbers — revenue, growth, a metric over
time. `"display"` is optional formatted text shown above the bar (e.g.
`"$410k"`); falls back to the raw `"value"` if omitted.
`{"type":"chart_bar","title":"ARR growth","bars":[{"label":"Q4 2025","value":180,"display":"$180k"},{"label":"Q1 2026","value":410,"display":"$410k"}]}`

**logo_wall** — a grid of partner/client names as styled text badges.
This skill never fabricates a company's actual logo artwork, so use this
for a "trusted by" slide instead of inventing logo images.
`{"type":"logo_wall","title":"Piloting with","logos":["Meridian Logistics","Coldpoint Storage","Harbor Fulfillment"]}`

**vertical_timeline** — a top-to-bottom milestone list. Reach for this
instead of `timeline` when there are more than ~4 milestones, or each one
needs a real supporting sentence rather than one short line.
`{"type":"vertical_timeline","title":"How we got here","milestones":[{"label":"2024","text":"Two ex-warehouse-robotics engineers prototype the first auto-charging dock in a garage."}]}`

## Filling with real data, not placeholders

The whole point of this skill is that a finished deck should never say
"Lorem ipsum" or "Company X" unless the user explicitly asked for a blank
template. Before writing the deck spec:

1. Pull real numbers from whatever the user gave you (a doc, a spreadsheet,
   a pasted email, prior conversation context) or from live research
   (web search, a connected data source) if the task calls for current
   facts you don't already have.
2. If a number or fact genuinely isn't available, don't invent one — write
   a bracketed placeholder like `[REVENUE FIGURE NEEDED]` so it's obviously
   not a real value someone could mistake for data, and flag it to the user
   instead of silently making something up.
3. Only produce a deliberately generic/blank version when the user asks for
   "just a template" — see SKILL.md.
