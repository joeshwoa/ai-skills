# Design system — what "premium" means in every document

## 1. Principles (apply to decks, documents, sheets)
1. **One idea per unit.** One message per slide, one purpose per page section, one question per sheet.
2. **Real content.** Real numbers, real names, real dates. A gap is written `[NEEDS: Q3 revenue]` and
   reported to the user — never invented, never lorem ipsum.
3. **Hierarchy you can see from 2 m away.** Title ≥ 2.4× body; one accent colour used for meaning
   (the number that matters, the active step), not decoration.
4. **Rhythm.** Everything sits on the grid; equal gaps; aligned edges. Misalignment is what makes
   things look "AI-made".
5. **Variety with a system.** Mix layouts (stats row, timeline, cards, chart + insight, full-bleed
   photo) but keep the same margins, colours, fonts and icon family.
6. **Editable.** Native text, native tables, native charts. Pictures only for photos/art.
7. **Accessible.** Contrast ≥ 4.5:1 for text (tokens enforce it), ≥ 10.5 pt body in print,
   ≥ 18 pt on slides, never colour alone to carry meaning (add an icon or label).

## 2. Grids
| Medium | Grid | Margins | Gutter |
|---|---|---|---|
| 16:9 slide 13.33×7.5 in | 12 columns | 0.8 in sides, 0.5 top, 0.6 bottom | 0.3 in |
| A4 document | 6 columns | 20–22 mm (normal), 14 (narrow), 28 (wide) | 6 mm |
| Spreadsheet | column A label, data from B; 1 blank row between blocks | — | — |
Half/third splits: 1:1 (compare), 1:2 / 2:1 (image + text), 3 equal (cards).

## 3. Type scale
| Role | Slide | Document | Sheet |
|---|---|---|---|
| Display / cover | 40–54 pt | 30–34 pt | 16–20 pt |
| H1 | 30 pt | 20–22 pt | 14 pt |
| H2 | 22–24 pt | 14–15 pt | 12 pt |
| Body | 17–20 pt | 10.5–11 pt | 10.5 pt |
| Caption / source | 11–12 pt | 8–8.5 pt | 9 pt |
Line height: Latin 1.3–1.45 · Arabic 1.6–1.85. Max line length ≈ 70 characters (Latin), 60 (Arabic).
Weights: 800–900 for display, 700 headings, 400 body. Two families max.

## 4. Colour
Tokens (from `pdk.themes.tokens`): `paper`, `paper_alt` (panels/zebra), `ink`, `ink_soft`, `muted`
(captions), `line` (hairlines), `accent` (contrast-safe), `accent_2`, `accent_soft` (callout fill),
`on_accent`, `stage_*` for slides. Use: 60% paper · 30% ink/neutral · 10% accent. Status colours
are fixed: success 1E7A46 / E9F7EF, warning B45309 / FFF4E5, error 9C0006 / FFC7CE.

## 5. Patterns by document type
- **Pitch / board deck**: title → problem (image_split) → solution (feature/image) → traction
  (kpi) → market (chart + insight) → business model (pricing/table) → competition (matrix) → team
  → ask (big_statement) → closing. 10–15 slides.
- **Teaching deck**: title (image_hero) → objectives → hook (big_statement/quote_image) → concept
  (definition) → worked example (code/process) → check (quiz → reveal) → practice (activity) →
  recap (icon_grid) → homework (closing). Change slide type at least every 2 slides.
- **Report**: cover (photo) → contents → executive summary (lead + stats + callout recommendation)
  → findings (heading, chart + caption, table) → recommendations (cards/steps) → appendix.
- **Proposal**: split cover → summary → objectives → approach (steps/timeline) → plan table →
  budget (chart + table) → why us (cards) → signatures.
- **Course plan**: band cover → overview kv → outcomes table → alignment matrix → module map
  (steps) → schedule → assessment (table + donut) → rubrics → materials → policies.
- **Worksheet / exam**: band header + name/class/date fields → instructions → questions with points
  and answer space → challenge callout. Answer key = same questions, answers shown.
- **CV**: dark sidebar (contact, skills, languages) + main (name, role, profile, experience,
  education). One page unless 10+ years.
- **Invoice**: logo + INVOICE + number → from / bill-to / dates → items table → totals box with
  the grand total in the accent → payment details → thanks.
- **Certificate**: landscape, double frame, org, title, recipient as the largest text, reason,
  date, signatures, optional seal.
- **Dashboard (sheet)**: KPI cards row (4 max) → 2–3 charts in a 2-column grid → data on its own
  sheets; every KPI is a formula, never a typed number.

## 6. Images
- Photos: one style per document (all colour or all duotone; similar light). Crop to fill
  (object-fit cover), keep faces in the upper third, never stretch.
- Prefer concrete subjects ("teacher pointing at whiteboard with code") over abstract
  ("technology"). English queries; 2–3 phrasings; look at the contact sheet.
- Icons: one Iconify family per document (default material-symbols), single colour = accent.
- Generated art for covers/dividers when no meaningful photo exists — never as a fake photo.

## 7. QA checklist (every deliverable)
Validator clean → contact sheet looked at → zoom on 2–3 key pages → no overflow/overlap, no orphan
headings at page bottom, no empty pages → Arabic shaped and right-aligned, code left-to-right →
numbers re-checked against the source → credits present when required → file names clean.
