"""Draw an automation as a professional diagram — from an n8n workflow JSON or a platform-neutral plan.

Outputs (pick with --formats): svg · png · pdf (Graphviz, print-quality) · html (interactive page: zoom,
click a node to see its type, parameters and notes; self-contained) · mmd (Mermaid source for docs,
GitHub, Notion) · excalidraw (open at excalidraw.com, edit freely; also imports into FigJam/Miro as image).

Plan format (design a flow before choosing a platform):
{"title": "Lead intake", "steps": [
   {"id": "in", "label": "New lead (form)", "kind": "trigger", "app": "Typeform"},
   {"id": "ok", "label": "Valid email?", "kind": "decision"},
   {"id": "crm", "label": "Create contact", "kind": "action", "app": "HubSpot"},
   {"id": "ai", "label": "Score lead", "kind": "ai"}, {"id": "err", "label": "Alert on failure", "kind": "error"}],
 "edges": [["in", "ok"], ["ok", "crm", "yes"], ["ok", "err", "no"]]}
kinds: trigger · action · decision · loop · transform · code · ai · ai_sub · wait · output · error · subflow · note
"""
from __future__ import annotations

import html
import json
import shutil
import subprocess
from pathlib import Path

STYLE = {  # fill, border, text
    "trigger": ("#E8F7EE", "#1E9E5A", "#0F3D24"), "action": ("#EEF0FF", "#4F46E5", "#1E1B4B"),
    "decision": ("#FFF6E5", "#D97706", "#4A2A00"), "loop": ("#FFF6E5", "#D97706", "#4A2A00"),
    "transform": ("#EAF4FF", "#2F6FED", "#0B2559"), "code": ("#F1F5F9", "#475569", "#0F172A"),
    "ai": ("#FCE8F3", "#C026D3", "#4A044E"), "ai_sub": ("#FDF4FF", "#D946EF", "#4A044E"),
    "wait": ("#F5F5F4", "#78716C", "#292524"), "output": ("#E6FFFA", "#0D9488", "#134E4A"),
    "error": ("#FEECEC", "#DC2626", "#450A0A"), "subflow": ("#EEF2FF", "#6366F1", "#1E1B4B"),
    "note": ("#FFFBEA", "#CA8A04", "#3F2E00"),
}
LOGIC = {"if", "switch", "filter", "compareDatasets"}
LOOP = {"splitInBatches", "loop"}
TRANSFORM = {"set", "splitOut", "aggregate", "merge", "itemLists", "sort", "limit", "removeDuplicates", "dateTime", "crypto",
             "xml", "html", "markdown", "renameKeys", "summarize", "extractFromFile", "convertToFile", "compression", "noOp", "editImage"}


def classify(n: dict) -> str:
    t = n.get("type", "")
    short = t.split(".")[-1]
    if t == "n8n-nodes-base.stickyNote":
        return "note"
    if short == "errorTrigger" or short == "stopAndError":
        return "error"
    if short.endswith("Trigger") or short in ("webhook", "cron", "interval"):
        return "trigger"
    if short in LOGIC:
        return "decision"
    if short in LOOP:
        return "loop"
    if short == "code" or short == "function" or short == "functionItem":
        return "code"
    if short in ("wait",):
        return "wait"
    if short in ("respondToWebhook",):
        return "output"
    if short in ("executeWorkflow",):
        return "subflow"
    if t.startswith("@n8n/n8n-nodes-langchain."):
        if short.startswith(("lmChat", "lm", "memory", "embeddings", "vectorStore", "textSplitter", "documentDefault",
                             "outputParser", "retriever", "reranker")) or short.startswith("tool"):
            return "ai_sub"
        return "ai"
    if short in TRANSFORM:
        return "transform"
    return "action"


def from_n8n(wf: dict) -> dict:
    nodes = [n for n in wf.get("nodes", [])]
    steps, edges = [], []
    by_name = {n["name"]: n for n in nodes}
    for n in nodes:
        if n.get("type") == "n8n-nodes-base.stickyNote":
            continue
        t = n.get("type", "")
        steps.append({"id": n["name"], "label": n["name"], "kind": classify(n),
                      "app": t.split(".")[-1], "type": t, "version": n.get("typeVersion"),
                      "params": n.get("parameters", {}), "position": n.get("position"), "disabled": n.get("disabled", False),
                      "notes": n.get("notes", ""), "credentials": list((n.get("credentials") or {}).keys())})
    for src, ports in (wf.get("connections") or {}).items():
        if src not in by_name:
            continue
        st = by_name[src].get("type", "").split(".")[-1]
        for ptype, outs in ports.items():
            for oi, targets in enumerate(outs or []):
                for t in targets or []:
                    label = ""
                    if ptype.startswith("ai_"):
                        label = ptype[3:].replace("languageModel", "model").replace("outputParser", "parser")
                    elif st == "if":
                        label = "true" if oi == 0 else "false"
                    elif st == "filter" and oi == 1:
                        label = "discarded"
                    elif st == "splitInBatches":
                        label = "done" if oi == 0 else "each batch"
                    elif st == "switch":
                        rules = (((by_name[src].get("parameters") or {}).get("rules") or {}).get("values") or [])
                        label = (rules[oi].get("outputKey") if oi < len(rules) and isinstance(rules[oi], dict) else None) or f"case {oi}"
                    elif len(outs) > 1:
                        label = f"out {oi}"
                    edges.append([src, t["node"], label, "ai" if ptype.startswith("ai_") else "main"])
    for n in nodes:
        if n.get("type") == "n8n-nodes-base.stickyNote":
            txt = (n.get("parameters") or {}).get("content", "")
            if txt.strip():
                steps.append({"id": n["name"], "label": txt.strip().splitlines()[0].lstrip("# ")[:60], "kind": "note",
                              "params": {"content": txt}, "position": n.get("position")})
    return {"title": wf.get("name", "Workflow"), "steps": steps, "edges": edges}


def _dot(plan: dict) -> str:
    q = lambda s: '"' + str(s).replace('"', '\\"') + '"'
    lines = [f"digraph G {{", 'graph [rankdir=LR, splines=spline, nodesep=0.45, ranksep=0.7, pad=0.4, bgcolor="white",',
             f'  fontname="Helvetica", labelloc=t, fontsize=20, label=<<b>{html.escape(plan.get("title", ""))}</b>>];',
             'node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=12, penwidth=1.6, margin="0.18,0.10"];',
             'edge [fontname="Helvetica", fontsize=10, color="#64748B", arrowsize=0.8, penwidth=1.3];']
    for s in plan["steps"]:
        fill, border, text = STYLE.get(s.get("kind", "action"), STYLE["action"])
        shape = {"decision": "diamond", "loop": "box", "note": "note"}.get(s["kind"], "box")
        sub = s.get("app") or s.get("kind")
        if s.get("type"):
            sub = s["type"].split(".")[-1]
        lab = f'<<b>{html.escape(s["label"])}</b><br/><font point-size="9" color="{border}">{html.escape(str(sub))}</font>>'
        extra = ', style="rounded,filled,dashed"' if s.get("disabled") or s["kind"] == "ai_sub" else ""
        if shape == "diamond":
            extra += ', margin="0.05,0.05"'
        lines.append(f'{q(s["id"])} [label={lab}, shape={shape}, fillcolor="{fill}", color="{border}", fontcolor="{text}"{extra}];')
    for e in plan["edges"]:
        src, dst = e[0], e[1]
        label = e[2] if len(e) > 2 else ""
        kind = e[3] if len(e) > 3 else "main"
        attrs = []
        if label:
            col = {"true": "#1E9E5A", "yes": "#1E9E5A", "false": "#DC2626", "no": "#DC2626", "error": "#DC2626"}.get(str(label).lower(), "#475569")
            attrs.append(f'label=<<font color="{col}"><b>{html.escape(str(label))}</b></font>>')
        if kind == "ai":
            attrs += ['style=dashed', 'color="#D946EF"', 'arrowhead=odiamond']
        lines.append(f'{q(src)} -> {q(dst)} [{", ".join(attrs)}];')
    lines.append("}")
    return "\n".join(lines)


def _mermaid(plan: dict) -> str:
    ids = {s["id"]: f"n{i}" for i, s in enumerate(plan["steps"])}
    out = ["flowchart LR"]
    for s in plan["steps"]:
        lab = s["label"].replace('"', "'")
        k = s.get("kind")
        shape = {"decision": ('{"', '"}'), "trigger": ('(["', '"])'), "output": ('[/"', '"/]'), "subflow": ('[["', '"]]'),
                 "ai": ('{{"', '"}}'), "error": ('>"', '"]'), "note": ('>"', '"]')}.get(k, ('["', '"]'))
        out.append(f'  {ids[s["id"]]}{shape[0]}{lab}{shape[1]}')
    for e in plan["edges"]:
        if e[0] not in ids or e[1] not in ids:
            continue
        arrow = "-.->" if (len(e) > 3 and e[3] == "ai") else "-->"
        lab = f"|{e[2]}|" if len(e) > 2 and e[2] else ""
        a, b = (ids[e[0]], ids[e[1]])
        out.append(f"  {a} {arrow}{lab} {b}")
    for k, (fill, border, text) in STYLE.items():
        out.append(f"  classDef {k} fill:{fill},stroke:{border},color:{text},stroke-width:1.5px")
    for s in plan["steps"]:
        out.append(f"  class {ids[s['id']]} {s.get('kind', 'action')}")
    return "\n".join(out)


def _excalidraw(plan: dict) -> dict:
    els, pos = [], {}
    xs = [s.get("position") for s in plan["steps"] if s.get("position")]
    for i, s in enumerate(plan["steps"]):
        p = s.get("position") or [i * 260, 0]
        x, y = p[0] * 1.0, p[1] * 1.0
        w, h = 200, 70
        fill, border, _ = STYLE.get(s.get("kind", "action"), STYLE["action"])
        rid, tid = f"r{i}", f"t{i}"
        pos[s["id"]] = (x, y, w, h, rid)
        els.append({"id": rid, "type": "diamond" if s.get("kind") == "decision" else "rectangle", "x": x, "y": y, "width": w, "height": h,
                    "angle": 0, "strokeColor": border, "backgroundColor": fill, "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
                    "roughness": 0, "opacity": 100, "roundness": {"type": 3}, "seed": i + 1, "version": 1, "isDeleted": False,
                    "boundElements": [{"type": "text", "id": tid}], "groupIds": [], "frameId": None, "link": None, "locked": False})
        els.append({"id": tid, "type": "text", "x": x + 10, "y": y + 22, "width": w - 20, "height": 25, "angle": 0, "strokeColor": "#1e1e1e",
                    "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid", "roughness": 0,
                    "opacity": 100, "seed": 1000 + i, "version": 1, "isDeleted": False, "text": s["label"][:40], "fontSize": 16,
                    "fontFamily": 2, "textAlign": "center", "verticalAlign": "middle", "containerId": rid, "originalText": s["label"][:40],
                    "lineHeight": 1.25, "boundElements": None, "groupIds": [], "frameId": None, "link": None, "locked": False})
    for j, e in enumerate(plan["edges"]):
        if e[0] not in pos or e[1] not in pos:
            continue
        x1, y1, w1, h1, r1 = pos[e[0]]
        x2, y2, w2, h2, r2 = pos[e[1]]
        sx, sy = x1 + w1, y1 + h1 / 2
        ex, ey = x2, y2 + h2 / 2
        els.append({"id": f"a{j}", "type": "arrow", "x": sx, "y": sy, "width": ex - sx, "height": ey - sy, "angle": 0,
                    "strokeColor": "#D946EF" if len(e) > 3 and e[3] == "ai" else "#64748b", "backgroundColor": "transparent",
                    "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "dashed" if len(e) > 3 and e[3] == "ai" else "solid",
                    "roughness": 0, "opacity": 100, "seed": 5000 + j, "version": 1, "isDeleted": False,
                    "points": [[0, 0], [ex - sx, ey - sy]], "startBinding": {"elementId": r1, "focus": 0, "gap": 4},
                    "endBinding": {"elementId": r2, "focus": 0, "gap": 4}, "startArrowhead": None, "endArrowhead": "arrow",
                    "boundElements": None, "groupIds": [], "frameId": None, "link": None, "locked": False})
        if len(e) > 2 and e[2]:
            els.append({"id": f"l{j}", "type": "text", "x": (sx + ex) / 2 - 30, "y": (sy + ey) / 2 - 22, "width": 60, "height": 18,
                        "angle": 0, "strokeColor": "#475569", "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 1,
                        "strokeStyle": "solid", "roughness": 0, "opacity": 100, "seed": 8000 + j, "version": 1, "isDeleted": False,
                        "text": str(e[2]), "fontSize": 13, "fontFamily": 2, "textAlign": "center", "verticalAlign": "top",
                        "containerId": None, "originalText": str(e[2]), "lineHeight": 1.25, "boundElements": None, "groupIds": [],
                        "frameId": None, "link": None, "locked": False})
    return {"type": "excalidraw", "version": 2, "source": "automation-studio", "elements": els,
            "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None}, "files": {}}


def _html(plan: dict, svg: str | None, mmd: str) -> str:
    data = {s["id"]: {k: s.get(k) for k in ("label", "kind", "type", "version", "params", "notes", "credentials")} for s in plan["steps"]}
    legend = "".join(f'<span class="lg" style="background:{f};border-color:{b};color:{t}">{k.replace("_", " ")}</span>'
                     for k, (f, b, t) in STYLE.items() if any(s.get("kind") == k for s in plan["steps"]))
    body = svg if svg else f'<pre class="mermaid">{html.escape(mmd)}</pre>'
    mermaid_js = "" if svg else '<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script><script>mermaid.initialize({startOnLoad:true});</script>'
    return f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(plan.get('title', 'Workflow'))}</title><style>
body{{margin:0;font:14px/1.5 -apple-system,Helvetica,Arial,sans-serif;color:#0f172a;background:#f8fafc;display:grid;grid-template-columns:1fr 360px;height:100vh}}
#canvas{{overflow:auto;padding:16px;background:white;border-right:1px solid #e2e8f0}} #canvas svg{{max-width:none;height:auto}}
#side{{padding:18px;overflow:auto}} h1{{font-size:18px;margin:0 0 8px}} .lg{{display:inline-block;border:1.5px solid;border-radius:8px;padding:1px 8px;margin:2px;font-size:12px}}
pre{{white-space:pre-wrap;word-break:break-word;background:#f1f5f9;padding:10px;border-radius:8px;font-size:12px}} .muted{{color:#64748b}}
g.node{{cursor:pointer}} g.node:hover path,g.node:hover polygon{{stroke-width:3}}
@media (max-width:900px){{body{{grid-template-columns:1fr;height:auto}} #side{{border-top:1px solid #e2e8f0}}}}
</style></head><body><div id="canvas">{body}</div><div id="side"><h1>{html.escape(plan.get('title', ''))}</h1>
<div>{legend}</div><p class="muted">Click a step to see its settings.</p><div id="info"></div></div>{mermaid_js}
<script>const D={json.dumps(data, ensure_ascii=False)};
document.querySelectorAll('g.node').forEach(g=>{{g.addEventListener('click',()=>{{const id=g.querySelector('title').textContent;const d=D[id]||{{}};
document.getElementById('info').innerHTML='<h3>'+(d.label||id)+'</h3><p class=muted>'+(d.type||d.kind||'')+(d.version?' v'+d.version:'')+'</p>'+
(d.credentials&&d.credentials.length?'<p><b>Credentials:</b> '+d.credentials.join(', ')+'</p>':'')+(d.notes?'<p>'+d.notes+'</p>':'')+
'<pre>'+JSON.stringify(d.params||{{}},null,2).replace(/</g,'&lt;')+'</pre>';}});}});
</script></body></html>"""


def render(src: dict, outdir: Path, formats=("svg", "png", "pdf", "html", "mmd", "excalidraw"), title=None) -> list[str]:
    plan = from_n8n(src) if "nodes" in src else src
    if title:
        plan["title"] = title
    outdir.mkdir(parents=True, exist_ok=True)
    import re
    stem = re.sub(r"[^\w\-]+", "_", (plan.get("title") or "workflow").strip(), flags=re.ASCII).strip("_")[:60] or "workflow"
    files = []
    dot = _dot(plan)
    mmd = _mermaid(plan)
    (outdir / f"{stem}.dot").write_text(dot)
    svg_text = None
    has_dot = shutil.which("dot")
    for f in formats:
        f = f.strip()
        if f in ("svg", "png", "pdf"):
            if not has_dot:
                continue
            out = outdir / f"{stem}.{f}"
            args = ["dot", f"-T{f}", "-o", str(out)]
            if f == "png":
                args.insert(1, "-Gdpi=170")
            subprocess.run(args, input=dot, text=True, check=True)
            files.append(str(out))
        elif f == "mmd":
            (outdir / f"{stem}.mmd").write_text(mmd)
            files.append(str(outdir / f"{stem}.mmd"))
        elif f == "excalidraw":
            (outdir / f"{stem}.excalidraw").write_text(json.dumps(_excalidraw(plan)))
            files.append(str(outdir / f"{stem}.excalidraw"))
    if "html" in formats:
        if has_dot:
            svg_text = subprocess.run(["dot", "-Tsvg"], input=dot, text=True, capture_output=True).stdout
            svg_text = svg_text[svg_text.find("<svg"):]
        (outdir / f"{stem}.html").write_text(_html(plan, svg_text, mmd), encoding="utf-8")
        files.append(str(outdir / f"{stem}.html"))
    if not has_dot and any(f in formats for f in ("svg", "png", "pdf")):
        files.append("(svg/png/pdf skipped — Graphviz not installed: brew install graphviz; the HTML uses Mermaid instead)")
    return files
