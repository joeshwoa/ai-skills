#!/usr/bin/env python3
"""autokit — the automation-studio toolkit (n8n first, every other platform second).

  doctor                                   what is installed, n8n version, targets, secrets file
  nodes <words…> [--limit 15]               search the node catalog of the installed n8n
  node <type> [--version V] [--ts] [--filter resource=…]  versions, credentials, fields; --ts = exact parameter types
  guide [list|sdk|patterns|params|<technique>|<PARAM_GUIDE>]   n8n's own building guidance (installed version)
  new list | new <pattern|number> -o flow.ts   start from a tested pattern (copies cases + sub-workflows)
  build <flow.ts|flow.json> -o flow.json   SDK code → JSON; normalise ids, webhookIds, settings, layout
  validate <flow.json> [--lenient] [--json]    static checks + official SDK schema validation
  test <flow.json> <cases.json> [--keep] [--json]   run every case in a throw-away local n8n
  diagram <flow.json|plan.json> -o <dir> [--formats svg,png,pdf,html,mmd,excalidraw]
  creds <flow.json> [--apply --target T] [--schema TYPE]   needed credentials + how to get them; create from secrets file
  deploy <flow.json> --target local|cloud|… [--activate] [--id ID]   create/update through the REST API
  pull --target T --id ID -o flow.json      download a workflow from an instance
  list --target T                           workflows on an instance
  trigger --target T --path P [--data '{…}'|@file] [--method POST] [-H 'Name: v'] [--test]   call a webhook, show the run
  executions --target T [--id WF] [--limit 5]   recent runs with per-node status
  activate | deactivate --target T --id WF     switch a workflow on/off
  convert <flow.json> --to node-red|make|zapier|power-automate|pipedream|activepieces -o <dir>
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from n8nenv import Env  # noqa: E402

SKILL = HERE.parent


def load_json(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"{p}: invalid JSON — {e}")


def dump(obj, p):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


# ------------------------------------------------------------------------------------------ build
def normalise(wf: dict, cat: dict | None = None) -> dict:
    """Make a workflow import-ready: ids, webhookIds, settings, positions (left→right layout)."""
    wf.setdefault("name", "Untitled workflow")
    wf.setdefault("connections", {})
    st = wf.setdefault("settings", {})
    st.setdefault("executionOrder", "v1")
    for n in wf.get("nodes", []):
        n.setdefault("id", str(uuid.uuid4()))
        n.setdefault("parameters", {})
        t = n.get("type", "")
        if (t.endswith(".webhook") or t.endswith("formTrigger") or t.endswith("chatTrigger") or t.endswith(".wait")
                or (cat and (cat.get(t) or {}).get("webhook"))) and not n.get("webhookId"):
            n["webhookId"] = str(uuid.uuid4())
        if cat and n.get("typeVersion") is None and t in cat:
            n["typeVersion"] = cat[t]["defaultVersion"]
    if any("position" not in n for n in wf.get("nodes", [])):
        layout(wf)
    return wf


def layout(wf: dict, dx=260, dy=180):
    """Layered left→right layout (longest path from triggers), AI sub-nodes placed under their root."""
    nodes = {n["name"]: n for n in wf["nodes"]}
    conns = wf.get("connections", {})
    succ, preds, ai_parent = {k: [] for k in nodes}, {k: [] for k in nodes}, {}
    for s, ports in conns.items():
        for pt, outs in ports.items():
            for targets in outs or []:
                for t in targets or []:
                    if t["node"] not in nodes or s not in nodes:
                        continue
                    if pt.startswith("ai_"):
                        ai_parent.setdefault(s, t["node"])
                    else:
                        succ[s].append(t["node"])
                        preds[t["node"]].append(s)
    level = {}
    roots = [k for k in nodes if not preds[k] and k not in ai_parent]
    for r in roots:
        level[r] = 0
    changed, guard = True, 0
    while changed and guard < 200:
        changed, guard = False, guard + 1
        for s in nodes:
            if s not in level:
                continue
            for t in succ[s]:
                if level.get(t, -1) < level[s] + 1 and level[s] + 1 < 60:
                    level[t] = level[s] + 1
                    changed = True
    rows = {}
    for k in nodes:
        if k in ai_parent:
            continue
        lv = level.get(k, 0)
        rows.setdefault(lv, []).append(k)
    for lv, ks in rows.items():
        for i, k in enumerate(ks):
            nodes[k]["position"] = [240 + lv * dx, 300 + (i - (len(ks) - 1) / 2) * dy]
    kids = {}
    for k, p in ai_parent.items():
        kids.setdefault(p, []).append(k)
    for p, ks in kids.items():
        px, py = nodes[p].get("position", [240, 300])
        for i, k in enumerate(ks):
            nodes[k]["position"] = [px - 80 + i * 150, py + 220]
    for n in wf["nodes"]:
        n["position"] = [int(round(n["position"][0])), int(round(n["position"][1]))]


def cmd_build(a, env):
    src = Path(a.src)
    out = Path(a.output or src.with_suffix(".json"))
    if src.suffix in (".ts", ".js"):
        env.require()
        r = env.js("sdk_build.js", src, out)
        if r.returncode:
            raise SystemExit("SDK code → JSON failed:\n" + (r.stderr or r.stdout)[-2500:])
        wf = load_json(out)
    else:
        wf = load_json(src)
    cat = env.catalog() if env.ok else None
    if a.relayout:
        for n in wf.get("nodes", []):
            n.pop("position", None)
    wf = normalise(wf, cat)
    dump(wf, out)
    print(f"built {out}  ({len(wf['nodes'])} nodes)")
    if not a.no_validate and env.ok:
        return cmd_validate(argparse.Namespace(flow=str(out), lenient=False, json=False, no_sdk=False), env)
    return 0


# ------------------------------------------------------------------------------------------ catalog
def cmd_nodes(a, env):
    cat = env.catalog()
    words = [w.lower() for w in a.words]
    scored = []
    for t, m in cat.items():
        hay = " ".join([t, m.get("displayName") or "", m.get("description") or "", " ".join(m.get("categories") or [])]).lower()
        s = sum(3 if w in (m.get("displayName") or "").lower() else 1 for w in words if w in hay)
        if any(w == t.split(".")[-1].lower() or w == (m.get("displayName") or "").lower() for w in words):
            s += 3
        if s == len(words) or s >= len(words) + 1 or (s and len(words) == 1):
            if t.endswith("Tool") and "tool" not in words:
                s -= 0.5
            scored.append((s, t, m))
    scored.sort(key=lambda x: (-x[0], len(x[1])))
    for s, t, m in scored[: a.limit]:
        trig = " [trigger]" if "trigger" in (m.get("group") or []) else ""
        cred = f"  creds: {', '.join(m['credentials'][:3])}" if m["credentials"] else ""
        print(f"{t}  v{m['defaultVersion']}{trig} — {m.get('displayName')}: {(m.get('description') or '')[:80]}{cred}")
    if not scored:
        print("no match — try other words (English, the app's name, or the action: 'send email', 'spreadsheet')")
    return 0


def cmd_node(a, env):
    cat = env.catalog()
    t = a.type if "." in a.type else ("n8n-nodes-base." + a.type)
    if t not in cat and ("@n8n/n8n-nodes-langchain." + a.type) in cat:
        t = "@n8n/n8n-nodes-langchain." + a.type
    m = cat.get(t)
    if not m:
        raise SystemExit(f"unknown node type {t} — search: autokit nodes <words>")
    v = str(a.version or m["defaultVersion"])
    print(f"{t} — {m.get('displayName')}\n  versions: {m['versions']} (default {m['defaultVersion']})")
    print(f"  group: {m.get('group')}  credentials: {m['credentials'] or 'none'}  categories: {m.get('categories')}")
    print(f"  fields v{v}: {', '.join(m['props'].get(v, []))}")
    if a.ts:
        defs = env.ensure_defs()
        pkg = "n8n-nodes-langchain" if t.startswith("@n8n/") else "n8n-nodes-base"
        name = t.split(".")[-1]
        base = defs / pkg / "nodes" / pkg / name
        vs = "v" + v.replace(".", "")
        cands = [base / f"{vs}.ts", base / vs]
        tgt = next((c for c in cands if c.exists()), None)
        if not tgt:
            print(f"  (no type file at {base}/{vs})")
            return 0
        files = [tgt] if tgt.is_file() else sorted(p for p in tgt.rglob("*.ts") if not p.name.endswith(".schema.ts"))
        if a.filter:
            k, _, val = a.filter.partition("=")
            files = [f for f in files if f.name == "index.ts" or f"{k}_{val}".lower() in str(f).lower()]
        for f in files[:12]:
            print(f"\n// ===== {f.relative_to(defs)}")
            print(f.read_text()[:9000])
        if len(files) > 12:
            print(f"\n… {len(files) - 12} more files — narrow with --filter resource=<r> or operation=<o>")
    return 0


def cmd_guide(a, env):
    env.require()
    r = env.js("guide.js", a.topic or "list")
    print(r.stdout or r.stderr)
    return r.returncode


def cmd_new(a, env):
    root = SKILL / "patterns"
    pats = sorted(p for p in root.iterdir() if p.is_dir())
    if a.pattern in ("list", "ls"):
        for p in pats:
            first = (p / "workflow.ts").read_text().splitlines()[0].lstrip("/ ").strip() if (p / "workflow.ts").exists() else ""
            print(f"{p.name:32s} {first}")
        return 0
    hits = [p for p in pats if p.name == a.pattern or p.name.startswith(a.pattern) or a.pattern in p.name]
    if len(hits) != 1:
        raise SystemExit(f"pattern '{a.pattern}' → {len(hits)} matches. Try: autokit new list")
    pat = hits[0]
    src = next((p for p in (pat / "workflow.ts", pat / "workflow.json") if p.exists()), None)
    out = Path(a.output or f"{pat.name}{src.suffix}")
    out.write_text(src.read_text())
    if (pat / "cases.json").exists():
        out.with_name(out.stem + ".cases.json").write_text((pat / "cases.json").read_text())
    for extra in sorted(pat.glob("sub-workflow*")) + sorted(pat.glob("sample-*")):
        if extra.suffix in (".ts", ".json", ".pdf"):
            (out.parent / extra.name).write_bytes(extra.read_bytes())
    print(f"copied {pat.name}/{src.name} → {out} (+ cases/sub-workflows). Edit, then: autokit build {out} -o {out.with_suffix('.json')}")
    return 0


# ------------------------------------------------------------------------------------------ validate / test
def cmd_validate(a, env):
    from wfcheck import check
    wf = load_json(a.flow)
    cat = env.catalog()
    res = check(wf, cat, env, sdk=not a.no_sdk, lenient=a.lenient)
    if a.json:
        print(json.dumps(res, indent=1, ensure_ascii=False))
    else:
        print(f"{'❌' if res['errors'] else '✅'} {Path(a.flow).name}: {len(wf.get('nodes', []))} nodes, triggers: {', '.join(res['triggers']) or '—'}")
        for e in res["errors"]:
            print("  ERROR:", e)
        for w in res["warnings"]:
            print("  WARN: ", w)
        for i in res["info"]:
            print("  info: ", i)
    return 1 if res["errors"] else 0


def cmd_test(a, env):
    import wftest
    wf = load_json(a.flow)
    spec = load_json(a.cases)
    cases = spec["cases"] if isinstance(spec, dict) else spec
    cat = env.catalog()
    res = wftest.run(env, wf, cases, cat, keep=a.keep)
    if a.json:
        print(json.dumps(res, indent=1, ensure_ascii=False, default=str))
    bad = 0
    for r in res:
        bad += not r.get("ok")
        if a.json:
            continue
        print(f"{'✅' if r.get('ok') else '❌'} {r['case']}  → {r.get('status')}"
              + (f"  [{r.get('error')}]" if r.get("error") else ""))
        sb = r.get("sandbox") or {}
        print(f"   trigger: {sb.get('trigger')} · mocked: {', '.join(sb.get('mocked') or []) or '—'} · passthrough: "
              f"{', '.join(sb.get('passthrough') or []) or '—'} · live HTTP: {', '.join(sb.get('live_http') or []) or '—'}")
        for nm, n in (r.get("nodes") or {}).items():
            first = json.dumps(n["first"][0], ensure_ascii=False)[:110] if n["first"] and n["first"][0] is not None else ""
            print(f"   · {nm}: out {n['outputs']}{'  ERROR ' + n['error'] if n.get('error') else ''}  {first}")
        for c in r.get("checks") or []:
            print(f"   {'✓' if c['ok'] else '✗'} {c['check']}" + ("" if c["ok"] else f"   (got: {c['got']})"))
    print(f"---- {len(res) - bad}/{len(res)} case(s) passed")
    return 1 if bad else 0


# ------------------------------------------------------------------------------------------ diagrams / creds / api / convert
def cmd_diagram(a, env):
    import diagram
    files = diagram.render(load_json(a.src), Path(a.output), formats=a.formats.split(","), title=a.title)
    for f in files:
        print("wrote", f)
    return 0


def cmd_creds(a, env):
    import creds
    if a.schema:
        return creds.schema(env, a.target, a.schema)
    if a.apply:
        return creds.apply(Path(a.flow), env.catalog(), env, a.target)
    return creds.report(load_json(a.flow), env.catalog(), env)


def cmd_api(a, env):
    import n8napi
    return n8napi.dispatch(a, env)


def cmd_convert(a, env):
    import convert
    files = convert.convert(load_json(a.flow), a.to, Path(a.output), env)
    for f in files:
        print("wrote", f)
    return 0


def cmd_doctor(a, env):
    print(f"n8n dir : {env.dir or '— not installed (bash scripts/setup_n8n.sh)'}")
    print(f"node    : {env.node or '—'} (v{env.node_version() or '?'})")
    if env.ok:
        print(f"n8n     : {env.version}")
        cat = env.catalog()
        print(f"catalog : {len(cat)} node types")
        defs = env.dir / "node-defs" / ".autokit-version"
        print(f"schemas : {'ready' if defs.exists() else 'generated on first validate'}")
    import shutil
    print(f"graphviz: {shutil.which('dot') or '— (diagrams fall back to HTML/Mermaid; brew install graphviz)'}")
    print(f"docker  : {shutil.which('docker') or '—'}")
    tg = env.cfg.get("targets") or {}
    shown = ", ".join(k + "=" + str(v.get("url")) for k, v in tg.items()) or "local=http://localhost:5678 (default)"
    print(f"targets : {shown}")
    env.ensure_secrets_template()
    sec = env.secrets()
    keys = [k for k, v in (sec.get('n8n_api_keys') or {}).items() if v]
    print(f"secrets : {env.secrets_path} — API keys set for: {', '.join(keys) or 'none'}; credentials: {len(sec.get('credentials') or {})}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="autokit", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor")
    p = sub.add_parser("nodes"); p.add_argument("words", nargs="+"); p.add_argument("--limit", type=int, default=15)
    p = sub.add_parser("node"); p.add_argument("type"); p.add_argument("--version"); p.add_argument("--ts", action="store_true"); p.add_argument("--filter")
    p = sub.add_parser("guide"); p.add_argument("topic", nargs="?")
    p = sub.add_parser("new"); p.add_argument("pattern"); p.add_argument("-o", "--output")
    p = sub.add_parser("build"); p.add_argument("src"); p.add_argument("-o", "--output"); p.add_argument("--relayout", action="store_true"); p.add_argument("--no-validate", action="store_true")
    p = sub.add_parser("validate"); p.add_argument("flow"); p.add_argument("--lenient", action="store_true"); p.add_argument("--json", action="store_true"); p.add_argument("--no-sdk", action="store_true")
    p = sub.add_parser("test"); p.add_argument("flow"); p.add_argument("cases"); p.add_argument("--keep", action="store_true"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("diagram"); p.add_argument("src"); p.add_argument("-o", "--output", default="diagram"); p.add_argument("--formats", default="svg,png,pdf,html,mmd,excalidraw"); p.add_argument("--title")
    p = sub.add_parser("creds"); p.add_argument("flow", nargs="?"); p.add_argument("--apply", action="store_true"); p.add_argument("--target", default="local"); p.add_argument("--schema", metavar="TYPE")
    p = sub.add_parser("deploy"); p.add_argument("flow"); p.add_argument("--target", default="local"); p.add_argument("--activate", action="store_true"); p.add_argument("--id")
    p = sub.add_parser("pull"); p.add_argument("--target", default="local"); p.add_argument("--id", required=True); p.add_argument("-o", "--output", required=True)
    p = sub.add_parser("list"); p.add_argument("--target", default="local")
    for c in ("activate", "deactivate"):
        p = sub.add_parser(c); p.add_argument("--target", default="local"); p.add_argument("--id", required=True)
    p = sub.add_parser("trigger"); p.add_argument("--target", default="local"); p.add_argument("--path", required=True); p.add_argument("--data", default="{}"); p.add_argument("--method", default="POST"); p.add_argument("--test", action="store_true"); p.add_argument("--wait", type=float, default=2.0); p.add_argument("--header", "-H", action="append", default=[], help="Name: value (repeatable)")
    p = sub.add_parser("executions"); p.add_argument("--target", default="local"); p.add_argument("--id"); p.add_argument("--limit", type=int, default=5)
    p = sub.add_parser("convert"); p.add_argument("flow"); p.add_argument("--to", required=True); p.add_argument("-o", "--output", default="converted")
    a = ap.parse_args(argv)
    env = Env()
    fn = {"doctor": cmd_doctor, "nodes": cmd_nodes, "node": cmd_node, "guide": cmd_guide, "new": cmd_new, "build": cmd_build,
          "validate": cmd_validate, "test": cmd_test, "diagram": cmd_diagram, "creds": cmd_creds, "convert": cmd_convert,
          "deploy": cmd_api, "pull": cmd_api, "list": cmd_api, "trigger": cmd_api, "executions": cmd_api, "activate": cmd_api, "deactivate": cmd_api}[a.cmd]
    if a.cmd in ("nodes", "node", "build", "validate", "test", "creds") and not env.ok and a.cmd != "build":
        env.require()
    return fn(a, env) or 0


if __name__ == "__main__":
    sys.exit(main())
