#!/usr/bin/env python3
"""Build or validate campaign/ad set/ad names so reports can be parsed automatically.

  naming.py build --level campaign --brand acme --objective sales --platform meta --market eg --period 2026-11 --offer whiteFriday
  naming.py build --level ad --concept ugc-hook3 --format 9x16 --version v2 [+ the campaign fields]
  naming.py parse "acme_sales_meta_eg_2026-11_whiteFriday"
Pattern: campaign  = brand_objective_platform_market_period_offer
         adset     = campaign + "|" + audience_placement_budgettype
         ad        = adset + "|" + concept_format_version
Segments are lower-camel/ASCII, no spaces, no pipes or underscores inside a segment.
"""
import argparse, re, sys

def seg(v):
    if re.search(r"[^\x00-\x7f]", v): sys.exit("non-ASCII segment: " + v)
    return re.sub(r"[^A-Za-z0-9.\-]", "", v.replace(" ", "-"))

ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest="cmd", required=True)
b = sp.add_parser("build")
b.add_argument("--level", choices=["campaign", "adset", "ad"], required=True)
for k in ("brand", "objective", "platform", "market", "period", "offer"): b.add_argument("--" + k, required=True)
for k in ("audience", "placement", "budgettype", "concept", "format", "version"): b.add_argument("--" + k)
p = sp.add_parser("parse"); p.add_argument("name")
a = ap.parse_args()
if a.cmd == "build":
    camp = "_".join(seg(getattr(a, k)) for k in ("brand", "objective", "platform", "market", "period", "offer"))
    if a.level == "campaign": print(camp); sys.exit()
    for k in ("audience", "placement", "budgettype"):
        if not getattr(a, k): sys.exit("--%s required for adset/ad" % k)
    adset = camp + "|" + "_".join(seg(getattr(a, k)) for k in ("audience", "placement", "budgettype"))
    if a.level == "adset": print(adset); sys.exit()
    for k in ("concept", "format", "version"):
        if not getattr(a, k): sys.exit("--%s required for ad" % k)
    print(adset + "|" + "_".join(seg(getattr(a, k)) for k in ("concept", "format", "version")))
else:
    parts = a.name.split("|")
    keys = [["brand", "objective", "platform", "market", "period", "offer"], ["audience", "placement", "budgettype"], ["concept", "format", "version"]]
    out = {}
    for ks, part in zip(keys, parts):
        vals = part.split("_")
        if len(vals) != len(ks): sys.exit("segment count mismatch in '%s'" % part)
        out.update(dict(zip(ks, vals)))
    print(out)
