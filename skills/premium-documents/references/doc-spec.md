# doc_spec.json — full reference

## Top level
| Key | Values | Notes |
|---|---|---|
| `type` | see doc-types.md | picks the layout preset (cover, toc, numbering, special layouts) |
| `theme` | kit theme id or `{"base": id, …overrides}` | default `plain-pro` |
| `brand` | creative-studio slug / brand.json path / inline dict | only when the user asks |
| `language` | `en` · `ar` | Arabic → RTL everything; auto-detected when omitted |
| `arabic_style` | modern · corporate · classic · friendly · safe | Arabic font pairing |
| `heading_font`, `body_font` | font names | override the theme |
| `page` | `{"size": "A4|A5|A3|Letter|Legal", "orientation": "portrait|landscape", "margins": "normal|narrow|wide|[t,r,b,l mm]"}` | |
| `meta` | title, subtitle, kicker, author, prepared_for, org, date, version, confidential, … | type-specific keys below |
| `cover` | `{"style": photo|art|split|band|minimal|none, "image": ref, "art": kind, "dark": bool, "logo": ref, "kicker": "…"}` | |
| `toc` / `toc_depth` | bool / 1–3 | |
| `numbered` / `number_depth` | bool / 1–3 | 1, 1.1 … numbering |
| `header`, `footer` | text | running header/footer; page "X of Y" is automatic |
| `currency` | "EGP", "$", "ج.م" … | invoices / items |
| `labels` | {key: text} | override any built-in label (see doc_common.LABELS) |
| `icon_set` | Iconify prefix | one family per document |
| `blocks` | list | the content |

Type-specific `meta`:
- letter/cover_letter: `org`, `org_address` (multi-line), `logo`, `to`, `subject`, `date`.
- memo/minutes: `to`, `from`, `cc`, `subject`, `date`, `attendees` (minutes).
- invoice/quotation/receipt: `org`, `from`, `bill_to`, `number`, `date`, `due`.
- cv: `name`, `role`, `photo` (their own). Blocks with `"column": "side"` or type contact/skills go to the sidebar.
- certificate: `org`, `title`, `recipient`, `reason`, `date`, `presented_to`, `signatures` [{name, role}], `seal`.
- handout/worksheet/lab_sheet/exam/answer_key: `course`/`kicker`, `instructions`, `duration`, `student_fields`.
- flyer/one_pager: `subtitle`, `cta` {text, detail, contact}; `cover.image` is the hero.

## Blocks
| Block | Fields |
|---|---|
| heading | `text`, `level` 1–3, `numbered` (false to skip), `toc` (false to hide) |
| section | `title`, `intro`, `image`, `number` — starts a new page with a big number |
| paragraph | `text` (inline markup), `style`: `lead` |
| bullets / numbered | `items`: strings or `{"point", "detail"}`; `style`: number |
| checklist | `items`: strings or `{"text", "done"}` |
| callout | `kind`: info · tip · warning · success · note · example; `title`; `text` or `blocks`; `icon` |
| quote | `text`, `author` · pull_quote: `text` |
| table | `headers`, `rows`, `widths` (% list), `caption`, `total_row` (last row bold), `style`: minimal, `numeric` (col indexes) |
| image | `image` ref, `caption`, `width`: full · half · third, `float`, `height_mm` |
| chart | `chart`: {type bar/hbar/stacked/line/area/pie/donut/scatter, categories, series, unit, prefix, highlight, title, source, center}, `caption`, `height_in` |
| stats | `items`: [{value, label}] (2–4) |
| timeline | `items`: [{date, title, text}] |
| steps | `items`: [{title, text}] |
| two_column | `left`, `right` (block lists), `ratio`: "1:1" · "1:2" · "2:1" |
| cards | `items`: [{icon, title, text}], `cols` 2–4 |
| definition | `term`, `text`, `example` |
| code | `code`, `lang`, `caption` |
| kv | `items`: [[key, value]] |
| box | `title`, `blocks` |
| gallery | `items`: [{image, caption}] |
| schedule | `items`: [{time, duration, title, text}] |
| rubric | `levels`: [...], `criteria`: [{name, weight, descriptors: [...]}] |
| items | invoice lines: `items`: [{description, detail, qty, price}], `tax_pct`, `discount` / `discount_pct`, `shipping`, `currency` |
| questions | `items`: [{q, kind: mcq·tf·short·essay·code·fill, options, answer (index or text), points, lines, explanation}], `show_answers`, `start` |
| experience / education | `items`: [{role/degree, org/school, place, from, to, bullets, text}] |
| skills | `groups`: [{group, items, levels (0–100, optional bars)}] |
| contact | `items`: [[label, value]] |
| signature | `parties`: [{name, role, date_line}] |
| note_lines | `lines` |
| divider · spacer (`mm`) · page_break · toc | |

## Inline markup
`**bold**` · `*accent*` (accent colour, bold) · `` `code` `` (LTR, monospace) · `[text](https://url)`.

## Assets
Any `image`/`icon` field takes the kit's asset refs: a path, `{"photo": "english query",
"orientation": …}`, `{"stock": "provider:id"}`, `{"icon": "words" | "prefix:name"}`, `{"art": kind}`,
`{"chart": {…}}`. Credits required by licences are printed at the end automatically.
