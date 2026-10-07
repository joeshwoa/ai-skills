"""Generated decorative art in the theme's colours — covers, section dividers, panels, page corners.

Original, licence-free, deterministic (seeded). Use when a design needs visual richness and no real
photo is wanted/available. Never a substitute for a REAL image the content needs (a product, a place,
a person) — for those use assets.find_photo (stock-library) or the user's own files.

kinds: mesh (soft gradient mesh) · blobs (organic glow shapes) · geo (overlapping geometric shapes) ·
       waves (layered waves) · dots (halftone dot field) · grid (engineering grid + glow) ·
       stripes (diagonal bands) · arcs (concentric arcs)
"""
from __future__ import annotations

import math
import random
from pathlib import Path

from .themes import hex_rgb, mix

KINDS = ("mesh", "blobs", "geo", "waves", "dots", "grid", "stripes", "arcs")


def art(kind: str, tk: dict, out: str | Path, w: int = 2400, h: int = 1350, *, seed: int = 7,
        dark: bool | None = None, intensity: float = 1.0) -> str:
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter

    rnd = random.Random(f"{kind}-{seed}-{tk['accent']}")
    dark = (tk.get("style") == "dark") if dark is None else dark
    bg = tk["stage_bg"] if dark else tk["paper"]
    bg2 = tk["stage_bg_alt"] if dark else tk["paper_alt"]
    a1, a2 = (tk["stage_accent"], tk["accent_2"]) if dark else (tk["accent"], tk["accent_2"])
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)

    xs, ys = np.meshgrid(np.linspace(0, 1, w, dtype=np.float32), np.linspace(0, 1, h, dtype=np.float32))
    t = ((xs * 0.7 + ys * 0.3) / 1.0)[..., None]
    base = np.array(hex_rgb(bg), np.float32) * (1 - t) + np.array(hex_rgb(bg2), np.float32) * t
    img = Image.fromarray(base.clip(0, 255).astype("uint8"), "RGB").convert("RGBA")
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    A = lambda a: int(max(0, min(255, a * intensity)))

    if kind == "mesh":
        pts = [(rnd.uniform(.1, .9), rnd.uniform(.1, .9), c) for c in (a1, a2, mix(a1, a2, .5), a1)]
        acc = np.zeros((h, w, 3), np.float32)
        wsum = np.zeros((h, w, 1), np.float32)
        for px, py, c in pts:
            wgt = np.exp(-(((xs - px) ** 2) + ((ys - py) ** 2)) / 0.06)[..., None]
            acc += np.array(hex_rgb(c), np.float32) * wgt
            wsum += wgt
        mesh = acc / np.maximum(wsum, 1e-6)
        alpha = (np.clip(wsum, 0, 1) * (0.85 if dark else 0.7) * intensity)
        mixed = base * (1 - alpha) + mesh * alpha
        img = Image.fromarray(mixed.clip(0, 255).astype("uint8"), "RGB").convert("RGBA")
    elif kind == "blobs":
        for i in range(5):
            r = rnd.uniform(.12, .32) * w
            cx, cy = rnd.uniform(.3, 1.05) * w, rnd.uniform(-.1, 1.1) * h
            c = hex_rgb(a1 if i % 2 == 0 else a2)
            d.ellipse([cx - r, cy - r * rnd.uniform(.7, 1.2), cx + r, cy + r], fill=(*c, A(110 if dark else 95)))
        layer = layer.filter(ImageFilter.GaussianBlur(w * 0.04))
    elif kind == "geo":
        for i in range(9):
            c = hex_rgb([a1, a2, mix(a1, bg, .5)][i % 3])
            x0, y0 = rnd.uniform(.45, 1) * w, rnd.uniform(-.1, 1) * h
            s = rnd.uniform(.08, .26) * w
            shape = rnd.choice(["circle", "square", "tri", "ring"])
            al = A(rnd.randint(60, 150) if dark else rnd.randint(40, 110))
            if shape == "circle":
                d.ellipse([x0, y0, x0 + s, y0 + s], fill=(*c, al))
            elif shape == "ring":
                d.ellipse([x0, y0, x0 + s, y0 + s], outline=(*c, al), width=max(6, int(s * .06)))
            elif shape == "square":
                d.rounded_rectangle([x0, y0, x0 + s, y0 + s], radius=s * .18, fill=(*c, al))
            else:
                d.polygon([(x0, y0 + s), (x0 + s / 2, y0), (x0 + s, y0 + s)], fill=(*c, al))
    elif kind == "waves":
        for i in range(6):
            c = hex_rgb(mix(a1, a2, i / 5))
            amp, freq, ph = h * rnd.uniform(.04, .09), rnd.uniform(1.2, 2.4), rnd.uniform(0, 6.28)
            y0 = h * (.45 + i * .1)
            poly = [(x, y0 + amp * math.sin(freq * 2 * math.pi * x / w + ph)) for x in range(0, w + 20, 20)]
            d.polygon(poly + [(w, h), (0, h)], fill=(*c, A(70 if dark else 45)))
    elif kind == "dots":
        step = w // 60
        for gy in range(0, h, step):
            for gx in range(0, w, step):
                f = max(0.0, (gx / w - 0.35) / 0.65) * (1 - abs(gy / h - .5))
                r = step * 0.42 * f
                if r > 0.6:
                    d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(*hex_rgb(a1), A(170 if dark else 120)))
    elif kind == "grid":
        step = w // 32
        for x in range(0, w, step):
            d.line([(x, 0), (x, h)], fill=(*hex_rgb(tk["muted"]), A(28)), width=1)
        for y in range(0, h, step):
            d.line([(0, y), (w, y)], fill=(*hex_rgb(tk["muted"]), A(28)), width=1)
        g = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        gd.ellipse([w * .62, -h * .2, w * 1.1, h * .6], fill=(*hex_rgb(a1), A(120 if dark else 70)))
        layer = Image.alpha_composite(layer, g.filter(ImageFilter.GaussianBlur(w * .05)))
    elif kind == "stripes":
        bw = w // 9
        for i in range(-4, 14):
            c = hex_rgb(a1 if i % 3 == 0 else a2 if i % 3 == 1 else mix(a1, bg, .6))
            x0 = i * bw * 1.2
            d.polygon([(x0, h), (x0 + bw, h), (x0 + bw + h * .6, 0), (x0 + h * .6, 0)], fill=(*c, A(40 if not dark else 70)))
    elif kind == "arcs":
        cx, cy = w * 1.02, h * 0.98
        for i in range(14):
            r = (i + 1) * w * 0.055
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(*hex_rgb(a1 if i % 2 else a2), A(90 if dark else 70)),
                      width=max(3, w // 300))
    else:
        raise ValueError(f"unknown art kind {kind!r}; choose from {KINDS}")

    img = Image.alpha_composite(img, layer).convert("RGB")
    img.save(out, quality=92)
    return str(out)
