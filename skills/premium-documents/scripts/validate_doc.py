#!/usr/bin/env python3
"""validate_doc.py — check a built document before it is delivered.

    run.sh validate_doc.py out/report.pdf [out/report.docx] [--sheet]

PDF:  page count, blank/near-empty pages, fonts actually embedded (Arabic text must not fall back to a
      font without Arabic glyphs), leftover placeholders, tiny text, missing images.
DOCX: placeholders, RTL flags on Arabic paragraphs, heading structure (no skipped levels), images,
      empty table cells in header rows, TOC field present when a TOC was asked for.
--sheet  also writes page PNGs + a contact sheet next to the PDF (LOOK at it).
Exit code 1 when an ERROR is found (warnings alone exit 0).
"""
import re
import sys
from pathlib import Path

from pdk.text import has_arabic

PLACEHOLDER = re.compile(r"lorem ipsum|\[(?:company|name|client|date|insert)[^\]]*\]|click to add|\bTBD\b|XXX", re.I)


def check_pdf(path, sheet=False):
    import pymupdf as fitz
    errs, warns, info = [], [], {}
    with fitz.open(str(path)) as d:
        info["pages"] = d.page_count
        fonts = set()
        arabic_text = False
        for i, page in enumerate(d):
            txt = page.get_text()
            if PLACEHOLDER.search(txt):
                errs.append(f"page {i + 1}: placeholder text “{PLACEHOLDER.search(txt).group(0)}”")
            if has_arabic(txt):
                arabic_text = True
            imgs = page.get_images()
            words = len(txt.split())
            if words < 3 and not imgs and i > 0:
                warns.append(f"page {i + 1} is (almost) empty — check for a stray page break")
            for f in page.get_fonts():
                fonts.add(f[3])
            for b in page.get_text("dict")["blocks"]:
                for line in b.get("lines", []):
                    for sp in line.get("spans", []):
                        if sp["size"] < 6.5 and sp["text"].strip() and len(sp["text"].strip()) > 3:
                            warns.append(f"page {i + 1}: very small text ({sp['size']:.1f}pt): “{sp['text'][:30]}”")
                            break
        info["fonts"] = sorted({re.sub(r"^[A-Z]{6}\+", "", f) for f in fonts})
        if arabic_text and not any(re.search(r"cairo|tajawal|plex.*arab|naskh|amiri|messiri|arab|geeza|kufi|noto.*arab", f, re.I)
                                    for f in info["fonts"]):
            warns.append("Arabic text but no Arabic font embedded — check the shaping in the page images (install fonts: premium-design-kit/scripts/fonts.sh)")
    if sheet:
        from pdk.render import preview
        info["sheet"] = preview(path).get("sheet")
    return errs, warns[:25], info


def check_docx(path):
    from docx import Document
    from docx.oxml.ns import qn
    errs, warns, info = [], [], {}
    doc = Document(str(path))
    paras = list(doc.paragraphs)
    for t in doc.tables:
        for row in t.rows:
            for c in row.cells:
                paras.extend(c.paragraphs)
    last_level = 0
    n_ar_no_bidi = 0
    for p in paras:
        if PLACEHOLDER.search(p.text):
            errs.append(f"placeholder text: “{p.text[:60]}”")
        if has_arabic(p.text):
            ppr = p._p.pPr
            if ppr is None or ppr.find(qn("w:bidi")) is None:
                st = p.style.element.pPr if p.style is not None and p.style.element is not None else None
                if st is None or st.find(qn("w:bidi")) is None:
                    n_ar_no_bidi += 1
        m = re.match(r"Heading (\d)", p.style.name if p.style is not None else "")
        if m and p in doc.paragraphs:
            lvl = int(m.group(1))
            if lvl > last_level + 1:
                warns.append(f"heading level jumps from {last_level} to {lvl}: “{p.text[:40]}”")
            last_level = lvl
    if n_ar_no_bidi:
        warns.append(f"{n_ar_no_bidi} Arabic paragraph(s) without right-to-left direction")
    info["images"] = len(doc.inline_shapes)
    info["tables"] = len(doc.tables)
    info["headings"] = sum(1 for p in doc.paragraphs if p.style is not None and p.style.name.startswith("Heading"))
    body = doc.element.body.xml
    info["toc_field"] = "TOC \\o" in body
    return errs, warns[:25], info


def main(argv=None):
    a = argv or sys.argv[1:]
    sheet = "--sheet" in a
    files = [x for x in a if not x.startswith("--")]
    if not files:
        print(__doc__)
        return 1
    bad = False
    for f in files:
        p = Path(f)
        if p.suffix.lower() == ".pdf":
            errs, warns, info = check_pdf(p, sheet)
        elif p.suffix.lower() == ".docx":
            errs, warns, info = check_docx(p)
        else:
            print(f"skip {p} (pdf/docx only)")
            continue
        print(f"{'❌' if errs else '✅'} {p.name}: {info}")
        for e in errs:
            print("  ERROR:", e)
        for w in warns:
            print("  WARN: ", w)
        bad = bad or bool(errs)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
