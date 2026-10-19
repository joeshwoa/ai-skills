#!/usr/bin/env python3
"""nx — n8n + browser-agent toolkit.  bash nx.sh <command> …

  doctor                         what is installed / running (python, playwright, chrome, n8n, browserd, secrets)
  probe URL                      look at a site: API? feeds? SPA? login? captcha/bot-protection?  (read-only)
  ladder [--url U|--probe F] …   rank the ways to automate it (official node/API → hidden JSON → recipe → agent → human)
  start|stop|status              run browserd (the local browser worker n8n calls) in the background
  login URL --session NAME       you sign in once in a visible Chrome window; the session is kept for recipes
  chrome                         how to start your real Chrome for attach mode (CDP) on a separate profile
  recipe list|validate F|run F|new TEMPLATE -o F     browser recipes (JSON steps)
  new PATTERN -o DIR [--recipe NAME --path P --session S --browserd URL]   scaffold an n8n flow (TypeScript) + test cases
  build|test|validate|deploy|creds|diagram …            → automation-studio's auto.sh (same engine, same checks)
  secret NAME                    store a website secret for {{secret:NAME}} (prompts; value never echoed or logged)
  selftest                       end-to-end proof: mock site → browserd → real n8n engine
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

def _real_home() -> Path:
    h = Path.home()
    parts = h.parts
    if ".gemini" in parts and "users" in parts:
        idx = parts.index(".gemini")
        return Path(*parts[:idx])
    return h


REAL_HOME = _real_home()
HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
AUTO = SKILL.parent / "automation-studio" / "scripts" / "auto.sh"
STATE = Path(os.environ.get("NX_STATE", REAL_HOME / ".local/share/ai-skills/browserd"))
SECRETS = Path(os.environ.get("NX_SECRETS", REAL_HOME / ".config/ai-skills/automation-secrets.json"))
PORT = int(os.environ.get("NX_PORT", "7788"))
PATTERNS = {"recipe": "01-browser-recipe", "agent": "02-agent-browser-tools", "mcp": "03-mcp-bridge"}


def sh(cmd, **kw):
    return subprocess.run(cmd, **kw)


def health(port=PORT):
    try:
        return json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=2))
    except Exception:
        return None


def cmd_doctor(a):
    print("n8n-agent-studio doctor")
    ok = True

    def line(name, good, detail=""):
        nonlocal ok
        print(f"  {'✓' if good else '✗'} {name:<22}{detail}")
        ok = ok and good
    line("python", sys.version_info >= (3, 9), sys.version.split()[0])
    try:
        import playwright  # noqa
        line("playwright", True, getattr(playwright, "__version__", ""))
    except Exception:
        line("playwright", False, "pip install playwright && python3 -m playwright install chromium")
    chrome = os.environ.get("NX_CHROME") or shutil.which("google-chrome") or shutil.which("chromium") or ""
    for p in ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]:
        if not chrome and Path(p).exists():
            chrome = p
    cache = list(Path.home().glob(".cache/ms-playwright/chromium-*")) + list(Path.home().glob("Library/Caches/ms-playwright/chromium-*")) + list(Path("/opt/pw-browsers").glob("chromium-*"))
    line("chrome/chromium", bool(chrome or cache), chrome or (str(cache[0]) if cache else "none → playwright install chromium, or NX_CHANNEL=chrome to use installed Chrome"))
    h = health()
    line("browserd", bool(h), f"running on :{PORT} sessions={h['sessions']} allow={h['allow']}" if h else f"not running → nx start --allow <domains>")
    r = sh(["bash", str(AUTO), "doctor"], capture_output=True, text=True)
    n8n = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith(("n8n ", "n8n:", "targets", "catalog"))]
    print("  automation-studio:", " | ".join(x.replace("  ", " ") for x in n8n) or "not set up (bash ../automation-studio/scripts/setup_n8n.sh --yes)")
    try:
        d = json.loads(SECRETS.read_text())
        print(f"  web secrets: {', '.join((d.get('web_secrets') or {}).keys()) or 'none'}   (names only)")
    except Exception:
        print("  web secrets: none")
    return 0 if ok else 1


def cmd_start(a):
    if health(a.port):
        print(f"browserd already running on :{a.port}")
        return 0
    if not a.allow:
        sys.exit("nx start: --allow example.com,app.example.com is required (the browser may only visit these)")
    STATE.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, str(HERE / "browserd.py"), "serve", "--allow", a.allow, "--port", str(a.port)]
    for f, k in [(a.headed, "--headed"), (a.allow_private, "--allow-private"), (a.allow_eval, "--allow-eval")]:
        if f:
            cmd.append(k)
    if a.cdp:
        cmd += ["--cdp", a.cdp]
    log = open(STATE / "browserd.log", "ab")
    p = subprocess.Popen(cmd, stdout=log, stderr=log, start_new_session=True)
    (STATE / "browserd.pid").write_text(str(p.pid))
    for _ in range(40):
        if health(a.port):
            print(f"browserd up on http://127.0.0.1:{a.port}  allow={a.allow}  (log: {STATE/'browserd.log'})")
            return 0
        time.sleep(0.5)
    print("browserd did not come up — see", STATE / "browserd.log")
    return 1


def cmd_stop(a):
    f = STATE / "browserd.pid"
    if f.exists():
        try:
            os.kill(int(f.read_text()), signal.SIGTERM)
            print("stopped")
        except Exception as e:
            print("not running:", e)
        f.unlink(missing_ok=True)
    else:
        print("no pid file")
    return 0


def cmd_status(a):
    h = health(a.port)
    print(json.dumps(h, indent=2) if h else "browserd is not running")
    return 0 if h else 1


def cmd_chrome(a):
    prof = Path.home() / ".local/share/ai-skills/chrome-cdp-profile"
    mac = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    print(f"""Attach mode — let the automation use a Chrome that YOU control and are logged in to.
1. Start a dedicated Chrome (Chrome refuses CDP on your default profile, and a separate profile keeps your personal browsing out of reach):
     "{mac}" --remote-debugging-port=9222 --user-data-dir="{prof}"
   (Windows: chrome.exe …; Linux: google-chrome …). Sign in to the sites you need in THAT window.
2. nx start --allow <domains> --cdp http://127.0.0.1:9222
3. Recipes now run in that window (tabs you can watch). CDP gives full control of that Chrome — keep port 9222 on 127.0.0.1 only; never expose it.""")
    return 0


def cmd_login(a):
    return sh([sys.executable, str(HERE / "browserd.py"), "login", a.url, "--session", a.session]).returncode


def cmd_secret(a):
    if not re.fullmatch(r"\w+", a.name):
        sys.exit("secret name: letters/digits/underscore")
    val = getpass.getpass(f"value for {a.name} (hidden): ")
    try:
        d = json.loads(SECRETS.read_text())
    except Exception:
        d = {}
    d.setdefault("web_secrets", {})[a.name] = val
    SECRETS.parent.mkdir(parents=True, exist_ok=True)
    SECRETS.write_text(json.dumps(d, indent=2))
    SECRETS.chmod(0o600)
    print(f"saved {a.name} → use as {{{{secret:{a.name}}}}} in recipes (file mode 600; prefer a real password manager for high-value accounts)")
    return 0


def cmd_recipe(a):
    bd = [sys.executable, str(HERE / "browserd.py")]
    if a.action == "list":
        sys.path.insert(0, str(HERE))
        import browserd
        for r in browserd.list_recipes():
            print(f"  {r['name']:<24}{r['description'][:90]}")
        tdir = SKILL / "recipes" / "templates"
        print("templates:", ", ".join(p.stem for p in sorted(tdir.glob("*.json"))))
        return 0
    if a.action == "validate":
        return sh(bd + ["validate", a.target]).returncode
    if a.action == "run":
        extra = ["--vars", a.vars] if a.vars else []
        if a.allow:
            extra += ["--allow", a.allow]
        if a.allow_private:
            extra.append("--allow-private")
        if a.headed:
            extra.append("--headed")
        return sh(bd + ["run", a.target, "--session", a.session] + extra).returncode
    if a.action == "new":
        src = SKILL / "recipes" / "templates" / f"{a.target}.json"
        if not src.exists():
            sys.exit(f"template {a.target!r} not found. Have: " + ", ".join(p.stem for p in (SKILL / 'recipes' / 'templates').glob('*.json')))
        out = Path(a.output or f"{a.target}.json")
        out.write_text(src.read_text())
        print(f"wrote {out} — replace every REPLACE: selector (open the site, DevTools → pick the element → copy a stable selector: prefer ids, data-* attrs, aria-labels, visible text; avoid nth-child/generated class names)")
        return 0


def cmd_new(a):
    name = PATTERNS.get(a.pattern, a.pattern)
    src = SKILL / "patterns" / name
    if not src.is_dir():
        sys.exit("patterns: " + ", ".join(f"{k} ({v})" for k, v in PATTERNS.items()))
    out = Path(a.output or name)
    out.mkdir(parents=True, exist_ok=True)
    rep = {"__RECIPE__": a.recipe, "__PATH__": a.path, "__SESSION__": a.session, "__BROWSERD__": a.browserd.rstrip("/")}
    for f in src.iterdir():
        t = f.read_text()
        for k, v in rep.items():
            t = t.replace(k, v)
        (out / f.name).write_text(t)
    print(f"scaffolded {out}/  (workflow.ts, cases.json)\nnext:\n  bash {AUTO} build {out}/workflow.ts -o {out}/flow.json\n  bash {AUTO} test {out}/flow.json {out}/cases.json")
    return 0


def passthru(a, rest):
    return sh(["bash", str(AUTO), a.cmd] + rest).returncode


def cmd_selftest(a):
    return sh(["bash", str(HERE / "selftest.sh")]).returncode


def main():
    ap = argparse.ArgumentParser(prog="nx", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor")
    p = sub.add_parser("start"); p.add_argument("--allow", default=""); p.add_argument("--port", type=int, default=PORT)
    p.add_argument("--headed", action="store_true"); p.add_argument("--allow-private", action="store_true"); p.add_argument("--allow-eval", action="store_true"); p.add_argument("--cdp", default="")
    for c in ("stop", "status", "chrome", "selftest"):
        q = sub.add_parser(c)
        if c == "status":
            q.add_argument("--port", type=int, default=PORT)
    p = sub.add_parser("login"); p.add_argument("url"); p.add_argument("--session", default="default")
    p = sub.add_parser("secret"); p.add_argument("name")
    p = sub.add_parser("recipe"); p.add_argument("action", choices=["list", "validate", "run", "new"]); p.add_argument("target", nargs="?", default="")
    p.add_argument("-o", "--output"); p.add_argument("--vars", default=""); p.add_argument("--session", default="default"); p.add_argument("--allow", default="")
    p.add_argument("--allow-private", action="store_true"); p.add_argument("--headed", action="store_true")
    p = sub.add_parser("new"); p.add_argument("pattern"); p.add_argument("-o", "--output"); p.add_argument("--recipe", default="my-recipe"); p.add_argument("--path", default="web-run")
    p.add_argument("--session", default="default"); p.add_argument("--browserd", default=f"http://127.0.0.1:{PORT}")
    argv = sys.argv[1:]
    if argv and argv[0] == "probe":
        sys.exit(sh([sys.executable, str(HERE / "siteprobe.py")] + argv[1:]).returncode)
    if argv and argv[0] == "ladder":
        sys.exit(sh([sys.executable, str(HERE / "ladder.py")] + argv[1:]).returncode)
    if argv and argv[0] in ("build", "test", "validate", "deploy", "creds", "diagram", "nodes", "node", "guide", "pull", "list", "trigger", "executions", "convert", "activate", "deactivate", "delete"):
        sys.exit(sh(["bash", str(AUTO)] + argv).returncode)
    a = ap.parse_args()
    fn = {"doctor": cmd_doctor, "start": cmd_start, "stop": cmd_stop, "status": cmd_status, "chrome": cmd_chrome, "login": cmd_login, "secret": cmd_secret,
          "recipe": cmd_recipe, "new": cmd_new, "selftest": cmd_selftest}[a.cmd]
    sys.exit(fn(a) or 0)


if __name__ == "__main__":
    main()
