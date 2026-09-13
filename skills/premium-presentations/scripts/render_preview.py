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

    if t == "agenda":
        rows = "".join(
            f'<div class="agenda-row"><span class="agenda-num">{i+1:02d}</span>'
            f'<span class="agenda-item">{esc(item)}</span></div>'
            for i, item in enumerate(spec.get("items", []))
        )
        return f'''<div class="slide">
          <h2>{esc(spec.get("title","Agenda"))}</h2><div class="accent-bar small"></div>
          <div class="agenda-list">{rows}</div>
        </div>'''

    if t == "two_column":
        def col(heading, items):
            h = f'<h3>{esc(heading)}</h3>' if heading else ""
            lis = "".join(f'<li>{esc(i)}</li>' for i in items)
            return f'<div class="col">{h}<ul class="dash-list">{lis}</ul></div>'
        return f'''<div class="slide">
          <h2>{esc(spec["title"])}</h2><div class="accent-bar small"></div>
          <div class="two-col">{col(spec.get("left_heading",""), spec.get("left_items",[]))}
          <div class="col-divider"></div>
          {col(spec.get("right_heading",""), spec.get("right_items",[]))}</div>
        </div>'''

    if t == "comparison":
        def card(label, points, cls):
            lis = "".join(f'<li>{esc(p)}</li>' for p in points)
            return f'<div class="cmp-card {cls}"><div class="cmp-head">{esc(label).upper()}</div><ul>{lis}</ul></div>'
        return f'''<div class="slide">
          <h2>{esc(spec["title"])}</h2><div class="accent-bar small"></div>
          <div class="comparison">
            {card(spec.get("left_label","Before"), spec.get("left_points",[]), "muted")}
            {card(spec.get("right_label","After"), spec.get("right_points",[]), "accent")}
          </div>
        </div>'''

    if t == "timeline":
        n = len(spec.get("milestones", [])) or 1
        def _inset_pct(i, n):
            # Remap 0..100% into an 8..92% band so edge item boxes (which are
            # centered on their point) can't overhang the slide's padding.
            if n <= 1:
                return 50.0
            return 8 + (i / (n - 1)) * 84
        dots = "".join(
            f'<div class="tl-item" style="left:{_inset_pct(i, n):.2f}%">'
            f'<div class="tl-label">{esc(m.get("label",""))}</div><div class="tl-dot"></div>'
            f'<div class="tl-text">{esc(m.get("text",""))}</div></div>'
            for i, m in enumerate(spec.get("milestones", []))
        )
        return f'''<div class="slide">
          <h2>{esc(spec["title"])}</h2><div class="accent-bar small"></div>
          <div class="timeline"><div class="tl-line"></div>{dots}</div>
        </div>'''

    if t == "process":
        n = len(spec.get("steps", [])) or 1
        def _inset_pct(i, n):
            # Same edge-safe remap as the timeline: keeps centered item boxes
            # from overhanging the slide at the first/last step.
            if n <= 1:
                return 50.0
            return 8 + (i / (n - 1)) * 84
        steps = "".join(
            f'<div class="proc-item" style="left:{_inset_pct(i, n):.2f}%">'
            f'<div class="proc-circle">{esc(s.get("number", i+1))}</div>'
            f'<div class="proc-label">{esc(s.get("label",""))}</div>'
            f'<div class="proc-detail">{esc(s.get("detail",""))}</div></div>'
            for i, s in enumerate(spec.get("steps", []))
        )
        return f'''<div class="slide">
          <h2>{esc(spec["title"])}</h2><div class="accent-bar small"></div>
          <div class="process">{f'<div class="proc-line"></div>' if n > 1 else ''}{steps}</div>
        </div>'''

    if t == "big_statement":
        support = f'<p class="support">{esc(spec["support"])}</p>' if spec.get("support") else ""
        return f'''<div class="slide big-statement">
          <h1 class="statement">{esc(spec["statement"])}</h1>{support}
        </div>'''

    if t == "team":
        cards = "".join(
            f'<div class="person"><div class="avatar">{esc("".join(w[0].upper() for w in str(p.get("name","?")).split()[:2]) or "?")}</div>'
            f'<div class="person-name">{esc(p.get("name",""))}</div>'
            f'<div class="person-role">{esc(p.get("role",""))}</div></div>'
            for p in spec.get("people", [])
        )
        return f'''<div class="slide">
          <h2>{esc(spec.get("title","Team"))}</h2><div class="accent-bar small"></div>
          <div class="team-grid">{cards}</div>
        </div>'''

    if t == "feature":
        desc = f'<p class="feature-desc">{esc(spec["description"])}</p>' if spec.get("description") else ""
        bullets = "".join(f'<li>{esc(b)}</li>' for b in spec.get("bullets", []))
        label = f'<div class="panel-label">{esc(spec["panel_label"]).upper()}</div>' if spec.get("panel_label") else ""
        caption = f'<div class="panel-caption">{esc(spec["panel_caption"])}</div>' if spec.get("panel_caption") else ""
        return f'''<div class="slide">
          <h2>{esc(spec["title"])}</h2><div class="accent-bar small"></div>
          <div class="feature-layout">
            <div class="feature-text">{desc}<ul class="bullets">{bullets}</ul></div>
            <div class="feature-panel">{label}<div class="panel-value">{esc(spec.get("panel_value",""))}</div>{caption}</div>
          </div>
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

    glow = theme.get("glow", [theme["primary"], theme["primary"]])
    grad_angle = theme.get("gradient_angle", 135)
    grid_rgb_hex = theme["secondary"]
    grid_alpha = theme.get("grid_alpha", 18) / 255

    css = f"""
    :root {{
      --bg: #{theme['bg']}; --bg-alt: #{theme['bg_alt']};
      --primary: #{theme['primary']}; --secondary: #{theme['secondary']};
      --glow1: #{glow[0]}; --glow2: #{glow[-1]};
      --text: #{text_color};
      --heading-font: '{theme['heading_font']}', Georgia, serif;
      --body-font: '{theme['body_font']}', -apple-system, sans-serif;
    }}
    * {{ box-sizing: border-box; }}
    html,body {{ margin:0; height:100%; background:#111; font-family: var(--body-font); }}
    #deck {{ position:relative; width:100vw; height:100vh; overflow:hidden; }}
    .slide-wrap {{
      position:absolute; inset:0; display:flex; align-items:center; justify-content:flex-start;
      color: var(--text); overflow:hidden;
      opacity:0; pointer-events:none; transition: {TRANSITIONS_CSS.get(transition,'opacity .6s ease')};
      transform: translateX(2%);
      background:
        radial-gradient(closest-side, color-mix(in srgb, var(--glow1) 55%, transparent), transparent 70%) 92% 8% / 55% 55% no-repeat,
        radial-gradient(closest-side, color-mix(in srgb, var(--glow2) 35%, transparent), transparent 70%) 4% 96% / 45% 45% no-repeat,
        repeating-linear-gradient(90deg, color-mix(in srgb, var(--secondary) {theme.get('grid_alpha',18)*100//255}%, transparent) 0 1px, transparent 1px 42px),
        repeating-linear-gradient(0deg, color-mix(in srgb, var(--secondary) {theme.get('grid_alpha',18)*100//255}%, transparent) 0 1px, transparent 1px 42px),
        linear-gradient({grad_angle}deg, var(--bg), var(--bg-alt));
      background-blend-mode: screen, screen, normal, normal, normal;
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

    .agenda-list {{ max-width:70ch; margin-top:1vh; }}
    .agenda-row {{ display:flex; align-items:center; gap:24px; padding:16px 0; border-bottom:1px solid rgba(128,128,128,.25); }}
    .agenda-num {{ font-family:var(--heading-font); font-weight:700; color:var(--primary); font-size:clamp(18px,2vw,26px); width:2.2ch; }}
    .agenda-item {{ font-size:clamp(16px,1.8vw,22px); }}

    .two-col {{ display:flex; gap:5vw; margin-top:1vh; }}
    .col {{ flex:1; }}
    .col h3 {{ font-family:var(--heading-font); color:var(--primary); font-size:clamp(16px,1.6vw,20px); margin:0 0 .6em; }}
    .col-divider {{ width:1px; background:rgba(128,128,128,.35); }}
    .dash-list {{ list-style:none; padding:0; margin:0; }}
    .dash-list li {{ font-size:clamp(14px,1.4vw,17px); margin-bottom:14px; padding-left:1.6em; position:relative; }}
    .dash-list li::before {{ content:"—"; position:absolute; left:0; opacity:.7; }}

    .comparison {{ display:flex; gap:2.5vw; margin-top:1vh; }}
    .cmp-card {{ flex:1; border-radius:16px; overflow:hidden; background:rgba(255,255,255,.05); border:1px solid rgba(128,128,128,.25); }}
    .cmp-head {{ padding:16px 20px; font-weight:700; letter-spacing:.05em; font-size:14px; }}
    .cmp-card.muted .cmp-head {{ background:var(--secondary); color:var(--bg); }}
    .cmp-card.accent .cmp-head {{ background:var(--primary); color:var(--bg); }}
    .cmp-card ul {{ list-style:none; margin:0; padding:18px 20px; }}
    .cmp-card li {{ font-size:15px; margin-bottom:10px; padding-left:1.3em; position:relative; }}
    .cmp-card li::before {{ content:"•"; color:var(--primary); position:absolute; left:0; }}

    .timeline {{ position:relative; height:22vh; margin-top:6vh; }}
    .tl-line {{ position:absolute; left:8%; right:8%; top:50%; height:2px; background:var(--primary); }}
    .tl-item {{ position:absolute; top:50%; transform:translate(-50%,-50%); text-align:center; width:160px; }}
    .tl-dot {{ width:16px; height:16px; border-radius:50%; background:var(--primary); margin:0 auto; }}
    .tl-label {{ font-family:var(--heading-font); font-weight:700; color:var(--primary); font-size:15px; margin-bottom:8px; }}
    .tl-text {{ font-size:13px; color:var(--text); margin-top:8px; }}

    .process {{ position:relative; height:34vh; margin-top:4vh; }}
    .proc-line {{ position:absolute; left:8%; right:8%; top:56px; height:2px; background:var(--secondary); opacity:.5; }}
    .proc-item {{ position:absolute; top:0; transform:translateX(-50%); text-align:center; width:180px; }}
    .proc-circle {{ width:80px; height:80px; border-radius:50%; background:var(--primary); color:var(--bg);
                     display:flex; align-items:center; justify-content:center; font-family:var(--heading-font);
                     font-weight:700; font-size:28px; margin:0 auto 14px; }}
    .proc-label {{ font-family:var(--heading-font); font-weight:700; font-size:16px; margin-bottom:6px; }}
    .proc-detail {{ font-size:13px; color:var(--secondary); }}

    .big-statement {{ display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; height:100%; }}
    .statement {{ max-width:16ch; margin:0 auto; }}
    .support {{ color:var(--primary); font-size:clamp(14px,1.4vw,18px); margin-top:1.2em; }}

    .team-grid {{ display:flex; flex-wrap:wrap; gap:4vw; margin-top:2vh; }}
    .person {{ width:160px; text-align:center; }}
    .avatar {{ width:80px; height:80px; border-radius:50%; background:var(--primary); color:var(--bg);
               display:flex; align-items:center; justify-content:center; font-family:var(--heading-font);
               font-weight:700; font-size:22px; margin:0 auto 12px; }}
    .person-name {{ font-weight:700; font-size:15px; }}
    .person-role {{ color:var(--secondary); font-size:12px; margin-top:4px; }}

    .feature-layout {{ display:flex; gap:4vw; margin-top:1vh; align-items:flex-start; }}
    .feature-text {{ flex:1.3; }}
    .feature-desc {{ font-size:clamp(14px,1.4vw,17px); max-width:55ch; }}
    .feature-panel {{ flex:1; background:rgba(255,255,255,.05); border:1px solid rgba(128,128,128,.25);
                       border-radius:18px; padding:32px 24px; text-align:center; }}
    .panel-label {{ font-size:12px; letter-spacing:.08em; color:var(--secondary); font-weight:700; margin-bottom:14px; }}
    .panel-value {{ font-family:var(--heading-font); font-weight:700; color:var(--primary); font-size:clamp(32px,4vw,48px); }}
    .panel-caption {{ font-size:13px; margin-top:14px; }}
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
