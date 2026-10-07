"""Designed-PDF renderer: normalised Doc → print HTML/CSS → Chromium PDF.

The PDF is the "agency" version of a document: full-bleed covers, section openers, grids, cards, icon
callouts, charts, running headers and page numbers, real TOC page numbers (two-pass), Arabic RTL with
proper shaping (the browser shapes Arabic) and fonts embedded in the PDF.
"""
from __future__ import annotations

import base64
import mimetypes
import re
from pathlib import Path

from pdk.render import html_to_pdf, pdf_pages
from pdk.text import esc, inline_md, is_rtl
from pdk.themes import mix

GOOGLE_FONTS = {
    "Cairo": "Cairo:wght@400;600;700;800", "Tajawal": "Tajawal:wght@400;500;700;800",
    "IBM Plex Sans Arabic": "IBM+Plex+Sans+Arabic:wght@400;500;600;700", "Amiri": "Amiri:wght@400;700",
    "Noto Naskh Arabic": "Noto+Naskh+Arabic:wght@400;600;700", "El Messiri": "El+Messiri:wght@400;600;700",
    "Inter": "Inter:wght@400;500;600;700;800", "Poppins": "Poppins:wght@400;500;600;700",
    "Playfair Display": "Playfair+Display:wght@500;700;800", "Merriweather": "Merriweather:wght@400;700",
    "Lora": "Lora:wght@400;600;700", "Montserrat": "Montserrat:wght@400;600;700;800",
}


def uri(path) -> str:
    if not path:
        return ""
    p = Path(path)
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def md(s):
    return inline_md(s).replace("\n", "<br>")


def dir_attr(s):
    return ' dir="rtl"' if is_rtl(s) else ' dir="ltr"'


class HtmlRenderer:
    def __init__(self, doc):
        self.d = doc
        self.tk = doc.tk
        self.L = doc.label
        self.fig = 0
        self.tab = 0

    # ================================================================== public
    def render(self, out_pdf: Path, *, offline=False) -> dict:
        page_map = {}
        html = self.html(page_map, offline=offline)
        rep = html_to_pdf(html, out_pdf, base_dir=out_pdf.parent)
        if self.d.toc and self.d.outline:
            page_map = self._outline_pages(out_pdf)
            if page_map:
                html = self.html(page_map, offline=offline)
                rep = html_to_pdf(html, out_pdf, base_dir=out_pdf.parent)
        rep["html"] = html
        return rep

    def _outline_pages(self, pdf):
        """Read heading → page from the PDF outline (Chromium writes it from <h1>-<h3>)."""
        try:
            import pymupdf as fitz
        except ImportError:
            return {}
        out = {}
        with fitz.open(str(pdf)) as d:
            toc = d.get_toc(simple=True)

        def words(t):   # Chromium writes RTL outline text in visual order → compare word SETS, digits removed
            return frozenset(w for w in re.findall(r"[^\W\d_]+", t))
        entries = [(words(t), p) for _, t, p in toc]
        k = 0
        for o in self.d.outline:
            target = words(o["text"])
            for j in range(k, len(entries)):
                if entries[j][0] == target:
                    out[o["id"]] = entries[j][1]
                    k = j + 1
                    break
        return out

    # ================================================================== page
    def html(self, page_map, *, offline=False) -> str:
        d = self.d
        self.page_map = page_map
        self.fig = self.tab = 0
        body = []
        lay = d.layout
        if lay == "flow":
            body.append(self.cover())
            if d.toc and d.outline:
                body.append(self.toc_page())
            body.append(f'<main class="flow{" cols2" if d.preset.get("columns") == 2 else ""}">{self.blocks(d.blocks)}</main>')
        else:
            body.append(getattr(self, f"layout_{lay}")())
        if d.credits():
            body.append('<section class="credits"><h4>' + ("حقوق الصور" if d.rtl else "Image credits") + "</h4>"
                        + "".join(f"<p>{esc(c)}</p>" for c in d.credits()) + "</section>")
        fonts = {d.tk["head_font"], d.tk["body_font"], d.tk["head_font_latin"], d.tk["body_font_latin"]}
        link = ""
        fams = [GOOGLE_FONTS[f] for f in fonts if f in GOOGLE_FONTS]
        if fams and not offline:
            link = ('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
                    f'<link href="https://fonts.googleapis.com/css2?family={"&family=".join(fams)}&display=block" rel="stylesheet">')
        title = esc(d.meta.get("title", "Document"))
        return (f'<!doctype html><html lang="{d.lang}" dir="{"rtl" if d.rtl else "ltr"}"><head><meta charset="utf-8">'
                f"<title>{title}</title>{link}<style>{self.css()}</style></head>"
                f'<body class="t-{d.type} l-{lay}">{"".join(body)}</body></html>')

    # ================================================================== css
    def css(self) -> str:
        t, d = self.tk, self.d
        w, h = d.page_mm
        mt, mr, mb, ml = d.margins_mm
        head, body = t["head_font"], t["body_font"]
        lat_h, lat_b = t["head_font_latin"], t["body_font_latin"]
        fallback = "'Cairo','Tajawal','Noto Naskh Arabic','Geeza Pro','Arial'" if d.rtl else "'Helvetica Neue','Helvetica','Inter','Arial'"
        header_txt = d.spec.get("header") if d.spec.get("header") is not None else (d.meta.get("title", "") if d.preset.get("header") else "")
        footer_txt = d.spec.get("footer", d.meta.get("org", ""))
        pg = f'"{d.L["page"]} " counter(page) " {d.L["of"]} " counter(pages)'
        start, end = ("right", "left") if d.rtl else ("left", "right")
        acc, acc2 = t["accent"], t["accent_2"]
        return f"""
:root {{ --paper:#{t['paper']}; --paper2:#{t['paper_alt']}; --ink:#{t['ink']}; --ink2:#{t['ink_soft']}; --muted:#{t['muted']};
  --line:#{t['line']}; --acc:#{acc}; --acc2:#{acc2}; --accsoft:#{t['accent_soft']}; --onacc:#{t['on_accent']};
  --stage:#{t['stage_bg']}; --stage2:#{t['stage_bg_alt']}; --stagetext:#{t['stage_text']};
  --panel:#{t['stage_bg'] if t['style'] == 'dark' else t['accent']}; --paneltext:#{t['stage_text'] if t['style'] == 'dark' else t['on_accent']};
  --hf:'{head}','{lat_h}',{fallback},sans-serif; --bf:'{body}','{lat_b}',{fallback},sans-serif; }}
@page {{ size:{w}mm {h}mm; margin:{mt}mm {mr}mm {mb}mm {ml}mm; background:#{t['paper']};
  @top-{start} {{ content:"{esc(header_txt)}"; font:600 8pt var(--bf); color:var(--muted); letter-spacing:.04em; }}
  @bottom-{start} {{ content:"{esc(footer_txt)}"; font:8pt var(--bf); color:var(--muted); }}
  @bottom-{end} {{ content:{pg}; font:600 8pt var(--bf); color:var(--muted); }} }}
@page cover {{ margin:0; @top-{start}{{content:none}} @bottom-{start}{{content:none}} @bottom-{end}{{content:none}} }}
@page bare {{ margin:0; @top-{start}{{content:none}} @bottom-{start}{{content:none}} @bottom-{end}{{content:none}} }}
@page plain {{ margin:{mt}mm {mr}mm {mb}mm {ml}mm; @top-{start}{{content:none}} @bottom-{start}{{content:none}} @bottom-{end}{{content:none}} }}
* {{ box-sizing:border-box; }}
html {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
body {{ margin:0; font:10.5pt/1.62 var(--bf); color:var(--ink); background:var(--paper); }}
{"body { line-height:1.85; }" if d.rtl else ""}
h1,h2,h3,h4 {{ font-family:var(--hf); color:var(--ink); line-height:1.25; break-after:avoid; }}
h1 {{ font-size:22pt; font-weight:800; margin:0 0 10pt; }}
h2 {{ font-size:15pt; font-weight:700; margin:20pt 0 6pt; }}
h3 {{ font-size:12pt; font-weight:700; margin:14pt 0 4pt; color:var(--ink2); }}
h4 {{ font-size:10.5pt; font-weight:700; margin:10pt 0 3pt; }}
h2 .num, h1 .num, h3 .num, h4 .num {{ color:var(--acc); margin-inline-end:8pt; font-variant-numeric:tabular-nums; }}
h2.rule {{ padding-bottom:5pt; border-bottom:1.5pt solid var(--line); }}
p {{ margin:0 0 8pt; orphans:3; widows:3; }}
a {{ color:var(--acc); text-decoration:none; }}
strong {{ font-weight:700; color:var(--ink); }} em.hl {{ font-style:normal; color:var(--acc); font-weight:700; }}
code {{ font-family:'JetBrains Mono','SF Mono',Menlo,Consolas,monospace; font-size:.9em; background:var(--paper2); padding:1pt 4pt; border-radius:3pt; direction:ltr; unicode-bidi:isolate; }}
.lead {{ font-size:12.5pt; color:var(--ink2); line-height:1.6; }}
ul.b, ol.b {{ margin:0 0 9pt; padding-inline-start:16pt; }} ul.b li, ol.b li {{ margin:0 0 4pt; }}
ul.b li::marker {{ color:var(--acc); }} ol.b li::marker {{ color:var(--acc); font-weight:700; }}
ul.check {{ list-style:none; padding:0; margin:0 0 9pt; }} ul.check li {{ padding-inline-start:20pt; position:relative; margin-bottom:5pt; }}
ul.check li::before {{ content:""; position:absolute; inset-inline-start:0; top:3pt; width:10pt; height:10pt; border:1.3pt solid var(--acc); border-radius:2.5pt; }}
ul.check li.done::before {{ background:var(--acc); }}
.callout {{ display:flex; gap:10pt; padding:10pt 12pt; border-radius:8pt; margin:10pt 0; background:var(--accsoft); break-inside:avoid; }}
.callout .ci {{ width:20pt; height:20pt; flex:none; }} .callout .ct {{ font:700 9pt var(--hf); color:var(--acc); text-transform:uppercase; letter-spacing:.05em; margin-bottom:2pt; }}
.callout.warning {{ background:#FFF4E5; }} .callout.warning .ct {{ color:#B45309; }}
.callout.success {{ background:#E9F7EF; }} .callout.success .ct {{ color:#1E7A46; }}
.callout.note {{ background:var(--paper2); }} .callout.note .ct {{ color:var(--ink2); }}
.callout p:last-child {{ margin:0; }}
blockquote {{ margin:12pt 0; padding:4pt 14pt; border-inline-start:3pt solid var(--acc); font:italic 11.5pt/1.55 var(--hf); color:var(--ink2); }}
blockquote cite {{ display:block; font:600 9pt var(--bf); font-style:normal; color:var(--muted); margin-top:4pt; }}
.pull {{ font:800 17pt/1.35 var(--hf); color:var(--acc); margin:14pt 0; padding:10pt 0; border-top:1.5pt solid var(--acc); border-bottom:1.5pt solid var(--acc); break-inside:avoid; }}
table.t {{ width:100%; border-collapse:collapse; margin:8pt 0 4pt; font-size:9.5pt; break-inside:auto; }}
table.t th {{ background:var(--acc); color:var(--onacc); font:700 9pt var(--hf); text-align:start; padding:6pt 8pt; }}
table.t td {{ padding:5.5pt 8pt; border-bottom:.6pt solid var(--line); vertical-align:top; }}
table.t tr:nth-child(even) td {{ background:var(--paper2); }}
table.t.minimal th {{ background:none; color:var(--ink); border-bottom:1.5pt solid var(--ink); }}
table.t.minimal tr:nth-child(even) td {{ background:none; }}
table.t td.num, table.t th.num {{ text-align:end; font-variant-numeric:tabular-nums; }}
table.t tr.total td {{ font-weight:800; border-top:1.5pt solid var(--ink); background:none; }}
tr {{ break-inside:avoid; }} thead {{ display:table-header-group; }}
.cap {{ font-size:8.5pt; color:var(--muted); margin:3pt 0 12pt; }} .cap b {{ color:var(--ink2); }}
figure {{ margin:10pt 0; break-inside:avoid; }} figure img {{ width:100%; display:block; border-radius:6pt; }}
figure.half {{ width:50%; }} figure.third {{ width:34%; }} figure.float {{ float:inline-end; margin-inline-start:14pt; }}
.stats {{ display:flex; gap:10pt; margin:12pt 0; break-inside:avoid; }}
.stat {{ flex:1; border-top:3pt solid var(--acc); padding-top:6pt; }} .stat .v {{ font:800 22pt/1.1 var(--hf); color:var(--acc); }}
.stat .l {{ font-size:8.5pt; color:var(--ink2); }}
.cards {{ display:grid; gap:10pt; margin:10pt 0; }} .cards.c2 {{ grid-template-columns:1fr 1fr; }} .cards.c3 {{ grid-template-columns:repeat(3,1fr); }} .cards.c4 {{ grid-template-columns:repeat(4,1fr); }}
.card {{ background:var(--paper2); border-radius:8pt; padding:11pt; break-inside:avoid; }}
.card .ci {{ width:22pt; height:22pt; margin-bottom:5pt; }} .card h4 {{ margin:0 0 3pt; font-size:10.5pt; }} .card p {{ font-size:9pt; margin:0; color:var(--ink2); }}
.tl {{ position:relative; margin:10pt 0; padding-inline-start:16pt; border-inline-start:2pt solid var(--line); }}
.tl-i {{ position:relative; margin-bottom:9pt; break-inside:avoid; }} .tl-i::before {{ content:""; position:absolute; inset-inline-start:-21pt; top:3pt; width:8pt; height:8pt; border-radius:50%; background:var(--acc); }}
.tl-d {{ font:700 8.5pt var(--hf); color:var(--acc); text-transform:uppercase; letter-spacing:.04em; }} .tl-t {{ font-weight:700; }}
.steps {{ counter-reset:s; margin:10pt 0; }} .step {{ display:flex; gap:10pt; margin-bottom:8pt; break-inside:avoid; }}
.step .n {{ flex:none; width:22pt; height:22pt; border-radius:50%; background:var(--acc); color:var(--onacc); font:700 10pt/22pt var(--hf); text-align:center; }}
.step h4 {{ margin:2pt 0 1pt; font-size:10.5pt; }} .step p {{ margin:0; color:var(--ink2); }}
.cols {{ display:grid; grid-template-columns:1fr 1fr; gap:16pt; }} .cols.r12 {{ grid-template-columns:1fr 2fr; }} .cols.r21 {{ grid-template-columns:2fr 1fr; }}
.def {{ border:1pt solid var(--line); border-radius:8pt; padding:9pt 12pt; margin:10pt 0; break-inside:avoid; }}
.def .term {{ font:800 12pt var(--hf); color:var(--acc); }} .def .kt {{ font:700 7.5pt var(--bf); letter-spacing:.08em; text-transform:uppercase; color:var(--muted); }}
pre.code {{ direction:ltr; text-align:left; background:#1E2433; color:#E6EDF3; border-radius:8pt; padding:10pt 12pt; font:8.8pt/1.5 'JetBrains Mono','SF Mono',Menlo,Consolas,monospace; white-space:pre-wrap; break-inside:avoid; }}
pre.code .c,pre.code .c1,pre.code .cm {{ color:#8B9AAB; font-style:italic; }} pre.code .k,pre.code .kd,pre.code .kn,pre.code .kc,pre.code .nb {{ color:#7EE0FF; }}
pre.code .s,pre.code .s1,pre.code .s2,pre.code .sa {{ color:#E8C547; }} pre.code .m,pre.code .mi,pre.code .mf {{ color:#C3A6FF; }} pre.code .nf,pre.code .nc {{ color:#9BE36D; }} pre.code .o,pre.code .ow {{ color:#FF6B9D; }}
dl.kv {{ display:grid; grid-template-columns:max-content 1fr; gap:3pt 14pt; margin:8pt 0; }} dl.kv dt {{ font-weight:700; color:var(--muted); font-size:9pt; }} dl.kv dd {{ margin:0; }}
.sig {{ display:flex; gap:30pt; margin-top:30pt; break-inside:avoid; }} .sig > div {{ flex:1; }} .sig .line {{ border-bottom:1pt solid var(--ink); height:34pt; }}
.sig .nm {{ font-weight:700; margin-top:4pt; }} .sig .rl {{ font-size:8.5pt; color:var(--muted); }}
hr.div {{ border:0; border-top:1pt solid var(--line); margin:14pt 0; }}
.box {{ border:1.2pt solid var(--line); border-radius:9pt; padding:10pt 13pt; margin:10pt 0; break-inside:avoid; }} .box > h4 {{ margin-top:0; color:var(--acc); }}
.gallery {{ display:grid; gap:8pt; grid-template-columns:repeat(3,1fr); margin:10pt 0; }} .gallery img {{ width:100%; aspect-ratio:4/3; object-fit:cover; border-radius:6pt; }}
.gallery figcaption {{ font-size:8pt; color:var(--muted); }}
.lines {{ margin:6pt 0; }} .lines div {{ border-bottom:.7pt solid var(--line); height:20pt; }}
.sched {{ width:100%; border-collapse:collapse; font-size:9pt; }} .sched td {{ padding:6pt 8pt; border-bottom:.6pt solid var(--line); vertical-align:top; }}
.sched td.tm {{ width:70pt; font:700 9pt var(--hf); color:var(--acc); white-space:nowrap; }} .sched td.du {{ width:48pt; color:var(--muted); white-space:nowrap; }}
/* questions */
.qs {{ counter-reset:q; }} .q {{ margin:0 0 12pt; break-inside:avoid; }} .q .qh {{ display:flex; gap:8pt; font-weight:600; }}
.q .qn {{ flex:none; font:800 10pt var(--hf); color:var(--acc); min-width:18pt; }} .q .pts {{ margin-inline-start:auto; font-size:8pt; color:var(--muted); white-space:nowrap; }}
.q ol.opts {{ list-style:none; padding:0; margin:5pt 0 0; padding-inline-start:26pt; display:grid; grid-template-columns:1fr 1fr; gap:3pt 16pt; }}
.q ol.opts li {{ display:flex; gap:6pt; }} .q ol.opts .bx {{ flex:none; width:15pt; height:15pt; border:1pt solid var(--ink2); border-radius:50%; font:700 7.5pt/13pt var(--hf); text-align:center; color:var(--ink2); }}
.q ol.opts li.right .bx {{ background:var(--acc); border-color:var(--acc); color:var(--onacc); }} .q ol.opts li.right {{ font-weight:700; }}
.q .ans {{ margin:5pt 0 0; padding-inline-start:26pt; color:#1E7A46; font-weight:600; font-size:9.5pt; }}
.q .alines {{ padding-inline-start:26pt; }}
/* cover */
.cover {{ page:cover; position:relative; width:{w}mm; height:{h}mm; overflow:hidden; break-after:page; background:var(--paper); }}
.cover .bg {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
.cover .shade {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(10,12,20,.15) 0%, rgba(10,12,20,.35) 40%, rgba(10,12,20,.9) 100%); }}
.cover .ct {{ position:absolute; inset-inline:18mm; bottom:24mm; color:#fff; }}
.cover .kick {{ font:700 10pt var(--hf); letter-spacing:.14em; text-transform:uppercase; color:var(--acc2); margin-bottom:8pt; }}
.cover h1 {{ color:inherit; font-size:34pt; line-height:1.12; margin:0 0 10pt; max-width:150mm; }}
.cover .sub {{ font-size:13pt; opacity:.9; max-width:140mm; }}
.cover .meta {{ margin-top:18pt; display:flex; gap:22pt; font-size:9pt; opacity:.92; }} .cover .meta b {{ display:block; font-size:7.5pt; letter-spacing:.08em; text-transform:uppercase; opacity:.75; }}
.cover .logo {{ position:absolute; top:16mm; inset-inline-start:18mm; height:13mm; }}
.cover.c-photo .kick {{ color:#fff; opacity:.85; }}
.cover.c-minimal .ct, .cover.c-band .ct {{ color:var(--ink); }} .cover.c-minimal .kick, .cover.c-band .kick {{ color:var(--acc); }}
.cover.c-minimal .ct {{ top:62mm; bottom:auto; }} .cover.c-minimal .bar {{ position:absolute; top:52mm; inset-inline-start:18mm; width:28mm; height:2.2mm; background:var(--acc); }}
.cover.c-minimal .foot {{ position:absolute; bottom:18mm; inset-inline:18mm; border-top:1pt solid var(--line); padding-top:8pt; font-size:9pt; color:var(--muted); display:flex; justify-content:space-between; }}
.cover.c-band .band {{ position:absolute; top:0; inset-inline:0; height:46%; background:var(--acc); overflow:hidden; }} .cover.c-band .band img {{ width:100%; height:100%; object-fit:cover; mix-blend-mode:multiply; opacity:.55; }}
.cover.c-band .ct {{ top:52%; bottom:auto; }}
.cover.c-split .panel {{ position:absolute; top:0; bottom:0; inset-inline-start:0; width:46%; background:var(--panel); }}
.cover.c-split .pic {{ position:absolute; top:0; bottom:0; inset-inline-end:0; width:54%; }} .cover.c-split .pic img {{ width:100%; height:100%; object-fit:cover; }}
.cover.c-split .ct {{ inset-inline-start:14mm; inset-inline-end:58%; top:70mm; bottom:auto; color:var(--paneltext); }} .cover.c-split .kick {{ color:var(--paneltext); opacity:.8; }} .cover.c-split h1 {{ font-size:28pt; }}
.cover.c-art .ct {{ color:var(--ink); }} .cover.c-art .kick {{ color:var(--acc); }}
.cover.c-art.dark .ct {{ color:#fff; }}
/* toc */
.tocp {{ break-after:page; }} .tocp h1 {{ margin-bottom:16pt; }}
.toc a {{ display:flex; align-items:baseline; color:var(--ink); padding:4pt 0; }} .toc a.l1 {{ font:700 11pt var(--hf); margin-top:6pt; }}
.toc a.l2 {{ padding-inline-start:18pt; font-size:9.8pt; color:var(--ink2); }} .toc .num {{ color:var(--acc); min-width:22pt; font-weight:700; }}
.toc .dots {{ flex:1; border-bottom:1pt dotted var(--line); margin:0 6pt; transform:translateY(-3pt); }} .toc .pg {{ font-variant-numeric:tabular-nums; color:var(--muted); min-width:16pt; text-align:end; }}
/* section opener */
.sec {{ break-before:page; padding-top:20mm; margin-bottom:14pt; }} .sec .sn {{ font:800 60pt/1 var(--hf); color:var(--accsoft); -webkit-text-stroke:1.2pt var(--acc); }}
.sec h1 {{ font-size:26pt; margin-top:6pt; }} .sec .intro {{ font-size:12pt; color:var(--ink2); max-width:140mm; }}
.sec img {{ width:100%; height:62mm; object-fit:cover; border-radius:8pt; margin-top:10pt; }}
.sec.chapter .sn::before {{ content:"{esc(d.L['chapter'])} "; font-size:14pt; -webkit-text-stroke:0; color:var(--acc); letter-spacing:.1em; display:block; }}
.mast {{ border-top:6pt solid var(--acc); border-bottom:1.2pt solid var(--ink); padding:8pt 0 6pt; margin-bottom:14pt; display:grid; grid-template-columns:1fr auto; align-items:end; }}
.mast-k {{ grid-column:1 / -1; font:700 8.5pt var(--hf); letter-spacing:.14em; text-transform:uppercase; color:var(--acc); }}
.mast-t {{ font:800 30pt/1.1 var(--hf); }} .mast-i {{ font-size:9pt; color:var(--muted); }}
main.flow.cols2 {{ column-count:2; column-gap:9mm; }} main.flow.cols2 h2 {{ column-span:all; }}
.credits {{ break-before:auto; margin-top:24pt; padding-top:8pt; border-top:1pt solid var(--line); font-size:7.5pt; color:var(--muted); }} .credits h4 {{ margin:0 0 4pt; font-size:8pt; }} .credits p {{ margin:0 0 2pt; }}
/* letter & memo */
.lh {{ display:flex; justify-content:space-between; align-items:flex-start; border-bottom:2pt solid var(--acc); padding-bottom:10pt; margin-bottom:22pt; }}
.lh img {{ height:14mm; }} .lh .org {{ font:800 15pt var(--hf); color:var(--acc); }} .lh .addr {{ font-size:8.5pt; color:var(--muted); text-align:end; white-space:pre-line; }}
.letter .to {{ margin:0 0 16pt; white-space:pre-line; }} .letter .dt {{ color:var(--muted); margin-bottom:14pt; }} .letter .subj {{ font:700 11pt var(--hf); margin-bottom:12pt; }}
.memo-h {{ font:800 26pt var(--hf); color:var(--acc); letter-spacing:.06em; margin-bottom:10pt; }}
.memo-meta {{ display:grid; grid-template-columns:max-content 1fr; gap:4pt 16pt; padding:10pt 0; border-top:1pt solid var(--line); border-bottom:1pt solid var(--line); margin-bottom:16pt; }}
.memo-meta b {{ color:var(--muted); font-size:9pt; text-transform:uppercase; letter-spacing:.05em; }}
/* invoice */
.inv-top {{ display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:22pt; }} .inv-top img {{ height:15mm; }}
.inv-title {{ font:800 28pt var(--hf); color:var(--acc); letter-spacing:.04em; text-align:end; }} .inv-title small {{ display:block; font:600 9.5pt var(--bf); color:var(--muted); letter-spacing:0; }}
.inv-parties {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:14pt; margin-bottom:18pt; }} .inv-parties h5 {{ margin:0 0 3pt; font:700 7.5pt var(--bf); letter-spacing:.08em; text-transform:uppercase; color:var(--muted); }}
.inv-parties div {{ white-space:pre-line; font-size:9.5pt; }}
.inv-tot {{ margin-inline-start:auto; width:46%; margin-top:8pt; }} .inv-tot div {{ display:flex; justify-content:space-between; padding:4pt 0; border-bottom:.6pt solid var(--line); }}
.inv-tot .grand {{ background:var(--acc); color:var(--onacc); padding:8pt 10pt; border-radius:6pt; font:800 12pt var(--hf); border:0; margin-top:6pt; }}
/* cv */
.cv {{ page:bare; display:grid; grid-template-columns:66mm 1fr; min-height:{h}mm; }}
.cv .side {{ background:var(--stage); color:var(--stagetext); padding:16mm 9mm; }} .cv .side h4 {{ color:var(--acc2); font-size:8pt; letter-spacing:.12em; text-transform:uppercase; margin:16pt 0 6pt; }}
.cv .side img.ph {{ width:38mm; height:38mm; border-radius:50%; object-fit:cover; display:block; margin:0 auto 12pt; border:2pt solid var(--acc2); }}
.cv .side p, .cv .side li {{ font-size:8.8pt; }} .cv .side ul {{ list-style:none; padding:0; margin:0; }} .cv .side li {{ margin-bottom:4pt; }}
.cv .bar {{ height:4pt; background:rgba(255,255,255,.18); border-radius:2pt; margin:2pt 0 6pt; }} .cv .bar i {{ display:block; height:100%; background:var(--acc2); border-radius:2pt; }}
.cv .main {{ padding:16mm 13mm 14mm; }} .cv .nm {{ font:800 25pt/1.1 var(--hf); }} .cv .role {{ font:600 12pt var(--hf); color:var(--acc); margin:3pt 0 12pt; }}
.cv h2 {{ font-size:11pt; text-transform:uppercase; letter-spacing:.1em; color:var(--acc); border-bottom:1pt solid var(--line); padding-bottom:3pt; margin:16pt 0 8pt; }}
.xp {{ margin-bottom:10pt; break-inside:avoid; }} .xp .hd {{ display:flex; justify-content:space-between; gap:10pt; }} .xp .rl {{ font:700 10.5pt var(--hf); }} .xp .dt {{ font-size:8.5pt; color:var(--muted); white-space:nowrap; }}
.xp .org {{ font-size:9pt; color:var(--acc); font-weight:600; }} .xp ul {{ margin:3pt 0 0; padding-inline-start:14pt; font-size:9.2pt; }}
.chips {{ display:flex; flex-wrap:wrap; gap:4pt; }} .chips span {{ background:rgba(255,255,255,.12); border-radius:10pt; padding:1pt 7pt; font-size:8pt; }}
/* certificate */
.cert {{ page:bare; width:{w}mm; height:{h}mm; position:relative; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; background:var(--paper); }}
.cert .frame {{ position:absolute; inset:9mm; border:2.4pt solid var(--acc); }} .cert .frame2 {{ position:absolute; inset:12mm; border:.8pt solid var(--acc2); }}
.cert .orn {{ position:absolute; width:46mm; height:46mm; opacity:.9; }}
.cert .k {{ font:700 11pt var(--hf); letter-spacing:.3em; text-transform:uppercase; color:var(--acc2); }}
.cert h1 {{ font-size:34pt; margin:6pt 0 14pt; color:var(--acc); }} .cert .pt {{ font-size:11pt; color:var(--muted); }}
.cert .who {{ font:800 30pt var(--hf); margin:6pt 0 4pt; padding:0 20mm 6pt; border-bottom:1.2pt solid var(--acc2); }}
.cert .why {{ font-size:11.5pt; max-width:190mm; margin-top:10pt; color:var(--ink2); }} .cert img.logo {{ height:16mm; margin-bottom:8pt; }}
.cert .sigs {{ display:flex; gap:40mm; margin-top:20mm; }} .cert .sigs div {{ min-width:55mm; border-top:1pt solid var(--ink); padding-top:4pt; font-size:9pt; }}
.cert .sigs b {{ display:block; font-size:10pt; }} .cert .seal {{ position:absolute; bottom:22mm; inset-inline-end:28mm; width:30mm; height:30mm; border-radius:50%; background:var(--acc); color:var(--onacc); display:flex; align-items:center; justify-content:center; font:800 9pt var(--hf); text-align:center; box-shadow:0 0 0 3pt var(--paper), 0 0 0 4.2pt var(--acc); }}
/* handout / worksheet / exam */
.hband {{ display:flex; justify-content:space-between; align-items:flex-end; gap:14pt; border-bottom:2.5pt solid var(--acc); padding-bottom:8pt; margin-bottom:12pt; }}
.hband .k {{ font:700 8.5pt var(--hf); letter-spacing:.12em; text-transform:uppercase; color:var(--acc); }} .hband h1 {{ margin:2pt 0 0; font-size:20pt; }}
.hband img {{ height:12mm; }}
.fields {{ display:grid; grid-template-columns:2fr 1fr 1fr; gap:10pt; margin-bottom:14pt; font-size:9pt; }} .fields div {{ border-bottom:1pt solid var(--ink2); padding-bottom:2pt; color:var(--muted); }}
.instr {{ background:var(--paper2); border-radius:8pt; padding:8pt 12pt; margin-bottom:14pt; font-size:9.5pt; }}
/* flyer / one pager */
.flyer {{ page:bare; width:{w}mm; min-height:{h}mm; position:relative; }}
.flyer .hero {{ height:44%; position:relative; overflow:hidden; }} .flyer .hero img {{ width:100%; height:100%; object-fit:cover; }}
.flyer .hero .shade {{ position:absolute; inset:0; background:linear-gradient(180deg, transparent 30%, rgba(10,12,20,.85)); }}
.flyer .hero .ct {{ position:absolute; inset-inline:14mm; bottom:12mm; color:#fff; }} .flyer .hero h1 {{ color:#fff; font-size:32pt; margin:0; }}
.flyer .body {{ padding:12mm 14mm 34mm; }} .flyer .cta {{ position:absolute; bottom:0; inset-inline:0; background:var(--acc); color:var(--onacc); padding:9mm 14mm; display:flex; justify-content:space-between; align-items:center; font:800 15pt var(--hf); }}
.flyer .cta small {{ font:500 9.5pt var(--bf); display:block; opacity:.9; }}
"""

    # ================================================================== cover/toc
    def cover(self):
        d, c = self.d, self.d.cover
        style = c.get("style", "minimal")
        if style == "none":
            return ""
        m = d.meta
        if style == "masthead":     # newsletter: a title band at the top of page 1, no separate cover page
            issue = " · ".join(v for v in (m.get("issue", ""), m.get("date", "")) if v)
            return (f'<header class="mast"><div class="mast-k">{esc(m.get("org", ""))}</div><div class="mast-t">{esc(m.get("title", ""))}</div>'
                    f'<div class="mast-i">{esc(issue)}</div></header>')
        logo = f'<img class="logo" src="{uri(d.asset(c.get("logo") or ({"path": d.logo} if d.logo else None)))}">' if (c.get("logo") or d.logo) else ""
        kick = f'<div class="kick">{esc(c.get("kicker") or m.get("kicker") or "")}</div>' if (c.get("kicker") or m.get("kicker")) else ""
        sub = f'<div class="sub">{md(m.get("subtitle", ""))}</div>' if m.get("subtitle") else ""
        metas = []
        for k, lab in (("prepared_for", d.label("prepared_for")), ("author", d.label("prepared_by")), ("date", d.label("date")),
                       ("version", d.label("version"))):
            if m.get(k):
                metas.append(f"<div><b>{esc(lab)}</b>{esc(m[k])}</div>")
        meta = f'<div class="meta">{"".join(metas)}</div>' if metas else ""
        title = f'<h1>{esc(m.get("title", ""))}</h1>'
        if style == "photo":
            img = d.asset(c.get("image") or {"art": "mesh", "dark": True}, size=(1800, 2500), orientation="portrait")
            return f'<section class="cover c-photo"><img class="bg" src="{uri(img)}"><div class="shade"></div>{logo}<div class="ct">{kick}{title}{sub}{meta}</div></section>'
        if style == "art":
            dark = c.get("dark", self.tk.get("style") == "dark")
            img = d.asset(c.get("image") or {"art": c.get("art", "blobs"), "dark": dark, "seed": c.get("seed", 3)}, size=(1800, 2500))
            return f'<section class="cover c-art{" dark" if dark else ""}"><img class="bg" src="{uri(img)}">{logo}<div class="ct">{kick}{title}{sub}{meta}</div></section>'
        if style == "band":
            img = d.asset(c.get("image"), size=(1800, 1200)) if c.get("image") else d.asset({"art": "geo", "dark": False, "seed": 5}, size=(1800, 1200))
            return f'<section class="cover c-band"><div class="band"><img src="{uri(img)}"></div>{logo}<div class="ct">{kick}{title}{sub}{meta}</div></section>'
        if style == "split":
            img = d.asset(c.get("image") or {"art": "geo", "dark": True}, size=(1200, 2400), orientation="portrait")
            return f'<section class="cover c-split"><div class="panel"></div><div class="pic"><img src="{uri(img)}"></div>{logo}<div class="ct">{kick}{title}{sub}{meta}</div></section>'
        # minimal
        org = esc(m.get("org", ""))
        conf = f'<span>{esc(d.label("confidential"))}</span>' if m.get("confidential") else f"<span>{esc(m.get('date', ''))}</span>"
        return f'<section class="cover c-minimal">{logo}<div class="bar"></div><div class="ct">{kick}{title}{sub}{meta}</div><div class="foot"><span>{org}</span>{conf}</div></section>'

    def toc_page(self):
        rows = []
        for o in self.d.outline:
            pg = self.page_map.get(o["id"], "")
            num = f'<span class="num">{esc(o["num"])}</span>' if o["num"] else ""
            rows.append(f'<a class="l{o["level"]}" href="#{o["id"]}">{num}<span>{esc(o["text"])}</span><span class="dots"></span><span class="pg">{pg}</span></a>')
        return f'<section class="tocp"><h1>{esc(self.d.label("contents"))}</h1><nav class="toc">{"".join(rows)}</nav></section>'

    # ================================================================== blocks
    def blocks(self, blocks):
        return "".join(self.block(b) for b in blocks or [])

    def icon(self, ref, color=None, cls="ci"):
        if not ref:
            return ""
        p = self.d.asset({"icon": ref} if isinstance(ref, str) else ref, color=color or self.tk["accent"])
        return f'<img class="{cls}" src="{uri(p)}">' if p else ""

    def block(self, b):
        t = b["type"]
        fn = getattr(self, f"b_{t}", None)
        return fn(b) if fn else ""

    def b_heading(self, b):
        lvl = min(int(b.get("_level", b.get("level", 1))) + 1, 4)
        num = f'<span class="num">{esc(b["_num"])}</span>' if b.get("_num") else ""
        rule = ' class="rule"' if lvl == 2 and self.d.spec.get("heading_rule", True) else ""
        return f'<h{lvl} id="{b.get("_id", "")}"{rule}>{num}{esc(b.get("text", ""))}</h{lvl}>'

    def b_section(self, b):
        img = f'<img src="{uri(self.d.asset(b["image"], size=(1800, 800)))}">' if b.get("image") else ""
        sn = b.get("number") or b.get("_num") or ""
        chap = " chapter" if self.d.preset.get("chapters") else ""
        intro = f'<p class="intro">{md(b["intro"])}</p>' if b.get("intro") else ""
        num = f'<span class="num" style="display:none">{esc(b["_num"])}</span>' if b.get("_num") else ""
        return f'<div class="sec{chap}"><div class="sn">{esc(sn)}</div><h1 id="{b.get("_id", "")}">{num}{esc(b.get("title", b.get("text", "")))}</h1>{intro}{img}</div>'

    def b_paragraph(self, b):
        cls = ' class="lead"' if b.get("style") == "lead" else ""
        return f"<p{cls}>{md(b.get('text', ''))}</p>"

    def b_bullets(self, b, ordered=False):
        tag = "ol" if ordered or b.get("style") == "number" else "ul"
        items = []
        for it in b.get("items", []):
            if isinstance(it, dict):
                items.append(f"<li><strong>{md(it.get('point', it.get('title', '')))}</strong>"
                             f"{(' — ' + md(it['detail'])) if it.get('detail') else ''}</li>")
            else:
                items.append(f"<li>{md(it)}</li>")
        return f'<{tag} class="b">{"".join(items)}</{tag}>'

    def b_numbered(self, b):
        return self.b_bullets(b, True)

    def b_checklist(self, b):
        items = "".join(f'<li class="{"done" if isinstance(i, dict) and i.get("done") else ""}">{md(i.get("text", "") if isinstance(i, dict) else i)}</li>'
                        for i in b.get("items", []))
        return f'<ul class="check">{items}</ul>'

    ICONS = {"info": "material-symbols:info-outline", "tip": "material-symbols:lightbulb-outline",
             "warning": "material-symbols:warning-outline", "success": "material-symbols:check-circle-outline",
             "note": "material-symbols:sticky-note-2-outline", "example": "material-symbols:science-outline"}

    def b_callout(self, b):
        kind = b.get("kind", "info")
        col = {"warning": "B45309", "success": "1E7A46", "note": self.tk["ink_soft"]}.get(kind, self.tk["accent"])
        ic = self.icon(b.get("icon") or self.ICONS.get(kind, self.ICONS["info"]), col)
        title = b.get("title") or self.d.label(kind)
        return f'<div class="callout {kind}">{ic}<div><div class="ct">{esc(title)}</div>{self.blocks(b["blocks"]) if b.get("blocks") else "<p>" + md(b.get("text", "")) + "</p>"}</div></div>'

    def b_quote(self, b):
        cite = f"<cite>— {esc(b['author'])}</cite>" if b.get("author") else ""
        return f"<blockquote>{md(b.get('text', ''))}{cite}</blockquote>"

    def b_pull_quote(self, b):
        return f'<div class="pull">{md(b.get("text", ""))}</div>'

    def b_table(self, b):
        self.tab += 1
        heads = b.get("headers", [])
        numcols = set(b.get("numeric", []))
        if not numcols and b.get("rows"):
            for j in range(len(heads)):
                col = [str(r[j]) for r in b["rows"] if j < len(r)]
                if col and all(re.fullmatch(r"[\s$€£%+\-−.,0-9٠-٩EGPج.م]*", c) and re.search(r"[0-9٠-٩]", c) for c in col):
                    numcols.add(j)
        th = "".join(f'<th class="{"num" if j in numcols else ""}">{md(h)}</th>' for j, h in enumerate(heads))
        rows = ""
        for i, r in enumerate(b.get("rows", [])):
            cls = ' class="total"' if b.get("total_row") and i == len(b["rows"]) - 1 else ""
            rows += f"<tr{cls}>" + "".join(f'<td class="{"num" if j in numcols else ""}">{md(c)}</td>' for j, c in enumerate(r)) + "</tr>"
        cap = f'<div class="cap"><b>{esc(self.d.label("table"))} {self.tab}.</b> {md(b["caption"])}</div>' if b.get("caption") else ""
        widths = "".join(f'<col style="width:{w}%">' for w in b.get("widths", []))
        return f'<table class="t {b.get("style", "")}"><colgroup>{widths}</colgroup><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table>{cap}'

    def b_image(self, b):
        size = b.get("width", "full")
        p = self.d.asset(b.get("image"), size=(1800, 1000) if size == "full" else (1000, 800))
        if not p:
            return ""
        self.fig += 1
        cap = f'<figcaption class="cap"><b>{esc(self.d.label("figure"))} {self.fig}.</b> {md(b["caption"])}</figcaption>' if b.get("caption") else ""
        cls = size + (" float" if b.get("float") else "")
        style = f' style="height:{b["height_mm"]}mm;object-fit:cover"' if b.get("height_mm") else ""
        return f'<figure class="{cls}"><img src="{uri(p)}"{style}>{cap}</figure>'

    def b_chart(self, b):
        spec = dict(b.get("chart", b))
        spec.pop("type", None) if spec.get("type") == "chart" else None
        if "chart" in b and isinstance(b["chart"], dict):
            spec = dict(b["chart"])
        spec.setdefault("type", "bar")
        p = self.d.asset({"chart": spec, "width_in": 7.0, "height_in": float(b.get("height_in", 3.4))})
        self.fig += 1
        cap = f'<figcaption class="cap"><b>{esc(self.d.label("figure"))} {self.fig}.</b> {md(b["caption"])}</figcaption>' if b.get("caption") else ""
        return f'<figure><img src="{uri(p)}" style="border-radius:0">{cap}</figure>'

    def b_stats(self, b):
        return '<div class="stats">' + "".join(f'<div class="stat"><div class="v">{esc(s.get("value", ""))}</div><div class="l">{md(s.get("label", ""))}</div></div>'
                                               for s in b.get("items", [])) + "</div>"

    def b_timeline(self, b):
        return '<div class="tl">' + "".join(f'<div class="tl-i"><div class="tl-d">{esc(i.get("date", ""))}</div><div class="tl-t">{md(i.get("title", ""))}</div>'
                                            f'<div>{md(i.get("text", ""))}</div></div>' for i in b.get("items", [])) + "</div>"

    def b_steps(self, b):
        return '<div class="steps">' + "".join(f'<div class="step"><div class="n">{k + 1}</div><div><h4>{md(i.get("title", ""))}</h4><p>{md(i.get("text", ""))}</p></div></div>'
                                               for k, i in enumerate(b.get("items", []))) + "</div>"

    def b_two_column(self, b):
        r = {"1:2": "r12", "2:1": "r21"}.get(b.get("ratio", ""), "")
        return f'<div class="cols {r}"><div>{self.blocks(b.get("left"))}</div><div>{self.blocks(b.get("right"))}</div></div>'

    def b_cards(self, b):
        items = b.get("items", [])
        cols = b.get("cols") or (2 if len(items) in (2, 4) else 3)
        return f'<div class="cards c{cols}">' + "".join(
            f'<div class="card">{self.icon(i.get("icon"))}<h4>{md(i.get("title", ""))}</h4><p>{md(i.get("text", ""))}</p></div>' for i in items) + "</div>"

    def b_definition(self, b):
        ex = f'<p><em class="hl">{esc(self.d.label("example"))}:</em> {md(b["example"])}</p>' if b.get("example") else ""
        return f'<div class="def"><div class="kt">{esc(self.d.label("key_term"))}</div><div class="term">{esc(b.get("term", ""))}</div><p>{md(b.get("text", ""))}</p>{ex}</div>'

    def b_code(self, b):
        try:
            from pygments import highlight
            from pygments.formatters import HtmlFormatter
            from pygments.lexers import get_lexer_by_name, guess_lexer
            lx = get_lexer_by_name(b["lang"]) if b.get("lang") else guess_lexer(b.get("code", ""))
            code = highlight(b.get("code", ""), lx, HtmlFormatter(nowrap=True))
        except Exception:
            code = esc(b.get("code", ""))
        cap = f'<div class="cap">{md(b["caption"])}</div>' if b.get("caption") else ""
        return f'<pre class="code">{code}</pre>{cap}'

    def b_kv(self, b):
        return '<dl class="kv">' + "".join(f"<dt>{esc(k)}</dt><dd>{md(v)}</dd>" for k, v in b.get("items", [])) + "</dl>"

    def b_signature(self, b):
        return '<div class="sig">' + "".join(f'<div><div class="line"></div><div class="nm">{esc(p.get("name", ""))}</div><div class="rl">{esc(p.get("role", ""))}'
                                             f'{(" · " + esc(self.d.label("date")) + ": ____") if p.get("date_line", True) else ""}</div></div>'
                                             for p in b.get("parties", [])) + "</div>"

    def b_page_break(self, b):
        return '<div style="break-after:page"></div>'

    def b_divider(self, b):
        return '<hr class="div">'

    def b_spacer(self, b):
        return f'<div style="height:{float(b.get("mm", 8))}mm"></div>'

    def b_toc(self, b):
        return self.toc_page()

    def b_box(self, b):
        h = f"<h4>{md(b['title'])}</h4>" if b.get("title") else ""
        return f'<div class="box">{h}{self.blocks(b.get("blocks"))}</div>'

    def b_gallery(self, b):
        return '<div class="gallery">' + "".join(
            f'<figure style="margin:0"><img src="{uri(self.d.asset(i.get("image"), size=(1000, 750)))}"><figcaption>{md(i.get("caption", ""))}</figcaption></figure>'
            for i in b.get("items", [])) + "</div>"

    def b_note_lines(self, b):
        return '<div class="lines">' + "<div></div>" * int(b.get("lines", 5)) + "</div>"

    def b_schedule(self, b):
        rows = "".join(f'<tr><td class="tm"><span dir="ltr">{esc(r.get("time", ""))}</span></td><td class="du"><span dir="ltr">{esc(r.get("duration", ""))}</span></td>'
                       f'<td><strong>{md(r.get("title", ""))}</strong>{("<br>" + md(r["text"])) if r.get("text") else ""}</td></tr>' for r in b.get("items", []))
        return f'<table class="sched">{rows}</table>'

    def b_rubric(self, b):
        levels = b.get("levels", [])
        th = f"<th>{esc(self.d.label('criteria'))}</th>" + "".join(f"<th>{esc(l)}</th>" for l in levels)
        rows = "".join("<tr><td><strong>" + md(c.get("name", "")) + "</strong>" + (f"<br><span class='cap'>{esc(c['weight'])}</span>" if c.get("weight") else "")
                       + "</td>" + "".join(f"<td>{md(x)}</td>" for x in c.get("descriptors", [])) + "</tr>" for c in b.get("criteria", []))
        return f'<table class="t"><thead><tr>{th}</tr></thead><tbody>{rows}</tbody></table>'

    def b_items(self, b):  # invoice / quotation items
        T = self.d.invoice_totals(b)
        cur = b.get("currency", self.d.spec.get("currency", ""))
        L = self.d.label
        rows = "".join(f'<tr><td><strong>{md(r[0])}</strong>{("<br><span class=cap>" + md(r[1]) + "</span>") if r[1] else ""}</td>'
                       f'<td class="num">{r[2]:g}</td><td class="num">{self.d.money(r[3], cur)}</td><td class="num">{self.d.money(r[4], cur)}</td></tr>' for r in T["rows"])
        tot = f'<div><span>{L("subtotal")}</span><span>{self.d.money(T["subtotal"], cur)}</span></div>'
        if T["discount"]:
            tot += f'<div><span>{L("discount")}</span><span>− {self.d.money(T["discount"], cur)}</span></div>'
        if T["tax_pct"]:
            tot += f'<div><span>{L("tax")} ({T["tax_pct"]:g}%)</span><span>{self.d.money(T["tax"], cur)}</span></div>'
        tot += f'<div class="grand"><span>{L("total")}</span><span>{self.d.money(T["total"], cur)}</span></div>'
        return (f'<table class="t"><thead><tr><th>{L("item")}</th><th class="num">{L("qty")}</th><th class="num">{L("price")}</th>'
                f'<th class="num">{L("amount")}</th></tr></thead><tbody>{rows}</tbody></table><div class="inv-tot">{tot}</div>')

    def b_questions(self, b):
        show = b.get("show_answers", self.d.type == "answer_key")
        letters = "أبجدهو" if self.d.rtl else "ABCDEF"
        out = []
        for k, q in enumerate(b.get("items", []), start=int(b.get("start", 1))):
            kind = q.get("kind", "mcq" if q.get("options") else "short")
            pts = f'<span class="pts">{q["points"]} {esc(self.d.label("points"))}</span>' if q.get("points") else ""
            body = ""
            if kind in ("mcq", "tf"):
                opts = q.get("options") or [self.d.label("true"), self.d.label("false")]
                ans = q.get("answer")
                body = '<ol class="opts">' + "".join(
                    f'<li class="{"right" if show and (ans == j or ans == o) else ""}"><span class="bx">{letters[j]}</span><span>{md(o)}</span></li>'
                    for j, o in enumerate(opts)) + "</ol>"
            elif kind in ("short", "essay", "fill", "code"):
                n = int(q.get("lines", 2 if kind == "short" else 6 if kind == "essay" else 1))
                if show and q.get("answer") is not None:
                    body = f'<div class="ans">✓ {md(q["answer"])}</div>'
                elif kind != "fill":
                    body = '<div class="alines lines">' + "<div></div>" * n + "</div>"
            if show and q.get("explanation"):
                body += f'<div class="ans" style="color:var(--ink2);font-weight:400">{md(q["explanation"])}</div>'
            out.append(f'<div class="q"><div class="qh"><span class="qn">{k}.</span><span>{md(q.get("q", ""))}</span>{pts}</div>{body}</div>')
        return f'<div class="qs">{"".join(out)}</div>'

    def b_experience(self, b):
        out = ""
        for x in b.get("items", []):
            dates = " – ".join(v for v in (x.get("from", ""), x.get("to", "")) if v)
            bl = "".join(f"<li>{md(i)}</li>" for i in x.get("bullets", []))
            out += (f'<div class="xp"><div class="hd"><span class="rl">{esc(x.get("role", x.get("degree", "")))}</span><span class="dt">{esc(dates)}</span></div>'
                    f'<div class="org">{esc(" · ".join(v for v in (x.get("org", x.get("school", "")), x.get("place", "")) if v))}</div>'
                    f'{("<ul>" + bl + "</ul>") if bl else ""}{("<p style=margin:2pt_0>" + md(x["text"]) + "</p>") if x.get("text") else ""}</div>')
        return out

    def b_education(self, b):
        return self.b_experience(b)

    def b_skills(self, b):
        return "".join(f"<p><strong>{esc(g.get('group', ''))}</strong> — {esc(', '.join(g.get('items', [])))}</p>" for g in b.get("groups", []))

    def b_contact(self, b):
        return self.b_kv({"items": b.get("items", [])})

    # ================================================================== special layouts
    def _org_head(self):
        d, m = self.d, self.d.meta
        logo = f'<img src="{uri(d.asset({"path": d.logo}) if d.logo else d.asset(m.get("logo")))}">' if (d.logo or m.get("logo")) else f'<div class="org">{esc(m.get("org", ""))}</div>'
        return f'<div class="lh">{logo}<div class="addr">{esc(m.get("org_address", ""))}</div></div>'

    def layout_letter(self):
        d, m = self.d, self.d.meta
        to = f'<div class="to">{esc(m.get("to", ""))}</div>' if m.get("to") else ""
        subj = f'<div class="subj">{esc(d.label("subject"))}: {esc(m.get("subject", ""))}</div>' if m.get("subject") else ""
        return (f'<main class="letter" style="page:plain">{self._org_head()}<div class="dt">{esc(m.get("date", ""))}</div>{to}{subj}'
                f'{self.blocks(d.blocks)}</main>')

    def layout_memo(self):
        d, m = self.d, self.d.meta
        rows = "".join(f"<b>{esc(d.label(k))}</b><span>{esc(m[k])}</span>" for k in ("to", "from", "cc", "date", "subject") if m.get(k))
        if d.type == "minutes" and m.get("attendees"):
            rows += f"<b>{esc(d.label('attendees'))}</b><span>{esc(', '.join(m['attendees']) if isinstance(m['attendees'], list) else m['attendees'])}</span>"
        head = esc(m.get("title") or ("مذكرة" if d.rtl else "Memo"))
        return f'<main>{self._org_head() if (d.logo or m.get("org")) else ""}<div class="memo-h">{head}</div><div class="memo-meta">{rows}</div>{self.blocks(d.blocks)}</main>'

    def layout_invoice(self):
        d, m = self.d, self.d.meta
        logo = f'<img src="{uri(d.asset({"path": d.logo}))}">' if d.logo else f'<div class="org" style="font:800 16pt var(--hf);color:var(--acc)">{esc(m.get("org", ""))}</div>'
        kind = d.label(d.type if d.type in ("invoice", "quotation", "receipt") else "invoice")
        num = f'<small>{esc(d.label("number"))} {esc(m.get("number", ""))}</small>' if m.get("number") else ""
        parties = (f'<div><h5>{esc(d.label("from"))}</h5><div>{esc(m.get("from", m.get("org", "")))}</div></div>'
                   f'<div><h5>{esc(d.label("bill_to"))}</h5><div>{esc(m.get("bill_to", ""))}</div></div>'
                   f'<div><h5>{esc(d.label("date"))}</h5><div>{esc(m.get("date", ""))}</div>'
                   + (f'<h5 style="margin-top:8pt">{esc(d.label("due"))}</h5><div>{esc(m["due"])}</div>' if m.get("due") else "") + "</div>")
        return f'<main style="page:plain"><div class="inv-top">{logo}<div class="inv-title">{esc(kind)}{num}</div></div><div class="inv-parties">{parties}</div>{self.blocks(d.blocks)}</main>'

    def layout_cv(self):
        d, m = self.d, self.d.meta
        side_blocks, main_blocks = [], []
        for b in d.blocks:
            (side_blocks if b.get("column") == "side" or b["type"] in ("contact", "skills") else main_blocks).append(b)
        photo = f'<img class="ph" src="{uri(d.asset(m["photo"]))}">' if m.get("photo") else ""
        side = photo
        for b in side_blocks:
            side += f"<h4>{esc(b.get('title') or d.label(b['type']))}</h4>"
            if b["type"] == "contact":
                side += "<ul>" + "".join(f"<li><b style='opacity:.7'>{esc(k)}</b><br>{esc(v)}</li>" for k, v in b.get("items", [])) + "</ul>"
            elif b["type"] == "skills":
                for g in b.get("groups", []):
                    if g.get("levels"):
                        side += "".join(f'<p style="margin:0">{esc(n)}</p><div class="bar"><i style="width:{int(l)}%"></i></div>' for n, l in zip(g["items"], g["levels"]))
                    else:
                        side += (f'<p style="margin:4pt 0 3pt;opacity:.8">{esc(g.get("group", ""))}</p>' if g.get("group") else "") + \
                                '<div class="chips">' + "".join(f"<span>{esc(i)}</span>" for i in g.get("items", [])) + "</div>"
            else:
                side += self.block(b)
        main = f'<div class="nm">{esc(m.get("title") or m.get("name", ""))}</div><div class="role">{esc(m.get("subtitle") or m.get("role", ""))}</div>'
        for b in main_blocks:
            if b["type"] in ("experience", "education") or b.get("title"):
                main += f"<h2>{esc(b.get('title') or d.label(b['type']))}</h2>"
            main += self.block(b)
        return f'<div class="cv"><aside class="side">{side}</aside><main class="main">{main}</main></div>'

    def layout_certificate(self):
        d, m = self.d, self.d.meta
        orn = d.asset({"art": "arcs", "dark": False, "seed": 2}, size=(600, 600))
        logo = f'<img class="logo" src="{uri(d.asset({"path": d.logo}))}">' if d.logo else ""
        sigs = "".join(f"<div><b>{esc(s.get('name', ''))}</b>{esc(s.get('role', ''))}</div>" for s in m.get("signatures", []))
        seal = f'<div class="seal">{esc(m.get("seal", ""))}</div>' if m.get("seal") else ""
        return (f'<section class="cert"><div class="frame"></div><div class="frame2"></div>'
                f'<img class="orn" src="{uri(orn)}" style="top:12mm;inset-inline-start:12mm"><img class="orn" src="{uri(orn)}" style="bottom:12mm;inset-inline-end:12mm;transform:rotate(180deg)">'
                f'{logo}<div class="k">{esc(m.get("org", ""))}</div><h1>{esc(m.get("title") or d.label("certificate_of"))}</h1>'
                f'<div class="pt">{esc(m.get("presented_to") or d.label("presented_to"))}</div><div class="who">{esc(m.get("recipient", ""))}</div>'
                f'<div class="why">{md(m.get("reason", ""))}</div><div class="pt" style="margin-top:8pt">{esc(m.get("date", ""))}</div>'
                f'<div class="sigs">{sigs}</div>{seal}</section>')

    def layout_handout(self):
        d, m = self.d, self.d.meta
        logo = f'<img src="{uri(d.asset({"path": d.logo}))}">' if d.logo else ""
        kick = esc(m.get("kicker") or m.get("course", ""))
        fields = ""
        if d.type in ("worksheet", "lab_sheet") or m.get("student_fields"):
            fields = (f'<div class="fields"><div>{esc(d.label("name"))}:</div><div>{esc(d.label("class"))}:</div>'
                      f'<div>{esc(d.label("date"))}:</div></div>')
        instr = f'<div class="instr">{md(m["instructions"])}</div>' if m.get("instructions") else ""
        return (f'<main><div class="hband"><div><div class="k">{kick}</div><h1>{esc(m.get("title", ""))}</h1></div>{logo}</div>'
                f'{fields}{instr}{self.blocks(d.blocks)}</main>')

    def layout_exam(self):
        d, m = self.d, self.d.meta
        total = sum(float(q.get("points", 0)) for b in d.blocks if b["type"] == "questions" for q in b.get("items", []))
        logo = f'<img src="{uri(d.asset({"path": d.logo}))}">' if d.logo else ""
        info = " · ".join(v for v in (m.get("course", ""), (f'{esc(d.label("duration"))}: {m["duration"]}' if m.get("duration") else ""),
                                      (f'{d.label("score")}: ____ / {total:g}' if total else "")) if v)
        fields = "" if d.type == "answer_key" else (f'<div class="fields"><div>{esc(d.label("name"))}:</div><div>{esc(d.label("class"))}:</div>'
                                                    f'<div>{esc(d.label("date"))}:</div></div>')
        instr = f'<div class="instr">{md(m["instructions"])}</div>' if m.get("instructions") else ""
        return (f'<main><div class="hband"><div><div class="k">{esc(info)}</div><h1>{esc(m.get("title", ""))}</h1></div>{logo}</div>'
                f'{fields}{instr}{self.blocks(d.blocks)}</main>')

    def layout_flyer(self):
        d, m, c = self.d, self.d.meta, self.d.cover
        img = d.asset(c.get("image") or {"art": "mesh", "dark": True}, size=(1800, 1300))
        cta = m.get("cta", {})
        cta_html = f'<div class="cta"><div>{esc(cta.get("text", ""))}<small>{esc(cta.get("detail", ""))}</small></div><div>{esc(cta.get("contact", ""))}</div></div>' if cta else ""
        sub = f'<p style="color:#fff;opacity:.9;margin:6pt 0 0;font-size:12pt">{md(m["subtitle"])}</p>' if m.get("subtitle") else ""
        return (f'<section class="flyer"><div class="hero"><img src="{uri(img)}"><div class="shade"></div><div class="ct"><h1>{esc(m.get("title", ""))}</h1>{sub}</div></div>'
                f'<div class="body">{self.blocks(d.blocks)}</div>{cta_html}</section>')

    def layout_one_pager(self):
        return self.layout_flyer()
