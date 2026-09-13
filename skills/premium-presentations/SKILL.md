---
name: premium-presentations
description: >
  Build fully editable, professional/premium presentations (and the same
  quality bar for documents, spreadsheets, and PDFs) — not flat images, not
  generic template filler. Use this whenever the user asks for a
  presentation, slide deck, pitch deck, investor deck, PowerPoint, keynote,
  or any "make me slides about X" request, even if they don't say
  "professional" or "premium" explicitly — treat every deck request as
  wanting agency-quality output unless they clearly say otherwise (e.g.
  "just a rough draft"). If the user hasn't specified a visual style/theme,
  ALWAYS stop and ask them (see "Step 1: figure out the design" below)
  instead of guessing — a wrong visual direction is expensive to redo, a
  quick question is not. Also use this skill's methodology (deck-spec to
  native-format generation, ask-before-guessing on design, real data not
  placeholders) as the pattern for sibling skills that build documents or
  spreadsheets to the same premium bar.
---

# Premium Presentations

## Why this skill exists

Most AI-generated decks fail in one of two ways: either they're gorgeous
HTML that becomes a flattened, uneditable mess the moment someone tries to
tweak a bullet point in PowerPoint, or they're a real .pptx that looks like
the default Office template with "Click to add text" energy. This skill is
built to avoid both failure modes: it generates a **real, natively editable
.pptx** (every title, bullet, and table cell is a genuine text run — not a
picture of text) using a themed design system, and it never ships a deck
full of "[Company Name]" and "Lorem ipsum" unless the user explicitly asked
for a blank template.

## The two outputs, and why there are two

| Output | Built by | Purpose |
|---|---|---|
| `.pptx` | `scripts/build_deck.py` (python-pptx, direct) | The deliverable. Fully editable in PowerPoint, Keynote, Google Slides. |
| `.html` | `scripts/render_preview.py` | A preview with real CSS transitions/animations, and the source for a polished PDF export. |

Both read the *same* `deck_spec.json`, so they always match. Do **not** try
to build the .pptx by converting the HTML — LibreOffice/unoconv-style HTML
→ PPTX conversion flattens text into images or uneditable boxes, which
defeats the entire point of "fully editable." Generate them independently
from the shared spec instead.

## Step 1: figure out the design

If the user gave you a theme, brand colors, an example deck, or a company
style guide to follow — use it, skip the questions below.

**If they didn't specify anything about visual style**, don't guess. Ask,
briefly, covering:

1. **Purpose & audience** — investor pitch, internal review, sales deck,
   conference talk, etc. (This alone often implies a theme — an investor
   deck usually wants `onyx-gold` or `sunset-startup`, an engineering
   review wants `cobalt-tech`.)
2. **Show the theme gallery** — render
   `scripts/themes.py` → `assets/theme_gallery.html` (or open the one
   already in this folder) and share it so they can pick by eye rather than
   by reading hex codes. Recommend one based on (1) and say why.
3. **Roughly how many slides / how long a talk.**
4. **Do they have the content already** (a doc, notes, data) or do you need
   to draft the narrative and pull real numbers yourself?
5. **Output needed**: editable .pptx, a PDF leave-behind, or both.

Keep this to one focused round of questions, not an interrogation — default
sensible answers for anything they don't care about (e.g. assume both pptx
+ pdf if they don't say). If you have follow-up ideas the user didn't ask
for (e.g. "want a one-page PDF summary too, for the email that goes out
before the meeting?"), offer them briefly rather than silently deciding.

## Step 2: write the content — with real data

Never ship a deck of placeholders unless the user explicitly wants "just a
template." Before writing `deck_spec.json`:

- Pull real facts/numbers from whatever the user gave you (an attached
  file, pasted text, earlier context) or from live research if the task
  needs current information you don't have.
- If a number genuinely isn't available, write an obvious bracketed
  placeholder (`[REVENUE FIGURE NEEDED]`) and flag it to the user — never
  invent a number that could be mistaken for a real one.
- Write actual sentences, not generic corporate filler. A bullet like
  "Increased efficiency" is weak; "Cut average onboarding time from 9 days
  to 36 minutes by shipping self-serve signup" is what this skill is for.
  Use the `{"point": ..., "detail": ...}` bullet form (see schema) to
  separate the headline claim from its supporting evidence — that split is
  what makes a slide read as "premium" instead of "bullet soup."

Full schema and all 7 slide types (`title`, `section`, `bullets`, `stats`,
`quote`, `table`, `closing`) are in `references/deck_spec_schema.md`, with
a worked example at `examples/sample_deck_spec.json`. Read the schema file
before writing your first deck spec.

## Step 3: generate

```bash
python3 scripts/build_deck.py   deck_spec.json  output.pptx   # the deliverable
python3 scripts/render_preview.py deck_spec.json output.html  # animated preview
```

To also produce a PDF (from the .pptx, which is the higher-fidelity source —
not from the HTML, whose CSS LibreOffice renders imperfectly):

```bash
soffice --headless --convert-to pdf output.pptx
```

If `soffice`/LibreOffice isn't available in your environment, use whatever
document-conversion skill/tool is available, or hand back the .pptx and
let the user's own PowerPoint/Keynote export the PDF — don't silently skip
the PDF if the user asked for one.

## Step 4: check it before you hand it over

Open the generated file (or convert one slide to an image and look at it —
`soffice --headless --convert-to pdf` then `pdftoppm -png` on 2-3 slides is
a fast way to sanity-check layout) and check for:

- Text overflowing its box, or a table wider than the slide.
- Enough contrast between text and background (the built-in themes are
  pre-checked, but if you add a custom theme, verify it).
- The story arc makes sense slide-to-slide, not just each slide in
  isolation.

Then deliver both files, plus a one-line note on how to get the PDF if they
didn't already get one.

## Animations & transitions — what's realistic

The user will often ask for "animations and transitions." Be upfront about
what each output format can actually do, rather than promising more than
PowerPoint delivers:

- **Slide transitions** (fade/push/wipe between slides): `build_deck.py`
  writes these directly into the .pptx via `add_transition()` — they work
  natively in PowerPoint, Keynote, and Google Slides.
- **Object-level entrance animations** (bullets flying in one by one, etc.):
  python-pptx has no public API for this, and hand-writing the OOXML
  `<p:timing>` tree is fragile and easy to corrupt. If the user specifically
  needs this, either (a) do it by hand in PowerPoint after generating the
  base deck — it's a few clicks per object — or (b) lean on the HTML
  version, which has full, reliable CSS animation support and looks great
  for a live/embedded presentation, a video capture, or a webpage version
  of the deck.
- Don't silently skip this — tell the user which path you're taking and
  why, in one sentence, so they're not surprised the .pptx doesn't have
  bullets flying in.

## Adding themes or slide types

Themes live entirely in `scripts/themes.py` — add a dict to `THEMES` (see
the file for the schema: bg/bg_alt/primary/secondary/fonts/style). New
slide types go in `scripts/build_deck.py` (a `slide_x(prs, theme, spec)`
function added to `SLIDE_BUILDERS`) **and** the matching branch in
`scripts/render_preview.py`'s `render_slide_body()` — keep both renderers
in sync or the preview and the deliverable will drift apart.

## Applying this to documents, sheets, and PDFs

The user may also ask for a report/doc, a spreadsheet, or a standalone PDF
built to the same bar. The pattern here generalizes:

1. Ask about design/format only when it's not specified (don't ask about
   things you can reasonably default).
2. Build natively in the target format (python-docx for Word, openpyxl for
   Excel — this repo already has both available) rather than converting
   from HTML, for the same "must stay editable" reason.
3. Fill with real content/data, flag genuine gaps instead of inventing
   numbers.
4. Visually verify the output before handing it over.

If a dedicated doc/sheet/pdf skill already exists in this environment
(check the available skills first), prefer it and use this skill only for
presentations — don't duplicate work. If none exists, this section is your
starting methodology for building one, following the same repo's
`skills/<name>/` layout.
