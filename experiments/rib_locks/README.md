# Fewer-fastener rib joints — Rev D study

[Project overview](../../README.md) · [Existing assembly guide](../../docs/assembly_guide.md)

**Experimental CAD · November 12, 2026 · Not released for fabrication**

This study replaces selected M4 bolt/nut/washer sets with a single printed quarter-turn lock. It preserves metal fasteners at the hub, feed-anchor ribs, trunnion-adjacent ribs, legs, axle and elevation lock. The original Rev C.2 fabrication files remain the baseline; do not mix these parts into that package without following the experimental drawings and completing the tests below.

## How it works

![Exploded CAD view of the fit coupon](coupon/exploded.svg)

1. Align the T-head with the vertical opening in the two flanges and plywood.
2. Insert the lock through all three layers.
3. Turn it 90 degrees. The rigid T-head now overlaps the far flange and blocks withdrawal.
4. A small spring bead seats in a pocket on the near flange to indicate the locked position and resist unintended rotation.

The 8 mm barrel transfers shear; the T-head and handle resist separation. The flexible arm is only an angular detent. This is a **tool-free printed fastener**, not an entirely fastener-free joint, and its load capacity has not been measured. It is intended to reduce bought hardware and assembly steps while keeping the lock replaceable.

![Assembled fit coupon](coupon/assembled.svg)

## Where the locks go

| Connection | Proposed treatment | Reason |
|---|---|---|
| All 18 middle spacer/rib connections | One printed lock each | Candidate locations for reducing repeated hardware; still need stiffness/load tests |
| Both rim connections on 11 ordinary ribs | Two printed locks per rib | Avoid replacing the direct feed and axle load-transfer connections |
| Rim connections at 60°, 180°, 300° | Keep M4 sets | Feed-anchor ribs |
| Rim connections at 80°, 100°, 260°, 280° | Keep M4 sets | Boundaries of the two trunnion bays at 90° and 270° |
| All 18 hub connections | Keep M4 pins/nuts | Thin wood at the centre leaves little room for a larger printed connection |
| Legs, feed supports, axle and elevation lock | Keep existing hardware | Concentrated loads and adjustment/clamping requirements |

The eligible rim ribs are **0°, 20°, 40°, 120°, 140°, 160°, 200°, 220°, 240°, 320° and 340°**. The selection is generated from the baseline parameters, with a guard against unsupported rib/anchor layouts.

## Hardware reduction

| Count | Rev C.2 | Candidate Rev D |
|---|---:|---:|
| Bolted rib connections | 72 | 32 |
| Printed rib locks | 0 | 40 |
| Metal bolts, nuts and washers across the telescope | 423 | 303 |
| Metal hardware plus the new printed locks | 423 | 343 |

Replacing 40 sets removes **120 metal pieces**, a **28.4% reduction in purchased hardware count**. Including the 40 new printed locks, the reduction is **80 fastening pieces, or 18.9%**. Bearings, mesh ties and the existing printed structure are outside this comparison. This is a count comparison, not proof that all 40 locations can safely use the prototype.

At the allowances in the [priced BOM](../../bom/README.md), the M4 buying quantities would change as follows:

| Item | Existing model / buy | Candidate model / buy | Allowance saving |
|---|---:|---:|---:|
| M4 × 20 | 84 / 93 | 44 / 49 | CAD $15.40 |
| M4 nuts | 96 / 106 | 56 / 62 | CAD $6.60 |
| M4 washers | 86 / 95 | 46 / 51 | CAD $3.52 |
| **Projected bought-hardware saving** | | | **CAD $25.52** |

Savings exclude the extra printed material, support waste and any reprints. The released shopping list has not been reduced because the new joints are not approved for use yet.

## Print a coupon first

Download these three prototype STLs:

- [Near flange with detent pocket](coupon/near_flange.stl)
- [Far flange](coupon/far_flange.stl)
- [Quarter-turn lock](coupon/quarter_turn_lock.stl)

The [coupon STEP](coupon/coupon.step) contains all four bodies, including a plywood reference body. Use an offcut of your **actual plywood**, not a printed substitute, for the physical rib layer. The wood opening is the union of an 8.5 mm circle and a centred 6.5 × 16.5 mm rectangle. These are **default prototype dimensions**, not instructions to modify the existing ribs now.

Use the intended final filament and printer. Start with PETG, a 0.4 mm nozzle, 0.2 mm layers, at least six perimeters and solid infill for the lock. Slice and inspect the narrow arm and the supporting material under the head before printing. The lock's shaft lies along the bed so the principal axial load is not carried exclusively across layer interfaces; local supports are still required. Do not let automatic orientation stand the shaft upright just to reduce support.

The coupon uses 3.175 mm wood, 0.2 mm clearance on each wood face, 0.5 mm diametral clearance at the shaft and 0.6 mm total axial play. **It does not reproduce the preload of a tightened bolt.** If the joint moves enough to distort the reflector, reject it or revise the fit; do not accept a loose connection simply because the detent clicks.

## Generate or adjust the CAD

Install the repository's normal Python requirements, then run from the repository root:

```bash
# Fit coupon and isolated connection checks
python cad/rib_lock_prototype.py

# Example coupon using measured plywood and a tighter trial fit
python cad/rib_lock_prototype.py --rib-thickness 3.1 --clearance 0.3 --out /tmp/rib-lock-trial

# Build the experimental dish and run static geometry checks
python cad/rib_lock_assembly.py

# Also generate the experimental STEP assembly and modified support STLs
python cad/rib_lock_assembly.py --export

# Exercise nine thickness/clearance combinations and check joint selection
python -m unittest discover -s cad -p 'test_rib_locks.py'
```

All experiment outputs go under this folder by default. The assembly script uses the baseline dimensions in `cad/parameters.yaml` and the saved baseline axle height in `analysis/assembly_report.md`. It retains that axle position for comparison; it does not claim the modified dish is rebalanced. Changed rim/spacer supports receive `D-` IDs so they are distinguishable from the original parts. The complete telescope motion sweep and revised structural analysis are not part of this experiment.

## What the checks mean

**Checks completed on November 12, 2026:** [five automated tests passed](test_results.json), including nine coupon fit combinations and the actual middle/rim support pairs. The [experimental dish report](dish/checks.json) found no invalid/disconnected solids, no static part or retained-hardware clashes above its 0.05 mm³ reporting threshold, and no modified printed parts outside the specified bed envelope. It confirms 40 omitted M4 sets and 40 printed locks. These are geometry results, not strength results.

The [coupon report](coupon/checks.json) records solid validity, sampled insertion clearance, sampled rigid-body rotation clearance and geometric obstruction to pulling out a locked T-head. The detent is excluded from the rigid rotation check because it must flex during engagement. An approximate beam-strain screen is a design calculation, not a PETG material qualification.

The experimental dish report records connected-solid validity, static part/hardware clashes, print-envelope fit and the count of omitted M4 sets. Static clearance does not establish assembly access, full elevation clearance, strength, fatigue life or outdoor durability. Review the generated report before using any generated export.

## Physical tests before adoption

1. **Fit:** record the measured plywood thickness, printer settings and clearance variant. Confirm insertion and removal without hammering, cracking or tearing the wood.
2. **Retention:** check that the T-head overlaps both sides of the far opening, the detent seats, and the locked orientation cannot slide out. Record the torque required to rotate it unintentionally.
3. **Backlash:** measure relative movement across the joint under reversing loads and compare it with the original bolted joint. Check reflector alignment, not just whether the parts stay attached.
4. **Load and failure mode:** test sacrificial samples in shear and separation. Record load versus displacement and whether the lock, flange or plywood fails first. Required loads and safety factors must come from a revised joint/load analysis; the coupon geometry alone supplies no working-load rating.
5. **Creep and cycling:** repeat measurements after sustained loading, repeated lock/unlock cycles and exposure to the intended temperature/moisture conditions. Record duration and conditions; a short test is not a lifetime rating.
6. **Assembly and motion:** prove installation access on adjacent real bays, then check the full dish sweep, stiffness, balance and interference before expanding to all 40 positions.

Do not enlarge all 18 ribs or print the entire modified support set before the coupon and one real connection have passed. If the lock cannot meet stiffness and retention requirements, keep the M4 joint at that location.

## Why not simple snap tabs or friction alone?

Snap tabs are useful for assembly retention, but a thin tab held bent by a structural load can creep and lose holding force. The proposed load path therefore uses solid bearing surfaces with a separate locating detent. Friction-only wedges would depend on plywood thickness, humidity and maintained contact pressure. Fully bonded sockets could remove more loose pieces, but would make replacement difficult and need adhesive/wood-surface qualification.

Design references reviewed:

- [Protolabs Network: designing snap-fit joints](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/) — creep, fatigue, root geometry, orientation and separating alignment/shear features from flexible tabs.
- [Formlabs: designing snap-fit enclosures](https://formlabs.com/blog/designing-3d-printed-snap-fit-enclosures/) — prototyping, tolerances and material-dependent behaviour.

These sources inform the design approach. Neither validates this telescope joint, its printed material or its load capacity.
