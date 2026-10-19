#!/usr/bin/env python3
"""Build a tracked URL with consistent lower-case UTM parameters.
  utm.py URL --source instagram --medium social --campaign ramadan-2027 [--content reel-03] [--term kw]
Rules: lower-case, hyphens not spaces, ASCII only (transliterate Arabic campaign names), existing query kept.
"""
import argparse, re, sys
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

def clean(v):
    v = v.strip().lower()
    v = re.sub(r"[\s_]+", "-", v)
    if re.search(r"[^\x00-\x7f]", v):
        sys.exit("UTM value '%s' is not ASCII; transliterate it (e.g. ramadan-sale)" % v)
    return re.sub(r"[^a-z0-9.\-]", "", v)

ap = argparse.ArgumentParser()
ap.add_argument("url")
for k in ("source", "medium", "campaign"):
    ap.add_argument("--" + k, required=True)
for k in ("content", "term", "id"):
    ap.add_argument("--" + k)
a = ap.parse_args()
u = urlparse(a.url if "//" in a.url else "https://" + a.url)
q = dict(parse_qsl(u.query))
for k in ("source", "medium", "campaign", "content", "term", "id"):
    v = getattr(a, k)
    if v:
        q["utm_" + k] = clean(v)
print(urlunparse(u._replace(query=urlencode(q))))
