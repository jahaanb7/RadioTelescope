# Inputs and assumptions register

Revision C, 2026-11-10 (register first written in Rev A, 2026-11-09). Status of the whole package: **NOT RELEASED FOR FABRICATION**.

"Confirmed" below means confirmed against the supplied CAD export. Nothing has been
confirmed against the physical wood yet.

## Files inspected

| File | What it contains | Use |
|---|---|---|
| `inputs/Wood_Rib_Frame.stl` | One body, 432 triangles, 500 × 5 × 156 mm. A hollow 1 mm outline of the rib. | Only source of rib geometry. |
| `inputs/RadioTelescope.step` | No geometry. Only a steel material and an empty shape. | None. The export needs redoing. |
| `~/Downloads/radioTelescope _ Drawing 1.html` | Saved Onshape page shell. The drawing itself is not in the saved file. | None. |
| `~/Downloads/Master.step` | 65-part printer/gantry assembly. No rib, dish or feed parts. | Unrelated project. |
| The four reference photographs named in the brief | Not found. | Missing. |
| `~/Downloads/radio_telescope.pdf`, `Radio_Telescope_Paper.pdf`, funding proposal PDFs | Not yet read. | To review in the next stage. |

## Register

| Quantity | Value | Status | Source |
|---|---:|---|---|
| Rib count | 18 | confirmed | brief |
| Rib radial span R | 500.000 mm | confirmed (CAD) | STL bounding box |
| Rib rise d at rim | 156.000 mm | confirmed (CAD) | STL bounding box |
| Top-edge shape | parabola | confirmed (CAD) | 49 STL vertices, max deviation 0.00004 mm |
| Focal length f | 400.641 mm | calculated | R²/(4d) |
| f/D | 0.4006 | calculated | |
| Focus above rim plane | 244.641 mm | calculated | f − d |
| Rim half-angle seen from focus | 63.93° | calculated | 2·atan(R/2f) |
| Wavelength at 1420.405751 MHz | 211.061 mm | calculated | c/f |
| Rib bottom edge | flat, on z = 0 | confirmed (CAD) | STL bottom chord |
| Vertex end vs rim end | pointed end = centre | confirmed (CAD) | STL: zero height at r = 0, 156 mm at r = 500 |
| Rib body is solid wood under the curve | yes | **assumed** | STL interior is empty; the brief's description implies a solid wedge |
| Board thickness | 5 mm | **requires measurement** | STL extrusion depth only |
| Wood species / plywood grade | unknown | **requires measurement** | |
| As-cut profile accuracy | unknown | **requires measurement** | |
| Tip condition (r < 60 mm, under 2.3 mm tall) | unknown | **requires measurement** | likely fragile or already broken |
| Tip relief radius | 60 mm | confirmed by the owner (Rev C) | ribs are also drilled: owner approved, 2026-11-10 |
| Reflector RMS target | 5 mm | assumed | brief; Ruze surface factor 0.915 at 21 cm |
| Printer | Prusa CORE One L, 300 × 300 × 330 mm | confirmed | owner; Prusa product page |
| Filament | PETG | confirmed | owner. Interlayer strength 18 ± 4 MPa (Prusament data) |
| Long members | softwood battens, 19 × 38 (1x2), 19 × 64 (1x3), 19 × 19 | **requires measurement** | owner chose battens; sizes are nominal |
| Azimuth bearing | 6 in square lazy susan, 152.4 mm, 7.93 mm thick | **requires measurement** (plate thickness) | supplier data |
| Elevation bearings | 608 (22 × 8 × 7 mm) | confirmed | standard |
| Feed can | Ø150 × 280 mm, 0.40 kg | assumed | formula values |
| LNA, SDR, power, budget, site | unknown | requires input | |

## Measurements needed from the physical ribs

1. Board thickness with calipers at three places on three different ribs.
2. Whether the rib is solid under the curve, or a hollow frame like the STL.
3. Rise above the flat bottom edge at r = 100, 200, 300, 400 and 500 mm from the pointed end, on at least three ribs. Nominal values: 6.24, 24.96, 56.16, 99.84, 156.00 mm.
4. Overall length along the flat edge (nominal 500 mm).
5. How far the pointed tips survive intact, and the wood type.

## Measurements needed for Rev C (then rebuild with `python3 cad/build.py`)

| Measure | Where it goes in `cad/parameters.yaml` | Why it matters |
|---|---|---|
| Rib thickness | `rib.thickness_board` | Every rib slot and flange gap |
| Batten thickness and width (each size) | `battens.section`, `beam_section`, `feed_leg_section` | Socket bores; sockets are only 0.8 mm larger |
| Lazy-susan overall thickness and plate size | `lazy_susan.thickness`, `size`, `plate_thickness` | Recess depth and the kingpin length |
| Feed can diameter and length | `feed_can.diameter`, `length` | Collar bore |
| FIT-01 results | `tolerances.*` | Printer-specific clearances |
