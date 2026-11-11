# Shopping list: everything you need to build Rev C

Quantities come from the model (`bom/bom.csv`, `bom/hardware.csv`, `bom/cut_list.csv`), and the fasteners
include about 10 % spare. Nothing has been priced.

## 1. Materials

| Item | Quantity | Notes |
|---|---|---|
| PETG filament, 1.75 mm | **8 × 1 kg spools** | The parts use about 6.6 kg (`print/print_specs.csv`), plus spare for failed prints. Use one brand and colour throughout, so the fit coupon is valid for every part |
| Two-part epoxy, 30 minute | 2 × 25 ml | Glues the 28 normal rib supports (`RIM-01`, `SPC-01`) and the rim-bay flanges to the ribs |
| 1/8 in (3.2 mm) plywood ribs | 18, already cut | Your existing ribs. Cut the tip relief as in `bom/rib_modifications.csv`; no drilling |
| 1x2 softwood batten (actual 19 × 38 mm) | **2 × 8 ft** (2.44 m) | Board 1: 4 × `LEG-A` at 570 mm. Board 2: 2 × `SIL-01` at 418 mm |
| 1x3 softwood batten (actual 19 × 64 mm) | **2 × 8 ft** | Board 1: 4 × `SPK-01` at 507 mm. Board 2: 3 × `LEG-G` at 586 mm |
| 3/4 in square softwood (19 × 19 mm) | **1 × 6 ft** (1.83 m) | 3 × `LEG-F` at 492 mm |
| Reflector mesh: galvanised hardware cloth or aluminium mesh, 6 mm (1/4 in) openings or finer | **about 1.2 × 1.2 m** (the dish surface is 0.86 m²) | Openings must stay under 21 mm (a tenth of the 21 cm wavelength); 1/4 in is a good choice. Aluminium is lighter |
| Feed can: metal can, about 150 mm diameter × 280 mm long, one closed end | 1 | A coffee or paint can works. Measure it and put the size in `parameters.yaml` before printing `FRG-01` |
| Exterior wood sealer or varnish | small tin | For the batten ends and faces |
| Zip ties, 2.5 mm wide UV-resistant, or stainless wire | about 300 | For fastening the mesh to the ribs |

Batten tip: look for straight, knot-free pieces, and sight along each board before buying. Cut lengths are exact,
with 3 mm of saw kerf allowed for between pieces.

## 2. Bought mechanical parts

| Item | Quantity | Used in |
|---|---|---|
| 608-2RS ball bearing (8 × 22 × 7 mm, skateboard size) | 4, plus 1 spare | Fork top nodes `FKT-01` and `FKT-02` |
| 6 in (152 mm) square lazy-susan bearing, about 8 mm thick, rated for 100 kg or more | 1 | Azimuth: between `AZB-01` and `AZT-01` |

## 3. Fasteners (zinc-plated steel, grade 8.8)

| Item | Count in model | Buy |
|---|---:|---:|
| M4 × 12 hex bolt | 2 | 3 |
| M4 × 20 hex bolt | 18 | 20 |
| M4 × 30 hex bolt | 2 | 3 |
| M4 × 35 hex bolt | 8 | 9 |
| M4 nut | 30 | 33 |
| M4 washer | 38 | 42 |
| M6 × 35 hex bolt | 2 | 3 |
| M6 × 40 hex bolt | 52 | 58 |
| M6 × 70 carriage bolt (elevation lock) | 1 | 2 |
| M6 nut | 55 | 61 |
| M6 washer | 109 | 120 |
| M8 × 90 hex bolt (elevation axles) | 2 | 3 |
| M8 nyloc nut | 2 | 3 |
| M8 washer | 2 | 3 |
| M10 × 60 hex bolt (kingpin) | 1 | 2 |
| M10 × 70 hex bolt (levelling feet) | 3 | 4 |
| M10 nut (captured in the feet) | 3 | 4 |
| M10 nyloc nut (kingpin) | 1 | 2 |
| M10 washer | 1 | 2 |

Boxed assortments of M4 and M6 bolts are usually cheaper than buying them loose.

## 4. Electronics (not designed yet; listed so nothing is forgotten)

| Item | Notes |
|---|---|
| Low-noise amplifier (LNA) for 1420 MHz, with a filter | Fits in `LNA-01`; the box is an envelope, so check the size |
| SDR receiver (for example an RTL-SDR or Airspy class) | In `EBOX-01` |
| Raspberry Pi 5, power supply, SSD | In `EBOX-01` |
| Coax: a short lead from the probe to the LNA, then about 3 m to the box | Leave a loop at the elevation axle |
| Feed probe: a quarter-wave monopole made from brass rod and an N or SMA panel connector | The position in the can must be set from the can's measured size |

## 5. Ballast and tools

- **Ballast:** three sandbags or water jugs, up to 5 kg each, hung from the foot eyes in wind.
- **Tools:**
  - drill with 2.5, 4.5 and 6.5 mm bits;
  - saw with a mitre box;
  - 7, 10, 13 and 17 mm spanners;
  - calipers, square and spirit level;
  - vice (for pressing the bearings);
  - soldering iron (for setting nuts in the printed pockets);
  - tin snips (for cutting the mesh).
