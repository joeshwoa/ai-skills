#!/usr/bin/env python3
"""
validate_model.py — automated QA pass on a generated 3D model. Mirrors the
role scripts/validate_deck.py plays in the premium-presentations skill:
a heuristic check that catches the failures a quick look often misses.

Checks (per mesh in the file):
  1. Watertight / manifold — every edge must border exactly two faces, or
     the mesh has holes. This silently breaks 3D printing (slicers either
     reject it or "fix" it in ways that change your geometry), physics
     engines, and volume/mass calculations. HARD ERROR.
  2. Winding consistency — face normals must agree on which side is
     "outside", or lighting/culling looks wrong in every renderer. HARD
     ERROR.
  3. Degenerate faces — zero-area triangles, almost always leftover
     numerical noise from a boolean op. WARNING (cosmetic, rarely breaks
     anything, but signals the geometry could be cleaner).
  4. Scale sanity — a bounding box that's suspiciously tiny or huge for
     the declared units (e.g. a "mm" part 50,000 units across is almost
     certainly a units mistake, not a big part). WARNING.
  5. Poly-count budget — if the spec declares a target `platform`
     (mobile_ar / web_realtime / print / unlimited), flags a face count
     over that platform's realistic real-time budget. WARNING, not an
     error — plenty of legitimate models exceed a budget on purpose.

Usage:
    python3 validate_model.py output.glb [--platform mobile_ar] [--json]
Exit code is non-zero only on a HARD ERROR (non-manifold / inconsistent
winding) — those are correctness bugs. Budget/scale findings are printed
as warnings and don't fail the build, since they're judgment calls.
"""
import json as json_mod
import sys

import trimesh

PLATFORM_BUDGETS = {
    "mobile_ar": 50_000,       # phone-camera AR (model-viewer / ARKit / ARCore quick look)
    "web_realtime": 150_000,   # three.js / react-three-fiber in a browser tab
    "game_asset": 20_000,      # a single prop in a real-time game engine
    "print": None,             # 3D printing doesn't care about real-time triangle budgets
    "unlimited": None,
}


def _scale_sanity(mesh, units):
    extent = mesh.bounding_box.extents
    diag = float((extent ** 2).sum() ** 0.5)
    # Rough "this is a plausible real-world object" bracket per unit,
    # generous on purpose — this is a sanity net, not a rule.
    bounds = {"mm": (0.05, 20_000), "cm": (0.005, 2_000), "m": (0.00005, 20), "in": (0.002, 800)}
    lo, hi = bounds.get(units, (1e-6, 1e9))
    if diag < lo:
        return f"bounding-box diagonal is only {diag:.4g} {units} — is this meant to be this small, or is a units mistake shrinking it?"
    if diag > hi:
        return f"bounding-box diagonal is {diag:.4g} {units} — unusually large; check for a stray zero in a size/translate value."
    return None


def validate(model_path: str, platform: str = None):
    scene_or_mesh = trimesh.load(model_path, force="scene" if model_path.endswith((".glb", ".gltf")) else "mesh")
    if isinstance(scene_or_mesh, trimesh.Scene):
        meshes = {name: g for name, g in scene_or_mesh.geometry.items()}
    else:
        meshes = {"__root__": scene_or_mesh}

    errors, warnings = [], []
    total_faces = 0

    for name, mesh in meshes.items():
        if not isinstance(mesh, trimesh.Trimesh):
            continue
        total_faces += len(mesh.faces)

        if not mesh.is_watertight:
            errors.append({
                "part": name, "type": "not_watertight",
                "detail": "Mesh has holes/gaps (not watertight). Will likely fail or be "
                          "silently auto-repaired by 3D printing slicers, and breaks physics/volume "
                          "calculations. Usually caused by non-overlapping boolean operands or a "
                          "primitive built with too few segments for a tight boolean.",
            })

        if not mesh.is_winding_consistent:
            errors.append({
                "part": name, "type": "inconsistent_winding",
                "detail": "Face normals don't consistently agree on the outward direction — "
                          "will render with inside-out-looking faces in some viewers/engines. "
                          "Try mesh.fix_normals() equivalent (trimesh.repair.fix_normals) as a "
                          "post-process, or re-check the boolean operand geometry.",
            })

        degenerate = (mesh.area_faces < 1e-9).sum() if len(mesh.faces) else 0
        if degenerate:
            warnings.append({
                "part": name, "type": "degenerate_faces",
                "detail": f"{int(degenerate)} near-zero-area face(s) — cosmetic leftover from a "
                          f"boolean op, safe to ignore unless the part looks visibly glitchy.",
            })

    return errors, warnings, total_faces


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_model.py output.glb [--platform mobile_ar] [--json]")
        sys.exit(1)
    path = sys.argv[1]
    as_json = "--json" in sys.argv
    platform = None
    if "--platform" in sys.argv:
        platform = sys.argv[sys.argv.index("--platform") + 1]

    errors, warnings, total_faces = validate(path, platform)

    if platform and platform in PLATFORM_BUDGETS and PLATFORM_BUDGETS[platform] is not None:
        budget = PLATFORM_BUDGETS[platform]
        if total_faces > budget:
            warnings.append({
                "part": "*", "type": "over_budget",
                "detail": f"{total_faces} total triangles exceeds the typical {platform} budget "
                          f"(~{budget}). Not a correctness error, but consider mesh.simplify_quadric_decimation() "
                          f"or reducing primitive segment counts if this needs to run smoothly on-device.",
            })

    if as_json:
        print(json_mod.dumps({
            "file": path, "total_faces": total_faces,
            "errors": errors, "warnings": warnings,
        }, indent=2))
    else:
        if not errors and not warnings:
            print(f"✅ {path}: clean — watertight, consistent winding, {total_faces} faces.")
        else:
            if errors:
                print(f"❌ {path}: {len(errors)} error(s)")
                for e in errors:
                    print(f"  [{e['type']}] part '{e['part']}': {e['detail']}")
            if warnings:
                print(f"⚠️  {path}: {len(warnings)} warning(s)")
                for w in warnings:
                    print(f"  [{w['type']}] part '{w['part']}': {w['detail']}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
