"""Port an n8n workflow to other automation platforms.

node-red      flows.json that RUNS (tested by `autokit test-nodered`): every n8n core node becomes a
              Node-RED function node running a small n8n-compatible runtime (items, $json, $('Node'),
              expressions, IF/Switch/Filter conditions, Set, Code, Split Out, Aggregate, Merge),
              Webhook → http in, Respond to Webhook → http response, HTTP Request → http request,
              Schedule → inject. App nodes become clearly marked TODO pass-through nodes.
make          Make.com scenario blueprint (import: Scenarios → ⋯ → Import Blueprint) — core modules
              (Webhooks, HTTP, Router + filters, Set variables, Iterator, Aggregator, Sleep, Webhook
              response); app modules become named placeholders to swap in Make — plus MAKE_GUIDE.md.
zapier / power-automate / pipedream / activepieces
              a step-by-step build guide (trigger, each action with field mappings, filters/paths,
              code steps ready to paste) — these platforms have no reliable import format.
"""
from __future__ import annotations

import json
import re
import uuid
from pathlib import Path

# ----------------------------------------------------------------------------------------- helpers
def _order(wf):
    """Nodes in execution order (BFS from triggers, then the rest)."""
    nodes = {n["name"]: n for n in wf.get("nodes", []) if n.get("type") != "n8n-nodes-base.stickyNote"}
    conns = wf.get("connections", {})
    indeg = {k: 0 for k in nodes}
    for s, ports in conns.items():
        for outs in (ports.get("main") or []):
            for t in outs or []:
                if t["node"] in indeg:
                    indeg[t["node"]] += 1
    q = [k for k, d in indeg.items() if d == 0]
    seen, out = set(), []
    while q:
        k = q.pop(0)
        if k in seen or k not in nodes:
            continue
        seen.add(k)
        out.append(nodes[k])
        for outs in (conns.get(k, {}).get("main") or []):
            for t in outs or []:
                q.append(t["node"])
    out += [n for k, n in nodes.items() if k not in seen]
    return out


def _main_outs(wf, name):
    return (wf.get("connections", {}).get(name, {}).get("main")) or []


def _short(t):
    return t.split(".")[-1]


# ----------------------------------------------------------------------------------------- Node-RED
RUNTIME = r"""
// ---- n8n-compatible runtime (automation-studio) ----
const N = msg._nodes = msg._nodes || {};
const items = Array.isArray(msg.items) ? msg.items : [{ json: (typeof msg.payload === 'object' && msg.payload) || { value: msg.payload } }];
const DT = (d) => ({ toISO: () => d.toISOString(), toISODate: () => d.toISOString().slice(0, 10), toMillis: () => d.getTime(),
  toFormat: (f) => d.toISOString(), plus: (o) => DT(new Date(d.getTime() + ((o.days||0)*864e5 + (o.hours||0)*36e5 + (o.minutes||0)*6e4))),
  minus: (o) => DT(new Date(d.getTime() - ((o.days||0)*864e5 + (o.hours||0)*36e5 + (o.minutes||0)*6e4))), toString: () => d.toISOString() });
const $now = DT(new Date());
const $today = DT(new Date(new Date().toISOString().slice(0, 10)));
function $(name) { const its = N[name] || []; return { item: its[0] || { json: {} }, first: () => its[0] || { json: {} },
  last: () => its[its.length - 1] || { json: {} }, all: () => its }; }
function evalExpr(v, item, i) {
  if (typeof v !== 'string' || !v.startsWith('=')) return v;
  const src = v.slice(1);
  const run = (code) => new Function('$json', '$', '$now', '$today', '$input', '$itemIndex', 'return (' + code + ');')(
      item.json, $, $now, $today, { item, all: () => items, first: () => items[0] }, i);
  const whole = src.match(/^\s*\{\{([\s\S]*)\}\}\s*$/);
  if (whole && whole[1].indexOf('}}') < 0) return run(whole[1]);
  return src.replace(/\{\{([\s\S]*?)\}\}/g, (_, c) => { const r = run(c); return typeof r === 'object' ? JSON.stringify(r) : String(r); });
}
function cond(c, item, i) {
  const l = evalExpr(c.leftValue, item, i), r = evalExpr(c.rightValue, item, i), op = (c.operator || {}).operation, ty = (c.operator || {}).type;
  const s = (x) => (x === undefined || x === null) ? '' : String(x);
  switch (op) {
    case 'exists': return l !== undefined && l !== null; case 'notExists': return l === undefined || l === null;
    case 'empty': return l === undefined || l === null || l === '' || (Array.isArray(l) && !l.length) || (typeof l === 'object' && !Object.keys(l).length);
    case 'notEmpty': return !(l === undefined || l === null || l === '' || (Array.isArray(l) && !l.length) || (ty === 'object' && typeof l === 'object' && !Object.keys(l).length));
    case 'equals': return ty === 'number' ? Number(l) === Number(r) : (ty === 'string' ? s(l) === s(r) : l == r);
    case 'notEquals': return ty === 'number' ? Number(l) !== Number(r) : s(l) !== s(r);
    case 'contains': return Array.isArray(l) ? l.includes(r) : s(l).includes(s(r)); case 'notContains': return !(Array.isArray(l) ? l.includes(r) : s(l).includes(s(r)));
    case 'startsWith': return s(l).startsWith(s(r)); case 'endsWith': return s(l).endsWith(s(r));
    case 'regex': return new RegExp(s(r)).test(s(l)); case 'notRegex': return !new RegExp(s(r)).test(s(l));
    case 'gt': return Number(l) > Number(r); case 'lt': return Number(l) < Number(r); case 'gte': return Number(l) >= Number(r); case 'lte': return Number(l) <= Number(r);
    case 'true': return l === true; case 'false': return l === false;
    case 'after': return new Date(l) > new Date(r); case 'before': return new Date(l) < new Date(r);
    case 'lengthEquals': return (l || []).length === Number(r); case 'lengthGt': return (l || []).length > Number(r); case 'lengthLt': return (l || []).length < Number(r);
    default: node.warn('unsupported operator ' + op); return false;
  }
}
function filterOk(f, item, i) { const cs = (f && f.conditions) || []; const res = cs.map(c => cond(c, item, i)); return (f && f.combinator) === 'or' ? res.some(Boolean) : res.every(Boolean); }
function emit(name, outs) { // outs: array (per output) of item arrays
  const res = outs.map(its => { if (!its || !its.length) return null; N[name] = its; return Object.assign({}, msg, { items: its, payload: its.length === 1 ? its[0].json : its.map(x => x.json), _nodes: Object.assign({}, N) }); });
  return res.length === 1 ? res[0] : res;
}
"""


def _nr_body(n):
    t, p, nm = _short(n["type"]), n.get("parameters") or {}, n["name"]
    js = json.dumps
    if t == "set":
        assigns = ((p.get("assignments") or {}).get("assignments")) or []
        keep = p.get("includeOtherFields", False)
        return (f"const A = {js(assigns)};\nconst out = items.map((it, i) => {{ const j = {'Object.assign({}, it.json)' if keep else '{}'}; "
                "for (const a of A) { let v = evalExpr(a.value, it, i); if (a.type === 'number') v = Number(v); if (a.type === 'boolean') v = (v === true || v === 'true'); "
                "if ((a.type === 'object' || a.type === 'array') && typeof v === 'string') { try { v = JSON.parse(v); } catch (e) {} } "
                "const path = a.name.split('.'); let o = j; while (path.length > 1) { const k = path.shift(); o = o[k] = o[k] || {}; } o[path[0]] = v; } "
                "return { json: j }; });\nreturn emit(" + js(nm) + ", [out]);"), 1
    if t in ("if", "filter"):
        cond_p = p.get("conditions") or {}
        if t == "if":
            return (f"const F = {js(cond_p)};\nconst yes = [], no = [];\nitems.forEach((it, i) => (filterOk(F, it, i) ? yes : no).push(it));\n"
                    f"return emit({js(nm)}, [yes, no]);"), 2
        return (f"const F = {js(cond_p)};\nconst yes = items.filter((it, i) => filterOk(F, it, i));\nreturn emit({js(nm)}, [yes]);"), 1
    if t == "switch":
        rules = ((p.get("rules") or {}).get("values")) or []
        fb = (p.get("options") or {}).get("fallbackOutput")
        n_out = len(rules) + (1 if fb == "extra" else 0)
        return (f"const R = {js([r.get('conditions') for r in rules])};\nconst outs = Array.from({{length: {n_out}}}, () => []);\n"
                f"items.forEach((it, i) => {{ const k = R.findIndex(f => filterOk(f, it, i)); if (k >= 0) outs[k].push(it); "
                f"else if ({str(fb == 'extra').lower()}) outs[{len(rules)}].push(it); }});\nreturn emit({js(nm)}, outs);"), max(n_out, 1)
    if t == "code":
        code = p.get("jsCode", "return $input.all();")
        each = p.get("mode") == "runOnceForEachItem"
        if each:
            return ("const out = [];\nfor (let i = 0; i < items.length; i++) { const $input = { item: items[i] }; const $json = items[i].json;\n"
                    f"  const r = await (async () => {{\n{code}\n}})();\n  if (r) out.push(r.json ? r : {{ json: r }});\n}}\nreturn emit({js(nm)}, [out]);"), 1
        return ("const $input = { all: () => items, first: () => items[0], last: () => items[items.length - 1], item: items[0] };\n"
                "const $json = (items[0] || {}).json;\n"
                f"let r = await (async () => {{\n{code}\n}})();\nif (!Array.isArray(r)) r = [r];\nr = r.map(x => (x && x.json) ? x : {{ json: x }});\n"
                f"return emit({js(nm)}, [r]);"), 1
    if t == "splitOut":
        f = p.get("fieldToSplitOut", "")
        return (f"const out = [];\nitems.forEach(it => {{ const v = {f!r}.split('.').reduce((o, k) => o && o[k], it.json); "
                "(Array.isArray(v) ? v : [v]).forEach(x => out.push({ json: (typeof x === 'object' && x) ? x : { " + js(f.split('.')[-1] or 'value') + ": x } })); });\n"
                f"return emit({js(nm)}, [out]);"), 1
    if t == "aggregate":
        return (f"return emit({js(nm)}, [[{{ json: {{ data: items.map(x => x.json) }} }}]]);"), 1
    if t == "removeDuplicates":
        across = p.get("operation") == "removeItemsSeenInPreviousExecutions"
        key = p.get("dedupeValue") or "={{ JSON.stringify($json) }}"
        return (f"const across = {str(across).lower()};\nconst store = {js('seen_' + re.sub(r'[^A-Za-z0-9_]', '_', nm))};\nconst seen = new Set(across ? (flow.get(store) || []) : []);\n"
                "const kept = [], dropped = [], now = new Set();\n"
                f"items.forEach((it, i) => {{ const k = String(evalExpr({js(key)}, it, i)); if (seen.has(k) || (!across && now.has(k))) dropped.push(it); else {{ kept.push(it); now.add(k); }} }});\n"
                "if (across) { const all = [...seen, ...now]; flow.set(store, all.slice(-" + str(int((p.get('options') or {}).get('historySize', 10000))) + ")); }\n"
                f"return emit({js(nm)}, across ? [kept, dropped] : [kept]);"), (2 if across else 1)
    if t == "splitInBatches":
        return (f"// Node-RED runs the loop body once with ALL items (no batching); add a 'delay' node in rate-limit mode\n"
                f"// inside the loop if the API needs pacing. Output 0 = done, output 1 = loop.\nreturn emit({js(nm)}, [items, items]);"), 2
    if t in ("noOp", "merge", "limit", "sort"):
        if t == "limit":
            return f"return emit({js(nm)}, [items.slice(0, {int(p.get('maxItems', 1))})]);", 1
        return f"return emit({js(nm)}, [items]);", 1
    if t == "respondToWebhook":
        kind = p.get("respondWith", "firstIncomingItem")
        status = (p.get("options") or {}).get("responseCode", 200)
        body = p.get("responseBody", "") if kind in ("json", "text") else None
        return (f"const it = items[0] || {{ json: {{}} }};\nlet body = {js(body)} !== null ? evalExpr({js(body)}, it, 0) : "
                f"({js(kind)} === 'allIncomingItems' ? items.map(x => x.json) : it.json);\nif ({js(kind)} === 'json' && typeof body === 'string') {{ try {{ body = JSON.parse(body); }} catch (e) {{}} }}\n"
                f"N[{js(nm)}] = items; msg.statusCode = {int(status)}; msg.payload = body; return msg;"), 1
    if t == "httpRequest":
        hdrs = (p.get("headerParameters") or {}).get("parameters") or []
        qs = (p.get("queryParameters") or {}).get("parameters") or []
        bodyp = (p.get("bodyParameters") or {}).get("parameters") or []
        return (f"const it = items[0] || {{ json: {{}} }};\nmsg.method = {js(p.get('method', 'GET'))};\nlet url = evalExpr({js(p.get('url', ''))}, it, 0);\n"
                f"const qs = {js(qs)}.map(q => encodeURIComponent(q.name) + '=' + encodeURIComponent(evalExpr(q.value, it, 0))).join('&');\n"
                "msg.url = qs ? url + (url.includes('?') ? '&' : '?') + qs : url;\n"
                f"msg.headers = Object.fromEntries({js(hdrs)}.map(h => [h.name, evalExpr(h.value, it, 0)]));\n"
                f"const B = {js(bodyp)}; if (B.length) {{ msg.payload = Object.fromEntries(B.map(b => [b.name, evalExpr(b.value, it, 0)])); msg.headers['content-type'] = 'application/json'; }}\n"
                f"else if ({js(p.get('jsonBody'))}) {{ msg.payload = evalExpr({js(p.get('jsonBody'))}, it, 0); }} else {{ delete msg.payload; }}\n"
                "msg._httpNode = " + js(nm) + "; return msg;"), 1
    if t == "wait":
        return f"return emit({js(nm)}, [items]);", 1
    return (f"node.warn('TODO: “{nm}” ({n['type']}) has no built-in Node-RED equivalent — install the matching node-red-contrib "
            f"package or call its REST API with an http request node. Passing items through.');\nreturn emit({js(nm)}, [items]);"), 1


def _reaches(wf, a, b):
    """True if b is downstream of a (used to spot loop-back edges)."""
    seen, stack = set(), [a]
    while stack:
        x = stack.pop()
        for outs in _main_outs(wf, x):
            for tg in outs or []:
                if tg["node"] == b:
                    return True
                if tg["node"] not in seen:
                    seen.add(tg["node"]); stack.append(tg["node"])
    return False


def to_node_red(wf: dict) -> tuple[list, list]:
    tab = "tab_" + uuid.uuid4().hex[:8]
    flows = [{"id": tab, "type": "tab", "label": wf.get("name", "n8n flow"), "disabled": False, "info": "Converted from n8n by automation-studio"}]
    notes = []
    ids, outs_count, post = {}, {}, {}
    order = _order(wf)
    x0 = 120
    for i, n in enumerate(order):
        ids[n["name"]] = "n_" + uuid.uuid4().hex[:10]
    pos = {n["name"]: n.get("position") or [i * 220, 0] for i, n in enumerate(order)}
    for n in order:
        t, nm, nid = _short(n["type"]), n["name"], ids[n["name"]]
        x, y = int(pos[nm][0] * 0.9 + x0), int(pos[nm][1] * 0.6 + 120)
        if t in ("webhook",):
            p = n.get("parameters") or {}
            hin = "h_" + uuid.uuid4().hex[:8]
            flows.append({"id": hin, "type": "http in", "z": tab, "name": nm, "url": "/" + p.get("path", "hook").lstrip("/"),
                          "method": p.get("httpMethod", "GET").lower(), "upload": False, "x": x - 180, "y": y, "wires": [[nid]]})
            func = ("msg.items = [{ json: { body: msg.payload, headers: msg.req.headers, query: msg.req.query, params: msg.req.params } }];\n"
                    "msg._nodes = {}; msg._nodes[" + json.dumps(nm) + "] = msg.items; return msg;")
            flows.append({"id": nid, "type": "function", "z": tab, "name": nm + " (items)", "func": func, "outputs": 1, "x": x, "y": y, "wires": [[]]})
            outs_count[nm] = 1
            if p.get("responseMode") in ("onReceived", None):
                resp = "r_" + uuid.uuid4().hex[:8]
                flows.append({"id": resp, "type": "http response", "z": tab, "name": "200 received", "statusCode": "200", "headers": {}, "x": x, "y": y + 60, "wires": []})
                post.setdefault(nm, []).append(resp)
            continue
        if t in ("manualTrigger", "scheduleTrigger", "cron", "interval"):
            p = n.get("parameters") or {}
            rep, crontab = "", ""
            iv = ((p.get("rule") or {}).get("interval") or [{}])[0] if t == "scheduleTrigger" else {}
            if iv.get("field") in ("minutes", "hours", "seconds"):
                mul = {"seconds": 1, "minutes": 60, "hours": 3600}[iv["field"]]
                rep = str(int(iv.get(iv["field"] + "Interval", 1)) * mul)
            elif iv.get("field") == "cronExpression":
                crontab = iv.get("expression", "")
            inj = {"id": nid, "type": "inject", "z": tab, "name": nm, "props": [{"p": "payload"}], "repeat": rep, "crontab": crontab,
                   "once": False, "topic": "", "payload": "{}", "payloadType": "json", "x": x, "y": y, "wires": [[]]}
            flows.append(inj)
            outs_count[nm] = 1
            continue
        body, n_out = _nr_body(n)
        flows.append({"id": nid, "type": "function", "z": tab, "name": nm, "func": RUNTIME + "\n// ---- " + nm + " ----\n" + body,
                      "outputs": n_out, "timeout": 0, "noerr": 0, "initialize": "", "finalize": "", "libs": [], "x": x, "y": y,
                      "wires": [[] for _ in range(n_out)]})
        outs_count[nm] = n_out
        if t == "respondToWebhook":
            resp = "r_" + uuid.uuid4().hex[:8]
            flows.append({"id": resp, "type": "http response", "z": tab, "name": nm + " →", "statusCode": "", "headers": {}, "x": x + 200, "y": y, "wires": []})
            post.setdefault(nm, []).append(resp)
        if t == "httpRequest":
            hreq = "q_" + uuid.uuid4().hex[:8]
            back = "b_" + uuid.uuid4().hex[:8]
            flows.append({"id": hreq, "type": "http request", "z": tab, "name": nm + " (call)", "method": "use", "ret": "obj", "paytoqs": "ignore",
                          "url": "", "tls": "", "persist": False, "proxy": "", "authType": "", "senderr": False, "headers": [], "x": x + 160, "y": y + 50, "wires": [[back]]})
            flows.append({"id": back, "type": "function", "z": tab, "name": nm + " (items)", "outputs": 1, "x": x + 320, "y": y + 50, "wires": [[]],
                          "func": "const N = msg._nodes = msg._nodes || {}; const p = msg.payload; const its = (Array.isArray(p) ? p : [p]).map(x => ({ json: (typeof x === 'object' && x) ? x : { data: x } }));\n"
                                  "N[msg._httpNode] = its; msg.items = its; return msg;"})
            flows[-3]["wires"] = [[hreq]]
            post[nm] = ["__via__" + back]
        if t not in ("set", "if", "filter", "switch", "code", "splitOut", "aggregate", "noOp", "merge", "limit", "sort", "removeDuplicates",
                     "respondToWebhook", "httpRequest", "wait", "splitInBatches"):
            notes.append(f"“{nm}” ({n['type']}) → TODO pass-through: use a node-red-contrib package or an http request to its API")
    byid = {f["id"]: f for f in flows}
    for n in order:
        nm = n["name"]
        src_id = ids[nm]
        via = [p for p in post.get(nm, []) if p.startswith("__via__")]
        src = byid[via[0][7:]] if via else byid.get(src_id)
        if src is None:
            continue
        outs = _main_outs(wf, nm)
        for oi, targets in enumerate(outs):
            if oi >= len(src["wires"]):
                break
            for tg in targets or []:
                if tg["node"] in ids:
                    tid = ids[tg["node"]]
                    tnode = wf_node = next((x for x in order if x["name"] == tg["node"]), None)
                    if tnode and _short(tnode["type"]) == "webhook":
                        continue
                    if tnode and _short(tnode["type"]) == "splitInBatches" and _reaches(wf, tnode["name"], nm):
                        continue                      # loop-back edge (nextBatch): Node-RED has no batch loop

                    src["wires"][oi].append(tid)
        for extra in post.get(nm, []):
            if not extra.startswith("__via__"):
                byid[src_id]["wires"][0].append(extra)
    return flows, notes


# ----------------------------------------------------------------------------------------- Make
def _split_top(code, sep):
    parts, depth, cur, i, q = [], 0, "", 0, None
    while i < len(code):
        ch = code[i]
        if q:
            cur += ch
            if ch == "\\" and i + 1 < len(code):
                cur += code[i + 1]; i += 2; continue
            if ch == q:
                q = None
        elif ch in "\"'`":
            q = ch; cur += ch
        elif ch in "([{":
            depth += 1; cur += ch
        elif ch in ")]}":
            depth -= 1; cur += ch
        elif depth == 0 and code.startswith(sep, i):
            parts.append(cur); cur = ""; i += len(sep); continue
        else:
            cur += ch
        i += 1
    parts.append(cur)
    return [p.strip() for p in parts]


def _balanced_wrap(c, o, cl):
    if not (c.startswith(o) and c.endswith(cl)):
        return False
    d = 0
    for i, ch in enumerate(c):
        d += ch == o
        d -= ch == cl
        if d == 0 and i < len(c) - 1:
            return False
    return True


def _top_ops(code, ops):
    """Positions of top-level operators (outside strings/brackets/regex-free code), longest match first."""
    found, depth, q, i = [], 0, None, 0
    ops = sorted(ops, key=len, reverse=True)
    while i < len(code):
        ch = code[i]
        if q:
            if ch == "\\":
                i += 2; continue
            if ch == q:
                q = None
            i += 1; continue
        if ch in "\"'`":
            q = ch; i += 1; continue
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif depth == 0:
            for op in ops:
                if code.startswith(op, i):
                    prev = code[:i].rstrip()
                    if op in "+-" and (not prev or prev[-1] in "(*/+-<>=!&|?:,"):
                        break                         # unary sign
                    if op in (">", "<") and (code.startswith("=>", i - 1) or code.startswith(">=", i) or code.startswith("<=", i)):
                        break
                    found.append((i, op)); i += len(op) - 1
                    break
        i += 1
    return found


def op_left_assoc(group):
    return group[0] in ("+", "*", "&&")


class MakeX:
    """Translate n8n JS expressions to Make formulas ({{1.email}}, trim(), lower(), ifempty() …)."""
    def __init__(self):
        self.src = {}        # field name -> module id that outputs it
        self.mid = {}        # n8n node name -> module id
        self.hook = None     # webhook module id
        self.untranslated = []

    def ref(self, path, prev):
        head = path.split(".")[0]
        return f"{self.src.get(head, prev)}.{path}"

    def tr(self, c, prev):
        c = c.strip()
        while _balanced_wrap(c, "(", ")"):
            c = c[1:-1].strip()
        alts = _split_top(c, "||")
        if len(alts) > 1:
            out = self.tr(alts[-1], prev)
            for a in reversed(alts[:-1]):
                t = self.tr(a, prev)
                if t is None or out is None:
                    return None
                out = f"ifempty({t}; {out})"
            return out
        for group, mk in ((("&&",), None), (("===", "!==", "==", "!=", ">=", "<=", ">", "<"), None), (("+", "-"), None), (("*", "/"), None)):
            pos = _top_ops(c, group)
            if pos:
                i, op = pos[-1] if op_left_assoc(group) else pos[0]
                a, b = self.tr(c[:i], prev), self.tr(c[i + len(op):], prev)
                if a is None or b is None:
                    return None
                mop = {"&&": "and", "===": "=", "==": "=", "!==": "!=", "!=": "!="}.get(op, op)
                return f"{a} {mop} {b}"
        m = re.fullmatch(r"Math\.(round|floor|ceil|abs|max|min)\(([\s\S]+)\)", c)
        if m:
            args = [self.tr(x, prev) for x in _split_top(m.group(2), ",")]
            return None if None in args else f"{m.group(1)}({'; '.join(args)})"
        m = re.fullmatch(r"Number\(([\s\S]+)\)", c)
        if m:
            a = self.tr(m.group(1), prev)
            return None if a is None else f'parseNumber({a}; ".")'
        m = re.fullmatch(r"(.+)\.length", c, re.S)
        if m:
            a = self.tr(m.group(1), prev)
            return None if a is None else f"length({a})"
        m = re.fullmatch(r"(.+)\.includes\((.+)\)", c, re.S)
        if m:
            a, b = self.tr(m.group(1), prev), self.tr(m.group(2), prev)
            return None if a is None or b is None else f"contains({a}; {b})"
        m = re.fullmatch(r"(.+)\.slice\(\s*(\d+)\s*,\s*(\d+)\s*\)", c, re.S)
        if m:
            a = self.tr(m.group(1), prev)
            return None if a is None else f"substring({a}; {m.group(2)}; {m.group(3)})"
        m = re.fullmatch(r"(.+)\.replace\((\"[^\"]*\"|'[^']*'),\s*(\"[^\"]*\"|'[^']*')\)", c, re.S)
        if m:
            a = self.tr(m.group(1), prev)
            return None if a is None else f'replace({a}; "{m.group(2)[1:-1]}"; "{m.group(3)[1:-1]}")'
        if c == "[]":
            return "emptyarray"
        if c == "$execution.id":
            return "executionId"
        if re.fullmatch(r'"[^"]*"|\'[^\']*\'|-?\d+(\.\d+)?|true|false', c):
            return '"' + c[1:-1] + '"' if c[0] == "'" else c
        m = re.fullmatch(r"(.+)\.(trim|toLowerCase|toUpperCase)\(\)", c, re.S)
        if m:
            inner = self.tr(m.group(1), prev)
            return None if inner is None else f"{ {'trim': 'trim', 'toLowerCase': 'lower', 'toUpperCase': 'upper'}[m.group(2)] }({inner})"
        m = re.fullmatch(r"(.+)\.replace\((/.+/[gimsu]*),\s*(\"[^\"]*\"|'[^']*')\)", c, re.S)
        if m:
            inner = self.tr(m.group(1), prev)
            rep = m.group(3)
            return None if inner is None else f'replace({inner}; {m.group(2)}; "{rep[1:-1]}")'
        m = re.fullmatch(r"\$json\.body\.([\w.]+)", c)
        if m and self.hook:
            return f"{self.hook}.{m.group(1)}"
        m = re.fullmatch(r"\$json\.([\w.]+)", c)
        if m:
            return self.ref(m.group(1), prev)
        m = re.fullmatch(r"\$\((['\"])(.+?)\1\)\.(?:item|first\(\)|last\(\))\.json\.([\w.]+)", c)
        if m and m.group(2) in self.mid:
            return f"{self.mid[m.group(2)]}.{m.group(3)}"
        if re.fullmatch(r"\$now(\.toISO\(\))?", c):
            return "now"
        if c == "$today.toISODate()" or c == "$now.toISODate()":
            return 'formatDate(now; "YYYY-MM-DD")'
        return None

    def value(self, v, prev):
        """n8n parameter value -> Make mapper value (string with {{…}})."""
        if not isinstance(v, str) or not v.startswith("="):
            return v
        s = v[1:]
        whole = re.fullmatch(r"\s*\{\{([\s\S]*)\}\}\s*", s)
        if whole and "}}" not in whole.group(1):
            code = whole.group(1).strip()
            if _balanced_wrap(code, "{", "}"):          # object literal -> JSON text with mapped values
                parts = []
                for kv in _split_top(code[1:-1], ","):
                    if not kv:
                        continue
                    k, _, val = kv.partition(":")
                    t = self.tr(val, prev)
                    k = k.strip().strip("\"'")
                    if t is None:
                        self.untranslated.append(val.strip()); return "⚠ TRANSLATE: " + s
                    lit = re.fullmatch(r'"[^"]*"|-?\d+(\.\d+)?|true|false', t)
                    parts.append(f'"{k}": ' + (t if lit else '"{{' + t + '}}"'))
                return "{" + ", ".join(parts) + "}"
            t = self.tr(code, prev)
            if t is None:
                self.untranslated.append(code); return "⚠ TRANSLATE: " + s
            return t.strip('"') if re.fullmatch(r'"[^"]*"', t) else "{{" + t + "}}"
        def seg(m):
            t = self.tr(m.group(1), prev)
            if t is None:
                self.untranslated.append(m.group(1).strip()); return "⚠{{" + m.group(1) + "}}"
            return "{{" + t + "}}"
        return re.sub(r"\{\{([\s\S]*?)\}\}", seg, s)


# verified against Make's module catalog (app-modules_list, 2026-10): n8n type -> Make "app:Module" (app version)
MAKE_APPS = {
    "googleSheets": {"append": "google-sheets:addRow (v2)", "appendOrUpdate": "google-sheets:filterRows + updateRow/addRow (v2)",
                     "update": "google-sheets:updateRow (v2)", "read": "google-sheets:filterRows (v2)", "delete": "google-sheets:deleteRow (v2)",
                     "*": "google-sheets (v2) — Add a Row / Search Rows / Update a Row"},
    "gmail": {"send": "google-email:ActionSendEmail (v2)", "reply": "google-email:ActionSendEmail (v2)", "*": "google-email (v2)"},
    "slack": {"post": "slack:CreateMessage (v4)", "*": "slack:CreateMessage (v4)"},
    "telegram": {"sendMessage": "telegram:SendReplyMessage (v1)", "sendPhoto": "telegram:SendPhoto (v1)", "sendDocument": "telegram:SendDocument (v1)",
                 "*": "telegram:SendReplyMessage (v1)"},
    "telegramTrigger": {"*": "telegram:WatchUpdates (v1)"},
    "openAi": {"*": "openai-gpt-3:CreateCompletion (v1) — or createModelResponse"},
    "lmChatOpenAi": {"*": "openai-gpt-3:CreateCompletion (v1)"},
    "agent": {"*": "openai-gpt-3:createModelResponse (v1) — Make has no agent loop; or use Make AI Agents"},
    "informationExtractor": {"*": "openai-gpt-3:transformTextToStructuredData (v1)"},
    "googleSheetsTrigger": {"*": "google-sheets:watchRows (v2)"},
    "gmailTrigger": {"*": "google-email:TriggerNewEmail (v2)"},
}


def make_app_hint(n):
    t = n["type"].split(".")[-1]
    p = n.get("parameters") or {}
    m = MAKE_APPS.get(t)
    if not m:
        return None
    return m.get(p.get("operation", ""), m.get("*"))


MAKE_OPS = {"equals": "text:equal", "notEquals": "text:notequal", "contains": "text:contain", "notContains": "text:notcontain",
            "startsWith": "text:startwith", "endsWith": "text:endwith", "regex": "text:pattern", "notRegex": "text:notpattern",
            "gt": "number:greater", "lt": "number:less", "gte": "number:greaterorequal", "lte": "number:lessorequal",
            "exists": "exist", "notEmpty": "exist", "notExists": "notexist", "empty": "notexist", "true": "boolean:equal", "false": "boolean:equal"}


def to_make(wf: dict) -> tuple[dict, list]:
    order = _order(wf)
    byname = {n["name"]: n for n in order}
    X = MakeX()
    notes = []
    counter = [0]

    def new_id():
        counter[0] += 1
        return counter[0]

    def meta(n, extra=""):
        pos = n.get("position") or [0, 0]
        return {"designer": {"x": int(pos[0]), "y": int(pos[1])}, "restore": {}, "notes": n["name"] + extra}

    def module(n, prev):
        t, p = _short(n["type"]), n.get("parameters") or {}
        mid = new_id()
        X.mid[n["name"]] = mid
        base = {"id": mid, "module": "", "version": 1, "parameters": {}, "mapper": {}, "metadata": meta(n)}
        if t in ("formTrigger", "chatTrigger"):
            X.hook = mid
            base.update({"module": "gateway:CustomWebHook", "parameters": {"hook": None, "maxResults": 1}, "mapper": None})
            base["metadata"]["notes"] = f"{n['name']} (was {t})"
            if t == "chatTrigger":
                notes.append(f"{n['name']}: Make has no hosted chat — send chat messages from your widget/bot to the webhook of module {mid}.")
            else:
              notes.append(f"{n['name']}: Make has no hosted form — point a Tally / Google Forms / Typeform / Jotform webhook at module {mid}, "
                         "using the same field names (" + ", ".join(f.get("fieldLabel", "") for f in ((p.get("formFields") or {}).get("values") or [])) + ").")
        elif t == "webhook":
            X.hook = mid
            base.update({"module": "gateway:CustomWebHook", "parameters": {"hook": None, "maxResults": 1}, "mapper": None})
            notes.append(f"{n['name']}: open module {mid} → Add → create the webhook, send one sample request (Redetermine data structure), "
                         "then point the caller at the new URL.")
        elif t == "scheduleTrigger":
            base.update({"module": "util:SetVariables", "mapper": {"variables": [{"name": "started_at", "value": "{{now}}"}]}})
            notes.append("Schedule: in Make the schedule is a scenario setting (clock icon on the first module) — set it after import.")
        elif t == "httpRequest":
            body = {b["name"]: X.value(b.get("value"), prev) for b in ((p.get("bodyParameters") or {}).get("parameters") or [])}
            base.update({"module": "http:ActionSendData", "version": 3, "mapper": {
                "url": X.value(p.get("url", ""), prev), "method": p.get("method", "GET").lower(),
                "headers": [{"name": h["name"], "value": X.value(h.get("value"), prev)} for h in ((p.get("headerParameters") or {}).get("parameters") or [])],
                "qs": [{"name": q["name"], "value": X.value(q.get("value"), prev)} for q in ((p.get("queryParameters") or {}).get("parameters") or [])],
                "bodyType": "raw" if p.get("sendBody") else "", "contentType": "application/json" if p.get("sendBody") else None,
                "data": (json.dumps(body, ensure_ascii=False) if body else X.value(p.get("jsonBody"), prev)) if p.get("sendBody") else None,
                "parseResponse": True, "shareCookies": False, "followRedirect": True, "useQuerystring": False, "gzip": True,
                "useMtls": False, "rejectUnauthorized": True, "followAllRedirects": False, "serializeUrl": False, "ca": "", "timeout": ""}, "parameters": {"handleErrors": True}})
        elif t == "set":
            vs = [{"name": a["name"], "value": X.value(a.get("value"), prev)} for a in (((p.get("assignments") or {}).get("assignments")) or [])]
            base.update({"module": "util:SetVariables", "mapper": {"variables": vs}})
            for v in vs:
                X.src[v["name"]] = mid
        elif t == "respondToWebhook":
            body = p.get("responseBody", "")
            base.update({"module": "gateway:WebhookRespond", "mapper": {"status": int((p.get("options") or {}).get("responseCode", 200)),
                         "body": X.value(body if isinstance(body, str) else json.dumps(body), prev),
                         "headers": [{"key": "Content-Type", "value": "application/json"}]}})
        elif t == "splitOut":
            f = p.get("fieldToSplitOut", "items")
            base.update({"module": "builtin:BasicFeeder", "mapper": {"array": "{{" + X.ref(f, prev) + "}}"}})
        elif t == "aggregate":
            base.update({"module": "builtin:BasicAggregator", "parameters": {"feeder": prev}, "mapper": None})
        elif t == "wait":
            base.update({"module": "util:FunctionSleep", "mapper": {"duration": min(300, int(p.get("amount", 5) or 5))}})
        else:
            base.update({"module": "util:SetVariables", "mapper": {"variables": [{"name": "TODO", "value": f"replace with the Make module for {n['type']}"}]}})
            base["metadata"]["notes"] = f"PLACEHOLDER → {n['name']} ({n['type']} {p.get('resource', '')} {p.get('operation', '')})".strip()
            hint = make_app_hint(n)
            notes.append(f"Module {mid} “{n['name']}” is a placeholder — replace it with "
                         + (f"**{hint}**" if hint else f"the {n['type'].split('.')[-1]} app module ({p.get('resource', '')} {p.get('operation', '')})")
                         + " and map its fields.")
        return base

    def filt(name, conds, prev):
        if not conds:
            return {"name": name, "conditions": []}
        rows = []
        for x in conds.get("conditions") or []:
            op = (x.get("operator") or {}).get("operation")
            mop = MAKE_OPS.get(op, "text:equal")
            if mop.startswith("text:") and not (conds.get("options") or {}).get("caseSensitive", True):
                mop += ":ci"                                  # Make's case-insensitive text operators
            row = {"a": X.value(x.get("leftValue"), prev), "o": mop}
            if op not in ("exists", "notEmpty", "notExists", "empty"):
                row["b"] = "true" if op == "true" else "false" if op == "false" else X.value(x.get("rightValue"), prev)
            rows.append(row)
        return {"name": name, "conditions": [rows] if conds.get("combinator") != "or" else [[r] for r in rows]}

    def chain(names, prev):
        flow = []
        while names:
            nm = names.pop(0)
            n = byname.get(nm)
            if n is None or nm in X.mid:
                continue
            t = _short(n["type"])
            if t in ("if", "switch", "filter"):
                rid = new_id()
                X.mid[nm] = rid
                p = n.get("parameters") or {}
                conds = [p.get("conditions")] if t in ("if", "filter") else [r.get("conditions") for r in ((p.get("rules") or {}).get("values") or [])]
                routes = []
                for oi, targets in enumerate(_main_outs(wf, nm)):
                    if not targets:
                        continue
                    label = (["true", "false"][oi] if t == "if" else f"route {oi}")
                    c = conds[oi] if oi < len(conds) else None
                    sub = chain([tg["node"] for tg in targets], prev)
                    if sub:
                        sub[0]["filter"] = filt(f"{nm}: {label if c else 'otherwise'}", c, prev)
                        routes.append({"flow": sub})
                if t == "if" and len(routes) == 2:
                    notes.append(f"Router “{nm}”: set the second route as the fallback route (route ⋯ → Set as fallback) — Make has no 'else'.")
                flow.append({"id": rid, "module": "builtin:BasicRouter", "version": 1, "mapper": None, "metadata": meta(n), "routes": routes})
                break
            m = module(n, prev)
            prev = m["id"]
            flow.append(m)
            outs = _main_outs(wf, nm)
            if len(outs) > 1 and any(outs[1:]):
                notes.append(f"“{nm}” has more than one output — only the first is converted; add a router for the others.")
            names = ([tg["node"] for tg in outs[0]] if outs and outs[0] else []) + names
        return flow

    targets = {tg["node"] for s in wf.get("connections", {}).values() for outs in (s.get("main") or []) for tg in outs or []}
    roots = [n["name"] for n in order if n["name"] not in targets]
    flow = chain(roots[:1], 0)
    if X.untranslated:
        notes.append("Expressions marked ⚠ TRANSLATE need Make functions by hand: " + " · ".join(sorted(set(X.untranslated)))[:800])
    bp = {"name": wf.get("name", "Scenario"), "flow": flow,
          "metadata": {"instant": X.hook is not None, "version": 1,
                       "scenario": {"roundtrips": 1, "maxErrors": 3, "autoCommit": True, "autoCommitTriggerLast": True, "sequential": False,
                                    "confidential": False, "dataloss": False, "dlq": False, "freshVariables": False},
                       "designer": {"orphans": []}, "zone": "eu1.make.com"}}
    return bp, notes


# ----------------------------------------------------------------------------------------- guides
PLATFORM = {
    "zapier": {"title": "Zapier", "trigger": "Trigger", "if": "Paths by Zapier (one path per branch) — or Filter by Zapier for a single yes-branch",
               "code": "Code by Zapier → Run JavaScript (inputs arrive as `inputData`, return an object or array)",
               "http": "Webhooks by Zapier → Custom Request (or API Request in the app's own actions)",
               "webhook": "Webhooks by Zapier → Catch Hook (copy the URL it gives you)", "schedule": "Schedule by Zapier",
               "set": "Formatter by Zapier (text/number/date utilities) or map fields directly in the next step",
               "loop": "Looping by Zapier (Create Loop From Line Items)", "respond": "not supported — a Zapier Catch Hook always answers 200 at once and the Zap runs afterwards; if the caller needs this reply, keep this flow on n8n/Make/Pipedream",
               "notes": "Each action step = 1 task per run (pricing). Test every step with sample data in the editor; turn the Zap on at the end."},
    "power-automate": {"title": "Microsoft Power Automate", "trigger": "Trigger", "if": "Condition (Yes/No) or Switch",
                       "code": "No JavaScript runtime — use expressions (Compose), 'Run script' in Excel Online, or an Azure Function",
                       "http": "HTTP action (premium connector)", "webhook": "When an HTTP request is received (premium) — copy the generated URL",
                       "schedule": "Recurrence", "set": "Compose / Initialize variable / Set variable",
                       "loop": "Apply to each", "respond": "Response action (status code + body)",
                       "notes": "Expressions: triggerBody()?['email'], body('Step')?['field'], formatDateTime(utcNow(),'yyyy-MM-dd'). HTTP + Request trigger need a premium licence."},
    "pipedream": {"title": "Pipedream", "trigger": "Trigger", "if": "a Node.js step with `return $.flow.exit('reason')` to stop, or 'Filter' / 'Delay' built-ins",
                  "code": "Node.js code step: export default defineComponent({ async run({ steps, $ }) { … } })",
                  "http": "HTTP / Webhook → Send any HTTP request (or `axios` in a code step)", "webhook": "HTTP / Webhook trigger (gives a URL)",
                  "schedule": "Schedule trigger", "set": "code step returning the new object", "loop": "plain JavaScript loop in a code step",
                  "respond": "`await $.respond({ status: 200, body })` in a code step (enable HTTP response in the trigger)",
                  "notes": "Connected accounts hold credentials; steps reference earlier ones as steps.<name>.$return_value."},
    "activepieces": {"title": "Activepieces", "trigger": "Trigger", "if": "Branch (conditions) / Router",
                     "code": "Code piece: export const code = async (inputs) => { … return result; }",
                     "http": "HTTP piece → Send HTTP request", "webhook": "Webhook trigger (Catch webhook)", "schedule": "Schedule trigger",
                     "set": "Data Mapper / Text helper pieces, or a Code piece", "loop": "Loop on items",
                     "respond": "Webhook → Return response", "notes": "Open source (self-host with Docker) — closest to n8n in ideas."},
}


def _v(x):
    """Readable value for guides: drop n8n's '=' expression prefix and resource-locator wrappers."""
    if isinstance(x, str):
        return x[1:] if x.startswith("=") else x
    if isinstance(x, dict) and x.get("__rl"):
        return x.get("cachedResultName") or x.get("value") or "(choose in the app)"
    if isinstance(x, dict):
        return {k: _v(v) for k, v in x.items() if k not in ("schema", "attemptToConvertTypes", "convertFieldsToString", "matchingColumns")}
    if isinstance(x, list):
        return [_v(v) for v in x]
    return x


def guide(wf: dict, platform: str) -> str:
    P = PLATFORM[platform]
    order = _order(wf)
    lines = [f"# {wf.get('name', 'Workflow')} — build guide for {P['title']}", "",
             f"Converted from an n8n workflow by automation-studio. {P['notes']}", "", "## Steps", ""]
    code_steps = []
    for i, n in enumerate(order, 1):
        t, p, nm = _short(n["type"]), n.get("parameters") or {}, n["name"]
        if t == "webhook":
            how = f"{P['webhook']} — method {p.get('httpMethod', 'GET')}, path `{p.get('path', '')}`"
        elif t in ("scheduleTrigger", "cron"):
            how = f"{P['schedule']} — {json.dumps(p.get('rule', p))[:160]}"
        elif t in ("if", "filter", "switch"):
            how = f"{P['if']}\n   conditions: " + "; ".join(
                f"`{_v(c.get('leftValue'))}` {(c.get('operator') or {}).get('operation')} `{_v(c.get('rightValue', ''))}`"
                for c in (((p.get("conditions") or {}).get("conditions")) or [])) + (
                "" if t != "switch" else " ".join(f"\n   - route {k}: " + "; ".join(
                    f"`{_v(c.get('leftValue'))}` {(c.get('operator') or {}).get('operation')} `{_v(c.get('rightValue', ''))}`"
                    for c in ((r.get('conditions') or {}).get('conditions') or [])) for k, r in enumerate(((p.get('rules') or {}).get('values') or []))))
        elif t == "code":
            how = P["code"] + f" — see code step {len(code_steps) + 1} below"
            code_steps.append((nm, p.get("jsCode", "")))
        elif t == "httpRequest":
            how = f"{P['http']} — {p.get('method', 'GET')} `{_v(p.get('url', ''))}`"
        elif t == "set":
            how = P["set"] + ": " + ", ".join(f"`{a['name']}` = `{_v(a.get('value'))}`" for a in (((p.get('assignments') or {}).get('assignments')) or []))
        elif t in ("splitInBatches", "splitOut"):
            how = P["loop"]
        elif t == "respondToWebhook":
            how = P["respond"] + f" — status {(p.get('options') or {}).get('responseCode', 200)}, body `{_v(p.get('responseBody', ''))}`"
        else:
            how = f"{n.get('type').split('.')[-1]} → use the {P['title']} app for it; operation: {p.get('resource', '')} {p.get('operation', '')}".strip()
            fields = {k: v for k, v in p.items() if k not in ("resource", "operation", "options", "authentication") and v not in ("", None, {}, [])}
            if fields:
                how += "\n   fields: " + json.dumps(_v(fields), ensure_ascii=False)[:700]
        nxt = [tg["node"] for outs in _main_outs(wf, nm) for tg in outs or []]
        lines.append(f"{i}. **{nm}** — {how}" + (f"\n   → next: {', '.join(nxt)}" if nxt else ""))
    if code_steps:
        lines += ["", "## Code steps (paste as-is, then adjust the input mapping)", ""]
        for k, (nm, code) in enumerate(code_steps, 1):
            if platform == "pipedream":
                wrapped = ("export default defineComponent({\n  async run({ steps, $ }) {\n    const items = [{ json: steps.trigger.event.body || steps.trigger.event }];\n"
                           "    const $input = { all: () => items, first: () => items[0] };\n" + "\n".join("    " + l for l in code.splitlines()) + "\n  },\n});")
            elif platform == "activepieces":
                wrapped = ("export const code = async (inputs) => {\n  const items = [{ json: inputs }];\n  const $input = { all: () => items, first: () => items[0] };\n"
                           + "\n".join("  " + l for l in code.splitlines()) + "\n};")
            elif platform == "zapier":
                wrapped = ("// Code by Zapier (JavaScript). Map the fields you need into inputData in the step setup.\n"
                           "const items = [{ json: inputData }];\nconst $input = { all: () => items, first: () => items[0] };\n"
                           "const result = (() => {\n" + code + "\n})();\noutput = Array.isArray(result) ? result.map(r => r.json || r) : (result.json || result);")
            else:
                wrapped = "// No JavaScript runtime in Power Automate — rebuild this logic with expressions/Compose:\n" + code
            lines += [f"### Code step {k}: {nm}", "```javascript", wrapped, "```", ""]
    lines += ["", "## Test", "", "Run the trigger with the same sample data used for the n8n tests (the .cases.json file) and compare each step's output."]
    return "\n".join(lines)


def convert(wf: dict, to: str, outdir: Path, env=None) -> list[str]:
    outdir.mkdir(parents=True, exist_ok=True)
    stem = re.sub(r"[^\w\-]+", "_", wf.get("name", "workflow"), flags=re.ASCII).strip("_") or "workflow"
    files = []
    if to == "node-red":
        flows, notes = to_node_red(wf)
        f = outdir / f"{stem}.node-red.json"
        f.write_text(json.dumps(flows, indent=1, ensure_ascii=False))
        files.append(str(f))
        g = outdir / "NODE_RED_NOTES.md"
        g.write_text("# Node-RED import\n\nMenu → Import → select the file → Deploy.\n\n" + "\n".join(f"- {x}" for x in notes) + "\n")
        files.append(str(g))
    elif to == "make":
        bp, notes = to_make(wf)
        f = outdir / f"{stem}.make-blueprint.json"
        f.write_text(json.dumps(bp, indent=1, ensure_ascii=False))
        files.append(str(f))
        g = outdir / "MAKE_GUIDE.md"
        def rows(flow, depth=0):
            out = []
            for m in flow:
                fl = m.get("filter", {}).get("name")
                out.append(f"{'  ' * depth}- **{m['id']}** `{m['module']}` — {m['metadata'].get('notes', '')}" + (f"  _(filter: {fl})_" if fl else ""))
                for r in m.get("routes", []):
                    out += rows(r["flow"], depth + 1)
            return out
        g.write_text("# Make.com import\n\n1. Scenarios → Create a new scenario → ⋯ (bottom toolbar) → **Import Blueprint** → choose the file → Save.\n"
                     "2. Open each module marked below, connect the app account and check the mapped fields "
                     "(Make refers to earlier modules by number, e.g. `{{2.email}}`).\n3. Run once with sample data, then switch the scenario ON.\n\n"
                     "## Modules\n\n" + "\n".join(rows(bp["flow"])) + "\n\n## To finish by hand\n\n" + "\n".join(f"- {x}" for x in notes) + "\n")
        files.append(str(g))
    elif to in PLATFORM:
        f = outdir / f"{stem}.{to}-guide.md"
        f.write_text(guide(wf, to))
        files.append(str(f))
    else:
        raise SystemExit(f"unknown platform '{to}' — node-red, make, zapier, power-automate, pipedream, activepieces")
    return files
