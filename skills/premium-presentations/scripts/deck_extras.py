"""
deck_extras.py — the v2 layer of build_deck.py:

* Arabic / RTL decks: every slide is built on the normal grid, then MIRRORED (positions flipped,
  paragraphs right-aligned + rtl, tables rtl, arrows flipped, chart categories reversed) and every
  run gets an Arabic complex-script font. Shapes named "keep-ltr" (code) are not mirrored.
* Real images: photos/illustrations from free stock (stock-library), the user's files, icons (Iconify),
  generated theme art — through the shared design kit's Assets resolver (pdk.assets).
* New slide types: image_hero, image_split, gallery, chart (native editable PowerPoint charts),
  diagram (cycle, pyramid, funnel, hierarchy, venn, matrix), objectives, quiz, activity, definition,
  kpi, quote_image, credits.
* Per-slide extras on ANY slide: "notes" (speaker notes), "background" (image + overlay), "icon"
  on icon_grid/process/stats items, "photo" on team members, "image" on feature.

All builders follow build_deck.py's conventions: inches on a 13.333 x 7.5 grid, every text box
through add_textbox (fixed boxes, word wrap), native shapes, editable text.
"""
from __future__ import annotations

import math
from copy import deepcopy
from pathlib import Path

from lxml import etree
from pptx.chart.data import CategoryChartData, XyChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt, Emu

B = None          # build_deck module, injected by register()
ASSETS = None     # pdk.assets.Assets for the current build
TOKENS = None     # pdk tokens for the current theme
RTL = False

W_IN, H_IN = 13.333, 7.5


def register(build_module):
    global B
    B = build_module
    return {
        "image_hero": slide_image_hero, "image_split": slide_image_split, "gallery": slide_gallery,
        "chart": slide_chart, "diagram": slide_diagram, "objectives": slide_objectives, "quiz": slide_quiz,
        "activity": slide_activity, "definition": slide_definition, "kpi": slide_kpi,
        "quote_image": slide_quote_image, "credits": slide_credits,
    }


# ------------------------------------------------------------------------------------------ helpers
def tc(theme):
    return theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]


def on_primary(theme):
    from pdk.themes import readable_on
    return readable_on(theme["primary"])


def new_slide(prs, theme, variant="content", title=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    B.set_background(slide, theme, variant)
    if title:
        B.header(slide, theme, title, tc(theme))
    return slide


def asset(ref, **kw):
    if not ref:
        return None
    if ASSETS is None:
        p = ref if isinstance(ref, str) else ref.get("path")
        return p if p and Path(p).exists() else None
    return ASSETS.resolve(ref, **kw)


def picture_cover(slide, path, x, y, w, h, *, rounded=0.0, name=None):
    """Picture that FILLS the box (cropped, never stretched) — like CSS object-fit: cover."""
    from PIL import Image
    iw, ih = Image.open(path).size
    box = w / h
    img = iw / ih
    pic = slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
    if img > box:                      # too wide → crop sides
        c = (1 - box / img) / 2
        pic.crop_left = pic.crop_right = c
    elif img < box:                    # too tall → crop top/bottom (keep a little more top: faces)
        c = 1 - img / box
        pic.crop_top, pic.crop_bottom = c * 0.35, c * 0.65
    if rounded:
        pic.auto_shape_type = MSO_SHAPE.ROUNDED_RECTANGLE
        try:
            pic._element.spPr.find(qn("a:prstGeom")).find(qn("a:avLst"))
            geom = pic._element.spPr.find(qn("a:prstGeom"))
            av = geom.find(qn("a:avLst"))
            for g in list(av):
                av.remove(g)
            gd = etree.SubElement(av, qn("a:gd"))
            gd.set("name", "adj")
            gd.set("fmla", f"val {int(rounded * 100000)}")
        except Exception:
            pass
    if name:
        pic.name = name
    return pic


def picture_contain(slide, path, x, y, w, h):
    from PIL import Image
    iw, ih = Image.open(path).size
    s = min(w / iw, h / ih)
    pw, ph = iw * s, ih * s
    return slide.shapes.add_picture(str(path), Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2), Inches(pw), Inches(ph))


def set_alpha(shape, alpha: float):
    """alpha 0..1 on a solid-filled autoshape."""
    sf = shape.fill._xPr.find(qn("a:solidFill"))
    if sf is None:
        return
    clr = sf[0]
    for a in clr.findall(qn("a:alpha")):
        clr.remove(a)
    el = etree.SubElement(clr, qn("a:alpha"))
    el.set("val", str(int(alpha * 100000)))


def rect(slide, x, y, w, h, fill, *, alpha=None, shape=MSO_SHAPE.RECTANGLE, line=None, radius=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = B.rgb(fill)
        if alpha is not None:
            set_alpha(s, alpha)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = B.rgb(line[0])
        s.line.width = Pt(line[1])
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    if radius is not None:
        try:
            s.adjustments[0] = radius
        except Exception:
            pass
    return s


def text(slide, x, y, w, h, value, font, size, color, *, bold=False, align=PP_ALIGN.LEFT, anchor=None, italic=False):
    _, tf = B.add_textbox(slide, Inches(x), Inches(y), Inches(w), Inches(h), align=align, anchor=anchor)
    B.style_run(B.set_text(tf, str(value if value is not None else ""), align=align), font, size, color,
                bold=bold, italic=italic)
    return tf


def gradient_overlay(path_out, color_hex, w=1600, h=900, direction="left", strength=0.92):
    """PNG overlay that darkens one side of a photo so text on it stays readable."""
    from PIL import Image
    import numpy as np
    from pdk.themes import hex_rgb
    r, g, b = hex_rgb(color_hex)
    xs = np.linspace(0, 1, w)
    if direction == "left":
        a = np.clip(1.15 - xs * 1.25, 0.18, 1.0)
    elif direction == "right":
        a = np.clip(xs * 1.25 - 0.1, 0.18, 1.0)
    else:  # bottom
        a = None
    arr = np.zeros((h, w, 4), np.uint8)
    arr[..., 0], arr[..., 1], arr[..., 2] = r, g, b
    if a is None:
        ys = np.linspace(0, 1, h)
        col = np.clip(ys * 1.3 - 0.15, 0.1, 1.0)
        arr[..., 3] = (np.repeat(col[:, None], w, axis=1) * 255 * strength).astype(np.uint8)
    else:
        arr[..., 3] = (np.repeat(a[None, :], h, axis=0) * 255 * strength).astype(np.uint8)
    Image.fromarray(arr, "RGBA").save(path_out)
    return path_out


def overlay_png(color_hex, direction, strength=0.92):
    d = Path(ASSETS.dir if ASSETS else "/tmp") / f"overlay-{color_hex}-{direction}-{int(strength * 100)}.png"
    if not d.exists():
        gradient_overlay(d, color_hex, direction=direction, strength=strength)
    return str(d)


def bullets_box(slide, theme, x, y, w, h, items, size=17, color=None, marker="●"):
    color = color or tc(theme)
    _, tf = B.add_textbox(slide, Inches(x), Inches(y), Inches(w), Inches(h))
    for i, b in enumerate(items or []):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(10)
        if isinstance(b, dict):
            r = p.add_run()
            r.text = f"{marker}  {b.get('point', '')}"
            B.style_run(r, theme["body_font"], size, color, bold=bool(b.get("detail")))
            if b.get("detail"):
                p2 = tf.add_paragraph()
                p2.space_after = Pt(8)
                r2 = p2.add_run()
                r2.text = f"     {b['detail']}"
                B.style_run(r2, theme["body_font"], size - 3, theme["secondary"])
        else:
            r = p.add_run()
            r.text = f"{marker}  {b}"
            B.style_run(r, theme["body_font"], size, color)
    return tf


def icon_or_glyph(slide, theme, ref, glyph, x, y, d, *, fill=None, on=None):
    """A circle with an Iconify icon inside (or the glyph letters when no icon)."""
    fill = fill or theme["primary"]
    on = on or on_primary(theme)
    B.add_circle(slide, Inches(x + d / 2), Inches(y + d / 2), Inches(d), fill)
    p = asset({"icon": ref} if isinstance(ref, str) else ref, color=on) if ref else None
    if p:
        m = d * 0.22
        slide.shapes.add_picture(p, Inches(x + m), Inches(y + m), Inches(d - 2 * m), Inches(d - 2 * m))
    else:
        text(slide, x, y, d, d, str(glyph or "")[:2].upper(), theme["heading_font"], max(10, int(d * 20)), on,
             bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# --------------------------------------------------------------------------------- per-slide extras
def apply_background(slide, theme, ref, overlay=0.55, direction="full"):
    """Replace the theme background with an image + a readability overlay (inserted at the back)."""
    p = asset(ref, size=(2000, 1125))
    if not p:
        return
    pic = picture_cover(slide, p, 0, 0, W_IN, H_IN)
    tree = slide.shapes._spTree
    tree.remove(pic._element)
    tree.insert(3, pic._element)  # just above the theme background picture
    if overlay:
        if direction == "full":
            ov = rect(slide, 0, 0, W_IN, H_IN, theme["bg"], alpha=overlay)
        else:
            ov = slide.shapes.add_picture(overlay_png(theme["bg"], direction, overlay), 0, 0, Inches(W_IN), Inches(H_IN))
        tree.remove(ov._element)
        tree.insert(4, ov._element)


def set_notes(slide, notes):
    if not notes:
        return
    if isinstance(notes, list):
        notes = "\n".join(f"• {n}" for n in notes)
    tf = slide.notes_slide.notes_text_frame
    tf.text = str(notes)
    if RTL:
        for p in tf.paragraphs:
            pPr = p._p.get_or_add_pPr()
            pPr.set("rtl", "1")
            pPr.set("algn", "r")


# ------------------------------------------------------------------------------------------- RTL
FLIP_SHAPES = {"chevron", "homePlate", "rightArrow", "leftArrow", "notchedRightArrow", "stripedRightArrow",
               "rightArrowCallout", "bentArrow", "curvedRightArrow", "circularArrow"}


def rtl_font_runs(slide, head_font, body_font):
    """Every run gets the Arabic font as its complex-script (cs) face so Word/PowerPoint render the
    Arabic letters in the theme's Arabic font even where the Latin face is different."""
    for r in slide._element.iter(qn("a:rPr"), qn("a:endParaRPr"), qn("a:defRPr")):
        latin = r.find(qn("a:latin"))
        face = latin.get("typeface") if latin is not None else body_font
        cs = r.find(qn("a:cs"))
        if cs is None:
            cs = etree.SubElement(r, qn("a:cs"))
        cs.set("typeface", face)
        if r.get("lang") is None and r.tag == qn("a:rPr"):
            r.set("lang", "ar-EG")


def mirror_slide(slide):
    """Mirror the finished slide for right-to-left reading."""
    sw = Inches(W_IN)
    for shp in slide.shapes:
        name = shp.name or ""
        if name.startswith("keep-ltr"):
            continue
        ltr_text = name.startswith("ltr-text")
        try:
            if shp.width < sw - 10:          # full-bleed pictures/backgrounds stay put
                shp.left = sw - shp.left - shp.width
        except Exception:
            pass
        el = shp._element
        geom = el.find(".//" + qn("a:prstGeom"))
        if geom is not None and geom.get("prst") in FLIP_SHAPES:
            xfrm = el.find(".//" + qn("a:xfrm"))
            if xfrm is not None:
                xfrm.set("flipH", "0" if xfrm.get("flipH") == "1" else "1")
        if shp.has_text_frame and ltr_text:
            for p in shp.text_frame.paragraphs:
                pPr = p._p.get_or_add_pPr()
                pPr.set("algn", {"r": "l", "l": "r"}.get(pPr.get("algn"), pPr.get("algn") or "r"))
        if shp.has_text_frame and not ltr_text:
            for p in shp.text_frame.paragraphs:
                pPr = p._p.get_or_add_pPr()
                pPr.set("rtl", "1")
                al = pPr.get("algn")
                pPr.set("algn", {"l": "r", None: "r", "r": "l", "just": "just"}.get(al, al))
        if shp.has_table:
            tblPr = el.find(".//" + qn("a:tblPr"))
            if tblPr is not None:
                tblPr.set("rtl", "1")
            for row in shp.table.rows:
                for cell in row.cells:
                    for p in cell.text_frame.paragraphs:
                        pPr = p._p.get_or_add_pPr()
                        pPr.set("rtl", "1")
                        al = pPr.get("algn")
                        pPr.set("algn", {"l": "r", None: "r", "r": "l"}.get(al, al))
        if getattr(shp, "has_chart", False) and shp.has_chart:
            ch = shp.chart
            try:
                if ch.chart_type not in (XL_CHART_TYPE.PIE, XL_CHART_TYPE.DOUGHNUT):
                    ch.category_axis.reverse_order = True
                    # value axis to the right side
                    crosses = ch._chartSpace.find(".//" + qn("c:valAx") + "/" + qn("c:crosses"))
            except Exception:
                pass


# ------------------------------------------------------------------------------------- image slides
def slide_image_hero(prs, theme, spec):
    """Full-bleed photo, dark gradient on the text side, big title. Covers, section openers, chapter
    starts. {"type":"image_hero","image":{...},"kicker":"","title":"","subtitle":"","align":"left|bottom"}"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    B.set_background(slide, theme, "hero")
    p = asset(spec.get("image"), size=(2000, 1125), orientation="landscape")
    dark = theme["bg"] if theme["style"] == "dark" else "0B0F19"
    lay = spec.get("align", "left")
    if p:
        picture_cover(slide, p, 0, 0, W_IN, H_IN)
        side = "bottom" if lay == "bottom" else ("right" if RTL else "left")   # dark where the text will be
        slide.shapes.add_picture(overlay_png(dark, side, spec.get("overlay", 0.9)),
                                 0, 0, Inches(W_IN), Inches(H_IN))
    white = "FFFFFF"
    if lay == "bottom":
        y0, w = 3.9, 11.6
    else:
        y0, w = 1.9, 7.6
    if spec.get("kicker"):
        text(slide, 0.9, y0 - 0.5, w, 0.4, spec["kicker"].upper(), theme["body_font"], 14, theme["primary"], bold=True)
    rect(slide, 0.9, y0 - 0.06, 0.9, 0.055, theme["primary"])
    title = spec.get("title", "")
    size = 44 if len(title) < 26 else 38 if len(title) < 50 else 32
    if RTL:
        size -= 4                         # Arabic glyphs sit taller in the same point size
    th = 2.1
    text(slide, 0.9, y0 + 0.1, w, th, title, theme["heading_font"], size, white, bold=True)
    if spec.get("subtitle"):
        text(slide, 0.9, y0 + th + 0.2, w, 1.0, spec["subtitle"], theme["body_font"], 19, "E6E8EE")
    return slide


def slide_image_split(prs, theme, spec):
    """Half photo, half content. {"type":"image_split","image":{...},"title":"","text":"","bullets":[...],
    "side":"right|left","caption":""}"""
    slide = new_slide(prs, theme)
    side = spec.get("side", "right")
    img_w = 5.9
    ix = W_IN - img_w if side == "right" else 0
    p = asset(spec.get("image"), size=(1300, 1650), orientation="portrait")
    if p:
        picture_cover(slide, p, ix, 0, img_w, H_IN)
    tx = 0.85 if side == "right" else img_w + 0.7
    tw = W_IN - img_w - 1.55
    text(slide, tx, 0.75, tw, 1.3, spec.get("title", ""), theme["heading_font"], 30, tc(theme), bold=True)
    rect(slide, tx, 2.1, 0.9, 0.055, theme["primary"])
    y = 2.4
    if spec.get("text"):
        text(slide, tx, y, tw, 1.5, spec["text"], theme["body_font"], 17, tc(theme))
        y += 1.6
    if spec.get("bullets"):
        bullets_box(slide, theme, tx, y, tw, 6.9 - y, spec["bullets"], size=16)
    if spec.get("caption") and p:
        rect(slide, ix, H_IN - 0.55, img_w, 0.55, "000000", alpha=0.55)
        text(slide, ix + 0.25, H_IN - 0.5, img_w - 0.5, 0.45, spec["caption"], theme["body_font"], 11, "FFFFFF")
    return slide


def slide_gallery(prs, theme, spec):
    """2–6 images in a clean grid with captions. {"type":"gallery","title":"","items":[{"image":{...},
    "caption":""}]}"""
    slide = new_slide(prs, theme, title=spec.get("title"))
    items = spec.get("items", [])[:6]
    n = max(len(items), 1)
    cols = n if n <= 3 else 3
    rows = math.ceil(n / cols)
    gap = 0.3
    cw = (11.65 - gap * (cols - 1)) / cols
    cap_h = 0.45 if any(i.get("caption") for i in items) else 0
    ch = (5.05 - gap * (rows - 1)) / rows - cap_h
    for i, it in enumerate(items):
        c, r = i % cols, i // cols
        x = 0.84 + c * (cw + gap)
        y = 1.65 + r * (ch + cap_h + gap)
        p = asset(it.get("image"), size=(1200, int(1200 * ch / cw)))
        if p:
            picture_cover(slide, p, x, y, cw, ch, rounded=0.04)
        else:
            rect(slide, x, y, cw, ch, theme["bg_alt"], shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.04)
        if it.get("caption"):
            text(slide, x, y + ch + 0.05, cw, cap_h - 0.05, it["caption"], theme["body_font"], 13, theme["secondary"])
    return slide


def slide_quote_image(prs, theme, spec):
    """A quote over a photo (or theme art). {"type":"quote_image","quote":"","author":"","image":{...}}"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    B.set_background(slide, theme, "hero")
    p = asset(spec.get("image") or {"art": "mesh", "dark": True}, size=(2000, 1125))
    if p:
        picture_cover(slide, p, 0, 0, W_IN, H_IN)
        rect(slide, 0, 0, W_IN, H_IN, "0B0F19", alpha=0.62)
    text(slide, 1.2, 0.3, 1.4, 2.1, "“", "Georgia", 110, theme["primary"], bold=True)
    q = spec.get("quote", "")
    size = 34 if len(q) < 90 else 27 if len(q) < 170 else 22
    text(slide, 1.6, 2.45, 10.2, 2.95, q, theme["heading_font"], size, "FFFFFF", bold=True, anchor=MSO_ANCHOR.TOP)
    if spec.get("author"):
        text(slide, 1.6, 5.55, 10.2, 0.6, "— " + spec["author"], theme["body_font"], 18, theme["primary"], bold=True)
    return slide


# -------------------------------------------------------------------------------- native charts
CHART_TYPES = {
    "bar": XL_CHART_TYPE.COLUMN_CLUSTERED, "column": XL_CHART_TYPE.COLUMN_CLUSTERED,
    "stacked": XL_CHART_TYPE.COLUMN_STACKED, "stacked100": XL_CHART_TYPE.COLUMN_STACKED_100,
    "hbar": XL_CHART_TYPE.BAR_CLUSTERED, "line": XL_CHART_TYPE.LINE_MARKERS, "area": XL_CHART_TYPE.AREA,
    "pie": XL_CHART_TYPE.PIE, "donut": XL_CHART_TYPE.DOUGHNUT, "doughnut": XL_CHART_TYPE.DOUGHNUT,
    "scatter": XL_CHART_TYPE.XY_SCATTER, "radar": XL_CHART_TYPE.RADAR_MARKERS,
}


def chart_palette(theme, n):
    from pdk.themes import mix
    base = [theme["primary"], theme["secondary"], mix(theme["primary"], tc(theme), 0.45),
            mix(theme["primary"], theme["bg"], 0.45), mix(theme["secondary"], theme["bg"], 0.4), mix(tc(theme), theme["bg"], 0.5)]
    while len(base) < n:
        base.append(mix(base[len(base) % 6], theme["bg"], 0.3))
    return base[:n]


def add_native_chart(slide, theme, spec, x, y, w, h):
    kind = spec.get("chart", spec.get("kind", "bar"))
    ct = CHART_TYPES.get(kind, XL_CHART_TYPE.COLUMN_CLUSTERED)
    series = spec.get("series") or [{"name": spec.get("series_name", ""), "values": spec.get("values", [])}]
    if kind == "scatter":
        cd = XyChartData()
        for s in series:
            se = cd.add_series(s.get("name", ""))
            for xv, yv in zip(s.get("x", []), s["values"]):
                se.add_data_point(xv, yv)
    else:
        cd = CategoryChartData()
        cd.categories = [str(c) for c in spec.get("categories", [])]
        fmt = spec.get("number_format")
        for s in series:
            cd.add_series(s.get("name", ""), [float(v) for v in s["values"]], number_format=fmt)
    gf = slide.shapes.add_chart(ct, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart
    ch.has_title = False          # the slide title is the chart title
    txt = tc(theme)
    ch.font.size = Pt(13)
    ch.font.name = theme["body_font"]
    ch.font.color.rgb = B.rgb(txt)
    pal = chart_palette(theme, max(len(series), len(spec.get("categories", []))))
    hl = spec.get("highlight")
    if kind in ("pie", "donut", "doughnut"):
        plot = ch.plots[0]
        for i, pt in enumerate(plot.series[0].points):
            pt.format.fill.solid()
            col = pal[i % len(pal)]
            if hl is not None:
                from pdk.themes import mix
                col = theme["primary"] if i == hl else mix(theme["secondary"], theme["bg"], 0.35 + 0.1 * (i % 3))
            pt.format.fill.fore_color.rgb = B.rgb(col)
            pt.format.line.color.rgb = B.rgb(theme["bg"])
        plot.has_data_labels = True
        dl = plot.data_labels
        dl.show_value = True
        dl.show_category_name = False
        dl.number_format = spec.get("label_format", '0"%"' if spec.get("unit") == "%" else "General")
        dl.number_format_is_linked = False
        dl.font.size = Pt(13)
        dl.font.bold = True
        dl.font.color.rgb = B.rgb(on_primary(theme))
        if kind != "pie":
            try:
                plot._element.find(qn("c:holeSize")).set("val", "58")
            except Exception:
                pass
        ch.has_legend = True
        ch.legend.position = XL_LEGEND_POSITION.RIGHT
        ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(14)
        ch.legend.font.color.rgb = B.rgb(txt)
    else:
        plot = ch.plots[0]
        for i, s in enumerate(plot.series):
            col = pal[i % len(pal)]
            if kind in ("line", "radar", "scatter"):
                s.format.line.color.rgb = B.rgb(col)
                s.format.line.width = Pt(3)
                s.smooth = False
                try:
                    s.marker.format.fill.solid()
                    s.marker.format.fill.fore_color.rgb = B.rgb(col)
                    s.marker.format.line.color.rgb = B.rgb(col)
                except Exception:
                    pass
            else:
                s.format.fill.solid()
                s.format.fill.fore_color.rgb = B.rgb(col)
                if hl is not None and len(plot.series) == 1:
                    from pdk.themes import mix
                    for j, pt in enumerate(s.points):
                        pt.format.fill.solid()
                        pt.format.fill.fore_color.rgb = B.rgb(theme["primary"] if j == hl else mix(theme["secondary"], theme["bg"], 0.45))
        if kind in ("bar", "column", "stacked", "hbar"):
            try:
                plot.gap_width = 70
                if kind != "stacked":
                    plot.overlap = -10 if len(series) > 1 else 0
            except Exception:
                pass
        if spec.get("labels", True) and kind not in ("stacked", "stacked100", "radar", "scatter"):
            plot.has_data_labels = True
            dl = plot.data_labels
            dl.show_value = True
            dl.font.size = Pt(12)
            dl.font.bold = True
            dl.font.color.rgb = B.rgb(txt)
            if spec.get("label_format"):
                dl.number_format = spec["label_format"]
                dl.number_format_is_linked = False
            try:
                dl.position = XL_LABEL_POSITION.OUTSIDE_END if kind in ("bar", "column", "hbar") else XL_LABEL_POSITION.ABOVE
            except Exception:
                pass
        try:
            va = ch.value_axis
            va.has_major_gridlines = True
            va.major_gridlines.format.line.color.rgb = B.rgb(theme["secondary"])
            va.major_gridlines.format.line.width = Pt(0.5)
            va.format.line.fill.background()
            va.tick_labels.font.size = Pt(12)
            va.tick_labels.font.color.rgb = B.rgb(theme["secondary"])
            if spec.get("number_format"):
                va.tick_labels.number_format = spec["number_format"]
                va.tick_labels.number_format_is_linked = False
            if "y_min" in spec:
                va.minimum_scale = spec["y_min"]
            ca = ch.category_axis
            ca.format.line.color.rgb = B.rgb(theme["secondary"])
            ca.tick_labels.font.size = Pt(13)
            ca.tick_labels.font.color.rgb = B.rgb(txt)
            ca.has_major_gridlines = False
        except Exception:
            pass
        ch.has_legend = len(series) > 1
        if ch.has_legend:
            ch.legend.position = XL_LEGEND_POSITION.TOP
            ch.legend.include_in_layout = False
            ch.legend.font.size = Pt(13)
            ch.legend.font.color.rgb = B.rgb(txt)
    return gf


def slide_chart(prs, theme, spec):
    """A NATIVE PowerPoint chart (double-click → edit data in PowerPoint). chart: bar|stacked|hbar|line|
    area|pie|donut|scatter|radar. Optional side "insight" text and "source" line.
    {"type":"chart","title":"","chart":"bar","categories":[...],"series":[{"name":"","values":[...]}],
     "insight":"…","source":"…","highlight":2,"number_format":"0%","y_min":0}"""
    slide = new_slide(prs, theme, title=spec.get("title"))
    has_side = bool(spec.get("insight") or spec.get("takeaways"))
    cw = 7.9 if has_side else 11.7
    add_native_chart(slide, theme, spec, 0.75, 1.6, cw, 4.85)
    if has_side:
        x = 0.75 + cw + 0.35
        w = W_IN - x - 0.75
        rect(slide, x, 1.75, w, 4.6, theme["bg_alt"], shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
        y = 2.05
        if spec.get("insight_label"):
            text(slide, x + 0.3, y, w - 0.6, 0.4, spec["insight_label"].upper(), theme["body_font"], 12, theme["primary"], bold=True)
            y += 0.45
        if spec.get("insight"):
            text(slide, x + 0.3, y, w - 0.6, 1.8, spec["insight"], theme["heading_font"], 19, tc(theme), bold=True)
            y += 1.9
        if spec.get("takeaways"):
            bullets_box(slide, theme, x + 0.3, y, w - 0.6, 6.2 - y, spec["takeaways"], size=14)
    if spec.get("source"):
        text(slide, 0.8, 6.55, 9, 0.35, spec["source"], theme["body_font"], 10, theme["secondary"], italic=True)
    return slide


# ------------------------------------------------------------------------------------------ diagrams
def _node(slide, theme, x, y, w, h, label, sub="", *, fill=None, color=None, size=15, radius=0.18):
    fill = fill or theme["bg_alt"]
    color = color or tc(theme)
    rect(slide, x, y, w, h, fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=radius)
    if sub:
        text(slide, x + 0.12, y + 0.08, w - 0.24, h * 0.45, label, theme["heading_font"], size, color, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM)
        text(slide, x + 0.12, y + h * 0.5, w - 0.24, h * 0.48, sub, theme["body_font"], max(10, size - 4),
             color if fill == theme["primary"] else theme["secondary"], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.TOP)
    else:
        text(slide, x + 0.1, y, w - 0.2, h, label, theme["heading_font"], size, color, bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def _connector(slide, theme, x1, y1, x2, y2, arrow=True, color=None):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = B.rgb(color or theme["secondary"])
    c.line.width = Pt(1.75)
    if arrow:
        ln = c.line._get_or_add_ln()
        tail = etree.SubElement(ln, qn("a:tailEnd"))
        tail.set("type", "triangle")
        tail.set("w", "med")
        tail.set("len", "med")
    return c


def slide_diagram(prs, theme, spec):
    """Native-shape diagrams. kind: cycle | pyramid | funnel | hierarchy | venn | matrix.
    items: [{"label":"","detail":""}] (hierarchy: {"label","children":[...]}; matrix: 4 items +
    "axes":["x label","y label"])."""
    slide = new_slide(prs, theme, title=spec.get("title"))
    kind = spec.get("kind", "cycle")
    items = spec.get("items", [])
    fn = {"cycle": _d_cycle, "pyramid": _d_pyramid, "funnel": _d_funnel, "hierarchy": _d_hierarchy,
          "venn": _d_venn, "matrix": _d_matrix}.get(kind)
    if not fn:
        raise ValueError(f"diagram kind '{kind}' unknown (cycle, pyramid, funnel, hierarchy, venn, matrix)")
    fn(slide, theme, items, spec)
    if spec.get("caption"):
        text(slide, 0.8, 6.55, 11.7, 0.4, spec["caption"], theme["body_font"], 13, theme["secondary"], align=PP_ALIGN.CENTER)
    return slide


def _d_cycle(slide, theme, items, spec):
    n = max(len(items), 2)
    cx, cy, R = W_IN / 2, 4.15, 2.05
    ring = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx - R), Inches(cy - R), Inches(2 * R), Inches(2 * R))
    ring.fill.background()
    ring.line.color.rgb = B.rgb(theme["secondary"])
    ring.line.width = Pt(2)
    ring.line.dash_style = 4
    ring.shadow.inherit = False
    if spec.get("center"):
        text(slide, cx - 1.3, cy - 0.5, 2.6, 1.0, spec["center"], theme["heading_font"], 20, theme["primary"], bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    nw, nh = 2.45, 1.0 if not any(i.get("detail") for i in items) else 1.25
    for i, it in enumerate(items):
        a = -math.pi / 2 + 2 * math.pi * i / n
        x, y = cx + R * math.cos(a) * 1.55 - nw / 2, cy + R * math.sin(a) * 1.05 - nh / 2
        hot = i == 0
        _node(slide, theme, x, y, nw, nh, f"{i + 1}. {it.get('label', '')}", it.get("detail", ""),
              fill=theme["primary"] if hot else theme["bg_alt"], color=on_primary(theme) if hot else tc(theme), size=14)


def _d_pyramid(slide, theme, items, spec):
    """items[0] = the top (smallest) level."""
    n = max(len(items), 1)
    top, bottom = 1.75, 6.35
    gap = 0.07
    lh = (bottom - top) / n
    cx, base_w = 3.9, 6.2
    from pdk.themes import mix
    for i, it in enumerate(items):
        y = top + i * lh
        h = lh - gap
        w_top = base_w * (i * lh) / (n * lh)
        w_bot = base_w * ((i + 1) * lh - gap) / (n * lh)
        if i == 0:
            s = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(cx - w_bot / 2), Inches(y), Inches(w_bot), Inches(h))
        else:
            s = slide.shapes.add_shape(MSO_SHAPE.TRAPEZOID, Inches(cx - w_bot / 2), Inches(y), Inches(w_bot), Inches(h))
            try:
                s.adjustments[0] = ((w_bot - w_top) / 2) / min(w_bot, h)
            except Exception:
                pass
        s.fill.solid()
        s.fill.fore_color.rgb = B.rgb(mix(theme["primary"], theme["bg"], 0.14 * i))
        s.line.fill.background()
        s.shadow.inherit = False
        ty = y + h * (0.35 if i == 0 else 0)
        text(slide, cx - w_bot / 2, ty, w_bot, h - (ty - y), str(i + 1), theme["heading_font"], 16, on_primary(theme),
             bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        rect(slide, 7.25, y + h / 2 - 0.01, 0.35, 0.03, theme["primary"])
        text(slide, 7.75, y + max(0, h / 2 - 0.5), 4.9, 0.45, it.get("label", ""), theme["heading_font"], 17, tc(theme), bold=True,
             anchor=MSO_ANCHOR.BOTTOM)
        if it.get("detail"):
            text(slide, 7.75, y + h / 2 - 0.02, 4.9, min(0.9, h / 2 + 0.1), it["detail"], theme["body_font"], 13, theme["secondary"])


def _d_funnel(slide, theme, items, spec):
    n = max(len(items), 1)
    top, bottom = 1.75, 6.35
    lh = (bottom - top) / n
    cx, w0, w1 = 4.0, 6.6, 2.0
    from pdk.themes import mix
    for i, it in enumerate(items):
        w = w0 - (w0 - w1) * i / max(n - 1, 1)
        y = top + i * lh
        rect(slide, cx - w / 2, y, w, lh - 0.1, mix(theme["primary"], theme["bg"], 0.13 * i),
             shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.25)
        text(slide, cx - w / 2, y, w, lh - 0.1, str(it.get("value", "")) or it.get("label", ""), theme["heading_font"],
             18, on_primary(theme), bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        text(slide, 7.7, y + 0.05, 4.9, 0.45, it.get("label", "") if it.get("value") is not None else "", theme["heading_font"], 17,
             tc(theme), bold=True)
        if it.get("detail"):
            text(slide, 7.7, y + 0.5, 4.9, max(0.3, lh - 0.55), it["detail"], theme["body_font"], 13, theme["secondary"])


def _d_hierarchy(slide, theme, items, spec):
    root = items[0] if items else {"label": ""}
    kids = root.get("children", [])
    n = max(len(kids), 1)
    rw, rh = 3.2, 0.95
    _node(slide, theme, W_IN / 2 - rw / 2, 1.7, rw, rh, root.get("label", ""), root.get("detail", ""),
          fill=theme["primary"], color=on_primary(theme), size=17)
    gap = 0.25
    kw = min(3.0, (11.8 - gap * (n - 1)) / n)
    total = kw * n + gap * (n - 1)
    x0 = (W_IN - total) / 2
    y1 = 3.35
    bus_y = 3.0
    if kids:
        _connector(slide, theme, W_IN / 2, 1.7 + rh, W_IN / 2, bus_y, arrow=False)
        _connector(slide, theme, x0 + kw / 2, bus_y, x0 + total - kw / 2, bus_y, arrow=False)
    for i, k in enumerate(kids):
        x = x0 + i * (kw + gap)
        _connector(slide, theme, x + kw / 2, bus_y, x + kw / 2, y1, arrow=False)
        _node(slide, theme, x, y1, kw, 0.9, k.get("label", ""), k.get("detail", ""), size=14)
        gk = k.get("children", [])
        for j, g in enumerate(gk[:4]):
            gy = y1 + 1.15 + j * 0.62
            rect(slide, x + 0.25, gy, kw - 0.25, 0.5, None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, line=(theme["secondary"], 1), radius=0.2)
            text(slide, x + 0.3, gy, kw - 0.35, 0.5, g.get("label", g) if isinstance(g, dict) else g, theme["body_font"], 12,
                 tc(theme), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            _connector(slide, theme, x + 0.1, gy + 0.25, x + 0.25, gy + 0.25, arrow=False)
        if gk:
            _connector(slide, theme, x + 0.1, y1 + 0.9, x + 0.1, y1 + 1.15 + (min(len(gk), 4) - 1) * 0.62 + 0.25, arrow=False)


def _d_venn(slide, theme, items, spec):
    n = min(max(len(items), 2), 3)
    d = 3.9
    cy = 4.15
    pos = [(W_IN / 2 - 1.25, cy), (W_IN / 2 + 1.25, cy)] if n == 2 else [(W_IN / 2 - 1.15, cy - 0.55), (W_IN / 2 + 1.15, cy - 0.55), (W_IN / 2, cy + 1.05)]
    if n == 3:
        d = 3.2
    cols = [theme["primary"], theme["secondary"], tc(theme)]
    for i in range(n):
        x, y = pos[i]
        s = rect(slide, x - d / 2, y - d / 2, d, d, cols[i], alpha=0.32, shape=MSO_SHAPE.OVAL)
        it = items[i] if i < len(items) else {}
        dx = (-1 if x < W_IN / 2 - 0.1 else 1 if x > W_IN / 2 + 0.1 else 0)
        ty = y - 0.35 if n == 2 else (y - 0.6 if i < 2 else y + 0.35)
        text(slide, x - d / 2 + dx * 0.55 * (d / 2) + 0.2, ty, d - 0.4 - 0.2, 0.9, it.get("label", ""), theme["heading_font"], 16,
             tc(theme), bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if spec.get("center"):
        text(slide, W_IN / 2 - 0.9, cy - 0.35 if n == 2 else cy - 0.15, 1.8, 0.7, spec["center"], theme["heading_font"], 14,
             theme["primary"] if theme["style"] == "light" else "FFFFFF", bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


def _d_matrix(slide, theme, items, spec):
    x0, y0, cw, chh = 3.2, 1.75, 3.45, 2.2
    for i in range(4):
        it = items[i] if i < len(items) else {}
        c, r = i % 2, i // 2
        hot = it.get("highlight")
        fill = theme["primary"] if hot else theme["bg_alt"]
        col = on_primary(theme) if hot else tc(theme)
        x, y = x0 + c * (cw + 0.15), y0 + r * (chh + 0.15)
        rect(slide, x, y, cw, chh, fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
        text(slide, x + 0.25, y + 0.2, cw - 0.5, 0.5, it.get("label", ""), theme["heading_font"], 17, col, bold=True)
        text(slide, x + 0.25, y + 0.75, cw - 0.5, chh - 0.9, it.get("detail", ""), theme["body_font"], 13,
             col if hot else theme["secondary"])
    axes = spec.get("axes", ["", ""])
    if axes and axes[0]:
        text(slide, x0, y0 + 2 * chh + 0.3 + 0.05, 2 * cw + 0.15, 0.4, axes[0] + "  →", theme["body_font"], 13, theme["secondary"], bold=True, align=PP_ALIGN.CENTER)
    if len(axes) > 1 and axes[1]:
        text(slide, 0.8, y0 + chh - 0.2, 2.25, 0.6, "↑  " + axes[1], theme["body_font"], 13, theme["secondary"], bold=True, align=PP_ALIGN.RIGHT)


# --------------------------------------------------------------------------------- teaching slides
def slide_objectives(prs, theme, spec):
    """Learning objectives as numbered cards with the Bloom verb emphasised.
    {"type":"objectives","title":"By the end of this session you can…","items":[{"verb":"Write","text":"…"}]}"""
    slide = new_slide(prs, theme, title=spec.get("title", "Objectives"))
    items = spec.get("items", [])[:6]
    n = max(len(items), 1)
    cols = 1 if n <= 3 else 2
    rows = math.ceil(n / cols)
    gap = 0.25
    cw = (11.7 - gap * (cols - 1)) / cols
    rh = min(1.35, (5.0 - gap * (rows - 1)) / rows)
    for i, it in enumerate(items):
        c, r = i % cols, i // cols
        x, y = 0.8 + c * (cw + gap), 1.75 + r * (rh + gap)
        rect(slide, x, y, cw, rh, theme["bg_alt"], shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
        rect(slide, x, y, 0.95, rh, theme["primary"], shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
        rect(slide, x + 0.6, y, 0.35, rh, theme["primary"])
        text(slide, x, y, 0.95, rh, f"{i + 1:02d}", theme["heading_font"], 22, on_primary(theme), bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        it = it if isinstance(it, dict) else {"text": it}
        _, tf = B.add_textbox(slide, Inches(x + 1.2), Inches(y), Inches(cw - 1.4), Inches(rh), anchor=MSO_ANCHOR.MIDDLE)
        p = tf.paragraphs[0]
        if it.get("verb"):
            r1 = p.add_run()
            r1.text = it["verb"] + " "
            B.style_run(r1, theme["heading_font"], 18, theme["primary"], bold=True)
        r2 = p.add_run()
        r2.text = it.get("text", "")
        B.style_run(r2, theme["body_font"], 17, tc(theme))
    return slide


def slide_quiz(prs, theme, spec):
    """A check-for-understanding question with 2–4 options. "reveal": true marks the answer (use a
    second copy of the slide for the reveal). {"type":"quiz","question":"","options":["",""],
    "answer":1,"reveal":false,"explanation":""}"""
    slide = new_slide(prs, theme)
    label = spec.get("label", "اختبر نفسك" if RTL else "Quick check")
    text(slide, 0.8, 0.55, 6, 0.4, label.upper(), theme["body_font"], 14, theme["primary"], bold=True)
    q = spec.get("question", "")
    text(slide, 0.8, 0.95, 11.7, 1.45, q, theme["heading_font"], 28 if len(q) < 90 else 22, tc(theme), bold=True)
    opts = spec.get("options", [])[:4]
    n = max(len(opts), 1)
    cols = 2 if n > 2 else n
    rows = math.ceil(n / cols)
    gap = 0.3
    cw = (11.7 - gap * (cols - 1)) / cols
    rh = 1.2 if rows > 1 else 1.6
    ans = spec.get("answer")
    letters = "أبجد" if RTL else "ABCD"
    for i, o in enumerate(opts):
        c, r = i % cols, i // cols
        x, y = 0.8 + c * (cw + gap), 2.65 + r * (rh + gap)
        right = spec.get("reveal") and ans == i
        wrong = spec.get("reveal") and ans != i
        fill = theme["primary"] if right else theme["bg_alt"]
        col = on_primary(theme) if right else (theme["secondary"] if wrong else tc(theme))
        rect(slide, x, y, cw, rh, fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
        B.add_circle(slide, Inches(x + 0.65), Inches(y + rh / 2), Inches(0.7), theme["bg"] if right else theme["primary"])
        text(slide, x + 0.3, y + rh / 2 - 0.35, 0.7, 0.7, ("✓" if right else letters[i]), theme["heading_font"], 18,
             theme["primary"] if right else on_primary(theme), bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        text(slide, x + 1.2, y, cw - 1.4, rh, o, theme["body_font"], 18, col, bold=bool(right), anchor=MSO_ANCHOR.MIDDLE)
    if spec.get("reveal") and spec.get("explanation"):
        text(slide, 0.8, 2.65 + rows * (rh + gap) + 0.05, 11.7, 0.9, spec["explanation"], theme["body_font"], 15, theme["secondary"])
    return slide


def slide_activity(prs, theme, spec):
    """A hands-on task the class does now: icon, duration badge, mode (solo/pairs/groups), numbered
    steps, deliverable. {"type":"activity","title":"","minutes":15,"mode":"pairs","icon":"…",
    "steps":["",""],"deliverable":""}"""
    slide = new_slide(prs, theme)
    rect(slide, 0, 0, 4.2, H_IN, theme["primary"])
    icon_or_glyph(slide, theme, spec.get("icon", "mdi:pencil-ruler"), "✎", 1.3, 1.1, 1.6,
                  fill=theme["bg"] if theme["style"] == "dark" else "FFFFFF", on=theme["primary"])
    lab = spec.get("label", "نشاط" if RTL else "Activity")
    text(slide, 0.5, 3.0, 3.2, 0.5, lab.upper(), theme["body_font"], 16, on_primary(theme), bold=True, align=PP_ALIGN.CENTER)
    if spec.get("minutes"):
        mins = f"{spec['minutes']} " + ("دقيقة" if RTL else "min")
        text(slide, 0.5, 3.55, 3.2, 1.0, mins, theme["heading_font"], 40, on_primary(theme), bold=True, align=PP_ALIGN.CENTER)
    if spec.get("mode"):
        text(slide, 0.5, 4.6, 3.2, 0.5, spec["mode"], theme["body_font"], 16, on_primary(theme), align=PP_ALIGN.CENTER)
    text(slide, 4.8, 0.7, 7.9, 1.2, spec.get("title", ""), theme["heading_font"], 30, tc(theme), bold=True)
    y = 2.0
    for i, s in enumerate(spec.get("steps", [])[:6]):
        B.add_circle(slide, Inches(5.1), Inches(y + 0.3), Inches(0.5), theme["primary"])
        text(slide, 4.85, y + 0.05, 0.5, 0.5, str(i + 1), theme["heading_font"], 14, on_primary(theme), bold=True,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        text(slide, 5.6, y, 7.1, 0.75, s, theme["body_font"], 16, tc(theme), anchor=MSO_ANCHOR.MIDDLE)
        y += 0.8
    if spec.get("deliverable"):
        rect(slide, 4.85, 6.25, 7.8, 0.75, theme["bg_alt"], shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.2)
        pre = "التسليم: " if RTL else "Deliver: "
        text(slide, 5.1, 6.25, 7.4, 0.75, pre + spec["deliverable"], theme["body_font"], 15, tc(theme), bold=True,
             anchor=MSO_ANCHOR.MIDDLE)
    return slide


def slide_definition(prs, theme, spec):
    """A key term: the word, a plain definition, an example and (optional) a common mistake.
    {"type":"definition","term":"","pronounce":"","definition":"","example":"","mistake":"","image":{...}}"""
    slide = new_slide(prs, theme)
    has_img = bool(spec.get("image"))
    w = 7.4 if has_img else 11.7
    text(slide, 0.8, 0.6, 5, 0.4, (spec.get("label") or ("مصطلح" if RTL else "Key term")).upper(), theme["body_font"], 14, theme["primary"], bold=True)
    text(slide, 0.8, 1.0, w, 1.2, spec.get("term", ""), theme["heading_font"], 46, tc(theme), bold=True)
    y = 2.25
    if spec.get("pronounce"):
        text(slide, 0.8, y - 0.1, w, 0.45, spec["pronounce"], theme["body_font"], 16, theme["secondary"], italic=True)
        y += 0.45
    rect(slide, 0.8, y + 0.05, 0.9, 0.055, theme["primary"])
    text(slide, 0.8, y + 0.3, w, 1.55, spec.get("definition", ""), theme["body_font"], 21, tc(theme))
    y += 1.95
    if spec.get("example"):
        rect(slide, 0.8, y, w, 1.15, theme["bg_alt"], shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
        text(slide, 1.05, y + 0.08, w - 0.5, 0.32, ("مثال" if RTL else "Example").upper(), theme["body_font"], 11, theme["primary"], bold=True)
        text(slide, 1.05, y + 0.42, w - 0.5, 0.68, spec["example"], theme["body_font"], 15, tc(theme))
        y += 1.3
    if spec.get("mistake"):
        text(slide, 0.8, y, w, 0.75, ("⚠  " + spec["mistake"]), theme["body_font"], 14, theme["secondary"])
    if has_img:
        p = asset(spec["image"], size=(1100, 1300))
        if p:
            picture_cover(slide, p, 8.7, 0.8, 3.85, 5.9, rounded=0.05)
    return slide


def slide_kpi(prs, theme, spec):
    """KPI dashboard: 2–4 metric cards (value, label, delta ▲▼, icon) above an optional native chart.
    {"type":"kpi","title":"","metrics":[{"value":"92%","label":"","delta":"+4 pts","good":true,"icon":"…"}],
     "chart":{…chart spec…}}"""
    slide = new_slide(prs, theme, title=spec.get("title"))
    ms = spec.get("metrics", [])[:4]
    n = max(len(ms), 1)
    gap = 0.3
    cw = (11.7 - gap * (n - 1)) / n
    ch_ = 1.65 if spec.get("chart") else 3.2
    for i, m in enumerate(ms):
        x = 0.8 + i * (cw + gap)
        rect(slide, x, 1.65, cw, ch_, theme["bg_alt"], shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
        if m.get("icon"):
            icon_or_glyph(slide, theme, m["icon"], "", x + cw - 0.85, 1.85, 0.55)
        text(slide, x + 0.3, 1.76, cw - 1.2, 0.38, m.get("label", ""), theme["body_font"], 13, theme["secondary"], bold=True)
        text(slide, x + 0.3, 2.14, cw - 0.5, 0.74, m.get("value", ""), theme["heading_font"], 32, tc(theme), bold=True)
        if m.get("delta"):
            good = m.get("good", True)
            col = "1E9E5A" if good else "D64545"
            text(slide, x + 0.3, 2.9 if spec.get("chart") else 3.1, cw - 0.5, 0.36, ("▲ " if good else "▼ ") + m["delta"],
                 theme["body_font"], 13, col, bold=True)
    if spec.get("chart"):
        add_native_chart(slide, theme, spec["chart"], 0.75, 3.55, 11.8, 3.0)
    return slide


def slide_credits(prs, theme, spec):
    """Image/icon credits (auto-added when a licence asks for attribution)."""
    slide = new_slide(prs, theme, title=spec.get("title") or ("حقوق الصور" if RTL else "Image credits"))
    lines = spec.get("lines", [])
    box, tf = B.add_textbox(slide, Inches(0.85), Inches(1.7), Inches(11.6), Inches(5.0))
    box.name = "allow-wrap credits"
    for i, l in enumerate(lines[:18]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(4)
        r = p.add_run()
        r.text = l
        B.style_run(r, theme["body_font"], 11 if len(lines) > 10 else 13, theme["secondary"])
    return slide
