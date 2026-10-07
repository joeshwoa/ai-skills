#!/usr/bin/env python3
"""premium-design-kit command line (run through run.sh so the kit is importable).

  kit.py themes [--html gallery.html]          list themes / write the visual gallery
  kit.py tokens <theme|--brand slug> [--ar]    print derived tokens (JSON)
  kit.py chart  spec.json out.png [--theme id] themed chart image
  kit.py art    <kind> out.jpg [--theme id] [--w 2400 --h 1350 --dark --seed 3]
  kit.py asset  '<ref json>' outdir [--theme id]   resolve one asset ref (stock photo/icon/art/chart)
  kit.py preview <file.pdf|pptx|docx|xlsx> [outdir]   page PNGs + contact sheet (LOOK at it)
  kit.py brand  <slug|brand.json> [--dark]     brand kit → theme JSON
"""
import argparse
import json
import sys
from pathlib import Path

from pdk import themes as T


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("themes"); a.add_argument("--html")
    a = sub.add_parser("tokens"); a.add_argument("theme", nargs="?"); a.add_argument("--brand"); a.add_argument("--ar", action="store_true")
    a = sub.add_parser("chart"); a.add_argument("spec"); a.add_argument("out"); a.add_argument("--theme", default="plain-pro"); a.add_argument("--brand")
    a = sub.add_parser("art"); a.add_argument("kind"); a.add_argument("out"); a.add_argument("--theme", default="plain-pro"); a.add_argument("--brand")
    a.add_argument("--w", type=int, default=2400); a.add_argument("--h", type=int, default=1350); a.add_argument("--dark", action="store_true"); a.add_argument("--seed", type=int, default=7)
    a = sub.add_parser("asset"); a.add_argument("ref"); a.add_argument("outdir"); a.add_argument("--theme", default="plain-pro"); a.add_argument("--brand")
    a = sub.add_parser("preview"); a.add_argument("file"); a.add_argument("outdir", nargs="?")
    a = sub.add_parser("brand"); a.add_argument("brand"); a.add_argument("--dark", action="store_true")
    o = ap.parse_args(argv)

    if o.cmd == "themes":
        for t in T.THEMES:
            print(f"{t['id']:<20} {t['style']:<5}  {t['tagline']}")
        if o.html:
            sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "premium-presentations" / "scripts"))
            from themes import build_theme_gallery_html
            build_theme_gallery_html(o.html)
            print("gallery →", o.html)
        return 0
    if o.cmd == "brand":
        print(json.dumps(T.theme_from_brand(T.load_brand(o.brand), dark=o.dark), indent=1, ensure_ascii=False))
        return 0
    th = T.resolve_theme(getattr(o, "theme", None), getattr(o, "brand", None))
    tk = T.tokens(th, arabic=getattr(o, "ar", False))
    if o.cmd == "tokens":
        print(json.dumps(tk, indent=1))
    elif o.cmd == "chart":
        from pdk.charts import render_chart
        print(render_chart(json.loads(Path(o.spec).read_text(encoding="utf-8")), tk, o.out))
    elif o.cmd == "art":
        from pdk.art import art
        print(art(o.kind, tk, o.out, o.w, o.h, seed=o.seed, dark=o.dark or None))
    elif o.cmd == "asset":
        from pdk.assets import Assets
        A = Assets(o.outdir, tk)
        print(A.resolve(json.loads(o.ref)))
        for w in A.warnings:
            print("WARN:", w)
        for c in A.credits():
            print("CREDIT:", c)
    elif o.cmd == "preview":
        from pdk.render import preview
        print(json.dumps(preview(o.file, o.outdir), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
