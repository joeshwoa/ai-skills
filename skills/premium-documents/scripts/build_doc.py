#!/usr/bin/env python3
"""build_doc.py — one document spec → an editable Word file AND a designed PDF.

    run.sh build_doc.py doc_spec.json out/report            # → out/report.docx + out/report.pdf
    run.sh build_doc.py spec.json out/report --pdf-only | --docx-only | --offline | --html

(run.sh = skills/premium-design-kit/scripts/run.sh: right Python + the shared design kit.)
The .docx is native Word (real styles, headings, TOC field, tables, RTL) for editing; the .pdf is the
designed version (covers, grids, cards, real TOC page numbers, fonts embedded) for sending/printing.
Both come from the same spec, so the content always matches.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KIT = HERE.parents[1] / "premium-design-kit" / "lib"
for p in (str(HERE), str(KIT)):
    if p not in sys.path:
        sys.path.insert(0, p)

from doc_common import Doc, SpecError, load, placeholders  # noqa: E402


def build(spec_path, out_base, *, pdf=True, docx=True, offline=False, keep_html=False):
    spec, base = load(spec_path)
    out_base = Path(out_base)
    if out_base.suffix in (".pdf", ".docx"):
        out_base = out_base.with_suffix("")
    out_base.parent.mkdir(parents=True, exist_ok=True)
    doc = Doc(spec, base, out_base, offline=offline)
    report = {"type": doc.type, "rtl": doc.rtl, "theme": doc.theme["id"], "files": [], "warnings": []}
    ph = placeholders(spec)
    if ph:
        report["warnings"].append("placeholder text left in the spec (never ship): " + "; ".join(ph[:6]))
    if docx:
        from doc_docx import DocxRenderer
        f = out_base.with_suffix(".docx")
        DocxRenderer(doc).render(f)
        report["files"].append(str(f))
    if pdf:
        from doc_html import HtmlRenderer
        f = out_base.with_suffix(".pdf")
        r = HtmlRenderer(doc).render(f, offline=offline)
        report["files"].append(str(f))
        report["pages"] = r.get("pages")
        if keep_html:
            out_base.with_suffix(".html").write_text(r["html"], encoding="utf-8")
            report["files"].append(str(out_base.with_suffix(".html")))
        if r.get("overflow"):
            report["warnings"].append("content overflowing its box: " + "; ".join(r["overflow"][:6]))
        if r.get("missing_images"):
            report["warnings"].append("images that did not load: " + "; ".join(r["missing_images"][:4]))
    report["warnings"] += doc.assets.warnings
    report["credits"] = doc.credits()
    return report


def main(argv=None):
    a = [x for x in (argv or sys.argv[1:])]
    flags = {x for x in a if x.startswith("--")}
    args = [x for x in a if not x.startswith("--")]
    if len(args) != 2:
        print(__doc__)
        return 1
    try:
        rep = build(args[0], args[1], pdf="--docx-only" not in flags, docx="--pdf-only" not in flags,
                    offline="--offline" in flags, keep_html="--html" in flags)
    except SpecError as e:
        print(f"SPEC ERROR: {e}")
        return 2
    for f in rep["files"]:
        print("wrote", f)
    print(f"type={rep['type']} theme={rep['theme']} rtl={rep['rtl']} pages={rep.get('pages')}")
    for w in rep["warnings"]:
        print("WARN:", w)
    if rep["credits"]:
        print(f"{len(rep['credits'])} image credit(s) printed at the end of the PDF/DOCX")
    return 0


if __name__ == "__main__":
    sys.exit(main())
