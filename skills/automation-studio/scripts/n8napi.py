"""n8n public REST API client (n8n Cloud, self-hosted, local) — deploy, pull, list, trigger, executions,
credentials. Auth: header X-N8N-API-KEY from the secrets file / env (never printed).

The API key is created by the USER in n8n: Settings → n8n API → Create an API key (n8n Cloud: paid plans
only — NOT during the free trial; local and self-hosted: always). Put it in ~/.config/ai-skills/automation-secrets.json → n8n_api_keys.<target>.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

WRITABLE = ("name", "nodes", "connections", "settings", "staticData")
SETTINGS_OK = {"saveExecutionProgress", "saveManualExecutions", "saveDataErrorExecution", "saveDataSuccessExecution",
               "executionTimeout", "errorWorkflow", "timezone", "executionOrder", "callerPolicy", "callerIds",
               "timeSavedPerExecution", "availableInMCP"}


class Api:
    def __init__(self, target: dict):
        self.t = target
        if not target.get("key"):
            raise SystemExit(f"no API key for target '{target['name']}'. Create one in n8n (Settings → n8n API) and put it in "
                             f"the secrets file under n8n_api_keys.{target['name']} (autokit doctor shows the path).")

    def req(self, method, path, body=None, query=None, raw_url=None):
        url = raw_url or f"{self.t['url']}/api/v1{path}"
        if query:
            url += "?" + urllib.parse.urlencode({k: v for k, v in query.items() if v is not None})
        data = json.dumps(body).encode() if body is not None else None
        rq = urllib.request.Request(url, data=data, method=method, headers={
            "X-N8N-API-KEY": self.t["key"], "Accept": "application/json", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(rq, timeout=60) as r:
                txt = r.read().decode()
                return json.loads(txt) if txt else {}
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:600]
            raise SystemExit(f"{method} {path} → HTTP {e.code}: {msg}")
        except urllib.error.URLError as e:
            raise SystemExit(f"cannot reach {self.t['url']} ({e.reason}) — is n8n running? (local: bash scripts/setup_n8n.sh --start)")

    def all(self, path, query=None):
        out, cursor = [], None
        while True:
            q = dict(query or {}, limit=100, cursor=cursor)
            r = self.req("GET", path, query=q)
            out += r.get("data", [])
            cursor = r.get("nextCursor")
            if not cursor:
                return out


def clean_for_api(wf: dict) -> dict:
    body = {k: wf[k] for k in WRITABLE if k in wf}
    body["settings"] = {k: v for k, v in (wf.get("settings") or {}).items() if k in SETTINGS_OK}
    body["settings"].setdefault("executionOrder", "v1")
    for n in body.get("nodes", []):
        for k in ("notesInFlow",):
            pass
    return body


def resolve_workflow_refs(api, body):
    """Sub-workflow calls written as workflowId "name:<workflow name>" → the real id on this instance."""
    names = None
    for n in body.get("nodes", []):
        ref = (n.get("parameters") or {}).get("workflowId")
        val = ref.get("value") if isinstance(ref, dict) else ref
        if isinstance(val, str) and val.startswith("name:"):
            if names is None:
                names = {w.get("name"): w["id"] for w in api.all("/workflows")}
            target = val[5:].strip()
            if target not in names:
                raise SystemExit(f"“{n['name']}” calls sub-workflow “{target}”, which is not on {api.t['name']} — deploy it first.")
            n["parameters"]["workflowId"] = {"__rl": True, "mode": "list", "value": names[target], "cachedResultName": target}
            print(f"  linked “{n['name']}” → sub-workflow “{target}” ({names[target]})")


def deploy(env, a):
    api = Api(env.target(a.target))
    wf = json.loads(Path(a.flow).read_text())
    body = clean_for_api(wf)
    resolve_workflow_refs(api, body)
    wid = a.id
    if not wid:
        same = [w for w in api.all("/workflows") if w.get("name") == body["name"]]
        wid = same[0]["id"] if same else None
    if wid:
        r = api.req("PUT", f"/workflows/{wid}", body)
        print(f"updated workflow {wid} “{r.get('name')}” on {api.t['name']}")
    else:
        r = api.req("POST", "/workflows", body)
        wid = r["id"]
        print(f"created workflow {wid} “{r.get('name')}” on {api.t['name']}")
    if a.activate:
        try:
            api.req("POST", f"/workflows/{wid}/activate")
            print("activated ✓ (production webhooks/schedules are live)")
        except SystemExit as e:
            print(f"could not activate: {e}\n→ usually a missing credential or a trigger that needs setup; open it in n8n.")
    print(f"open: {api.t['url']}/workflow/{wid}")
    Path(a.flow).with_suffix(".deployed.json").write_text(json.dumps({"target": api.t["name"], "id": wid, "url": f"{api.t['url']}/workflow/{wid}"}))
    return 0


def pull(env, a):
    api = Api(env.target(a.target))
    wf = api.req("GET", f"/workflows/{a.id}")
    keep = {k: wf.get(k) for k in ("id", "name", "nodes", "connections", "settings", "staticData", "pinData", "tags") if k in wf}
    Path(a.output).write_text(json.dumps(keep, indent=2, ensure_ascii=False))
    print(f"pulled “{wf.get('name')}” ({len(wf.get('nodes', []))} nodes) → {a.output}")
    return 0


def list_wf(env, a):
    api = Api(env.target(a.target))
    for w in api.all("/workflows"):
        print(f"{w['id']}  {'● active' if w.get('active') else '○       '}  {w.get('name')}  ({len(w.get('nodes', []))} nodes, updated {w.get('updatedAt', '')[:16]})")
    return 0


def summarize_execution(ex: dict) -> str:
    lines = [f"execution {ex.get('id')} — {ex.get('status')} ({ex.get('mode')}) {ex.get('startedAt', '')[:19]}"]
    rd = ((ex.get("data") or {}).get("resultData") or {})
    for nm, runs in (rd.get("runData") or {}).items():
        last = runs[-1]
        outs = [len(o or []) for o in ((last.get("data") or {}).get("main") or [])]
        err = (last.get("error") or {}).get("message")
        first = None
        try:
            first = (last["data"]["main"][0] or [{}])[0].get("json")
        except Exception:
            pass
        lines.append(f"  · {nm}: out {outs}{'  ERROR ' + err if err else ''}  {json.dumps(first, ensure_ascii=False)[:120] if first else ''}")
    if rd.get("error"):
        lines.append(f"  ✗ {rd['error'].get('message')}")
    return "\n".join(lines)


def trigger(env, a):
    t = env.target(a.target)
    base = "webhook-test" if a.test else "webhook"
    url = f"{t['url']}/{base}/{a.path.lstrip('/')}"
    data = a.data
    if data.startswith("@"):
        data = Path(data[1:]).read_text()
    body = data.encode() if a.method.upper() not in ("GET", "HEAD") else None
    if a.method.upper() in ("GET", "HEAD") and data and data != "{}":
        url += "?" + urllib.parse.urlencode(json.loads(data))
    hdrs = {"Content-Type": "application/json"}
    for h in getattr(a, "header", None) or []:
        k, _, v = h.partition(":")
        hdrs[k.strip()] = v.strip()
    rq = urllib.request.Request(url, data=body, method=a.method.upper(), headers=hdrs)
    t0 = time.time()
    try:
        with urllib.request.urlopen(rq, timeout=120) as r:
            print(f"HTTP {r.status} in {time.time() - t0:.1f}s ← {url}\n{r.read().decode()[:2000]}")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} ← {url}\n{e.read().decode()[:2000]}")
    if a.test:
        print("(test URL: n8n must be listening — click 'Listen for test event' in the editor first)")
        return 0
    if t.get("key"):
        time.sleep(a.wait)
        api = Api(t)
        ex = api.req("GET", "/executions", query={"limit": 1, "includeData": "true"})
        if ex.get("data"):
            print(summarize_execution(ex["data"][0]))
    return 0


def executions(env, a):
    api = Api(env.target(a.target))
    r = api.req("GET", "/executions", query={"limit": a.limit, "workflowId": a.id, "includeData": "true"})
    for ex in r.get("data", []):
        print(summarize_execution(ex))
    return 0


def create_credential(env, target: str, name: str, ctype: str, data: dict) -> str:
    api = Api(env.target(target))
    r = api.req("POST", "/credentials", {"name": name, "type": ctype, "data": data})
    return r.get("id")


def credential_schema(env, target: str, ctype: str) -> dict:
    return Api(env.target(target)).req("GET", f"/credentials/schema/{ctype}")


def set_active(env, a):
    api = Api(env.target(a.target))
    r = api.req("POST", f"/workflows/{a.id}/{a.cmd}")
    print(f"{a.cmd}d “{r.get('name')}” ({a.id}) on {api.t['name']}")
    return 0


def dispatch(a, env):
    return {"deploy": deploy, "pull": pull, "list": list_wf, "trigger": trigger, "executions": executions,
            "activate": set_active, "deactivate": set_active}[a.cmd](env, a)
