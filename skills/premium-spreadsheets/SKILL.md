---
name: premium-spreadsheets
description: A spreadsheet/financial-modelling studio that builds professional, formula-driven Excel workbooks (.xlsx, also fine in Google Sheets/LibreOffice) — budgets, financial models and forecasts, KPI dashboards with native charts, trackers, inventories, invoices registers, timesheets, gradebooks, attendance sheets, question banks and course schedules — with real Excel tables, live formulas (no pasted results), named inputs, drop-down validation, conditional formatting, contents sheet, print setup, Arabic right-to-left sheets, and an automatic recalculation check that reports every formula error. Use for any request to make, clean, model or redesign a spreadsheet, Excel file, tracker, dashboard, budget or gradebook.
---

# Premium Spreadsheets

Analyst + modeller + designer + auditor on the shared design kit (`../premium-design-kit`).
One `sheet_spec.json` → a workbook where every calculated number is a formula, inputs are yellow,
and the dashboard updates when an input changes.

## Setup
`bash ../premium-design-kit/scripts/setup.sh` once; `R="bash ../premium-design-kit/scripts/run.sh"`.
LibreOffice (optional) enables the automatic recalculation/error check and previews.

## Gates
1. **Brief** — what decision or job the workbook serves · who edits it (inputs) and who reads it
   (dashboard) · the data (their file → read it first; or build the structure with blank rows) ·
   language (Arabic → right-to-left) · currency, units, period · look (kit theme, brand if asked).
2. **Model design** — sheets in order: Contents → Inputs (assumptions, named) → Data tables →
   Calculations → Dashboard. Write down which columns are inputs and which are formulas. No
   hard-coded numbers inside formulas — reference an input (`TaxRate`, `Price`).
3. **Build** — `$R scripts/build_sheet.py spec.json out/name.xlsx`. Presets for common jobs in
   `scripts/presets.py`: `gradebook`, `attendance`, `question_bank`, `tracker`, `schedule`
   (return a spec — fill with real rows, save as JSON, build).
4. **Audit (mandatory)** — the build recalculates in LibreOffice and lists every `#DIV/0! #REF!
   #NAME? #VALUE! #N/A` with its cell — fix until there are none. Check the printed dashboard
   values against a hand calculation for one or two rows. Then `kit.py preview out/name.xlsx` and
   LOOK at the sheets (headers, widths, ### columns, charts).
5. **Deliver** — the file + how to use it (which yellow cells to change) + assumptions.

## Spec (full reference `references/sheet-spec.md`)
```json
{"title": "…", "theme": "plain-pro", "language": "en", "currency": "EGP",
 "sheets": [
  {"name": "Inputs", "kind": "inputs", "fields": [{"label": "Tax rate", "name": "TaxRate", "value": 0.14, "type": "percent"}]},
  {"name": "Sales", "kind": "table", "columns": [{"name": "Item"}, {"name": "Qty", "type": "int", "input": true},
     {"name": "Price", "type": "money", "input": true}, {"name": "Total", "type": "money", "formula": "=[Qty]*[Price]*(1+TaxRate)"}],
   "rows": [["Course", 3, 4500]], "totals": {"Total": "sum"}, "validation": {"Item": ["Course", "Workshop"]},
   "conditional": [{"column": "Total", "type": "data_bar"}]},
  {"name": "Dashboard", "kind": "dashboard", "kpis": [{"label": "Revenue", "formula": "={Sales.Total.total}", "type": "money"}],
   "charts": [{"type": "bar", "data_sheet": "Sales", "categories": "Item", "values": ["Total"], "title": "Revenue by item"}]}]}
```
Sheet kinds: `table` (an Excel Table + banding + totals + validation + conditional formats),
`inputs` (named assumptions), `calc` (statement rows: label + formula per period, `{col}`/`{prev}`/
`{id}` references — P&L, cash flow), `dashboard` (KPI cards + charts in a grid), `text` (notes).
Formula templates: `[Col]` this row · `[Col:all]` the whole column range · `{row}` `{prev}` `{first}`
`{last}` · `{Sheet.Col}` range in another sheet · `{Sheet.Col.total|last|first}` one cell · named
inputs by name. Types: text, int, number, decimal, money, percent, pct, date, datetime, time, score.
Examples: `examples/budget_en.json`, `pnl_en.json`, `gradebook_ar.json`, `tracker_en.json`.

## Rules
- Inputs yellow with blue text; formulas black; totals bold with a top border.
- One table per sheet, starting under the title band; headers short; units in the header ("Price (EGP)").
- Dates as real dates, money as numbers with a number format — never text.
- Dashboards: ≤ 4 KPI cards, 2–3 charts, every value a formula.
- Arabic workbooks: right-to-left sheets, Arabic headers; keep formulas/function names in English
  (Excel translates them on Arabic systems).
- Reading a user's messy file: keep the original, write a cleaned copy; list every change.

## Hand-offs
premium-documents (a report/invoice from the numbers) · premium-presentations (charts for a
deck — use the native chart slide) · course-studio (gradebook, question bank, schedule).
