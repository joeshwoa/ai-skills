"""Script/direction helpers. Office files get logical-order Unicode (Word/PowerPoint shape Arabic
themselves); only RASTER output (matplotlib charts, PIL art) needs `shape()`."""
from __future__ import annotations

import re

AR = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿]")
LAT = re.compile(r"[A-Za-z]")
AR_DIGITS = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")


def has_arabic(s) -> bool:
    return bool(s) and bool(AR.search(str(s)))


def is_rtl(s) -> bool:
    """True when the text is mainly Arabic (at least as many Arabic words as Latin ones)."""
    words = str(s or "").split()
    ar = sum(1 for w in words if AR.search(w))
    lat = sum(1 for w in words if LAT.search(w) and not AR.search(w))
    return ar > 0 and ar >= lat


def spec_is_rtl(spec: dict) -> bool:
    """Decide a whole spec's direction: explicit language/dir wins, else majority of text."""
    lang = str(spec.get("language") or spec.get("lang") or "").lower()
    if spec.get("dir") in ("rtl", "ltr"):
        return spec["dir"] == "rtl"
    if lang.startswith("ar"):
        return True
    if lang.startswith("en"):
        return False
    texts = []

    def walk(o):
        if isinstance(o, str):
            texts.append(o)
        elif isinstance(o, dict):
            for k, v in o.items():
                if k not in ("type", "theme", "icon", "image", "path", "query", "id", "layout", "style"):
                    walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(spec)
    joined = " ".join(texts)
    return is_rtl(joined)


def shape(s: str) -> str:
    """Visual-order, joined Arabic for raster renderers that do no shaping (matplotlib, PIL)."""
    if not has_arabic(s):
        return s
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
    except ImportError:  # pragma: no cover
        return s
    return get_display(arabic_reshaper.reshape(str(s)))


def arabic_digits(s: str) -> str:
    return str(s).translate(AR_DIGITS)


def esc(s) -> str:
    import html
    return html.escape(str(s if s is not None else ""))


def inline_md(s) -> str:
    """Tiny inline markup for HTML renderers: **bold**, *accent*, `code`, [text](url)."""
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r'<em class="hl">\1</em>', s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    s = re.sub(r"\[(.+?)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


def runs(s) -> list[tuple[str, dict]]:
    """Split inline markup into (text, style) runs for Office renderers: bold/accent/code."""
    out = []
    pat = re.compile(r"(\*\*.+?\*\*|(?<![\w*])\*(?!\s).+?(?<!\s)\*(?![\w*])|`.+?`)")
    pos = 0
    s = str(s if s is not None else "")
    for m in pat.finditer(s):
        if m.start() > pos:
            out.append((s[pos:m.start()], {}))
        tok = m.group(0)
        if tok.startswith("**"):
            out.append((tok[2:-2], {"bold": True}))
        elif tok.startswith("`"):
            out.append((tok[1:-1], {"code": True}))
        else:
            out.append((tok[1:-1], {"accent": True, "bold": True}))
        pos = m.end()
    if pos < len(s):
        out.append((s[pos:], {}))
    return out or [("", {})]
