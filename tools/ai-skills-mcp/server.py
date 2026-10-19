#!/usr/bin/env python3
"""ai-skills MCP server — one connection gives any MCP client every skill in the library.

Reads straight from the skills/ folder of this repo (no copies). Exposes three tools:
  list_skills()                  name + description of every installed skill
  get_skill(name)                full SKILL.md of one skill
  read_skill_file(name, path)    any file inside a skill folder (references, scripts, examples)

Stdlib only. Speaks MCP over stdio (newline-delimited JSON-RPC 2.0).
Set AI_SKILLS_ROOT to point at another skills folder (default: ../../skills from this file).
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("AI_SKILLS_ROOT") or Path(__file__).resolve().parents[2] / "skills").resolve()
PROTOCOL = "2024-11-05"
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
MAX_FILE = 300_000


def known_skills():
    """Skill folders = folders under ROOT that contain SKILL.md."""
    if not ROOT.is_dir():
        return {}
    return {d.name: d for d in sorted(ROOT.iterdir()) if d.is_dir() and (d / "SKILL.md").is_file()}


def describe(name, folder):
    """Full description from manifest.json when present (multi-line safe), else the frontmatter line."""
    manifest = ROOT / "manifest.json"
    if manifest.is_file():
        try:
            for s in json.loads(manifest.read_text(encoding="utf-8")).get("skills", []):
                if s.get("name") == name:
                    return s.get("description", "")
        except Exception:
            pass
    text = (folder / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^description:\s*(.+)$", text, re.M)
    return m.group(1).strip().strip('"') if m else ""


def tool_list_skills(_args):
    rows = [{"name": n, "description": describe(n, f)} for n, f in known_skills().items()]
    return json.dumps(rows, ensure_ascii=False, indent=2)


def tool_get_skill(args):
    name = args.get("name", "")
    skills = known_skills()
    if not NAME_RE.match(name) or name not in skills:
        raise ValueError(f"unknown skill: {name!r}. Call list_skills first.")
    return (skills[name] / "SKILL.md").read_text(encoding="utf-8", errors="replace")


def tool_read_skill_file(args):
    name, rel = args.get("name", ""), args.get("path", "")
    skills = known_skills()
    if not NAME_RE.match(name) or name not in skills:
        raise ValueError(f"unknown skill: {name!r}")
    base = skills[name].resolve()
    target = (base / rel).resolve()
    if base != target and base not in target.parents:
        raise ValueError("path escapes the skill folder")
    if not target.is_file():
        raise ValueError(f"no such file in {name}: {rel}")
    if target.stat().st_size > MAX_FILE:
        raise ValueError(f"file too large (> {MAX_FILE} bytes)")
    return target.read_text(encoding="utf-8", errors="replace")


TOOLS = {
    "list_skills": (tool_list_skills, {"type": "object", "properties": {}}),
    "get_skill": (tool_get_skill, {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    "read_skill_file": (tool_read_skill_file, {"type": "object", "properties": {
        "name": {"type": "string"}, "path": {"type": "string", "description": "path inside the skill folder, e.g. references/x.md"}},
        "required": ["name", "path"]}),
}


def reply(msg_id, result=None, error=None):
    out = {"jsonrpc": "2.0", "id": msg_id}
    if error is not None:
        out["error"] = error
    else:
        out["result"] = result
    sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def handle(msg):
    method, mid, params = msg.get("method"), msg.get("id"), msg.get("params") or {}
    if method is None or mid is None:          # notifications (e.g. notifications/initialized) get no reply
        return
    if method == "initialize":
        return reply(mid, {"protocolVersion": PROTOCOL, "capabilities": {"tools": {}},
                           "serverInfo": {"name": "ai-skills", "version": "1.0.0"}})
    if method == "ping":
        return reply(mid, {})
    if method == "tools/list":
        return reply(mid, {"tools": [{"name": n, "description": (fn.__doc__ or n), "inputSchema": schema}
                                     for n, (fn, schema) in TOOLS.items()]})
    if method == "tools/call":
        name = params.get("name")
        if name not in TOOLS:
            return reply(mid, error={"code": -32602, "message": f"unknown tool {name}"})
        try:
            text = TOOLS[name][0](params.get("arguments") or {})
            return reply(mid, {"content": [{"type": "text", "text": text}], "isError": False})
        except Exception as e:
            return reply(mid, {"content": [{"type": "text", "text": str(e)}], "isError": True})
    return reply(mid, error={"code": -32601, "message": f"method not found: {method}"})


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            handle(json.loads(line))
        except Exception as e:
            sys.stderr.write(f"ai-skills-mcp: {e}\n")


if __name__ == "__main__":
    main()
