# Changelog

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
