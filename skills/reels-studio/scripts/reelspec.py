"""Shared helpers for reels-studio scripts: load a reel spec + brand, language facts,
speech-time estimates. Standard library only (python-docx is needed only by the DOCX writer).
"""
from __future__ import annotations

import json
import os
import re
import unicodedata

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDS_DIR = os.path.join(SKILL_DIR, "brands")
FONTS_DIR = os.path.join(SKILL_DIR, "assets", "fonts")

RTL_LANGS = {"ar", "fa", "ur", "he", "ps", "ckb", "yi", "dv", "sd", "ug"}

# Spoken words per second for a natural reel delivery (not a news read). Estimates,
# deliberately on the brisk side of conversational. Override with brief.words_per_sec.
WORDS_PER_SEC = {
    "ar": 2.1, "en": 2.5, "fr": 2.7, "es": 2.9, "pt": 2.8, "it": 2.7, "de": 2.2,
    "ru": 2.2, "tr": 2.3, "fa": 2.2, "ur": 2.4, "hi": 2.6, "id": 2.5, "nl": 2.4,
}
# Measured in characters (syllable blocks) per second instead of words: scripts written without
# spaces (Chinese, Japanese, Thai) and Korean, whose syllable rate is the more stable measure.
CHARS_PER_SEC = {"zh": 4.5, "ja": 7.0, "th": 8.0, "ko": 5.0}
# ISO 639-3 codes for spoken Arabic varieties → treated as Arabic everywhere.
ARABIC_VARIETIES = {"arz", "apc", "ajp", "acm", "afb", "ary", "aeb", "arq", "ayl", "acq", "ars", "apd", "abv"}
DEFAULT_WPS = 2.4
PAUSE_SEC = 0.6

BLOCK_TYPES = {
    # type: (default label, audience)  audience: editor | talent | neutral
    "visual": ("Visual", "editor"),
    "sfx": ("SFX", "editor"),
    "music": ("Music", "editor"),
    "broll": ("B-Roll", "editor"),
    "onscreen_text": ("On-screen Text", "editor"),
    "camera": ("Camera", "editor"),
    "transition": ("Transition", "editor"),
    "note": ("Note", "editor"),
    "super": ("Super", "editor"),            # legal line / disclaimer / price text burned on screen
    "lower_third": ("Lower Third", "editor"),
    "graphic": ("Graphic", "editor"),         # chart, diagram, screen insert, animation
    "question": ("Question", "talent"),       # interviewer/host question (podcast, interview, vox pop)
    "dialogue": ("Dialogue", "talent"),
    "voiceover": ("Voice-over", "talent"),
    "direction": ("Direction", "talent"),
}

ARABIC_RE = re.compile(r"[֐-ࣿיִ-﷿ﹰ-﻿]")
LATIN_RE = re.compile(r"[A-Za-z]")


class SpecError(Exception):
    pass


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def base_lang(lang: str | None) -> str:
    b = (lang or "en").split("-")[0].split("_")[0].lower()
    return "ar" if b in ARABIC_VARIETIES else b


def is_egyptian(lang: str | None) -> bool:
    l = (lang or "").lower().replace("_", "-")
    return l in ("ar-eg", "arz") or l.startswith("arz-")


def as_list(x) -> list:
    """Accept a list, a single string, or nothing."""
    if x is None:
        return []
    if isinstance(x, (list, tuple)):
        return list(x)
    return [x]


def meta_items(meta) -> list:
    """meta may be [[label, value], ...], a {label: value} dict, or plain strings."""
    if isinstance(meta, dict):
        return [[k, v] for k, v in meta.items()]
    return as_list(meta)


DURATION_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*(?:s\b|sec|secs|second|seconds|ث|ثانية|ثواني|ثوان)", re.I)


def parse_duration(text) -> float | None:
    if isinstance(text, (int, float)):
        return float(text)
    m = DURATION_RE.search(str(text or ""))
    return float(m.group(1).replace(",", ".")) if m else None


def direction_for(spec: dict) -> str:
    d = spec.get("direction")
    if d in ("rtl", "ltr"):
        return d
    return "rtl" if base_lang(spec.get("language")) in RTL_LANGS else "ltr"


def has_rtl_chars(text: str) -> bool:
    return bool(ARABIC_RE.search(text or ""))


def load_brand(name: str | None) -> dict:
    """Brand file merged over default.json. `name` may be a brand slug or a path."""
    base = load_json(os.path.join(BRANDS_DIR, "default.json"))
    if not name:
        return base
    path = name if name.endswith(".json") and os.path.exists(name) else os.path.join(BRANDS_DIR, f"{name}.json")
    if not os.path.exists(path):
        raise SpecError(f"brand '{name}' not found (looked for {path}); available: {', '.join(list_brands())}")
    return deep_merge(base, load_json(path))


def list_brands() -> list[str]:
    return sorted(f[:-5] for f in os.listdir(BRANDS_DIR) if f.endswith(".json"))


def deep_merge(a: dict, b: dict) -> dict:
    out = dict(a)
    for k, v in b.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def line_text(item) -> tuple[str, str]:
    """A block line is a string or a dict. Returns (kind, text).
    kinds: line | pause | direction"""
    if isinstance(item, str):
        return "line", item
    if isinstance(item, dict):
        if item.get("pause"):
            return "pause", item.get("text") or "Pause."
        if "direction" in item:
            return "direction", str(item["direction"])
        if "text" in item:
            return "line", str(item["text"])
    raise SpecError(f"unsupported line entry: {item!r}")


def safe_lines(block: dict):
    """(kind, text) for each well-formed line; malformed entries are skipped here and reported
    by the validator's structure check."""
    for item in as_list(block.get("lines")):
        try:
            yield line_text(item)
        except SpecError:
            continue


def spoken_lines(spec: dict):
    """Yield (scene_index, block, text) for every spoken (talent) line."""
    for si, scene in enumerate(spec.get("scenes") or []):
        if not isinstance(scene, dict):
            continue
        for block in scene.get("blocks") or []:
            if isinstance(block, dict) and block.get("type") in SPOKEN:
                for kind, text in safe_lines(block):
                    if kind == "line":
                        yield si, block, text


def count_units(text: str, lang: str) -> int:
    """Words, or characters for scripts written without spaces."""
    b = base_lang(lang)
    clean = re.sub(r"[\"'“”‘’«»()\[\]…\.,،؛;:!?؟—–\-]", " ", text)
    if b in CHARS_PER_SEC:
        return sum(1 for ch in clean if not ch.isspace() and unicodedata.category(ch)[0] in "LN")
    return len([w for w in clean.split() if w.strip()])


def speech_seconds(text: str, lang: str, wps: float | None = None) -> float:
    b = base_lang(lang)
    units = count_units(text, lang)
    if b in CHARS_PER_SEC and not wps:
        return units / CHARS_PER_SEC[b]
    return units / (wps or WORDS_PER_SEC.get(b, DEFAULT_WPS))


SPOKEN = ("dialogue", "voiceover", "question")


def scene_has_words(scene: dict) -> bool:
    return any(isinstance(b, dict) and b.get("type") in SPOKEN + ("onscreen_text", "super") and b.get("lines")
               for b in scene.get("blocks") or [])


def estimate_scene_seconds(scene: dict, lang: str, wps: float | None = None) -> float:
    """duration_sec if given, else the printed `duration` ("6 sec"), else spoken time."""
    if not isinstance(scene, dict):
        return 0.0
    if isinstance(scene.get("duration_sec"), (int, float)):
        return float(scene["duration_sec"])
    total = 0.0
    for block in scene.get("blocks") or []:
        if isinstance(block, dict) and block.get("type") in SPOKEN:
            for kind, text in safe_lines(block):
                total += PAUSE_SEC if kind == "pause" else (speech_seconds(text, lang, wps) if kind == "line" else 0)
    printed = parse_duration(scene.get("duration"))
    return max(total, printed) if printed is not None else total


CONTENT_TYPES = ("reel", "ad", "long_form")


def content_type(spec: dict) -> str:
    brief = spec.get("brief") if isinstance(spec.get("brief"), dict) else {}
    ct = str(brief.get("content_type") or "reel").lower().replace("-", "_")
    return {"short": "reel", "short_form": "reel", "reels": "reel", "commercial": "ad", "ads": "ad",
            "long": "long_form", "longform": "long_form", "youtube": "long_form"}.get(ct, ct)


def fmt_tc(sec: float) -> str:
    sec = int(round(sec))
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def scene_starts(spec: dict, lang: str, wps=None) -> list:
    """Estimated start time (s) of every scene, in order."""
    t, out = 0.0, []
    for sc in as_list(spec.get("scenes")):
        out.append(t)
        t += estimate_scene_seconds(sc, lang, wps)
    return out


def cut_scene_indices(cut: dict, n_scenes: int) -> list:
    """1-based scene numbers of a cutdown. Only whole numbers (not bools, strings or 1.9)."""
    raw = as_list(cut.get("scenes"))
    if not raw:
        raise SpecError(f"cutdown '{cut.get('name')}' lists no scenes")
    out = []
    for n in raw:
        if isinstance(n, bool) or not isinstance(n, (int, float)) or int(n) != n:
            raise SpecError(f"cutdown '{cut.get('name')}': scene numbers must be whole numbers, got {n!r}")
        if not 1 <= int(n) <= n_scenes:
            raise SpecError(f"cutdown '{cut.get('name')}': scene {int(n)} doesn't exist (1–{n_scenes})")
        out.append(int(n))
    return out


def target_range(spec: dict) -> tuple[float, float] | None:
    brief = spec.get("brief") or {}
    d = brief.get("duration_sec")
    if isinstance(d, (int, float)):
        return float(d), float(d)
    if isinstance(d, list) and len(d) == 2:
        return float(d[0]), float(d[1])
    return None
