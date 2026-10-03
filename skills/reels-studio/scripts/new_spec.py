#!/usr/bin/env python3
"""Start a reel spec from a template.

    python3 scripts/new_spec.py --list
    python3 scripts/new_spec.py --template talking_head --language ar-EG --brand neoai \
        --title "REEL — …" --out project/spec.json

Every {{…}} left in the file is a blank the validator refuses, so nothing ships half-filled.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reelspec import SKILL_DIR, list_brands, load_brand  # noqa: E402

TEMPLATES = os.path.join(SKILL_DIR, "templates")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--template")
    ap.add_argument("--language")
    ap.add_argument("--brand")
    ap.add_argument("--title")
    ap.add_argument("--color-mode", choices=["editor_talent", "mono"])
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    names = sorted(f[:-5] for f in os.listdir(TEMPLATES) if f.endswith(".json"))
    if a.list or not a.template:
        for n in names:
            about = json.load(open(os.path.join(TEMPLATES, n + ".json"), encoding="utf-8")).get("about", "")
            print(f"{n:20} {about}")
        print("\nbrands:", ", ".join(list_brands()))
        return 0
    if a.template not in names:
        print(f"unknown template '{a.template}'. choose: {', '.join(names)}", file=sys.stderr)
        return 2
    if not (a.language and a.out):
        print("--language and --out are required", file=sys.stderr)
        return 2
    spec = json.load(open(os.path.join(TEMPLATES, a.template + ".json"), encoding="utf-8"))
    spec["language"] = a.language
    if a.brand:
        load_brand(a.brand)  # fail early on a typo
        spec["brand"] = a.brand
    else:
        spec.pop("brand", None)
    if a.title:
        spec["title"] = a.title
    if a.color_mode:
        spec["color_mode"] = a.color_mode
    if os.path.exists(a.out):
        print(f"refusing to overwrite {a.out}", file=sys.stderr)
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
    print("wrote", a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
