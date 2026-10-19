#!/usr/bin/env python3
"""ai-skills MCP server — one connection gives any MCP client every skill in the library.

Reads straight from the skills/ folder of this repo (no copies). Exposes four tools:
  list_skills()                  name + description of every installed skill
  get_skill(name)                full SKILL.md of one skill
  read_skill_file(name, path)    any file inside a skill folder (references, scripts, examples)
  report_skill_gap(...)          anonymous non-personal improvement report (see skills/skill-feedback)

Stdlib only. Speaks MCP over stdio (newline-delimited JSON-RPC 2.0).
Set AI_SKILLS_ROOT to point at another skills folder (default: ../../skills from this file).

GitHub is the source every client reads: when this file lives in a git clone of the repo, each
tool call first fast-forwards that clone from origin (at most once a minute, silently, never blocking
on failure), so every agent always sees the latest pushed skills. Set AI_SKILLS_NO_SYNC=1 to disable.
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(os.environ.get("AI_SKILLS_ROOT") or Path(__file__).resolve().parents[2] / "skills").resolve()
PROTOCOL = "2024-11-05"
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
MAX_FILE = 300_000
REPO = Path(__file__).resolve().parents[2]
SYNC_EVERY = 60  # seconds between GitHub pulls
_last_sync = 0.0


def sync_from_github():
    """Fast-forward the clone from origin, at most once per SYNC_EVERY seconds. Never raises."""
    global _last_sync
    if os.environ.get("AI_SKILLS_NO_SYNC") or not (REPO / ".git").exists():
        return
    now = time.time()
    if now - _last_sync < SYNC_EVERY:
        return
    _last_sync = now
    try:
        subprocess.run(["git", "-C", str(REPO), "pull", "--ff-only", "--quiet"],
                       timeout=15, capture_output=True)
    except Exception:
        pass


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
    """List every skill in Joshua's library with its description. Call first to choose a skill."""
    rows = [{"name": n, "description": describe(n, f)} for n, f in known_skills().items()]
    return json.dumps(rows, ensure_ascii=False, indent=2)


def tool_get_skill(args):
    """Return the full SKILL.md of one skill (name from list_skills)."""
    name = args.get("name", "")
    skills = known_skills()
    if not NAME_RE.match(name) or name not in skills:
        raise ValueError(f"unknown skill: {name!r}. Call list_skills first.")
    return (skills[name] / "SKILL.md").read_text(encoding="utf-8", errors="replace")


def tool_read_skill_file(args):
    """Read a file inside a skill folder (references/, scripts/, templates/, data/)."""
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


def tool_report_skill_gap(args):
    """Send an anonymous, non-personal improvement report when a skill missed something, was wrong or outdated, or a task needed something it lacks. Fields are fixed enums plus a short GENERIC text (no names, emails, links, paths, prompts or file contents). Opt-out: AI_SKILLS_TELEMETRY=off. Never blocks the task."""
    name = args.get("skill", "")
    if not NAME_RE.match(name):
        raise ValueError("skill must be a skill folder name")
    script = ROOT / "skill-feedback" / "scripts" / "report.py"
    if not script.is_file():
        raise ValueError("skill-feedback is not installed in this library")
    cmd = [sys.executable, str(script), "--skill", name, "--event", args.get("event", "gap"),
           "--surface", args.get("surface", "cli"), "--agent", args.get("agent", "other")]
    for flag in ("outcome", "tags", "gap", "suggestion"):
        if args.get(flag):
            cmd += ["--" + flag, str(args[flag])]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    return (r.stdout or r.stderr).strip() or "done"


TOOLS = {
    "list_skills": (tool_list_skills, {"type": "object", "properties": {}}),
    "get_skill": (tool_get_skill, {"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
    "read_skill_file": (tool_read_skill_file, {"type": "object", "properties": {
        "name": {"type": "string"}, "path": {"type": "string", "description": "path inside the skill folder, e.g. references/x.md"}},
        "required": ["name", "path"]}),
    "report_skill_gap": (tool_report_skill_gap, {"type": "object", "properties": {
        "skill": {"type": "string", "description": "skill folder name the report is about"},
        "event": {"type": "string", "enum": ["gap", "failure", "wrong_info", "suggestion", "new_skill_request", "success_note"]},
        "outcome": {"type": "string", "enum": ["success", "partial", "failure"]},
        "tags": {"type": "string", "description": "comma list from: platform-rule-outdated, missing-platform, missing-case, script-bug, unclear-instructions, automation-gap, language-dialect, too-long, tool-unavailable, wrong-output, missing-reference, other"},
        "gap": {"type": "string", "description": "what was missing or wrong, generic, <=300 chars"},
        "suggestion": {"type": "string", "description": "what to add or change, generic, <=500 chars"},
        "agent": {"type": "string", "enum": ["claude", "cursor", "gemini", "antigravity", "windsurf", "chatgpt", "codex", "copilot", "other"]},
        "surface": {"type": "string", "enum": ["cli", "desktop", "web", "mobile", "ide", "api", "other"]}},
        "required": ["skill", "event"]}),
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
        sync_from_github()
        return reply(mid, {"tools": [{"name": n, "description": (fn.__doc__ or n), "inputSchema": schema}
                                     for n, (fn, schema) in TOOLS.items()]})
    if method == "tools/call":
        sync_from_github()
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
