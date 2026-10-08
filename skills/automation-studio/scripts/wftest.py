"""Run an n8n workflow for real in a throw-away local n8n (no account, no server, no credentials needed)
and check what every node produced.

How: each test case gets a sandbox copy of the workflow where
  * the trigger is replaced by Manual Trigger → a Code node with the SAME NAME that emits the case's
    trigger items (so $json and $('Trigger name') still work),
  * nodes that need credentials or reach outside (app nodes, AI agents/chains, sub-workflow calls,
    Wait, Respond to Webhook …) are replaced by Code nodes with the same name that return the case's
    mock output (or pass their input through),
  * HTTP Request without credentials runs LIVE unless mocked (`"mock_http": true` or a mock given),
  * everything else (IF, Switch, Set, Code, Merge, Loop, Split Out, Aggregate, Filter, Sort, Date &
    Time, Crypto, XML, HTML, Markdown, Remove Duplicates …) runs for real.
Then `n8n execute` runs it and the run data of every node is checked against the case's `expect`.

cases.json:
{"cases": [{
   "name": "valid lead",
   "trigger": {"body": {"email": "a@b.co"}},                 // object, list of objects, or [{"json": …}]
   "mocks": {"Send email": [{"id": "msg_1"}], "Ask AI": [{"output": "positive"}]},
   "passthrough": ["Wait 1h"],                               // mocked nodes that just pass items on
   "live": ["Get weather"],                                  // force a credential-less node to run live
   "mock_http": false,
   "env": {"API_BASE": "https://example.com"},
   "runs": 2,                                                // run N times in the same sandbox, check the last
                                                             // (proves dedupe / idempotency / static data)
   "expect": {
     "status": "success",                                    // or "error"
     "nodes": {"Mark valid": {"items": 1, "json": {"status": "valid"}},   // json = subset match on item 0
               "Reject": {"ran": false},
               "Route": {"output": 1, "items": 2},               // items on a specific output index
               "Summary": {"contains": "3 leads"}}               // text anywhere in the node output
   }}]}
"""
from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import uuid
from pathlib import Path

from wfcheck import is_trigger

ALWAYS_MOCK_SUFFIX = ("agent", "chainLlm", "chainRetrievalQa", "chainSummarization", "informationExtractor", "textClassifier",
                      "sentimentAnalysis", "openAi", "anthropic", "googleGemini", "ollama", "mistralAi", "groq", "perplexity")
ALWAYS_MOCK_TYPES = {"n8n-nodes-base.executeWorkflow", "n8n-nodes-base.wait", "n8n-nodes-base.respondToWebhook",
                     "n8n-nodes-base.emailSend", "n8n-nodes-base.sendEmail", "n8n-nodes-base.ssh", "n8n-nodes-base.ftp",
                     "n8n-nodes-base.executeCommand", "n8n-nodes-base.readWriteFile", "n8n-nodes-base.form",
                     "n8n-nodes-base.dataTable", "n8n-nodes-base.n8n"}
AI_PORTS_PREFIX = "ai_"
RESPONSE_SUFFIX = " ⟶ response"


def _items(v):
    if v is None:
        return [{"json": {}}]
    if isinstance(v, dict):
        v = [v]
    out = []
    for x in v:
        out.append(x if isinstance(x, dict) and set(x.keys()) <= {"json", "binary", "pairedItem"} and "json" in x else {"json": x})
    return out


def _code_node(name, pos, js):
    return {"parameters": {"jsCode": js}, "id": str(uuid.uuid4()), "name": name, "type": "n8n-nodes-base.code",
            "typeVersion": 2, "position": pos or [0, 0]}


def _respond_as_set(n: dict) -> dict:
    p = n.get("parameters") or {}
    kind = p.get("respondWith", "firstIncomingItem")
    status = (p.get("options") or {}).get("responseCode", 200)
    a = [{"id": "st", "name": "status", "value": status, "type": "number"}]
    if kind == "json":
        body = p.get("responseBody", "")
        a.append({"id": "rb", "name": "response", "value": body if isinstance(body, str) else json.dumps(body),
                  "type": "object"})
    elif kind == "text":
        a.append({"id": "rb", "name": "response", "value": p.get("responseBody", ""), "type": "string"})
    elif kind == "redirect":
        a.append({"id": "rb", "name": "redirect", "value": p.get("redirectURL", ""), "type": "string"})
    else:
        a.append({"id": "rb", "name": "response", "value": "={{ $json }}", "type": "object"})
    return {"parameters": {"mode": "manual", "assignments": {"assignments": a}, "options": {}}, "id": str(uuid.uuid4()),
            "name": n["name"], "type": "n8n-nodes-base.set", "typeVersion": 3.4, "position": n.get("position", [0, 0])}


def sandbox_copy(wf: dict, case: dict, cat: dict) -> tuple[dict, dict]:
    """Return (sandbox workflow, report of what was mocked)."""
    wf = json.loads(json.dumps(wf))
    nodes = wf.get("nodes", [])
    conns = wf.setdefault("connections", {})
    mocks = case.get("mocks") or {}
    passthrough = set(case.get("passthrough") or [])
    live = set(case.get("live") or [])
    mock_http = case.get("mock_http", False)
    report = {"trigger": None, "mocked": [], "passthrough": [], "removed_subnodes": [], "live_http": []}
    by_name = {n["name"]: n for n in nodes}
    # incoming AI sub-node map
    ai_children = {}
    for src, ports in conns.items():
        for ptype, outs in ports.items():
            if ptype.startswith(AI_PORTS_PREFIX):
                for targets in outs or []:
                    for t in targets or []:
                        ai_children.setdefault(t["node"], []).append(src)
    triggers = [n for n in nodes if n.get("type") != "n8n-nodes-base.stickyNote" and is_trigger(n["type"], cat)]
    triggers.sort(key=lambda n: n["type"] == "n8n-nodes-base.errorTrigger")   # error trigger only if nothing else
    chosen = case.get("trigger_node") or (triggers[0]["name"] if triggers else None)
    new_nodes = []
    removed = set()
    mocked_roots = set()
    responders = []
    for n in nodes:
        nm, t = n["name"], n["type"]
        if t == "n8n-nodes-base.stickyNote":
            continue
        meta = cat.get(t) or {}
        if nm == chosen:
            items = _items(case.get("trigger", case.get("input")))
            new_nodes.append(_code_node(nm, n.get("position"), f"return {json.dumps(items)};"))
            report["trigger"] = nm
            continue
        if n in triggers and nm != chosen:
            removed.add(nm)
            continue
        is_ai_sub = any(ptype.startswith(AI_PORTS_PREFIX) for ptype in conns.get(nm, {}))
        if is_ai_sub:
            continue  # decided after roots
        needs_cred = bool(meta.get("credentials")) and (bool(n.get("credentials")) or t not in (
            "n8n-nodes-base.httpRequest", "n8n-nodes-base.webhook", "n8n-nodes-base.respondToWebhook"))
        is_http = t == "n8n-nodes-base.httpRequest"
        http_needs_auth = is_http and (n.get("parameters") or {}).get("authentication", "none") != "none"
        should_mock = (nm in mocks or nm in passthrough or t in ALWAYS_MOCK_TYPES or t.split(".")[-1] in ALWAYS_MOCK_SUFFIX
                       or t.startswith("@n8n/n8n-nodes-langchain.") or (needs_cred and not is_http) or http_needs_auth
                       or (is_http and mock_http))
        if nm in live:
            should_mock = False
        if should_mock and t == "n8n-nodes-base.respondToWebhook" and nm not in mocks:
            # like the real node: pass items on unchanged; a sibling Set node fed by the same parents
            # computes the exact status + body, which the test merges into this node's result
            new_nodes.append(_code_node(nm, n.get("position"), "return $input.all();"))
            cap = _respond_as_set(n)
            cap["name"] = nm + RESPONSE_SUFFIX
            cap["position"] = [(n.get("position") or [0, 0])[0], (n.get("position") or [0, 0])[1] + 160]
            new_nodes.append(cap)
            responders.append(nm)
            report["passthrough"].append(nm + " (response captured)")
            continue
        if should_mock:
            if nm in mocks:
                js = f"return {json.dumps(_items(mocks[nm]))};"
                report["mocked"].append(nm)
            else:
                js = "return $input.all();"
                report["passthrough"].append(nm)
            if t.startswith("@n8n/n8n-nodes-langchain."):
                mocked_roots.add(nm)
            new_nodes.append(_code_node(nm, n.get("position"), js))
        else:
            if is_http:
                report["live_http"].append(nm)
            new_nodes.append(n)
    # AI sub-nodes: keep only if their root is still real
    for n in nodes:
        nm = n["name"]
        if any(ptype.startswith(AI_PORTS_PREFIX) for ptype in conns.get(nm, {})):
            roots = [t["node"] for ptype, outs in conns.get(nm, {}).items() for targets in outs or [] for t in targets or []]
            if all(r in mocked_roots or r in removed for r in roots):
                removed.add(nm)
                report["removed_subnodes"].append(nm)
            else:
                new_nodes.append(n)
    new_conns = {}
    for src, ports in conns.items():
        if src in removed:
            continue
        keep = {}
        for ptype, outs in ports.items():
            if ptype.startswith(AI_PORTS_PREFIX) and src in report["removed_subnodes"]:
                continue
            keep[ptype] = [[t for t in (targets or []) if t["node"] not in removed] for targets in outs or []]
        new_conns[src] = keep
    for r in responders:                       # wire the response-capture siblings
        for src, ports in list(new_conns.items()):
            for outs in ports.get("main") or []:
                for tg in list(outs or []):
                    if tg["node"] == r:
                        outs.append({"node": r + RESPONSE_SUFFIX, "type": "main", "index": tg.get("index", 0)})
    # mocked nodes have one output: fold multi-output connections of mocked nodes onto output 0
    mocked_names = set(report["mocked"]) | set(report["passthrough"])
    for src in list(new_conns):
        if src in mocked_names and "main" in new_conns[src] and len(new_conns[src]["main"]) > 1:
            pick = int((case.get("mock_output") or {}).get(src, 0))
            outs = new_conns[src]["main"]
            new_conns[src]["main"] = [outs[pick] if pick < len(outs) else []]
    start = "__autokit_start__"
    new_nodes.insert(0, {"parameters": {}, "id": str(uuid.uuid4()), "name": start, "type": "n8n-nodes-base.manualTrigger",
                         "typeVersion": 1, "position": [-400, 0]})
    if chosen:
        new_conns[start] = {"main": [[{"node": chosen, "type": "main", "index": 0}]]}
    wf["nodes"] = new_nodes
    wf["connections"] = new_conns
    wf.pop("pinData", None)
    wf["active"] = False
    wf.setdefault("settings", {})["executionOrder"] = "v1"
    return wf, report


def run_case(env, wf: dict, case: dict, cat: dict, work: Path, idx: int) -> dict:
    sb, rep = sandbox_copy(wf, case, cat)
    wid = f"autokitTest{idx:04d}{uuid.uuid4().hex[:4]}"
    sb["id"] = wid
    sb["name"] = f"[test] {wf.get('name', 'workflow')} — {case.get('name', idx)}"
    f = work / f"case{idx}.json"
    f.write_text(json.dumps(sb))
    uf = work / "n8n"
    r = env.n8n_cli("import:workflow", f"--input={f}", user_folder=uf, timeout=240)
    if r.returncode:
        return {"case": case.get("name", idx), "ok": False, "error": "import failed: " + (r.stderr or r.stdout)[-600:], "sandbox": rep}
    extra = {k: str(v) for k, v in (case.get("env") or {}).items()}
    for _ in range(max(1, int(case.get("runs", 1))) - 1):   # earlier runs (dedupe/idempotency state); last one is checked
        env.n8n_cli("execute", f"--id={wid}", "--rawOutput", user_folder=uf, timeout=int(case.get("timeout", 240)), extra_env=extra)
    r = env.n8n_cli("execute", f"--id={wid}", "--rawOutput", user_folder=uf, timeout=int(case.get("timeout", 240)), extra_env=extra)
    out = r.stdout
    i = out.find("{")
    try:
        data = json.loads(out[i:]) if i >= 0 else None
    except json.JSONDecodeError:
        j = out.rfind("\n{")
        try:
            data = json.loads(out[j + 1:]) if j >= 0 else None
        except Exception:
            data = None
    if not data:
        msg = (r.stderr + "\n" + r.stdout).strip()
        err = [l for l in msg.splitlines() if l.strip() and not l.startswith(("n8n Task Broker", "[license", "Failed to start Python", "    at ", "===="))]
        err = list(dict.fromkeys(err))               # the CLI prints the message several times
        text = "\n".join(err[-6:])[-1200:]
        ex = case.get("expect") or {}
        checks = [{"check": "status == " + ex.get("status", "success"), "ok": ex.get("status") == "error", "got": "error"}]
        for nm, e in (ex.get("nodes") or {}).items():   # node expectations that can be judged from the error text
            if "error" in e:
                checks.append({"check": f"{nm} errors with “{e['error']}”", "ok": e["error"] in msg, "got": text[:200]})
            elif e.get("ran") is False:
                checks.append({"check": f"{nm} did not run (run stopped by the error)", "ok": True, "got": None})
        return {"case": case.get("name", idx), "ok": all(c["ok"] for c in checks), "checks": checks,
                "status": "error", "error": text, "sandbox": rep, "nodes": {}}
    rd = (data.get("data") or {}).get("resultData") or {}
    nodes = {}
    for nm, runs in (rd.get("runData") or {}).items():
        if nm == "__autokit_start__":
            continue
        last = runs[-1]
        outs = ((last.get("data") or {}).get("main")) or []
        nodes[nm] = {"runs": len(runs), "outputs": [len(o or []) for o in outs],
                     "first": [((o or [{}])[0] or {}).get("json") if o else None for o in outs],
                     "all": [[it.get("json") for it in (o or [])][:50] for o in outs],
                     "error": (last.get("error") or {}).get("message"), "ms": last.get("executionTime")}
    for nm in [k for k in nodes if k.endswith(RESPONSE_SUFFIX)]:   # merge captured responses into their node
        cap = nodes.pop(nm)
        base = nodes.get(nm[: -len(RESPONSE_SUFFIX)])
        resp = (cap["first"] or [None])[0]
        if base is not None and resp is not None:
            base["response"] = resp
            base["first"] = [dict((base["first"] or [None])[0] or {}, **resp)] + list(base["first"][1:])
    status = data.get("status") or ("error" if rd.get("error") else "success")
    result = {"case": case.get("name", idx), "status": status, "sandbox": rep, "nodes": nodes,
              "error": (rd.get("error") or {}).get("message"), "last_node": rd.get("lastNodeExecuted")}
    result["checks"] = assertions(case.get("expect") or {}, result)
    result["ok"] = all(c["ok"] for c in result["checks"]) and (status == (case.get("expect") or {}).get("status", "success"))
    return result


def _subset(expected, actual) -> bool:
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(k in actual and _subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return isinstance(actual, list) and len(expected) <= len(actual) and all(_subset(e, a) for e, a in zip(expected, actual))
    return expected == actual or (isinstance(expected, (int, float)) and isinstance(actual, (int, float)) and abs(expected - actual) < 1e-9)


def assertions(expect: dict, res: dict) -> list[dict]:
    out = []
    st = expect.get("status", "success")
    out.append({"check": f"status == {st}", "ok": res["status"] == st, "got": res["status"] + (f" ({res.get('error')})" if res.get("error") else "")})
    for nm, ex in (expect.get("nodes") or {}).items():
        got = res["nodes"].get(nm)
        if ex.get("ran") is False:
            out.append({"check": f"{nm} did not run", "ok": got is None or sum(got["outputs"]) == 0, "got": got and got["outputs"]})
            continue
        if got is None:
            out.append({"check": f"{nm} ran", "ok": False, "got": "did not run"})
            continue
        oi = int(ex.get("output", 0))
        n_items = got["outputs"][oi] if oi < len(got["outputs"]) else 0
        if "items" in ex:
            out.append({"check": f"{nm} output {oi} has {ex['items']} item(s)", "ok": n_items == ex["items"], "got": n_items})
        if "min_items" in ex:
            out.append({"check": f"{nm} output {oi} has ≥ {ex['min_items']} item(s)", "ok": n_items >= ex["min_items"], "got": n_items})
        if "json" in ex:
            first = got["first"][oi] if oi < len(got["first"]) else None
            out.append({"check": f"{nm} item 0 ⊇ {json.dumps(ex['json'], ensure_ascii=False)[:80]}", "ok": _subset(ex["json"], first),
                        "got": json.dumps(first, ensure_ascii=False)[:200]})
        if "contains" in ex:
            blob = json.dumps(got["all"], ensure_ascii=False)
            out.append({"check": f"{nm} output contains “{ex['contains']}”", "ok": str(ex["contains"]) in blob, "got": blob[:160]})
        if "error" in ex:
            out.append({"check": f"{nm} errors with “{ex['error']}”", "ok": bool(got.get("error")) and ex["error"] in got["error"], "got": got.get("error")})
    return out


def run(env, wf: dict, cases: list[dict], cat: dict, keep=False) -> list[dict]:
    work = Path(tempfile.mkdtemp(prefix="autokit-test-"))
    try:
        out = []
        offline = os.environ.get("AUTOKIT_OFFLINE") == "1"
        for i, c in enumerate(cases):
            if offline and c.get("live"):
                out.append({"case": c.get("name", i), "ok": True, "status": "skipped", "skipped": True,
                            "sandbox": {"trigger": "—"}, "nodes": {}, "checks": []})
                continue
            out.append(run_case(env, wf, c, cat, work, i))
        return out
    finally:
        if not keep:
            shutil.rmtree(work, ignore_errors=True)
