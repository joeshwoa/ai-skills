---
name: premium-presentations
description: >
  Build fully editable, agency-quality presentations — real .pptx (every title, bullet, table cell
  and chart is native and editable) plus an animated HTML version — in English or Arabic (full
  right-to-left), with real photos from free stock, icons, generated art, native PowerPoint charts,
  diagrams (cycle, funnel, pyramid, hierarchy, venn, matrix), KPI dashboards, teaching slides
  (objectives, definitions, quizzes with reveal, activities), speaker notes, brand kits and 24 themes.
  Use whenever the user asks for a presentation, slide deck, pitch/investor/sales deck, PowerPoint,
  Keynote, lecture or lesson slides, or "make me slides about X" — even without the word
  "professional". If no visual style is given, ask before building. For documents use
  premium-documents, for spreadsheets premium-spreadsheets, for a whole course course-studio.
---

# Premium Presentations

A presentation studio: strategist, writer, art director, data designer, photo editor and QA, on
the shared design kit (`../premium-design-kit`). Output: an editable `.pptx` (PowerPoint, Keynote,
Google Slides) + an animated `.html` (present in a browser, send as one file) + a PDF on request.

## Setup
`bash ../premium-design-kit/scripts/setup.sh` once (Python deps). Run every script through
`R="bash ../premium-design-kit/scripts/run.sh"`. Stock photos/icons need the user's studio-mcp
(creative-studio bootstrap); without it decks still build with generated art.

## The team and the gates
| Role | Does |
|---|---|
| Strategist | purpose, audience, the ONE message, story arc, slide count |
| Writer | headlines that say the point ("Prep time fell 40%"), point/detail bullets, speaker notes |
| Art director | theme or brand, cover style, image direction, icon family, variety of slide types |
| Data designer | native charts with the takeaway highlighted, KPI cards, true numbers + sources |
| Photo editor | stock searches (English, concrete), picks from the contact sheet, credits |
| QA | validator, page images, contrast, RTL, story read-through |

1. **Brief (ask once, briefly)** — purpose & audience · language (Arabic → RTL deck) · length/time ·
   style: show the gallery (`$R ../premium-design-kit/scripts/kit.py themes --html gallery.html`) and
   recommend one; brand only if the user asks (`"brand": "<slug>"`) · content source (their doc/data,
   or research) · outputs (pptx + html default; PDF?). Default sensible answers; don't interrogate.
2. **Story** — write the arc as slide headlines first (one line each). Check: does it flow if you
   read only the headlines? Pick the slide TYPE that matches each point (see the patterns in
   `../premium-design-kit/references/design-system.md`). Never more than 2 `bullets` slides in a row.
3. **Content with real data** — numbers from the user/research; gaps as `[NEEDS: …]` and flagged.
4. **Assets** — photos: `{"photo": "concrete english query"}`; LOOK at the printed contact sheet and
   pin better picks with `{"stock": "<id>"}`. Icons: one family (`icon_set`). Art for covers/dividers.
5. **Build** — `$R scripts/build_deck.py deck.json out/deck.pptx` and
   `$R scripts/render_preview.py deck.json out/deck.html` (same spec → same content).
6. **QA (mandatory)** — `$R scripts/validate_deck.py out/deck.pptx` (overflow/overlap) → fix → then
   `$R ../premium-design-kit/scripts/kit.py preview out/deck.pptx` and LOOK at the contact sheet;
   zoom on any slide that looks off. PDF: `soffice --headless --convert-to pdf out/deck.pptx`.
7. **Deliver** — files + one line on what was assumed + credits note if stock was used.

## Spec
Full schema: `references/deck_spec_schema.md` — 33 slide types. Examples:
`examples/v2_types_deck_spec.json` (pitch deck: image_split, kpi, native charts, diagrams, gallery),
`examples/lesson_deck_ar.json` (Arabic lesson: objectives, definition, code, process, cycle, quiz +
reveal, activity), `examples/full_types_deck_spec.json` (the 21 classic types).

Classic: title, section, bullets, stats, quote, table, closing, agenda, two_column, comparison,
timeline, process, big_statement, team, feature, icon_grid, pricing, faq, chart_bar, logo_wall,
vertical_timeline, array_pass, code, shot, relation.
v2: image_hero, image_split, gallery, quote_image, chart (native), diagram, kpi, objectives,
definition, quiz, activity, credits. Any slide: `notes`, `background` + `overlay`.

## Writing rules
- Headline = the conclusion, ≤ 10 words. Body ≤ 5 bullets, ≤ 12 words each; use point/detail.
- One accent per slide: the number or step that matters (`highlight` in charts).
- Arabic decks: write in the register the audience speaks (Egyptian for students/social, MSA for
  formal/government); keep technical terms in English where people say them that way (Python, for).
- Speaker notes carry what you would SAY; slides carry what they must SEE.
- Never invent a person's photo, a logo, a quote or a statistic.

## Animations
Slide transitions are native in the .pptx. Object-by-object entrance animations: use the HTML
version (full CSS motion) or add them in PowerPoint; say which you did. For real motion graphics →
motion-design-studio.

## Hand-offs
premium-documents (handouts, reports from the same content) · premium-spreadsheets (the data behind
charts) · course-studio (full courses) · stock-library (photos/icons with licences) ·
motion-design-studio (animated intros) · creative-studio (brand kits).
