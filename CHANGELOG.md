# Changelog

## Rev C.1, 2026-11-10

- Rib supports now come in two types. Normal: `RIM-01` rim bay (10) and `SPC-01` spacer (18) have no screw holes or
  nut pockets and are glued to the ribs. Feed: `FLA-01` anchor (3) and the new `RIM-02` rim bay (6, beside ribs 60,
  180 and 300 deg) keep the M4 holes and nut pockets that hold the feed tripod.
- The ribs are no longer drilled. Removed: 54 rib bolts, the mesh-screw holes in the rim chords and spacers, drill jigs
  `JIG-01`/`JIG-02`, and the drilling template (now `drawings/RIB_cut_template_1to1.dxf`).
- 2 mm fillets on every rib support (`rib_support.fillet_radius`), applied edge by edge; bed faces stay sharp.
- Fasteners 494 to 332. PETG 7.2 to 6.6 kg, print time 235 to 210 h. Dish 6.2 to 5.5 kg; axle height 724 mm.
- Not tested: the epoxy joint between plywood and PETG. `RIM-T` and the hub keeper keep their bolts.

## Rev C, 2026-11-10

- Redesign for minimum wood: only the 18 existing ribs and straight softwood battens; everything else printed in PETG
  for a Prusa CORE One L. Replaces the Rev B plywood discs, ring, spars and rocker board.
- New generator `cad/build.py` (replaces `cad/build_assembly.py`). Three kinematic stages: fixed stand, turning base
  (azimuth about Z on a 6 in lazy-susan bearing and M10 kingpin), dish (elevation about Y on 608 bearings, -5 to 90 deg).
- Every joint modelled with its bolts, nuts, washers, nut pockets and batten sockets; printed tolerances from
  `tolerances` in `cad/parameters.yaml`.
- Checks in `analysis/assembly_report.md`: solid validity, single-solid parts, bed fit, interference within each stage,
  every fastener against its parts, elevation sweep every 5 deg, azimuth sweep every 15 deg, 3D beam frame for the
  battens, joint bearing and shear, PETG creep limits, kingpin, bearings, lock clamp, tipping and ballast in wind.
- Exports: nested STEP assembly, three stage STEPs for Fusion 360, one STEP per part, print-oriented STLs with a print
  list, BOM, hardware list, batten cut list, rib modifications, rib drilling DXF template and PNG views.
- Fusion 360 script `cad/fusion/telescope_joints` imports the stages and adds the azimuth and elevation joints.
- Shop aids: FIT-01 fit coupon, JIG-01 and JIG-02 rib drill jigs.
- Rib audit outputs moved to `exports/rib_audit/` and `drawings/rib_audit/`. Rev B outputs removed.
- Nothing released for fabrication.

## Rev B, 2026-11-09

- Added `cad/build_assembly.py`: 186-solid provisional assembly with fork mount, feed support and base.
- Hub disc radius changed from 110 to 200 mm so the inner rib clamps sit where the rib is 18 mm tall.
- Interference checks: zero within dish group, zero within mount, zero over the elevation sweep from -5 to 90 degrees.
- Added mass and balance, mesh faceting, feed-can formula values and wind screening to `analysis/assembly_report.md`.
- Added part STEP files, printed-part STL, fit coupon, DXF outlines, SVG views and a provisional BOM.
- Nothing released for fabrication.

## Rev A, 2026-11-09

- Audited supplied files. Rib geometry taken from `inputs/Wood_Rib_Frame.stl`; `inputs/RadioTelescope.step` found empty.
- Confirmed the rib top edge is the parabola with f = 400.641 mm (CAD only).
- Built parametric rib generator, 18-rib array and pairwise interference check.
- Centre-joint study: provisional Option A, 60 mm tip relief, awaiting owner decision.
- Exported provisional reflector skeleton to STEP and STL, and the rib profile to DXF.
- Nothing released for fabrication.
