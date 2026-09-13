"""
Theme registry for the premium-presentations skill.

A "theme" is a small, self-contained design spec: colors, fonts, and a
background style. Both renderers (build_deck.py for editable .pptx and
render_preview.py for the animated HTML preview) read themes from here,
so the two outputs always look identical.

To add a theme: append a dict to THEMES. Keep hex colors as "RRGGBB"
(no '#') since python-pptx wants that format; render_preview.py adds the
'#' back for CSS.
"""

THEMES = [
    {
        "id": "onyx-gold",
        "name": "Onyx & Gold",
        "tagline": "Dark, premium, executive — for board decks and investor pitches",
        "bg": "12141C",
        "bg_alt": "1B1E2B",
        "primary": "D4AF6A",       # gold accent
        "secondary": "8A93A8",     # muted slate for body text on dark
        "text_on_dark": "F5F1E8",
        "text_on_light": "12141C",
        "heading_font": "Georgia",
        "body_font": "Calibri",
        "style": "dark",
    },
    {
        "id": "arctic-minimal",
        "name": "Arctic Minimal",
        "tagline": "Clean white space, one accent color — for product & UX decks",
        "bg": "FFFFFF",
        "bg_alt": "F4F6F8",
        "primary": "2F6FED",       # bright blue accent
        "secondary": "5B6472",
        "text_on_dark": "FFFFFF",
        "text_on_light": "1B1E2B",
        "heading_font": "Helvetica",
        "body_font": "Helvetica",
        "style": "light",
    },
    {
        "id": "sunset-startup",
        "name": "Sunset Startup",
        "tagline": "Warm gradient energy — for pitch decks and launch announcements",
        "bg": "1A1030",
        "bg_alt": "2A1745",
        "primary": "FF6B5B",       # coral
        "secondary": "FFC15E",     # amber
        "text_on_dark": "FFF7ED",
        "text_on_light": "1A1030",
        "heading_font": "Poppins",
        "body_font": "Poppins",
        "style": "dark",
    },
    {
        "id": "sage-editorial",
        "name": "Sage Editorial",
        "tagline": "Soft, calm, magazine-style — for research & strategy decks",
        "bg": "F6F5EF",
        "bg_alt": "EAE7DA",
        "primary": "4B6B57",       # sage green
        "secondary": "8A7F6A",
        "text_on_dark": "F6F5EF",
        "text_on_light": "27362E",
        "heading_font": "Georgia",
        "body_font": "Calibri",
        "style": "light",
    },
    {
        "id": "cobalt-tech",
        "name": "Cobalt Tech",
        "tagline": "High-contrast, technical, confident — for engineering & product reviews",
        "bg": "0B1220",
        "bg_alt": "121C33",
        "primary": "4CC2FF",
        "secondary": "7C8AA5",
        "text_on_dark": "E9F1FF",
        "text_on_light": "0B1220",
        "heading_font": "Calibri",
        "body_font": "Calibri",
        "style": "dark",
    },
    {
        "id": "ivory-luxe",
        "name": "Ivory Luxe",
        "tagline": "Understated luxury, lots of air — for brand & agency decks",
        "bg": "FBF9F4",
        "bg_alt": "F0EBDD",
        "primary": "9A7B4F",       # bronze
        "secondary": "6B6255",
        "text_on_dark": "FBF9F4",
        "text_on_light": "2A2620",
        "heading_font": "Georgia",
        "body_font": "Georgia",
        "style": "light",
    },
]


def get_theme(theme_id: str) -> dict:
    for t in THEMES:
        if t["id"] == theme_id:
            return t
    raise ValueError(
        f"Unknown theme '{theme_id}'. Available: {', '.join(t['id'] for t in THEMES)}"
    )


def build_theme_gallery_html(out_path: str) -> None:
    """Render a visual gallery (one card per theme) so the user can pick by eye
    instead of by reading hex codes. Used during the 'ask for design details'
    step of the skill when the user hasn't specified a look."""
    cards = []
    for t in THEMES:
        text_color = t["text_on_dark"] if t["style"] == "dark" else t["text_on_light"]
        cards.append(f"""
        <div class="card" style="background:linear-gradient(135deg,#{t['bg']},#{t['bg_alt']});">
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
        display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;}}
  .card{{border-radius:16px;padding:28px 24px;min-height:150px;
         box-shadow:0 8px 24px rgba(0,0,0,.35);}}
  .swatches{{display:flex;gap:8px;margin-bottom:14px;}}
  .swatches span{{width:22px;height:22px;border-radius:50%;display:inline-block;
                   box-shadow:0 0 0 2px rgba(255,255,255,.15);}}
  h2{{margin:0 0 6px;font-size:22px;}}
  p{{margin:0 0 14px;font-size:14px;}}
  code{{font-size:11px;}}
</style></head><body>
{''.join(cards)}
</body></html>"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    import sys
    build_theme_gallery_html(sys.argv[1] if len(sys.argv) > 1 else "theme_gallery.html")
    print(f"Themes: {[t['id'] for t in THEMES]}")
