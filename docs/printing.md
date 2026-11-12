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

## Rev C.2 parts

The uploaded print list is the source for this table. The ZIP did not include print_specs.csv; previous per-part support and time estimates were stale. Inspect supports and estimate time in your slicer before printing.

| Part | Quantity | Footprint | Settings |
|---|---:|---|---|
| HUB-01 | 1 | 280 x 280 x 15 | 5 perimeters, 30% gyroid |
| RIM-01 | 10 | 153 x 167 x 64 | 4 perimeters, 25% gyroid |
| RIM-02 | 6 | 153 x 132 x 148 | 4 perimeters, 25% gyroid |
| RIM-T | 2 | 200 x 56 x 170 | 5 perimeters, 30% gyroid; axle pocket faces up |
| SPC-01 | 18 | 53 x 103 x 40 | 4 perimeters, 25% gyroid |
| FLA-01 | 3 | 154 x 97 x 208 | 4 perimeters, 25% gyroid |
| FRG-01 | 1 | 235 x 260 x 58 | 4 perimeters, 25% gyroid |
| LNA-01 | 1 | 103 x 88 x 35 | 4 perimeters, 25% gyroid |
| LNA-02 | 1 | 103 x 88 x 5 | 4 perimeters, 25% gyroid |
| ELS-01 | 1 | 114 x 141 x 6 | 5 perimeters, 40% gyroid |
| SPR-03 | 1 | 30 x 30 x 6 | 4 perimeters, 25% gyroid |
| SPR-01 | 2 | 12 x 2 x 12 | 4 perimeters, 25% gyroid |
| SPR-02 | 2 | 12 x 31 x 12 | 4 perimeters, 25% gyroid |
| FKT-01 | 1 | 133 x 113 x 47 | 6 perimeters, 40% gyroid; bearing bores print vertical |
| FKT-02 | 1 | 122 x 113 x 45 | 6 perimeters, 40% gyroid |
| KNB-01 | 1 | 42 x 42 x 16 | 4 perimeters, 25% gyroid |
| FKC-01 | 2 | 137 x 147 x 137 | 5 perimeters, 30% gyroid |
| FKC-02 | 2 | 137 x 147 x 137 | 5 perimeters, 30% gyroid |
| EBOX-01 | 1 | 150 x 110 x 60 | 4 perimeters, 25% gyroid |
| EBOX-02 | 1 | 150 x 110 x 6 | 4 perimeters, 25% gyroid |
| FIT-01 | 1 | 236 x 128 x 16 | same settings as the real parts |
| JIG-01 | 1 | 51 x 115 x 16 | 4 perimeters, 25% gyroid |
| JIG-02 | 1 | 220 x 42 x 16 | 4 perimeters, 25% gyroid |
