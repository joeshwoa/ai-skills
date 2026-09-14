#!/usr/bin/env python3
"""
build_model.py — turns a JSON "model spec" into real 3D geometry: a .glb
(the universal deliverable — opens in Blender, renders in a browser via
<model-viewer>/three.js, and embeds in Flutter via model_viewer_plus) and
optionally .stl/.obj for 3D printing or other CAD tooling.

Usage:
    python3 build_model.py model_spec.json output_basename
    # writes output_basename.glb (+ .stl/.obj per spec["export"])

Why a parametric CSG tree instead of freeform sculpting: this pipeline
guarantees exact, editable, re-runnable geometry — change one number in
the spec and rebuild, instead of hand-editing a mesh. That's the same
"real, structured source of truth" idea premium-presentations uses for
decks (a JSON spec two renderers read), applied to geometry.

ALWAYS run scripts/validate_model.py on the output before handing a model
over — see SKILL.md's "check it before you hand it over" step. A
non-manifold mesh looks fine in a naive preview and then fails silently
in a slicer, a physics engine, or an AR viewer.

Model spec schema: see ../references/model_spec_schema.md
"""
import json
import sys
from pathlib import Path

import numpy as np
import trimesh

sys.path.insert(0, str(Path(__file__).parent))
from primitives import apply_material, apply_transform, boolean_op, make_primitive

UNIT_TO_METERS = {"mm": 0.001, "cm": 0.01, "m": 1.0, "in": 0.0254}

BOOLEAN_TYPES = {"union", "difference", "intersection"}


def build_registry(spec):
    """Walks spec["parts"] in order, building a dict of id -> trimesh.Trimesh.
    Parts are processed strictly in the order given, so a boolean can only
    reference ids that appear earlier in the list — same rule as a
    dependency graph written out by hand."""
    registry = {}
    for part in spec["parts"]:
        pid = part["id"]
        if pid in registry:
            raise ValueError(f"Duplicate part id '{pid}' — every id must be unique.")

        ptype = part["type"]
        if ptype in BOOLEAN_TYPES:
            if ptype == "difference":
                base_id = part["base"]
                sub_ids = part["subtract"]
                missing = [i for i in [base_id, *sub_ids] if i not in registry]
                if missing:
                    raise ValueError(f"Part '{pid}': unknown part id(s) referenced: {missing}")
                mesh = boolean_op("difference", [registry[base_id]] + [registry[i] for i in sub_ids])
            else:
                ids = part["parts"]
                missing = [i for i in ids if i not in registry]
                if missing:
                    raise ValueError(f"Part '{pid}': unknown part id(s) referenced: {missing}")
                mesh = boolean_op(ptype, [registry[i] for i in ids])
            apply_transform(mesh, part)
        else:
            mesh = make_primitive(part)

        registry[pid] = mesh
    return registry


def build_scene(spec):
    registry = build_registry(spec)
    outputs = spec.get("output") or [spec["parts"][-1]["id"]]
    materials_by_id = {p["id"]: p.get("material") for p in spec["parts"]}

    scene = trimesh.Scene()
    for oid in outputs:
        if oid not in registry:
            raise ValueError(f"output id '{oid}' was never built — check spec['output'].")
        mesh = registry[oid].copy()
        apply_material(mesh, materials_by_id.get(oid))
        scene.add_geometry(mesh, node_name=oid, geom_name=oid)
    return scene


def build(spec_path: str, out_basename: str):
    spec = json.loads(Path(spec_path).read_text(encoding="utf-8"))
    scene = build_scene(spec)

    export_cfg = spec.get("export", {"glb": True})
    unit = spec.get("units", "mm")
    scale_to_m = UNIT_TO_METERS.get(unit)
    if scale_to_m is None:
        raise ValueError(f"Unknown units '{unit}'. Use one of: {', '.join(UNIT_TO_METERS)}")

    out_path = Path(out_basename)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    written = []

    if export_cfg.get("glb", True):
        # glTF/GLB's spec assumes meters. Exporting spec-unit numbers
        # unscaled is the #1 cause of "my model is either huge or a
        # speck" bug reports in web/AR viewers, so we always convert.
        glb_scene = scene.copy()
        glb_scene.apply_scale(scale_to_m)
        glb_path = out_path.with_suffix(".glb")
        glb_scene.export(str(glb_path))
        written.append(str(glb_path))

    if export_cfg.get("stl", False):
        # STL/OBJ carry no unit metadata by convention their consumers
        # (slicers, Blender's raw import) usually assume the numbers are
        # already in the tool's working unit — so these stay in the
        # spec's declared units, unscaled, unlike the .glb above.
        stl_path = out_path.with_suffix(".stl")
        if len(scene.geometry) == 1:
            list(scene.geometry.values())[0].export(str(stl_path))
        else:
            combined = trimesh.util.concatenate(list(scene.geometry.values()))
            combined.export(str(stl_path))
        written.append(str(stl_path))

    if export_cfg.get("obj", False):
        obj_path = out_path.with_suffix(".obj")
        scene.export(str(obj_path))
        written.append(str(obj_path))

    n_parts = len(scene.geometry)
    n_faces = sum(len(g.faces) for g in scene.geometry.values())
    print(f"Wrote {', '.join(written)}  ({n_parts} part(s), {n_faces} faces, units={unit})")
    return written


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 build_model.py model_spec.json output_basename")
        sys.exit(1)
    build(sys.argv[1], sys.argv[2])
