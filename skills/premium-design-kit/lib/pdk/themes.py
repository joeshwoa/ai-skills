"""Design tokens shared by every premium document skill (decks, documents, spreadsheets, courses).

A theme is a small design system: colours, fonts and a background recipe. `tokens(theme)` derives
everything a renderer needs for BOTH dark stages (slides) and light paper (documents/sheets), with
accents adjusted until they pass contrast on paper — so a dark slide theme still prints well.

Add a theme: append a dict to THEMES (hex without '#').
"""
from __future__ import annotations

import colorsys
import json
import os
from pathlib import Path

THEMES = [
    {
        "id": "onyx-gold", "name": "Onyx & Gold",
        "tagline": "Dark, premium, executive — board decks and investor pitches",
        "bg": "12141C", "bg_alt": "1E2233", "primary": "D4AF6A", "secondary": "8A93A8",
        "text_on_dark": "F5F1E8", "text_on_light": "12141C",
        "heading_font": "Georgia", "body_font": "Calibri", "style": "dark",
        "gradient_angle": 135, "glow": ["D4AF6A", "6B5B3A"], "grid_alpha": 22, "glow_alpha": 90,
    },
    {
        "id": "arctic-minimal", "name": "Arctic Minimal",
        "tagline": "Clean white space, one accent color — product & UX decks",
        "bg": "FFFFFF", "bg_alt": "E8EEF7", "primary": "2F6FED", "secondary": "5B6472",
        "text_on_dark": "FFFFFF", "text_on_light": "1B1E2B",
        "heading_font": "Helvetica", "body_font": "Helvetica", "style": "light",
        "gradient_angle": 160, "glow": ["2F6FED", "8FB5FF"], "grid_alpha": 14, "glow_alpha": 55,
    },
    {
        "id": "sunset-startup", "name": "Sunset Startup",
        "tagline": "Warm gradient energy — pitch decks and launch announcements",
        "bg": "1A1030", "bg_alt": "331B4D", "primary": "FF6B5B", "secondary": "FFC15E",
        "text_on_dark": "FFF7ED", "text_on_light": "1A1030",
        "heading_font": "Poppins", "body_font": "Poppins", "style": "dark",
        "gradient_angle": 120, "glow": ["FF6B5B", "FFC15E"], "grid_alpha": 16, "glow_alpha": 110,
    },
    {
        "id": "sage-editorial", "name": "Sage Editorial",
        "tagline": "Soft, calm, magazine-style — research & strategy decks",
        "bg": "F6F5EF", "bg_alt": "E4E9DE", "primary": "4B6B57", "secondary": "8A7F6A",
        "text_on_dark": "F6F5EF", "text_on_light": "27362E",
        "heading_font": "Georgia", "body_font": "Calibri", "style": "light",
        "gradient_angle": 150, "glow": ["4B6B57", "9CB89E"], "grid_alpha": 12, "glow_alpha": 50,
    },
    {
        "id": "cobalt-tech", "name": "Cobalt Tech",
        "tagline": "High-contrast, technical, confident — engineering & product reviews",
        "bg": "0B1220", "bg_alt": "16233F", "primary": "4CC2FF", "secondary": "7C8AA5",
        "text_on_dark": "E9F1FF", "text_on_light": "0B1220",
        "heading_font": "Calibri", "body_font": "Calibri", "style": "dark",
        "gradient_angle": 110, "glow": ["4CC2FF", "2A5C99"], "grid_alpha": 28, "glow_alpha": 100,
    },
    {
        "id": "ivory-luxe", "name": "Ivory Luxe",
        "tagline": "Understated luxury, lots of air — brand & agency decks",
        "bg": "FBF9F4", "bg_alt": "EFE6D2", "primary": "9A7B4F", "secondary": "6B6255",
        "text_on_dark": "FBF9F4", "text_on_light": "2A2620",
        "heading_font": "Georgia", "body_font": "Georgia", "style": "light",
        "gradient_angle": 140, "glow": ["9A7B4F", "D9C39A"], "grid_alpha": 10, "glow_alpha": 45,
    },
    {
        "id": "midnight-violet", "name": "Midnight Violet",
        "tagline": "Futuristic, moody, high-end — AI/product launch decks",
        "bg": "0D0B1E", "bg_alt": "241A3F", "primary": "B27CFF", "secondary": "6E67A8",
        "text_on_dark": "F1ECFF", "text_on_light": "0D0B1E",
        "heading_font": "Helvetica", "body_font": "Helvetica", "style": "dark",
        "gradient_angle": 125, "glow": ["B27CFF", "FF7CD1"], "grid_alpha": 20, "glow_alpha": 120,
    },
    {
        "id": "crimson-editorial", "name": "Crimson Editorial",
        "tagline": "Bold, high-contrast, magazine energy — brand statements & keynotes",
        "bg": "150707", "bg_alt": "2B0E0E", "primary": "E6483C", "secondary": "AD9A93",
        "text_on_dark": "F7EDEA", "text_on_light": "150707",
        "heading_font": "Georgia", "body_font": "Helvetica", "style": "dark",
        "gradient_angle": 100, "glow": ["E6483C", "8A1F1A"], "grid_alpha": 18, "glow_alpha": 100,
    },
    {
        "id": "mint-fresh", "name": "Mint Fresh",
        "tagline": "Light, clean, energizing — health, wellness & consumer decks",
        "bg": "F2FBF8", "bg_alt": "D8F0E6", "primary": "18A999", "secondary": "5E7A74",
        "text_on_dark": "F2FBF8", "text_on_light": "0E2E28",
        "heading_font": "Helvetica", "body_font": "Helvetica", "style": "light",
        "gradient_angle": 155, "glow": ["18A999", "7BE0C9"], "grid_alpha": 12, "glow_alpha": 55,
    },
    {
        "id": "graphite-mono", "name": "Graphite Mono",
        "tagline": "Near-monochrome, restrained, corporate — internal & governance decks",
        "bg": "1B1B1D", "bg_alt": "2C2C30", "primary": "E7E7EA", "secondary": "8C8C93",
        "text_on_dark": "F2F2F4", "text_on_light": "1B1B1D",
        "heading_font": "Helvetica", "body_font": "Helvetica", "style": "dark",
        "gradient_angle": 135, "glow": ["E7E7EA", "5A5A61"], "grid_alpha": 24, "glow_alpha": 60,
    },
    {
        "id": "blush-luxury", "name": "Blush Luxury",
        "tagline": "Soft rose-gold luxury — beauty, fashion & lifestyle brand decks",
        "bg": "FBF1F0", "bg_alt": "F3DEDB", "primary": "B5686E", "secondary": "8C7268",
        "text_on_dark": "FBF1F0", "text_on_light": "3A2223",
        "heading_font": "Georgia", "body_font": "Georgia", "style": "light",
        "gradient_angle": 145, "glow": ["B5686E", "E7B7AE"], "grid_alpha": 10, "glow_alpha": 50,
    },
    {
        "id": "forest-corporate", "name": "Forest Corporate",
        "tagline": "Deep green + gold, grounded and trustworthy — ESG & sustainability decks",
        "bg": "0B1F17", "bg_alt": "153327", "primary": "C9A24B", "secondary": "7FA08E",
        "text_on_dark": "EFF5F0", "text_on_light": "0B1F17",
        "heading_font": "Georgia", "body_font": "Calibri", "style": "dark",
        "gradient_angle": 130, "glow": ["C9A24B", "2E5C46"], "grid_alpha": 18, "glow_alpha": 85,
    },
    {
        "id": "azure-finance", "name": "Azure Finance",
        "tagline": "Conservative navy + azure — finance, banking & institutional decks",
        "bg": "F5F8FC", "bg_alt": "DCE6F5", "primary": "134A8C", "secondary": "51677F",
        "text_on_dark": "F5F8FC", "text_on_light": "0E2340",
        "heading_font": "Georgia", "body_font": "Calibri", "style": "light",
        "gradient_angle": 165, "glow": ["134A8C", "6FA0E0"], "grid_alpha": 14, "glow_alpha": 45,
    },
    {
        "id": "amber-warmth", "name": "Amber Warmth",
        "tagline": "Warm cream + burnt orange — editorial, lifestyle & culture decks",
        "bg": "FBF3E8", "bg_alt": "F1DDBE", "primary": "C1631E", "secondary": "8A6A4E",
        "text_on_dark": "FBF3E8", "text_on_light": "3A2510",
        "heading_font": "Georgia", "body_font": "Georgia", "style": "light",
        "gradient_angle": 150, "glow": ["C1631E", "F0A968"], "grid_alpha": 10, "glow_alpha": 55,
    },
    {
        "id": "neon-pulse", "name": "Neon Pulse",
        "tagline": "Near-black with neon glow — creative, gaming & entertainment decks",
        "bg": "07080D", "bg_alt": "10131F", "primary": "39FF9E", "secondary": "6F76A8",
        "text_on_dark": "EAFBF2", "text_on_light": "07080D",
        "heading_font": "Helvetica", "body_font": "Helvetica", "style": "dark",
        "gradient_angle": 115, "glow": ["39FF9E", "FF3EC9"], "grid_alpha": 26, "glow_alpha": 100,
    },
    {
        "id": "slate-professional", "name": "Slate Professional",
        "tagline": "Light slate + indigo — SaaS, enterprise & sales decks",
        "bg": "F7F8FA", "bg_alt": "E4E7EE", "primary": "4338CA", "secondary": "5B6472",
        "text_on_dark": "F7F8FA", "text_on_light": "1E2130",
        "heading_font": "Helvetica", "body_font": "Helvetica", "style": "light",
        "gradient_angle": 160, "glow": ["4338CA", "9C97F0"], "grid_alpha": 14, "glow_alpha": 55,
    },
    {
        "id": "neoai-dark", "name": "NeoAI Dark",
        "tagline": "Simple full-dark with NeoAI orange — event and speech decks",
        "bg": "0E1116", "bg_alt": "1A222D", "primary": "FF5A00", "secondary": "8B95A5",
        "text_on_dark": "F4F6F8", "text_on_light": "0E1116",
        "heading_font": "Helvetica", "body_font": "Helvetica", "style": "dark",
        "gradient_angle": 135, "glow": ["FF5A00", "1F3A5F"], "grid_alpha": 18, "glow_alpha": 70,
    },
    {
        "id": "neoai-light", "name": "NeoAI Light",
        "tagline": "Simple full-light with NeoAI orange — event and speech decks",
        "bg": "F6F7F9", "bg_alt": "E7ECF2", "primary": "E85D04", "secondary": "5B6573",
        "text_on_dark": "FFFFFF", "text_on_light": "161B22",
        "heading_font": "Helvetica", "body_font": "Helvetica", "style": "light",
        "gradient_angle": 155, "glow": ["FF5A00", "FFB27A"], "grid_alpha": 12, "glow_alpha": 45,
    },
    {
        "id": "ltc-academy", "name": "LTC Academy",
        "tagline": "Navy grid, orange and teal — LTC Academy course decks",
        "bg": "0B1533", "bg_alt": "152040", "primary": "FF7A1A", "secondary": "32C79A",
        "text_on_dark": "F7F8FC", "text_on_light": "0B1533",
        "heading_font": "Calibri", "body_font": "Calibri", "style": "dark",
        "gradient_angle": 155, "glow": ["FF7A1A", "32C79A"], "grid_alpha": 26, "glow_alpha": 70,
    },
    {
        "id": "donbosco-lab", "name": "Don Bosco Lab",
        "tagline": "Salesian navy, red, and gold — classroom teaching decks",
        "bg": "F7F3EC", "bg_alt": "FFFFFF", "primary": "C8102E", "secondary": "8A7348",
        "text_on_dark": "F7F3EC", "text_on_light": "161D32",
        "heading_font": "Calibri", "body_font": "Calibri", "style": "light",
        "gradient_angle": 160, "glow": ["C8102E", "B8965A"], "grid_alpha": 10, "glow_alpha": 36,
    },
]


# Neutral document-first themes (no brand). "plain-pro" is the default when nobody asked for a style.
THEMES += [
    {
        "id": "plain-pro", "name": "Plain Pro",
        "tagline": "Neutral, unbranded, crisp — the default for any document without a brand",
        "bg": "FFFFFF", "bg_alt": "EEF1F5", "primary": "1F4FD1", "secondary": "5A6472",
        "text_on_dark": "FFFFFF", "text_on_light": "151A22",
        "heading_font": "Helvetica", "body_font": "Helvetica", "style": "light",
        "gradient_angle": 160, "glow": ["1F4FD1", "8FB0FF"], "grid_alpha": 10, "glow_alpha": 30,
    },
    {
        "id": "paper-ink", "name": "Paper & Ink",
        "tagline": "Editorial black on warm paper with one red — reports, essays, books",
        "bg": "FBFAF7", "bg_alt": "EFEBE3", "primary": "C2271B", "secondary": "6B645A",
        "text_on_dark": "FBFAF7", "text_on_light": "141414",
        "heading_font": "Georgia", "body_font": "Georgia", "style": "light",
        "gradient_angle": 150, "glow": ["C2271B", "E9A39C"], "grid_alpha": 8, "glow_alpha": 28,
    },
    {
        "id": "school-bright", "name": "School Bright",
        "tagline": "Friendly blue + sunshine yellow — school lessons, worksheets, kids' material",
        "bg": "FFFFFF", "bg_alt": "E9F3FF", "primary": "1668E3", "secondary": "F5B700",
        "text_on_dark": "FFFFFF", "text_on_light": "14213D",
        "heading_font": "Helvetica", "body_font": "Helvetica", "style": "light",
        "gradient_angle": 160, "glow": ["1668E3", "F5B700"], "grid_alpha": 10, "glow_alpha": 40,
    },
    {
        "id": "royal-academic", "name": "Royal Academic",
        "tagline": "Navy and gold on ivory — university courses, certificates, formal programmes",
        "bg": "FCFBF7", "bg_alt": "EDE8DA", "primary": "17305E", "secondary": "B08D3C",
        "text_on_dark": "FCFBF7", "text_on_light": "111C33",
        "heading_font": "Georgia", "body_font": "Calibri", "style": "light",
        "gradient_angle": 155, "glow": ["17305E", "B08D3C"], "grid_alpha": 9, "glow_alpha": 35,
    },
]

ARABIC_FONTS = {
    # (heading, body). Cairo/Tajawal/IBM Plex Sans Arabic are free Google fonts (scripts/fonts.sh);
    # "Arial" is the safe fallback that exists with Arabic glyphs on every Mac/Windows PC.
    "modern": ("Cairo", "Tajawal"),
    "corporate": ("IBM Plex Sans Arabic", "IBM Plex Sans Arabic"),
    "classic": ("Amiri", "Noto Naskh Arabic"),
    "friendly": ("El Messiri", "Tajawal"),
    "safe": ("Arial", "Arial"),
}


def get_theme(theme_id: str) -> dict:
    for t in THEMES:
        if t["id"] == theme_id:
            return dict(t)
    raise ValueError(f"Unknown theme '{theme_id}'. Available: {', '.join(t['id'] for t in THEMES)}")


# ----------------------------------------------------------------------------------- colour maths
def hex_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_hex(rgb) -> str:
    return "".join(f"{max(0, min(255, int(round(c)))):02X}" for c in rgb)


def luminance(h: str) -> float:
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = hex_rgb(h)
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a: str, b: str) -> float:
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def mix(a: str, b: str, t: float) -> str:
    ra, rb = hex_rgb(a), hex_rgb(b)
    return rgb_hex([x * (1 - t) + y * t for x, y in zip(ra, rb)])


def shade_to_contrast(color: str, against: str, target: float = 4.5) -> str:
    """Darken (on light) or lighten (on dark) `color` keeping its hue until it reaches `target`."""
    if contrast(color, against) >= target:
        return color
    r, g, b = [c / 255 for c in hex_rgb(color)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    dark_bg = luminance(against) < 0.4
    for _ in range(60):
        l = min(1, l + 0.02) if dark_bg else max(0, l - 0.02)
        c = rgb_hex([x * 255 for x in colorsys.hls_to_rgb(h, l, s)])
        if contrast(c, against) >= target:
            return c
    return "FFFFFF" if dark_bg else "000000"


def readable_on(bg: str) -> str:
    return "FFFFFF" if contrast("FFFFFF", bg) >= contrast("111111", bg) else "111111"


# ----------------------------------------------------------------------------------------- tokens
def tokens(theme: dict, *, arabic: bool = False, arabic_style: str = "modern") -> dict:
    """Everything a renderer needs. Keys (hex without '#'):
    stage_bg, stage_bg_alt, stage_text (slides) · paper, paper_alt, ink, ink_soft, muted, line,
    accent (contrast ≥ 4.5 on paper), accent_2, accent_soft (tint for panels), on_accent ·
    head_font, body_font, mono_font · dir ('rtl'|'ltr') · align ('right'|'left')."""
    t = dict(theme)
    light = t.get("style") == "light"
    paper = t["bg"] if light else "FFFFFF"
    if luminance(paper) < 0.7:
        paper = "FFFFFF"
    ink = t["text_on_light"] if contrast(t["text_on_light"], paper) >= 7 else "151A22"
    accent = shade_to_contrast(t["primary"], paper, 4.5)
    accent2 = shade_to_contrast(t["secondary"], paper, 3.0)
    head, body = t["heading_font"], t["body_font"]
    if arabic:
        head, body = t.get("heading_font_ar") or ARABIC_FONTS.get(arabic_style, ARABIC_FONTS["modern"])[0], \
            t.get("body_font_ar") or ARABIC_FONTS.get(arabic_style, ARABIC_FONTS["modern"])[1]
    return {
        "id": t["id"], "name": t["name"],
        "stage_bg": t["bg"], "stage_bg_alt": t["bg_alt"],
        "stage_text": t["text_on_light"] if light else t["text_on_dark"],
        "stage_accent": t["primary"],
        "paper": paper, "paper_alt": mix(paper, t["bg_alt"] if light else t["primary"], 0.35 if light else 0.06),
        "ink": ink, "ink_soft": mix(ink, paper, 0.25), "muted": shade_to_contrast(mix(ink, paper, 0.45), paper, 4.5),
        "line": mix(ink, paper, 0.85),
        "accent": accent, "accent_2": accent2, "accent_soft": mix(accent, paper, 0.88),
        "on_accent": readable_on(accent),
        "head_font": head, "body_font": body,
        "head_font_latin": t["heading_font"], "body_font_latin": t["body_font"],
        "mono_font": "Consolas" if not arabic else "Consolas",
        "dir": "rtl" if arabic else "ltr", "align": "right" if arabic else "left",
        "style": t.get("style", "light"),
    }


# ------------------------------------------------------------------------------------- brand kits
def studio_home() -> Path | None:
    env = os.environ.get("STUDIO_HOME", "").strip()
    if env:
        return Path(env).expanduser()
    root = Path.home() / ".config" / "studio-mcp" / "root"
    if root.exists():
        try:
            return Path(root.read_text().strip()).expanduser()
        except Exception:
            pass
    for c in (Path.home() / "AI-Projects" / "creative-studio",):
        if c.exists():
            return c
    return None


def load_brand(brand) -> dict | None:
    """A brand from creative-studio (slug → STUDIO_HOME/brands/<slug>/brand.json), a folder, a
    brand.json path, or an inline dict. Returns None when brand is empty. Raises when not found."""
    if not brand:
        return None
    if isinstance(brand, dict):
        kit, base = dict(brand), Path.cwd()
    else:
        p = Path(str(brand)).expanduser()
        cands = [p / "brand.json", p] if p.suffix != ".json" else [p]
        sh = studio_home()
        if sh:
            cands.append(sh / "brands" / str(brand).strip().lower().replace(" ", "-") / "brand.json")
        f = next((c for c in cands if c.is_file()), None)
        if not f:
            raise FileNotFoundError(f"brand '{brand}' not found (looked in: {', '.join(map(str, cands))}). "
                                    "Make one with creative-studio (brand_create) or pass a brand.json.")
        kit, base = json.loads(f.read_text(encoding="utf-8")), f.parent
    kit["_dir"] = str(base)
    return kit


def theme_from_brand(kit: dict, *, dark: bool = False) -> dict:
    """Turn a brand kit into a theme dict usable everywhere a theme id is accepted."""
    c = kit.get("colors", {})
    f = kit.get("fonts", {})
    primary = (c.get("primary") or "1F4FD1").lstrip("#")
    secondary = (c.get("secondary") or c.get("accent") or "5A6472").lstrip("#")
    ink = (c.get("ink") or "151A22").lstrip("#")
    paper = (c.get("paper") or "FFFFFF").lstrip("#")
    surface = (c.get("surface") or mix(paper, primary, 0.08)).lstrip("#")
    logo = None
    files = (kit.get("logo") or {}).get("png") or (kit.get("logo") or {}).get("files") or {}
    for k in ("horizontal", "primary", "mark", "icon"):
        if files.get(k):
            logo = str(Path(kit.get("_dir", ".")) / files[k])
            break
    th = {
        "id": f"brand-{kit.get('slug') or 'custom'}", "name": kit.get("name") or "Brand",
        "tagline": kit.get("tagline") or "Brand theme",
        "bg": ink if dark else paper, "bg_alt": mix(ink, primary, 0.25) if dark else surface,
        "primary": primary, "secondary": secondary,
        "text_on_dark": paper if luminance(paper) > 0.6 else "FFFFFF", "text_on_light": ink,
        "heading_font": f.get("head") or "Helvetica", "body_font": f.get("body") or "Helvetica",
        "heading_font_ar": f.get("head_ar"), "body_font_ar": f.get("body_ar"),
        "style": "dark" if dark else "light",
        "gradient_angle": 140, "glow": [primary, secondary], "grid_alpha": 12 if not dark else 20,
        "glow_alpha": 40 if not dark else 85, "logo": logo, "brand": kit.get("slug"),
    }
    return th


def resolve_theme(theme=None, brand=None, *, dark: bool | None = None, default: str = "plain-pro") -> dict:
    """theme id / theme dict / brand → theme dict. A brand always wins over a theme id."""
    kit = load_brand(brand) if brand else None
    if kit:
        return theme_from_brand(kit, dark=bool(dark))
    if isinstance(theme, dict):
        base = get_theme(theme["base"]) if theme.get("base") else get_theme(default)
        base.update({k: v.lstrip("#") if isinstance(v, str) and k in ("bg", "bg_alt", "primary", "secondary", "text_on_dark", "text_on_light") else v for k, v in theme.items() if k != "base"})
        return base
    return get_theme(theme or default)
