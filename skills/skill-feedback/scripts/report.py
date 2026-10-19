#!/usr/bin/env python3
"""Send an anonymous, non-personal improvement report about a skill (stdlib only).

  report.py --skill social-media-manager --event gap --outcome partial \
            --tags missing-case,platform-rule-outdated \
            --gap "No case for a hijacked Telegram channel" \
            --suggestion "Add recovery steps to the telegram platform file"
  report.py --print-url ...   # print the GET URL (for agents that can only fetch a URL)
  report.py --dry-run ...     # show exactly what would be sent, send nothing
  report.py --status          # show install id, opt-out state, queued reports
  report.py --flush           # retry queued reports

What is sent: skill name, event kind, outcome, agent family, surface, OS family, skill version,
up to 5 tags from a fixed list, a short generic gap/suggestion (<=300/500 chars), a random install id.
Never sent: names, emails, handles, URLs, file paths, IPs, prompts, file contents, tokens.
Text is auto-redacted here and validated again by the server (which rejects, not stores, anything personal).
Opt out: AI_SKILLS_TELEMETRY=off, or DO_NOT_TRACK=1, or create ~/.config/ai-skills/telemetry-off
Never blocks a task: network failure queues the report locally and the exit code is 0.
"""
import argparse, json, os, platform, re, sys, time, uuid
from urllib import request, parse, error

HERE = os.path.dirname(os.path.abspath(__file__))
CONF_DIR = os.path.expanduser(os.environ.get("AI_SKILLS_CONFIG_DIR", "~/.config/ai-skills"))
OUTBOX = os.path.expanduser(os.environ.get("AI_SKILLS_OUTBOX", "~/.cache/ai-skills/outbox"))
EVENTS = ["gap", "failure", "wrong_info", "suggestion", "new_skill_request", "success_note"]
TAGS = ["platform-rule-outdated", "missing-platform", "missing-case", "script-bug", "unclear-instructions",
        "automation-gap", "language-dialect", "too-long", "tool-unavailable", "wrong-output", "missing-reference", "other"]
PII = [
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    re.compile(r"(^|\s)@[A-Za-z0-9_.]{2,}"),
    re.compile(r"(https?://|www\.)\S+", re.I),
    re.compile(r"\b[a-z0-9-]+\.(com|net|org|io|co|app|dev|ai|me|eg|sa|ae|info|xyz)\b", re.I),
    re.compile(r"[A-Za-z]:\\\S*|/Users/\S*|/home/\S*|/Volumes/\S*|~/\S*"),
    re.compile(r"\b\d{1,3}(\.\d{1,3}){3}\b"),
    re.compile(r"\b(?=[A-Za-z0-9_-]*\d)(?=[A-Za-z0-9_-]*[A-Za-z])[A-Za-z0-9_-]{24,}\b"),
    re.compile(r"\+?\d[\d\s().-]{7,}\d"),
    re.compile(r"\d{6,}"),
]


def disabled():
    v = os.environ.get("AI_SKILLS_TELEMETRY", "").strip().lower()
    return (v in ("off", "0", "false", "no", "disabled") or os.environ.get("DO_NOT_TRACK") == "1"
            or os.path.exists(os.path.join(CONF_DIR, "telemetry-off")))


def install_id():
    p = os.path.join(CONF_DIR, "install-id")
    try:
        v = open(p).read().strip()
        uuid.UUID(v)
        return v
    except Exception:
        pass
    v = str(uuid.uuid4())
    try:
        os.makedirs(CONF_DIR, exist_ok=True)
        open(p, "w").write(v + "\n")
    except Exception:
        pass
    return v


def detect_agent():
    e = os.environ
    if e.get("CLAUDECODE") or e.get("CLAUDE_CODE_ENTRYPOINT") or e.get("CLAUDE_CODE_REMOTE"): return "claude"
    if e.get("CURSOR_TRACE_ID") or e.get("CURSOR_AGENT"): return "cursor"
    if e.get("GEMINI_CLI") or e.get("GEMINI_API_KEY"): return "gemini"
    if e.get("WINDSURF") or e.get("CODEIUM_API_KEY"): return "windsurf"
    if e.get("CODEX_HOME") or e.get("CODEX_SANDBOX"): return "codex"
    return "other"


def os_family():
    return {"darwin": "macos", "windows": "windows", "linux": "linux"}.get(platform.system().lower(), "unknown")


def redact(s):
    if not s:
        return s
    for r in PII:
        s = r.sub(lambda m: (m.group(1) if m.groups() and m.group(1) is not None and m.group(1) in ("", " ", "\n") else "") + "[removed]", s)
    return re.sub(r"\s+", " ", s).strip()


def skill_version():
    try:
        import subprocess
        v = subprocess.run(["git", "-C", HERE, "rev-parse", "--short", "HEAD"], capture_output=True, text=True, timeout=3).stdout.strip()
        if re.fullmatch(r"[0-9a-f]{4,40}", v):
            return v
    except Exception:
        pass
    for rel in ("../../manifest.json", "../../../skills/manifest.json"):
        p = os.path.join(HERE, rel)
        try:
            m = json.load(open(p))
            return str(m.get("version") or m.get("generated") or "unknown")[:40].replace(" ", "-")
        except Exception:
            continue
    return "unknown"


def endpoint():
    if os.environ.get("AI_SKILLS_FEEDBACK_URL"):
        return os.environ["AI_SKILLS_FEEDBACK_URL"]
    return json.load(open(os.path.join(HERE, "..", "config.json")))["endpoint"]


def build(a):
    tags = [t for t in (a.tags.split(",") if a.tags else []) if t in TAGS][:5]
    p = {"install_id": install_id(), "skill": a.skill, "event": a.event, "agent": a.agent or detect_agent(),
         "surface": a.surface, "os": os_family(), "skill_version": skill_version(), "tags": tags}
    if a.outcome: p["outcome"] = a.outcome
    g, s = redact(a.gap)[:300] if a.gap else None, redact(a.suggestion)[:500] if a.suggestion else None
    if g: p["gap"] = g
    if s: p["suggestion"] = s
    return p


def post(p, timeout=6):
    req = request.Request(endpoint(), data=json.dumps(p).encode(), headers={"content-type": "application/json"}, method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read() or b"{}")
    except error.HTTPError as e:
        try: return e.code, json.loads(e.read() or b"{}")
        except Exception: return e.code, {}
    except Exception:
        return 0, {}


def queue(p):
    try:
        os.makedirs(OUTBOX, exist_ok=True)
        open(os.path.join(OUTBOX, "%d-%s.json" % (time.time() * 1000, uuid.uuid4().hex[:6])), "w").write(json.dumps(p))
    except Exception:
        pass


def flush(limit=10):
    n = 0
    try: files = sorted(os.listdir(OUTBOX))[:limit]
    except Exception: return 0
    for f in files:
        path = os.path.join(OUTBOX, f)
        try: p = json.load(open(path))
        except Exception:
            continue
        code, _ = post(p, 4)
        if code == 200 or 400 <= code < 500 and code != 429:   # delivered, or permanently rejected: drop
            try: os.rename(path, path + ".done")
            except Exception: pass
            n += 1
        elif code == 0:
            break
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skill"); ap.add_argument("--event", choices=EVENTS)
    ap.add_argument("--outcome", choices=["success", "partial", "failure"])
    ap.add_argument("--tags"); ap.add_argument("--gap"); ap.add_argument("--suggestion")
    ap.add_argument("--agent"); ap.add_argument("--surface", default="cli",
                    choices=["cli", "desktop", "web", "mobile", "ide", "api", "other"])
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--print-url", action="store_true")
    ap.add_argument("--status", action="store_true"); ap.add_argument("--flush", action="store_true")
    a = ap.parse_args()

    if a.status:
        q = len([f for f in os.listdir(OUTBOX) if f.endswith(".json")]) if os.path.isdir(OUTBOX) else 0
        print(json.dumps({"enabled": not disabled(), "install_id": install_id(), "queued": q, "endpoint": endpoint()}, indent=1))
        return 0
    if disabled():
        print("disabled (opt-out active); nothing sent"); return 0
    if a.flush:
        print("flushed", flush()); return 0
    if not (a.skill and a.event):
        ap.error("--skill and --event are required")
    p = build(a)
    if not (p.get("gap") or p.get("suggestion") or a.event == "success_note"):
        ap.error("give --gap or --suggestion")
    if a.dry_run:
        print(json.dumps(p, ensure_ascii=False, indent=1)); return 0
    if a.print_url:
        q = dict(p); q["tags"] = ",".join(q.get("tags", []))
        print(endpoint() + "?" + parse.urlencode(q)); return 0
    flush(3)
    code, body = post(p)
    if code == 200:
        print("sent" + (" (duplicate ignored)" if body.get("duplicate") else ""))
    elif code in (0, 429, 500, 502, 503, 504):
        queue(p); print("queued (will retry on next run)")
    else:
        print("rejected: %s" % body.get("error", code))   # not queued: it would be rejected again
    return 0


if __name__ == "__main__":
    sys.exit(main())
