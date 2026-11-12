"""Print preparation for the Rev C printed parts.

Run after cad/build.py:   python3 cad/print_prep.py

For every STL in print/ it
  1. picks the bed orientation with the least overhang: it tries every large flat face of the part
     as the bed face (plus the six axis directions) and scores overhang area (> 45 deg from vertical),
     bed contact and height;
  2. checks the part fits the Prusa CORE One L bed;
  3. estimates filament and print time for PETG at 0.2 mm layers;
  4. rewrites the STL in that orientation and writes print/print_specs.csv.

Time model (rough, +/- 30 %; slice in PrusaSlicer for the real figure): walls and top/bottom skins at
7 mm^3/s, sparse infill at 14 mm^3/s, plus 3 s per layer for travel, retraction and layer change.
"""
import csv
import math
import os
import sys

import numpy as np
import trimesh
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW = yaml.safe_load(open(os.path.join(ROOT, "cad", "parameters.yaml")))
BED = [float(x) for x in RAW["printer"]["build_volume"]["value"]]
MARGIN = float(RAW["printer"]["bed_margin"]["value"])
RHO = float(RAW["petg"]["density_solid"]["value"]) / 1000.0     # g/cm^3
LAYER = 0.2
LINE = 0.45
Q_WALL, Q_INFILL, T_LAYER = 7.0, 14.0, 3.0
OVERHANG_COS = math.cos(math.radians(45))
SUPPORT_LIMIT_CM2 = 4.0          # below this, overhangs are short bridges the printer handles

# Per-part print settings: (perimeters, infill %, top/bottom layers, note)
DEFAULT = (4, 25, 5, "")
SETTINGS = {
    "FKT-01": (6, 40, 6, "Bearing bores must print vertical (kept). Press the 608s in with a vice, not a hammer."),
    "FKT-02": (6, 40, 6, "Bearing bores must print vertical (kept). Slip fit: the bearing should slide in by hand."),
    "FKC-01": (5, 30, 5, "Socket walls carry the fork; do not reduce perimeters."),
    "FKC-02": (5, 30, 5, "Socket walls carry the fork; do not reduce perimeters."),
    "HUB-01": (5, 30, 5, "Large flat part: brim 5 mm, clean bed, 0.2 mm first layer."),
    "RIM-01": (4, 25, 5, "Normal rim bay: side bolts through the ribs only, plain front. Print 10."),
    "RIM-02": (4, 25, 5, "Feed rim bay: side bolts plus front pads for the feed anchor screws. Print 6."),
    "RIM-T": (5, 30, 5, "Carries the elevation axle; do not reduce perimeters."),
    "ELS-01": (5, 40, 6, "Lock sector: clamped by the knob; 100 % infill is fine if you have time."),
    "FLA-01": (4, 25, 5, "Tall: brim 5 mm, slow the top 30 mm if it wobbles."),
    "FRG-01": (4, 25, 5, ""),
    "SPC-01": (4, 25, 5, "Mid-span spacer: one side bolt per rib, plain front. Print 18. Six per plate."),
    "JIG-01": (4, 25, 5, "Drill guide: use a sharp 4.5 mm bit, light pressure."),
    "JIG-02": (4, 25, 5, "Drill guide: use a sharp 4.5 mm bit, light pressure."),
    "KNB-01": (4, 25, 5, "Press an M6 nut into the hex pocket (heat it with a soldering iron if tight)."),
    "SPR-01": (4, 100, 5, "Tiny ring, print solid. An M8 washer (1.6 mm) plus a 0.5 mm shim is an alternative."),
    "SPR-02": (4, 100, 5, "Print solid; it bears on the inner races."),
    "SPR-03": (4, 100, 5, "Print solid."),
    "FIT-01": (4, 25, 5, "PRINT THIS FIRST with exactly the settings and filament you will use for the real parts."),
}
KEEP_ORIENTATION = {"FKT-01", "FKT-02"}   # orientation chosen for strength, not overhang


def rotation_to_down(n):
    """Rotation matrix taking unit vector n to (0, 0, -1)."""
    n = n / np.linalg.norm(n)
    t = np.array([0, 0, -1.0])
    v = np.cross(n, t)
    c = float(np.dot(n, t))
    if np.linalg.norm(v) < 1e-9:
        return np.eye(3) if c > 0 else np.diag([1.0, -1.0, -1.0])
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    return np.eye(3) + vx + vx @ vx * (1 / (1 + c))


def score(m):
    n, c, a = m.face_normals, m.triangles_center, m.area_faces
    zmin = m.bounds[0][2]
    on_bed = (n[:, 2] < -0.99) & (c[:, 2] < zmin + 0.3)
    over = (n[:, 2] < -OVERHANG_COS) & ~on_bed
    return a[over].sum() / 100.0, a[on_bed].sum() / 100.0, m.extents[2]


def fits(m):
    lim = [b - 2 * MARGIN for b in BED]
    x, y, z = m.extents
    return z <= lim[2] and ((x <= lim[0] and y <= lim[1]) or (y <= lim[0] and x <= lim[1]))


def flat_footprint(m):
    """Rotate about Z so the footprint is smallest (helps it fit and pack)."""
    best, best_m = None, m
    for deg in range(0, 180, 5):
        mm = m.copy()
        mm.apply_transform(trimesh.transformations.rotation_matrix(math.radians(deg), [0, 0, 1]))
        area = mm.extents[0] * mm.extents[1]
        if best is None or area < best - 1e-6:
            best, best_m = area, mm
    return best_m


def orient(m, pid):
    facets = sorted(zip(m.facets_area, m.facets_normal), key=lambda t: -t[0])[:25] if len(m.facets) else []
    if pid in KEEP_ORIENTATION:       # only the two orientations that keep the current vertical axis vertical
        cands = [np.array((0, 0, -1.0)), np.array((0, 0, 1.0))]
    else:
        cands = [np.array(v, float) for v in ((0, 0, -1), (0, 0, 1), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0))]
        cands += [nrm for _, nrm in facets]
    min_bed = min(2.0, 0.5 * facets[0][0] / 100.0) if facets else 0.0
    best = None
    for nrm in cands:
        mm = m.copy()
        T = np.eye(4)
        T[:3, :3] = rotation_to_down(nrm)
        mm.apply_transform(T)
        ov, bed, h = score(mm)
        if bed < min_bed:                   # must stand on a real flat face
            continue
        if not fits(flat_footprint(mm)):
            continue
        key = ov - 0.25 * bed + 0.02 * h      # overhang first, then bed contact, then height
        if best is None or key < best[0] - 1e-6:
            best = (key, mm, (ov, bed, h))
    if best is None:
        return m, score(m)
    return best[1], best[2]


def estimate(m, pid):
    per, infill, tb, _ = SETTINGS.get(pid, DEFAULT)
    vol = abs(m.volume) / 1000.0                       # cm^3
    area = m.area / 100.0                              # cm^2
    wall_cm3 = min(vol, area * per * LINE / 10.0)      # walls and skins, approx
    infill_cm3 = max(vol - wall_cm3, 0.0) * infill / 100.0
    grams = (wall_cm3 + infill_cm3) * RHO
    layers = m.extents[2] / LAYER
    sec = (wall_cm3 * 1000 / Q_WALL) + (infill_cm3 * 1000 / Q_INFILL) + layers * T_LAYER
    return grams, sec / 3600.0


def main():
    pdir = os.path.join(ROOT, "print")
    qty = {}
    with open(os.path.join(pdir, "print_list.csv")) as fh:
        for row in csv.DictReader(fh):
            if row["part"] and row["part"] != "ALL" and row["qty"]:
                qty[row["part"]] = (int(row["qty"]), row["name"])
    rows, tot_g, tot_h = [], 0.0, 0.0
    for fn in sorted(os.listdir(pdir)):
        if not fn.endswith(".stl"):
            continue
        pid = fn[:-4]
        m = trimesh.load(os.path.join(pdir, fn))
        m, (ov, bed, h) = orient(m, pid)
        m = flat_footprint(m)
        m.apply_translation(-m.bounds[0])
        m.export(os.path.join(pdir, fn))
        q, name = qty.get(pid, (1, pid))
        g, hrs = estimate(m, pid)
        per, infill, tb, note = SETTINGS.get(pid, DEFAULT)
        sup = "none" if ov < SUPPORT_LIMIT_CM2 else f"yes, build plate only ({ov:.0f} cm2 of overhang)"
        tall = m.extents[2] > 2.5 * min(m.extents[0], m.extents[1])
        brim = "5 mm" if (bed < 15 or tall or "brim" in note) else "no"
        tot_g += g * q
        tot_h += hrs * q
        rows.append(dict(part=pid, name=name, qty=q, size_mm=f"{m.extents[0]:.0f} x {m.extents[1]:.0f} x {m.extents[2]:.0f}",
                         fits_bed="yes" if fits(m) else "NO", perimeters=per, infill=f"{infill}% gyroid",
                         top_bottom_layers=tb, supports=sup, brim=brim, grams_each=round(g), hours_each=round(hrs, 1),
                         grams_total=round(g * q), hours_total=round(hrs * q, 1), notes=note))
        print(f"{pid:8s} x{q:<2d} {rows[-1]['size_mm']:>16s}  overhang {ov:6.1f} cm2  bed {bed:6.1f} cm2  "
              f"{g:5.0f} g  {hrs:4.1f} h  supports: {sup}")
    with open(os.path.join(pdir, "print_specs.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"TOTAL {tot_g / 1000:.2f} kg PETG, about {tot_h:.0f} h of printing")
    return 0 if all(r["fits_bed"] == "yes" for r in rows) else 1


if __name__ == "__main__":
    sys.exit(main())
