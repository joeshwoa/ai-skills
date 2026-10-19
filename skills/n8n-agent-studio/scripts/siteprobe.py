#!/usr/bin/env python3
"""siteprobe — look at a website/web app and say HOW it can be automated (stdlib only, read-only: GETs a few public URLs).

    python3 siteprobe.py https://example.com [--json] [--cookie-file cookies.txt]

Finds: official API hints (openapi/swagger/graphql/developer pages), feeds (RSS/Atom/sitemap), embedded JSON state
(__NEXT_DATA__, __NUXT__, ld+json), forms/login, SPA-ness, bot-protection/captcha markers, robots.txt rules, export links.
It never logs in, never submits forms, never tries to get around protection — it only reports what it saw.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from urllib.parse import urljoin, urlparse

UA = "Mozilla/5.0 (compatible; ai-skills-siteprobe/1.0; +read-only)"
PROBE_PATHS = ["/openapi.json", "/swagger.json", "/api/docs", "/api", "/graphql", "/.well-known/openid-configuration", "/sitemap.xml", "/robots.txt", "/feed", "/rss", "/atom.xml"]
CAPTCHA = {"recaptcha": r"google\.com/recaptcha|g-recaptcha", "hcaptcha": r"hcaptcha\.com|h-captcha", "turnstile": r"challenges\.cloudflare\.com/turnstile|cf-turnstile",
           "cloudflare_challenge": r"cf-chl|Just a moment\.\.\.|_cf_chl_opt", "datadome": r"datadome", "perimeterx": r"px-captcha|perimeterx", "akamai": r"akamai.*bot|_abck"}


def fetch(url, timeout=12, headers=None, cookie=None):
    h = {"User-Agent": UA, "Accept": "text/html,application/json;q=0.9,*/*;q=0.5"}
    h.update(headers or {})
    if cookie:
        h["Cookie"] = cookie
    req = urllib.request.Request(url, headers=h)
    try:
        r = urllib.request.urlopen(req, timeout=timeout)
        body = r.read(600_000)
        return r.status, dict(r.headers), body.decode("utf-8", "replace"), r.geturl()
    except urllib.error.HTTPError as e:
        try:
            body = e.read(200_000).decode("utf-8", "replace")
        except Exception:
            body = ""
        return e.code, dict(e.headers or {}), body, url
    except Exception as e:
        return 0, {}, str(e), url


def probe(url: str, cookie: str | None = None) -> dict:
    if not re.match(r"https?://", url):
        url = "https://" + url
    base = "{0.scheme}://{0.netloc}".format(urlparse(url))
    rep: dict = {"url": url, "base": base, "signals": [], "api": [], "feeds": [], "embedded_json": [], "forms": [], "protection": [], "notes": []}
    status, hdr, html, final = fetch(url, cookie=cookie)
    rep["status"], rep["final_url"] = status, final
    if status == 0:
        rep["notes"].append("unreachable: " + html[:120])
        return rep
    low = html.lower()
    hl = {k.lower(): v for k, v in hdr.items()}
    server = hl.get("server", "")
    rep["server"] = server
    if "cloudflare" in server.lower() or "cf-ray" in hl:
        rep["signals"].append("behind Cloudflare")
    for name, pat in CAPTCHA.items():
        if re.search(pat, html, re.I) or re.search(pat, json.dumps(hl), re.I):
            rep["protection"].append(name)
    if status in (403, 429, 503) and (rep["protection"] or "captcha" in low or "access denied" in low):
        rep["protection"].append(f"blocked_http_{status}")
    if status == 401 or "www-authenticate" in hl:
        rep["signals"].append("HTTP auth required (401)")
    if urlparse(final).path != urlparse(url).path and re.search(r"login|signin|sign-in|auth|sso", final, re.I):
        rep["signals"].append("redirects to a login page")
    # forms
    for m in re.finditer(r"<form\b(.*?)</form>", html, re.I | re.S):
        blk = m.group(1)
        inputs = re.findall(r"<input\b[^>]*>", blk, re.I)
        has_pw = any(re.search(r'type=["\']?password', i, re.I) for i in inputs)
        act = re.search(r'action=["\']([^"\']*)', blk, re.I)
        rep["forms"].append({"action": urljoin(final, act.group(1)) if act else final, "password": has_pw, "inputs": len(inputs)})
    if any(f["password"] for f in rep["forms"]):
        rep["signals"].append("has a login form")
    # SPA-ness
    body_text = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", html, flags=re.S | re.I)
    words = len(body_text.split())
    spa = bool(re.search(r'<div id=["\'](root|app|__next|__nuxt)["\']', html, re.I)) and words < 120
    rep["spa"] = spa
    rep["visible_words"] = words
    if spa:
        rep["signals"].append("JS single-page app (content is rendered in the browser → look for its JSON API in the network tab, or use a browser)")
    # embedded json
    for label, pat in [("__NEXT_DATA__", r'<script id="__NEXT_DATA__"[^>]*>'), ("__NUXT__", r"window\.__NUXT__"), ("__INITIAL_STATE__", r"window\.__(INITIAL|PRELOADED)_STATE__"),
                       ("ld+json", r'<script type="application/ld\+json"'), ("apollo", r"__APOLLO_STATE__")]:
        if re.search(pat, html):
            rep["embedded_json"].append(label)
    # feeds / links
    for m in re.finditer(r'<link[^>]+type=["\']application/(rss|atom)\+xml["\'][^>]*href=["\']([^"\']+)', html, re.I):
        rep["feeds"].append(urljoin(final, m.group(2)))
    for m in re.finditer(r'href=["\']([^"\']+\.(?:csv|xlsx|json|xml|ics))["\']', html, re.I):
        rep["feeds"].append(urljoin(final, m.group(1)))
    for m in re.finditer(r'href=["\']([^"\']*(?:developer|/api|swagger|openapi|graphql|webhooks?)[^"\']*)["\']', html, re.I):
        rep["api"].append(urljoin(final, m.group(1)))
    rep["feeds"] = sorted(set(rep["feeds"]))[:8]
    rep["api"] = sorted(set(rep["api"]))[:8]
    # well-known endpoints (cheap GETs)
    for p in PROBE_PATHS:
        s2, h2, b2, _ = fetch(base + p, timeout=8, cookie=cookie)
        ct = {k.lower(): v for k, v in h2.items()}.get("content-type", "")
        if s2 == 200:
            if p == "/robots.txt":
                dis = [l.split(":", 1)[1].strip() for l in b2.splitlines() if l.lower().startswith("disallow:") and l.split(":", 1)[1].strip()]
                rep["robots_disallow"] = dis[:15]
                if re.search(r"user-agent:\s*\*\s*\n\s*disallow:\s*/\s*$", b2, re.I | re.M):
                    rep["notes"].append("robots.txt disallows everything for all agents — respect it; prefer an official route")
            elif p in ("/openapi.json", "/swagger.json") and ("openapi" in b2[:400] or "swagger" in b2[:400]):
                rep["api"].insert(0, base + p + "  (OpenAPI spec!)")
            elif p == "/graphql" and ("graphql" in b2.lower() or "json" in ct):
                rep["api"].append(base + p + "  (GraphQL endpoint answers)")
            elif p in ("/sitemap.xml",) and "<urlset" in b2[:600]:
                rep["feeds"].append(base + p)
            elif p in ("/feed", "/rss", "/atom.xml") and ("<rss" in b2[:400] or "<feed" in b2[:400]):
                rep["feeds"].append(base + p)
            elif p == "/.well-known/openid-configuration":
                rep["signals"].append("OIDC/OAuth provider (official login flow exists)")
        elif s2 in (401, 403) and p in ("/api", "/graphql") and ("json" in ct or "graphql" in ct or "www-authenticate" in {k.lower() for k in h2}):
            rep["api"].append(f"{base}{p}  (exists but needs auth: HTTP {s2})")
    rep["api"] = list(dict.fromkeys(rep["api"]))[:10]
    rep["feeds"] = list(dict.fromkeys(rep["feeds"]))[:10]
    return rep


def render(rep: dict) -> str:
    L = [f"siteprobe  {rep['url']}  → HTTP {rep.get('status')}  ({rep.get('final_url')})"]
    for k, t in [("signals", "signals"), ("protection", "bot-protection"), ("api", "API hints"), ("feeds", "feeds / exports"), ("embedded_json", "embedded JSON"), ("notes", "notes")]:
        if rep.get(k):
            L.append(f"  {t}:")
            L += [f"    - {x}" for x in rep[k]]
    if rep.get("forms"):
        L.append("  forms: " + "; ".join(f"{f['action'].split('?')[0]} ({'login' if f['password'] else str(f['inputs']) + ' inputs'})" for f in rep["forms"][:5]))
    L.append(f"  SPA: {rep.get('spa')}  visible words: {rep.get('visible_words')}")
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--cookie", default="")
    a = ap.parse_args()
    r = probe(a.url, a.cookie or None)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else render(r))
