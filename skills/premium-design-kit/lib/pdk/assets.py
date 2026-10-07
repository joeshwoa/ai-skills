"""Asset resolution for every document skill: one place that turns an asset REFERENCE in a spec into a
real local file + its licence/credit.

Reference forms (anywhere a spec takes "image"/"icon"/"background"):
  "path/to/file.png"                       user's own file (relative to the spec's folder)
  {"path": "logo.svg"}                     same
  {"photo": "students coding laptops classroom", "orientation": "landscape", "pick": 1}
                                           free stock photo via stock-library (studio-mcp)
  {"stock": "pexels:12345"}                an exact stock id chosen from a contact sheet
  {"illustration": "...", "vector": "..."} illustration/vector search (same tool, other kind)
  {"icon": "mdi:school"} | {"icon": "graduation cap"}   Iconify icon recoloured to the theme
  {"art": "mesh|blobs|geo|waves|dots|grid|stripes|arcs", "seed": 3, "dark": true}  generated art
  {"chart": {...chart spec...}}            a themed chart image (charts.render_chart)
  {"url": "https://..."}                   NOT fetched (licence unknown) → error, use stock or path

Stock is fetched through the user's studio-mcp (skills/stock-library/scripts/call.sh). If it is not
installed or offline, photo refs fall back to generated art and a warning — never a broken image, and
never a scraped picture. Every downloaded file keeps its .license.json; `credits()` returns the lines.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

from . import SKILLS
from .art import art as make_art
from .charts import render_chart

CALL = SKILLS / "stock-library" / "scripts" / "call.sh"


def _relevance(r: dict, query: str, orientation: str = "") -> float:
    """Cheap relevance for auto-picking: query words in the title/tags, enough pixels, right shape."""
    import re
    words = {w for w in re.findall(r"[a-z]+", query.lower()) if len(w) > 2}
    title = " ".join(str(r.get(k, "")) for k in ("title", "tags", "description")).lower()
    hits = sum(1 for w in words if w in title or w.rstrip("s") in title)
    score = hits * 2.0
    try:
        w, h = (int(x) for x in str(r.get("size", "0x0")).lower().split("x")[:2])
    except ValueError:
        w = h = 0
    score += 1.0 if min(w, h) >= 1000 else (0.4 if min(w, h) >= 700 else -1.5)
    if orientation and w and h:
        shape = "landscape" if w > h * 1.1 else "portrait" if h > w * 1.1 else "square"
        score += 0.8 if shape == orientation else -0.4
    if str(r.get("provider", r.get("id", ""))).split(":")[0] in ("pexels", "unsplash", "pixabay"):
        score += 1.5          # curated stock beats archive photos
    if re.search(r"\b1[89]\d\d\b|circa|archive|scan", title):
        score -= 2.5          # historic scans rarely suit a modern document
    return score - (int(r.get("n", 1)) * 0.05)


class Assets:
    def __init__(self, workdir: str | Path, tk: dict, *, base: str | Path | None = None, project: str = "",
                 offline: bool = False, icon_set: str = "material-symbols"):
        self.dir = Path(workdir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.tk = tk
        self.base = Path(base) if base else Path.cwd()
        self.project = project or "docs"
        self.offline = offline or os.environ.get("PDK_OFFLINE") == "1"
        self.icon_set = icon_set          # one icon family per document = visual consistency
        self.warnings: list[str] = []
        self.credits_: list[dict] = []
        self._cachef = self.dir / "_assets.json"
        try:
            self.cache = json.loads(self._cachef.read_text())
        except Exception:
            self.cache = {}

    # ---------------------------------------------------------------- public
    def resolve(self, ref, *, purpose: str = "image", orientation: str = "", size: tuple[int, int] = (1600, 900),
                color: str | None = None) -> str | None:
        """Return a local file path for `ref` (or None if ref is empty)."""
        if not ref:
            return None
        if isinstance(ref, str):
            ref = {"path": ref}
        if not isinstance(ref, dict):
            raise TypeError(f"asset ref must be str or dict, got {type(ref).__name__}")
        sized = any(k in ref for k in ("art", "chart", "path"))     # stock/icons: one file whatever the box
        key = hashlib.sha1(json.dumps([ref, orientation if not sized else "", list(size) if sized else None, color,
                                       self.tk["accent"]], sort_keys=True).encode()).hexdigest()[:14]
        hit = self.cache.get(key)
        if hit and Path(hit["file"]).exists():
            if hit.get("credit"):
                self._add_credit(hit["credit"])
            return hit["file"]
        self._fell_back = False
        f, credit = self._resolve(ref, key, purpose, orientation, size, color)
        if f:
            f = self._normalize(f, key)
        if f and not self._fell_back:
            self.cache[key] = {"file": f, "credit": credit, "ref": ref}
            self._cachef.write_text(json.dumps(self.cache, ensure_ascii=False, indent=1))
            if credit:
                self._add_credit(credit)
        return f

    def credits(self) -> list[str]:
        out, seen = [], set()
        for c in self.credits_:
            line = c.get("attribution") or ""
            if line and line not in seen:
                seen.add(line)
                out.append(line)
        return out

    # --------------------------------------------------------------- private
    def _add_credit(self, c):
        if c and c not in self.credits_:
            self.credits_.append(c)

    def _resolve(self, ref, key, purpose, orientation, size, color):
        if "path" in ref:
            p = Path(os.path.expanduser(str(ref["path"])))
            if not p.is_absolute():
                p = (self.base / p).resolve()
            if not p.exists():
                raise FileNotFoundError(f"image not found: {p}")
            if p.suffix.lower() == ".svg":
                return self._svg_to_png(p, key, size), None
            return str(p), None
        if "url" in ref:
            raise ValueError("remote URLs are not fetched (unknown licence). Use {'photo': '<query>'} for free "
                             "stock, {'stock': '<id>'}, or download the file yourself and pass {'path': ...}.")
        if "art" in ref:
            out = self.dir / f"art-{ref['art']}-{key}.jpg"
            return make_art(ref["art"], self.tk, out, size[0], size[1], seed=ref.get("seed", 7),
                            dark=ref.get("dark"), intensity=ref.get("intensity", 1.0)), None
        if "chart" in ref:
            out = self.dir / f"chart-{key}.png"
            return render_chart(ref["chart"], self.tk, out, width_in=ref.get("width_in", 7.0),
                                height_in=ref.get("height_in", 3.6)), None
        if "icon" in ref:
            return self._icon(ref, key, color)
        for kind in ("photo", "illustration", "vector"):
            if kind in ref:
                return self._stock_search(ref[kind], kind, ref, key, orientation or ref.get("orientation", ""), size)
        if "stock" in ref:
            return self._stock_ids([ref["stock"]], key, size)
        raise ValueError(f"unknown asset ref {ref}")

    def _normalize(self, f: str, key: str, max_px: int = 2600) -> str:
        """Office files only take PNG/JPEG/GIF/BMP, and huge photos bloat documents: convert WEBP/TIFF/
        HEIC/… to JPEG (or PNG when transparent) and cap the long side at max_px."""
        from PIL import Image, ImageOps
        p = Path(f)
        try:
            im = Image.open(p)
        except Exception:
            return f
        ok_fmt = p.suffix.lower() in (".png", ".jpg", ".jpeg") and im.format in ("PNG", "JPEG")
        if ok_fmt and im.format == "JPEG":
            try:      # python-docx/pptx reject some valid JPEGs (no JFIF/EXIF header) → re-encode those
                from docx.image.image import Image as _DocxImage
                _DocxImage.from_file(str(p))
            except ImportError:
                pass
            except Exception:
                ok_fmt = False
        if ok_fmt and max(im.size) <= max_px:
            return f
        im = ImageOps.exif_transpose(im)
        if max(im.size) > max_px:
            im.thumbnail((max_px, max_px), Image.LANCZOS)
        alpha = im.mode in ("RGBA", "LA", "P") and "A" in im.convert("RGBA").getbands()
        if alpha and im.convert("RGBA").getextrema()[3][0] < 255:
            out = self.dir / f"norm-{key}.png"
            im.convert("RGBA").save(out, optimize=True)
        else:
            out = self.dir / f"norm-{key}.jpg"
            im.convert("RGB").save(out, quality=88, optimize=True, progressive=True)
        lic = Path(str(p) + ".license.json")
        if lic.exists():
            Path(str(out) + ".license.json").write_bytes(lic.read_bytes())
        return str(out)

    def _svg_to_png(self, p: Path, key: str, size) -> str:
        out = self.dir / f"svg-{key}.png"
        try:
            import cairosvg  # type: ignore
            cairosvg.svg2png(url=str(p), write_to=str(out), output_width=size[0])
            return str(out)
        except Exception:
            pass
        from .render import html_screenshot
        html = f"<html><body style='margin:0;background:transparent'><img src='{p.as_uri()}' style='width:{size[0]}px'></body></html>"
        return html_screenshot(html, out, width=size[0], height=None, transparent=True)

    def _studio(self, tool: str, args: dict) -> dict | None:
        if self.offline:
            return None
        if not CALL.exists():
            self.warnings.append("stock-library not found next to this skill — stock refs fell back to generated art")
            return None
        try:
            r = subprocess.run(["bash", str(CALL), "--json", tool, json.dumps(args, ensure_ascii=False)],
                               capture_output=True, text=True, timeout=240)
        except Exception as e:  # pragma: no cover
            self.warnings.append(f"{tool} failed to run: {e}")
            return None
        try:
            out = json.loads(r.stdout)
        except json.JSONDecodeError:
            msg = (r.stderr or r.stdout).strip().splitlines()[-1:] or ["?"]
            self.warnings.append(f"{tool} unavailable ({msg[0][:160]}) — used a fallback")
            return None
        if not out.get("ok", True):
            out.setdefault("data", {})
        return out

    def _icon(self, ref, key, color):
        q = ref["icon"]
        col = "#" + (color or ref.get("color") or self.tk["accent"]).lstrip("#")
        res = self._studio("stock_icon", {"query": q, "color": col, "size": 512, "count": 1, "project": self.project})
        icons = ((res or {}).get("data") or {}).get("icons") or []
        # word queries: prefer clean single-colour sets (consistent, recolourable) over emoji/colour sets
        if icons and ":" not in str(q):
            pref = [ref.get("set") or self.icon_set]
            pref += ["material-symbols", "tabler", "lucide", "ph", "mdi", "solar", "carbon", "fluent", "heroicons"]
            prefix = icons[0]["id"].split(":")[1]
            if prefix != pref[0]:
                alts = ((res or {}).get("data") or {}).get("alternatives") or []
                best = sorted((a for a in alts if a["id"].split(":")[0] in pref),
                              key=lambda a: pref.index(a["id"].split(":")[0]))
                if best:
                    r2 = self._studio("stock_icon", {"query": best[0]["id"], "color": col, "size": 512, "count": 1,
                                                     "project": self.project})
                    icons = ((r2 or {}).get("data") or {}).get("icons") or icons
        if not icons:
            self.warnings.append(f"icon '{q}' not found/unavailable — drawn as a monogram")
            self._fell_back = True
            return self._monogram(str(q), key, col), None
        ic = icons[0]
        dst = self.dir / f"icon-{key}.png"
        shutil.copyfile(ic["png"], dst)
        shutil.copyfile(ic["svg"], dst.with_suffix(".svg"))
        return str(dst), {"title": ic.get("id"), "attribution": ic.get("attribution") if ic.get("attribution_required") else "",
                          "license": ic.get("license")}

    def _monogram(self, q, key, col):
        from PIL import Image, ImageDraw
        from .themes import hex_rgb
        im = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.ellipse([16, 16, 496, 496], outline=(*hex_rgb(col.lstrip("#")), 255), width=28)
        out = self.dir / f"mono-{key}.png"
        im.save(out)
        return str(out)

    def _stock_search(self, query, kind, ref, key, orientation, size):
        args = {"query": query, "kind": kind, "count": max(6, int(ref.get("pick", 1))), "project": self.project,
                "commercial": True}
        if orientation:
            args["orientation"] = orientation
        res = self._studio("stock_search", args)
        results = ((res or {}).get("data") or {}).get("results") or []
        words = str(query).split()
        for n in (3, 2):                      # too specific → broaden step by step
            if results or res is None or len(words) <= n:
                continue
            args["query"] = " ".join(words[:n])
            res = self._studio("stock_search", args)
            results = ((res or {}).get("data") or {}).get("results") or []
            if results:
                self.warnings.append(f"'{query}' had no free {kind}; used the broader '{args['query']}'")
        if not results:
            if res is not None:
                self.warnings.append(f"no free {kind} found for '{query}' — used generated art; try other words")
            self._fell_back = True
            return make_art("mesh", self.tk, self.dir / f"art-fallback-{key}.jpg", size[0], size[1]), None
        if ref.get("pick"):
            pick = max(1, int(ref["pick"]))
            ranked = [results[min(pick, len(results)) - 1]]
        else:
            ranked = sorted(results, key=lambda r: -_relevance(r, query, orientation))
        for item in ranked[:3]:                 # a source can fail to download → try the next best
            f, credit = self._stock_ids([item["id"]], key, size, quiet=True)
            if f:
                pick = results.index(item) + 1
                if res and res.get("previews"):
                    self.warnings.append(f"'{query}': auto-picked #{pick} \"{str(item.get('title', ''))[:50]}\" ({item.get('id')}) — "
                                         f"LOOK at the contact sheet and pin a better one with {{\"stock\": \"<id>\"}}: {res['previews'][0]}")
                return f, credit
        self.warnings.append(f"'{query}': downloads failed — used generated art")
        self._fell_back = True
        return make_art("mesh", self.tk, self.dir / f"art-fallback-{key}.jpg", size[0], size[1]), None

    def _stock_ids(self, ids, key, size, quiet=False):
        res = self._studio("stock_download", {"ids": ids, "quality": "hd", "max_width": max(1600, size[0]),
                                              "project": self.project})
        items = ((res or {}).get("data") or {}).get("downloaded") or []
        if not items:
            if quiet:
                return None, None
            self.warnings.append(f"stock download failed for {ids} — used generated art")
            self._fell_back = True
            return make_art("mesh", self.tk, self.dir / f"art-fallback-{key}.jpg", size[0], size[1]), None
        it = items[0]
        src = Path(it["file"])
        dst = self.dir / f"stock-{key}{src.suffix.lower()}"
        shutil.copyfile(src, dst)
        lic = Path(str(src) + ".license.json")
        credit = {"title": it.get("title") or it.get("id"), "attribution": it.get("attribution", ""),
                  "license": it.get("license", ""), "id": it.get("id")}
        if lic.exists():
            shutil.copyfile(lic, Path(str(dst) + ".license.json"))
            try:
                L = json.loads(lic.read_text())
                credit["attribution"] = credit["attribution"] or L.get("attribution", "")
                credit["license"] = credit["license"] or L.get("license", "")
            except Exception:
                pass
        return str(dst), credit
