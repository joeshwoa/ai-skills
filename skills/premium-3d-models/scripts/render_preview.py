#!/usr/bin/env python3
"""
render_preview.py — a quick-look image of a generated .glb, since not
everyone reading this has a 3D viewer open. This is a heuristic preview
(matplotlib software shading, no ray tracing) — good enough to sanity
check proportions, hole placement, and color, NOT a substitute for
opening the real .glb in Blender/model-viewer/Flutter to judge material
quality.

Two modes:
  hero       — one nicely lit 3/4 view. Good default for an organic/
               "designer" piece where the point is how it looks.
  multiview  — a 2x2 orthographic sheet (iso / front / top / right) in
               the style of an engineering drawing. Good default for a
               mechanical "engineer" part where proportions and hole
               placement across faces matter more than a pretty angle.
  turntable  — an animated GIF, N frames spinning the hero view. Useful
               for a quick "does this read correctly from every side"
               check, or to hand someone a preview without a 3D viewer.

Usage:
    python3 render_preview.py model.glb out.png --mode hero
    python3 render_preview.py model.glb out.png --mode multiview
    python3 render_preview.py model.glb out.gif --mode turntable --frames 24
"""
import argparse
import io
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from primitives import face_shade_colors

BG_DARK = "#12141C"
BG_LIGHT = "#F3F1EA"


def _load_parts(glb_path):
    """Returns a list of (mesh, base_rgb01) for every real geometry in the
    file, reading each part's own baseColorFactor so multi-material scenes
    shade correctly instead of collapsing to one color."""
    loaded = trimesh.load(glb_path, force="scene")
    parts = []
    geoms = loaded.geometry.values() if isinstance(loaded, trimesh.Scene) else [loaded]
    for mesh in geoms:
        rgb = (0.75, 0.75, 0.78)
        try:
            mat = mesh.visual.material
            base = getattr(mat, "baseColorFactor", None)
            if base is not None:
                vals = [float(c) for c in base[:3]]
                # PBRMaterial.baseColorFactor round-trips through glTF as
                # 0-255 uint8 on read even though it's specified 0-1 —
                # normalize so shading math (which expects 0-1) is correct.
                if max(vals) > 1.0:
                    vals = [v / 255.0 for v in vals]
                rgb = tuple(vals)
        except Exception:
            pass
        parts.append((mesh, rgb))
    return parts


def _combined_bounds(parts):
    mins = np.array([p[0].bounds[0] for p in parts])
    maxs = np.array([p[0].bounds[1] for p in parts])
    lo, hi = mins.min(axis=0), maxs.max(axis=0)
    center = (lo + hi) / 2
    scale = max((hi - lo).max() / 2, 1e-6)
    return center, scale


def _draw(ax, parts, elev, azim, dark, light_dir=(0.45, -0.55, 0.72), ortho=False):
    if ortho:
        ax.set_proj_type("ortho")
    for mesh, rgb in parts:
        colors = face_shade_colors(mesh, rgb, light_dir=light_dir, ambient=0.4 if dark else 0.5)
        tris = mesh.vertices[mesh.faces]
        edge = (1, 1, 1, 0.12) if dark else (0, 0, 0, 0.15)
        coll = Poly3DCollection(tris, facecolors=colors, edgecolor=edge, linewidths=0.15)
        ax.add_collection3d(coll)
    center, scale = _combined_bounds(parts)
    for setter, c in zip((ax.set_xlim, ax.set_ylim, ax.set_zlim), center):
        setter(c - scale * 1.05, c + scale * 1.05)
    ax.set_box_aspect([1, 1, 1])
    ax.view_init(elev=elev, azim=azim)
    ax.axis("off")


def render_hero(glb_path, out_path, dark=True, elev=22, azim=35):
    parts = _load_parts(glb_path)
    bg = BG_DARK if dark else BG_LIGHT
    fig = plt.figure(figsize=(6, 4.5), dpi=180)
    fig.patch.set_facecolor(bg)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor(bg)
    _draw(ax, parts, elev, azim, dark)
    plt.savefig(out_path, facecolor=bg, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return out_path


def render_multiview(glb_path, out_path, dark=True):
    parts = _load_parts(glb_path)
    bg = BG_DARK if dark else BG_LIGHT
    fig = plt.figure(figsize=(8, 6), dpi=170)
    fig.patch.set_facecolor(bg)
    views = [
        ("ISO", 25, 45, False),
        ("FRONT", 0, -90, True),
        ("TOP", 90, -90, True),
        ("RIGHT", 0, 0, True),
    ]
    for i, (label, elev, azim, ortho) in enumerate(views, start=1):
        ax = fig.add_subplot(2, 2, i, projection="3d")
        ax.set_facecolor(bg)
        _draw(ax, parts, elev, azim, dark, ortho=ortho)
        ax.text2D(0.02, 0.94, label, transform=ax.transAxes,
                   color="#D4AF6A" if dark else "#7A5A1E", fontsize=11, fontweight="bold")
    plt.subplots_adjust(wspace=0.02, hspace=0.08)
    plt.savefig(out_path, facecolor=bg, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return out_path


def render_turntable(glb_path, out_path, dark=True, frames=24, elev=20):
    parts = _load_parts(glb_path)
    bg = BG_DARK if dark else BG_LIGHT
    images = []
    for i in range(frames):
        azim = 360 * i / frames
        fig = plt.figure(figsize=(4, 3), dpi=120)
        fig.patch.set_facecolor(bg)
        ax = fig.add_subplot(111, projection="3d")
        ax.set_facecolor(bg)
        _draw(ax, parts, elev, azim, dark)
        buf = io.BytesIO()
        plt.savefig(buf, format="png", facecolor=bg, bbox_inches="tight", pad_inches=0.1)
        plt.close(fig)
        buf.seek(0)
        images.append(Image.open(buf).convert("RGB"))
    w = min(im.width for im in images)
    h = min(im.height for im in images)
    images = [im.resize((w, h)) for im in images]
    images[0].save(out_path, save_all=True, append_images=images[1:], duration=1000 // 12, loop=0)
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("glb_path")
    ap.add_argument("out_path")
    ap.add_argument("--mode", choices=["hero", "multiview", "turntable"], default="hero")
    ap.add_argument("--light-bg", action="store_true", help="Use a light background instead of dark.")
    ap.add_argument("--frames", type=int, default=24)
    args = ap.parse_args()

    dark = not args.light_bg
    if args.mode == "hero":
        render_hero(args.glb_path, args.out_path, dark=dark)
    elif args.mode == "multiview":
        render_multiview(args.glb_path, args.out_path, dark=dark)
    else:
        render_turntable(args.glb_path, args.out_path, dark=dark, frames=args.frames)
    print(f"Wrote {args.out_path}")


if __name__ == "__main__":
    main()
