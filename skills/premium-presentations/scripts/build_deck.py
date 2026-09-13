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

ALWAYS run scripts/validate_deck.py on the output before handing a deck
over — see SKILL.md's "Check it before you hand it over" step. It caught
real bugs during this skill's own development (a too-tight section-number
box, an empty-footer crash) that eyeballing a few slides missed.

Deck spec schema: see ../references/deck_spec_schema.md
"""
import json
import math
import sys
import tempfile
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

sys.path.insert(0, str(Path(__file__).parent))
from themes import get_theme, render_background_png

SLIDE_W = Inches(13.333)  # 16:9
SLIDE_H = Inches(7.5)

# One background PNG per (theme, variant) is plenty to render every slide
# in a deck sharply — generating one per slide would just waste build time
# for a pixel-identical result.
_BG_CACHE = {}


def rgb(hexstr):
    return RGBColor.from_string(hexstr)


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


def add_textbox(slide, x, y, w, h, align=PP_ALIGN.LEFT, anchor=None):
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
    if anchor is not None:
        tf.vertical_anchor = anchor
    tf.paragraphs[0].alignment = align
    return box, tf


def set_text(tf, text, align=None):
    """Use instead of `tf.text = text`. python-pptx's tf.text setter leaves a
    paragraph with ZERO runs when text is an empty string — style_run() then
    crashes on paragraphs[0].runs[0]. This always leaves exactly one real run
    to style, even for "" (a deck that omits an optional field, e.g. no
    footer, must never crash the build). Returns the run."""
    p = tf.paragraphs[0]
    if align is not None:
        p.alignment = align
    run = p.add_run()
    run.text = text if text is not None else ""
    return run


def style_run(run, font_name, size, color_hex, bold=False, italic=False):
    run.font.name = font_name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = rgb(color_hex)


def add_footer(slide, theme, page_num, total, footer_text=""):
    if footer_text:
        _, tf = add_textbox(slide, Inches(0.5), SLIDE_H - Inches(0.45), Inches(8), Inches(0.35))
        style_run(set_text(tf, footer_text), theme["body_font"], 10, theme["secondary"])

    _, tf2 = add_textbox(slide, SLIDE_W - Inches(1.6), SLIDE_H - Inches(0.45), Inches(1.2), Inches(0.35),
                          align=PP_ALIGN.RIGHT)
    style_run(set_text(tf2, f"{page_num:02d} / {total:02d}"), theme["body_font"], 10, theme["secondary"])


def add_accent_bar(slide, theme, x=Inches(0.5), y=Inches(1.15), width=Inches(0.9), height=Pt(4)):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, width, height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = rgb(theme["primary"])
    bar.line.fill.background()
    bar.shadow.inherit = False
    return bar


def add_line(slide, x, y, w, h, color_hex):
    """A thin filled rectangle used as a connector/divider line — simpler and
    more predictable across renderers than python-pptx's connector shapes."""
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    line.fill.solid()
    line.fill.fore_color.rgb = rgb(color_hex)
    line.line.fill.background()
    line.shadow.inherit = False
    return line


def add_circle(slide, cx, cy, diameter, fill_hex):
    d = diameter
    circ = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx - d // 2, cy - d // 2, d, d)
    circ.fill.solid()
    circ.fill.fore_color.rgb = rgb(fill_hex)
    circ.line.fill.background()
    circ.shadow.inherit = False
    return circ


def add_panel(slide, x, y, w, h, fill_hex):
    panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    try:
        panel.adjustments[0] = 0.06
    except Exception:
        pass
    panel.fill.solid()
    panel.fill.fore_color.rgb = rgb(fill_hex)
    panel.line.fill.background()
    panel.shadow.inherit = False
    return panel


def header(slide, theme, title, text_color):
    """Shared title + accent bar used by every content-slide layout, so
    every slide type lines up on the same grid."""
    _, tf = add_textbox(slide, Inches(0.7), Inches(0.5), Inches(11.9), Inches(0.9))
    style_run(set_text(tf, title), theme["heading_font"], 30, text_color, bold=True)
    add_accent_bar(slide, theme)


# ---------------------------------------------------------------- slide types

def slide_title(prs, theme, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout
    set_background(slide, theme, "hero")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]

    if spec.get("kicker"):
        _, tf = add_textbox(slide, Inches(0.9), Inches(2.05), Inches(11.5), Inches(0.4))
        style_run(set_text(tf, spec["kicker"].upper()), theme["body_font"], 14, theme["primary"], bold=True)

    # 1.7in comfortably fits a 44pt title up to 2 wrapped lines without the
    # box reaching into the subtitle's box below (validate_deck.py checks this).
    _, tf = add_textbox(slide, Inches(0.9), Inches(2.5), Inches(11.5), Inches(1.7))
    style_run(set_text(tf, spec["title"]), theme["heading_font"], 44, text_color, bold=True)

    if spec.get("subtitle"):
        _, tf = add_textbox(slide, Inches(0.9), Inches(4.35), Inches(10.5), Inches(1.1))
        style_run(set_text(tf, spec["subtitle"]), theme["body_font"], 20, theme["secondary"])

    add_accent_bar(slide, theme, y=Inches(2.28))
    return slide


def slide_section(prs, theme, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "hero")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]

    # 72pt digits need ~1.4in of real box height (glyph + leading + margins).
    _, tf = add_textbox(slide, Inches(0.9), Inches(2.35), Inches(3), Inches(1.45))
    style_run(set_text(tf, spec.get("number", "")), theme["heading_font"], 72, theme["primary"], bold=True)

    _, tf = add_textbox(slide, Inches(0.9), Inches(3.95), Inches(10.5), Inches(1.3))
    style_run(set_text(tf, spec["title"]), theme["heading_font"], 36, text_color, bold=True)
    return slide


def slide_bullets(prs, theme, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "content")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]
    header(slide, theme, spec["title"], text_color)

    _, tf = add_textbox(slide, Inches(0.9), Inches(1.7), Inches(11.5), Inches(5.2))
    bullets = spec.get("bullets", [])
    for i, bullet in enumerate(bullets):
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
    header(slide, theme, spec["title"], text_color)

    stats = spec.get("stats", [])
    n = max(len(stats), 1)
    col_w = Inches(11.5) / n
    for i, s in enumerate(stats):
        x = Inches(0.9) + col_w * i
        _, tf = add_textbox(slide, x, Inches(2.4), col_w - Inches(0.3), Inches(1.4))
        style_run(set_text(tf, str(s.get("value", ""))), theme["heading_font"], 40, theme["primary"], bold=True)

        _, tf2 = add_textbox(slide, x, Inches(3.8), col_w - Inches(0.3), Inches(1.0))
        style_run(set_text(tf2, str(s.get("label", ""))), theme["body_font"], 16, theme["secondary"])
    return slide


def slide_quote(prs, theme, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "content")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]

    _, tf = add_textbox(slide, Inches(1.5), Inches(2.2), Inches(10.3), Inches(2.4))
    style_run(set_text(tf, f"“{spec['quote']}”"), theme["heading_font"], 28, text_color, italic=True)

    if spec.get("attribution"):
        _, tf2 = add_textbox(slide, Inches(1.5), Inches(4.8), Inches(10.3), Inches(0.6))
        style_run(set_text(tf2, f"— {spec['attribution']}"), theme["body_font"], 16, theme["primary"])
    return slide


def slide_table(prs, theme, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "content")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]
    header(slide, theme, spec["title"], text_color)

    headers_ = spec["headers"]
    rows = spec["rows"]
    n_rows, n_cols = len(rows) + 1, len(headers_)
    table_shape = slide.shapes.add_table(
        n_rows, n_cols, Inches(0.9), Inches(1.8), Inches(11.5), Inches(0.5) * n_rows
    )
    table = table_shape.table
    for c, h in enumerate(headers_):
        cell = table.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = rgb(theme["primary"])
        style_run(set_text(cell.text_frame, str(h), align=PP_ALIGN.LEFT), theme["body_font"], 14,
                   theme["bg"] if theme["style"] == "dark" else "FFFFFF", bold=True)
    for r, row in enumerate(rows, start=1):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(theme["bg_alt"] if r % 2 == 0 else theme["bg"])
            style_run(set_text(cell.text_frame, str(val), align=PP_ALIGN.LEFT), theme["body_font"], 13, text_color)
    return slide


def slide_closing(prs, theme, spec):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "hero")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]

    _, tf = add_textbox(slide, Inches(0.9), Inches(2.9), Inches(11.5), Inches(1.2))
    style_run(set_text(tf, spec.get("title", "Thank you")), theme["heading_font"], 40, text_color, bold=True)

    if spec.get("contact"):
        _, tf2 = add_textbox(slide, Inches(0.9), Inches(4.1), Inches(10.5), Inches(0.8))
        style_run(set_text(tf2, spec["contact"]), theme["body_font"], 18, theme["primary"])
    add_accent_bar(slide, theme, y=Inches(2.65))
    return slide


def slide_agenda(prs, theme, spec):
    """A numbered list with more air than `bullets` — for a talk outline or
    table of contents, not for dense supporting detail."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "content")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]
    header(slide, theme, spec.get("title", "Agenda"), text_color)

    items = spec.get("items", [])
    n = max(len(items), 1)
    top, bottom = 1.85, 6.9
    row_h = (bottom - top) / n
    font_size = 20 if n <= 5 else (16 if n <= 8 else 13)
    for i, item in enumerate(items):
        y = Inches(top + i * row_h)
        _, tf_num = add_textbox(slide, Inches(0.9), y, Inches(1.1), Inches(row_h - 0.08),
                                 anchor=MSO_ANCHOR.MIDDLE)
        style_run(set_text(tf_num, f"{i+1:02d}"), theme["heading_font"], font_size + 4, theme["primary"], bold=True)

        _, tf_item = add_textbox(slide, Inches(2.15), y, Inches(10.0), Inches(row_h - 0.08),
                                  anchor=MSO_ANCHOR.MIDDLE)
        style_run(set_text(tf_item, str(item)), theme["body_font"], font_size, text_color)

        if i < n - 1:
            add_line(slide, Inches(0.9), Inches(top + (i + 1) * row_h), Inches(10.5), Pt(0.75), theme["secondary"])
    return slide


def slide_two_column(prs, theme, spec):
    """Two independent lists side by side — problem/solution, before/after
    in plain text, current-state/future-state, etc."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "content")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]
    header(slide, theme, spec["title"], text_color)

    def column(x, heading, items):
        cursor = 1.9
        if heading:
            _, tf = add_textbox(slide, Inches(x), Inches(cursor), Inches(5.3), Inches(0.5))
            style_run(set_text(tf, heading), theme["heading_font"], 18, theme["primary"], bold=True)
            cursor += 0.65
        _, tf = add_textbox(slide, Inches(x), Inches(cursor), Inches(5.3), Inches(6.9 - cursor))
        for i, it in enumerate(items):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = PP_ALIGN.LEFT
            p.space_after = Pt(12)
            r = p.add_run()
            r.text = f"—  {it}"
            style_run(r, theme["body_font"], 16, text_color)

    column(0.9, spec.get("left_heading", ""), spec.get("left_items", []))
    column(6.9, spec.get("right_heading", ""), spec.get("right_items", []))
    add_line(slide, Inches(6.6), Inches(1.9), Pt(1), Inches(4.9), theme["secondary"])
    return slide


def slide_comparison(prs, theme, spec):
    """Two labeled cards for a direct A/B — before/after, us/them, current
    plan/proposed plan. More visually distinct than two_column's plain split."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "content")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]
    header(slide, theme, spec["title"], text_color)

    card_y, card_h, card_w, gap = 1.85, 4.95, 5.6, 0.33
    left_x, right_x = 0.7, 0.7 + card_w + gap

    def card(x, label, points, header_fill, header_text_color, body_fill):
        add_panel(slide, Inches(x), Inches(card_y), Inches(card_w), Inches(card_h), body_fill)
        strip = add_panel(slide, Inches(x), Inches(card_y), Inches(card_w), Inches(0.7), header_fill)
        _, tf = add_textbox(slide, Inches(x + 0.3), Inches(card_y), Inches(card_w - 0.6), Inches(0.7),
                             anchor=MSO_ANCHOR.MIDDLE)
        style_run(set_text(tf, label.upper()), theme["body_font"], 16, header_text_color, bold=True)
        _, tf2 = add_textbox(slide, Inches(x + 0.3), Inches(card_y + 0.9), Inches(card_w - 0.6),
                              Inches(card_h - 1.1))
        for i, pt in enumerate(points):
            p = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
            p.alignment = PP_ALIGN.LEFT
            p.space_after = Pt(10)
            r = p.add_run()
            r.text = f"•  {pt}"
            style_run(r, theme["body_font"], 15, text_color)

    header_text_on_primary = theme["bg"] if theme["style"] == "dark" else "FFFFFF"
    card(left_x, spec.get("left_label", "Before"), spec.get("left_points", []),
         theme["secondary"], theme["bg"] if theme["style"] == "dark" else "FFFFFF", theme["bg_alt"])
    card(right_x, spec.get("right_label", "After"), spec.get("right_points", []),
         theme["primary"], header_text_on_primary, theme["bg_alt"])
    return slide


def slide_timeline(prs, theme, spec):
    """A horizontal chronological line with milestones — roadmap, history,
    launch schedule."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "content")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]
    header(slide, theme, spec["title"], text_color)

    milestones = spec.get("milestones", [])
    n = max(len(milestones), 1)
    line_y, x0, x1 = 4.2, 1.3, 12.0
    add_line(slide, Inches(x0), Inches(line_y), Inches(x1 - x0), Pt(2.5), theme["primary"])

    span = (x1 - x0) / max(n - 1, 1) if n > 1 else 0
    box_w = min(2.3, span if n > 1 else 4.0)
    for i, m in enumerate(milestones):
        cx = x0 + (span * i if n > 1 else (x1 - x0) / 2)
        add_circle(slide, Inches(cx), Inches(line_y + 0.0125), Inches(0.22), theme["primary"])
        _, tf_l = add_textbox(slide, Inches(cx - box_w / 2), Inches(line_y - 1.0), Inches(box_w), Inches(0.85),
                               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM)
        style_run(set_text(tf_l, str(m.get("label", "")), align=PP_ALIGN.CENTER),
                  theme["heading_font"], 15, theme["primary"], bold=True)
        _, tf_t = add_textbox(slide, Inches(cx - box_w / 2), Inches(line_y + 0.3), Inches(box_w), Inches(1.4),
                               align=PP_ALIGN.CENTER)
        style_run(set_text(tf_t, str(m.get("text", "")), align=PP_ALIGN.CENTER), theme["body_font"], 13, text_color)
    return slide


def slide_process(prs, theme, spec):
    """Numbered circles for a how-it-works / step-by-step flow — distinct
    from `timeline` (which is chronological/dated) by reading as ordered
    steps rather than a calendar."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "content")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]
    header(slide, theme, spec["title"], text_color)

    steps = spec.get("steps", [])
    n = max(len(steps), 1)
    y_center, diameter, x0, x1 = 3.0, 1.05, 1.6, 11.7
    span = (x1 - x0) / max(n - 1, 1) if n > 1 else 0
    if n > 1:
        add_line(slide, Inches(x0), Inches(y_center - 0.02), Inches(x1 - x0), Pt(2), theme["secondary"])

    box_w = min(2.6, max(span, 1.8) if n > 1 else 4.0)
    circle_text_color = theme["bg"] if theme["style"] == "dark" else "FFFFFF"
    for i, s in enumerate(steps):
        cx = x0 + (span * i if n > 1 else (x1 - x0) / 2)
        add_circle(slide, Inches(cx), Inches(y_center), Inches(diameter), theme["primary"])
        _, tf_n = add_textbox(slide, Inches(cx - diameter / 2), Inches(y_center - diameter / 2),
                               Inches(diameter), Inches(diameter), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        style_run(set_text(tf_n, str(s.get("number", i + 1)), align=PP_ALIGN.CENTER),
                  theme["heading_font"], 26, circle_text_color, bold=True)

        _, tf_l = add_textbox(slide, Inches(cx - box_w / 2), Inches(y_center + diameter / 2 + 0.25),
                               Inches(box_w), Inches(0.5), align=PP_ALIGN.CENTER)
        style_run(set_text(tf_l, str(s.get("label", "")), align=PP_ALIGN.CENTER),
                  theme["heading_font"], 16, text_color, bold=True)
        _, tf_d = add_textbox(slide, Inches(cx - box_w / 2), Inches(y_center + diameter / 2 + 0.8),
                               Inches(box_w), Inches(1.6), align=PP_ALIGN.CENTER)
        style_run(set_text(tf_d, str(s.get("detail", "")), align=PP_ALIGN.CENTER), theme["body_font"], 13,
                  theme["secondary"])
    return slide


def slide_big_statement(prs, theme, spec):
    """One huge, unavoidable line — a milestone number, a mission statement,
    a single hard-hitting claim. Use sparingly, once or twice a deck."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "hero")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]

    statement = spec["statement"]
    size = 54 if len(statement) < 40 else (40 if len(statement) < 80 else 30)
    box_h = 2.6 if size >= 40 else 3.2
    _, tf = add_textbox(slide, Inches(1.15), Inches(2.6), Inches(11.0), Inches(box_h),
                         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    style_run(set_text(tf, statement, align=PP_ALIGN.CENTER), theme["heading_font"], size, text_color, bold=True)

    if spec.get("support"):
        _, tf2 = add_textbox(slide, Inches(1.65), Inches(2.6 + box_h + 0.1), Inches(10.0), Inches(0.9),
                              align=PP_ALIGN.CENTER)
        style_run(set_text(tf2, spec["support"], align=PP_ALIGN.CENTER), theme["body_font"], 18, theme["primary"])
    return slide


def slide_team(prs, theme, spec):
    """A grid of people — initials in a colored circle stand in for headshots
    since this skill never fabricates photos of real people."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "content")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]
    header(slide, theme, spec.get("title", "Team"), text_color)

    people = spec.get("people", [])
    n = max(len(people), 1)
    cols = min(n, 5)
    rows_n = math.ceil(n / cols)
    card_w = 11.4 / cols
    row_h = min(2.7, (6.9 - 1.9) / rows_n)
    avatar_d = 1.0
    circle_text_color = theme["bg"] if theme["style"] == "dark" else "FFFFFF"

    for i, person in enumerate(people):
        col, row = i % cols, i // cols
        cx = 0.9 + card_w * col + card_w / 2
        top = 2.0 + row * row_h
        initials = "".join(w[0].upper() for w in str(person.get("name", "?")).split()[:2]) or "?"
        add_circle(slide, Inches(cx), Inches(top + avatar_d / 2), Inches(avatar_d), theme["primary"])
        _, tf_i = add_textbox(slide, Inches(cx - avatar_d / 2), Inches(top), Inches(avatar_d), Inches(avatar_d),
                               align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        style_run(set_text(tf_i, initials, align=PP_ALIGN.CENTER), theme["heading_font"], 22, circle_text_color,
                  bold=True)

        _, tf_n = add_textbox(slide, Inches(cx - card_w / 2 + 0.1), Inches(top + avatar_d + 0.15),
                               Inches(card_w - 0.2), Inches(0.45), align=PP_ALIGN.CENTER)
        style_run(set_text(tf_n, str(person.get("name", "")), align=PP_ALIGN.CENTER),
                  theme["heading_font"], 15, text_color, bold=True)
        _, tf_r = add_textbox(slide, Inches(cx - card_w / 2 + 0.1), Inches(top + avatar_d + 0.58),
                               Inches(card_w - 0.2), Inches(0.5), align=PP_ALIGN.CENTER)
        style_run(set_text(tf_r, str(person.get("role", "")), align=PP_ALIGN.CENTER), theme["body_font"], 12,
                  theme["secondary"])
    return slide


def slide_feature(prs, theme, spec):
    """Text + a stat callout panel on the side — the layout to reach for
    when a slide "needs an image": a real, meaningful number in a styled
    panel reads as more premium than a stock photo, and this skill never
    fabricates a fake photo to fill space."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme, "content")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]
    header(slide, theme, spec["title"], text_color)

    cursor = 1.9
    if spec.get("description"):
        _, tf = add_textbox(slide, Inches(0.9), Inches(cursor), Inches(6.3), Inches(1.3))
        style_run(set_text(tf, spec["description"]), theme["body_font"], 17, text_color)
        cursor += 1.5

    _, tf = add_textbox(slide, Inches(0.9), Inches(cursor), Inches(6.3), Inches(6.8 - cursor))
    for i, b in enumerate(spec.get("bullets", [])):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(12)
        r = p.add_run()
        r.text = f"●  {b}"
        style_run(r, theme["body_font"], 16, text_color)

    panel_x, panel_w = 7.8, 4.6
    add_panel(slide, Inches(panel_x), Inches(1.9), Inches(panel_w), Inches(4.9), theme["bg_alt"])
    py = 2.5
    if spec.get("panel_label"):
        _, tfl = add_textbox(slide, Inches(panel_x + 0.4), Inches(py), Inches(panel_w - 0.8), Inches(0.4),
                              align=PP_ALIGN.CENTER)
        style_run(set_text(tfl, spec["panel_label"].upper(), align=PP_ALIGN.CENTER), theme["body_font"], 13,
                  theme["secondary"], bold=True)
        py += 0.6
    _, tfv = add_textbox(slide, Inches(panel_x + 0.3), Inches(py), Inches(panel_w - 0.6), Inches(1.6),
                          align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    style_run(set_text(tfv, str(spec.get("panel_value", "")), align=PP_ALIGN.CENTER), theme["heading_font"], 48,
              theme["primary"], bold=True)
    py += 1.7
    if spec.get("panel_caption"):
        _, tfc = add_textbox(slide, Inches(panel_x + 0.4), Inches(py), Inches(panel_w - 0.8), Inches(0.8),
                              align=PP_ALIGN.CENTER)
        style_run(set_text(tfc, spec["panel_caption"], align=PP_ALIGN.CENTER), theme["body_font"], 14, text_color)
    return slide


SLIDE_BUILDERS = {
    "title": slide_title,
    "section": slide_section,
    "bullets": slide_bullets,
    "stats": slide_stats,
    "quote": slide_quote,
    "table": slide_table,
    "closing": slide_closing,
    "agenda": slide_agenda,
    "two_column": slide_two_column,
    "comparison": slide_comparison,
    "timeline": slide_timeline,
    "process": slide_process,
    "big_statement": slide_big_statement,
    "team": slide_team,
    "feature": slide_feature,
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
            raise ValueError(
                f"Unknown slide type '{s['type']}' (slide {i}). Available: {', '.join(SLIDE_BUILDERS)}"
            )
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
