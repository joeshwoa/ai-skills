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
]


def get_theme(theme_id: str) -> dict:
    for t in THEMES:
        if t["id"] == theme_id:
            return t
    raise ValueError(
        f"Unknown theme '{theme_id}'. Available: {', '.join(t['id'] for t in THEMES)}"
    )


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
