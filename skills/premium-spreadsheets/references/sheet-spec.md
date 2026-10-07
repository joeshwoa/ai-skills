# sheet_spec.json — reference

Top level: `title`, `subtitle`, `author`, `theme` / `brand`, `language` (ar → RTL), `currency`,
`font`, `contents` (true/false — a linked contents sheet; default when > 2 sheets), `sheets`.

## kind: table
| Key | Meaning |
|---|---|
| `name`, `title`, `subtitle`, `note`, `description` (shown on the contents sheet) | |
| `columns` | [{name, type, format, width, input (yellow), formula, bold, align, wrap, currency}] |
| `rows` | list of row lists; a cell may be a formula string `"=…"` using the templates |
| `blank_rows` | extra empty rows for data entry (formulas are still filled) |
| `totals` | {column: sum|average|count|max|min} → SUBTOTAL row (ignores filtered rows) |
| `validation` | {column: [list] | {"type": "decimal|whole|date", "min", "max", "error"} | {"list_range": "=Lists!$A$2:$A$20"}} |
| `conditional` | [{column, type: data_bar|color_scale (reverse)|icon_set|rule, operator, value, formula, style good|bad|warn, whole_row}] |
| `freeze` / `freeze_cols` | freeze header row / first n columns |
| `table_name`, `table_style` | Excel table object name/style |
| `names` | {name: "B5"} extra named cells |
| `charts` | charts placed under the table (see below) |

## kind: inputs
`fields`: [{label, name (defined name), value, type/format, note, options (drop-down)}].

## kind: calc
`columns` (period headers), `lines`: [{id, label, values: [...] or formula: "={rev}+{cogs}",
style: header|total, indent, input, type, name}]. Tokens: `{id}` line `id` in this column ·
`{id@prev}` line `id` in the previous column (growth) · `{id#}` its row number (`=SUM(B{opex#}:E{opex#})`)
· `{col}` / `{prev}` column letters. Example: `examples/pnl_en.json`.

## kind: dashboard
`kpis`: [{label, formula, type/format, note}] (≤ 4 per row) · `charts`: auto-placed in a 2-column grid.

## Charts (any sheet)
{type: bar|hbar|stacked|stacked100|line|area|pie|donut|scatter, title, data_sheet, categories
(column name), values: [column names], labels (data labels), anchor ("H5"), width_cm, height_cm}.

## Recalc report
`errors`: list of "Sheet!A1 = #DIV/0!" · `sample`: dashboard values after recalculation — compare
them with a quick hand calculation before delivering.
