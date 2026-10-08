"""Static checks for an n8n workflow JSON — everything that can be caught BEFORE running it.

Layer 1 (our checks, need only the node catalog): known node types and versions, unique names,
connections to existing nodes, trigger rules, credentials each node needs, hard-coded secrets,
expression syntax ({{ }} balance, `=` prefix, references to existing nodes), Code-node JavaScript
syntax (node --check) and a return statement, Python Code nodes flagged, AI sub-node wiring
(every AI root has a chat model), webhook path collisions, settings, unreachable nodes.
Layer 2 (official n8n Workflow SDK from the installed n8n): graph validation + per-node parameter
schema validation for the exact node version (INVALID_PARAMETER = error unless --lenient).
"""
from __future__ import annotations

import json
import re
import subprocess
import tempfile
from pathlib import Path

AI_PORTS = {"ai_languageModel", "ai_memory", "ai_tool", "ai_outputParser", "ai_embedding", "ai_vectorStore",
            "ai_retriever", "ai_document", "ai_textSplitter", "ai_reranker"}
AI_ROOTS = {"agent", "chainLlm", "chainRetrievalQa", "informationExtractor", "textClassifier", "sentimentAnalysis", "agentTool"}
SECRET_RX = re.compile(r"(sk-[A-Za-z0-9_\-]{20,}|xox[abp]-[A-Za-z0-9\-]{10,}|ghp_[A-Za-z0-9]{30,}|AIza[0-9A-Za-z_\-]{30,}|"
                       r"Bearer\s+[A-Za-z0-9._\-]{20,}|eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{10,})")
TRIGGER_HINT = re.compile(r"(Trigger$|^webhook$|^cron$|^interval$)")
CRED_OPTIONAL = ("n8n-nodes-base.httpRequest", "n8n-nodes-base.webhook", "n8n-nodes-base.respondToWebhook",
                 "n8n-nodes-base.formTrigger", "n8n-nodes-base.wait", "n8n-nodes-base.form",
                 "@n8n/n8n-nodes-langchain.agent", "@n8n/n8n-nodes-langchain.chatTrigger", "@n8n/n8n-nodes-langchain.mcpTrigger",
                 "n8n-nodes-base.crypto")


def is_trigger(ntype: str, cat: dict) -> bool:
    info = cat.get(ntype) or {}
    if "trigger" in (info.get("group") or []):
        return True
    return bool(TRIGGER_HINT.search(ntype.split(".")[-1]))


def _walk_strings(obj, path=""):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from _walk_strings(v, f"{path}.{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _walk_strings(v, f"{path}[{i}]")


def check(wf: dict, cat: dict, env=None, *, sdk=True, lenient=False) -> dict:
    errors, warnings, info = [], [], []
    E, W = errors.append, warnings.append
    nodes = wf.get("nodes") or []
    conns = wf.get("connections") or {}
    result = {"errors": errors, "warnings": warnings, "info": info, "triggers": [], "credentials": {}}
    if not nodes:
        E("workflow has no nodes")
        return result
    names = [n.get("name") for n in nodes]
    by_name = {n.get("name"): n for n in nodes}
    for nm in sorted({x for x in names if names.count(x) > 1}):
        E(f"duplicate node name '{nm}' — names must be unique (connections and expressions use names)")
    needed_creds, triggers, webhook_paths = {}, [], {}
    for n in nodes:
        nm, t = n.get("name"), n.get("type", "")
        if not nm or not t:
            E(f"node without name/type: {json.dumps(n)[:80]}")
            continue
        if t == "n8n-nodes-base.stickyNote":
            continue
        meta = cat.get(t)
        if meta is None:
            E(f"'{nm}': unknown node type '{t}' in this n8n version (find the right one: autokit nodes \"…\")")
            continue
        tv = n.get("typeVersion")
        if tv is None:
            E(f"'{nm}': missing typeVersion (newest is {meta['defaultVersion']})")
        elif float(tv) not in [float(v) for v in meta["versions"]]:
            E(f"'{nm}': typeVersion {tv} does not exist for {t} (valid: {meta['versions']})")
        elif float(tv) < float(meta["defaultVersion"]):
            info.append(f"'{nm}': {t} v{tv} (newest v{meta['defaultVersion']}) — fine for existing flows, prefer newest for new ones")
        if "position" not in n:
            W(f"'{nm}': no position (autokit build lays the canvas out)")
        props = set(meta["props"].get(str(tv), meta["props"].get(str(meta["defaultVersion"]), [])))
        if props:
            for k in (n.get("parameters") or {}):
                if k not in props:
                    W(f"'{nm}': parameter '{k}' is not a field of {t} v{tv} — typo or wrong version?")
        params = n.get("parameters") or {}
        if meta["credentials"]:
            have = set((n.get("credentials") or {}).keys())
            optional = t in CRED_OPTIONAL
            if not have and (not optional or params.get("authentication") not in (None, "none")):
                needed_creds[nm] = meta["credentials"]
            for ctype, ref in (n.get("credentials") or {}).items():
                if not isinstance(ref, dict) or not ref.get("id"):
                    W(f"'{nm}': credential '{ctype}' has no id yet — create/select it in n8n (autokit creds) before running live")
        if is_trigger(t, cat):
            triggers.append(nm)
        if t.endswith(".webhook") or t.endswith(".formTrigger"):
            p = params.get("path")
            if p:
                key = (params.get("httpMethod", "GET"), p)
                if key in webhook_paths:
                    E(f"'{nm}' and '{webhook_paths[key]}' share webhook {key} — paths must be unique")
                webhook_paths[key] = nm
            if not n.get("webhookId"):
                W(f"'{nm}': no webhookId (autokit build adds one; needed for production URLs)")
        if t == "n8n-nodes-base.code":
            lang = params.get("language", "javaScript")
            code = params.get("jsCode") if lang == "javaScript" else params.get("pythonCode")
            if lang != "javaScript":
                W(f"'{nm}': Python Code node — needs the Python task runner (n8n Cloud: yes; self-host: external runner)")
            elif code and env is not None and env.node:
                err = js_syntax(code, env.node)
                if err:
                    E(f"'{nm}': JavaScript syntax error — {err}")
                if not re.search(r"\breturn\b", code):
                    E(f"'{nm}': Code node never returns — it must return items (e.g. return $input.all();)")
        for path, s in _walk_strings(params):
            if SECRET_RX.search(s):
                E(f"'{nm}': looks like a hard-coded secret in parameters.{path} — use an n8n credential instead")
            if t == "n8n-nodes-base.code" and path in ("jsCode", "pythonCode"):
                continue
            if "{{" in s or "}}" in s:
                if s.count("{{") != s.count("}}"):
                    E(f"'{nm}': unbalanced {{{{ }}}} in parameters.{path}: {s[:70]}")
                elif not s.startswith("="):
                    W(f"'{nm}': parameters.{path} has {{{{ }}}} but does not start with '=' — n8n will treat it as plain text")
            for ref in re.findall(r"\$\(\s*['\"]([^'\"]+)['\"]\s*\)", s) + re.findall(r"\$node\[['\"]([^'\"]+)['\"]\]", s):
                if ref not in by_name:
                    E(f"'{nm}': expression references node '{ref}' which does not exist")
    # connections
    incoming = {nm: [] for nm in names}
    for src, ports in conns.items():
        if src not in by_name:
            E(f"connection from unknown node '{src}'")
            continue
        for ptype, outs in ports.items():
            for oi, targets in enumerate(outs or []):
                for tgt in targets or []:
                    tn = tgt.get("node")
                    if tn not in by_name:
                        E(f"'{src}' output {oi} connects to unknown node '{tn}'")
                        continue
                    incoming[tn].append((src, ptype))
    for nm, n in by_name.items():
        if n.get("type") == "n8n-nodes-base.stickyNote" or nm in triggers:
            continue
        if not incoming.get(nm) and not any(k in AI_PORTS for k in conns.get(nm, {})):
            W(f"'{nm}' has no input connection — it will never run")
    for r in nodes:
        t = r.get("type", "")
        if t.startswith("@n8n/n8n-nodes-langchain.") and t.split(".")[-1] in AI_ROOTS:
            ports = {pt for _, pt in incoming.get(r["name"], [])}
            if "ai_languageModel" not in ports:
                E(f"'{r['name']}': AI node has no chat model connected (ai_languageModel)")
    if not triggers:
        W("no trigger node — the workflow only runs when called (Execute Workflow) or by hand")
    st = wf.get("settings") or {}
    if st.get("executionOrder") != "v1":
        W("settings.executionOrder should be 'v1' — autokit build sets it")
    if not st.get("errorWorkflow") and len(nodes) > 6:
        info.append("no error workflow set — production flows should report failures (pattern: error-alerts)")
    for nm, creds in needed_creds.items():
        info.append(f"'{nm}' needs a credential: {' or '.join(creds)}")
    if sdk and env is not None and env.ok:
        res = sdk_validate(wf, env)
        for x in res.get("errors", []):
            E(f"[n8n SDK] {(x.get('node') or '')}: {x['message']}")
        for x in res.get("warnings", []):
            if x.get("severity") == "informational":
                continue
            (W if (lenient or x.get("code") != "INVALID_PARAMETER") else E)(f"[n8n SDK] {x['message']}")
    result["triggers"] = triggers
    result["credentials"] = needed_creds
    return result


def js_syntax(code: str, node: str) -> str | None:
    wrapped = ("async function __n8n_code__($input, $json, $items, $node, $workflow, $execution, $env, $now, $today, "
               "$jmespath, $, $vars, $prevNode, $runIndex, $item, $binary, $parameter, $position, $data){\n" + code + "\n}")
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(wrapped)
        p = f.name
    r = subprocess.run([node, "--check", p], capture_output=True, text=True)
    Path(p).unlink(missing_ok=True)
    if r.returncode:
        lines = [l for l in r.stderr.splitlines() if "Error" in l]
        return (lines[0] if lines else r.stderr.strip().splitlines()[-1])[:200]
    return None


def sdk_validate(wf: dict, env) -> dict:
    env.ensure_defs()
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(wf, f)
        p = f.name
    r = env.js("sdk_validate.js", p, timeout=180)
    Path(p).unlink(missing_ok=True)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"errors": [], "warnings": [{"code": "SDK", "message": "SDK validation unavailable: " + (r.stderr or r.stdout)[-300:]}]}
