# Design brief

Revision C, 2026-11-10. **NOT RELEASED FOR FABRICATION.**
Numbers quoted here come from `analysis/assembly_report.md`, which `cad/build.py` rewrites on every run.
Evidence level: modelled and checked analytically (solid intersections, 3D beam frame, hand checks of joints).
Nothing has been physically tested.

## Goal of Rev C

Use as little wood as possible: the 18 existing ribs plus straight softwood battens from a hardware store.
Everything else is printed in PETG on a Prusa CORE One L (300 × 300 × 330 mm). The dish must turn in
azimuth and tilt in elevation, and every joint is modelled with its real bolts, nuts, washers and pockets.

## Architecture

```
dish (tilts about Y)          turning base (turns about Z)        fixed stand
18 existing ribs              2 fork top nodes (608 bearings)     3 ground legs, 1x3 batten
HUB-01 + HUB-02 keeper        4 fork legs, 1x2 batten             3 FOOT-01 (levelling bolt, ballast eye)
16 RIM-01 + 2 RIM-T bays      2 sills 1x2, 4 spokes 1x3           AZB-01 fixed plate
18 SPC-01 mid spacers         4 corner nodes FKC-01/02            6 in lazy-susan bearing + M10 kingpin
3 feed legs 19x19 + FLA-01    AZT-01 turning plate, EBOX
FRG-01 collar, feed can, LNA  ELS-01 lock sector + KNB-01 knob
```

## Design decisions

| Area | Rev C choice | Why | Alternative considered |
|---|---|---|---|
| Rib ring | 18 printed rim girder bays (chords, X bracing) bolted rib to rib, two of them carry the trunnions | Turns 18 loose ribs into a stiff ring and gives the axle a printed seat; every bay fits the bed | Plywood rim ring: needs a 1 m sheet and a router |
| Centre | Printed hub with 18 slots plus a keeper ring on 6 M4 bolts | Clamps the 60 mm tip relief; no glue | Plywood disc: Rev B, heavier |
| Mid span | 18 printed spacers through the r = 300 mm hole | Stops the ribs buckling sideways and sets the spacing for the mesh | Battens between ribs: Rev B, more wood |
| Long members | Softwood battens in printed sockets, two cross bolts each end | Wood is stiff and cheap in length; PETG is not. Joints are bolted, so parts come apart | All-printed tubes: creep and a lot of filament |
| Elevation | M8 axle bolts in 608 bearings, one fixed and one floating side | Balanced dish (centre of mass on the axle), smooth, cheap | Plain PETG bushings: stick-slip |
| Elevation lock | Slotted sector with carriage bolt and knob; slot ends are the hard stops at −5° and 90° | One part does lock and limits | Separate stop blocks |
| Azimuth | 6 in lazy-susan bearing between two printed plates, M10 kingpin with nyloc and friction knob | Bought bearing carries the load; the knob sets the drag | Rev B PTFE glides |
| Stand | Three legs, three feet with levelling bolts and ballast eyes | Three points never rock | Four legs: needs shimming |
| Shop aids | FIT-01 coupon | Tolerances are checked before printing 6 kg. The ribs are not drilled (Rev C.1), so the drill jigs are gone | Marking by hand |

## Receiver chain (not yet specified)

```
feed probe -> short coax -> LNA (in LNA-01 on the collar shelf) -> coax down a feed leg
           -> SDR in EBOX-01 on the +Y sill -> USB -> Raspberry Pi 5 -> SSD
```

No noise, gain or power budget has been calculated because no LNA, SDR or feed has been chosen.

## Open items

1. Measure: rib thickness, batten sizes, lazy-susan plate thickness, feed can size. Update `cad/parameters.yaml` and rebuild.
2. Print FIT-01 and set the slot, bore, socket and nut-pocket tolerances from it.
3. Mesh type not chosen; mass per m² is a placeholder.
4. Electronics enclosures are sized envelopes; no board drawings checked.
5. Wind: ballast is needed above about 8 m/s (see the report). Do not leave it out unattended in wind.
6. Not done: dimensioned PDF drawings, assembly guide, commissioning plan.
