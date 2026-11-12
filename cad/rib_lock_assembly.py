"""Generate an isolated Rev D experimental dish with quarter-turn rib locks.

The mount, hub pins, feed-anchor connections and trunnion-adjacent rib bolts
remain Rev C.2. Output is isolated from the standard fabrication package.
Run from the repository root: python cad/rib_lock_assembly.py
"""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re

import cadquery as cq
import numpy as np

import build as b
from rib_lock_prototype import LockDesign, joint_plan, ROOT, on_bed


def sites():
    result = []
    for row in joint_plan():
        angle = row["angle_deg"]
        result.append((angle, b.MID_HOLE_R, b.MID_HOLE_Z))
        if row["rim"].startswith("2"):
            result.extend((angle,b.RIM_HOLE_R,z) for z in b.RIM_HOLE_Z)
    return result


def placed(shape, site):
    a,r,z = site
    return b.rz(shape.translate((r,0,z)),a)


def modify_support(solid, design, site):
    """Restore old pockets locally, then cut the new window and detent pocket.

    Determine which half of the joint belongs to this support by volume overlap.
    Repair circles lie entirely within the original flange lobes.
    """
    changed = False
    for side in (-1,1):
        lo = -design.half if side < 0 else design.off
        repair = placed(b.cyl(9.5,design.flange,(0,lo,0),(0,1,0)),site)
        if not b.bb_overlap(solid.BoundingBox(),repair.BoundingBox()):
            continue
        if solid.intersect(repair).Volume() < 5:
            continue
        changed = True
        solid = solid.fuse(repair)
        if side < 0:
            solid = solid.fuse(placed(design.receiver_pad(),site))
            solid = solid.cut(placed(design.detent_pocket(),site))
    if changed:
        solid = solid.cut(placed(design.slot(),site)).clean()
    return solid, changed


def build_experimental_dish(design):
    if abs(design.wood-b.W)>1e-9:
        raise ValueError("Update cad/parameters.yaml for assembly thickness; coupon override is independent")
    selected = sites()
    old_bolt = b.bolt
    omitted = []
    def bolt(*args, **kwargs):
        m,length,seat,direction,group = args[:5]
        if m==4 and length==20 and group=="dish":
            for site in selected:
                a,r,z=site
                ar=math.radians(a)
                expected=np.array([r*math.cos(ar)-design.half*math.sin(ar),
                                   r*math.sin(ar)+design.half*math.cos(ar),z])
                if np.linalg.norm(np.asarray(seat)-expected)<1e-5:
                    omitted.append(site)
                    return
        return old_bolt(*args,**kwargs)
    b.PARTS.clear()
    b.bolt=bolt
    try:
        # Preserve Rev C.2 axle location for this dish-only fit study. Do not
        # silently rebalance or regenerate its base; mass/balance need rechecking.
        baseline_report=(ROOT/"analysis"/"assembly_report.md").read_text()
        match=re.search(r"parallel to Y, ([0-9.]+) mm above the dish vertex",baseline_report)
        if not match:
            raise ValueError("Cannot identify the baseline axle position; review the current assembly report")
        b.build_dish(float(match[1]))
    finally:
        b.bolt=old_bolt
    if len(omitted)!=len(selected) or len(set(omitted))!=len(selected):
        raise AssertionError(f"Expected {len(selected)} removed sets, got {len(omitted)}")
    print("Applying the 40 replacement joints to the dish supports...",flush=True)
    modified=[]
    for part in b.PARTS:
        if part["id"]=="RIB":
            changed=False
            for site in selected:
                cutter=placed(design.slot(),site)
                if b.bb_overlap(part["solid"].BoundingBox(),cutter.BoundingBox()):
                    if part["solid"].intersect(cutter).Volume()>1e-5:
                        part["solid"]=part["solid"].cut(cutter).clean()
                        changed=True
            if changed:
                part["id"]="D-"+part["name"].replace("existing rib ","RIB-")
        elif part["id"].startswith(("SPC-","RIM-")):
            changed=False
            for site in selected:
                part["solid"],done=modify_support(part["solid"],design,site)
                changed |= done
            if changed:
                angle=float(re.search(r"(\d+(?:\.\d+)?) deg",part["name"])[1])
                part["id"]=f"D-{part['id']}-{angle:03.0f}"
                part["print_rot"]=[((0,0,1),-angle)]+part["print_rot"]
                modified.append(part["id"])
    lock=design.lock()
    for site in selected:
        a,r,z=site
        b.add("D-LOCK-01",f"quarter-turn lock rib {a:g} deg r{r:g} z{z:g}",placed(lock,site),
              "petg","dish","print",print_rot=[((0,0,1),-a)])
    return selected,modified


def validate(selected, modified):
    errors=[]
    for p in b.PARTS:
        if not p["solid"].isValid() or len(p["solid"].Solids())!=1:
            errors.append(p["name"])
    structural=[p for p in b.PARTS if p["kind"] in ("print","existing","wood","purchase") and p["check"]]
    clashes=b.overlaps(structural,min_vol=0.05)
    metal=[dict(p,check=True) for p in b.PARTS if p["kind"]=="hardware"]
    metal_clashes=b.overlaps(metal,structural,min_vol=0.05)
    oversized=[]
    for p in b.PARTS:
        if p["kind"]=="print" and p["id"].startswith("D-"):
            if not b.fits_bed(b.print_oriented(p))[0]:
                oversized.append(p["id"])
    counts=Counter(p["id"] for p in b.PARTS if p["kind"]=="hardware")
    return {"status":"PROTOTYPE; no strength or full motion validation", "invalid_or_disconnected":errors,
            "dish_clashes":clashes,"remaining_hardware_clashes":metal_clashes,"oversized_parts":oversized,
            "removed_sets":len(selected),"removed_metal_pieces":3*len(selected),"modified_supports":modified,
            "dish_hardware_counts":dict(sorted(counts.items())),"printed_locks":40,
            "mesh_fit":"not physically verified", "full_telescope_sweep":"NOT RUN",
            "strength_fatigue_creep":"NOT VALIDATED"}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out",type=Path,default=ROOT/"experiments"/"rib_locks"/"dish")
    ap.add_argument("--export",action="store_true",help="also write experimental STEP and modified STLs")
    args=ap.parse_args()
    design=LockDesign()
    print("Building the original dish, omitting only selected M4 sets...",flush=True)
    selected,modified=build_experimental_dish(design)
    print("Checking connected solids, static clearances and bed fit...",flush=True)
    report=validate(selected,modified)
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"checks.json").write_text(json.dumps(report,indent=2)+"\n")
    failed=any(report[k] for k in ("invalid_or_disconnected","dish_clashes","remaining_hardware_clashes","oversized_parts"))
    if failed:
        print(json.dumps(report,indent=2),flush=True)
        raise SystemExit("Geometry checks failed; no fabrication exports written")
    if args.export:
        assembly=cq.Assembly(name="Rev_D_EXPERIMENTAL_dish_NOT_FOR_FABRICATION")
        for i,p in enumerate(b.PARTS):
            if p["id"]!="MESH-01":
                assembly.add(p["solid"],name=f"{p['id']}_{i}")
            if p["kind"]=="print" and p["id"].startswith("D-"):
                if p["id"]=="D-LOCK-01":
                    shape=on_bed(design.lock(),pin=True)
                else:
                    shape=b.print_oriented(p)
                path=args.out/(p["id"]+".stl")
                if not path.exists():
                    cq.exporters.export(shape,str(path),tolerance=0.1,angularTolerance=0.2)
        assembly.export(str(args.out/"experimental_dish.step"))
    print(json.dumps(report,indent=2),flush=True)


if __name__=="__main__":
    main()
