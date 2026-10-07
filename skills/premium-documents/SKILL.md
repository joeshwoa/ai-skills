---
name: premium-documents
description: A document design studio that writes and designs any document as BOTH an editable Word file (.docx — real styles, headings, TOC, tables, RTL) and a designed PDF (covers, grids, cards, charts, real TOC page numbers, embedded fonts) from one spec — reports, proposals, business plans, whitepapers, e-books and guides, manuals, policies/SOPs, case studies, newsletters, brochures, flyers and one-pagers, letters, cover letters, memos and minutes, contracts and NDAs, invoices, quotations and receipts, CVs, certificates, lesson plans, syllabi, handouts, worksheets, lab sheets, exams and answer keys — in English or Arabic (right-to-left), with real photos, icons, charts and brand kits. Use for any request to write, design, format or redo a document, report, letter, CV, invoice, certificate, worksheet or PDF, even when no format is named.
---

# Premium Documents

Writer + editor + art director + layout designer + pre-press, on the shared design kit
(`../premium-design-kit`). One `doc_spec.json` → `name.docx` (to edit) + `name.pdf` (to send/print).

## Setup
`bash ../premium-design-kit/scripts/setup.sh` once. Scripts run through
`R="bash ../premium-design-kit/scripts/run.sh"`. The PDF needs Chromium (setup shares creative-
studio's). Office previews need LibreOffice (optional).

## Gates
1. **Brief** (ask once, short): document type · purpose & reader · language/register · length ·
   look (theme gallery from the kit, or brand when asked; default `plain-pro`, unbranded) · content
   source (their notes/data or research) · outputs (docx + pdf by default). For school/legal/finance
   documents ask for the facts you must not guess (names, amounts, dates, clauses, grading rules).
2. **Outline** — section headings first; check against `references/doc-types.md` (what that type
   must contain, in what order). Show the outline when the document is long or high-stakes.
3. **Write** — real content, the reader's language; numbers with sources; gaps as `[NEEDS: …]` and
   listed to the user. Mix blocks (stats, callout, chart, table, cards, steps, timeline) — a wall
   of paragraphs is not premium.
4. **Design** — cover style, images (`{"photo": …}` concrete English queries; pin picks with
   `{"stock": id}` after looking at the contact sheet), icon family, charts with the point
   highlighted.
5. **Build** — `$R scripts/build_doc.py spec.json out/name` (→ .docx + .pdf; `--pdf-only`,
   `--docx-only`, `--offline`, `--html` to keep the print HTML).
6. **QA (mandatory)** — `$R scripts/validate_doc.py out/name.pdf out/name.docx --sheet` → read the
   contact sheet image; zoom on pages that look off (`kit.py preview`). Fix and rebuild until clean:
   no overflow, no empty pages, headings not stranded at a page bottom, Arabic shaped + right-aligned,
   numbers re-checked.
7. **Deliver** — both files, the assumptions, the `[NEEDS]` list, and that the Word TOC fills in when
   Word asks to update fields (F9).

## Spec (full reference: `references/doc-spec.md`)
```json
{"type": "report", "theme": "plain-pro", "brand": "", "language": "en",
 "page": {"size": "A4", "orientation": "portrait", "margins": "normal"},
 "meta": {"title": "…", "subtitle": "…", "author": "…", "prepared_for": "…", "date": "…", "org": "…", "kicker": "…"},
 "cover": {"style": "photo|art|split|band|minimal|none", "image": {"photo": "…"}},
 "toc": true, "numbered": true, "header": "…", "footer": "…",
 "blocks": [ {"type": "heading", "text": "…"}, {"type": "paragraph", "text": "…"} ]}
```
Types (with layout presets): report, whitepaper, proposal, business_plan, ebook, guide, manual,
policy, sop, case_study, newsletter, brochure, flyer, one_pager, letter, cover_letter, memo, minutes,
contract, nda, invoice, quotation, receipt, cv, certificate, lesson_plan, syllabus, course_plan,
handout, worksheet, lab_sheet, exam, answer_key, instructor_guide, document.
Blocks: heading, section, paragraph (`style: lead`), bullets, numbered, checklist, callout
(info/tip/warning/success/note), quote, pull_quote, table (`total_row`, `widths`, `caption`,
`style: minimal`), image (`width: full|half|third`, `float`), chart, stats, timeline, steps,
two_column (`ratio`), cards (icons), definition, code, kv, box, gallery, schedule, rubric, items
(invoice lines + totals), questions (mcq/tf/short/essay/code/fill; `show_answers`), experience,
education, skills, contact, signature, note_lines, divider, spacer, page_break, toc.
Inline text: `**bold**`, `*accent*`, `` `code` ``, `[link](https://…)`.
Examples: `examples/report_en.json`, `proposal_ar.json`, `worksheet_ar.json`, `invoice_en.json`,
`cv_en.json`, `cert_ar.json`, `letter_en.json`.

## Rules
- Editable means native: never screenshots of text. Images only for photos, art, charts.
- Legal documents (contract, nda, policy): clear numbered clauses, defined terms, signature block —
  and say plainly that it is a draft to be reviewed by a lawyer; never invent legal facts.
- Invoices/quotations: amounts computed by the builder from qty × price, tax %, discount — never
  typed totals. Check currency and tax rules with the user.
- CVs: facts only from the person; 1 page unless long career; no photo unless they give one.
- Certificates: names spelled exactly as given; Arabic names verified letter by letter.
- School material: age-appropriate language and examples; answer keys always separate files.

## Hand-offs
premium-presentations (the deck version) · premium-spreadsheets (data, invoices register,
gradebooks) · course-studio (whole courses) · stock-library (photos/licences) · creative-studio
(brand kits, posters, social graphics) · reels-studio (scripts).
