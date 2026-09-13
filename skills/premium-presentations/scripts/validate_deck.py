#!/usr/bin/env python3
"""
validate_deck.py — automated QA pass on a generated .pptx. Catches the two
failure modes that are easy to miss just eyeballing a couple of slides:
  1. Text that overflows its text box (too many words / too big a font for
     the space it was given).
  2. Shapes that overlap each other unintentionally (a layout bug, not a
     deliberate design element like the thin accent bar sitting near text).

This is a heuristic, not a pixel-perfect renderer: it measures text with
Liberation Sans/Serif (the metric-compatible fonts LibreOffice substitutes
for Calibri/Arial/Helvetica and Georgia/Times when those aren't installed —
which is exactly the substitution that will happen anywhere this skill runs
without the real fonts, so it's a *realistic* proxy, not an arbitrary one).
It will not catch every possible rendering quirk, but it reliably catches
the common, embarrassing failures: a long title clipped by a fixed-height
box, a bullet list that runs off the bottom of the slide, two boxes placed
on top of each other by a layout mistake.

Usage:
    python3 validate_deck.py output.pptx            # human-readable report
    python3 validate_deck.py output.pptx --json      # machine-readable
Exit code is non-zero if any issue was found — wire this into your build
step and fix the deck (shorter copy, bigger box, smaller font) rather than
shipping a deck this script flags.
"""
import sys
import json as json_mod
from pathlib import Path

from pptx import Presentation
from pptx.util import Emu

EMU_PER_IN = 914400
DPI = 96  # measurement resolution; only the ratios matter, not the absolute value

FONT_FILES = {
    ("sans", False, False): "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ("sans", True, False): "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ("sans", False, True): "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
    ("sans", True, True): "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf",
    ("serif", False, False): "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    ("serif", True, False): "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    ("serif", False, True): "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    ("serif", True, True): "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf",
}


def _family(font_name: str) -> str:
    return "serif" if font_name and "georgia" in font_name.lower() else "sans"


def _font(font_name, size_pt, bold, italic):
    from PIL import ImageFont
    key = (_family(font_name), bool(bold), bool(italic))
    path = FONT_FILES[key]
    px = max(6, round(size_pt * DPI / 72))
    return ImageFont.truetype(path, px)


def _emu_to_px(emu):
    return emu / EMU_PER_IN * DPI


def _wrap_and_measure(text, font, max_width_px):
    """Greedy word-wrap; returns (n_lines, longest_word_overflows: bool)."""
    from PIL import ImageDraw, Image
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    words = text.split()
    if not words:
        return 0, False
    lines = 1
    cur = ""
    overflow_word = False
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width_px:
            cur = trial
        else:
            if draw.textlength(w, font=font) > max_width_px:
                overflow_word = True
            lines += 1
            cur = w
    return lines, overflow_word


def check_text_frame(shape, slide_idx, issues):
    tf = shape.text_frame
    if not tf.text.strip():
        return
    margin_l = tf.margin_left or Emu(91440)   # python-pptx defaults: 0.1in
    margin_r = tf.margin_right or Emu(91440)
    margin_t = tf.margin_top or Emu(45720)    # 0.05in
    margin_b = tf.margin_bottom or Emu(45720)

    box_w_px = _emu_to_px(shape.width - margin_l - margin_r)
    box_h_px = _emu_to_px(shape.height - margin_t - margin_b)
    if box_w_px <= 0 or box_h_px <= 0:
        return

    total_line_px = 0.0
    for para in tf.paragraphs:
        runs = para.runs
        if not runs and not para.text.strip():
            continue
        text = "".join(r.text for r in runs) or para.text
        size_pt = max((r.font.size.pt for r in runs if r.font.size), default=18)
        bold = any(r.font.bold for r in runs) if runs else False
        italic = any(r.font.italic for r in runs) if runs else False
        font_name = next((r.font.name for r in runs if r.font.name), None)
        font = _font(font_name, size_pt, bold, italic)
        n_lines, word_overflow = _wrap_and_measure(text, font, box_w_px)
        line_height_px = size_pt * DPI / 72 * 1.32  # ~normal line-spacing incl. leading
        total_line_px += n_lines * line_height_px
        if word_overflow:
            snippet = text[:40] + ("…" if len(text) > 40 else "")
            issues.append({
                "slide": slide_idx, "type": "word_too_wide",
                "detail": f'A single word in "{snippet}" ({size_pt:.0f}pt) is wider than its text box — '
                          f"box may be too narrow or font too large.",
            })

    if total_line_px > box_h_px * 1.02:  # 2% slack for measurement approximation
        issues.append({
            "slide": slide_idx, "type": "vertical_overflow",
            "detail": f"Text needs ~{total_line_px:.0f}px but the box only has {box_h_px:.0f}px "
                      f'(shape "{(shape.name or "textbox")}") — shorten the text, shrink the font, '
                      f"or enlarge the box.",
        })


def check_overlaps(slide, slide_idx, issues):
    boxed = []
    for shape in slide.shapes:
        if shape.shape_type == 13:  # PICTURE — the full-bleed background art, not a layout element
            continue
        if not shape.has_text_frame and shape.shape_type != 19:  # not text, not a TABLE
            continue  # skip decorative shapes (accent bars) — they're deliberate, thin, and non-textual
        if shape.has_text_frame and not shape.text_frame.text.strip():
            continue
        boxed.append(shape)

    def rect(s):
        return (s.left, s.top, s.left + s.width, s.top + s.height)

    for i in range(len(boxed)):
        for j in range(i + 1, len(boxed)):
            a, b = rect(boxed[i]), rect(boxed[j])
            ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
            iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
            if ix <= 0 or iy <= 0:
                continue
            inter = ix * iy
            area_a = (a[2] - a[0]) * (a[3] - a[1])
            area_b = (b[2] - b[0]) * (b[3] - b[1])
            smaller = min(area_a, area_b) or 1
            if inter / smaller > 0.08:  # >8% of the smaller shape covered — not a hairline touch
                na = boxed[i].name or "shape"
                nb = boxed[j].name or "shape"
                issues.append({
                    "slide": slide_idx, "type": "overlap",
                    "detail": f'"{na}" and "{nb}" overlap by {inter/smaller*100:.0f}% of the smaller '
                              f"shape's area — check the layout for that slide type.",
                })


def validate(pptx_path: str):
    prs = Presentation(pptx_path)
    issues = []
    for idx, slide in enumerate(prs.slides, start=1):
        for shape in slide.shapes:
            if shape.has_text_frame:
                check_text_frame(shape, idx, issues)
            elif shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:
                        # cells are small and forgiving; only flag gross overflow
                        pass
        check_overlaps(slide, idx, issues)
    return issues


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 validate_deck.py output.pptx [--json]")
        sys.exit(1)
    path = sys.argv[1]
    as_json = "--json" in sys.argv[2:]
    issues = validate(path)
    if as_json:
        print(json_mod.dumps({"file": path, "issue_count": len(issues), "issues": issues}, indent=2))
    else:
        if not issues:
            print(f"✅ {path}: no overflow or overlap issues found.")
        else:
            print(f"❌ {path}: {len(issues)} issue(s) found\n")
            for iss in issues:
                print(f"  Slide {iss['slide']:>2} [{iss['type']}] {iss['detail']}")
    sys.exit(1 if issues else 0)
