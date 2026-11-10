# Changelog

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
