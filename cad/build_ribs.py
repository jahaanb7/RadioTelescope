"""Parametric rib and provisional reflector-skeleton generator.

Reads cad/parameters.yaml and:
  1. rebuilds the supplied outline (Wood_Rib_Frame.stl) and checks it numerically;
  2. builds the assumed physical rib (solid wedge under the parabola);
  3. arrays 18 ribs at 20 deg and measures every pairwise solid overlap,
     untrimmed and with the candidate tip relief;
  4. adds a provisional rear hub disc, rim ring and focus marker;
  5. writes STEP / STL / DXF outputs and analysis/rib_build_report.txt.

Run from the project root:   python3 cad/build_ribs.py
Everything produced here is PROVISIONAL - NOT RELEASED FOR FABRICATION.
"""
import math
import os
import struct
import sys
import warnings

import cadquery as cq
import numpy as np
import yaml

warnings.filterwarnings("ignore", category=FutureWarning)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PARAMS = os.path.join(ROOT, "cad", "parameters.yaml")
OUT_EXPORTS = os.path.join(ROOT, "exports")
OUT_DRAW = os.path.join(ROOT, "drawings")
OUT_ANALYSIS = os.path.join(ROOT, "analysis")
N_SAMPLES = 81


def load_params():
    with open(PARAMS) as fh:
        raw = yaml.safe_load(fh)

    def v(section, key):
        return raw[section][key]["value"]

    return {
        "n": int(v("rib", "count")),
        "R": float(v("rib", "radius_R")),
        "d": float(v("rib", "depth_d")),
        "w": float(v("rib", "thickness_board")),
        "t_outline": float(v("rib", "outline_line_width")),
        "stl_ref": os.path.join(ROOT, v("rib", "reference_stl")),
        "tip_relief": float(v("centre_joint", "tip_relief_radius_candidate")),
        "hub_r": float(v("centre_joint", "hub_disc_radius")),
        "plate_t": float(v("frame", "rear_plate_thickness")),
        "ring_w": float(v("frame", "rim_ring_radial_width")),
    }


def parabola(R, d, r_from=0.0, r_to=None, n=N_SAMPLES):
    f = R * R / (4.0 * d)
    r = np.linspace(r_from, R if r_to is None else r_to, n)
    return f, r, r * r / (4.0 * f), r / (2.0 * f)


def extrude_profile(pts, w):
    """Extrude an (x, z) polygon so the solid occupies Y in [0, w] like the STL."""
    solid = cq.Workplane("XZ").polyline(pts).close().extrude(w)
    bb = solid.val().BoundingBox()
    return solid.translate((0, -bb.ymin, 0))


def wedge_points(p, r_inner=0.0):
    """Solid wedge: flat bottom on z=0, parabolic top, tip at the axis, rim at x=-R.
    r_inner > 0 cuts the tip square at that radius (tip relief)."""
    _f, r, z, _s = parabola(p["R"], p["d"], r_from=r_inner)
    pts = [(-ri, zi) for ri, zi in zip(r, z)]
    pts.append((-p["R"], 0.0))
    if r_inner > 0:
        pts.append((-r_inner, 0.0))
    return pts


def build_outline_rib(p):
    """The supplied STL: 1 mm outline (top strip + bottom chord + rim post), hollow."""
    t = p["t_outline"]
    f = p["R"] ** 2 / (4.0 * p["d"])
    outer = extrude_profile(wedge_points(p), p["w"])

    def strip_bottom(r):
        return r * r / (4 * f) - t * math.sqrt(1 + (r / (2 * f)) ** 2)

    lo, hi = 0.0, p["R"]            # radius where the strip underside meets z = t
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if strip_bottom(mid) < t else (lo, mid)
    r0, r1 = hi, p["R"] - t
    r = np.linspace(r0, r1, N_SAMPLES)
    hole = [(-ri, strip_bottom(ri)) for ri in r] + [(-r1, t), (-r0, t)]
    hole_solid = extrude_profile(hole[:-1], p["w"])
    return outer.cut(hole_solid), r0


def stl_stats(path):
    with open(path, "rb") as fh:
        data = fh.read()
    n = struct.unpack("<I", data[80:84])[0]
    dt = np.dtype([("n", "<3f4"), ("v", "<9f4"), ("a", "<u2")])
    T = np.frombuffer(data[84:84 + 50 * n], dtype=dt)["v"].reshape(-1, 3, 3).astype(float)
    vol = abs(np.einsum("ij,ij->i", T[:, 0], np.cross(T[:, 1], T[:, 2])).sum()) / 6.0
    P = T.reshape(-1, 3)
    return {"triangles": n, "volume": vol, "min": P.min(0), "max": P.max(0), "P": P}


def pair_overlaps(ribs):
    out, max_r, max_z = [], 0.0, 0.0
    for i in range(len(ribs)):
        for j in range(i + 1, len(ribs)):
            shared = ribs[i].val().intersect(ribs[j].val())
            vol = shared.Volume()
            if vol > 1e-6:
                out.append((i, j, vol))
                for vtx in shared.Vertices():
                    max_r = max(max_r, math.hypot(vtx.X, vtx.Y))
                    max_z = max(max_z, vtx.Z)
    return out, max_r, max_z


def array(solid, n):
    return [solid.rotate((0, 0, 0), (0, 0, 1), k * 360.0 / n) for k in range(n)]


def main():
    p = load_params()
    f = p["R"] ** 2 / (4.0 * p["d"])
    lines = []

    def log(msg):
        print(msg)
        lines.append(msg)

    log(f"n={p['n']} R={p['R']} d={p['d']} board={p['w']} f={f:.3f} mm")

    # 1. Outline rib versus the supplied STL
    outline, r0 = build_outline_rib(p)
    log(f"[outline] valid={outline.val().isValid()} volume={outline.val().Volume():.2f} mm^3 "
        f"(hole starts at r={r0:.2f} mm)")
    if os.path.exists(p["stl_ref"]):
        s = stl_stats(p["stl_ref"])
        log(f"[stl]     triangles={s['triangles']} volume={s['volume']:.2f} mm^3 "
            f"bbox min={np.round(s['min'], 3).tolist()} max={np.round(s['max'], 3).tolist()}")
        log(f"[check]   outline/STL volume ratio = {outline.val().Volume() / s['volume']:.5f}")
        face = np.unique(np.round(s["P"][np.isclose(s["P"][:, 1], 0.0)], 4), axis=0)
        rr = -face[:, 0]
        par = rr * rr / (4 * f)
        top = np.isclose(face[:, 2], par, atol=0.01)
        log(f"[check]   {int(top.sum())} STL top-edge vertices, max |z - parabola| = "
            f"{np.max(np.abs(face[top, 2] - par[top])):.5f} mm")
    else:
        log(f"[stl]     reference not found at {p['stl_ref']} - comparison skipped")

    # 2. Assumed physical rib: solid wedge
    wedge = extrude_profile(wedge_points(p), p["w"])
    log(f"[wedge]   valid={wedge.val().isValid()} volume={wedge.val().Volume():.1f} mm^3")
    for rq in (15, 30, 50, 60, 80, 100, 150):
        log(f"[wedge]   height at r={rq:>3} mm = {rq * rq / (4 * f):6.2f} mm; "
            f"gap between adjacent rib faces = {2 * rq * math.sin(math.pi / p['n']) - p['w']:6.2f} mm")

    # 3. Interference, untrimmed and with tip relief
    ov, max_r, max_z = pair_overlaps(array(wedge, p["n"]))
    log(f"[clash]   untrimmed: {len(ov)} overlapping pairs of {p['n'] * (p['n'] - 1) // 2}; "
        f"overlap reaches r={max_r:.2f} mm, z={max_z:.3f} mm, total {sum(o[2] for o in ov):.3f} mm^3")
    relieved = extrude_profile(wedge_points(p, p["tip_relief"]), p["w"])
    ribs = array(relieved, p["n"])
    ov2, _, _ = pair_overlaps(ribs)
    removed = wedge.val().Volume() - relieved.val().Volume()
    log(f"[clash]   tip relief at r={p['tip_relief']} mm: {len(ov2)} overlapping pairs; "
        f"removes {removed:.1f} mm^3 per rib ({100 * removed / wedge.val().Volume():.3f} % of rib), "
        f"cut height {p['tip_relief'] ** 2 / (4 * f):.2f} mm")

    # 4. Provisional rear structure (below the rib bottoms, z = -plate_t .. 0)
    hub = cq.Workplane("XY").workplane(offset=-p["plate_t"]).circle(p["hub_r"]).extrude(p["plate_t"])
    ring = (cq.Workplane("XY").workplane(offset=-p["plate_t"])
            .circle(p["R"]).circle(p["R"] - p["ring_w"]).extrude(p["plate_t"]))
    focus = cq.Workplane("XY").sphere(4.0).translate((0, 0, f))
    bad = 0
    for part in (hub, ring):
        for r_ in ribs:
            if r_.val().intersect(part.val()).Volume() > 1e-6:
                bad += 1
    log(f"[frame]   hub disc r={p['hub_r']} and rim ring width={p['ring_w']}, t={p['plate_t']}: "
        f"{bad} rib/plate volume interferences (ribs rest on z=0 face)")
    log(f"[focus]   focal point at z={f:.3f} mm above vertex, {f - p['d']:.3f} mm above rim plane")

    # 5. Outputs
    for d_ in (OUT_EXPORTS, OUT_DRAW, OUT_ANALYSIS):
        os.makedirs(d_, exist_ok=True)
    asm = cq.Assembly(name="reflector_skeleton_PROVISIONAL")
    for k, r_ in enumerate(ribs):
        asm.add(r_, name=f"RIB-{k + 1:02d}", color=cq.Color(0.82, 0.68, 0.45))
    asm.add(hub, name="HUB-01_rear_disc", color=cq.Color(0.6, 0.45, 0.3))
    asm.add(ring, name="RING-01_rim_ring", color=cq.Color(0.6, 0.45, 0.3))
    asm.add(focus, name="REF_focus_marker", color=cq.Color(1.0, 0.1, 0.1))
    asm.export(os.path.join(OUT_EXPORTS, "reflector_skeleton_PROVISIONAL.step"))
    cq.exporters.export(wedge, os.path.join(OUT_EXPORTS, "RIB_solid_wedge_as_cut.step"))
    cq.exporters.export(relieved, os.path.join(OUT_EXPORTS, "RIB_solid_wedge_tip_relief_PROVISIONAL.step"))
    cq.exporters.export(outline, os.path.join(OUT_EXPORTS, "RIB_outline_reference_matches_STL.step"))
    cq.exporters.export(cq.Workplane().add(cq.Compound.makeCompound(
        [r_.val() for r_ in ribs] + [hub.val(), ring.val(), focus.val()])),
        os.path.join(OUT_EXPORTS, "reflector_skeleton_PROVISIONAL.stl"))
    cq.exporters.export(cq.Workplane("XZ").polyline(wedge_points(p)).close(),
                        os.path.join(OUT_DRAW, "RIB_profile_as_cut_1to1.dxf"))
    with open(os.path.join(OUT_ANALYSIS, "rib_build_report.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    log("outputs written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
