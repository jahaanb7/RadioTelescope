# Printing guide

Every printed part is PETG on a Prusa CORE One L (300 × 300 × 330 mm bed). The STLs in `print/` are already laid flat in the recommended bed orientation; import them without rotating them.

**Total: about 6.6 kg of PETG and 210 hours of printing** (66 parts, 26 part types). The times come from a simple model, `cad/print_prep.py`, and are accurate to about ±30 %. Slice in PrusaSlicer for real figures.

## Common settings

| Setting | Value |
|---|---|
| Printer profile | Prusa CORE One L, 0.4 mm nozzle (HF nozzle is fine) |
| Filament profile | Prusament PETG or generic PETG, 240–250 °C nozzle, 80–85 °C bed |
| Layer height | 0.20 mm (0.15 mm for `FIT-01` if you want to check finer tolerances) |
| Infill pattern | Gyroid |
| Perimeters, infill, top/bottom layers | Per part, in the table below |
| Supports | Build plate only, and only where the table says. Organic supports remove most easily |
| Seam | Aligned or rear |
| Cooling | PETG default (30–50 %); more fan on small parts like the knobs |
| Bed | Textured PEI sheet, or smooth PEI with glue stick as a release agent (PETG can bond too hard to bare smooth PEI) |
| Dry filament | Dry PETG at 65 °C for 4 h if it has been open for weeks. Wet PETG strings and makes weak layers |

**Print `FIT-01` first** and set the tolerances in `cad/parameters.yaml` from it. See [assembly_guide.md](assembly_guide.md), step 0.

## Per part

| Part | Qty | Size on bed (mm) | Perimeters | Infill | Top/bottom | Supports | Brim | g each | h each | h total | Notes |
|---|---:|---|---:|---|---:|---|---|---:|---:|---:|---|
| [`FIT-01`](../images/parts/FIT-01.png) | 1 | 236 x 128 x 16 | 4 | 25% gyroid | 5 | none | no | 183 | 5.7 | 5.7 | PRINT THIS FIRST with exactly the settings and filament you will use for the real parts. |
| [`AZB-01`](../images/parts/AZB-01.png) | 1 | 220 x 227 x 79 | 5 | 30% gyroid | 5 | yes, build plate only (286 cm2 of overhang) | no | 542 | 16.8 | 16.8 | Supports only under the 1.5 mm lazy-susan recess. Check the M10 kingpin head drops into its hex pocket. |
| [`AZT-01`](../images/parts/AZT-01.png) | 1 | 220 x 222 x 79 | 5 | 30% gyroid | 5 | yes, build plate only (303 cm2 of overhang) | no | 627 | 19.5 | 19.5 | Supports only under the 1.5 mm lazy-susan recess (use a support enforcer there); the plate must sit flat on the bearing, so clean the recess floor. |
| [`EBOX-01`](../images/parts/EBOX-01.png) | 1 | 150 x 110 x 60 | 4 | 25% gyroid | 5 | none | no | 155 | 5.1 | 5.1 |  |
| [`EBOX-02`](../images/parts/EBOX-02.png) | 1 | 150 x 110 x 6 | 4 | 25% gyroid | 5 | none | no | 89 | 2.7 | 2.7 |  |
| [`ELS-01`](../images/parts/ELS-01.png) | 1 | 130 x 113 x 6 | 5 | 40% gyroid | 6 | none | no | 66 | 2.1 | 2.1 | Lock sector: clamped by the knob; 100 % infill is fine if you have time. |
| [`FKC-01`](../images/parts/FKC-01.png) | 2 | 124 x 140 x 140 | 5 | 30% gyroid | 5 | yes, build plate only (61 cm2 of overhang) | no | 251 | 8.1 | 16.3 | Socket walls carry the fork; do not reduce perimeters. |
| [`FKC-02`](../images/parts/FKC-02.png) | 2 | 124 x 140 x 140 | 5 | 30% gyroid | 5 | yes, build plate only (61 cm2 of overhang) | no | 251 | 8.1 | 16.3 | Socket walls carry the fork; do not reduce perimeters. |
| [`FKT-01`](../images/parts/FKT-01.png) | 1 | 101 x 120 x 47 | 6 | 40% gyroid | 6 | yes, build plate only (34 cm2 of overhang) | no | 185 | 6.0 | 6.0 | Bearing bores must print vertical (kept). Press the 608s in with a vice, not a hammer. |
| [`FKT-02`](../images/parts/FKT-02.png) | 1 | 100 x 120 x 45 | 6 | 40% gyroid | 6 | yes, build plate only (34 cm2 of overhang) | no | 133 | 4.3 | 4.3 | Bearing bores must print vertical (kept). Slip fit: the bearing should slide in by hand. |
| [`FLA-01`](../images/parts/FLA-01.png) | 3 | 166 x 210 x 55 | 4 | 25% gyroid | 5 | yes, build plate only (96 cm2 of overhang) | 5 mm | 96 | 3.1 | 9.2 | Tall: brim 5 mm, slow the top 30 mm if it wobbles. |
| [`FOOT-01`](../images/parts/FOOT-01.png) | 3 | 141 x 34 x 71 | 5 | 30% gyroid | 5 | yes, build plate only (24 cm2 of overhang) | no | 130 | 4.3 | 12.9 | M10 nut pocket: pause at the layer above the pocket and drop the nut in, or press it in later. |
| [`FRG-01`](../images/parts/FRG-01.png) | 1 | 260 x 220 x 58 | 4 | 25% gyroid | 5 | yes, build plate only (79 cm2 of overhang) | no | 206 | 6.5 | 6.5 |  |
| [`HUB-01`](../images/parts/HUB-01.png) | 1 | 280 x 280 x 15 | 5 | 30% gyroid | 5 | none | 5 mm | 233 | 7.3 | 7.3 | Large flat part: brim 5 mm, clean bed, 0.2 mm first layer. |
| [`HUB-02`](../images/parts/HUB-02.png) | 1 | 280 x 280 x 6 | 4 | 25% gyroid | 5 | yes, build plate only (5 cm2 of overhang) | 5 mm | 88 | 2.8 | 2.8 | Flat top on the bed, curved mesh face up; brim 5 mm. |
| [`KNB-01`](../images/parts/KNB-01.png) | 1 | 39 x 39 x 16 | 4 | 25% gyroid | 5 | none | 5 mm | 14 | 0.5 | 0.5 | Press an M6 nut into the hex pocket (heat it with a soldering iron if tight). |
| [`KNB-02`](../images/parts/KNB-02.png) | 1 | 53 x 53 x 16 | 4 | 25% gyroid | 5 | none | no | 24 | 0.7 | 0.7 | Press the M10 nyloc nut into the hex pocket. |
| [`LNA-01`](../images/parts/LNA-01.png) | 1 | 90 x 50 x 35 | 4 | 25% gyroid | 5 | none | no | 39 | 1.4 | 1.4 |  |
| [`LNA-02`](../images/parts/LNA-02.png) | 1 | 50 x 90 x 5 | 4 | 25% gyroid | 5 | none | no | 24 | 0.8 | 0.8 |  |
| [`RIM-01`](../images/parts/RIM-01.png) | 10 | 153 x 170 x 14 | 4 | 25% gyroid | 5 | yes, build plate only (10 cm2 of overhang) | no | 79 | 2.5 | 24.5 | Normal rib support, no screw holes. Print 10. Glue into the rib slots with epoxy. |
| [`RIM-02`](../images/parts/RIM-02.png) | 6 | 153 x 170 x 14 | 4 | 25% gyroid | 5 | yes, build plate only (12 cm2 of overhang) | no | 82 | 2.5 | 15.3 | Feed rim bay: pads are drilled for the feed anchor screws. Print 6. |
| [`RIM-T`](../images/parts/RIM-T.png) | 2 | 170 x 34 x 200 | 5 | 30% gyroid | 5 | yes, build plate only (26 cm2 of overhang) | 5 mm | 263 | 7.7 | 15.5 | Carries the elevation axle; do not reduce perimeters. |
| [`SPC-01`](../images/parts/SPC-01.png) | 18 | 45 x 105 x 51 | 4 | 25% gyroid | 5 | none | 5 mm | 25 | 1.0 | 17.2 | Normal mid-span support, no screw holes. Print 18. Glue into the rib slots. |
| [`SPR-01`](../images/parts/SPR-01.png) | 2 | 12 x 12 x 2 | 4 | 100% gyroid | 5 | none | 5 mm | 0 | 0.0 | 0.0 | Tiny ring, print solid. An M8 washer (1.6 mm) plus a 0.5 mm shim is an alternative. |
| [`SPR-02`](../images/parts/SPR-02.png) | 2 | 12 x 12 x 31 | 4 | 100% gyroid | 5 | none | 5 mm | 2 | 0.2 | 0.4 | Print solid; it bears on the inner races. |
| [`SPR-03`](../images/parts/SPR-03.png) | 1 | 30 x 30 x 6 | 4 | 100% gyroid | 5 | none | 5 mm | 5 | 0.2 | 0.2 | Print solid. |

## Suggested print order

1. `FIT-01`, then adjust the tolerances and rebuild.
2. Cut the rib tip reliefs while the rest prints (no drilling).
3. Dish, normal rib supports (no screw holes): `HUB-01`, `HUB-02`, 10 × `RIM-01`, 18 × `SPC-01` (six per plate); then 2 × `RIM-T`, `ELS-01`, `SPR-01/02/03`.
4. Mount: `AZB-01`, `AZT-01`, 4 corner nodes, 2 fork top nodes, 3 feet, the knobs.
5. Feed supports (these keep their screw holes and nut pockets): 6 × `RIM-02`, 3 × `FLA-01`; then `FRG-01`, the LNA box, and finally the electronics box.

## Why the settings differ

- Parts that carry the dish or hold a bearing (`FKT`, `FKC`, `RIM-T`, `AZT`, `AZB`, `FOOT`, `ELS`) get more perimeters. In PETG, the walls carry the load, not the infill.
- The small spacers print solid, because they are clamped by the axle nut.
- The weakest direction of a print is across its layers (about 18 MPa for PETG). Bearing bores print vertically so the bearing load stays in the layer plane.

