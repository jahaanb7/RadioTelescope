# Design brief

Revision C.2, 2026-11-11. **NOT RELEASED FOR FABRICATION.**
Numbers quoted here come from `analysis/assembly_report.md`, which `cad/build.py` rewrites on every run.
Evidence level: modelled and checked analytically (solid intersections, 3D beam frame, hand checks of joints).
Nothing has been physically tested.

## Goal

Use as little wood as possible: the 18 existing ribs plus straight softwood battens from a hardware store.
Everything else is printed in PETG on a Prusa CORE One L (300 × 300 × 330 mm). The dish must tilt in
elevation and the base must be easy to turn by hand, and every joint is modelled with its real bolts, nuts, washers and pockets.

## Architecture

```
dish (tilts about Y)                     fixed base (stands on four corners)
18 existing ribs, drilled for M4         2 fork top nodes FKT-01/02 (608 bearings)
HUB-01 with an M4 pin per rib tip        4 fork legs LEG-A, 1x2 batten
10 RIM-01 + 6 RIM-02 + 2 RIM-T bays      2 sills SIL-01 1x2, 2 tie beams TIE-01 1x3
18 SPC-01 mid spacers                    4 corner nodes FKC-01/02 (also the feet)
3 feed legs 19x19 + 3 FLA-01 anchors     EBOX-01/02 on the +Y sill
FRG-01 collar, feed can, LNA             KNB-01 lock knob
ELS-01 lock sector, SPR-01/02/03
```

## Design decisions

| Area | Choice | Why | Alternative considered |
|---|---|---|---|
| Rib ring | 18 printed rim girder bays (chords, X bracing), two M4 side bolts through flange, rib, flange at each rib end; two of them carry the trunnions | Turns 18 loose ribs into a stiff ring and gives the axle a printed seat; every bay fits the bed | Glued supports (Rev C.1): untested epoxy joint on plywood and PETG |
| Centre | Printed hub with 18 channels; one M4 cross pin through each rib tip, below the reflector surface | Holds the 60 mm tip relief with nothing on the mesh | Keeper ring on 6 M4 bolts (Rev C): sat on the reflector surface |
| Mid span | 18 printed spacers, one M4 side bolt per rib at r = 300 mm | Stops the ribs buckling sideways and sets the spacing for the mesh | Battens between ribs: Rev B, more wood |
| Long members | Softwood battens in printed sockets, two cross bolts each end | Wood is stiff and cheap in length; PETG is not. Joints are bolted, so parts come apart | All-printed tubes: creep and a lot of filament |
| Elevation | M8 axle bolts in 608 bearings, one fixed and one floating side | Balanced dish (centre of mass on the axle), smooth, cheap | Plain PETG bushings: stick-slip |
| Elevation lock | Slotted sector with carriage bolt and knob; slot ends are the hard stops at −5° and 90° | One part does lock and limits | Separate stop blocks |
| Azimuth | None: turn the whole base | A transit dish for hydrogen-line work does not need a turntable; removes the lazy susan, kingpin, two big plates and the stand | Lazy susan and kingpin on a tripod (Rev C) |
| Base | Rectangle of two sills and two tie beams on four printed corner nodes that are the feet | Fewer parts; the 650 mm footprint gives the same tipping lever as the old tripod | Three legs with levelling feet (Rev C) |
| Shop aids | FIT-01 coupon, JIG-01 and JIG-02 rib drill jigs | Tolerances are checked before printing 5 kg; the jigs put the rib holes where the printed flanges expect them | Marking by hand |

## Receiver chain (not yet specified)

```
feed probe -> short coax -> LNA (in LNA-01 on the collar shelf) -> coax down a feed leg
           -> SDR in EBOX-01 on the +Y sill -> USB -> Raspberry Pi 5 -> SSD
```

No noise, gain or power budget has been calculated because no LNA, SDR or feed has been chosen.

## Open items

1. Measure: rib thickness, batten sizes, feed can size. Update `cad/parameters.yaml` and rebuild.
2. Print FIT-01 and set the slot, bore, socket and nut-pocket tolerances from it.
3. Mesh type not chosen; mass per m² is a placeholder.
4. Electronics enclosures are sized envelopes; no board drawings checked.
5. Wind: ballast is needed above about 8 m/s (see the report). Do not leave it out unattended in wind.
6. Not done: dimensioned PDF drawings, commissioning plan.
