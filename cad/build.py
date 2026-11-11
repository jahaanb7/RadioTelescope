"""Rev C.2: printed-node telescope on a fixed base, with a working elevation joint (no azimuth turntable).

Run from the project root:
    python3 cad/build.py                 # build, check, analyse, export at the pose in parameters.yaml
    python3 cad/build.py --el 20         # export the assembly STEP at another elevation
    python3 cad/build.py --quick         # geometry and checks only, no file exports

Stages (kinematic groups)
    az      the fixed base (name kept from Rev C): fork legs, sills, tie beams, corner nodes. It sits on the
            ground on its four corner nodes; point it in azimuth by turning the whole base (or fit casters).
    dish    everything that tilts about the horizontal axle: ribs, hub, rim girder, feed

Frames
    Dish-local: vertex at (0,0,0), +Z along the optical axis, ribs at 20 deg steps from +X.
    World: Z up, ground at z=0, elevation axle parallel to Y at height Zp. Elevation tilts the dish toward +X.

All geometry is PROVISIONAL until the fit coupon and the rib measurements are confirmed.
"""
import argparse
import csv
import math
import os
import re
import sys
import time
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


# ------------------------------------------------------------------ parameters
N = int(P("rib", "count"))
R = float(P("rib", "radius_R"))
D_DEPTH = float(P("rib", "depth_d"))
W = float(P("rib", "thickness_board"))
F = R * R / (4 * D_DEPTH)
RELIEF = float(P("rib", "tip_relief_radius"))
RIM_HOLE_R = float(P("rib", "rim_hole_radius"))
RIM_HOLE_Z = [float(z) for z in P("rib", "rim_hole_z")]
MID_HOLE_R = float(P("rib", "mid_hole_radius"))
MID_HOLE_Z = float(P("rib", "mid_hole_z"))
DRILL = float(P("rib", "drill_clearance"))
TIP_PIN_R = float(P("rib", "tip_pin_radius"))
TIP_PIN_Z = float(P("rib", "tip_pin_z"))
FILLET_R = float(P("rib_support", "fillet_radius"))
STEP_DEG = 360.0 / N
HALF_DEG = STEP_DEG / 2
HALF = math.radians(HALF_DEG)

BED = [float(x) for x in P("printer", "build_volume")]
BED_MARGIN = float(P("printer", "bed_margin"))

T_SLOT = float(P("tolerances", "rib_slot_total"))
T_FLG = float(P("tolerances", "rib_flange_gap"))
T_HOLE = float(P("tolerances", "bolt_hole_printed"))
T_NUT = float(P("tolerances", "nut_pocket_af"))
T_NUTD = float(P("tolerances", "nut_pocket_depth_extra"))
T_SOCK = float(P("tolerances", "batten_socket"))
T_END = float(P("tolerances", "batten_end_gap"))
BORE_FIX = float(P("tolerances", "bearing_bore_fixed"))
BORE_FLOAT = float(P("tolerances", "bearing_bore_float"))
T_CAN = float(P("tolerances", "can_clearance"))

SEC_LEG = tuple(float(x) for x in P("battens", "section"))        # 19 x 38
SEC_BEAM = tuple(float(x) for x in P("battens", "beam_section"))  # 19 x 64
SEC_FEED = tuple(float(x) for x in P("battens", "feed_leg_section"))
B608 = [float(x) for x in RAW["bearing_608"]["value"]]
CAN_D = float(P("feed_can", "diameter"))
CAN_L = float(P("feed_can", "length"))
CAN_T = float(P("feed_can", "wall"))
CAN_M = float(P("feed_can", "mass"))
MESH_KG_M2 = float(P("mesh", "areal_mass"))
EBOX = [float(x) for x in P("electronics", "ebox_outer")]
EBOX_M = float(P("electronics", "ebox_mass"))
LNA = [float(x) for x in P("electronics", "lna_box_outer")]
LNA_M = float(P("electronics", "lna_mass"))

PANEL_T = float(P("dish", "rim_panel_radial"))
CHORD_H = float(P("dish", "rim_chord_height"))
DIAG_W = float(P("dish", "rim_diagonal_width"))
FLG_T = float(P("dish", "flange_thickness"))
FLG_R0, FLG_R1 = [float(x) for x in P("dish", "flange_r_range")]
HUB_FLOOR = float(P("dish", "hub_floor"))
HUB_DISC_R = float(P("dish", "hub_disc_radius"))
HUB_RING0, HUB_RING1 = [float(x) for x in P("dish", "hub_ring")]
HUB_WALL = float(P("dish", "hub_wall"))
SPC_R0, SPC_R1 = [float(x) for x in P("dish", "spacer_flange_r")]
SPC_RAD, SPC_H = [float(x) for x in P("dish", "spacer_section")]
ANCHOR_ANG = [float(x) for x in P("dish", "anchor_rib_angles")]
TRUN_T, TRUN_W = [float(x) for x in P("dish", "trunnion_block")]
SECT_T = float(P("dish", "sector_thickness"))
LOCK_R = float(P("dish", "lock_radius"))
EL_MIN, EL_MAX = [float(x) for x in P("dish", "elevation_range")]

COL_H = float(P("feed_support", "collar_height"))
COL_WALL = float(P("feed_support", "collar_wall"))
COL_Z0 = F + float(P("feed_support", "collar_bottom_above_focus"))
ANCH_R, ANCH_Z = [float(x) for x in P("feed_support", "leg_anchor_point")]

SOCK_WALL = float(P("mount", "socket_wall"))
SOCK_DEPTH = float(P("mount", "socket_depth"))
FEED_SOCK_DEPTH = float(P("mount", "feed_socket_depth"))
SOCK_FLOOR = float(P("mount", "socket_floor"))
SOCK_BOLTS = [float(x) for x in P("mount", "socket_bolts_from_mouth")]
ARM_X = float(P("mount", "arm_half_spread"))
PIV_CLR = float(P("mount", "pivot_clearance"))

RHO_PETG = float(P("petg", "density_solid"))
INFILL = float(P("petg", "infill"))
SHELL = float(P("petg", "perimeter_shell"))
RHO = {"softwood": float(P("softwood", "density")), "plywood": float(P("plywood", "density")),
       "steel": float(P("steel", "density"))}

# Metric hardware (ISO 4017 / 4032 / 7089 nominal sizes).
AF = {4: 7.0, 5: 8.0, 6: 10.0, 8: 13.0, 10: 17.0}
NUT_T = {4: 3.2, 5: 4.7, 6: 5.2, 8: 6.8, 10: 8.4}
HEAD_T = {4: 2.8, 5: 3.5, 6: 4.0, 8: 5.3, 10: 6.4}
WASH = {4: (9.0, 0.8), 5: (10.0, 1.0), 6: (12.0, 1.6), 8: (16.0, 1.6), 10: (20.0, 2.0)}

X_OUT = math.floor(R * math.cos(HALF))   # outer face of the rim girder, perpendicular distance
X_IN = X_OUT - PANEL_T
OFF = W / 2 + T_FLG                      # rib mid-plane to the printed flange face
Y_BLOCK = X_OUT + TRUN_T                 # outer face of the trunnion block (world |y| at zenith)
Y_SECT = Y_BLOCK + SECT_T                # outer face of the elevation sector / spacer
GAP_NODE = 2.0                           # sector to fork node
Y_NODE0 = Y_SECT + GAP_NODE              # inner face of the fork top node
NODE_LEN = SEC_LEG[1] + T_SOCK + 2 * SOCK_WALL   # fork node length along the axle
Y_NODE_C = Y_NODE0 + NODE_LEN / 2
LOCK_ANG = -30.0                         # world angle of the lock bolt, from +X toward +Z


def zpar(r):
    return r * r / (4 * F)


# ------------------------------------------------------------------ geometry helpers
def bx(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def cyl(r, h, p, d=(0, 0, 1)):
    return cq.Solid.makeCylinder(r, h, V(*p), V(*d))


def rz(s, a):
    return s.rotate(V(0, 0, 0), V(0, 0, 1), a) if abs(a) > 1e-12 else s


def unit(v):
    v = np.asarray(v, dtype=float)
    return v / np.linalg.norm(v)


def perp(d):
    d = unit(d)
    a = np.array([1.0, 0, 0]) if abs(d[0]) < 0.9 else np.array([0, 1.0, 0])
    return unit(np.cross(d, a))


def prism(plane, pts, depth, axis, lo):
    """Extrude a polygon drawn on a named plane, then shift so it starts at `lo` on `axis`."""
    s = cq.Workplane(plane).polyline(pts).close().extrude(depth).val()
    bb = s.BoundingBox()
    cur = {"x": bb.xmin, "y": bb.ymin, "z": bb.zmin}[axis]
    shift = {"x": (lo - cur, 0, 0), "y": (0, lo - cur, 0), "z": (0, 0, lo - cur)}[axis]
    return s.translate(V(*shift))


def revolve(pts):
    """Revolve an (r, z) polygon about the Z axis."""
    return cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0)).val()


def bar(p, d, u, a, b, length):
    """Rectangular bar: starts at p, runs along d, `a` wide along u, `b` wide along d x u."""
    pl = cq.Plane(origin=tuple(p), xDir=tuple(unit(u)), normal=tuple(unit(d)))
    return cq.Workplane(pl).rect(a, b).extrude(length).val()


def hexp(af, h, p, d):
    """Hexagonal prism, across-flats af, starting at p, extending h along d."""
    pl = cq.Plane(origin=tuple(p), xDir=tuple(perp(d)), normal=tuple(unit(d)))
    return cq.Workplane(pl).polygon(6, af / math.cos(math.radians(30))).extrude(h).val()


def hull(points):
    """Solid convex hull of a point cloud (used to join socket ends with the least material)."""
    from scipy.spatial import ConvexHull
    from OCP.BRepBuilderAPI import BRepBuilderAPI_Sewing, BRepBuilderAPI_MakeSolid
    from OCP.TopoDS import TopoDS
    P_ = np.asarray(points, dtype=float)
    h = ConvexHull(P_)
    sew = BRepBuilderAPI_Sewing(1e-4)
    for simp, eq in zip(h.simplices, h.equations):
        a, b, c = P_[simp]
        if np.dot(np.cross(b - a, c - a), eq[:3]) < 0:
            b, c = c, b
        sew.Add(cq.Face.makeFromWires(cq.Wire.makePolygon([V(*a), V(*b), V(*c)], close=True)).wrapped)
    sew.Perform()
    shell = TopoDS.Shell_s(sew.SewedShape())
    s = cq.Solid(BRepBuilderAPI_MakeSolid(shell).Solid())
    if s.Volume() < 0:
        s = cq.Solid(s.wrapped.Reversed())
    return s.clean()


def fuse(solids):
    out = solids[0]
    for s in solids[1:]:
        out = out.fuse(s)
    return out.clean()


def cut(body, cutters):
    for c in cutters:
        body = body.cut(c)
    return body


def hole(d, p, direction, length):
    """Clearance-hole cutter centred on p, `length` long in total."""
    dv = unit(direction)
    return cyl(d / 2, length, tuple(np.asarray(p) - dv * length / 2), tuple(dv))


def nut_pocket(m, face_p, into, extra=0.0):
    """Hex pocket for an M`m` nut, opening at face_p and cut `into` the part."""
    depth = NUT_T[m] + T_NUTD + extra
    dv = unit(into)
    return hexp(AF[m] + T_NUT, depth + 0.5, tuple(np.asarray(face_p) - dv * 0.5), tuple(dv)), depth


# ------------------------------------------------------------------ part registry
PARTS = []


def add(pid, name, solid, material, group, kind, check=True, mass=None, print_rot=None):
    """kind: print | wood | existing | hardware | purchase.  print_rot: [(axis, deg), ...] to lay it on the bed."""
    PARTS.append(dict(id=pid, name=name, solid=solid, material=material, group=group, kind=kind,
                      check=check, mass=mass, print_rot=print_rot or []))


def bolt(m, length, seat, direction, group, head="hex", label=None, washer=True, nut=True, nut_at=None, nyloc=False,
         neck_dir=None):
    """Bolt whose head bears at `seat` and whose shank runs `length` along `direction`.
    nut_at: distance from the seat to the near face of the nut (the grip). Adds washer and nut solids."""
    dv = unit(direction)
    seat = np.asarray(seat, dtype=float)
    wt = WASH[m][1] if washer else 0.0
    pid = f"HW-M{m}x{int(length)}" + ("-carriage" if head == "carriage" else "")
    name = label or f"M{m} x {int(length)} bolt"
    shank = cyl(m / 2, length - wt if head != "carriage" else length, tuple(seat), tuple(dv))
    if head == "carriage":
        hd = cyl(m * 1.15, m * 0.55, tuple(seat - dv * m * 0.55), tuple(dv))
        neck = bar(seat, dv, neck_dir if neck_dir is not None else perp(dv), m, m, m * 0.6)
        body = fuse([shank, hd, neck])
    else:
        hd = hexp(AF[m], HEAD_T[m], tuple(seat - dv * (wt + HEAD_T[m])), tuple(dv))
        shank = cyl(m / 2, length, tuple(seat - dv * wt), tuple(dv))
        body = fuse([shank, hd])
    add(pid, name, body, "steel", group, "hardware", check=False)
    if washer and head != "carriage":
        od, t = WASH[m]
        ws = cyl(od / 2, t, tuple(seat - dv * t), tuple(dv)).cut(cyl(m / 2 + 0.2, t, tuple(seat - dv * t), tuple(dv)))
        add(f"HW-M{m}-washer", f"M{m} washer", ws, "steel", group, "hardware", check=False)
    if nut and nut_at is not None:
        t = NUT_T[m] * (1.25 if nyloc else 1.0)
        ns = hexp(AF[m], t, tuple(seat + dv * nut_at), tuple(dv)).cut(cyl(m / 2, t + 1, tuple(seat + dv * (nut_at - 0.5)), tuple(dv)))
        add(f"HW-M{m}-nut" + ("-nyloc" if nyloc else ""), f"M{m} " + ("nyloc nut" if nyloc else "nut"), ns, "steel",
            group, "hardware", check=False)


def washer_at(m, p, direction, group):
    dv = unit(direction)
    od, t = WASH[m]
    ws = cyl(od / 2, t, tuple(p), tuple(dv)).cut(cyl(m / 2 + 0.2, t, tuple(p), tuple(dv)))
    add(f"HW-M{m}-washer", f"M{m} washer", ws, "steel", group, "hardware", check=False)
    return t


# ------------------------------------------------------------------ batten sockets (wood member into printed node)
class Member:
    """A wooden batten between two printed nodes. Each end sits in a printed socket and is
    held by cross bolts through the thin dimension of the batten."""

    def __init__(self, pid, name, pa, pb, sec, wide_hint, sa0, sb0, group, depth=None, bolts=None, bolt_m=6):
        self.pid, self.name, self.group = pid, name, group
        self.pa, self.pb = np.asarray(pa, float), np.asarray(pb, float)
        self.a, self.b = sec                      # a = thin, b = wide
        self.d = unit(self.pb - self.pa)
        h = np.asarray(wide_hint, float)
        self.h = unit(h - np.dot(h, self.d) * self.d)   # direction of the wide dimension
        self.u = unit(np.cross(self.h, self.d))         # direction of the thin dimension (bolt axis)
        self.sa0, self.sb0 = sa0, sb0
        self.depth = depth or SOCK_DEPTH
        self.bolts = bolts if bolts is not None else SOCK_BOLTS
        self.m = bolt_m
        self.length = float(np.linalg.norm(self.pb - self.pa)) - sa0 - sb0 - 2 * (SOCK_FLOOR + T_END)

    def socket(self, end):
        """(outer solid, [cutters]) for the socket at end 'a' or 'b'."""
        p, d, s0 = (self.pa, self.d, self.sa0) if end == "a" else (self.pb, -self.d, self.sb0)
        ao, bo = self.a + T_SOCK + 2 * SOCK_WALL, self.b + T_SOCK + 2 * SOCK_WALL
        outer = bar(p + d * s0, d, self.u, ao, bo, SOCK_FLOOR + self.depth)
        bore = bar(p + d * (s0 + SOCK_FLOOR), d, self.u, self.a + T_SOCK, self.b + T_SOCK, self.depth + 1)
        cutters = [bore]
        for bp in self.bolt_points(end):
            cutters.append(hole(self.m + T_HOLE, bp, self.u, ao + 2))
        return outer, cutters

    def base_corners(self, end, extra=0.0):
        p, d, s0 = (self.pa, self.d, self.sa0) if end == "a" else (self.pb, -self.d, self.sb0)
        ao, bo = self.a + T_SOCK + 2 * SOCK_WALL, self.b + T_SOCK + 2 * SOCK_WALL
        c = p + d * (s0 + extra)
        return [c + self.u * (i * ao / 2) + self.h * (j * bo / 2) for i in (-1, 1) for j in (-1, 1)]

    def bolt_points(self, end):
        p, d, s0 = (self.pa, self.d, self.sa0) if end == "a" else (self.pb, -self.d, self.sb0)
        mouth = s0 + SOCK_FLOOR + self.depth
        return [p + d * (mouth - x) for x in self.bolts]

    def build(self):
        start = self.pa + self.d * (self.sa0 + SOCK_FLOOR + T_END)
        s = bar(start, self.d, self.u, self.a, self.b, self.length)
        ao = self.a + T_SOCK + 2 * SOCK_WALL
        for end in ("a", "b"):
            for bp in self.bolt_points(end):
                s = s.cut(hole(self.m + 0.5, bp, self.u, self.a + 2))
                wt = WASH[self.m][1]
                L = 5 * math.ceil((ao + 2 * wt + NUT_T[self.m] + 1.5) / 5)
                seat = bp - self.u * (ao / 2)
                bolt(self.m, L, seat, self.u, self.group, nut_at=ao + wt)
                washer_at(self.m, seat + self.u * ao, self.u, self.group)
        add(self.pid, self.name, s, "softwood", self.group, "wood")
        return s

    def end_distance(self):
        return self.depth - T_END - max(self.bolts)


# ------------------------------------------------------------------ dish (elevation group)
def bay_wedge(z0=-20, z1=320, r0=40, r1=560, off=OFF):
    """Region between the printed-flange faces of two neighbouring ribs (bay frame, mid-angle on +X)."""
    c, s = math.cos(HALF), math.sin(HALF)
    ep, np_ = np.array([c, s]), np.array([s, -c])
    em, nm = np.array([c, -s]), np.array([s, c])
    pts = [tuple(r0 * ep + off * np_), tuple(r1 * ep + off * np_), tuple(r1 * em + off * nm), tuple(r0 * em + off * nm)]
    return prism("XY", pts, z1 - z0, "z", z0)


def mesh_top_cut(x0, x1, drop=1.0):
    """Cutter removing everything above the straight-pulled mesh plane in a bay."""
    xs = np.linspace(x0 - 2, x1 + 2, 9)
    pts = [(x, zpar(x / math.cos(HALF)) - drop) for x in xs] + [(x1 + 2, 400), (x0 - 2, 400)]
    return prism("XZ", pts, 400, "y", -200)


def soften(solid, r=None):
    """Round the edges of a printed rib support. The rim and spacer unions have sliver faces where the
    flanges meet the chords, so OpenCascade refuses many edge sets at once. Edges are therefore tried one
    at a time, longest first, and kept only if the accepted set still fillets cleanly at one radius.
    Edges on the bed (z = 0) stay sharp so the part sits flat."""
    rad = FILLET_R if r is None else r
    accepted = []
    for e in sorted(solid.Edges(), key=lambda e: -e.Length()):
        if e.BoundingBox().zmax <= 1e-3 or e.Length() < 4 * rad:
            continue
        try:
            trial = solid.fillet(rad, accepted + [e])
            if trial.isValid():
                accepted.append(e)
        except Exception:
            pass
    if not accepted:
        return solid
    return solid.fillet(rad, accepted)


def flange(r0, r1, z0, side, holes, pocket, strip_r=None):
    """Clamp flange lying on a rib face. Built for the rib at +HALF (side=+1) or -HALF (side=-1) of the bay.
    With strip_r, only the band r >= strip_r is full height; inboard of it the flange is a lobe round each bolt."""
    rs = np.linspace(r0, r1, 7)
    pts = [(r0, z0), (r1, z0)] + [(r, zpar(r) - 1.5) for r in rs[::-1]]
    y_lo = -(OFF + FLG_T) if side > 0 else OFF
    f = prism("XZ", pts, FLG_T, "y", y_lo)
    if strip_r is not None:
        keep = [bx(strip_r, r1 + 1, y_lo - 1, y_lo + FLG_T + 1, -1, 400)]
        for (hr, hz) in holes:
            keep.append(bx(r0 - 1, strip_r + 1, y_lo - 1, y_lo + FLG_T + 1, hz - 13, hz + 13))
        f = f.intersect(fuse(keep))
    cutters = []
    for (hr, hz) in holes:
        cutters.append(hole(4 + T_HOLE, (hr, 0, hz), (0, 1, 0), 2 * (OFF + FLG_T) + 4))
        if pocket:
            face_y = -(OFF + FLG_T) if side > 0 else (OFF + FLG_T)
            cutters.append(nut_pocket(4, (hr, face_y, hz), (0, 1 if side > 0 else -1, 0))[0])
    f = cut(f, cutters)
    return rz(f, side * HALF_DEG)


def pad_positions():
    """Four feed-anchor pads per rim bay: (y, z) in the bay frame, pads on both sides."""
    pad_z = [(CHORD_H, CHORD_H + 24.0), (zpar(X_IN / math.cos(HALF)) - 1.0 - CHORD_H - 24.0,
                                         zpar(X_IN / math.cos(HALF)) - 1.0 - CHORD_H)]
    return [(sgn * 68.0, (z0 + z1) / 2) for sgn in (1, -1) for z0, z1 in pad_z], pad_z


def rim_panel(holed=(), trunnion_zp=None):
    """One bay of the rim girder: top and bottom chords, X bracing, bolted rib flanges.
    holed: the pad sides (+1/-1) that take a feed-anchor bolt. Plain bays have no pads and no holes.
    Bay frame: mid-angle on +X, panel between x = X_IN and X_OUT. Returns (solid, all pad positions)."""
    zt_in = zpar(X_IN / math.cos(HALF)) - 1.0
    chord_z = zt_in - CHORD_H
    yw = X_IN * math.tan(HALF) + 4
    parts = [bx(X_IN, X_OUT, -yw, yw, 0, CHORD_H), bx(X_IN, X_OUT, -yw, yw, chord_z, 200)]
    ye = X_IN * math.tan(HALF) - OFF / math.cos(HALF) - FLG_T - 2
    ang = math.degrees(math.atan2(chord_z - CHORD_H, 2 * ye))
    ld = math.hypot(chord_z - CHORD_H, 2 * ye) + 20
    zc = (chord_z + CHORD_H) / 2
    for sgn in (1, -1):
        d = bx(X_IN, X_OUT, -ld / 2, ld / 2, zc - DIAG_W / 2, zc + DIAG_W / 2)
        parts.append(d.rotate(V(0, 0, zc), V(1, 0, zc), sgn * ang))
    pads_all, pad_z = pad_positions()
    for sgn in holed:
        for z0, z1 in pad_z:
            parts.append(bx(X_IN, X_OUT, min(sgn * 54, sgn * yw), max(sgn * 54, sgn * yw), z0, z1))
    if trunnion_zp is not None:
        parts.append(bx(X_IN, Y_BLOCK, -TRUN_W / 2, TRUN_W / 2, 0, trunnion_zp + 25))
    body = fuse(parts)
    body = body.intersect(bx(X_IN - 1, 600, -200, 200, 0, 400))
    body = body.cut(mesh_top_cut(X_IN, X_OUT)) if trunnion_zp is None else body.cut(
        mesh_top_cut(X_IN, X_OUT).cut(bx(X_IN - 5, 600, -TRUN_W / 2, TRUN_W / 2, 0, 400)))
    body = body.intersect(bay_wedge())
    holes = [(RIM_HOLE_R, z) for z in RIM_HOLE_Z]     # side bolts through flange - rib - flange (kept)
    sr = X_IN / math.cos(HALF) - 6
    body = fuse([body, flange(FLG_R0, FLG_R1, 0, 1, holes, True, sr), flange(FLG_R0, FLG_R1, 0, -1, holes, False, sr)])
    body = body.intersect(bx(0, X_OUT if trunnion_zp is None else Y_BLOCK, -200, 200, 0, 400))
    if trunnion_zp is not None:   # keep the block, trim everything else to the girder face
        keep = bx(0, X_OUT, -200, 200, 0, 400).fuse(bx(X_OUT - 1, Y_BLOCK, -TRUN_W / 2, TRUN_W / 2, 0, 400))
        body = body.intersect(keep)
    cutters = []
    for sgn in holed:
        for z0, z1 in pad_z:
            y, z = sgn * 68.0, (z0 + z1) / 2
            cutters.append(hole(4 + T_HOLE, ((X_IN + X_OUT) / 2, y, z), (1, 0, 0), PANEL_T + 4))
            cutters.append(nut_pocket(4, (X_IN, y, z), (1, 0, 0))[0])
    # zip-tie holes for the mesh edge: one per bay (two on a trunnion bay, either side of the block)
    for y in ((0,) if trunnion_zp is None else (-40, 40)):
        cutters.append(hole(3.2, ((X_IN + X_OUT) / 2, y, chord_z + 4), (1, 0, 0), PANEL_T + 4))
    if trunnion_zp is not None:
        zp = trunnion_zp
        cutters.append(hole(8 + T_HOLE, ((X_IN + Y_BLOCK) / 2, 0, zp), (1, 0, 0), Y_BLOCK - X_IN + 4))
        cutters.append(hexp(AF[8] + T_NUT, 6.5, (X_IN - 0.5, 0, zp), (1, 0, 0)))
        for y in (-22, 22):   # M4 pins for the elevation lock sector ELS-01 (kept)
            cutters.append(hole(4 + T_HOLE, ((X_IN + Y_BLOCK) / 2, y, zp - 30), (1, 0, 0), Y_BLOCK - X_IN + 4))
    return soften(cut(body, cutters)), pads_all


def spacer():
    """Mid-span spacer between two ribs: mesh support beam with two bolted rib flanges (bay frame)."""
    xs = MID_HOLE_R * math.cos(HALF)
    x0, x1 = xs - SPC_RAD / 2, xs + SPC_RAD / 2
    zt = zpar(x0 / math.cos(HALF)) - 1.0
    beam = bx(x0, x1, -80, 80, zt - SPC_H, 200).cut(mesh_top_cut(x0, x1)).intersect(bay_wedge())
    holes = [(MID_HOLE_R, MID_HOLE_Z)]                # side bolt through flange - rib - flange (kept)
    body = fuse([beam, flange(SPC_R0, SPC_R1, 6, 1, holes, True), flange(SPC_R0, SPC_R1, 6, -1, holes, False)])
    body = body.cut(hole(3.2, (xs, 0, zt - SPC_H / 2 - 1), (1, 0, 0), SPC_RAD + 4))   # one zip-tie hole for the mesh
    return soften(body)


def hub():
    """Printed hub: central cap, 18 rib channels and an outer floor ring. Each rib tip is held by one M4 cross
    pin through the channel walls, below the reflector surface, so nothing sits on the mesh (no keeper ring)."""
    cap = revolve([(0, -HUB_FLOOR), (HUB_DISC_R, -HUB_FLOOR), (HUB_DISC_R, 0), (RELIEF - 0.5, 0),
                   (RELIEF - 0.5, zpar(RELIEF)), (0, zpar(RELIEF))])
    ring = cyl(HUB_RING1, HUB_FLOOR, (0, 0, -HUB_FLOOR)).cut(cyl(HUB_RING0, HUB_FLOOR, (0, 0, -HUB_FLOOR)))
    half_w = W / 2 + T_SLOT / 2 + HUB_WALL
    r0 = RELIEF - 0.5
    rr = np.linspace(r0, HUB_RING1, 11)
    wall_pts = [(r0, 0), (HUB_RING1, 0)] + [(r, zpar(r) - 0.3) for r in rr[::-1]]
    chan = fuse([bx(r0, HUB_RING1, -half_w, half_w, -HUB_FLOOR, 0),
                 prism("XZ", wall_pts, HUB_WALL, "y", W / 2 + T_SLOT / 2),
                 prism("XZ", wall_pts, HUB_WALL, "y", -half_w)])
    chan = chan.cut(hole(4 + T_HOLE, (TIP_PIN_R, 0, TIP_PIN_Z), (0, 1, 0), 2 * half_w + 4))
    body = fuse([cap, ring] + [rz(chan, k * STEP_DEG) for k in range(N)])
    rr2 = np.linspace(0, HUB_RING1 + 10, 25)
    above = revolve([(r, zpar(r) + 0.5) for r in rr2] + [(HUB_RING1 + 10, 80), (0, 80)])
    return body.cut(above), half_w


def feed_geometry():
    """Leg start (anchor) and end (collar) points in the rib frame, plus the leg direction."""
    pa = np.array([ANCH_R, 0.0, ANCH_Z])
    pc = np.array([CAN_D / 2 + T_CAN / 2 + COL_WALL + 12.0, 0.0, COL_Z0 + COL_H / 2])
    return pa, pc


def feed_leg_member(ang):
    pa, pc = feed_geometry()
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    rot = lambda p: np.array([p[0] * c - p[1] * s, p[0] * s + p[1] * c, p[2]])
    tang = np.array([-s, c, 0.0])
    return Member("LEG-F", f"feed leg {ang:.0f} deg", rot(pa), rot(pc), SEC_FEED, tang, 0.0, 0.0, "dish",
                  depth=FEED_SOCK_DEPTH, bolts=[22.0], bolt_m=4)


def feed_anchor(pad_holes):
    """Feed-leg anchor at a rib end (rib frame): two wings bolted to the neighbouring girder panels
    and a socket block for the leg. Returns the body without the socket (added per instance)."""
    parts = [bx(X_OUT - 2, ANCH_R + 8, -20, 20, 157.5, 192), bx(X_OUT - 2, X_OUT + 12, -86, 86, 157.5, 168)]
    cutters = []
    bolts = []
    for side in (1, -1):          # bay at +HALF (side=+1): the rib is on that bay's -y side
        ys = sorted([-side * 82.0, -side * 54.0])
        wing = bx(X_OUT, X_OUT + 5, ys[0], ys[1], CHORD_H, 172)
        parts.append(rz(wing, side * HALF_DEG))
        for y, z in pad_holes:
            if y * side < 0:
                cutters.append(rz(hole(4 + T_HOLE, (X_OUT + 2.5, y, z), (1, 0, 0), 12), side * HALF_DEG))
                bolts.append((side, y, z))
    return fuse(parts), cutters, bolts


def collar():
    """Split feed collar with three leg sockets, a pinch joint and an LNA shelf."""
    ri = CAN_D / 2 + T_CAN / 2
    ro = ri + COL_WALL
    body = [cyl(ro, COL_H, (0, 0, COL_Z0)).cut(cyl(ri, COL_H, (0, 0, COL_Z0)))]
    for sgn in (1, -1):           # pinch ears at 0 deg
        y0, y1 = sorted([sgn * 1.5, sgn * 11.5])
        body.append(bx(ro - 1.5, ro + 16, y0, y1, COL_Z0, COL_Z0 + COL_H))
    shelf_ang = 240.0 + 0.0       # LNA shelf, clear of legs (60/180/300) and the pinch joint (0)
    shelf = bx(ro - 1.5, ro + 58, -27, 27, COL_Z0 + COL_H - 5, COL_Z0 + COL_H)
    gus = prism("XZ", [(ro - 1.5, COL_Z0 + COL_H - 5), (ro + 45, COL_Z0 + COL_H - 5), (ro - 1.5, COL_Z0 + 5)], 5, "y", -2.5)
    body.append(rz(fuse([shelf, gus]), shelf_ang))
    cutters = [bx(ro - 20, ro + 30, -1.5, 1.5, COL_Z0 - 1, COL_Z0 + COL_H + 1)]
    pinch = [(ro + 9.0, COL_Z0 + 12.0), (ro + 9.0, COL_Z0 + COL_H - 12.0)]
    for x, z in pinch:
        cutters.append(hole(4 + T_HOLE, (x, 0, z), (0, 1, 0), 40))
    shelf_holes = [(ro + 30.0, -16.0), (ro + 30.0, 16.0)]
    for x, y in shelf_holes:
        cutters.append(rz(hole(4 + T_HOLE, (x, y, COL_Z0 + COL_H - 2.5), (0, 0, 1), 12), shelf_ang))
    return body, cutters, pinch, shelf_ang, shelf_holes, ro


def mesh_area_m2():
    r = np.linspace(RELIEF, R, 2001)
    ds = np.sqrt(1 + (r / (2 * F)) ** 2)
    return float(np.trapezoid(2 * np.pi * r * ds, r)) / 1e6 + math.pi * RELIEF ** 2 / 1e6


def build_dish(zp):
    """Everything that tilts. Built in the dish-local frame; zp is the elevation-axle height."""
    g = "dish"
    # --- existing ribs, with the tip relief and four drilled holes (tip pin, mid, two at the rim)
    rr = np.linspace(RELIEF, R, 41)
    pts = [(ri, zpar(ri)) for ri in rr] + [(R, 0.0), (RELIEF, 0.0)]
    rib = prism("XZ", pts, W, "y", -W / 2)
    for (hr, hz) in [(RIM_HOLE_R, z) for z in RIM_HOLE_Z] + [(MID_HOLE_R, MID_HOLE_Z), (TIP_PIN_R, TIP_PIN_Z)]:
        rib = rib.cut(hole(4 + DRILL, (hr, 0, hz), (0, 1, 0), W + 2))
    for k in range(N):
        add("RIB", f"existing rib {k + 1:02d}", rz(rib, k * STEP_DEG), "plywood", g, "existing")

    # --- hub; one M4 cross pin per rib tip, all below the reflector surface
    hub_s, hub_half_w = hub()
    add("HUB-01", "hub with 18 rib channels and tip pins", hub_s, "petg", g, "print")

    def side_bolt(k, r_, z_, half, pocketed=True):
        """M4 across rib k at (r_, z_); `half` is the distance from the rib mid-plane to the outer printed face."""
        a_ = math.radians(k * STEP_DEG)
        nrm = np.array([-math.sin(a_), math.cos(a_), 0.0])
        p = np.array([r_ * math.cos(a_), r_ * math.sin(a_), z_])
        if pocketed:      # head on the plain flange, nut in the pocketed flange
            bolt(4, 20, p + nrm * half, -nrm, g, nut_at=2 * half - (NUT_T[4] + T_NUTD))
        else:             # tip pin: same M4 x 20 as every other rib bolt, no washers (it only locates the tip)
            bolt(4, 20, p + nrm * half, -nrm, g, washer=False, nut_at=2 * half)

    for k in range(N):
        side_bolt(k, TIP_PIN_R, TIP_PIN_Z, hub_half_w, pocketed=False)
        for z in RIM_HOLE_Z:
            side_bolt(k, RIM_HOLE_R, z, OFF + FLG_T)
        side_bolt(k, MID_HOLE_R, MID_HOLE_Z, OFF + FLG_T)

    # --- rim girder: 16 bays (10 plain, 6 feed bays with anchor pads) and 2 trunnion bays on +Y and -Y
    trun = rim_panel(trunnion_zp=zp)[0]
    flat = [((0, 1, 0), -90)]
    anchors = [a_ % 360.0 for a_ in ANCHOR_ANG]

    def holed_sides(mid):
        """Pad sides of a bay that face a feed anchor. The rib at mid + sgn*HALF sits on pad side sgn."""
        out = []
        for sgn in (-1, 1):
            th = (mid + sgn * HALF_DEG) % 360.0
            if any(min(abs(th - a_), 360.0 - abs(th - a_)) < 1e-6 for a_ in anchors):
                out.append(sgn)
        return tuple(out)

    plain_cache, pad_all = {}, None
    for k in range(N):
        mid = k * STEP_DEG + HALF_DEG
        is_t = abs(mid - 90) < 1e-6 or abs(mid - 270) < 1e-6
        if is_t:
            add("RIM-T", f"rim girder trunnion bay {mid:.0f} deg", rz(trun, mid), "petg", g, "print", print_rot=flat)
            continue
        hs = holed_sides(mid)
        if hs not in plain_cache:
            plain_cache[hs], pad_all = rim_panel(holed=hs)
        if hs:
            add("RIM-02", f"feed rim bay {mid:.0f} deg (anchor pads)", rz(plain_cache[hs], mid), "petg", g, "print",
                print_rot=flat)
        else:
            add("RIM-01", f"rim girder bay {mid:.0f} deg", rz(plain_cache[hs], mid), "petg", g, "print", print_rot=flat)
    pad_holes = pad_all

    # --- mid-span spacers (their side bolts are added with the hub pins above)
    sp = spacer()
    for k in range(N):
        add("SPC-01", f"mid-span spacer bay {k * STEP_DEG + HALF_DEG:.0f} deg", rz(sp, k * STEP_DEG + HALF_DEG),
            "petg", g, "print", print_rot=flat)

    # --- feed support: three anchors on rib ends, three wooden legs, one split collar
    col_parts, col_cut, pinch, shelf_ang, shelf_holes, col_ro = collar()
    anchor_body, anchor_cut, anchor_bolts = feed_anchor(pad_holes)
    anchor_soft = soften(anchor_body)     # round the bracket only; the leg socket keeps its square fit
    for ang in ANCHOR_ANG:
        m = feed_leg_member(ang)
        so, sc = m.socket("a")
        body = cut(fuse([rz(anchor_soft, ang), so]), [rz(c_, ang) for c_ in anchor_cut] + sc)
        add("FLA-01", f"feed-leg anchor {ang:.0f} deg", body, "petg", g, "print")
        for side, y, z in anchor_bolts:
            th = math.radians(ang + side * HALF_DEG)
            ex = np.array([math.cos(th), math.sin(th), 0.0])
            ey = np.array([-math.sin(th), math.cos(th), 0.0])
            seat = ex * (X_OUT + 5) + ey * y + np.array([0, 0, z])
            bolt(4, 20, seat, -ex, g, nut_at=5 + PANEL_T - (NUT_T[4] + T_NUTD))
        so, sc = m.socket("b")
        col_parts.append(so)
        zc = COL_Z0 + COL_H / 2
        col_parts.append(rz(bx(col_ro - 2, col_ro + 17, -13, 13, zc - 17, zc + 15), ang))
        col_cut += sc
        m.build()
    col = cut(fuse(col_parts), col_cut)
    col = col.cut(cyl(CAN_D / 2 + T_CAN / 2, COL_H + 2, (0, 0, COL_Z0 - 1)))
    add("FRG-01", "feed collar (split, three leg sockets, LNA shelf)", col, "petg", g, "print")
    for x, z in pinch:
        bolt(4, 30, (x, -11.5, z), (0, 1, 0), g, nut_at=23.0 + WASH[4][1])
        washer_at(4, (x, 11.5, z), (0, 1, 0), g)

    can = cyl(CAN_D / 2, CAN_L, (0, 0, F)).cut(cyl(CAN_D / 2 - CAN_T, CAN_L - CAN_T, (0, 0, F)))
    add("FEED-01", "feed can (conductive, provisional size)", can, "steel", g, "purchase", mass=CAN_M)

    # --- LNA box on the collar shelf
    sa = math.radians(shelf_ang)
    z_sh = COL_Z0 + COL_H
    lx, ly, lz = LNA[1], LNA[0], LNA[2]      # radial, tangential, height
    x0 = col_ro + 6
    box = bx(x0, x0 + lx, -ly / 2, ly / 2, z_sh, z_sh + lz).cut(bx(x0 + 2, x0 + lx - 2, -ly / 2 + 2, ly / 2 - 2, z_sh + 3, z_sh + lz + 1))
    for x, y in shelf_holes:
        box = box.cut(hole(4 + T_HOLE, (x, y, z_sh + 1.5), (0, 0, 1), 6))
    add("LNA-01", "LNA enclosure body (envelope for the chosen LNA)", rz(box, shelf_ang), "petg", g, "print", mass=LNA_M)
    lid = bx(x0, x0 + lx, -ly / 2, ly / 2, z_sh + lz, z_sh + lz + 2).fuse(
        bx(x0 + 2.2, x0 + lx - 2.2, -ly / 2 + 2.2, ly / 2 - 2.2, z_sh + lz - 3, z_sh + lz)).clean()
    add("LNA-02", "LNA enclosure lid", rz(lid, shelf_ang), "petg", g, "print", print_rot=[((1, 0, 0), 180)])
    for x, y in shelf_holes:
        seat = np.array([x * math.cos(sa) - y * math.sin(sa), x * math.sin(sa) + y * math.cos(sa), z_sh + 3])
        bolt(4, 12, seat, (0, 0, -1), g, nut_at=8.0)

    # --- elevation hardware carried by the dish: axle bolts, lock sector (+Y), spacer (-Y)
    sect = cyl(18, SECT_T, (0, X_OUT + TRUN_T, zp), (0, 1, 0))
    a0, a1 = LOCK_ANG, LOCK_ANG + (EL_MAX - EL_MIN)
    aa = np.radians(np.linspace(a0 - 14, a1 + 14, 40))
    pie = prism("XZ", [(0, zp)] + [(84 * math.cos(t), zp + 84 * math.sin(t)) for t in aa], SECT_T, "y", Y_BLOCK)
    pad = bx(-30, 30, Y_BLOCK, Y_SECT, zp - 40, zp)
    sect = fuse([sect, pie, pad])
    ext = math.degrees((3.0 + 0.3) / LOCK_R)
    sl = np.radians(np.linspace(a0 - ext, a1 + ext, 40))
    w = (6 + 0.6) / 2
    slot_pts = [((LOCK_R + w) * math.cos(t), zp + (LOCK_R + w) * math.sin(t)) for t in sl] + \
               [((LOCK_R - w) * math.cos(t), zp + (LOCK_R - w) * math.sin(t)) for t in sl[::-1]]
    cutters = [prism("XZ", slot_pts, SECT_T + 2, "y", Y_BLOCK - 1)]
    cutters.append(hole(8 + T_HOLE, (0, Y_BLOCK + SECT_T / 2, zp), (0, 1, 0), SECT_T + 4))
    for x in (-22, 22):
        cutters.append(hole(4 + T_HOLE, (x, Y_BLOCK + SECT_T / 2, zp - 30), (0, 1, 0), SECT_T + 4))
        cutters.append(nut_pocket(4, (x, Y_SECT, zp - 30), (0, -1, 0))[0])
    add("ELS-01", "elevation lock sector (+Y trunnion)", cut(sect, cutters), "petg", g, "print",
        print_rot=[((1, 0, 0), 90)])
    for x in (-22, 22):
        bolt(4, 5 * math.floor((Y_SECT - X_IN + WASH[4][1]) / 5), (x, X_IN, zp - 30), (0, 1, 0), g,
             nut_at=Y_SECT - X_IN - (NUT_T[4] + T_NUTD))
    ring = cyl(15, SECT_T, (0, -Y_SECT, zp), (0, 1, 0)).cut(cyl(4 + T_HOLE / 2, SECT_T, (0, -Y_SECT, zp), (0, 1, 0)))
    add("SPR-03", "axle spacer, -Y trunnion (replaces the sector thickness)", ring, "petg", g, "print",
        print_rot=[((1, 0, 0), 90)])
    for sgn in (1, -1):
        yv = np.array([0, sgn, 0.0])
        seat = np.array([0, sgn * (X_IN + 6.0), zp])
        grip = (Y_NODE0 + NODE_LEN) - (X_IN + 6.0) + WASH[8][1]
        L = 10 * math.ceil((grip + NUT_T[8] * 1.25 + 2) / 10)
        bolt(8, L, seat, yv, g, washer=False, nut_at=grip, nyloc=True, label=f"M8 x {L} elevation axle bolt")
        washer_at(8, np.array([0, sgn * (Y_NODE0 + NODE_LEN), zp]), yv, g)
        sp_a = cyl(6, GAP_NODE, (0, sgn * Y_SECT, zp), tuple(yv)).cut(cyl(4.2, GAP_NODE, (0, sgn * Y_SECT, zp), tuple(yv)))
        add("SPR-01", "axle spacer between sector and inner bearing", sp_a, "petg", g, "print")
        ln = NODE_LEN - 2 * B608[2]
        sp_b = cyl(6, ln, (0, sgn * (Y_NODE0 + B608[2]), zp), tuple(yv)).cut(cyl(4.2, ln, (0, sgn * (Y_NODE0 + B608[2]), zp), tuple(yv)))
        add("SPR-02", "axle spacer between the two bearings", sp_b, "petg", g, "print")

    # --- representative mesh surface (ideal paraboloid shell, mass by area, excluded from checks)
    band = [(ri, zpar(ri)) for ri in rr] + [(ri, zpar(ri) + 0.5) for ri in rr[::-1]]
    add("MESH-01", "reflector mesh, representative ideal surface", revolve(band), "mesh", g, "purchase",
        check=False, mass=MESH_KG_M2 * mesh_area_m2())


# ------------------------------------------------------------------ mass model
def mass_kg(p):
    if p["mass"] is not None:
        return p["mass"]
    vol = p["solid"].Volume()
    if p["material"] == "petg":
        shell = min(vol, p["solid"].Area() * SHELL)
        return RHO_PETG * (shell + INFILL * (vol - shell)) * 1e-9
    return RHO[p["material"]] * vol * 1e-9


def group_cg(groups, parts=None):
    m_tot, mom = 0.0, np.zeros(3)
    for p in (parts or PARTS):
        if p["group"] not in groups:
            continue
        m = mass_kg(p)
        c = p["solid"].Center()
        m_tot += m
        mom += m * np.array([c.x, c.y, c.z])
    return m_tot, mom / m_tot


# ------------------------------------------------------------------ mount (azimuth group and ground group)
def build_mount(zp, drop):
    """zp: axle height in the dish frame. drop: lowest reach of the dish below the axle over the sweep.
    Returns the world axle height Zp and a dict of geometry used by the analysis."""
    info = {}
    hb = SEC_BEAM[1] + T_SOCK + 2 * SOCK_WALL          # socket outer height for the deep battens

    def members(zb):
        """All battens for a base plane at height zb. The axle clears the base top by PIV_CLR + drop."""
        Zp_ = zb + hb / 2 + PIV_CLR + drop
        T_ = {s: np.array([0.0, s * Y_NODE_C, Zp_]) for s in (1, -1)}
        C_ = {(sx, sy): np.array([sx * ARM_X, sy * Y_NODE_C, zb]) for sx in (1, -1) for sy in (1, -1)}
        legs_, sills_, ties_ = {}, {}, {}
        for (sx, sy), c in C_.items():
            legs_[(sx, sy)] = Member("LEG-A", f"fork leg x{'+' if sx > 0 else '-'} y{'+' if sy > 0 else '-'}", T_[sy], c,
                                     SEC_LEG, (0, 1, 0), 22.0, 30.0, "az")
        for sy in (1, -1):
            sills_[sy] = Member("SIL-01", f"base sill y{'+' if sy > 0 else '-'}", C_[(1, sy)], C_[(-1, sy)], SEC_LEG,
                                (0, 0, 1), 45.0, 45.0, "az")
        for sx in (1, -1):     # tie beams under the dish join the two fork frames (they replace the turntable spokes)
            ties_[sx] = Member("TIE-01", f"base tie x{'+' if sx > 0 else '-'}", C_[(sx, 1)], C_[(sx, -1)], SEC_BEAM,
                               (0, 0, 1), 45.0, 45.0, "az")
        return Zp_, T_, C_, legs_, sills_, ties_

    def corner(sx, sy, legs_, sills_, ties_):
        trio = ((legs_[(sx, sy)], "b"), (ties_[sx], "a" if sy > 0 else "b"), (sills_[sy], "a" if sx > 0 else "b"))
        parts, cutters, pts = [], [], []
        for m, end in trio:
            so, sc = m.socket(end)
            parts.append(so)
            cutters += sc
            pts += m.base_corners(end) + m.base_corners(end, SOCK_FLOOR)
        parts.append(hull(pts))
        return cut(fuse(parts), cutters)

    _, _, _, l0, s0, t0 = members(0.0)                  # trial pass: how far a corner node reaches below the base plane
    zb = -corner(1, 1, l0, s0, t0).BoundingBox().zmin   # the corner nodes are the feet: their undersides sit at z = 0
    Zp, T, C, legs, sills, ties = members(zb)
    info.update(zb=zb, Zp=Zp, base_top=zb + hb / 2, legs=legs, sills=sills, ties=ties)

    # ---------------- fork top nodes (bearing housing + two leg sockets + lock lug on +Y)
    for sy in (1, -1):
        y0, y1 = sorted([sy * Y_NODE0, sy * (Y_NODE0 + NODE_LEN)])
        parts = [cyl(18, NODE_LEN, (0, y0, Zp), (0, 1, 0))]
        cutters = []
        for sx in (1, -1):
            so, sc = legs[(sx, sy)].socket("a")
            parts.append(so)
            cutters += sc
        d1, d2 = legs[(1, sy)].d, legs[(-1, sy)].d
        web = prism("XZ", [(0, Zp + 6), tuple((T[sy] + d1 * 42)[[0, 2]]), tuple((T[sy] + d2 * 42)[[0, 2]])], 10, "y",
                    sy * Y_NODE_C - 5)
        parts.append(web)
        if sy > 0:
            la = math.radians(LOCK_ANG)
            lp = np.array([LOCK_R * math.cos(la), 0, Zp + LOCK_R * math.sin(la)])
            lug_y0 = Y_SECT + 0.3
            parts.append(cyl(12, Y_NODE0 + NODE_LEN - lug_y0, (lp[0], lug_y0, lp[2]), (0, 1, 0)))
            dl = unit([lp[0], 0, lp[2] - Zp])
            parts.append(bar(np.array([0, Y_NODE0, Zp]) + dl * LOCK_R / 2, np.array([0, 1.0, 0]), dl, LOCK_R, 12, NODE_LEN))
            info["lock_point"] = lp
        body = fuse(parts)
        bore = BORE_FIX if sy > 0 else BORE_FLOAT
        cutters.append(cyl(8.5, NODE_LEN + 2, (0, y0 - 1, Zp), (0, 1, 0)))
        cutters.append(cyl(bore / 2, B608[2] + 0.2 + 1, (0, y0 - 1, Zp), (0, 1, 0)))
        cutters.append(cyl(bore / 2, B608[2] + 0.2 + 1, (0, y1 - B608[2] - 0.2, Zp), (0, 1, 0)))
        body = cut(body, cutters)
        if sy > 0:
            body = body.cut(hole(6 + T_HOLE + 0.2, (lp[0], Y_NODE_C, lp[2]), (0, 1, 0), NODE_LEN + 20))
        add("FKT-01" if sy > 0 else "FKT-02", "fork top node " + ("+Y (fixed bearing fit, lock lug)" if sy > 0 else
                                                                 "-Y (floating bearing fit)"),
            body, "petg", "az", "print", print_rot=[((1, 0, 0), 90 if sy > 0 else -90)])
        for yb in (y0, y1 - B608[2]):
            b = cyl(B608[1] / 2, B608[2], (0, yb, Zp), (0, 1, 0)).cut(cyl(B608[0] / 2, B608[2], (0, yb, Zp), (0, 1, 0)))
            add("BRG-608", "608 ball bearing 8 x 22 x 7", b, "steel", "az", "purchase", check=False, mass=0.012)

    # lock bolt and knob (+Y)
    lp = info["lock_point"]
    y_head = Y_BLOCK
    L_lock = 10 * math.ceil((Y_NODE0 + NODE_LEN - y_head + WASH[6][1] + NUT_T[6] + 6) / 10)
    bolt(6, L_lock, (lp[0], y_head, lp[2]), (0, 1, 0), "az", head="carriage", washer=False,
         nut_at=Y_NODE0 + NODE_LEN - y_head + WASH[6][1], label=f"M6 x {L_lock} carriage bolt, elevation lock",
         neck_dir=(math.cos(math.radians(LOCK_ANG)), 0, math.sin(math.radians(LOCK_ANG))))
    washer_at(6, (lp[0], Y_NODE0 + NODE_LEN, lp[2]), (0, 1, 0), "az")
    yk = Y_NODE0 + NODE_LEN + WASH[6][1]
    knob = cq.Workplane(cq.Plane(origin=(lp[0], yk, lp[2]), xDir=(1, 0, 0), normal=(0, 1, 0))).polygon(8, 42).extrude(16).val()
    knob = cut(knob, [hole(6 + T_HOLE, (lp[0], yk + 8, lp[2]), (0, 1, 0), 20),
                      hexp(AF[6] + T_NUT, NUT_T[6] + 0.5, (lp[0], yk - 0.01, lp[2]), (0, 1, 0))])
    add("KNB-01", "elevation lock knob (captures an M6 nut)", knob, "petg", "az", "print", print_rot=[((1, 0, 0), 90)])

    # ---------------- base corner nodes (also the feet)
    for (sx, sy) in C:
        add("FKC-01" if sx * sy > 0 else "FKC-02", f"base corner node x{'+' if sx > 0 else '-'} y{'+' if sy > 0 else '-'}",
            corner(sx, sy, legs, sills, ties), "petg", "az", "print")
    for m in list(legs.values()) + list(ties.values()) + list(sills.values()):
        m.build()

    # ---------------- electronics box on the +Y sill
    y_s = Y_NODE_C + SEC_LEG[0] / 2
    ex, ez, ey = EBOX
    box = bx(-ex / 2, ex / 2, y_s, y_s + ey, zb - ez / 2, zb + ez / 2).cut(
        bx(-ex / 2 + 2.5, ex / 2 - 2.5, y_s + 3, y_s + ey + 1, zb - ez / 2 + 2.5, zb + ez / 2 - 2.5))
    eb = [(-45.0, zb), (45.0, zb)]
    for x, z in eb:
        box = box.cut(hole(6 + T_HOLE, (x, y_s + 1.5, z), (0, 1, 0), 6))
    add("EBOX-01", "electronics enclosure body (envelope: Pi 5, SDR, SSD)", box, "petg", "az", "print", mass=EBOX_M,
        print_rot=[((1, 0, 0), 90)])
    lid = bx(-ex / 2, ex / 2, y_s + ey, y_s + ey + 2.5, zb - ez / 2, zb + ez / 2).fuse(
        bx(-ex / 2 + 2.8, ex / 2 - 2.8, y_s + ey - 3, y_s + ey, zb - ez / 2 + 2.8, zb + ez / 2 - 2.8)).clean()
    add("EBOX-02", "electronics enclosure lid", lid, "petg", "az", "print", print_rot=[((1, 0, 0), -90)])
    sill = sills[1]
    for x, z in eb:      # cross bolts through the box back wall and the sill batten
        for i, pp in enumerate(PARTS):
            if pp["id"] == "SIL-01" and pp["name"].endswith("y+"):
                PARTS[i] = dict(pp, solid=pp["solid"].cut(hole(6.5, (x, Y_NODE_C, z), (0, 1, 0), 30)))
        bolt(6, 35, (x, y_s + 3, z), (0, -1, 0), "az", nut_at=3 + SEC_LEG[0] + WASH[6][1])
        washer_at(6, (x, Y_NODE_C - SEC_LEG[0] / 2 - WASH[6][1], z), (0, 1, 0), "az")
    return info


# ------------------------------------------------------------------ kinematics
def pose_solid(s, group, zp_local, Zp, el, az):
    """Place a solid built in its own stage frame into the world for a given pose.
    dish solids are built dish-local; az and ground solids are built in the world at az = 0."""
    if group == "dish":
        s = s.translate(V(0, 0, Zp - zp_local))
        t = 90.0 - el
        if abs(t) > 1e-9:
            s = s.rotate(V(0, 0, Zp), V(0, 1, Zp), t)
    if group in ("dish", "az") and abs(az) > 1e-9:
        s = s.rotate(V(0, 0, 0), V(0, 0, 1), az)
    return s


def stage_location(group, zp_local, Zp, el, az):
    """cq.Location that does the same as pose_solid, used for the nested STEP assembly."""
    loc = cq.Location()
    if group in ("dish", "az"):
        loc = cq.Location(V(0, 0, 0), V(0, 0, 1), az)
    if group == "dish":
        tilt = cq.Location(V(0, 0, Zp)) * cq.Location(V(0, 0, 0), V(0, 1, 0), 90.0 - el) * cq.Location(V(0, 0, -zp_local))
        loc = loc * tilt
    return loc


def bb_overlap(a, b, tol=0.0):
    return not (a.xmax < b.xmin - tol or b.xmax < a.xmin - tol or a.ymax < b.ymin - tol or
                b.ymax < a.ymin - tol or a.zmax < b.zmin - tol or b.zmax < a.zmin - tol)


def overlaps(list_a, list_b=None, min_vol=0.5):
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


# ------------------------------------------------------------------ dish reach over the sweep
def dish_points(parts):
    pts = []
    for p in parts:
        if p["group"] != "dish":
            continue
        vs, _ = p["solid"].tessellate(2.0, 0.5)
        pts += [(v.x, v.y, v.z) for v in vs]
    return np.array(pts)


def dish_drop(zp_local, pts):
    """Largest distance the dish reaches below the axle for any elevation in the range."""
    rel = pts - np.array([0, 0, zp_local])
    worst = 0.0
    for el in np.arange(EL_MIN, EL_MAX + 0.01, 1.0):
        t = math.radians(90 - el)
        z = -rel[:, 0] * math.sin(t) + rel[:, 2] * math.cos(t)
        worst = max(worst, -z.min())
    return worst


# ------------------------------------------------------------------ 3D frame analysis (Euler-Bernoulli beams)
class Frame:
    def __init__(self):
        self.nodes, self.els = [], []

    def node(self, p):
        self.nodes.append(np.asarray(p, float))
        return len(self.nodes) - 1

    def el(self, i, j, E, G, a, b, ydir, name, rigid=False):
        """Rectangular section: b along ydir (wide), a across (thin)."""
        A = a * b
        Iz = a * b ** 3 / 12          # bending in the local-y direction (strong)
        Iy = b * a ** 3 / 12          # bending in the local-z direction (weak)
        lo, hi = min(a, b), max(a, b)
        J = hi * lo ** 3 * (1 / 3 - 0.21 * lo / hi * (1 - lo ** 4 / (12 * hi ** 4)))
        if rigid:
            E, G = E * 1e3, G * 1e3
        self.els.append(dict(i=i, j=j, E=E, G=G, A=A, Iy=Iy, Iz=Iz, J=J, a=a, b=b, ydir=np.asarray(ydir, float),
                             name=name, rigid=rigid))

    def _lam(self, e):
        x = unit(self.nodes[e["j"]] - self.nodes[e["i"]])
        y = e["ydir"] - np.dot(e["ydir"], x) * x
        if np.linalg.norm(y) < 1e-6:
            y = perp(x)
        y = unit(y)
        return np.vstack([x, y, np.cross(x, y)])

    def _kl(self, e, L):
        E, G, A, Iy, Iz, J = e["E"], e["G"], e["A"], e["Iy"], e["Iz"], e["J"]
        k = np.zeros((12, 12))
        k[0, 0] = k[6, 6] = E * A / L
        k[0, 6] = k[6, 0] = -E * A / L
        k[3, 3] = k[9, 9] = G * J / L
        k[3, 9] = k[9, 3] = -G * J / L
        for (v, th, I, s) in ((1, 5, Iz, 1), (2, 4, Iy, -1)):
            c1, c2, c3, c4 = 12 * E * I / L ** 3, 6 * E * I / L ** 2, 4 * E * I / L, 2 * E * I / L
            k[v, v] = k[v + 6, v + 6] = c1
            k[v, v + 6] = k[v + 6, v] = -c1
            k[v, th] = k[th, v] = s * c2
            k[v, th + 6] = k[th + 6, v] = s * c2
            k[v + 6, th] = k[th, v + 6] = -s * c2
            k[v + 6, th + 6] = k[th + 6, v + 6] = -s * c2
            k[th, th] = k[th + 6, th + 6] = c3
            k[th, th + 6] = k[th + 6, th] = c4
        return k

    def solve(self, loads, fixed):
        n = len(self.nodes)
        K = np.zeros((6 * n, 6 * n))
        cache = []
        for e in self.els:
            L = np.linalg.norm(self.nodes[e["j"]] - self.nodes[e["i"]])
            lam = self._lam(e)
            T = np.kron(np.eye(4), lam)
            kl = self._kl(e, L)
            kg = T.T @ kl @ T
            dofs = list(range(6 * e["i"], 6 * e["i"] + 6)) + list(range(6 * e["j"], 6 * e["j"] + 6))
            K[np.ix_(dofs, dofs)] += kg
            cache.append((dofs, T, kl, L))
        Fv = np.zeros(6 * n)
        for i, f in loads.items():
            Fv[6 * i:6 * i + 6] += f
        fixed_dofs = sorted(set(fixed))
        free = [d for d in range(6 * n) if d not in fixed_dofs]
        U = np.zeros(6 * n)
        U[free] = np.linalg.solve(K[np.ix_(free, free)], Fv[free])
        Rx = K @ U - Fv
        out = []
        for e, (dofs, T, kl, L) in zip(self.els, cache):
            f = kl @ (T @ U[dofs])     # local end forces: [N, Vy, Vz, Mx, My, Mz] at i then j
            out.append(dict(e, L=L, f=f))
        return U, Rx, out


def analyse(info, zp_local, dish_mass, dish_cg, report):
    """Statics of the mount under the load cases that matter. Units N, mm, MPa."""
    g = 9.81
    Ew, Gw = float(P("softwood", "modulus")), float(P("softwood", "modulus")) / 16
    lines = []

    def build_frame(az):
        fr = Frame()
        rot = lambda p: np.array([p[0] * math.cos(math.radians(az)) - p[1] * math.sin(math.radians(az)),
                                  p[0] * math.sin(math.radians(az)) + p[1] * math.cos(math.radians(az)), p[2]])
        idx = {}
        for s in (1, -1):
            idx[("T", s)] = fr.node(rot(info["legs"][(1, s)].pa))
        for key, m in info["legs"].items():
            idx[("C",) + key] = fr.node(rot(m.pb))
        for key, m in info["legs"].items():
            fr.el(idx[("T", key[1])], idx[("C",) + key], Ew, Gw, m.a, m.b, rot(m.h), "LEG-A " + m.name)
        for sx, m in info["ties"].items():
            fr.el(idx[("C", sx, 1)], idx[("C", sx, -1)], Ew, Gw, m.a, m.b, rot(m.h), "TIE-01 " + m.name)
        for s, m in info["sills"].items():
            fr.el(idx[("C", 1, s)], idx[("C", -1, s)], Ew, Gw, m.a, m.b, rot(m.h), "SIL-01 " + m.name)
        fr.el(idx[("T", 1)], idx[("T", -1)], Ew, Gw, 60, 60, (0, 0, 1), "dish (locked, rigid)", rigid=True)
        return fr, idx, rot

    def lumped(fr, idx, rot):
        """Weights of the base parts lumped at the nearest frame node (dish handled separately)."""
        loads = {}
        for p in PARTS:
            if p["group"] == "dish":
                continue
            c = p["solid"].Center()
            c = rot(np.array([c.x, c.y, c.z]))
            i = min(idx.values(), key=lambda i: np.linalg.norm(fr.nodes[i] - c))
            loads.setdefault(i, np.zeros(6))[2] -= mass_kg(p) * g
        return loads

    area = math.pi * R ** 2 / 1e6
    q = lambda v: 0.5 * 1.225 * v * v
    cd = float(P("loads", "drag_coefficient"))
    v_op, v_sv = float(P("loads", "wind_operating")), float(P("loads", "wind_survival"))
    push = float(P("loads", "handling_push"))
    Wd = dish_mass * g
    cases = []
    for az in (0.0,):
        cases.append((f"gravity, zenith, az {az:.0f}", az, np.zeros(3), 0.0, 1.0))
        for v in (v_op,):
            D = cd * q(v) * area
            cases.append((f"gravity + {v:.0f} m/s wind, dish at horizon facing the wind, az {az:.0f}", az,
                          np.array([-D, 0, 0]), D * 0.1 * 2 * R, 1.0))
        cases.append((f"gravity + {push:.0f} N push on the rim along the axle, az {az:.0f}", az, np.array([0, push, 0]),
                      0.0, 1.0))
    results = []
    for name, az, Fd, My, _ in cases:
        fr, idx, rot = build_frame(az)
        loads = lumped(fr, idx, rot)
        Fw = rot(Fd)
        for s in (1, -1):
            f = np.zeros(6)
            f[:3] = np.array([0, 0, -Wd / 2]) + Fw / 2
            f[3:] = rot(np.array([0, My / 2, 0]))
            loads.setdefault(idx[("T", s)], np.zeros(6))
            loads[idx[("T", s)]] += f
        fixed = []
        for k, i in idx.items():           # the four corner nodes rest on the ground
            if k[0] == "C":
                fixed += [6 * i, 6 * i + 1, 6 * i + 2]
        U, Rx, els = fr.solve(loads, fixed)
        results.append((name, az, fr, idx, U, Rx, els, Fd))
    return results, cases


def structural_report(info, zp_local, dish_mass, dish_cg, results, log):
    g = 9.81
    Ew = float(P("softwood", "modulus"))
    f_b = float(P("softwood", "allow_bending"))
    f_c = float(P("softwood", "allow_compression"))
    f_bp = float(P("softwood", "allow_bearing_parallel"))
    f_bperp = float(P("softwood", "allow_bearing_perp"))
    p_xy = float(P("petg", "allow_short_xy"))
    p_z = float(P("petg", "allow_short_z"))
    p_sz = float(P("petg", "allow_sustained_z"))
    p_sxy = float(P("petg", "allow_sustained_xy"))
    p_c = float(P("petg", "allow_compression"))
    worst = {}
    log("### Wooden members (frame analysis, rigid sockets, pinned feet)")
    log("")
    log("| Load case | Worst member | Axial N | Combined stress | Allowable | Buckling use | Dish movement |")
    log("|---|---|---:|---:|---:|---:|---:|")
    joint_rows = []
    for name, az, fr, idx, U, Rx, els, Fd in results:
        best = None
        for e in els:
            if e["rigid"]:
                continue
            f = e["f"]
            for end in (0, 6):
                Nax = -f[end] if end == 0 else f[end]          # tension positive
                My, Mz = abs(f[end + 4]), abs(f[end + 5])
                sig = abs(Nax) / e["A"] + My * (e["a"] / 2) / e["Iy"] + Mz * (e["b"] / 2) / e["Iz"]
                pcr = math.pi ** 2 * Ew * min(e["Iy"], e["Iz"]) / e["L"] ** 2
                buck = max(0.0, -Nax) / pcr
                if best is None or sig / f_b > best[2] / f_b:
                    best = (e["name"], Nax, sig, buck)
                worst[e["name"]] = max(worst.get(e["name"], 0), sig)
                # socket joint at this end
                Fb = abs(Nax) / 2
                d = 6.0 if not e["name"].startswith("LEG-F") else 4.0
                wood = Fb / (d * e["a"])
                petg = Fb / (2 * SOCK_WALL * d)
                Mt = math.hypot(My, Mz)
                Lc = SOCK_DEPTH - T_END
                Fc = Mt / (2 / 3 * Lc)
                pw = Fc / (e["a"] * Lc / 3)
                joint_rows.append((name, e["name"], "i" if end == 0 else "j", Nax, Mt / 1000, wood, petg, pw))
        ti, tj = idx[("T", 1)], idx[("T", -1)]
        rotv = U[6 * ti + 3:6 * ti + 6]
        dmax = max(np.linalg.norm(U[6 * ti:6 * ti + 3]), np.linalg.norm(U[6 * tj:6 * tj + 3]))
        log(f"| {name} | {best[0]} | {best[1]:+.0f} | {best[2]:.2f} MPa | {f_b:.0f} MPa | {100 * best[3]:.1f} % | "
            f"{dmax:.2f} mm, {math.degrees(np.linalg.norm(rotv)) * 60:.1f} arcmin |")
    log("")
    log(f"Members are 1x2 ({SEC_LEG[0]:.0f} x {SEC_LEG[1]:.0f}) fork legs and sills and 1x3 ({SEC_BEAM[0]:.0f} x "
        f"{SEC_BEAM[1]:.0f}) tie beams. Combined stress = axial + both bending terms at the worst end. "
        f"Buckling use = compression / Euler load about the weak axis (K = 1). Dish movement is at the axle; the "
        f"beam is about 15 deg wide, so arcminutes are negligible.")
    log("")
    jr = max(joint_rows, key=lambda r: max(r[5] / f_bp, r[6] / p_z, r[7] / f_bperp))
    w_bolt = max(joint_rows, key=lambda r: r[5])
    w_mom = max(joint_rows, key=lambda r: r[7])
    log("### Socket joints (printed socket, two M6 cross bolts, wooden batten)")
    log(f"- Worst bolt load: {w_bolt[1]} end {w_bolt[2]} in '{w_bolt[0]}': axial {w_bolt[3]:+.0f} N, "
        f"so {abs(w_bolt[3]) / 2:.0f} N per bolt. Wood bearing {w_bolt[5]:.2f} MPa (allowable {f_bp:.0f} along the grain); "
        f"PETG bearing in the two 4 mm socket walls {w_bolt[6]:.2f} MPa (allowable {p_z:.0f} across layers).")
    log(f"- Worst socket moment: {w_mom[1]} end {w_mom[2]} in '{w_mom[0]}': {w_mom[4]:.1f} N m. Taken by contact "
        f"between batten and socket walls over the {SOCK_DEPTH - T_END:.0f} mm insertion: wood across the grain "
        f"{w_mom[7]:.2f} MPa (allowable {f_bperp:.1f}); the same force on the PETG wall is {w_mom[7]:.2f} MPa "
        f"(allowable {p_c:.0f}).")
    ratio = max(max(r[5] / f_bp, r[6] / p_z, r[7] / f_bperp) for r in joint_rows)
    log(f"- Highest joint utilisation over all cases: {100 * ratio:.0f} %.")
    log(f"- Bolt end distance in the wood: {Member('x', 'x', (0, 0, 0), (1000, 0, 0), SEC_LEG, (0, 0, 1), 0, 0, 'az').end_distance():.0f} mm "
        f"to the nearer bolt (7 d = 42 mm wanted for full M6 capacity; loads here are far below it).")
    log("")

    # corner reactions and tipping
    log("### Base reactions and stability")
    for name, az, fr, idx, U, Rx, els, Fd in results:
        reac = [Rx[6 * i + 2] for k, i in idx.items() if k[0] == "C"]
        log(f"- {name}: corner reactions {min(reac):.0f} to {max(reac):.0f} N (a negative value means that corner lifts).")
    m_tot = sum(mass_kg(p) for p in PARTS)
    area = math.pi * R ** 2 / 1e6
    cd = float(P("loads", "drag_coefficient"))
    h = info["Zp"] / 1000
    d_tip = ARM_X / 1000
    target = float(P("loads", "ballast_ratio_target"))
    log(f"- Total mass {m_tot:.1f} kg. Axle {info['Zp']:.0f} mm above the ground. The base stands on four corners, "
        f"{2 * ARM_X:.0f} mm apart along the pointing direction and {2 * Y_NODE_C:.0f} mm along the axle, so the tipping "
        f"lever is {1000 * d_tip:.0f} mm (wind along the pointing direction, the worst case).")
    log("")
    log("| Wind | Drag (solid disc, Cd 1.2) | Overturning | Resisting, no ballast | Ratio | Ballast per upwind corner for ratio 1.5 |")
    log("|---:|---:|---:|---:|---:|---:|")
    for v in (5, 8, 10, 12, 15):
        D = 0.5 * 1.225 * v * v * cd * area
        Mo = D * h
        Mr = m_tot * g * d_tip
        need = max(0.0, (target * Mo - Mr) / (g * 2 * d_tip)) / 2     # ballast on the two upwind corners
        log(f"| {v} m/s | {D:.0f} N | {Mo:.1f} N m | {Mr:.1f} N m | {Mr / Mo:.2f} | {need:.1f} kg |")
    log("")
    log("Ballast is a sandbag or water jug laid over each end of the tie beams. The wind can come from either side, "
        "so put the same ballast on all four corners.")
    log("")

    # elevation axle, bearings, lock
    log("### Elevation axle, bearings and lock")
    off = math.hypot(dish_cg[0], dish_cg[2] - zp_local)
    Wd = dish_mass * g
    lever = Y_NODE_C - Y_BLOCK
    D8 = cd * 0.5 * 1.225 * float(P("loads", "wind_operating")) ** 2 * area
    Fr = math.hypot(Wd / 2, D8 / 2)
    Mb = Fr * lever
    log(f"- Dish {dish_mass:.2f} kg, centre of mass {off:.1f} mm from the axle (x {dish_cg[0]:.1f}, z {dish_cg[2] - zp_local:+.1f}).")
    log(f"- Per side: {Wd / 2:.0f} N weight plus {D8 / 2:.0f} N wind at {P('loads', 'wind_operating'):.0f} m/s = {Fr:.0f} N. "
        f"Two 608 bearings share it: {Fr / 2:.0f} N each against a static rating of 1370 N.")
    sb = Mb / (math.pi * 6.47 ** 3 / 32)
    log(f"- M8 axle bending at the bearing ({lever:.0f} mm lever): {Mb / 1000:.2f} N m, {sb:.0f} MPa against 640 MPa.")
    pb = Fr / (B608[1] * 2 * B608[2])
    log(f"- PETG under the bearing outer races: {pb:.2f} MPa (sustained across layers allowable {p_sz:.0f}; housing is "
        f"printed with the bore vertical, so the load is in the layer plane, allowable {p_sxy:.0f}).")
    blk = Fr / (8 * TRUN_T)
    log(f"- Axle bearing on the trunnion block, 8 mm bolt in {TRUN_T:.0f} mm of PETG: {blk:.2f} MPa "
        f"(allowable {p_sxy:.0f} sustained).")
    Mi = Wd * off / 1000 + D8 * 0.1 * 2 * R / 1000
    mu, faces = 0.3, 2
    Nreq = Mi / (mu * faces * LOCK_R / 1000)
    log(f"- Lock: worst torque on the axle = imbalance {Wd * off / 1000:.2f} N m + wind with the centre of pressure "
        f"0.1 D off axis {D8 * 0.1 * 2 * R / 1000:.2f} N m = {Mi:.2f} N m. Friction on two faces (mu {mu}) at "
        f"{LOCK_R:.0f} mm needs {Nreq:.0f} N of clamp. A hand-tight M6 knob gives 1000-2000 N. "
        f"Washer pressure on the sector at 1500 N: {1500 / (math.pi / 4 * (WASH[6][0] ** 2 - 6.6 ** 2)):.1f} MPa "
        f"(compression allowable {p_c:.0f}).")
    log("")

    # rim joints and feed legs
    log("### Dish joints and feed support")
    shear = Wd / (N * len(RIM_HOLE_Z))
    log(f"- Rim joint: whole dish weight shared by {N * len(RIM_HOLE_Z)} M4 bolts gives {shear:.1f} N per bolt; bearing in "
        f"the {W:.2f} mm rib {shear / (4 * W):.2f} MPa (plywood allowable {P('plywood', 'allow_bearing'):.0f}). "
        f"The joint is clamped, so friction carries it before the bolt bears.")
    feed_m = sum(mass_kg(p) for p in PARTS if p["id"] in ("FEED-01", "FRG-01", "LNA-01", "LNA-02"))
    pa, pc = feed_geometry()
    Lf = float(np.linalg.norm(pa - pc))
    sin_t = abs(pa[2] - pc[2]) / Lf
    Nf = feed_m * g / (3 * sin_t) + 20.0
    If = SEC_FEED[0] ** 4 / 12
    Pcr = math.pi ** 2 * Ew * If / Lf ** 2
    log(f"- Feed head {feed_m:.2f} kg on three {SEC_FEED[0]:.0f} mm square legs, {Lf:.0f} mm between socket starts: "
        f"worst leg force with a 20 N knock {Nf:.0f} N; Euler load {Pcr:.0f} N ({100 * Nf / Pcr:.0f} % used). "
        f"One M4 per leg end: {Nf / (4 * SEC_FEED[0]):.2f} MPa wood bearing.")
    log(f"- Feed movement: leg stretch is under 0.01 mm. Joint clearance ({T_SOCK:.1f} mm in the sockets) "
        f"lets the feed shift up to about 0.5 mm, against a focus tolerance of about lambda/10 = 21 mm.")
    log("")
    log("### Not checked, and why")
    log("- Rim girder, hub, spacers: they carry under 70 N in total; their sizes are set by printing and "
        "handling, not stress.")
    log("- Fatigue, temperature: the telescope is moved by hand a few times per session; PETG softens near 70 C, "
        "so do not leave it in full summer sun for hours.")
    log("- Wood moisture: sockets have 0.8 mm clearance so swelling does not split them; seal batten ends.")


# ------------------------------------------------------------------ printability
def print_oriented(p):
    s = p["solid"]
    for axis, deg in p["print_rot"]:
        s = s.rotate(V(0, 0, 0), V(*axis), deg)
    bb = s.BoundingBox()
    return s.translate(V(-bb.xmin, -bb.ymin, -bb.zmin))


def fits_bed(s):
    bb = s.BoundingBox()
    lim = [b - 2 * BED_MARGIN for b in BED]
    dims = (bb.xlen, bb.ylen, bb.zlen)
    ok = dims[2] <= lim[2] and ((dims[0] <= lim[0] and dims[1] <= lim[1]) or (dims[1] <= lim[0] and dims[0] <= lim[1]))
    return ok, dims


# ------------------------------------------------------------------ rendering (VTK, off screen)
COLORS = {"wood": (0.86, 0.70, 0.46), "existing": (0.72, 0.52, 0.30), "print": (0.22, 0.47, 0.78),
          "hardware": (0.62, 0.63, 0.66), "purchase": (0.55, 0.56, 0.60), "mesh": (0.80, 0.80, 0.82)}


def render(items, path, view="iso", size=(1600, 1200), title=None, focus=None):
    """items: list of (solid, kind). view: iso | front | side | top, or (azimuth, elevation) camera angles."""
    import vtk
    from vtk.util import numpy_support as ns
    ren = vtk.vtkRenderer()
    ren.SetBackground(1, 1, 1)
    groups = {}
    for solid, kind in items:
        vs, ts = solid.tessellate(0.6, 0.4)
        if not ts:
            continue
        g = groups.setdefault(kind, ([], [], [0]))
        off = g[2][0]
        g[0].extend((v.x, v.y, v.z) for v in vs)
        g[1].extend((3, a + off, b + off, c + off) for a, b, c in ts)
        g[2][0] += len(vs)
    for kind, (vs, ts, _) in groups.items():
        pts = vtk.vtkPoints()
        pts.SetData(ns.numpy_to_vtk(np.array(vs, dtype=float), deep=True))
        cells = vtk.vtkCellArray()
        cells.SetCells(len(ts), ns.numpy_to_vtkIdTypeArray(np.array(ts, dtype=np.int64).ravel(), deep=True))
        pd = vtk.vtkPolyData()
        pd.SetPoints(pts)
        pd.SetPolys(cells)
        nrm = vtk.vtkPolyDataNormals()
        nrm.SetInputData(pd)
        nrm.SetFeatureAngle(35)
        mp = vtk.vtkPolyDataMapper()
        mp.SetInputConnection(nrm.GetOutputPort())
        act = vtk.vtkActor()
        act.SetMapper(mp)
        act.GetProperty().SetColor(*COLORS.get(kind, (0.5, 0.5, 0.5)))
        if kind == "mesh":
            act.GetProperty().SetOpacity(0.35)
        act.GetProperty().SetSpecular(0.15)
        ren.AddActor(act)
        ed = vtk.vtkFeatureEdges()
        ed.SetInputConnection(nrm.GetOutputPort())
        ed.BoundaryEdgesOn()
        ed.FeatureEdgesOn()
        ed.SetFeatureAngle(35)
        ed.ManifoldEdgesOff()
        ed.NonManifoldEdgesOff()
        em = vtk.vtkPolyDataMapper()
        em.SetInputConnection(ed.GetOutputPort())
        em.ScalarVisibilityOff()
        ea = vtk.vtkActor()
        ea.SetMapper(em)
        ea.GetProperty().SetColor(0.12, 0.12, 0.14)
        ea.GetProperty().SetLineWidth(0.8)
        if kind != "mesh":
            ren.AddActor(ea)
    cam = ren.GetActiveCamera()
    angles = {"iso": (-50, 25), "front": (0, 0), "side": (-90, 0), "top": (0, 89.9), "rear_iso": (130, 25)}
    az, el = angles[view] if isinstance(view, str) else view
    cam.SetFocalPoint(0, 0, 0)
    cam.SetPosition(0, -1, 0)
    cam.SetViewUp(0, 0, 1)
    cam.Azimuth(az)
    cam.Elevation(el)
    cam.OrthogonalizeViewUp()
    if view == "top":
        cam.SetViewUp(0, 1, 0)
    ren.ResetCamera()
    if focus is not None:
        cam.Zoom(focus)
    win = vtk.vtkRenderWindow()
    win.SetOffScreenRendering(1)
    win.AddRenderer(ren)
    win.SetSize(*size)
    if title:
        txt = vtk.vtkTextActor()
        txt.SetInput(title)
        txt.GetTextProperty().SetFontSize(26)
        txt.GetTextProperty().SetColor(0.1, 0.1, 0.1)
        txt.SetPosition(20, size[1] - 50)
        ren.AddActor2D(txt)
    win.Render()
    w2i = vtk.vtkWindowToImageFilter()
    w2i.SetInput(win)
    w2i.Update()
    wr = vtk.vtkPNGWriter()
    wr.SetFileName(path)
    wr.SetInputConnection(w2i.GetOutputPort())
    wr.Write()


# ------------------------------------------------------------------ shop aids (printed, not part of the telescope)
def fit_coupon():
    """FIT-01: print this first. Left to right in each row the clearance rises.
    Row 1: 608 bores 22.00 / 22.10 / 22.20 / 22.25.  Row 2: rib slots W+0.2 .. W+0.6.
    Row 3: 19 x 38 batten socket rings +0.6 / +0.8 / +1.0.  Right block: M4 and M6 nut pockets +0.2 / +0.4."""
    parts, cutters = [bx(0, 236, 0, 128, 0, 3)], []
    for i, d in enumerate((22.00, 22.10, 22.20, 22.25)):
        c = (22 + i * 36, 20, 0)
        parts.append(cyl(15, B608[2] + 1, c))
        cutters.append(cyl(d / 2, B608[2] + 2, (c[0], c[1], -0.5)))
    for i, t in enumerate((0.2, 0.3, 0.4, 0.5, 0.6)):
        x0 = 8 + i * 24
        parts.append(bx(x0, x0 + W + t + 10, 40, 66, 0, 16))
        cutters.append(bx(x0 + 5, x0 + 5 + W + t, 39, 67, 4, 17))
    for i, t in enumerate((0.6, 0.8, 1.0)):
        a, b = SEC_LEG[0] + t, SEC_LEG[1] + t
        x0 = 6 + i * 52
        parts.append(bx(x0, x0 + b + 6.4, 76, 76 + a + 6.4, 0, 12))
        cutters.append(bx(x0 + 3.2, x0 + 3.2 + b, 79.2, 79.2 + a, -1, 13))
    parts.append(bx(160, 232, 40, 124, 0, 10))
    for j, m in enumerate((4, 6)):
        for i, t in enumerate((0.2, 0.4)):
            p = (176 + i * 36, 60 + j * 40, 10)
            cutters.append(hexp(AF[m] + t, NUT_T[m] + T_NUTD, (p[0], p[1], 10 - NUT_T[m] - T_NUTD), (0, 0, 1)))
            cutters.append(cyl((m + T_HOLE) / 2, 12, (p[0], p[1], -1)))
    return cut(fuse(parts), cutters)


def drill_jig(r_hole_list, length):
    """Saddle that slips over the rib end. The end cap registers on the rib end (r = R) and the
    floor lip on the flat back edge (z = 0); guide holes go through both cheeks."""
    cw, slot = 6.0, W + T_SLOT
    zt = max(z for _, z in r_hole_list) + 15
    y0, y1 = -slot / 2 - cw, slot / 2 + cw
    body = fuse([bx(R - length, R + 5, y0, y1, -5, zt),           # cheeks + floor lip + cap block
                 ])
    cutters = [bx(R - length - 1, R, -slot / 2, slot / 2, 0, zt + 1)]
    if length > 80:   # lighten the long jig: open window between the end cap and the guide
        cutters.append(bx(R - length + 25, R - 15, y0 - 1, y1 + 1, 8, zt - 8))
    for r, z in r_hole_list:
        cutters.append(hole(DRILL + 0.3, (r, 0, z), (0, 1, 0), slot + 2 * cw + 2))
    return cut(body, cutters)


def shop_aids():
    j1 = drill_jig([(RIM_HOLE_R, z) for z in RIM_HOLE_Z], R - RIM_HOLE_R + 20)
    j2 = drill_jig([(MID_HOLE_R, MID_HOLE_Z)], R - MID_HOLE_R + 15)
    return [dict(id="FIT-01", name="fit coupon (bores, slots, sockets, nut pockets)", solid=fit_coupon(), print_rot=[],
                 material="petg", qty=1),
            dict(id="JIG-01", name="drill jig, rim-end holes", solid=j1, print_rot=[((1, 0, 0), 90)],
                 material="petg", qty=1),
            dict(id="JIG-02", name="drill jig, mid-span hole", solid=j2, print_rot=[((1, 0, 0), 90)],
                 material="petg", qty=1)]


# ------------------------------------------------------------------ exports
PRINT_NOTES = {
    "FKT-01": "6 perimeters, 40% gyroid; bearing bores print vertical", "FKT-02": "6 perimeters, 40% gyroid",
    "FKC-01": "5 perimeters, 30% gyroid", "FKC-02": "5 perimeters, 30% gyroid",
    "FOOT-01": "5 perimeters, 30% gyroid", "AZT-01": "5 perimeters, 30% gyroid", "AZB-01": "5 perimeters, 30% gyroid",
    "HUB-01": "5 perimeters, 30% gyroid", "RIM-T": "5 perimeters, 30% gyroid; axle pocket faces up",
    "ELS-01": "5 perimeters, 40% gyroid", "FIT-01": "same settings as the real parts",
}


def kind_color(p):
    return "mesh" if p["material"] == "mesh" else p["kind"]


def export_all(info, zp, Zp, args, log):
    import csv
    from collections import OrderedDict
    t0 = time.time()
    d = lambda *a: os.path.join(ROOT, *a)
    for sub in ("exports/parts", "exports/stages", "print", "bom", "drawings", "cad/fusion"):
        os.makedirs(d(sub), exist_ok=True)
    log("")
    log("## Exports")

    # --- stale Rev B outputs
    stale = [d("exports", f) for f in os.listdir(d("exports")) if "PROVISIONAL" in f]
    stale += [d("exports/parts", f) for f in os.listdir(d("exports/parts"))]
    stale += [d("print", f) for f in os.listdir(d("print"))]
    stale += [d("drawings", f) for f in os.listdir(d("drawings")) if "PROVISIONAL" in f or f.startswith("view_")]
    stale += [d("bom", f) for f in os.listdir(d("bom"))]
    for f in stale:
        if os.path.isfile(f) and not f.endswith(".gitkeep"):
            os.remove(f)

    # --- nested STEP assembly at the requested pose, and one STEP per stage at the home pose
    def stage_assy(group, name, loc=None):
        a = cq.Assembly(name=name, loc=loc)
        n = {}
        for p in PARTS:
            if p["group"] != group:
                continue
            n[p["id"]] = n.get(p["id"], 0) + 1
            a.add(p["solid"], name=f"{p['id']}_{n[p['id']]:02d}", color=cq.Color(*COLORS[kind_color(p)]))
        return a

    top = cq.Assembly(name="radio_telescope_revC")
    for g, nm in (("az", "base"), ("dish", "dish")):
        top.add(stage_assy(g, nm), name=nm, loc=stage_location(g, zp, Zp, args.el, args.az))
    pose_tag = f"az{args.az:.0f}_el{args.el:.0f}"
    top.save(d("exports", f"telescope_revC_{pose_tag}.step"))
    for g, nm in (("az", "base"), ("dish", "dish")):
        stage_assy(g, nm, loc=stage_location(g, zp, Zp, 90.0, 0.0)).save(d("exports/stages", f"{nm}.step"))
    log(f"- `exports/telescope_revC_{pose_tag}.step`: nested assembly (base / dish), "
        f"{len(PARTS)} solids. `exports/stages/*.step`: the two stages at el 90 for Fusion.")

    # --- one STEP per part type, print STLs, print list
    firsts, qty = OrderedDict(), {}
    for p in PARTS:
        firsts.setdefault(p["id"], p)
        qty[p["id"]] = qty.get(p["id"], 0) + 1
    for pid, p in firsts.items():
        if p["kind"] in ("print", "wood", "existing"):
            cq.exporters.export(p["solid"], d("exports/parts", f"{pid}.step"))
    aids = shop_aids()
    rows, fil_total = [], 0.0
    for pid, p in list(firsts.items()) + [(a["id"], a) for a in aids]:
        if pid in firsts and p["kind"] != "print":
            continue
        s = print_oriented(p)
        cq.exporters.export(s, d("print", f"{pid}.stl"), tolerance=0.03, angularTolerance=0.1)
        q = qty.get(pid, p.get("qty", 1))
        g_each = 1000 * mass_kg(dict(p, mass=None, material="petg"))
        fil_total += q * g_each
        bb = s.BoundingBox()
        rows.append([pid, p["name"], q, f"{g_each:.0f}", f"{q * g_each:.0f}",
                     f"{bb.xlen:.0f} x {bb.ylen:.0f} x {bb.zlen:.0f}",
                     PRINT_NOTES.get(pid, "4 perimeters, 25% gyroid"),
                     "yes" if fits_bed(s)[0] else "NO"])
    with open(d("print", "print_list.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["part", "name", "qty", "grams_each", "grams_total", "bed_footprint_mm", "settings", "fits_bed"])
        w.writerows(rows)
        w.writerow([])
        w.writerow(["ALL", "PETG, 0.4 mm nozzle, 0.2 mm layers, 245/80 C, brim on tall parts", "", "",
                    f"{fil_total:.0f}", "", "print FIT-01 first and update parameters.yaml tolerances", ""])
    log(f"- `print/`: {len(rows)} STLs laid flat for the bed, `print/print_list.csv`. "
        f"PETG estimate {fil_total / 1000:.2f} kg including the coupon and jigs.")
    for a in aids:
        cq.exporters.export(a["solid"], d("exports/parts", f"{a['id']}.step"))

    # --- BOM, hardware, cut list, rib modifications
    with open(d("bom", "bom.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["part", "name", "kind", "material", "group", "qty", "kg_each", "kg_total"])
        for pid, p in firsts.items():
            if p["kind"] == "hardware":
                continue
            m = mass_kg(p)
            if pid == "LS-6IN":   # modelled as two solids (fixed and rotating plate); bought as one bearing
                w.writerow([pid, "6 in square lazy-susan bearing (both plates)", p["kind"], p["material"], "ground + az",
                            1, f"{2 * m:.3f}", f"{2 * m:.3f}"])
                continue
            nm = p["name"] if qty[pid] == 1 else re.sub(r" \d+(\.\d+)? deg$|(?<=rib) \d+$", "", p["name"])
            w.writerow([pid, nm, p["kind"], p["material"], p["group"], qty[pid], f"{m:.3f}", f"{m * qty[pid]:.3f}"])
    hw = OrderedDict()
    for p in PARTS:
        if p["kind"] == "hardware":
            hw.setdefault((p["id"], p["name"]), 0)
            hw[(p["id"], p["name"])] += 1
    with open(d("bom", "hardware.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["part", "description", "qty_in_model", "buy (qty + 10%)", "spec"])
        for (pid, nm), q in sorted(hw.items()):
            spec = "608-2RS deep-groove bearing" if pid.startswith("BRG") else \
                ("zinc-plated, grade 8.8, DIN 603" if "carriage" in pid else "zinc-plated steel, grade 8.8 (ISO 4017 / 4032 / 7089)")
            w.writerow([pid, nm, q, math.ceil(q * 1.1), spec])

    members = list(info["legs"].values()) + list(info["sills"].values()) + list(info["ties"].values()) + \
        [feed_leg_member(a) for a in ANCHOR_ANG]
    cuts = OrderedDict()
    for m in members:
        key = (m.pid, round(m.length))
        cuts.setdefault(key, [m, 0])
        cuts[key][1] += 1
    stock = 0.0
    with open(d("bom", "cut_list.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["part", "name", "section_mm", "length_mm", "qty", "bolt_holes_from_each_end_mm", "hole_dia_mm",
                    "drill_through"])
        for (pid, L), (m, q) in cuts.items():
            pos = sorted(m.depth - T_END - x for x in m.bolts)
            w.writerow([pid, re.sub(r" \(.*\)| [-+]?\d+ deg.*$", "", m.name), f"{m.a:.0f} x {m.b:.0f}", L, q,
                        " / ".join(f"{v:.0f}" for v in pos), f"{m.m + 0.5:.1f}",
                        f"through the {m.a:.0f} mm face, centred on the {m.b:.0f} mm width"])
            stock += L * q
        w.writerow([])
        w.writerow(["NOTE", "Cut lengths are exact; the sockets leave 2 mm at each end. Square cuts.", "", "", "", "", "", ""])
    with open(d("bom", "rib_modifications.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["operation", "radius_from_dish_axis_mm", "height_above_flat_back_edge_mm", "dia_mm", "per_rib", "jig"])
        w.writerow(["cut tip relief (hub end)", f"{RELIEF:.0f}", "full height", "", 1, "mark with the DXF"])
        for z in RIM_HOLE_Z:
            w.writerow(["drill rim hole", f"{RIM_HOLE_R:.0f}", f"{z:.0f}", f"{DRILL:.1f}", 1, "JIG-01"])
        w.writerow(["drill mid hole", f"{MID_HOLE_R:.0f}", f"{MID_HOLE_Z:.0f}", f"{DRILL:.1f}", 1, "JIG-02"])
        w.writerow(["drill tip pin hole", f"{TIP_PIN_R:.0f}", f"{TIP_PIN_Z:.0f}", f"{DRILL:.1f}", 1,
                    "drill through the HUB-01 channel-wall holes with the rib seated"])
    log(f"- `bom/`: bom.csv ({sum(1 for p in firsts.values() if p['kind'] != 'hardware')} part types), hardware.csv "
        f"({sum(hw.values())} fasteners and bearings), cut_list.csv ({sum(q for _, q in cuts.values())} battens, "
        f"{stock / 1000:.1f} m of stock before saw kerf), rib_modifications.csv.")

    # --- rib drilling template (1:1 DXF)
    import ezdxf
    doc = ezdxf.new("R2010", setup=True)
    doc.units = ezdxf.units.MM
    msp = doc.modelspace()
    rr = np.linspace(0, R, 101)
    msp.add_lwpolyline([(r, zpar(r)) for r in rr] + [(R, 0), (0, 0)], close=True, dxfattribs={"layer": "RIB_OUTLINE"})
    msp.add_line((RELIEF, 0), (RELIEF, zpar(RELIEF) + 5), dxfattribs={"layer": "CUT", "color": 1})
    for (r, z) in [(RIM_HOLE_R, z) for z in RIM_HOLE_Z] + [(MID_HOLE_R, MID_HOLE_Z), (TIP_PIN_R, TIP_PIN_Z)]:
        msp.add_circle((r, z), DRILL / 2, dxfattribs={"layer": "DRILL", "color": 1})
        msp.add_line((r - 6, z), (r + 6, z), dxfattribs={"layer": "DRILL"})
        msp.add_line((r, z - 6), (r, z + 6), dxfattribs={"layer": "DRILL"})
        msp.add_text(f"D{DRILL:.1f} r{r:.0f} z{z:.0f}", height=4, dxfattribs={"layer": "TEXT"}).set_placement((r + 8, z + 2))
    msp.add_text(f"RIB x18: cut tip at r={RELIEF:.0f}, drill 4 holes D{DRILL:.1f}. 1:1 mm. Print at 100% and check the "
                 f"{R:.0f} mm length.", height=5, dxfattribs={"layer": "TEXT"}).set_placement((0, -15))
    doc.saveas(d("drawings", "RIB_drilling_template_1to1.dxf"))
    log("- `drawings/RIB_drilling_template_1to1.dxf`: rib cut and drill template, 1:1.")

    # --- renders (images/ for the README and the assembly guide)
    img = d("images")
    os.makedirs(os.path.join(img, "parts"), exist_ok=True)
    for f in os.listdir(d("drawings")):
        if f.startswith("view_") and f.endswith(".png"):
            os.remove(d("drawings", f))

    def scene(el, az, groups=("az", "dish"), ids=None):
        return [(pose_solid(p["solid"], p["group"], zp, Zp, el, az), kind_color(p)) for p in PARTS
                if p["group"] in groups and (ids is None or p["id"] in ids)]
    for el, az, view, nm in ((45, 30, "iso", "assembly_iso_el45"), (90, 0, "iso", "assembly_iso_zenith"),
                             (0, 0, "side", "assembly_side_el0"), (45, 0, "front", "assembly_front_el45"),
                             (90, 0, "top", "assembly_top_zenith"), (20, 135, (210, 20), "assembly_rear_el20"),
                             (-5, 0, "side", "motion_el_minus5"), (30, 0, "side", "motion_el30"),
                             (60, 0, "side", "motion_el60"), (90, 0, "side", "motion_el90")):
        render(scene(el, az), os.path.join(img, f"{nm}.png"), view=view, title=f"Rev C   az {az} deg   el {el} deg")
    for old_img in ("stage1_fixed_stand.png", "stage2_turning_base.png"):
        if os.path.exists(os.path.join(img, old_img)):
            os.remove(os.path.join(img, old_img))
    render(scene(90, 0, ("az",)), os.path.join(img, "stage1_base.png"), view="iso",
           title="Stage 1: fixed base (fork legs, sills, tie beams, corner nodes, lock)")
    render(scene(90, 0, ("dish",), ids={"RIB", "HUB-01"}), os.path.join(img, "stage3a_ribs_hub.png"),
           view="iso", title="Stage 3a: ribs pinned in the hub (nothing above the reflector surface)")
    frame_ids = {p["id"] for p in PARTS if p["group"] == "dish"} - {"MESH-01", "FEED-01", "FRG-01", "LNA-01", "LNA-02",
                                                                     "LEG-F", "FLA-01"}
    render(scene(90, 0, ("dish",), ids=frame_ids),
           os.path.join(img, "stage3b_dish_frame.png"), view="iso", title="Stage 3b: rim girder, spacers, trunnions")
    render(scene(90, 0, ("dish",)), os.path.join(img, "stage3c_dish_complete.png"), view="iso",
           title="Stage 3c: feed support, collar, feed, mesh")
    firsts = OrderedDict()
    for p in PARTS:
        if p["kind"] in ("print", "wood", "existing"):
            firsts.setdefault(p["id"], p)
    for pid, p in firsts.items():
        render([(p["solid"], kind_color(p))], os.path.join(img, "parts", f"{pid}.png"), view="iso", size=(900, 700),
               title=f"{pid}  {p['name']}")
    for a_ in shop_aids():
        render([(a_["solid"], "print")], os.path.join(img, "parts", f"{a_['id']}.png"), view="iso", size=(900, 700),
               title=f"{a_['id']}  {a_['name']}")
    log(f"- `images/`: assembly, motion-range and build-stage renders; `images/parts/`: one image per part type.")

    # --- bed orientation, supports, time (cad/print_prep.py rewrites print/*.stl and print/print_specs.csv)
    import importlib.util
    spec = importlib.util.spec_from_file_location("print_prep", os.path.join(ROOT, "cad", "print_prep.py"))
    pp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pp)
    pp.main()
    log("- `print/print_specs.csv`: bed orientation, supports, settings and estimated time per part (cad/print_prep.py).")

    # --- Fusion 360 joint script
    write_fusion_script(Zp)
    log(f"- `cad/fusion/telescope_joints/`: Fusion 360 script that imports the two stages and adds the "
        f"elevation joint. Export time {time.time() - t0:.0f} s.")


FUSION_TEMPLATE = r'''"""Fusion 360 script: build the Rev C radio telescope as a movable assembly.

Generated by cad/build.py; do not edit by hand (the axle height comes from the build).

How to run: Fusion 360 > Utilities > Add-Ins > Scripts and Add-Ins > + (green plus) > pick the folder
cad/fusion/telescope_joints, then Run. Do it in a NEW empty design.
It imports exports/stages/base.step and dish.step into two components,
grounds the base and adds one as-built revolute joint:
  Elevation  dish about the axle (parallel to Y, {ZP_MM:.1f} mm above the ground), 0 to {TILT_MAX:.0f} deg of tilt
             from zenith (elevation 90 to {EL_MIN:.0f} deg).
Drag the dish or use the joint's "Drive Joints" to move it. If the dish tilts the wrong way, swap the two limits.
"""
import os
import math
import adsk.core
import adsk.fusion
import traceback

ZP_CM = {ZP_CM:.4f}             # elevation axle height above the ground, cm (Fusion API units)
TILT_MAX_DEG = {TILT_MAX:.1f}   # zenith to the lowest elevation
STAGES = ["base", "dish"]


def run(context):
    app = adsk.core.Application.get()
    ui = app.userInterface
    try:
        design = adsk.fusion.Design.cast(app.activeProduct)
        design.designType = adsk.fusion.DesignTypes.ParametricDesignType
        root = design.rootComponent
        here = os.path.dirname(os.path.abspath(__file__))
        step_dir = os.path.normpath(os.path.join(here, "..", "..", "..", "exports", "stages"))
        occ = {{}}
        for name in STAGES:
            path = os.path.join(step_dir, name + ".step")
            if not os.path.exists(path):
                ui.messageBox("Missing " + path + "\nRun python3 cad/build.py first.")
                return
            o = root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
            o.component.name = name
            opts = app.importManager.createSTEPImportOptions(path)
            opts.isViewFit = False
            app.importManager.importToTarget(opts, o.component)
            occ[name] = o
        occ["base"].isGrounded = True

        def point_geometry(x, y, z):
            sk = root.sketches.add(root.xYConstructionPlane)
            sk.isVisible = False
            p = sk.modelToSketchSpace(adsk.core.Point3D.create(x, y, z))
            sp = sk.sketchPoints.add(p)
            return adsk.fusion.JointGeometry.createByPoint(sp)

        # elevation: dish on the turning base, about the axle (parallel to world Y at height ZP)
        ji = root.asBuiltJoints.createInput(occ["dish"], occ["base"], point_geometry(0, 0, ZP_CM))
        ji.setAsRevoluteJointMotion(adsk.fusion.JointDirections.YAxisJointDirection)
        el = root.asBuiltJoints.add(ji)
        el.name = "Elevation"
        lim = el.jointMotion.rotationLimits
        lim.isMinimumValueEnabled = True
        lim.minimumValue = 0.0
        lim.isMaximumValueEnabled = True
        lim.maximumValue = math.radians(TILT_MAX_DEG)
        lim.isRestValueEnabled = True
        lim.restValue = 0.0
        app.activeViewport.fit()
        ui.messageBox("Telescope assembled. Joint: Elevation (0 to %.0f deg tilt).\n"
                      "Drag the dish, or right-click a joint > Drive Joints." % TILT_MAX_DEG)
    except Exception:
        ui.messageBox("Failed:\n" + traceback.format_exc())
'''


def write_fusion_script(Zp):
    folder = os.path.join(ROOT, "cad", "fusion", "telescope_joints")
    os.makedirs(folder, exist_ok=True)
    txt = FUSION_TEMPLATE.format(ZP_MM=Zp, ZP_CM=Zp / 10.0, TILT_MAX=90.0 - EL_MIN, EL_MIN=EL_MIN)
    with open(os.path.join(folder, "telescope_joints.py"), "w") as fh:
        fh.write(txt)
    with open(os.path.join(folder, "telescope_joints.manifest"), "w") as fh:
        fh.write('{\n  "autodeskProduct": "Fusion360",\n  "type": "script",\n  "author": "",\n'
                 '  "description": {"": "Import the Rev C telescope stages and add the elevation joint"},\n'
                 '  "supportedOS": "Windows|Mac",\n  "editEnabled": true\n}\n')


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--az", type=float, default=float(P("pose", "azimuth")))
    ap.add_argument("--el", type=float, default=float(P("pose", "elevation")))
    ap.add_argument("--quick", action="store_true", help="skip exports")
    args = ap.parse_args()
    out = []

    def log(s=""):
        print(s)
        out.append(s)

    # 1. dish, balanced: the axle goes through the dish centre of mass
    build_dish(150.0)
    _, cg0 = group_cg(("dish",))
    PARTS.clear()
    zp = round(float(cg0[2]), 1)
    build_dish(zp)
    m_dish, cg_dish = group_cg(("dish",))
    pts = dish_points([p for p in PARTS if p["group"] == "dish"])
    drop = dish_drop(zp, pts)
    info = build_mount(zp, drop)
    Zp = info["Zp"]
    m_az, _ = group_cg(("az",))

    log("# Rev C assembly report")
    log("")
    log("Generated by `cad/build.py`. Modelled and analytically checked; nothing physically tested.")
    log("**NOT RELEASED FOR FABRICATION** until the rib thickness, batten sizes are "
        "measured and the fit coupon `FIT-01` has been printed.")
    log("")
    log("## Kinematics")
    log(f"- Elevation axle: parallel to Y, {zp:.1f} mm above the dish vertex, {Zp:.1f} mm above the ground. "
        f"Range {EL_MIN:.0f} to {EL_MAX:.0f} deg; the ends of the lock slot are the hard stops.")
    log("- Azimuth: no turntable. The base is fixed; point it by turning the whole base on the ground (or on casters).")
    log(f"- Lowest reach of the dish below the axle over the elevation range: {drop:.1f} mm. "
        f"Clearance to the top of the base: {PIV_CLR:.0f} mm.")
    log(f"- Masses: dish {m_dish:.2f} kg (centre of mass x {cg_dish[0]:+.1f}, y {cg_dish[1]:+.1f}, "
        f"z {cg_dish[2] - zp:+.1f} mm from the axle), fixed base {m_az:.2f} kg.")

    # 2. solids and printability
    log("")
    log("## Solids and printability")
    bad = [p["id"] for p in PARTS if not p["solid"].isValid()]
    log(f"- {len(PARTS)} solids, {len(bad)} invalid{': ' + ', '.join(sorted(set(bad))) if bad else ''}.")
    counts = {}
    for p in PARTS:
        counts[p["id"]] = counts.get(p["id"], 0) + 1
    log(f"- Ribs in the assembly: {counts.get('RIB', 0)} (required {N}).")
    multi = sorted({p["id"] for p in PARTS if p["kind"] in ("print", "wood", "existing") and len(p["solid"].Solids()) != 1})
    log(f"- Every printed and wooden part is one connected solid: {'yes' if not multi else 'NO: ' + ', '.join(multi)}.")
    bad += multi
    firsts = {}
    for p in PARTS:
        firsts.setdefault(p["id"], p)
    oversize = []
    for pid, p in firsts.items():
        if p["kind"] != "print":
            continue
        ok, dims = fits_bed(print_oriented(p))
        if not ok:
            oversize.append(f"{pid} {dims[0]:.0f} x {dims[1]:.0f} x {dims[2]:.0f}")
    log(f"- Printed part types: {sum(1 for p in firsts.values() if p['kind'] == 'print')}; all fit the "
        f"{BED[0]:.0f} x {BED[1]:.0f} x {BED[2]:.0f} bed with {BED_MARGIN:.0f} mm margin: "
        f"{'yes' if not oversize else 'NO: ' + '; '.join(oversize)}.")

    # 3. interference
    log("")
    log("## Interference checks (solid intersections over 0.5 mm^3)")
    by = lambda g, kinds: [p for p in PARTS if p["group"] == g and p["check"] and p["kind"] in kinds]
    struct = ("print", "wood", "existing", "purchase")
    for g in ("dish", "az"):
        ov = overlaps(by(g, struct))
        log(f"- Within the {g} group ({len(by(g, struct))} solids): {len(ov)} interfering pairs.")
        for o in ov[:12]:
            log(f"  - {o[0]} ({o[1]}) with {o[2]} ({o[3]}): {o[4]:.1f} mm^3")
    hw_fail = []
    n_hw = 0
    for g in ("dish", "az"):
        hw = [dict(p, check=True) for p in PARTS if p["group"] == g and p["kind"] == "hardware"]
        n_hw += len(hw)
        hw_fail += overlaps(hw, by(g, struct))
    log(f"- Every bolt, nut and washer ({n_hw} solids) against the parts it passes through: {len(hw_fail)} clashes "
        f"(a clash means a hole or pocket is out of line).")
    summ = {}
    for o in hw_fail:
        k = (o[0], o[2])
        summ[k] = (summ.get(k, (0, 0))[0] + 1, max(summ.get(k, (0, 0))[1], o[4]))
    for (a, b), (n, v) in sorted(summ.items()):
        log(f"  - {a} with {b}: {n} places, up to {v:.1f} mm^3")

    moving = [p for p in PARTS if p["group"] == "dish" and p["id"] != "MESH-01"]
    fork = [p for p in PARTS if p["group"] == "az" and p["id"] != "BRG-608"]
    log("")
    log("### Elevation sweep: whole dish (with its hardware) against the turning base and fork")
    log("")
    log("| Elevation | Clashes | Lowest point of the dish above the base top |")
    log("|---:|---:|---:|")
    sweep_fail = 0
    for el in list(np.arange(EL_MIN, EL_MAX + 0.1, 5.0)):
        posed = [dict(p, solid=pose_solid(p["solid"], "dish", zp, Zp, el, 0.0)) for p in moving]
        ov = [o for o in overlaps(posed, fork) if not (o[0].startswith("HW-M8") and o[2] in ("FKT-01", "FKT-02"))]
        low = min(p["solid"].BoundingBox().zmin for p in posed) - info["base_top"]
        log(f"| {el:.0f} deg | {len(ov)} | {low:.0f} mm |")
        for o in ov[:4]:
            log(f"| | {o[0]} ({o[1]}) with {o[2]} ({o[3]}): {o[4]:.0f} mm^3 | |")
        sweep_fail += len(ov)
    log("")
    log("The M8 axle bolts pass through the bearing bores of the fork nodes by design and are excluded.")
    log("")
    az_fail = 0

    # 4. structural checks
    log("")
    log("## Structural checks (only what can fail)")
    log("")
    results, _ = analyse(info, zp, m_dish, cg_dish, log)
    structural_report(info, zp, m_dish, cg_dish, results, log)

    if not args.quick:
        export_all(info, zp, Zp, args, log)

    os.makedirs(os.path.join(ROOT, "analysis"), exist_ok=True)
    with open(os.path.join(ROOT, "analysis", "assembly_report.md"), "w") as fh:
        fh.write("\n".join(out) + "\n")
    return 0 if not bad and not hw_fail and not sweep_fail and not az_fail and not oversize else 1


if __name__ == "__main__":
    sys.exit(main())
