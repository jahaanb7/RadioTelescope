# Bill of materials & cost estimate

[Project overview](../README.md) · [Shopping specifications](../docs/shopping_list.md) · [Assembly guide](../docs/assembly_guide.md)

**Revision C.2 · Canadian dollars (CAD) · Price research: November 11, 2026**

A purchase budget for one telescope, with materials, mechanical hardware and a provisional receiver setup. It includes purchased filament and spare fasteners rather than just the material installed in the model.

> **Budget, not a checkout quote.** “Listed” prices were visible in supplier listings during research. “Converted” prices use a stated planning exchange factor. “Allowance” prices are estimates, not verified supplier quotes. Taxes, shipping, import charges, tools, electricity and labour are excluded. Final RF selection and physical fit checks remain open.

## Total project budget

| Scope | CAD |
|---|---:|
| Materials, bearings and ballast | $390.65 |
| Fasteners, including the shopping quantities below | $119.92 |
| **Mechanical build subtotal** | **$510.57** |
| Provisional electronics and RF subtotal | $722.36 |
| **Complete reference build, before tax and shipping** | **$1,232.93** |
| Optional 15% planning contingency | $184.94 |
| **Planning budget including contingency** | **$1,417.87** |

The total assumes buying all listed materials, including plywood stock and computing hardware. Reusing the existing 18 ribs reduces the reference total by $60.00 to **$1,172.93**. If the ribs, Pi 5, microSD and SSD are already owned, the remaining listed purchases total **$748.43**; other items are still assumed to be purchased. Existing-item deductions are budget offsets, not resale values.

## Materials and bought mechanical parts

| Item | Buy quantity | Unit CAD | Extended CAD | Price basis | Scope / notes |
|---|---:|---:|---:|---|---|
| PETG, 1 kg spool | 7 | $19.95 | $139.65 | Listed · [S1](#price-sources) | 7 kg purchased; about 5.35 kg model estimate, with print waste/spares. |
| Plywood stock for 18 ribs | 1 | $60.00 | $60.00 | Allowance | Stock budget only; confirm sheet layout and actual 3.175 mm thickness. Existing ribs may be reused. |
| 1×2 softwood, 8 ft | 2 | $8.00 | $16.00 | Allowance · [S5](#price-sources) | Actual 19×38 mm; 4 legs and 2 sills. |
| 1×3 softwood, 8 ft | 1 | $12.00 | $12.00 | Allowance | Actual 19×64 mm; 2 base ties. |
| 19×19 mm softwood, 6 ft | 1 | $10.00 | $10.00 | Allowance | 3 feed legs. |
| Reflector mesh stock | 1 | $55.00 | $55.00 | Allowance | At least 1.2×1.2 m usable coverage; openings 6 mm or finer; joins need overlap. |
| Conductive feed can | 1 | $15.00 | $15.00 | Allowance | Provisional Ø150×280 mm; measure before printing collar. |
| Exterior wood sealer | 1 | $25.00 | $25.00 | Allowance | One small tin. |
| UV-resistant ties, 100-pack | 3 | $6.00 | $18.00 | Allowance | 2.5 mm width; 300 ties total. |
| 608-2RS bearings | 5 | $4.00 | $20.00 | Allowance | 4 installed + 1 spare. |
| Ballast containers and fill | 4 | $5.00 | $20.00 | Allowance | Provisional budget; determine ballast from site and physical stability checks. |

**Subtotal: $390.65 CAD.**

The filament line pays for all printed parts, enclosures, jigs and the fit coupon; do not add individual printed-part material costs again. Likewise, the batten stock covers the cut pieces in [cut_list.csv](cut_list.csv). Plywood is a stock allowance, not a validated nesting plan or CNC cutting quote. Retail mesh rolls may cost more than this allowance.

## Fasteners

Model and buy counts are copied from [hardware.csv](hardware.csv). Buy quantities include approximately 10% spare, rounded up. All prices below are **per-piece CAD allowances**; pack sizes, minimum orders and supplier specifications can change the amount paid.

| ID | Item | Model qty | Buy qty | Unit CAD | Extended CAD |
|---|---|---:|---:|---:|---:|
| `HW-M4-nut` | M4 nut | 96 | 106 | $0.15 | $15.90 |
| `HW-M4-washer` | M4 washer | 86 | 95 | $0.08 | $7.60 |
| `HW-M4x12` | M4 x 12 bolt | 2 | 3 | $0.30 | $0.90 |
| `HW-M4x20` | M4 x 20 bolt | 84 | 93 | $0.35 | $32.55 |
| `HW-M4x30` | M4 x 30 bolt | 2 | 3 | $0.45 | $1.35 |
| `HW-M4x35` | M4 x 35 bolt | 8 | 9 | $0.50 | $4.50 |
| `HW-M6-nut` | M6 nut | 35 | 39 | $0.25 | $9.75 |
| `HW-M6-washer` | M6 washer | 69 | 76 | $0.12 | $9.12 |
| `HW-M6x35` | M6 x 35 bolt | 2 | 3 | $0.60 | $1.80 |
| `HW-M6x40` | M6 x 40 bolt | 32 | 36 | $0.65 | $23.40 |
| `HW-M6x70-carriage` | M6 x 70 carriage bolt, elevation lock | 1 | 2 | $1.80 | $3.60 |
| `HW-M8-nut-nyloc` | M8 nyloc nut | 2 | 3 | $0.45 | $1.35 |
| `HW-M8-washer` | M8 washer | 2 | 3 | $0.20 | $0.60 |
| `HW-M8x90` | M8 x 90 elevation axle bolt | 2 | 3 | $2.50 | $7.50 |

**Subtotal: $119.92 CAD.**

Match the head geometry, length and material requirements in the CAD and assembly guide. Use grade 8.8 bolts where specified; nuts and washers need their own appropriate matching specifications. A generic assortment is only suitable if it actually supplies the required types and quantities.

## Electronics and RF — provisional

These are budgeting examples, **not a tested or finalized receiver BOM**. The printed electronics boxes are envelopes; confirm board, connector, cable and cooling clearances before printing. The mechanical subtotal alone does not produce a working radio receiver.

| Item | Buy quantity | Unit CAD | Extended CAD | Price basis | Scope / notes |
|---|---:|---:|---:|---|---|
| SAWbird+ H1 filtered LNA | 1 | $69.93 | $69.93 | Converted · [S2](#price-sources) | US$49.95 × 1.40 budget exchange factor. |
| NESDR SMArTee XTR bundle | 1 | $90.93 | $90.93 | Converted · [S3](#price-sources) | US$64.95 × 1.40; provisional receiver with bias tee. |
| Raspberry Pi 5, 8 GB | 1 | $249.50 | $249.50 | Listed · [S4](#price-sources) | Reference configuration; reuse a suitable computer where possible. |
| Pi 5-compatible USB-C supply | 1 | $20.00 | $20.00 | Allowance | Budget for a suitable 5.1 V / 5 A supply. |
| Pi cooling | 1 | $12.00 | $12.00 | Allowance | Check enclosure clearances and ventilation. |
| 32 GB microSD card | 1 | $15.00 | $15.00 | Allowance | Boot storage. |
| 2 TB SSD | 1 | $160.00 | $160.00 | Allowance | Reference storage budget; capacity depends on recording method. |
| USB SSD enclosure / adapter | 1 | $25.00 | $25.00 | Allowance | Match the selected SSD interface; omit if included. |
| 50 Ω coax and adapters | 1 | $45.00 | $45.00 | Allowance | Short feed lead + roughly 3 m receiver lead; verify losses and connectors. |
| Feed probe and panel connector | 1 | $15.00 | $15.00 | Allowance | Brass/copper probe stock plus N/SMA connector; geometry not finalized. |
| USB leads, cable glands and seals | 1 | $20.00 | $20.00 | Allowance | Weather protection and cable routing allowance. |

**Subtotal: $722.36 CAD.**

The example receiver includes a bias tee. Confirm its voltage/current capability against the selected LNA before wiring. The SAWbird manufacturer describes multiple power options; use only one at a time. External powering can require a DC block depending on the receiver. No wiring or RF commissioning validation is claimed here. A different receiver may require extra power or DC-blocking hardware and a revised budget.

## Price sources

Prices are a dated research snapshot, not live inventory. Recheck the linked supplier pages and selected variants before buying.

| Source | Supplier / reference | Observed price | Treatment |
|---|---|---:|---|
| S1 | [alpha@play PETG collection](https://alphaplay.ca/collections/filament/petg), “Filament PETG - Blue 1kg” | CAD $19.95 / kg | 7 spools = CAD $139.65; verify filament suitability with FIT-01. |
| S2 | [Nooelec SAWbird+ H1](https://nooelec.com/store/sdr/sawbird-h1.html) | USD $49.95 | CAD $69.93 using 1.40 CAD/USD. |
| S3 | [Nooelec SDR receivers](https://www.nooelec.com/store/sdr/sdr-receivers.html), NESDR SMArTee XTR Bundle | USD $64.95 | CAD $90.93 using 1.40 CAD/USD. |
| S4 | [PiShop.ca Pi 5 boards](https://www.pishop.ca/product-category/raspberry-pi/raspberry-pi-5/raspberry-pi-5-boards/), 8 GB | CAD $249.50 | Board only; accessories listed separately. |
| S5 | [Home Depot Canada 1×2×8 ft lumber](https://www.homedepot.ca/product/1x2x8-framing-lumber/1000173739) | No usable price returned | Size reference only; $8.00 per board is an allowance. |

**1.40 CAD/USD is an explicit budgeting assumption, not a verified live exchange rate.** Card conversion fees and import costs are not included. Unlinked allowance rows have no verified supplier quote. These estimates should be replaced with actual purchases as the design is built.

## Fabrication files

| File | Purpose |
|---|---|
| [bom.csv](bom.csv) | Model parts, quantities and estimated masses |
| [hardware.csv](hardware.csv) | Fastener specifications, model counts and buy quantities |
| [cut_list.csv](cut_list.csv) | Batten dimensions and hole locations |
| [rib_modifications.csv](rib_modifications.csv) | Required changes to the existing ribs |
| [print_list.csv](../print/print_list.csv) | Printed-part quantities and baseline settings |

The CSVs above are geometry-generated manufacturing records. This cost sheet is maintained separately so a CAD rebuild does not erase purchasing assumptions. When quantities change, revise this sheet and the README budget together.

## What is outside the total?

- 3D printer, saw, drill, calipers, spanners, soldering equipment and other workshop tools.
- Printing electricity, fabrication labour, paid cutting services and replacement costs beyond the included stock/spares.
- Tax, delivery, import charges and any weatherproofing or power infrastructure beyond the listed allowances.
- RF test equipment, calibration hardware and any additional parts required by the final feed and receiver design.

See the [shopping list](../docs/shopping_list.md) for dimensions, cutting notes and tools. Complete the [input measurements](../docs/inputs_and_assumptions.md) and [inspection checklist](../docs/inspection.md) before treating the design as fabrication-ready.
