# Deck spec schema

A deck spec is one JSON file that both renderers (`build_deck.py` → editable
`.pptx`, `render_preview.py` → animated `.html`) read, so the two outputs
always match.

```json
{
  "meta_title": "Q3 Board Update",
  "theme": "onyx-gold",
  "brand": "",
  "language": "en",
  "transition": "fade",
  "footer": "Company Name · Confidential",
  "icon_set": "material-symbols",
  "credits": true,
  "slides": [ ... ]
}
```

- `theme`: a theme id from the shared design kit (24 — `bash ../premium-design-kit/scripts/run.sh
  ../premium-design-kit/scripts/kit.py themes --html gallery.html` lists them and writes the gallery),
  or an inline override `{"base": "plain-pro", "primary": "0B6E4F"}`.
- `brand` (optional, only when the user asks): a creative-studio brand slug, a brand.json path or an
  inline brand dict — overrides theme colours, fonts and logo.
- `language`: `ar` → the whole deck is built right-to-left (mirrored layouts, RTL paragraphs and
  tables, Arabic fonts; code stays LTR). Detected automatically from the text when omitted.
  `arabic_style`: modern | corporate | classic | friendly | safe. `heading_font`/`body_font` override.
- `transition`: `fade` | `push` | `wipe` | `cut` (per slide: `"transition"` on the slide).
- `icon_set`: the Iconify family for every icon in the deck (one family = consistent look).
- `credits`: a credits slide is appended automatically when an image licence requires attribution.

### Fields any slide can have
- `"notes"`: speaker notes (string or list of strings → bullet notes).
- `"background"`: an asset ref (photo/art/file) behind the slide, with `"overlay": 0–1` darkening in
  the theme background colour (`"overlay_direction": "full|left|right|bottom"`).
- Asset refs (see premium-design-kit): `"path"`, `{"photo": "english query"}`, `{"stock": "pexels:id"}`,
  `{"icon": "graduation cap"}`, `{"art": "mesh|blobs|geo|waves|dots|grid|stripes|arcs"}`.
- `icon_grid` items, `process` steps and `kpi` metrics take `"icon"`; `team` people take `"photo"`
  (their own photo only); `feature` takes `"image"` (replaces the stat panel; panel_value becomes a badge).

## Slide types

Each entry in `slides` is an object with a `type` plus type-specific fields.
There are **33 types** (21 classic + 12 v2 types at the end of this file) — mix several across one deck instead of leaning on
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

**array_pass** — a picture of a sorted row. Bright cells are still in the window, the accent cell is the middle, dim cells are already out. `L`, `M`, and `R` mark left, mid, and right. One row, or up to three rows in `steps`.
`{"type":"array_pass","title":"Pass 1","values":[8,9,12,130,200,201,600],"left":0,"right":6,"mid":3,"caption":"130 is smaller than 200, so the next window starts at index 4."}`

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


## v2 types (images, native charts, diagrams, teaching)

**image_hero** — full-bleed photo with a gradient on the text side; covers, chapter openers.
`{"type":"image_hero","kicker":"Session 3","title":"Loops in Python","subtitle":"…","image":{"photo":"programming laptop code"},"align":"left|bottom"}`

**image_split** — half photo, half content (`side`: right|left).
`{"type":"image_split","title":"…","text":"…","bullets":[…],"image":{"photo":"…","orientation":"portrait"},"caption":"…"}`

**gallery** — 2–6 images with captions. `{"type":"gallery","title":"…","items":[{"image":{…},"caption":"…"}]}`

**quote_image** — a quote over a darkened photo or art. `{"type":"quote_image","quote":"…","author":"…","image":{…}}`

**chart** — a NATIVE PowerPoint chart (double-click → edit the data). `chart`: bar | column |
stacked | stacked100 | hbar | line | area | pie | donut | scatter | radar. Optional side panel
(`insight`, `insight_label`, `takeaways`), `source`, `highlight` (index), `number_format`
("0%", "#,##0"), `label_format`, `y_min`, `unit` ("%" for pie labels), `labels` (false = none).
`{"type":"chart","title":"Use of funds","chart":"donut","categories":["Product","Growth"],"series":[{"name":"Share","values":[60,40]}],"unit":"%","insight":"…"}`

**diagram** — native-shape diagrams. `kind`: cycle (items, `center`) · pyramid (items[0] = top) ·
funnel (items with `value`) · hierarchy (items[0] = root with `children`, grandchildren as strings)
· venn (2–3 items, `center`) · matrix (4 items, `axes`: [x, y], `highlight` on one item).
`{"type":"diagram","kind":"funnel","title":"…","items":[{"label":"Installs","value":"120k","detail":"…"}]}`

**kpi** — 2–4 metric cards (value, label, `delta`, `good`, `icon`) above an optional native chart.
`{"type":"kpi","title":"Traction","metrics":[{"label":"WAU","value":"18.4k","delta":"+32%","icon":"group"}],"chart":{"chart":"line","categories":[…],"series":[…]}}`

**objectives** — learning objectives as numbered cards, the Bloom verb in the accent colour.
`{"type":"objectives","title":"By the end you can…","items":[{"verb":"Write","text":"a for-loop that prints a times table"}]}`

**definition** — a key term, plain definition, example, common mistake, optional image.
`{"type":"definition","term":"Variable","definition":"…","example":"…","mistake":"…","image":{…}}`

**quiz** — check for understanding, 2–4 options. Make two consecutive slides: the question, then the
same with `"reveal": true` (+ `explanation`). `{"type":"quiz","question":"…","options":["…"],"answer":1}`

**activity** — a hands-on task: icon, minutes, mode (solo/pairs/groups), steps, deliverable.
`{"type":"activity","title":"…","minutes":15,"mode":"pairs","icon":"keyboard","steps":["…"],"deliverable":"…"}`

**credits** — added automatically when needed; `{"type":"credits","lines":["…"]}`.

`code` also takes `"caption"` (a sentence under the code panel).
