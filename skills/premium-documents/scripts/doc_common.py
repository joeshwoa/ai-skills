"""Shared logic for the two document renderers (doc_html → designed PDF, doc_docx → editable Word):
spec loading + validation, document-type presets, theme/brand/RTL resolution, asset resolution,
heading numbering, invoice maths and localised labels. Both renderers call `prepare(spec)` so they
always see the SAME normalised document."""
from __future__ import annotations

import copy
import datetime as _dt
import json
from pathlib import Path

from pdk.assets import Assets
from pdk.text import spec_is_rtl
from pdk.themes import ARABIC_FONTS, resolve_theme, tokens

# --------------------------------------------------------------------------------- type presets
# page: size/orientation; cover: default cover style; toc: table of contents by default;
# numbered: number headings 1, 1.1 …; header: show running header; layout: special layout engine.
PRESETS = {
    "report":       {"cover": "photo", "toc": True, "numbered": True, "header": True},
    "whitepaper":   {"cover": "art", "toc": True, "numbered": True, "header": True},
    "proposal":     {"cover": "split", "toc": True, "numbered": True, "header": True},
    "business_plan": {"cover": "photo", "toc": True, "numbered": True, "header": True},
    "ebook":        {"cover": "photo", "toc": True, "numbered": False, "header": True, "chapters": True},
    "guide":        {"cover": "art", "toc": True, "numbered": False, "header": True},
    "manual":       {"cover": "band", "toc": True, "numbered": True, "header": True},
    "policy":       {"cover": "band", "toc": True, "numbered": True, "header": True},
    "sop":          {"cover": "band", "toc": False, "numbered": True, "header": True},
    "case_study":   {"cover": "photo", "toc": False, "numbered": False, "header": True},
    "newsletter":   {"cover": "masthead", "toc": False, "numbered": False, "header": False, "columns": 2},
    "brochure":     {"cover": "photo", "toc": False, "numbered": False, "header": False, "page": {"size": "A4"}},
    "flyer":        {"cover": "none", "toc": False, "numbered": False, "header": False, "layout": "flyer"},
    "one_pager":    {"cover": "none", "toc": False, "numbered": False, "header": False, "layout": "one_pager"},
    "letter":       {"cover": "none", "toc": False, "numbered": False, "header": False, "layout": "letter"},
    "cover_letter": {"cover": "none", "toc": False, "numbered": False, "header": False, "layout": "letter"},
    "memo":         {"cover": "none", "toc": False, "numbered": False, "header": False, "layout": "memo"},
    "minutes":      {"cover": "none", "toc": False, "numbered": False, "header": True, "layout": "memo"},
    "contract":     {"cover": "minimal", "toc": False, "numbered": True, "header": True, "legal": True},
    "nda":          {"cover": "none", "toc": False, "numbered": True, "header": True, "legal": True},
    "invoice":      {"cover": "none", "toc": False, "numbered": False, "header": False, "layout": "invoice"},
    "quotation":    {"cover": "none", "toc": False, "numbered": False, "header": False, "layout": "invoice"},
    "receipt":      {"cover": "none", "toc": False, "numbered": False, "header": False, "layout": "invoice"},
    "cv":           {"cover": "none", "toc": False, "numbered": False, "header": False, "layout": "cv"},
    "certificate":  {"cover": "none", "toc": False, "numbered": False, "header": False, "layout": "certificate",
                     "page": {"size": "A4", "orientation": "landscape"}},
    "lesson_plan":  {"cover": "none", "toc": False, "numbered": False, "header": True},
    "syllabus":     {"cover": "band", "toc": False, "numbered": True, "header": True},
    "course_plan":  {"cover": "photo", "toc": True, "numbered": True, "header": True},
    "handout":      {"cover": "none", "toc": False, "numbered": False, "header": True, "layout": "handout"},
    "worksheet":    {"cover": "none", "toc": False, "numbered": False, "header": True, "layout": "handout"},
    "lab_sheet":    {"cover": "none", "toc": False, "numbered": False, "header": True, "layout": "handout"},
    "exam":         {"cover": "none", "toc": False, "numbered": False, "header": True, "layout": "exam"},
    "answer_key":   {"cover": "none", "toc": False, "numbered": False, "header": True, "layout": "exam"},
    "instructor_guide": {"cover": "band", "toc": True, "numbered": True, "header": True},
    "document":     {"cover": "minimal", "toc": False, "numbered": False, "header": True},
}

PAGE_SIZES_MM = {"A4": (210, 297), "A5": (148, 210), "A3": (297, 420), "Letter": (215.9, 279.4),
                 "Legal": (215.9, 355.6)}
MARGINS_MM = {"normal": (22, 20, 22, 20), "narrow": (14, 14, 16, 14), "wide": (28, 28, 28, 28)}  # t r b l

LABELS = {
    "en": {"contents": "Contents", "page": "Page", "of": "of", "figure": "Figure", "table": "Table",
           "invoice": "Invoice", "quotation": "Quotation", "receipt": "Receipt", "bill_to": "Bill to",
           "from": "From", "date": "Date", "due": "Due date", "number": "No.", "item": "Description",
           "qty": "Qty", "price": "Unit price", "amount": "Amount", "subtotal": "Subtotal", "tax": "Tax",
           "discount": "Discount", "total": "Total", "notes": "Notes", "signature": "Signature",
           "name": "Name", "student": "Student", "class": "Class", "score": "Score", "answer": "Answer",
           "points": "pts", "true": "True", "false": "False", "to": "To", "subject": "Subject",
           "cc": "Cc", "experience": "Experience", "education": "Education", "skills": "Skills",
           "languages": "Languages", "projects": "Projects", "contact": "Contact", "summary": "Profile",
           "certificate_of": "Certificate of Completion", "presented_to": "This certificate is presented to",
           "time": "Time", "duration": "Duration", "objectives": "Objectives", "materials": "Materials",
           "chapter": "Chapter", "tip": "Tip", "warning": "Warning", "note": "Note", "info": "Info",
           "success": "Good to know", "example": "Example", "key_term": "Key term", "level": "Level",
           "criteria": "Criteria", "attendees": "Attendees", "decisions": "Decisions", "actions": "Action items",
           "owner": "Owner", "prepared_for": "Prepared for", "prepared_by": "Prepared by", "version": "Version",
           "confidential": "Confidential"},
    "ar": {"contents": "المحتويات", "page": "صفحة", "of": "من", "figure": "شكل", "table": "جدول",
           "invoice": "فاتورة", "quotation": "عرض سعر", "receipt": "إيصال", "bill_to": "إلى",
           "from": "من", "date": "التاريخ", "due": "تاريخ الاستحقاق", "number": "رقم", "item": "البيان",
           "qty": "الكمية", "price": "سعر الوحدة", "amount": "الإجمالي", "subtotal": "الإجمالي الفرعي",
           "tax": "الضريبة", "discount": "الخصم", "total": "الإجمالي المستحق", "notes": "ملاحظات",
           "signature": "التوقيع", "name": "الاسم", "student": "الطالب", "class": "الفصل", "score": "الدرجة",
           "answer": "الإجابة", "points": "درجة", "true": "صح", "false": "خطأ", "to": "إلى", "subject": "الموضوع",
           "cc": "نسخة إلى", "experience": "الخبرات", "education": "التعليم", "skills": "المهارات",
           "languages": "اللغات", "projects": "المشروعات", "contact": "التواصل", "summary": "نبذة",
           "certificate_of": "شهادة إتمام", "presented_to": "تُمنح هذه الشهادة إلى",
           "time": "الوقت", "duration": "المدة", "objectives": "الأهداف", "materials": "الأدوات",
           "chapter": "الفصل", "tip": "نصيحة", "warning": "تنبيه", "note": "ملاحظة", "info": "معلومة",
           "success": "خلاصة", "example": "مثال", "key_term": "مصطلح", "level": "المستوى",
           "criteria": "المعيار", "attendees": "الحضور", "decisions": "القرارات", "actions": "المهام",
           "owner": "المسؤول", "prepared_for": "مُعد لـ", "prepared_by": "إعداد", "version": "الإصدار",
           "confidential": "سري"},
}

BLOCK_TYPES = {
    "heading", "paragraph", "bullets", "numbered", "checklist", "callout", "quote", "table", "image", "chart",
    "stats", "timeline", "steps", "two_column", "cards", "definition", "code", "kv", "signature",
    "page_break", "divider", "spacer", "toc", "section", "questions", "rubric", "items", "experience",
    "education", "skills", "contact", "gallery", "schedule", "pull_quote", "note_lines", "box",
}


class SpecError(ValueError):
    pass


def load(path) -> tuple[dict, Path]:
    p = Path(path)
    try:
        spec = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SpecError(f"{p.name}: invalid JSON — {e}") from e
    return spec, p.parent


def check(spec: dict) -> list[str]:
    """Structural problems that would make a broken document (raised before rendering)."""
    errs = []
    if not isinstance(spec.get("blocks", []), list):
        errs.append("'blocks' must be a list")

    def walk(blocks, where):
        for i, b in enumerate(blocks or []):
            if not isinstance(b, dict) or "type" not in b:
                errs.append(f"{where}[{i}]: every block needs a 'type'")
                continue
            if b["type"] not in BLOCK_TYPES:
                errs.append(f"{where}[{i}]: unknown block type '{b['type']}' (known: {', '.join(sorted(BLOCK_TYPES))})")
            if b["type"] == "table":
                w = len(b.get("headers") or (b.get("rows") or [[]])[0])
                for r, row in enumerate(b.get("rows", [])):
                    if len(row) != w:
                        errs.append(f"{where}[{i}] table row {r} has {len(row)} cells, header has {w}")
            if b["type"] == "two_column":
                walk(b.get("left"), f"{where}[{i}].left")
                walk(b.get("right"), f"{where}[{i}].right")
            if b["type"] == "box":
                walk(b.get("blocks"), f"{where}[{i}].blocks")
    walk(spec.get("blocks"), "blocks")
    t = spec.get("type", "document")
    if t not in PRESETS:
        errs.append(f"unknown document type '{t}' (known: {', '.join(PRESETS)})")
    return errs


def placeholders(spec) -> list[str]:
    """Leftover template text — never ship these."""
    import re
    bad = re.compile(r"lorem ipsum|\[(?:company|name|client|date|insert)[^\]]*\]|click to add|TBD\b|XXX", re.I)
    hits = []

    def walk(o, path):
        if isinstance(o, str):
            if bad.search(o):
                hits.append(f"{path}: “{o[:60]}”")
        elif isinstance(o, dict):
            for k, v in o.items():
                walk(v, f"{path}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{path}[{i}]")
    walk(spec, "spec")
    return hits


class Doc:
    """The normalised document both renderers draw."""

    def __init__(self, spec: dict, base: Path, out: Path, *, offline: bool = False):
        errs = check(spec)
        if errs:
            raise SpecError("spec problems:\n- " + "\n- ".join(errs))
        self.spec = copy.deepcopy(spec)
        self.base = base
        self.type = spec.get("type", "document")
        self.preset = dict(PRESETS.get(self.type, PRESETS["document"]))
        self.rtl = spec_is_rtl(spec)
        self.lang = "ar" if self.rtl else "en"
        self.L = dict(LABELS[self.lang])
        self.L.update(spec.get("labels", {}))
        theme = dict(resolve_theme(spec.get("theme"), spec.get("brand"), default="plain-pro"))
        if self.rtl:
            h, b = ARABIC_FONTS.get(spec.get("arabic_style", "modern"), ARABIC_FONTS["modern"])
            theme["heading_font_ar"] = theme.get("heading_font_ar") or h
            theme["body_font_ar"] = theme.get("body_font_ar") or b
        if spec.get("heading_font"):
            theme["heading_font_ar" if self.rtl else "heading_font"] = spec["heading_font"]
        if spec.get("body_font"):
            theme["body_font_ar" if self.rtl else "body_font"] = spec["body_font"]
        self.theme = theme
        self.tk = tokens(theme, arabic=self.rtl)
        if self.rtl:
            self.tk["head_font"] = theme["heading_font_ar"]
            self.tk["body_font"] = theme["body_font_ar"]
        self.logo = theme.get("logo")
        meta = dict(spec.get("meta", {}))
        meta.setdefault("date", _dt.date.today().isoformat() if spec.get("auto_date", True) else "")
        self.meta = meta
        page = dict(self.preset.get("page", {}))
        page.update(spec.get("page", {}))
        self.page_size = page.get("size", "A4")
        self.orientation = page.get("orientation", "portrait")
        w, h = PAGE_SIZES_MM.get(self.page_size, PAGE_SIZES_MM["A4"])
        if self.orientation == "landscape":
            w, h = h, w
        self.page_mm = (w, h)
        m = page.get("margins", "normal")
        self.margins_mm = MARGINS_MM.get(m, m) if isinstance(m, str) else tuple(m)
        self.cover = spec.get("cover", {})
        if isinstance(self.cover, str):
            self.cover = {"style": self.cover}
        self.cover.setdefault("style", self.preset.get("cover", "minimal"))
        self.toc = spec.get("toc", self.preset.get("toc", False))
        self.numbered = spec.get("numbered", self.preset.get("numbered", False))
        self.layout = self.preset.get("layout", "flow")
        self.assets = Assets(out.parent / f"_assets-{out.stem}", self.tk, base=base,
                             project=spec.get("project") or out.stem, offline=offline,
                             icon_set=spec.get("icon_set", "material-symbols"))
        self.blocks = self.spec.get("blocks", [])
        self._number_headings()

    # ------------------------------------------------------------------ helpers
    def _number_headings(self):
        counters = [0, 0, 0, 0]
        self.outline = []
        for b in self._iter(self.blocks):
            if b["type"] in ("heading", "section"):
                lvl = 1 if b["type"] == "section" else int(b.get("level", 1))
                counters[lvl - 1] += 1
                for j in range(lvl, 4):
                    counters[j] = 0
                depth = int(self.spec.get("number_depth", 2))
                num = ".".join(str(c) for c in counters[:lvl]) if self.numbered and b.get("numbered", True) and lvl <= depth else ""
                b["_num"] = num
                b["_id"] = f"h{len(self.outline) + 1}"
                b["_level"] = lvl
                if b.get("toc", True) and lvl <= int(self.spec.get("toc_depth", 2)):
                    self.outline.append({"id": b["_id"], "num": num, "text": b.get("text") or b.get("title", ""), "level": lvl})

    def _iter(self, blocks):
        for b in blocks or []:
            yield b
            if b.get("type") == "two_column":
                yield from self._iter(b.get("left"))
                yield from self._iter(b.get("right"))
            if b.get("type") == "box":
                yield from self._iter(b.get("blocks"))

    def asset(self, ref, **kw):
        return self.assets.resolve(ref, **kw) if ref else None

    def label(self, key):
        return self.L.get(key, key)

    def money(self, v, currency=None):
        cur = currency if currency is not None else self.spec.get("currency", "")
        s = f"{float(v):,.2f}"
        if not cur:
            return s
        if len(cur) == 1 and not self.rtl:      # $ € £ before the number
            return f"{cur}{s}"
        return f"{s} {cur}"                     # EGP 1,200.00 → 1,200.00 EGP / ج.م

    def invoice_totals(self, b):
        items = b.get("items", [])
        rows, sub = [], 0.0
        for it in items:
            q = float(it.get("qty", 1))
            p = float(it.get("price", 0))
            amt = q * p
            sub += amt
            rows.append((it.get("description", it.get("item", "")), it.get("detail", ""), q, p, amt))
        disc = float(b.get("discount", 0))
        if b.get("discount_pct"):
            disc = sub * float(b["discount_pct"]) / 100
        taxable = sub - disc
        tax_pct = float(b.get("tax_pct", 0))
        tax = taxable * tax_pct / 100
        total = taxable + tax + float(b.get("shipping", 0))
        return {"rows": rows, "subtotal": sub, "discount": disc, "tax_pct": tax_pct, "tax": tax, "total": total}

    def credits(self):
        return self.assets.credits()
