"""
primitives.py — the CSG building blocks build_model.py uses to turn a
model_spec.json into real trimesh meshes.

Every primitive returns a genuinely closed (watertight/manifold) mesh
wherever the underlying generator supports it, because everything
downstream — booleans, 3D printing, physics engines, even some AR
viewers — breaks or behaves unpredictably on a leaky mesh. If you add a
new primitive type here, check `.is_watertight` on it before trusting it
in a boolean chain.

Boolean ops use the `manifold3d` engine (trimesh's `engine="manifold"`),
which is dramatically more robust than the older blender/scad-subprocess
engines trimesh supports — no external binary required, pure Python
wheel, and it handles coplanar-face and near-degenerate cases that used
to be a common source of "boolean returned an empty/broken mesh" bugs.
"""
import math

import numpy as np
import trimesh
from shapely.geometry import Polygon
from trimesh.visual.material import PBRMaterial

BOOLEAN_ENGINE = "manifold"


def _vec3(v, default=(0.0, 0.0, 0.0)):
    if v is None:
        return np.array(default, dtype=float)
    if isinstance(v, (int, float)):
        return np.array([v, v, v], dtype=float)
    arr = np.array(v, dtype=float)
    if arr.shape != (3,):
        raise ValueError(f"Expected a 3-vector or a single number, got {v!r}")
    return arr


def hex_to_rgb01(hex_color, default=(0.8, 0.8, 0.8)):
    if not hex_color:
        return list(default)
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def apply_transform(mesh, spec):
    """Applies scale -> rotate -> translate, in that order (the order that
    matches how a human reads "make it this size, tip it this way, then
    put it here"). Mutates and returns the mesh."""
    scale = spec.get("scale")
    if scale is not None:
        mesh.apply_scale(_vec3(scale, (1.0, 1.0, 1.0)))

    rotate = spec.get("rotate_deg")
    if rotate is not None:
        rx, ry, rz = _vec3(rotate)
        for axis, deg in ((( 1, 0, 0), rx), ((0, 1, 0), ry), ((0, 0, 1), rz)):
            if deg:
                mesh.apply_transform(
                    trimesh.transformations.rotation_matrix(math.radians(deg), axis)
                )

    translate = spec.get("translate")
    if translate is not None:
        mesh.apply_translation(_vec3(translate))

    return mesh


def make_primitive(part):
    """part: {"type": "...", "params": {...}, "translate"/"rotate_deg"/"scale": ...}"""
    t = part["type"]
    p = part.get("params", {})

    if t == "box":
        extents = _vec3(p.get("size", 1.0), (1.0, 1.0, 1.0))
        mesh = trimesh.creation.box(extents=extents)

    elif t == "sphere":
        seg = int(p.get("segments", 32))
        mesh = trimesh.creation.uv_sphere(radius=p.get("radius", 1.0), count=[seg, seg])

    elif t == "cylinder":
        mesh = trimesh.creation.cylinder(
            radius=p["radius"], height=p["height"], sections=int(p.get("sections", 48))
        )

    elif t == "cone":
        mesh = trimesh.creation.cone(
            radius=p["radius"], height=p["height"], sections=int(p.get("sections", 48))
        )

    elif t == "capsule":
        mesh = trimesh.creation.capsule(radius=p["radius"], height=p["height"])

    elif t == "torus":
        mesh = trimesh.creation.torus(
            major_radius=p["major_radius"], minor_radius=p["minor_radius"],
            major_sections=int(p.get("major_sections", 48)),
            minor_sections=int(p.get("minor_sections", 24)),
        )

    elif t == "ring":  # a flat washer / annulus — r_min hole, r_max outside
        mesh = trimesh.creation.annulus(
            r_min=p["r_min"], r_max=p["r_max"], height=p.get("height", 1.0),
            sections=int(p.get("sections", 48)),
        )

    elif t == "extrude":  # a flat 2D polygon pushed up into a solid
        poly = Polygon(p["polygon"], holes=p.get("holes"))
        if not poly.is_valid:
            poly = poly.buffer(0)
        mesh = trimesh.creation.extrude_polygon(poly, height=p["height"])

    elif t == "revolve":  # a 2D profile spun around the Z axis (vases, bottles, wheels)
        profile = np.array(p["profile"], dtype=float)
        angle_deg = p.get("angle_deg", 360)
        full = angle_deg >= 359.999
        if full and not np.allclose(profile[0], profile[-1]):
            # A full 360 revolve sweeps each *segment* between consecutive
            # points into a band; trimesh does NOT implicitly add a
            # closing segment from the last point back to the first. Without
            # one, the result has an open ring where that segment should
            # have swept into a disk — a real bug this pipeline hit while
            # building the vase example (open bottom cap, not watertight).
            # Auto-closing here means every revolve is watertight by
            # construction instead of silently leaking unless the caller
            # remembers to repeat the first point.
            profile = np.vstack([profile, profile[0]])
        mesh = trimesh.creation.revolve(
            profile,
            angle=None if full else math.radians(angle_deg),
            cap=not full,
            sections=int(p.get("sections", 64)),
        )

    else:
        raise ValueError(
            f"Unknown primitive type '{t}'. Available: box, sphere, cylinder, cone, "
            f"capsule, torus, ring, extrude, revolve."
        )

    apply_transform(mesh, part)
    return mesh


def boolean_op(op_type, meshes):
    """Runs a CSG boolean via the manifold engine. Raises if any operand is
    empty (a common symptom of a typo'd id or a primitive with zero size)."""
    for m in meshes:
        if m is None or len(m.faces) == 0:
            raise ValueError("Boolean operand mesh is empty — check the part it references.")
    if op_type == "union":
        result = trimesh.boolean.union(meshes, engine=BOOLEAN_ENGINE)
    elif op_type == "difference":
        result = trimesh.boolean.difference(meshes, engine=BOOLEAN_ENGINE)
    elif op_type == "intersection":
        result = trimesh.boolean.intersection(meshes, engine=BOOLEAN_ENGINE)
    else:
        raise ValueError(f"Unknown boolean type '{op_type}'. Use union, difference, or intersection.")
    if result is None or len(result.faces) == 0:
        raise ValueError(
            f"Boolean '{op_type}' produced an empty mesh — the operands likely don't "
            f"overlap the way you expect (check positions/sizes)."
        )
    return result


def apply_material(mesh, material):
    """Assigns a PBR material (glTF's native material model — this is what
    ends up in the .glb, and what Blender/three.js/model-viewer all read
    the same way). No material -> a neutral default so nothing exports
    pitch black."""
    material = material or {}
    rgb = hex_to_rgb01(material.get("color"), default=(0.75, 0.75, 0.78))
    alpha = float(material.get("opacity", 1.0))
    emissive_hex = material.get("emissive")
    emissive = hex_to_rgb01(emissive_hex, default=(0, 0, 0)) if emissive_hex else [0, 0, 0]
    mat = PBRMaterial(
        baseColorFactor=[*rgb, alpha],
        metallicFactor=float(material.get("metallic", 0.1)),
        roughnessFactor=float(material.get("roughness", 0.6)),
        emissiveFactor=emissive,
    )
    mesh.visual = trimesh.visual.TextureVisuals(material=mat)
    return mesh


def face_shade_colors(mesh, base_rgb01, light_dir=(0.45, -0.55, 0.72), ambient=0.35):
    """Cheap Lambertian per-face shading for the matplotlib preview
    renderer (not used for the actual export — real materials/lighting
    are the .glb's job, rendered properly by whatever viewer opens it).
    Returns an (n_faces, 4) RGBA array."""
    light = np.array(light_dir, dtype=float)
    light /= np.linalg.norm(light)
    brightness = np.clip(mesh.face_normals @ light, 0, 1)
    brightness = ambient + (1 - ambient) * brightness
    base = np.array(base_rgb01, dtype=float)
    rgb = np.clip(base[None, :] * brightness[:, None], 0, 1)
    alpha = np.ones((len(mesh.faces), 1))
    return np.hstack([rgb, alpha])
