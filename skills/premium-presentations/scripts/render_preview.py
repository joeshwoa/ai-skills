#!/usr/bin/env python3
"""
render_preview.py — renders the SAME deck spec used by build_deck.py as a
self-contained, animated HTML deck (click / arrow-keys to advance, CSS
transitions between slides, subtle entrance animation on each element).

This is the "premium feel" preview: open it in a browser to see transitions
and motion before exporting the editable .pptx (motion doesn't carry over
to PowerPoint — see SKILL.md's "Animations & transitions" section for why).
It also converts cleanly to PDF via a headless browser or
`soffice --headless --convert-to pdf` for a polished leave-behind.

Usage:
    python3 render_preview.py deck_spec.json output.html
"""
import json
import sys
import html
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from themes import get_theme

TRANSITIONS_CSS = {
    "fade": "opacity 0.6s ease",
    "push": "transform 0.6s cubic-bezier(.4,0,.2,1), opacity 0.4s ease",
    "wipe": "clip-path 0.6s ease",
    "cut": "none",
}


def esc(s):
    return html.escape(str(s))


def render_slide_body(theme, spec):
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]
    t = spec["type"]

    if t == "title":
        kicker = f'<div class="kicker">{esc(spec.get("kicker","").upper())}</div>' if spec.get("kicker") else ""
        sub = f'<p class="subtitle">{esc(spec.get("subtitle",""))}</p>' if spec.get("subtitle") else ""
        return f'''<div class="slide title-slide">
          {kicker}
          <h1>{esc(spec["title"])}</h1>
          <div class="accent-bar"></div>
          {sub}
        </div>'''

    if t == "section":
        return f'''<div class="slide section-slide">
          <div class="big-num">{esc(spec.get("number",""))}</div>
          <h1>{esc(spec["title"])}</h1>
        </div>'''

    if t == "bullets":
        items = ""
        for b in spec.get("bullets", []):
            if isinstance(b, dict):
                items += f'<li><strong>{esc(b.get("point",""))}</strong><br><span class="detail">{esc(b.get("detail",""))}</span></li>'
            else:
                items += f'<li>{esc(b)}</li>'
        return f'''<div class="slide">
          <h2>{esc(spec["title"])}</h2><div class="accent-bar small"></div>
          <ul class="bullets">{items}</ul>
        </div>'''

    if t == "stats":
        cards = "".join(
            f'<div class="stat"><div class="stat-value">{esc(s.get("value",""))}</div>'
            f'<div class="stat-label">{esc(s.get("label",""))}</div></div>'
            for s in spec.get("stats", [])
        )
        return f'''<div class="slide">
          <h2>{esc(spec["title"])}</h2><div class="accent-bar small"></div>
          <div class="stat-row">{cards}</div>
        </div>'''

    if t == "quote":
        attr = f'<p class="attribution">— {esc(spec.get("attribution",""))}</p>' if spec.get("attribution") else ""
        return f'''<div class="slide quote-slide">
          <blockquote>“{esc(spec["quote"])}”</blockquote>{attr}
        </div>'''

    if t == "table":
        head = "".join(f"<th>{esc(h)}</th>" for h in spec["headers"])
        rows = "".join(
            "<tr>" + "".join(f"<td>{esc(v)}</td>" for v in row) + "</tr>"
            for row in spec["rows"]
        )
        return f'''<div class="slide">
          <h2>{esc(spec["title"])}</h2><div class="accent-bar small"></div>
          <table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>
        </div>'''

    if t == "closing":
        contact = f'<p class="contact">{esc(spec.get("contact",""))}</p>' if spec.get("contact") else ""
        return f'''<div class="slide title-slide">
          <h1>{esc(spec.get("title","Thank you"))}</h1>
          <div class="accent-bar"></div>{contact}
        </div>'''

    return f'<div class="slide"><p>Unknown slide type: {esc(t)}</p></div>'


def render(deck_spec_path: str, out_path: str):
    spec = json.loads(Path(deck_spec_path).read_text(encoding="utf-8"))
    theme = get_theme(spec["theme"])
    transition = spec.get("transition", "fade")
    text_color = theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]

    slides_html = "".join(
        f'<section class="slide-wrap" data-index="{i}">{render_slide_body(theme, s)}</section>'
        for i, s in enumerate(spec["slides"])
    )

    css = f"""
    :root {{
      --bg: #{theme['bg']}; --bg-alt: #{theme['bg_alt']};
      --primary: #{theme['primary']}; --secondary: #{theme['secondary']};
      --text: #{text_color};
      --heading-font: '{theme['heading_font']}', Georgia, serif;
      --body-font: '{theme['body_font']}', -apple-system, sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    html,body {{ margin:0; height:100%; background:#111; font-family: var(--body-font); }}
    #deck {{ position:relative; width:100vw; height:100vh; overflow:hidden; }}
    .slide-wrap {{
      position:absolute; inset:0; display:flex; align-items:center; justify-content:flex-start;
      background: var(--bg); color: var(--text);
      opacity:0; pointer-events:none; transition: {TRANSITIONS_CSS.get(transition,'opacity .6s ease')};
      transform: translateX(2%);
    }}
    .slide-wrap.active {{ opacity:1; pointer-events:auto; transform:translateX(0); z-index:2; }}
    .slide {{ width:100%; padding: 6vw 7vw; animation: rise .7s ease both; }}
    @keyframes rise {{ from {{ opacity:0; transform:translateY(16px);}} to {{opacity:1; transform:translateY(0);}} }}
    h1 {{ font-family: var(--heading-font); font-size: clamp(32px,5vw,64px); margin:.2em 0; }}
    h2 {{ font-family: var(--heading-font); font-size: clamp(24px,3.2vw,40px); margin:0 0 .3em; }}
    .kicker {{ color: var(--primary); font-weight:700; letter-spacing:.12em; font-size:14px; }}
    .subtitle {{ color: var(--secondary); font-size: clamp(16px,1.6vw,22px); max-width:60ch; }}
    .accent-bar {{ width:90px; height:5px; background:var(--primary); margin:14px 0 22px; border-radius:3px; }}
    .accent-bar.small {{ width:60px; height:4px; margin:6px 0 26px; }}
    .bullets {{ list-style:none; padding:0; margin:0; max-width:70ch; }}
    .bullets li {{ font-size: clamp(16px,1.8vw,22px); margin-bottom:20px; padding-left:28px; position:relative; }}
    .bullets li::before {{ content:"●"; color:var(--primary); position:absolute; left:0; font-size:12px; top:.4em; }}
    .bullets .detail {{ color:var(--secondary); font-size:.75em; }}
    .stat-row {{ display:flex; gap:6vw; flex-wrap:wrap; margin-top:2vh; }}
    .stat-value {{ font-family:var(--heading-font); font-size: clamp(36px,5vw,56px); color:var(--primary); font-weight:700; }}
    .stat-label {{ color:var(--secondary); font-size:16px; max-width:22ch; }}
    .quote-slide blockquote {{ font-family:var(--heading-font); font-style:italic; font-size:clamp(22px,3vw,34px); max-width:75ch; margin:0; }}
    .attribution {{ color:var(--primary); margin-top:20px; }}
    table {{ border-collapse:collapse; width:100%; font-size:15px; }}
    th,td {{ padding:10px 14px; text-align:left; border-bottom:1px solid rgba(128,128,128,.25); }}
    th {{ background:var(--primary); color: var(--bg); }}
    .big-num {{ font-family:var(--heading-font); font-size:22vh; color:var(--primary); opacity:.9; line-height:1; }}
    .contact {{ color:var(--primary); font-size:18px; margin-top:16px; }}
    #nav {{ position:fixed; bottom:18px; right:24px; z-index:10; color:var(--secondary);
            font-family: var(--body-font); font-size:13px; background:rgba(0,0,0,.25);
            padding:6px 12px; border-radius:20px; backdrop-filter: blur(4px); }}
    """

    js = """
    let idx = 0;
    const wraps = document.querySelectorAll('.slide-wrap');
    const counter = document.getElementById('counter');
    function show(i) {
      idx = Math.max(0, Math.min(wraps.length - 1, i));
      wraps.forEach((w,n) => w.classList.toggle('active', n === idx));
      counter.textContent = (idx+1) + ' / ' + wraps.length;
    }
    document.addEventListener('keydown', e => {
      if (['ArrowRight',' ','PageDown'].includes(e.key)) show(idx+1);
      if (['ArrowLeft','PageUp'].includes(e.key)) show(idx-1);
    });
    document.getElementById('deck').addEventListener('click', () => show(idx+1));
    show(0);
    """

    out = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{esc(spec.get('meta_title','Presentation'))}</title>
<style>{css}</style></head>
<body>
<div id="deck">{slides_html}</div>
<div id="nav">Space/→ next · ← back &nbsp;·&nbsp; <span id="counter"></span></div>
<script>{js}</script>
</body></html>"""

    Path(out_path).write_text(out, encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 render_preview.py deck_spec.json output.html")
        sys.exit(1)
    render(sys.argv[1], sys.argv[2])
