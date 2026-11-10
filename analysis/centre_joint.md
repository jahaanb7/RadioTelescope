# Centre-joint feasibility (brief section 4 gate)

Revision A, 2026-11-09. Modelled and analytically checked only. Nothing physically tested.
Numbers come from `cad/build_ribs.py`; raw output is in `rib_build_report.txt`.
All values assume a 5 mm board (Rev A). Rev C: the ribs are 1/8 in (3.175 mm), so the ribs meet even closer to the centre and the 60 mm tip relief has more margin; the hub in `cad/build.py` uses the real thickness.

## Finding

Eighteen untrimmed ribs cannot coexist at the vertex.

- 72 of the 153 rib pairs intersect as solids.
- The overlap reaches 14.62 mm from the axis.
- The wood involved is at most 0.12 mm tall, 17 mm³ in total. The collision is geometrically real but involves almost no material.

The tips are the real problem, not the overlap volume:

| Radius from axis | Rib height | Clear gap to next rib |
|---:|---:|---:|
| 15 mm | 0.14 mm | 0.2 mm |
| 30 mm | 0.56 mm | 5.4 mm |
| 50 mm | 1.56 mm | 12.4 mm |
| 60 mm | 2.25 mm | 15.8 mm |
| 80 mm | 3.99 mm | 22.8 mm |
| 100 mm | 6.24 mm | 29.7 mm |
| 150 mm | 14.04 mm | 47.1 mm |

No fastener can go into the rib inside roughly r = 100 mm. No option keeps all 18 tips intact to the axis.

## Options

**A. Flat rear plate with tip relief (provisional baseline).**
Ribs stand on their flat bottom edges on a rear hub disc and a rim ring. Each tip is cut square at r = 60 mm.
- Removes 228 mm³ per rib, 0.175 % of the rib, at a cut height of 2.25 mm.
- Zero rib-to-rib overlaps after the cut (checked on all 153 pairs).
- The parabola is untouched from r = 60 mm outward. No rib moves radially.
- The central 120 mm circle needs its own mesh support. It sits in the feed's shadow, and is 1.4 % of the aperture area.
- Rib retention would be side saddles or slotted blocks on the rear plate from about r = 100 mm outward, where the rib is tall enough to clamp.

**B. Slotted central hub with deeper relief.**
A printed or wooden hub with 18 radial slots grips the rib ends. A 5 mm slot wall needs gap ≥ 10 mm and enough height to grip, which pushes the cut to about r = 100–120 mm (6–9 mm tall).
- More positive indexing of the 20° spacing.
- Removes more of each rib and relies on a small part for alignment.

**C. Leave tips uncut and let them overlap.** Not feasible. The solids intersect.

## Provisional choice

Option A, because it alters the existing wood least and uses the flat bottom edge that the ribs already have as the assembly datum.

This needs the owner's decision before any rib is cut. `RIB_solid_wedge_tip_relief_PROVISIONAL.step` shows the cut. `RIB_solid_wedge_as_cut.step` is the untouched rib.

## Not yet checked

Fastener edge distances, saddle design, tool access, load path into the mount, and the choice between 60 mm and a larger relief once the real board thickness is known.
