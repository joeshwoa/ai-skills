"""HTML-preview twins of deck_extras.py's slide types (same spec → same content), plus RTL, images,
icons and per-slide backgrounds for the animated preview. Images are embedded as data URIs so the
preview is one self-contained file you can send."""
from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

from pdk.text import esc, inline_md

A = None        # pdk Assets (shared cache with build_deck → same pictures)
RTL = False
TK = None       # stage tokens (dark/light slide colours) for chart images


def data_uri(path) -> str:
    if not path:
        return ""
    p = Path(path)
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def img(ref, cls="", size=(1600, 900), style=""):
    p = A.resolve(ref, size=size) if (A and ref) else None
    if not p:
        return ""
    return f'<img class="{cls}" style="{style}" src="{data_uri(p)}" alt="">'


def icon_img(ref, color, cls="ico"):
    if not ref or not A:
        return ""
    p = A.resolve({"icon": ref} if isinstance(ref, str) else ref, color=color)
    return f'<img class="{cls}" src="{data_uri(p)}" alt="">' if p else ""


def stage_tokens(tk, theme):
    t = dict(tk)
    t.update({"paper": theme["bg"], "ink": tc(theme), "ink_soft": tc(theme), "muted": theme["secondary"],
              "line": theme["bg_alt"], "accent": theme["primary"], "accent_2": theme["secondary"]})
    return t


def tc(theme):
    return theme["text_on_dark"] if theme["style"] == "dark" else theme["text_on_light"]


def head(spec, default=""):
    t = spec.get("title", default)
    return f'<h2>{esc(t)}</h2><div class="accent-bar small"></div>' if t else ""


def chart_img(spec, theme):
    if not A:
        return ""
    from pdk.charts import render_chart
    c = dict(spec)
    c["type"] = {"column": "bar", "doughnut": "donut", "stacked100": "stacked", "radar": "line"}.get(
        spec.get("chart", "bar"), spec.get("chart", "bar"))
    c.pop("title", None)
    out = Path(A.dir) / f"pv-chart-{abs(hash(str(sorted(spec.items(), key=str)))) % 10**10}.png"
    render_chart(c, stage_tokens(TK, theme), out, width_in=8, height_in=4.2, transparent=True)
    return f'<img class="chart-img" src="{data_uri(out)}" alt="">'


def render_extra(theme, spec):
    t = spec["type"]
    on = "FFFFFF"
    if t == "image_hero":
        return f'''<div class="slide hero-img">{img(spec.get("image"), "bleed")}<div class="shade"></div>
          <div class="hero-text">{f'<div class="kicker">{esc(spec["kicker"].upper())}</div>' if spec.get("kicker") else ""}
          <div class="accent-bar"></div><h1>{esc(spec.get("title", ""))}</h1>
          {f'<p class="subtitle light">{esc(spec["subtitle"])}</p>' if spec.get("subtitle") else ""}</div></div>'''
    if t == "image_split":
        bl = "".join(f'<li>{esc(b.get("point", "") if isinstance(b, dict) else b)}'
                     f'{"<div class=detail>" + esc(b["detail"]) + "</div>" if isinstance(b, dict) and b.get("detail") else ""}</li>'
                     for b in spec.get("bullets", []))
        side = spec.get("side", "right")
        return f'''<div class="slide split {side}"><div class="split-text">{head(spec)}
          {f'<p class="lead">{esc(spec["text"])}</p>' if spec.get("text") else ""}<ul class="bullets">{bl}</ul></div>
          <div class="split-img">{img(spec.get("image"), "cover", (1300, 1650))}</div></div>'''
    if t == "gallery":
        items = "".join(f'<figure>{img(i.get("image"), "cover", (1200, 900))}<figcaption>{esc(i.get("caption", ""))}</figcaption></figure>'
                        for i in spec.get("items", [])[:6])
        return f'<div class="slide">{head(spec)}<div class="gallery">{items}</div></div>'
    if t == "quote_image":
        return f'''<div class="slide hero-img">{img(spec.get("image") or {"art": "mesh", "dark": True}, "bleed")}<div class="shade full"></div>
          <div class="quote-wrap"><div class="qmark">“</div><blockquote>{esc(spec.get("quote", ""))}</blockquote>
          <div class="qauthor">— {esc(spec.get("author", ""))}</div></div></div>'''
    if t == "chart":
        side = ""
        if spec.get("insight") or spec.get("takeaways"):
            tk_ = "".join(f"<li>{esc(x)}</li>" for x in spec.get("takeaways", []))
            side = f'<div class="insight"><div class="ins-text">{esc(spec.get("insight", ""))}</div><ul class="bullets small">{tk_}</ul></div>'
        src = f'<div class="source">{esc(spec["source"])}</div>' if spec.get("source") else ""
        return f'<div class="slide">{head(spec)}<div class="chart-row"><div class="chart-box">{chart_img(spec, theme)}</div>{side}</div>{src}</div>'
    if t == "kpi":
        cards = ""
        for m in spec.get("metrics", [])[:4]:
            d = ""
            if m.get("delta"):
                good = m.get("good", True)
                d = f'<div class="delta {"good" if good else "bad"}">{"▲" if good else "▼"} {esc(m["delta"])}</div>'
            cards += f'<div class="kpi-card">{icon_img(m.get("icon"), theme["primary"], "kpi-ico")}<div class="kpi-label">{esc(m.get("label", ""))}</div><div class="kpi-value">{esc(m.get("value", ""))}</div>{d}</div>'
        ch = f'<div class="chart-box wide">{chart_img(spec["chart"], theme)}</div>' if spec.get("chart") else ""
        return f'<div class="slide">{head(spec)}<div class="kpi-row">{cards}</div>{ch}</div>'
    if t == "diagram":
        return f'<div class="slide">{head(spec)}{_diagram(theme, spec)}' + (
            f'<div class="source center">{esc(spec["caption"])}</div>' if spec.get("caption") else "") + "</div>"
    if t == "objectives":
        items = "".join(f'<div class="obj"><div class="obj-n">{i + 1:02d}</div><div class="obj-t">'
                        f'{"<b>" + esc(it.get("verb", "")) + "</b> " if isinstance(it, dict) and it.get("verb") else ""}'
                        f'{esc(it.get("text", "") if isinstance(it, dict) else it)}</div></div>'
                        for i, it in enumerate(spec.get("items", [])[:6]))
        return f'<div class="slide">{head(spec, "Objectives")}<div class="obj-grid">{items}</div></div>'
    if t == "quiz":
        letters = "أبجد" if RTL else "ABCD"
        opts = ""
        for i, o in enumerate(spec.get("options", [])[:4]):
            right = spec.get("reveal") and spec.get("answer") == i
            cls = "right" if right else ("dim" if spec.get("reveal") else "")
            opts += f'<div class="opt {cls}"><span class="opt-l">{"✓" if right else letters[i]}</span>{esc(o)}</div>'
        ex = f'<p class="explain">{esc(spec["explanation"])}</p>' if spec.get("reveal") and spec.get("explanation") else ""
        lab = spec.get("label", "اختبر نفسك" if RTL else "Quick check")
        return f'<div class="slide"><div class="kicker">{esc(lab.upper())}</div><h2 class="q">{esc(spec.get("question", ""))}</h2><div class="opts">{opts}</div>{ex}</div>'
    if t == "activity":
        steps = "".join(f'<li><span>{i + 1}</span>{esc(s)}</li>' for i, s in enumerate(spec.get("steps", [])[:6]))
        mins = f'<div class="act-min">{spec["minutes"]} {"دقيقة" if RTL else "min"}</div>' if spec.get("minutes") else ""
        dl = f'<div class="deliver">{"التسليم: " if RTL else "Deliver: "}{esc(spec["deliverable"])}</div>' if spec.get("deliverable") else ""
        lab = spec.get("label", "نشاط" if RTL else "Activity")
        return f'''<div class="slide activity"><div class="act-side">{icon_img(spec.get("icon", "mdi:pencil-ruler"), theme["primary"], "act-ico")}
          <div class="act-lab">{esc(lab.upper())}</div>{mins}<div class="act-mode">{esc(spec.get("mode", ""))}</div></div>
          <div class="act-main"><h2>{esc(spec.get("title", ""))}</h2><ol class="steps">{steps}</ol>{dl}</div></div>'''
    if t == "definition":
        im = f'<div class="def-img">{img(spec["image"], "cover", (1100, 1300))}</div>' if spec.get("image") else ""
        ex = f'<div class="def-ex"><div class="kicker small">{"مثال" if RTL else "EXAMPLE"}</div>{esc(spec["example"])}</div>' if spec.get("example") else ""
        mi = f'<div class="def-mis">⚠ {esc(spec["mistake"])}</div>' if spec.get("mistake") else ""
        return f'''<div class="slide def"><div class="def-text"><div class="kicker">{esc((spec.get("label") or ("مصطلح" if RTL else "Key term")).upper())}</div>
          <h1>{esc(spec.get("term", ""))}</h1><div class="accent-bar small"></div><p class="lead">{esc(spec.get("definition", ""))}</p>{ex}{mi}</div>{im}</div>'''
    if t == "credits":
        return f'<div class="slide">{head(spec, "حقوق الصور" if RTL else "Image credits")}<div class="credits">' + "".join(
            f"<p>{esc(l)}</p>" for l in spec.get("lines", [])) + "</div></div>"
    return None


def _diagram(theme, spec):
    kind = spec.get("kind", "cycle")
    items = spec.get("items", [])
    if kind == "cycle":
        n = max(len(items), 2)
        nodes = "".join(f'<div class="cy-node {"hot" if i == 0 else ""}" style="--a:{i * 360 / n}deg"><b>{i + 1}. {esc(it.get("label", ""))}</b>'
                        f'<small>{esc(it.get("detail", ""))}</small></div>' for i, it in enumerate(items))
        return f'<div class="cycle"><div class="cy-ring"></div><div class="cy-center">{esc(spec.get("center", ""))}</div>{nodes}</div>'
    if kind in ("pyramid", "funnel"):
        n = max(len(items), 1)
        rows = ""
        for i, it in enumerate(items):
            w = (100 * (i + 1) / n) if kind == "pyramid" else (100 - 65 * i / max(n - 1, 1))
            lab = str(i + 1) if kind == "pyramid" else esc(it.get("value", it.get("label", "")))
            rows += (f'<div class="lvl"><div class="lvl-shape-wrap"><div class="lvl-shape {kind}" style="width:{w:.0f}%;--o:{1 - 0.12 * i:.2f}">{lab}</div></div>'
                     f'<div class="lvl-text"><b>{esc(it.get("label", ""))}</b><small>{esc(it.get("detail", ""))}</small></div></div>')
        return f'<div class="levels">{rows}</div>'
    if kind == "hierarchy":
        root = items[0] if items else {}
        kids = "".join(f'<div class="h-kid"><div class="h-node">{esc(k.get("label", ""))}<small>{esc(k.get("detail", ""))}</small></div>'
                       + "".join(f'<div class="h-leaf">{esc(g.get("label", g) if isinstance(g, dict) else g)}</div>' for g in k.get("children", [])[:4])
                       + "</div>" for k in root.get("children", []))
        return f'<div class="hier"><div class="h-node root">{esc(root.get("label", ""))}<small>{esc(root.get("detail", ""))}</small></div><div class="h-kids">{kids}</div></div>'
    if kind == "venn":
        circ = "".join(f'<div class="v-c v{i}"><span>{esc(it.get("label", ""))}</span></div>' for i, it in enumerate(items[:3]))
        return f'<div class="venn n{min(len(items), 3)}">{circ}<div class="v-center">{esc(spec.get("center", ""))}</div></div>'
    if kind == "matrix":
        cells = "".join(f'<div class="m-cell {"hot" if it.get("highlight") else ""}"><b>{esc(it.get("label", ""))}</b><small>{esc(it.get("detail", ""))}</small></div>'
                        for it in (items + [{}] * 4)[:4])
        ax = spec.get("axes", ["", ""])
        return f'<div class="matrix-wrap"><div class="m-y">{esc(ax[1] if len(ax) > 1 else "")} ↑</div><div class="matrix">{cells}</div><div class="m-x">{esc(ax[0] if ax else "")} →</div></div>'
    return ""


EXTRA_CSS = """
.hero-img { position:relative; height:100%; display:flex; align-items:center; padding:0 7vw; }
.bleed { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; z-index:0; }
.shade { position:absolute; inset:0; background:linear-gradient(90deg, rgba(8,10,18,.92) 0%, rgba(8,10,18,.75) 45%, rgba(8,10,18,.15) 100%); z-index:1; }
[dir=rtl] .shade { background:linear-gradient(270deg, rgba(8,10,18,.92) 0%, rgba(8,10,18,.75) 45%, rgba(8,10,18,.15) 100%); }
.shade.full { background:rgba(8,10,18,.62) !important; }
.hero-text, .quote-wrap { position:relative; z-index:2; max-width:58%; color:#fff; }
.subtitle.light { color:#E6E8EE; }
.quote-wrap { max-width:80%; } .qmark { font:700 120px/0.6 Georgia,serif; color:var(--primary); }
blockquote { margin:0; font-family:var(--heading-font); font-weight:700; font-size:clamp(24px,3vw,40px); }
.qauthor { color:var(--primary); font-weight:700; margin-top:24px; font-size:20px; }
.slide.split { display:flex; padding:0; height:100%; } .split-text { flex:1; padding:6vw 4vw 6vw 7vw; }
[dir=rtl] .split-text { padding:6vw 7vw 6vw 4vw; }
.split-img { width:44%; } .split.left { flex-direction:row-reverse; } .cover { width:100%; height:100%; object-fit:cover; display:block; }
.lead { font-size:clamp(16px,1.6vw,22px); max-width:60ch; }
.gallery { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:18px; height:58vh; }
.gallery figure { margin:0; display:flex; flex-direction:column; } .gallery img { flex:1; min-height:0; border-radius:12px; }
.gallery figcaption { color:var(--secondary); font-size:14px; margin-top:8px; }
.chart-row { display:flex; gap:28px; align-items:stretch; } .chart-box { flex:1; } .chart-box.wide { margin-top:18px; }
.chart-img { width:100%; max-height:56vh; object-fit:contain; }
.insight { width:30%; background:var(--bg-alt); border-radius:16px; padding:24px; }
.ins-text { font-family:var(--heading-font); font-weight:700; font-size:22px; margin-bottom:16px; }
.bullets.small li { font-size:15px; } .source { color:var(--secondary); font-size:13px; font-style:italic; margin-top:8px; } .center { text-align:center; }
.kpi-row { display:flex; gap:20px; } .kpi-card { flex:1; background:var(--bg-alt); border-radius:16px; padding:18px 22px; position:relative; }
.kpi-ico { position:absolute; top:16px; inset-inline-end:16px; width:34px; } .kpi-label { color:var(--secondary); font-weight:700; font-size:14px; }
.kpi-value { font-family:var(--heading-font); font-weight:700; font-size:clamp(30px,3.6vw,48px); } .delta.good { color:#1E9E5A; font-weight:700; } .delta.bad { color:#D64545; font-weight:700; }
.obj-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(420px,1fr)); gap:16px; }
.obj { display:flex; background:var(--bg-alt); border-radius:14px; overflow:hidden; min-height:84px; }
.obj-n { background:var(--primary); color:#fff; font:700 24px var(--heading-font); width:84px; display:flex; align-items:center; justify-content:center; }
.obj-t { padding:16px 20px; font-size:19px; display:flex; align-items:center; } .obj-t b { color:var(--primary); margin-inline-end:6px; }
.q { font-size:clamp(24px,2.8vw,36px); } .opts { display:grid; grid-template-columns:1fr 1fr; gap:18px; margin-top:24px; }
.opt { background:var(--bg-alt); border-radius:16px; padding:24px; font-size:20px; display:flex; align-items:center; gap:16px; }
.opt-l { width:42px; height:42px; border-radius:50%; background:var(--primary); color:#fff; display:inline-flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0; }
.opt.right { background:var(--primary); color:#fff; font-weight:700; } .opt.right .opt-l { background:#fff; color:var(--primary); } .opt.dim { opacity:.55; }
.explain { color:var(--secondary); font-size:17px; margin-top:18px; }
.slide.activity { display:flex; padding:0; height:100%; } .act-side { width:31%; background:var(--primary); color:#fff; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:10px; }
.act-ico { width:110px; padding:22px; background:#fff; border-radius:50%; filter:none; } .act-lab { font-weight:700; letter-spacing:.12em; }
.act-min { font:700 48px var(--heading-font); } .act-main { flex:1; padding:6vw 5vw; }
.steps { list-style:none; padding:0; } .steps li { display:flex; gap:16px; align-items:center; font-size:19px; margin:14px 0; }
.steps span { width:34px; height:34px; border-radius:50%; background:var(--primary); color:#fff; display:inline-flex; align-items:center; justify-content:center; font-weight:700; flex-shrink:0; }
.deliver { background:var(--bg-alt); border-radius:14px; padding:14px 20px; font-weight:700; margin-top:20px; }
.slide.def { display:flex; gap:4vw; align-items:center; } .def-text { flex:1; } .def-img { width:30%; height:62vh; } .def-img img { border-radius:16px; }
.def-ex { background:var(--bg-alt); border-radius:14px; padding:14px 20px; margin-top:16px; font-size:17px; } .kicker.small { font-size:11px; }
.def-mis { color:var(--secondary); margin-top:14px; }
.cycle { position:relative; height:60vh; } .cy-ring { position:absolute; left:50%; top:50%; width:40vh; height:40vh; transform:translate(-50%,-50%); border:2px dashed var(--secondary); border-radius:50%; }
.cy-center { position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); font:700 22px var(--heading-font); color:var(--primary); }
.cy-node { position:absolute; left:50%; top:50%; width:220px; transform:translate(-50%,-50%) rotate(var(--a)) translateY(-25vh) rotate(calc(-1 * var(--a))); background:var(--bg-alt); border-radius:14px; padding:12px; text-align:center; }
.cy-node.hot { background:var(--primary); color:#fff; } .cy-node small { display:block; color:var(--secondary); }
.levels { display:flex; flex-direction:column; gap:8px; } .lvl { display:flex; align-items:center; gap:30px; }
.lvl-shape-wrap { width:48%; display:flex; justify-content:center; } .lvl-shape { background:var(--primary); opacity:var(--o); color:#fff; font-weight:700; text-align:center; padding:16px 0; border-radius:10px; }
.lvl-text b { display:block; font-size:19px; } .lvl-text small { color:var(--secondary); font-size:14px; }
.hier { text-align:center; } .h-node { display:inline-block; background:var(--bg-alt); border-radius:12px; padding:12px 18px; font-weight:700; min-width:160px; }
.h-node.root { background:var(--primary); color:#fff; margin-bottom:30px; } .h-node small { display:block; font-weight:400; opacity:.8; }
.h-kids { display:flex; gap:18px; justify-content:center; } .h-kid { display:flex; flex-direction:column; gap:8px; } .h-leaf { border:1px solid var(--secondary); border-radius:10px; padding:6px; font-size:14px; }
.venn { position:relative; height:58vh; } .v-c { position:absolute; width:34vh; height:34vh; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; }
.v0 { background:color-mix(in srgb, var(--primary) 35%, transparent); left:calc(50% - 28vh); top:6vh; } .v1 { background:color-mix(in srgb, var(--secondary) 35%, transparent); left:calc(50% - 6vh); top:6vh; }
.v2 { background:color-mix(in srgb, var(--text) 25%, transparent); left:calc(50% - 17vh); top:22vh; } .v-center { position:absolute; left:50%; top:30vh; transform:translate(-50%,-50%); font-weight:700; color:var(--primary); }
.matrix-wrap { display:grid; grid-template-columns:auto 1fr; gap:10px; } .matrix { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
.m-cell { background:var(--bg-alt); border-radius:14px; padding:18px; min-height:20vh; } .m-cell.hot { background:var(--primary); color:#fff; } .m-cell small { display:block; margin-top:8px; opacity:.8; }
.m-y { writing-mode:vertical-rl; transform:rotate(180deg); color:var(--secondary); font-weight:700; } .m-x { grid-column:2; text-align:center; color:var(--secondary); font-weight:700; }
.credits p { font-size:13px; color:var(--secondary); margin:4px 0; }
.ico { width:60%; } .icon-glyph img.ico, .proc-ico img { width:62%; }
.slide-bg { position:absolute; inset:0; width:100%; height:100%; object-fit:cover; z-index:0; }
.slide-bg-shade { position:absolute; inset:0; z-index:0; }
.slide-wrap > .slide { position:relative; z-index:1; }
[dir=rtl] .tl-item { transform:translate(50%,-50%); } [dir=rtl] .proc-item { transform:translateX(50%); }
.code-panel, code, pre { direction:ltr; text-align:left; unicode-bidi:isolate; }
[dir=rtl] .bullets li { padding-left:0; padding-right:28px; } [dir=rtl] .bullets li::before { left:auto; right:0; }
"""
