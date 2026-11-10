"""Stage 3: provisional complete telescope assembly, checks and exports.

Run from the project root:   python3 cad/build_assembly.py

Frames
  Dish-local: vertex at (0,0,0), +Z toward the sky at zenith pointing, ribs at 20 deg steps
  from +X. The model is built at zenith, so dish-local equals world there.
  Elevation axis: parallel to Y through (0, 0, z_pivot). The dish tips toward +X.

Everything produced is PROVISIONAL - NOT RELEASED FOR FABRICATION.
"""
import csv
import math
import os
import sys
import warnings

import cadquery as cq
import numpy as np
import yaml

warnings.filterwarnings("ignore")

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW = yaml.safe_load(open(os.path.join(ROOT, "cad", "parameters.yaml")))
V = cq.Vector


def P(section, key):
    return RAW[section][key]["value"]


# ---------------------------------------------------------------- parameters
N = int(P("rib", "count"))
R = float(P("rib", "radius_R"))
D_DEPTH = float(P("rib", "depth_d"))
W = float(P("rib", "thickness_board"))
F = R * R / (4 * D_DEPTH)
RELIEF = float(P("centre_joint", "tip_relief_radius_candidate"))
HUB_R = float(P("centre_joint", "hub_disc_radius"))
PT = float(P("frame", "rear_plate_thickness"))
RING_W = float(P("frame", "rim_ring_radial_width"))
CLR = float(P("assembly", "rib_slot_clearance"))
SA_R = float(P("assembly", "saddle_a_radius"))
SB_R = float(P("assembly", "saddle_b_radius"))
SPAR_W, SPAR_H = P("assembly", "spar_section")
BAT_R = P("assembly", "batten_radii")
BAT_RAD, BAT_H = P("assembly", "batten_section")
MESH_KG_M2 = float(P("assembly", "mesh_areal_mass_kg_m2"))
CAN_D = float(P("feed", "can_diameter"))
CAN_L = float(P("feed", "can_length"))
CAN_T = float(P("feed", "can_wall"))
FP1, FP2 = P("feed", "plate_offsets_above_focus")
STRUT = float(P("feed", "strut_section"))
H_PIV = float(P("mount", "pivot_height_above_rocker"))
UP_X, UP_Y = P("mount", "upright_section")
ROCK_X, ROCK_Y, ROCK_T = P("mount", "rocker_board")
GD_R = float(P("mount", "ground_disc_radius"))
LEG_L = float(P("mount", "leg_length"))
EBOX = P("mount", "electronics_box")
EMASS = float(P("mount", "electronics_mass_kg"))
RHO = {k: float(v["value"]) for k, v in RAW["densities_kg_m3"].items()}
RHO["ptfe"] = 2200.0
STEP_DEG = 360.0 / N
HALF = math.radians(STEP_DEG / 2)


def zpar(r):
    return r * r / (4 * F)


# ---------------------------------------------------------------- primitives
def bx(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def cyl(r, h, p, d=(0, 0, 1)):
    return cq.Solid.makeCylinder(r, h, V(*p), V(*d))


def rz(s, a):
    return s.rotate(V(0, 0, 0), V(0, 0, 1), a)


def mirror_y(s):
    return s.mirror("XZ")


def prism(plane, pts, depth, axis, lo):
    """Extrude a polygon drawn on a named plane, then shift so it starts at `lo` on `axis`."""
    s = cq.Workplane(plane).polyline(pts).close().extrude(depth).val()
    bb = s.BoundingBox()
    cur = {"x": bb.xmin, "y": bb.ymin, "z": bb.zmin}[axis]
    shift = {"x": (lo - cur, 0, 0), "y": (0, lo - cur, 0), "z": (0, 0, lo - cur)}[axis]
    return s.translate(V(*shift))


def annulus(r_out, r_in, h, z0):
    return cyl(r_out, h, (0, 0, z0)).cut(cyl(r_in, h, (0, 0, z0)))


PARTS = []


def add(pid, name, solid, material, process, group, check=True):
    PARTS.append(dict(id=pid, name=name, solid=solid, material=material,
                      process=process, group=group, check=check))


# ---------------------------------------------------------------- dish group
def build_dish():
    # Ribs (existing wood) with provisional tip relief, centred on radial planes.
    r = np.linspace(RELIEF, R, 41)
    pts = [(ri, zpar(ri)) for ri in r] + [(R, 0.0), (RELIEF, 0.0)]
    rib = prism("XZ", pts, W, "y", -W / 2)
    for k in range(N):
        add("RIB", f"existing rib {k + 1:02d}", rz(rib, k * STEP_DEG), "plywood", "existing", "dish")

    # Rear plates: hub disc, six 60 deg ring segments, splice plates under the joints.
    add("HUB-01", "rear hub disc", cyl(HUB_R, PT, (0, 0, -PT)), "plywood", "cut", "dish")
    a = np.radians(np.linspace(-30, 30, 25))
    seg_pts = [(R * math.cos(t), R * math.sin(t)) for t in a] + \
              [((R - RING_W) * math.cos(t), (R - RING_W) * math.sin(t)) for t in a[::-1]]
    seg = prism("XY", seg_pts, PT, "z", -PT)
    for k in range(6):
        add("RING-01", f"rim ring segment {k + 1}", rz(seg, 30 + 60 * k), "plywood", "cut", "dish")
        add("SPL-01", f"ring splice plate {k + 1}",
            rz(bx(R - RING_W + 2, R - 2, -75, 75, -2 * PT, -PT), 60 * k), "plywood", "cut", "dish")
        add("SPAR-01", f"rear spar {k + 1}",
            rz(bx(30, R, -SPAR_W / 2, SPAR_W / 2, -PT - SPAR_H, -PT), 30 + 60 * k), "softwood", "cut", "dish")
    add("CAP-01", "centre mesh support disc", cyl(RELIEF, zpar(RELIEF), (0, 0, 0)), "printed", "print", "dish")

    # Rib clamps: two cheeks per station, holes for one plate screw and one cross bolt.
    def cheek(r_mid, height, bolt_z, cross_d, side):
        y0, y1 = (W + CLR) / 2, (W + CLR) / 2 + 17.0
        s = bx(r_mid - 15, r_mid + 15, y0, y1, 0, height)
        s = s.cut(cyl(2.25, height + 2, (r_mid, (y0 + y1) / 2 + 3, -1)))
        s = s.cut(cyl(cross_d / 2, 40, (r_mid, y0 - 1, bolt_z), (0, 1, 0)))
        return s if side > 0 else mirror_y(s)

    for k in range(N):
        for side in (1, -1):
            add("SAD-A", f"inner rib cheek r{k + 1:02d}", rz(cheek(SA_R, 14.0, 8.0, 3.4, side), k * STEP_DEG),
                "printed", "print", "dish")
            add("SAD-B", f"outer rib cheek r{k + 1:02d}", rz(cheek(SB_R, 45.0, 25.0, 4.5, side), k * STEP_DEG),
                "printed", "print", "dish")

    # Straight mesh-support battens between neighbouring ribs.
    for i, rb in enumerate(BAT_R):
        rm = rb * math.cos(HALF)
        # Square-cut ends: the inner corner is the one that reaches the angled rib face first.
        half_len = (rm - BAT_RAD / 2) * math.tan(HALF) - (W / 2) / math.cos(HALF) - 0.5
        top = zpar(rb) - 1.0
        bat = bx(rm - BAT_RAD / 2, rm + BAT_RAD / 2, -half_len, half_len, top - BAT_H, top)
        for k in range(N):
            add(f"BAT-{i + 1:02d}", f"mesh batten r={rb:.0f} #{k + 1:02d}",
                rz(bat, STEP_DEG / 2 + k * STEP_DEG), "softwood", "cut", "dish")

    # Trunnion plates on the elevation axis and two rim posts for the other feed legs.
    top_z = 170.0
    for side in (1, -1):
        tp = bx(-90, 90, R, R + PT, -PT - SPAR_H, top_z)
        add("TRUN-01", "trunnion plate " + ("+Y" if side > 0 else "-Y"), tp if side > 0 else mirror_y(tp),
            "plywood", "cut", "dish")
    for ang in (30, 150):
        add("POST-01", f"feed-leg rim post {ang} deg",
            rz(bx(R, R + 20, -22.5, 22.5, -PT - SPAR_H, top_z), ang), "softwood", "cut", "dish")

    # Feed support: three legs, two plywood rings, three spacer posts, two collars.
    z1, z2 = F + FP1, F + FP2
    for ang in (30, 150, 270):
        t = math.radians(ang)
        p0 = np.array([(R + 6) * math.cos(t), (R + 6) * math.sin(t), top_z])
        p1 = np.array([112 * math.cos(t), 112 * math.sin(t), z1])
        d = (p1 - p0) / np.linalg.norm(p1 - p0)
        length = np.linalg.norm(p1 - p0) - 30.0
        start = p0 + 15.0 * d
        plane = cq.Plane(origin=tuple(start), xDir=(-math.sin(t), math.cos(t), 0), normal=tuple(d))
        add("LEG-01", f"feed leg {ang} deg", cq.Workplane(plane).rect(STRUT, STRUT).extrude(length).val(),
            "softwood", "cut", "dish", check=False)
    hole_r = CAN_D / 2 + 3
    add("FPL-01", "feed ring lower", annulus(125, hole_r, PT, z1), "plywood", "cut", "dish")
    add("FPL-01", "feed ring upper", annulus(125, hole_r, PT, z2), "plywood", "cut", "dish")
    for ang in (90, 210, 330):
        add("FPO-01", f"feed ring spacer {ang} deg", rz(bx(96, 114, -9, 9, z1 + PT, z2), ang),
            "softwood", "cut", "dish")
    for zc in (z1 + PT, z2 + PT):
        add("COL-01", "feed can clamp collar", annulus(88, CAN_D / 2 + 0.3, 20, zc), "printed", "print", "dish")
    can = cyl(CAN_D / 2, CAN_L, (0, 0, F)).cut(cyl(CAN_D / 2 - CAN_T, CAN_L - CAN_T, (0, 0, F)))
    add("FEED-01", "feed can (conductive, provisional)", can, "steel", "purchase/make", "dish")
    add("LNA-BOX", "LNA enclosure envelope", bx(90, 130, -45, 45, z2 + PT, z2 + PT + 35), "printed", "print", "dish")

    # Representative mesh surface (0.5 mm shell on the ideal paraboloid); mass by area.
    rr = np.linspace(RELIEF, R, 41)
    band = [(ri, zpar(ri)) for ri in rr] + [(ri, zpar(ri) + 0.5) for ri in rr[::-1]]
    mesh = cq.Workplane("XZ").polyline(band).close().revolve(360, (0, 0, 0), (0, 1, 0)).val()
    add("MESH-01", "reflector mesh, representative ideal surface", mesh, "mesh", "purchase", "dish", check=False)


def mesh_area_m2():
    r = np.linspace(RELIEF, R, 2001)
    ds = np.sqrt(1 + (r / (2 * F)) ** 2)
    return float(np.trapezoid(2 * np.pi * r * ds, r)) / 1e6 + math.pi * RELIEF ** 2 / 1e6


def mass_kg(part):
    if part["material"] == "mesh":
        return MESH_KG_M2 * mesh_area_m2()
    if part["id"] == "EBOX-01":
        return EMASS
    return part["solid"].Volume() * 1e-9 * RHO[part["material"]]


def group_cg(group):
    m_tot, mom = 0.0, np.zeros(3)
    for p in PARTS:
        if p["group"] != group:
            continue
        m = mass_kg(p)
        c = p["solid"].Center()
        m_tot += m
        mom += m * np.array([c.x, c.y, c.z])
    return m_tot, mom / m_tot


# ---------------------------------------------------------------- mount group
def build_mount(zp):
    z_rt = zp - H_PIV
    # Elevation quadrant on the +Y trunnion (moves with the dish).
    ang = np.radians(np.linspace(-102, 12, 39))
    qpts = [(0.0, zp)] + [(180 * math.cos(t), zp + 180 * math.sin(t)) for t in ang]
    add("QUAD-01", "elevation clamp quadrant", prism("XZ", qpts, PT, "y", R + PT), "plywood", "cut", "dish")

    y0 = R + PT + PT + 6  # trunnion plate, quadrant, washer gap
    for side in (1, -1):
        up = bx(-UP_X / 2, UP_X / 2, y0, y0 + UP_Y, z_rt, zp + 60)
        add("UPR-01", "fork upright " + ("+Y" if side > 0 else "-Y"), up if side > 0 else mirror_y(up),
            "softwood", "cut", "mount")
        for xs in (UP_X / 2, -UP_X / 2 - PT):
            g = prism("YZ", [(y0, z_rt), (y0 - 250, z_rt), (y0, z_rt + 300)], PT, "x", xs)
            add("GUS-01", "upright gusset", g if side > 0 else mirror_y(g), "plywood", "cut", "mount")
    add("ROCK-01", "rocker board", bx(-ROCK_X / 2, ROCK_X / 2, -ROCK_Y / 2, ROCK_Y / 2, z_rt - ROCK_T, z_rt),
        "plywood", "cut", "mount")
    zg = z_rt - ROCK_T - 5
    for a_ in (90, 210, 330):
        add("GLIDE", f"PTFE azimuth glide {a_} deg", rz(cyl(12.5, 5, (220, 0, zg)), a_), "ptfe", "purchase", "mount")
        add("LEG-GND", f"ground leg {a_} deg", rz(bx(60, 60 + LEG_L, -45, 45, zg - 18 - 45, zg - 18), a_),
            "softwood", "cut", "mount")
        add("FOOT", f"levelling foot {a_} deg", rz(cyl(15, 20, (45 + LEG_L, 0, zg - 18 - 45 - 20)), a_),
            "steel", "purchase", "mount")
    add("GND-01", "ground disc", cyl(GD_R, 18, (0, 0, zg - 18)), "plywood", "cut", "mount")
    add("EBOX-01", "digital electronics enclosure envelope",
        bx(70, 70 + EBOX[0], 300, 300 + EBOX[1], z_rt, z_rt + EBOX[2]), "printed", "print", "mount")
    # Hardware shown for reference only; excluded from interference checks.
    for side in (1, -1):
        b = cyl(5, 110, (0, R - 6, zp), (0, 1, 0))
        add("HW-M10-PIV", "M10 elevation pivot bolt", b if side > 0 else mirror_y(b), "steel", "purchase", "hardware", False)
    add("HW-M8-LOCK", "M8 elevation clamp bolt", cyl(4, 80, (0, R + PT - 4, zp - 150), (0, 1, 0)),
        "steel", "purchase", "hardware", False)
    add("HW-M10-AZ", "M10 azimuth pivot bolt", cyl(5, 100, (0, 0, zg - 18 - 45 - 10)), "steel", "purchase", "hardware", False)
    return z_rt, zg - 18 - 45 - 20  # rocker top, ground level


# ---------------------------------------------------------------- checks
def bb_overlap(a, b, tol=0.0):
    return not (a.xmax < b.xmin - tol or b.xmax < a.xmin - tol or a.ymax < b.ymin - tol or
                b.ymax < a.ymin - tol or a.zmax < b.zmin - tol or b.zmax < a.zmin - tol)


def overlaps(list_a, list_b=None, min_vol=1.0):
    """Pairs of solids sharing more than min_vol mm^3."""
    found = []
    bbs_a = [p["solid"].BoundingBox() for p in list_a]
    same = list_b is None
    list_b = list_a if same else list_b
    bbs_b = bbs_a if same else [p["solid"].BoundingBox() for p in list_b]
    for i, pa in enumerate(list_a):
        for j, pb in enumerate(list_b):
            if same and j <= i:
                continue
            if not bb_overlap(bbs_a[i], bbs_b[j]):
                continue
            vol = pa["solid"].intersect(pb["solid"]).Volume()
            if vol > min_vol:
                found.append((pa["id"], pa["name"], pb["id"], pb["name"], vol))
    return found


def facet_error():
    """Normal-direction error of a mesh pulled straight between neighbouring ribs,
    relative to the ideal paraboloid. Returns raw RMS, RMS after refitting a paraboloid
    (new focal length and axial offset), the fitted focal length, and the peak error."""
    rs = np.linspace(RELIEF, R, 400)
    ph = np.linspace(-HALF, HALF, 81)
    rg, pg = np.meshgrid(rs, ph)
    rho = rg * math.cos(HALF) / np.cos(pg)          # radius of the point on the chord
    z_mesh = zpar(rg)
    cosn = 1 / np.sqrt(1 + (rho / (2 * F)) ** 2)
    wgt = rho                                        # area weight
    err = (z_mesh - zpar(rho)) * cosn
    raw = math.sqrt(np.average(err ** 2, weights=wgt))
    A = np.vstack([np.ones(rho.size), rho.ravel() ** 2]).T
    sw = np.sqrt(wgt.ravel())
    coef, *_ = np.linalg.lstsq(A * sw[:, None], z_mesh.ravel() * sw, rcond=None)
    fit = (z_mesh - (coef[0] + coef[1] * rho ** 2)) * cosn
    return raw, math.sqrt(np.average(fit ** 2, weights=wgt)), 1 / (4 * coef[1]), float(err.max()), float(coef[0])


def main():
    out = []

    def log(s=""):
        print(s)
        out.append(s)

    build_dish()
    m0, cg0 = group_cg("dish")
    zp = float(round(cg0[2]))
    z_rt, z_ground = build_mount(zp)
    m_dish, cg = group_cg("dish")
    m_mount, cg_m = group_cg("mount")

    log("# Stage 3 provisional assembly report")
    log("")
    log("Generated by `cad/build_assembly.py`. Modelled and analytically checked only; nothing")
    log("physically tested. All masses use generic densities. **NOT RELEASED FOR FABRICATION.**")
    log("")
    log("## Solids")
    bad = [p for p in PARTS if not p["solid"].isValid()]
    log(f"- {len(PARTS)} solids built, {len(bad)} invalid.")
    counts = {}
    for p in PARTS:
        counts[p["id"]] = counts.get(p["id"], 0) + 1
    log("- Part counts: " + ", ".join(f"{k} x{v}" for k, v in counts.items()))
    log(f"- Ribs in assembly: {counts.get('RIB', 0)} (required 18).")

    log("")
    log("## Mass and balance")
    log(f"- Moving dish group: {m_dish:.2f} kg, centre of mass at x={cg[0]:.1f}, y={cg[1]:.1f}, z={cg[2]:.1f} mm (dish-local).")
    log(f"- Elevation pivot set at z = {zp:.0f} mm. Residual offset of centre of mass from the pivot axis: "
        f"dx={cg[0]:.1f}, dz={cg[2] - zp:.1f} mm.")
    log(f"- Mount group: {m_mount:.2f} kg. Total: {m_dish + m_mount:.2f} kg.")
    log(f"- Mesh area {mesh_area_m2():.3f} m^2, mass {MESH_KG_M2 * mesh_area_m2():.2f} kg at the assumed {MESH_KG_M2} kg/m^2.")
    log(f"- Pivot height above ground: {zp - z_ground:.0f} mm. Rocker top is {H_PIV:.0f} mm below the pivot.")

    log("")
    log("## Interference checks (solid intersections over 1 mm^3)")
    dish = [p for p in PARTS if p["group"] == "dish" and p["check"]]
    mount = [p for p in PARTS if p["group"] == "mount" and p["check"]]
    ov = overlaps(dish)
    log(f"- Within the dish group ({len(dish)} solids; mesh, feed legs and bolts excluded): {len(ov)} interfering pairs.")
    for o in ov[:20]:
        log(f"  - {o[0]} ({o[1]}) with {o[2]} ({o[3]}): {o[4]:.1f} mm^3")
    ov = overlaps(mount)
    log(f"- Within the mount group ({len(mount)} solids): {len(ov)} interfering pairs.")
    for o in ov[:20]:
        log(f"  - {o[0]} ({o[1]}) with {o[2]} ({o[3]}): {o[4]:.1f} mm^3")
    legs = [p for p in PARTS if p["id"] == "LEG-01"]
    ov = overlaps(legs, [p for p in dish if p["id"] not in ("TRUN-01", "POST-01", "FPL-01")])
    log(f"- Feed legs against ribs, battens, clamps, can and collars: {len(ov)} interfering pairs.")
    for o in ov[:20]:
        log(f"  - {o[0]} ({o[1]}) with {o[2]} ({o[3]}): {o[4]:.1f} mm^3")

    log("")
    log("### Elevation sweep, moving group against mount")
    log("")
    log("| Elevation | Interfering pairs | Lowest point of dish group above ground |")
    log("|---:|---:|---:|")
    moving = [p for p in PARTS if p["group"] == "dish" and p["id"] != "MESH-01"]
    clear_range = []
    for el in (90, 75, 60, 45, 30, 15, 0, -5):
        th = 90 - el
        rot = [dict(p, solid=p["solid"].rotate(V(0, 0, zp), V(0, 1, zp), th)) for p in moving]
        ov = overlaps(rot, mount)
        low = min(p["solid"].BoundingBox().zmin for p in rot) - z_ground
        log(f"| {el} deg | {len(ov)} | {low:.0f} mm |")
        for o in ov[:6]:
            log(f"| | {o[0]} with {o[2]} ({o[3]}): {o[4]:.0f} mm^3 | |")
        if not ov:
            clear_range.append(el)
    log("")
    log(f"Clear at sampled elevations: {sorted(clear_range)} deg. Cables and fasteners are not modelled.")

    # ------------------------------------------------------------ RF geometry
    lam = 299792.458 / float(P("rf", "hydrogen_line_mhz"))
    raw, fit, f_fit, peak, a0 = facet_error()
    log("")
    log("## Reflector surface and RF geometry (calculated)")
    log(f"- Wavelength {lam:.2f} mm; f = {F:.3f} mm; f/D = {F / (2 * R):.4f}; focus {F - D_DEPTH:.1f} mm above the rim plane.")
    log(f"- Rim half-angle from the focus: {2 * math.degrees(math.atan(R / (2 * F))):.2f} deg. "
        f"Extra path loss at the rim: {20 * math.log10(1 + (R / (2 * F)) ** 2):.2f} dB.")
    log(f"- Half-power beamwidth, rough estimate 70*lambda/D: {70 * lam / (2 * R):.1f} deg.")
    log(f"- Mesh pulled straight between 18 ribs sits above the ideal surface by up to {peak:.2f} mm "
        f"(at the rim, midway between ribs). Raw RMS {raw:.2f} mm.")
    log(f"- That error is mostly a change of focal length. Best-fit paraboloid: f = {f_fit:.1f} mm "
        f"({f_fit - F:+.1f} mm), vertex offset {a0:+.2f} mm, residual RMS {fit:.2f} mm.")
    for e, label in ((fit, "faceting residual alone"), (2.0, "2 mm RMS"), (3.0, "3 mm RMS"), (5.0, "5 mm RMS target")):
        log(f"  - Ruze surface factor at {label} ({e:.2f} mm): {math.exp(-(4 * math.pi * e / lam) ** 2):.4f}")
    fc11 = 299792.458 / (1.7063 * CAN_D)
    fc01 = 299792.458 / (1.3065 * CAN_D)
    lg = lam / math.sqrt(1 - (lam / (1.7063 * CAN_D)) ** 2)
    log(f"- Provisional feed can, {CAN_D:.0f} mm diameter: TE11 cut-off {fc11:.0f} MHz, TM01 cut-off {fc01:.0f} MHz, "
        f"guide wavelength {lg:.1f} mm, quarter-wave probe distance from the closed end {lg / 4:.1f} mm, "
        f"0.75 guide wavelengths = {0.75 * lg:.0f} mm. Formula values only; not a validated feed.")
    blocked = (math.pi * (CAN_D / 2) ** 2 + 3 * STRUT * (R - CAN_D / 2)) / (math.pi * R * R)
    log(f"- Geometric blockage by the can and three legs (projected, screening): {100 * blocked:.1f} % of the aperture.")

    # ------------------------------------------------------------ structural screening
    g = 9.81
    area = math.pi * (R / 1000) ** 2
    h = (zp - z_ground) / 1000
    foot_r = (45 + LEG_L) / 1000
    d_tip = foot_r * math.cos(math.radians(60))
    wt = (m_dish + m_mount) * g
    log("")
    log("## Structural screening (calculated, conservative solid-disc drag)")
    log(f"Assumptions: air density 1.225 kg/m^3, drag coefficient 1.2 on the full {area:.3f} m^2 disc, dish at the horizon, "
        f"force applied at pivot height {h:.3f} m, three feet at {foot_r:.3f} m radius (tipping distance {d_tip:.3f} m), "
        f"no ballast, friction coefficient 0.4 for sliding.")
    log("")
    log("| Wind speed | Drag | Overturning moment | Resisting moment | Ratio | Sliding ratio |")
    log("|---:|---:|---:|---:|---:|---:|")
    for v in (3, 5, 8, 10, 15):
        drag = 0.5 * 1.225 * v * v * 1.2 * area
        log(f"| {v} m/s | {drag:.1f} N | {drag * h:.1f} N m | {wt * d_tip:.1f} N m | {wt * d_tip / (drag * h):.2f} | {0.4 * wt / drag:.2f} |")
    v_lim = math.sqrt(wt * d_tip / 1.5 / h / (0.5 * 1.225 * 1.2 * area))
    log("")
    log(f"- Wind speed at which the overturning ratio falls to 1.5 with no ballast: {v_lim:.1f} m/s. "
        f"Ballast needed on the legs for ratio 1.5 at 10 m/s: "
        f"{max(0.0, (1.5 * 0.5 * 1.225 * 100 * 1.2 * area * h / d_tip - wt) / g):.1f} kg.")
    imb = m_dish * g * (math.hypot(cg[0], cg[2] - zp) + 20) / 1000
    wind_t = 0.5 * 1.225 * 25 * 1.2 * area * 0.1 * 2 * R / 1000
    log(f"- Elevation clamp: torque from imbalance with a 20 mm mass-position allowance {imb:.2f} N m, plus wind torque at 5 m/s "
        f"with the pressure centre 0.1 D off-axis {wind_t:.2f} N m. Friction force needed at the 150 mm clamp radius: "
        f"{(imb + wind_t) / 0.15:.0f} N.")
    leg_len = math.hypot(R + 6 - 112, F + FP1 - 170) - 30
    inertia = STRUT ** 4 / 12
    pcr = math.pi ** 2 * 8000 * inertia / leg_len ** 2
    feed_m = sum(mass_kg(p) for p in PARTS if p["id"] in ("FEED-01", "COL-01", "FPL-01", "FPO-01", "LNA-BOX"))
    log(f"- Feed head mass {feed_m:.2f} kg. Feed leg length {leg_len:.0f} mm, {STRUT:.0f} mm square; Euler buckling load with an "
        f"assumed E = 8 GPa: {pcr:.0f} N per leg, against a feed weight of {feed_m * g:.1f} N. Leg axial stiffness "
        f"{8000 * STRUT ** 2 / leg_len:.0f} N/mm, so member stretch is negligible and joint slip will govern feed movement. "
        f"That must be measured.")
    log(f"- Pivot bolts: each M10 carries about {m_dish * g / 2:.0f} N in shear. Wood bearing at the trunnion plate, "
        f"12 mm ply on a 10 mm bolt: {m_dish * g / 2 / (10 * PT):.2f} MPa average.")
    log("- Not checked: rib bending, ring twist, printed-clamp strength and creep, fastener pull-out, wood splitting. "
        "No finite-element analysis was run.")

    # ------------------------------------------------------------ outputs
    ex, pr, dr, bom = (os.path.join(ROOT, d) for d in ("exports", "print", "drawings", "bom"))
    for d in (ex, pr, dr, bom, os.path.join(ex, "parts")):
        os.makedirs(d, exist_ok=True)
    colors = {"plywood": (0.80, 0.66, 0.44), "softwood": (0.90, 0.80, 0.58), "printed": (0.20, 0.45, 0.75),
              "steel": (0.65, 0.65, 0.68), "mesh": (0.75, 0.75, 0.75), "ptfe": (0.95, 0.95, 0.95)}
    asm = cq.Assembly(name="telescope_PROVISIONAL_zenith")
    seen = {}
    for p in PARTS:
        seen[p["id"]] = seen.get(p["id"], 0) + 1
        col = cq.Color(*colors[p["material"]], 0.35 if p["material"] == "mesh" else 1.0)
        asm.add(p["solid"], name=f"{p['id']}_{seen[p['id']]:02d}", color=col)
    asm.export(os.path.join(ex, "telescope_assembly_PROVISIONAL_zenith.step"))

    first = {}
    for p in PARTS:
        first.setdefault(p["id"], p)
    for pid, p in first.items():
        if p["group"] == "hardware" or pid in ("MESH-01", "RIB", "GLIDE", "FOOT"):
            continue
        cq.exporters.export(cq.Workplane().add(p["solid"]), os.path.join(ex, "parts", f"{pid}.step"))
        if p["process"] == "print" and pid not in ("LNA-BOX", "EBOX-01"):
            cq.exporters.export(cq.Workplane().add(p["solid"]), os.path.join(pr, f"{pid}_PROVISIONAL.stl"))

    # Fit coupon: five slots around the nominal board thickness.
    coupon = bx(0, 75, 0, 20, 0, 12)
    for i, dw in enumerate((-0.2, 0.0, 0.2, 0.4, 0.6)):
        xc = 10 + 14 * i
        coupon = coupon.cut(bx(xc - (W + dw) / 2, xc + (W + dw) / 2, -1, 21, 4, 13))
    cq.exporters.export(cq.Workplane().add(coupon), os.path.join(pr, "FIT-COUPON_rib_slot.stl"))

    # Flat-part outlines at 1:1 in mm.
    dxf_done, dxf_fail = [], []
    planes = {"HUB-01": "XY", "RING-01": "XY", "SPL-01": "XY", "FPL-01": "XY", "ROCK-01": "XY", "GND-01": "XY",
              "TRUN-01": "XZ", "QUAD-01": "XZ", "GUS-01": "YZ"}
    for pid, pl in planes.items():
        s = first[pid]["solid"]
        c = s.Center()
        try:
            sec = cq.Workplane(pl, origin=(c.x, c.y, c.z)).add(s).section()
            cq.exporters.export(sec, os.path.join(dr, f"{pid}_outline_PROVISIONAL.dxf"))
            dxf_done.append(pid)
        except Exception as exc:  # report, never hide
            dxf_fail.append(f"{pid}: {exc}")

    # Hidden-line views.
    comp = cq.Compound.makeCompound([p["solid"] for p in PARTS if p["id"] != "MESH-01"])
    # Rotate the model into screen axes (x right, y up, z toward the viewer), then project along z.
    views = {"iso": [((0, 0, 1), -30), ((1, 0, 0), -62)],
             "side_along_elevation_axis": [((1, 0, 0), -90)],
             "front_along_x": [((0, 0, 1), -90), ((1, 0, 0), -90)],
             "top": []}
    svg_fail = []
    for name, rots in views.items():
        try:
            shp = comp
            for axis, deg in rots:
                shp = shp.rotate(V(0, 0, 0), V(*axis), deg)
            cq.exporters.export(cq.Workplane().add(shp), os.path.join(dr, f"view_{name}_zenith.svg"),
                                opt={"projectionDir": (0, 0, 1), "showAxes": False, "showHidden": False,
                                     "width": 1400, "height": 1000, "strokeWidth": 0.6})
        except Exception as exc:
            svg_fail.append(f"{name}: {exc}")

    # BOM.
    rows = {}
    for p in PARTS:
        r_ = rows.setdefault(p["id"], dict(id=p["id"], description=p["name"], qty=0, material=p["material"],
                                           process=p["process"], group=p["group"], mass_each_kg=0.0, bbox_mm=""))
        r_["qty"] += 1
        if r_["qty"] == 1:
            bb = p["solid"].BoundingBox()
            dims = sorted([bb.xlen, bb.ylen, bb.zlen], reverse=True)
            r_["mass_each_kg"] = round(mass_kg(p), 3)
            r_["bbox_mm"] = " x ".join(f"{d_:.0f}" for d_ in dims)
    with open(os.path.join(bom, "bom_PROVISIONAL.csv"), "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=["id", "description", "qty", "material", "process", "group",
                                            "mass_each_kg", "bbox_mm", "owned_or_new", "est_price_cad", "source"])
        wr.writeheader()
        for r_ in rows.values():
            r_["owned_or_new"] = "owned" if r_["id"] == "RIB" else "new"
            r_["est_price_cad"] = "not yet sourced"
            r_["source"] = "not yet sourced"
            wr.writerow(r_)

    log("")
    log("## Files written")
    log(f"- `exports/telescope_assembly_PROVISIONAL_zenith.step` ({len(PARTS)} named solids)")
    log(f"- `exports/parts/` one STEP per manufactured part type")
    log(f"- `print/` STL for printed part types and `FIT-COUPON_rib_slot.stl`")
    log(f"- `drawings/` DXF outlines written for: {', '.join(dxf_done)}" + (f"; FAILED: {dxf_fail}" if dxf_fail else ""))
    log(f"- `drawings/view_*_zenith.svg`" + (f"; FAILED: {svg_fail}" if svg_fail else ""))
    log("- `bom/bom_PROVISIONAL.csv`")
    with open(os.path.join(ROOT, "analysis", "assembly_report.md"), "w") as fh:
        fh.write("\n".join(out) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
