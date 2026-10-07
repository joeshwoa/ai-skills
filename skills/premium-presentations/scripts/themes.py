"""
Theme registry for the premium-presentations skill.

A "theme" is a design spec: colors, fonts, and a *background recipe*
(gradient direction + a subtle grid + one or two soft glow blobs). Both
renderers read themes from here, so the .pptx and the HTML preview always
match. `render_background_png()` turns a theme into the actual raster
background image build_deck.py stamps behind every slide — flat solid
fills read as cheap/template-y, so every theme gets real depth: a gradient
base, a faint engineering-style grid, and colored glow for atmosphere.

To add a theme: append a dict to THEMES. Keep hex colors as "RRGGBB"
(no '#') since python-pptx wants that format; render_preview.py adds the
'#' back for CSS.
"""
import math

# The theme list now lives in the shared design kit (skills/premium-design-kit/lib/pdk/themes.py) so
# decks, documents, spreadsheets and courses share one design system.
import os as _os
import sys as _sys

_KIT = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "premium-design-kit", "lib")
if _os.path.isdir(_KIT) and _os.path.abspath(_KIT) not in _sys.path:
    _sys.path.insert(0, _os.path.abspath(_KIT))
from pdk.themes import THEMES, resolve_theme, tokens  # noqa: E402,F401


def get_theme(theme_id, brand=None) -> dict:
    """Theme id, inline theme dict ({"base": id, ...overrides}) or a brand (creative-studio slug /
    brand.json) → theme dict."""
    return resolve_theme(theme_id, brand)


# ------------------------------------------------------------- background art

def _hex_to_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def render_background_png(theme: dict, variant: str, out_path: str, w: int = 2000, h: int = 1125):
    """Generates the actual background image stamped behind a slide: a
    linear gradient (bg -> bg_alt on theme['gradient_angle']) + a faint
    engineering grid + one or two soft glow blobs in the theme's accent
    color(s). This is what makes a theme look like a real design system
    instead of a flat corporate-template fill.

    variant:
      "hero"    — title/section/closing slides: bigger, brighter glow,
                  grid confined mostly off to one side so it doesn't fight
                  the big title text.
      "content" — bullets/stats/table/quote slides: subtler grid across
                  the whole slide, glow pulled into a back corner so it
                  never reduces text contrast.
    """
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter

    bg = np.array(_hex_to_rgb(theme["bg"]), dtype=np.float32)
    bg_alt = np.array(_hex_to_rgb(theme["bg_alt"]), dtype=np.float32)
    angle = math.radians(theme.get("gradient_angle", 135))
    dx, dy = math.cos(angle), math.sin(angle)

    xs = np.linspace(0, 1, w, dtype=np.float32)
    ys = np.linspace(0, 1, h, dtype=np.float32)
    gx, gy = np.meshgrid(xs, ys)
    proj = gx * dx + gy * dy
    proj -= proj.min()
    denom = proj.max() or 1.0
    t = (proj / denom)[..., None]
    base = (bg[None, None, :] * (1 - t) + bg_alt[None, None, :] * t).astype(np.uint8)
    base_img = Image.fromarray(base, mode="RGB").convert("RGBA")

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")

    # --- faint grid ---
    grid_alpha = theme.get("grid_alpha", 18)
    grid_rgb = _hex_to_rgb(theme["secondary"])
    step = w // 26
    grid_region_x0 = 0 if variant == "content" else int(w * 0.42)
    for x in range(grid_region_x0, w, step):
        fade = 1.0
        if variant == "hero":
            fade = max(0.0, min(1.0, (x - grid_region_x0) / (w * 0.25)))
        draw.line([(x, 0), (x, h)], fill=(*grid_rgb, int(grid_alpha * fade)), width=1)
    for y in range(0, h, step):
        draw.line([(grid_region_x0, y), (w, y)], fill=(*grid_rgb, int(grid_alpha * 0.8)), width=1)

    # --- glow blobs ---
    glow_colors = theme.get("glow", [theme["primary"]])
    glow_alpha = theme.get("glow_alpha", 90)
    if variant == "hero":
        blobs = [
            (int(w * 0.82), int(h * 0.18), int(w * 0.28), glow_colors[0], glow_alpha),
            (int(w * 0.08), int(h * 0.95), int(w * 0.22), glow_colors[-1], int(glow_alpha * 0.7)),
        ]
    else:
        blobs = [
            (int(w * 0.94), int(h * 0.06), int(w * 0.16), glow_colors[0], int(glow_alpha * 0.55)),
        ]

    glow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer, "RGBA")
    for cx, cy, r, color_hex, alpha in blobs:
        rgb = _hex_to_rgb(color_hex)
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*rgb, alpha))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=w * 0.045))

    overlay = Image.alpha_composite(overlay, glow_layer)
    final = Image.alpha_composite(base_img, overlay)
    final.convert("RGB").save(out_path, "PNG")
    return out_path


def build_theme_gallery_html(out_path: str) -> None:
    """Render a visual gallery (one card per theme) so the user can pick by
    eye instead of by reading hex codes — approximates the real gradient +
    grid + glow background with CSS so the preview matches the generated
    deck's look."""
    cards = []
    for t in THEMES:
        text_color = t["text_on_dark"] if t["style"] == "dark" else t["text_on_light"]
        glow = t.get("glow", [t["primary"]])
        glow2 = glow[-1]
        bg_css = f"""
          background:
            radial-gradient(circle at 88% 10%, #{glow[0]}55, transparent 45%),
            radial-gradient(circle at 6% 95%, #{glow2}33, transparent 40%),
            linear-gradient({t.get('gradient_angle',135)}deg, #{t['bg']}, #{t['bg_alt']});
        """
        cards.append(f"""
        <div class="card" style="{bg_css}">
          <div class="swatches">
            <span style="background:#{t['primary']}"></span>
            <span style="background:#{t['secondary']}"></span>
          </div>
          <h2 style="color:#{text_color};font-family:'{t['heading_font']}',serif;">{t['name']}</h2>
          <p style="color:#{t['primary']};font-family:'{t['body_font']}',sans-serif;">{t['tagline']}</p>
          <code style="color:#{text_color};opacity:.55">id: {t['id']}</code>
        </div>""")

    html = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Presentation Themes</title>
<style>
  body{{margin:0;padding:32px;background:#0e0e12;font-family:system-ui,sans-serif;
        display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;}}
  .card{{border-radius:16px;padding:28px 24px;min-height:170px;position:relative;overflow:hidden;
         box-shadow:0 8px 24px rgba(0,0,0,.35);
         background-size: 200% 200%, 200% 200%, 100% 100%;}}
  .card::before{{content:"";position:absolute;inset:0;
    background-image:
      repeating-linear-gradient(90deg, rgba(255,255,255,.05) 0 1px, transparent 1px 28px),
      repeating-linear-gradient(0deg, rgba(255,255,255,.05) 0 1px, transparent 1px 28px);
    mask-image: linear-gradient(135deg, black, transparent 70%);
  }}
  .swatches{{display:flex;gap:8px;margin-bottom:14px;position:relative;}}
  .swatches span{{width:22px;height:22px;border-radius:50%;display:inline-block;
                   box-shadow:0 0 0 2px rgba(255,255,255,.15);}}
  h2{{margin:0 0 6px;font-size:22px;position:relative;}}
  p{{margin:0 0 14px;font-size:14px;position:relative;}}
  code{{font-size:11px;position:relative;}}
</style></head><body>
{''.join(cards)}
</body></html>"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    import sys
    build_theme_gallery_html(sys.argv[1] if len(sys.argv) > 1 else "theme_gallery.html")
    print(f"{len(THEMES)} themes: {[t['id'] for t in THEMES]}")
