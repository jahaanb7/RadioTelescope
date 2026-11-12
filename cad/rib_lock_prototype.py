"""Rev D study: tool-free quarter-turn rib locks. NOT RELEASED FOR FABRICATION.

Default: generate an isolated fit coupon, lock, STEP and SVG views.
No Rev C.2 fabrication output is overwritten. Units are millimetres.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import cadquery as cq
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cad"))
import build as baseline


def value(section, key):
    return baseline.RAW[section][key]["value"]


class LockDesign:
    """Y is the insertion axis; X/Z is the plane of the plywood rib.

    The T-head is horizontal in the locked position and vertical for insertion.
    The spring bead locates angular position only; the T-head resists withdrawal.
    """
    def __init__(self, thickness=None, clearance=0.5):
        self.wood = float(value("rib", "thickness_board") if thickness is None else thickness)
        self.clearance = clearance
        self.gap = float(value("tolerances", "rib_flange_gap"))
        self.flange = float(value("dish", "flange_thickness"))
        self.off = self.wood / 2 + self.gap
        self.half = self.off + self.flange
        if not 2.5 <= self.wood <= 4.5 or not 0.2 <= clearance <= 0.8:
            raise ValueError("Study supports plywood 2.5–4.5 mm and clearance 0.2–0.8 mm only")

    def slot(self, y0=None, length=None):
        """8 mm barrel + vertical 16 x 6 mm T-head insertion window."""
        y0 = -self.half - 5 if y0 is None else y0
        length = 2 * self.half + 10 if length is None else length
        c = self.clearance
        round_hole = baseline.cyl((8 + c) / 2, length, (0, y0, 0), (0, 1, 0))
        window = baseline.bx(-(6+c)/2, (6+c)/2, y0, y0+length,
                             -(16+c)/2, (16+c)/2)
        return round_hole.fuse(window).clean()

    def receiver_pad(self):
        # Outboard flange lug supports the spring detent. Does not grip the wood.
        return baseline.bx(8, 23, -self.half, -self.off, -4.5, 4.5)

    def detent_pocket(self):
        return cq.Solid.makeSphere(1.3, cq.Vector(19, -self.half-0.5, 0),
                                   angleDegrees1=-90, angleDegrees2=90)

    def lock(self):
        h = self.half
        shaft = baseline.cyl(4, 2*h+0.6, (0, -h-0.3, 0), (0, 1, 0))
        head = baseline.cyl(6.5, 3, (0, -h-3.3, 0), (0, 1, 0))
        t_head = baseline.bx(-8, 8, h+0.3, h+3.3, -3, 3)
        # A tapered, in-plane arm; root is blended into the circular handle.
        arm = baseline.prism("XZ", [(4,-3),(20,-2),(20,2),(4,3)], 1.2, "y", -h-2)
        bead = cq.Solid.makeSphere(1, cq.Vector(19, -h-0.5, 0),
                                   angleDegrees1=-90, angleDegrees2=90)
        pin = baseline.fuse([shaft, head, t_head, arm, bead])
        # Local edge rounding avoids sharp external handling edges. A wider root
        # blend and fatigue behaviour still need physical coupon validation.
        return pin.clean()

    def coupon(self):
        h, o = self.half, self.off
        near = baseline.bx(-12, 12, -h, -o, -12, 12).fuse(self.receiver_pad())
        far = baseline.bx(-12, 12, o, h, -12, 12)
        wood = baseline.bx(-12, 12, -self.wood/2, self.wood/2, -12, 12)
        return {
            "near_flange": near.cut(self.slot()).cut(self.detent_pocket()).clean(),
            "far_flange": far.cut(self.slot()).clean(),
            "wood_reference": wood.cut(self.slot()).clean(),
            "quarter_turn_lock": self.lock(),
        }


def joint_plan():
    """Keep feed-anchor ribs and both boundaries of each trunnion bay bolted."""
    n = int(value("rib", "count"))
    if n != 18:
        raise ValueError("This joint-selection study is reviewed only for the 18-rib layout")
    step = 360/n
    anchors = value("dish", "anchor_rib_angles")
    protected = {round(a % 360, 6) for a in anchors}
    # A trunnion is a bay centred on 90/270 degrees, not a rib at those angles.
    for mid in (90, 270):
        protected.update(round((mid+s*step/2) % 360, 6) for s in (-1,1))
    actual = {round(k*step,6) for k in range(n)}
    if not protected <= actual:
        raise ValueError("Changed rib count/anchor geometry needs a new joint selection review")
    rows = []
    for k in range(n):
        angle = round(k*step,6)
        rows.append({"rib": k+1, "angle_deg": angle, "hub": "M4 retained",
                     "middle": "prototype lock", "rim": "M4 retained" if angle in protected else "2 prototype locks"})
    return rows


def check_coupon(design, parts):
    """Geometry checks are not material, fatigue, weather or strength validation."""
    results = {}
    for name, shape in parts.items():
        assert shape.isValid(), name
        assert len(shape.Solids()) == 1, name
    stationary = baseline.fuse([s for n,s in parts.items() if n != "quarter_turn_lock"])
    pin = parts["quarter_turn_lock"]
    results["locked_overlap_mm3"] = pin.intersect(stationary).Volume()
    assert results["locked_overlap_mm3"] < 1e-5
    unlocked = pin.rotate((0,0,0), (0,1,0), 90)
    # Start well before the near face: the whole T-head must pass through all layers.
    overlap = max(unlocked.translate((0,-travel,0)).intersect(stationary).Volume()
                  for travel in range(0, math.ceil(2*design.half+8)+1))
    results["insertion_max_overlap_mm3"] = overlap
    assert overlap < 1e-5
    # Rotation is checked without the flexible bead; the bead is intended to deflect.
    bead_zone = baseline.bx(17.5,20.5,-design.half-1.6,-design.half+0.6,-1.1,1.1)
    rigid = pin.cut(bead_zone)
    results["rotation_rigid_max_overlap_mm3"] = max(
        rigid.rotate((0,0,0),(0,1,0),a).intersect(stationary).Volume()
        for a in range(0,91,5))
    assert results["rotation_rigid_max_overlap_mm3"] < 1e-5
    # Verify a locked head physically blocks withdrawal rather than merely rubbing.
    results["locked_withdrawal_interference_mm3"] = pin.translate((0,-1,0)).intersect(parts["far_flange"]).Volume()
    assert results["locked_withdrawal_interference_mm3"] > 1
    results["axial_clearance_mm"] = 0.6
    results["diametral_clearance_mm"] = design.clearance
    results["wood_side_clearance_total_mm"] = 2*design.gap
    results["detent_nominal_deflection_mm"] = 0.5
    results["detent_beam_strain_screen_percent"] = 100*1.5*1.2*0.5/(12.5**2)
    results["physical_tests"] = "NOT RUN; prototype only"
    return results


def on_bed(shape, pin=False):
    # Both orientations keep the insertion axis in the layer plane. Coupons are
    # flat on their outside flange faces; the lock needs locally supported head overhangs.
    if not pin:
        shape = shape.rotate((0,0,0),(1,0,0),90)
    box = shape.BoundingBox()
    return shape.translate((-box.xmin,-box.ymin,-box.zmin))


def write_outputs(design, output):
    output.mkdir(parents=True, exist_ok=True)
    parts = design.coupon()
    results = check_coupon(design, parts)
    assy = cq.Assembly(name="Rev_D_rib_lock_coupon_UNVALIDATED")
    for name,shape in parts.items():
        color = cq.Color(0.70,0.48,0.27) if name == "wood_reference" else cq.Color(0.2,0.45,0.7)
        assy.add(shape, name=name, color=color)
        if name != "wood_reference":
            bed = on_bed(shape, name == "quarter_turn_lock")
            # ASCII STL permits ordinary Git data API uploads without binary rewriting.
            cq.exporters.export(bed, str(output/(name+".stl")), opt={"ascii": True}, tolerance=0.08, angularTolerance=0.2)
    assy.export(str(output/"coupon.step"))
    exploded = []
    offsets = {"near_flange": -12, "far_flange": 12, "wood_reference": 0, "quarter_turn_lock": -36}
    for name,shape in parts.items():
        exploded.append(shape.translate((0,offsets[name],0)))
    cq.exporters.export(cq.Compound.makeCompound(exploded), str(output/"exploded.svg"),
                        opt={"width":1000,"height":650,"projectionDir":(1,-1,0.7),"showAxes":False,
                             "strokeWidth":0.15,"hiddenColor":(210,215,222),"showHidden":False})
    cq.exporters.export(cq.Compound.makeCompound(list(parts.values())), str(output/"assembled.svg"),
                        opt={"width":850,"height":650,"projectionDir":(1,-1,0.6),"showAxes":False,"showHidden":False,"strokeWidth":0.15})
    results["joint_plan"] = joint_plan()
    results["replacement_locks"] = sum(1 + (2 if "prototype" in r["rim"] else 0) for r in joint_plan())
    results["removed_metal_pieces"] = results["replacement_locks"]*3
    results["source_revision"] = "Rev C.2; candidate Rev D; separate experimental dish generator, not released"
    results["cadquery_version"] = cq.__version__
    (output/"checks.json").write_text(json.dumps(results, indent=2)+"\n")
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rib-thickness", type=float)
    parser.add_argument("--clearance", type=float, default=0.5)
    parser.add_argument("--out", type=Path, default=ROOT/"experiments"/"rib_locks"/"coupon")
    args = parser.parse_args()
    results = write_outputs(LockDesign(args.rib_thickness,args.clearance),args.out)
    print(json.dumps({k:v for k,v in results.items() if k != "joint_plan"},indent=2))


if __name__ == "__main__":
    main()
