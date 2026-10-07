---
name: premium-design-kit
description: The shared design engine and art department behind premium-presentations, premium-documents, premium-spreadsheets and course-studio — 24 themes plus brand kits (creative-studio brands), Arabic/RTL typography, contrast-safe colour tokens, real images from free stock, Iconify icons, generated original art (covers, backgrounds, patterns), themed charts, and visual QA (page/slide previews and contact sheets). Use when choosing or making a theme or brand look for any document, finding or generating images, icons, grids or backgrounds for a design, making a chart image, previewing/QA-ing a PDF/PPTX/DOCX/XLSX, or setting up the document skills on a new machine.
---

# Premium Design Kit

The art department every document skill shares, so a deck, a report, a worksheet and a gradebook
for the same client look like one family. Code lives in `lib/pdk/` (import `pdk`); scripts run
through `scripts/run.sh` (right Python + the kit on the path).

## Setup (once per machine)
```bash
bash scripts/setup.sh            # venv: python-pptx, python-docx, openpyxl, matplotlib, Arabic shaping, PyMuPDF, Playwright
bash scripts/fonts.sh            # free Arabic + Latin fonts (Cairo, Tajawal, IBM Plex Sans Arabic, Amiri, Inter…) — ask first
bash scripts/selftest.sh         # themes, chart, art, a deck, a document, a workbook
```
Chromium for designed PDFs is shared with creative-studio when installed (else setup asks).
LibreOffice is optional but recommended for previews of Office files: `brew install --cask libreoffice`.
Stock photos and icons come through the user's studio-mcp (`creative-studio/scripts/bootstrap.sh`);
without it the kit still works and uses generated art instead of photos.

## The art department
| Role | Owns | Tool |
|---|---|---|
| Art director | theme or brand, palette tokens, type pairing, grid, cover style | `kit.py themes / tokens / brand` |
| Typographer | Latin + Arabic fonts, RTL, sizes, line height | `pdk.themes.ARABIC_FONTS`, `fonts.sh` |
| Photo editor | real photos from free stock, cropping, licences, credits | `pdk.assets` → stock-library |
| Illustrator | icons (one icon family per document), original art | `{"icon": …}`, `{"art": …}` |
| Data-viz designer | charts true to the numbers, highlight the point | `pdk.charts` / native charts in decks & sheets |
| Pre-press / QA | page images, contact sheets, overflow, fonts embedded | `kit.py preview`, each skill's validator |

## Themes and brands
- `bash scripts/run.sh scripts/kit.py themes --html gallery.html` → list + visual gallery to show the
  user. 24 themes: 20 deck themes (onyx-gold, cobalt-tech, sage-editorial, neoai-dark/light,
  donbosco-lab, ltc-academy, …) and 4 document-first ones: **plain-pro** (the default — neutral, no
  brand), paper-ink, school-bright, royal-academic.
- **No brand by default.** Use a brand only when the user asks: `"brand": "<slug>"` (a creative-studio
  kit in `STUDIO_HOME/brands/<slug>/brand.json`), a path to a brand.json, or an inline dict with
  `colors` + `fonts` + `logo`. The brand overrides the theme's colours, fonts and logo everywhere.
  Inline tweak of a theme: `"theme": {"base": "plain-pro", "primary": "0B6E4F"}`.
- `tokens(theme)` derives stage colours (slides) and paper colours (documents) and darkens/lightens
  accents until they pass contrast (≥ 4.5:1 on paper) — a dark deck theme still prints well.

## Arabic
Specs with Arabic text (or `"language": "ar"`) render right-to-left automatically: mirrored slide
layouts, RTL Word paragraphs/tables/sections, `dir=rtl` PDFs, right-to-left sheets, Arabic fonts
(`arabic_style`: modern = Cairo/Tajawal · corporate = IBM Plex Sans Arabic · classic = Amiri/Noto
Naskh · friendly = El Messiri/Tajawal · safe = Arial). Code stays left-to-right. Charts shape
Arabic and read right-to-left. Egyptian Arabic is fine in content; keep one register per document.

## Assets — one reference format everywhere
Anywhere a spec takes `image`, `icon`, `background`, `photo`:
```json
"image": "photos/team.jpg"                                       // the user's own file
"image": {"photo": "students coding laptops classroom", "orientation": "landscape"}   // free stock
"image": {"stock": "pexels:123456"}                              // an exact pick from a contact sheet
"icon":  "graduation cap"   or  {"icon": "mdi:school"}           // Iconify, recoloured to the theme
"image": {"art": "mesh|blobs|geo|waves|dots|grid|stripes|arcs", "dark": true, "seed": 3}   // original art
"image": {"chart": {...}}                                        // themed chart picture
```
Rules: queries in English; the builder auto-picks the most relevant licence-clean result and prints
the contact sheet path — LOOK at it and pin a better one with `{"stock": id}` when needed. Never use
remote URLs of unknown licence, never a stock face to represent a real named person (use their own
photo or initials), avoid identifiable children and other brands' logos in marketing material.
Credits that a licence requires are added automatically at the end of the deck/document. Add free
keys (Pexels, Pixabay first) via stock-library for far better photos — the user creates the keys.

## Previews & QA
`bash scripts/run.sh scripts/kit.py preview <file.pdf|.pptx|.docx|.xlsx>` → page PNGs + a numbered
contact sheet. Read the sheet image before delivering; zoom into any page that looks off.
References: `references/design-system.md` (grids, type scales, spacing, colour, layout patterns per
document type, what "premium" means here).
