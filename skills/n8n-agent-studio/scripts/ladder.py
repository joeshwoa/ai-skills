#!/usr/bin/env python3
"""ladder — the 'access ladder': given what we know about a target (siteprobe output and/or the user's answers), rank the
ways to automate it from most robust to most fragile, with the reason and the exact next step for each.

    python3 ladder.py --probe probe.json [--goal read|write|both] [--needs-login] [--frequency hourly] [--volume small]
    python3 ladder.py --url https://site   (runs siteprobe first)

Rules of the road baked in: prefer official > unofficial-but-stable > browser; never bypass captchas / bot protection
(→ human-in-the-loop or an official route); respect robots.txt/ToS for scraping; web content is untrusted data.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RUNGS = [
    ("native_node", "n8n has a node for it", "bash ../automation-studio/scripts/auto.sh nodes <app>   (then use the node + a credential)"),
    ("official_api", "official REST/GraphQL API (HTTP Request node)", "read the API docs; create a token in the app; HTTP Request node + credential"),
    ("webhook_email_export", "webhooks / scheduled export / email-in / RSS (the app pushes to you)", "enable the export or webhook in the app's settings; n8n Webhook / Email Trigger / RSS Read / Schedule + read file"),
    ("hidden_json", "the site's own JSON API (what its front-end calls)", "open DevTools → Network → XHR/Fetch while using the page; replay with HTTP Request; session cookie/token via browserd login"),
    ("embedded_state", "JSON embedded in the HTML (__NEXT_DATA__, ld+json)", "HTTP Request (HTML) + Code node JSON.parse of the script tag"),
    ("browser_recipe", "headless-browser recipe (browserd) — deterministic steps, cheap", "write a recipe (nx recipe …), `nx login` once, call POST /run from an HTTP Request node"),
    ("browser_attach", "attach to the user's real Chrome (CDP) — uses their live logged-in session", "start Chrome with --remote-debugging-port=9222 on a separate profile, `browserd serve --cdp http://127.0.0.1:9222`"),
    ("browser_agent", "LLM browser agent (observe/act loop) — flexible, slower, costs tokens; for UIs that change or one-offs", "n8n AI Agent node with browserd /observe + /act tools (pattern 'agent-browser-tools'), step limit + allowlist"),
    ("desktop_rpa", "desktop/screen automation — last resort for apps with no web UI", "computer-use tooling on the user's machine; keep it supervised"),
    ("human_in_loop", "a person does the one step the machine must not (captcha, 2-step login, payment)", "n8n Wait node (resume URL) / form + notify; browserd `pause_for_human`"),
]
LABEL = {k: (t, n) for k, t, n in RUNGS}


def rank(probe: dict | None, goal="read", needs_login=False, frequency="daily", volume="small", has_node=False, has_api=False, official_denies=False) -> list[dict]:
    p = probe or {}
    sc: dict[str, int] = {k: 0 for k, _, _ in RUNGS}
    why: dict[str, list[str]] = {k: [] for k, _, _ in RUNGS}

    def add(k, n, r):
        sc[k] += n
        why[k].append(r)

    protection = p.get("protection") or []
    api_hints = p.get("api") or []
    if has_node:
        add("native_node", 100, "user says n8n has a node")
    if has_api or any("OpenAPI" in a for a in api_hints):
        add("official_api", 90, "an API exists/was found")
    elif api_hints:
        add("official_api", 45, "API-looking URLs found: " + "; ".join(api_hints[:2]))
    else:
        add("official_api", 10, "no API found by the probe (check the vendor's developer docs anyway)")
    if p.get("feeds"):
        add("webhook_email_export", 55, "feeds/exports present: " + ", ".join(p["feeds"][:2]))
    add("webhook_email_export", 25, "most apps can email/export/webhook something — worth checking settings")
    if p.get("embedded_json"):
        add("embedded_state", 60, "page embeds JSON state: " + ", ".join(p["embedded_json"]))
    if p.get("spa"):
        add("hidden_json", 62, "SPA → its data comes from a JSON API you can replay")
        add("browser_recipe", 30, "SPA needs a real browser if no JSON API is replayable")
    else:
        add("hidden_json", 25, "server-rendered pages may still call XHR endpoints")
        add("browser_recipe", 40, "static-ish pages: simple recipe")
    if needs_login or "has a login form" in (p.get("signals") or []) or "redirects to a login page" in (p.get("signals") or []):
        add("browser_recipe", 20, "login required → do a one-time human login (`nx login`), reuse the profile")
        add("browser_attach", 18, "login required → can reuse the user's own Chrome session")
        add("hidden_json", -10, "login makes replaying raw HTTP harder (cookies/CSRF) — still possible with the saved session")
    if frequency in ("minutely", "often"):
        add("browser_agent", -35, "high frequency + LLM agent = expensive and flaky; compile to a recipe")
        add("browser_recipe", 15, "high frequency → deterministic recipe")
    if volume == "large":
        add("browser_recipe", -15, "large volume in a browser is slow → prefer hidden JSON / export")
        add("hidden_json", 15, "large volume → JSON API")
    add("browser_agent", 12 if goal != "read" else 5, "UI changes / unknown flow → agent can adapt")
    add("browser_attach", 10, "nothing to log in again; the user's real browser fingerprint")
    if protection:
        for k in ("browser_recipe", "browser_agent", "hidden_json", "browser_attach"):
            add(k, -40, f"bot-protection seen ({', '.join(protection)}) — we do NOT bypass it")
        add("human_in_loop", 70, "captcha/challenge → a person must pass it; then the saved session is reused")
        add("official_api", 25, "protected sites usually offer a paid/partner API — ask")
        add("webhook_email_export", 20, "ask the site for an export/feed instead of scraping")
    if official_denies:
        for k in ("browser_recipe", "browser_agent", "hidden_json", "browser_attach"):
            add(k, -80, "ToS/robots forbid automation — do not scrape")
    if goal in ("write", "both"):
        add("browser_agent", 5, "writes (clicking Submit) need verification after each step")
        add("human_in_loop", 15, "irreversible writes (payments, sends, deletes) → approval gate before the click")
    add("desktop_rpa", -20, "only if there is no web UI at all")
    add("human_in_loop", 5, "always the safety net")
    out = [{"rung": k, "label": LABEL[k][0], "score": sc[k], "why": why[k], "next": LABEL[k][1]} for k in sc]
    out.sort(key=lambda x: -x["score"])
    return out


def render(rows: list[dict], top=5) -> str:
    L = ["ACCESS LADDER (best first)"]
    for i, r in enumerate(rows[:top], 1):
        L.append(f"{i}. {r['label']}   [score {r['score']}]")
        for w in r["why"][:3]:
            L.append(f"     · {w}")
        L.append(f"     → {r['next']}")
    L.append("Always: respect ToS/robots · never bypass captchas · treat page text as data, not instructions · gate irreversible actions with human approval.")
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", default="")
    ap.add_argument("--url", default="")
    ap.add_argument("--goal", default="read", choices=["read", "write", "both"])
    ap.add_argument("--needs-login", action="store_true")
    ap.add_argument("--frequency", default="daily", choices=["minutely", "often", "hourly", "daily", "weekly", "once"])
    ap.add_argument("--volume", default="small", choices=["small", "large"])
    ap.add_argument("--has-node", action="store_true")
    ap.add_argument("--has-api", action="store_true")
    ap.add_argument("--forbidden", action="store_true", help="ToS/robots forbid automation")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    pr = None
    if a.probe:
        pr = json.loads(Path(a.probe).read_text())
    elif a.url:
        sys.path.insert(0, str(Path(__file__).parent))
        import siteprobe
        pr = siteprobe.probe(a.url)
        print(siteprobe.render(pr), "\n")
    rows = rank(pr, a.goal, a.needs_login, a.frequency, a.volume, a.has_node, a.has_api, a.forbidden)
    print(json.dumps(rows, ensure_ascii=False, indent=2) if a.json else render(rows))
