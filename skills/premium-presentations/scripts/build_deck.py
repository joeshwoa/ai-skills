#!/usr/bin/env python3
"""
build_deck.py — turns a JSON "deck spec" into a fully editable, themed .pptx.

Usage:
    python3 build_deck.py deck_spec.json output.pptx

Why python-pptx directly (not HTML->PPTX conversion): HTML/LibreOffice
conversion flattens most text into images or uneditable boxes. Building
the deck natively with python-pptx keeps every title, bullet, and table
cell as real, editable PowerPoint text — which is the #1 requirement
for this skill ("fully editable"). The HTML renderer (render_preview.py)
reads the *same* deck spec + theme so the web preview and the .pptx
always match, and gives you rich CSS animations for previewing/PDF.

Deck spec schema: see ../references/deck_spec_schema.md
"""
import json
import sys
import tempfile
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

sys.path.insert(0, str(Path(__file__).parent))
from themes import get_theme, render_background_png

SLIDE_W = Inches(13.333)  # 16:9
SLIDE_H = Inches(7.5)

# One background PNG per (theme, variant) is plenty to render every slide
# in a deck sharply — generating 9 originals per deck instead of one per
# slide would just waste build time for a pixel-identical result.
_BG_CACHE = {}


def rgb(hexstr):
    return RGBColor.from_string(hexstr)


HERO_TYPES = {"title", "section", "closing"}


def set_background(slide, theme, variant):
    """Stamps the theme's generated gradient+grid+glow art as a full-bleed
    picture behind the slide's content, instead of a flat solid fill —
    flat fills are what make a deck look like a default template."""
    key = (theme["id"], variant)
    if key not in _BG_CACHE:
        tmp_dir = Path(tempfile.gettempdir()) / "premium_presentations_bg"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        path = tmp_dir / f"{theme['id']}_{variant}.png"
        if not path.exists():
            render_background_png(theme, variant, str(path))
        _BG_CACHE[key] = str(path)
    slide.shapes.add_picture(_BG_CACHE[key], 0, 0, width=SLIDE_W, height=SLIDE_H)


def add_transition(slide, kind="fade", duration_ms=700):
    """python-pptx has no public API for slide transitions, so we inject the
    <p:transition> element directly into the slide XML. 'fade' and 'push'
    render correctly in PowerPoint, Keynote, and Google Slides."""
    sld = slide._element
    existing = sld.find(qn('p:transition'))
    if existing is not None:
        sld.remove(existing)
    transition = etree.SubElement(sld, qn('p:transition'))
    transition.set('spd', 'med')
    transition.set('dur', str(duration_ms))
    effect_tag = {
        "fade": qn('p:fade'),
        "push": qn('p:push'),
        "wipe": qn('p:wipe'),
        "cut": None,
    }.get(kind)
    if effect_tag is not None:
        etree.SubElement(transition, effect_tag)


def add_textbox(slide, x, y, w, h, align=PP_ALIGN.LEFT, anchor_top=True):
    """Every textbox in this file goes through here. This matters more than
    it looks: if word_wrap / auto_size are left at python-pptx's defaults,
    LibreOffice (and some other renderers) silently auto-shrinks the box to
    fit its text and re-centers it around the *original* box's center —
    which quietly breaks left-alignment even though nothing in the XML looks
    wrong. Pinning word_wrap=True and auto_size=NONE makes every renderer
    respect the exact box you placed."""
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.paragraphs[0].alignment = align
    return box, tf


def style_run(run, font_name, size, color_hex, bold=False, italic=False):
    run.font.name = font_name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = rgb(color_hex)


def add_footer(slide, theme, page_num, total, footer_text=""):
    _, tf = add_textbox(slide, Inches(0.5), SLIDE_H - Inches(0.45), Inches(8), Inches(0.35))
    tf.text = footer_text
    style_run(tf.paragraphs[0].runs[0], theme["body_font"], 10, theme["secondary"])

    _, tf2 = add_textbox(slide, SLIDE_W - Inches(1.6), SLIDE_H - Inches(0.45), Inches(1.2), Inches(0.35),
                          align=PP_ALIGN.RIGHT)
    tf2.text = f"{page_num:02d} / {total:02d}"
    style_run(tf2.paragraphs[0].runs[0], theme["body_font"], 10, theme["secondary"])


def add_accent_bar(slide, theme, x=Inches(0.5), y=Inches(1.15), width=Inches(0.9), height=Pt(4)):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, width, height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = rgb(theme["primary"])
    bar.line.fill.background()
    bar.shadow.inherit = False


# ---------------------------------------------------------------- slide types

def slide_title(prs, theme, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout
    set_background(slide, theme, "hero")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]

    if spec.get("kicker"):
        _, tf = add_textbox(slide, Inches(0.9), Inches(2.1), Inches(11.5), Inches(0.5))
        tf.text = spec["kicker"].upper()
        style_run(tf.paragraphs[0].runs[0], theme["body_font"], 14, theme["primary"], bold=True)

    _, tf = add_textbox(slide, Inches(0.9), Inches(2.6), Inches(11.5), Inches(1.8))
    tf.text = spec["title"]
    style_run(tf.paragraphs[0].runs[0], theme["heading_font"], 44, text_color, bold=True)

    if spec.get("subtitle"):
        _, tf = add_textbox(slide, Inches(0.9), Inches(4.2), Inches(10.5), Inches(1.0))
        tf.text = spec["subtitle"]
        style_run(tf.paragraphs[0].runs[0], theme["body_font"], 20, theme["secondary"])

    add_accent_bar(slide, theme, y=Inches(2.35))
    return slide


def slide_section(prs, theme, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "hero")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]

    _, tf = add_textbox(slide, Inches(0.9), Inches(2.6), Inches(3), Inches(1.5))
    tf.text = spec.get("number", "")
    style_run(tf.paragraphs[0].runs[0], theme["heading_font"], 72, theme["primary"], bold=True)

    _, tf = add_textbox(slide, Inches(0.9), Inches(3.9), Inches(10.5), Inches(1.2))
    tf.text = spec["title"]
    style_run(tf.paragraphs[0].runs[0], theme["heading_font"], 36, text_color, bold=True)
    return slide


def slide_bullets(prs, theme, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "content")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]

    _, tf = add_textbox(slide, Inches(0.7), Inches(0.5), Inches(11.9), Inches(0.9))
    tf.text = spec["title"]
    style_run(tf.paragraphs[0].runs[0], theme["heading_font"], 30, text_color, bold=True)
    add_accent_bar(slide, theme)

    _, tf = add_textbox(slide, Inches(0.9), Inches(1.7), Inches(11.5), Inches(5.2))
    for i, bullet in enumerate(spec.get("bullets", [])):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(14)
        if isinstance(bullet, dict):
            head, detail = bullet.get("point", ""), bullet.get("detail", "")
        else:
            head, detail = bullet, ""
        run = p.add_run()
        run.text = f"●  {head}"
        style_run(run, theme["body_font"], 19, text_color, bold=bool(detail))
        if detail:
            p2 = tf.add_paragraph()
            p2.alignment = PP_ALIGN.LEFT
            p2.space_after = Pt(10)
            r2 = p2.add_run()
            r2.text = f"     {detail}"
            style_run(r2, theme["body_font"], 15, theme["secondary"])
    return slide


def slide_stats(prs, theme, spec):
    """Row of big KPI numbers — common in investor / QBR decks."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "content")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]

    _, tf = add_textbox(slide, Inches(0.7), Inches(0.5), Inches(11.9), Inches(0.9))
    tf.text = spec["title"]
    style_run(tf.paragraphs[0].runs[0], theme["heading_font"], 30, text_color, bold=True)
    add_accent_bar(slide, theme)

    stats = spec.get("stats", [])
    n = max(len(stats), 1)
    col_w = Inches(11.5) / n
    for i, s in enumerate(stats):
        x = Inches(0.9) + col_w * i
        _, tf = add_textbox(slide, x, Inches(2.4), col_w - Inches(0.3), Inches(1.4))
        tf.text = str(s.get("value", ""))
        style_run(tf.paragraphs[0].runs[0], theme["heading_font"], 40, theme["primary"], bold=True)

        _, tf2 = add_textbox(slide, x, Inches(3.8), col_w - Inches(0.3), Inches(1.0))
        tf2.text = str(s.get("label", ""))
        style_run(tf2.paragraphs[0].runs[0], theme["body_font"], 16, theme["secondary"])
    return slide


def slide_quote(prs, theme, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "content")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]

    _, tf = add_textbox(slide, Inches(1.5), Inches(2.2), Inches(10.3), Inches(2.4))
    tf.text = f"“{spec['quote']}”"
    style_run(tf.paragraphs[0].runs[0], theme["heading_font"], 28, text_color, italic=True)

    if spec.get("attribution"):
        _, tf2 = add_textbox(slide, Inches(1.5), Inches(4.8), Inches(10.3), Inches(0.6))
        tf2.text = f"— {spec['attribution']}"
        style_run(tf2.paragraphs[0].runs[0], theme["body_font"], 16, theme["primary"])
    return slide


def slide_table(prs, theme, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "content")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]

    _, tf = add_textbox(slide, Inches(0.7), Inches(0.5), Inches(11.9), Inches(0.9))
    tf.text = spec["title"]
    style_run(tf.paragraphs[0].runs[0], theme["heading_font"], 30, text_color, bold=True)
    add_accent_bar(slide, theme)

    headers = spec["headers"]
    rows = spec["rows"]
    n_rows, n_cols = len(rows) + 1, len(headers)
    table_shape = slide.shapes.add_table(
        n_rows, n_cols, Inches(0.9), Inches(1.8), Inches(11.5), Inches(0.5) * n_rows
    )
    table = table_shape.table
    for c, h in enumerate(headers):
        cell = table.cell(0, c)
        cell.text = str(h)
        cell.fill.solid()
        cell.fill.fore_color.rgb = rgb(theme["primary"])
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        style_run(p.runs[0], theme["body_font"], 14,
                   theme["bg"] if theme["style"] == "dark" else "FFFFFF", bold=True)
    for r, row in enumerate(rows, start=1):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = str(val)
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(theme["bg_alt"] if r % 2 == 0 else theme["bg"])
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT
            style_run(p.runs[0], theme["body_font"], 13, text_color)
    return slide


def slide_closing(prs, theme, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "hero")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]

    _, tf = add_textbox(slide, Inches(0.9), Inches(2.9), Inches(11.5), Inches(1.2))
    tf.text = spec.get("title", "Thank you")
    style_run(tf.paragraphs[0].runs[0], theme["heading_font"], 40, text_color, bold=True)

    if spec.get("contact"):
        _, tf2 = add_textbox(slide, Inches(0.9), Inches(4.1), Inches(10.5), Inches(0.8))
        tf2.text = spec["contact"]
        style_run(tf2.paragraphs[0].runs[0], theme["body_font"], 18, theme["primary"])
    add_accent_bar(slide, theme, y=Inches(2.65))
    return slide


SLIDE_BUILDERS = {
    "title": slide_title,
    "section": slide_section,
    "bullets": slide_bullets,
    "stats": slide_stats,
    "quote": slide_quote,
    "table": slide_table,
    "closing": slide_closing,
}


def build(deck_spec_path: str, out_path: str):
    spec = json.loads(Path(deck_spec_path).read_text(encoding="utf-8"))
    theme = get_theme(spec["theme"])

    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    slides_spec = spec["slides"]
    total = len(slides_spec)
    transition = spec.get("transition", "fade")

    for i, s in enumerate(slides_spec, start=1):
        builder = SLIDE_BUILDERS.get(s["type"])
        if builder is None:
            raise ValueError(f"Unknown slide type '{s['type']}' (slide {i})")
        slide = builder(prs, theme, s)
        if s["type"] not in ("title",):
            add_footer(slide, theme, i, total, footer_text=spec.get("footer", ""))
        add_transition(slide, kind=transition)

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    prs.save(out_path)
    print(f"Wrote {out_path}  ({total} slides, theme={theme['id']})")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 build_deck.py deck_spec.json output.pptx")
        sys.exit(1)
    build(sys.argv[1], sys.argv[2])
