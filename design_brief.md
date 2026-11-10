# Design brief: provisional baseline

Revision B, 2026-11-09. **NOT RELEASED FOR FABRICATION.**
Numbers quoted here come from `analysis/assembly_report.md`, which the generator rewrites on every run.
Evidence level throughout: modelled and analytically checked. Nothing simulated, nothing physically tested.

## Design decisions

| Area | Baseline | Why | Alternative considered |
|---|---|---|---|
| Rib datum | Ribs stand on their flat bottom edges on a rear plate plane (z = 0) | Uses the edge the ribs already have; no radial shift of the parabola | Hanging ribs from a front ring: needs a new accurate ring |
| Centre joint | 60 mm square tip relief, printed centre disc carries the mesh | Least change to existing wood; see `analysis/centre_joint.md` | Slotted hub with 100–120 mm relief |
| Rear structure | 400 mm plywood hub disc, six-segment rim ring with splice plates, six softwood spars | Flat parts cut from sheet; spars carry load to the trunnions | Full plywood back disc: heavier, 1 m sheet |
| Rib retention | Printed cheek pairs at r = 170 and 470 mm, one plate screw and one cross bolt each | Clamps where the rib is 18 mm and 138 mm tall | Glue blocks: not serviceable |
| Mesh support | Straight battens between ribs at r = 300 and 492 mm; mesh in 18 flat-ish gores | Mesh pulled straight between ribs has 0.75 mm residual RMS after refocus | Curved hoops: harder to make accurately |
| Feed | Circular waveguide can, 150 mm, single probe, clamped in two printed collars with axial slide | Simple, common for 21 cm at f/D near 0.4 | Dipole with reflector; choke-ring can. Not yet compared quantitatively |
| Feed support | Three 18 mm softwood legs from the rim to two plywood rings | Braced tripod; member loads are tiny | Single cantilever arm: rejected by the brief |
| Mount | Fork with elevation pivots at the rim, through the centre of mass | Balanced, so the clamp carries little load | Rear pivot behind the dish: narrower, but needs a counterweight and a stronger lock |
| Azimuth | Rocker board on three PTFE glides over a ground disc, centre bolt, three legs | Dobsonian-style; no bearings to buy | Lazy-susan bearing: a purchasable upgrade |
| Electronics | LNA box on the feed head; digital box on the rocker board | Shortest RF path before the LNA; Pi noise kept away from the feed | Everything at the feed: more mass and interference at the focus |

## Receiver chain (not yet specified)

```
feed probe -> short coax -> LNA (with filter if integrated) -> coax down a feed leg and spar
           -> SDR in the digital box -> USB -> Raspberry Pi 5 -> SSD
power: Pi supply -> Pi; SDR via USB; LNA via bias tee or separate feed (depends on the LNA model)
```

No noise, gain or power budget has been calculated because no LNA, SDR, feed or supply has been identified.

## Open items

1. Rib thickness, solidity and wood type are unmeasured. They drive every slot and clamp.
2. Tip relief needs the owner's decision.
3. Cross-bolt holes through the ribs (M3 at r = 170, M4 at r = 470) are a second change to existing wood. They also need a decision. A friction-only clamp is the alternative.
4. Not yet modelled: batten end clips, feed-leg end brackets, the arc slot in the elevation quadrant, elevation stops, azimuth and elevation scales, individual screws, cables and glands.
5. The LNA and digital enclosures are envelopes only. No Raspberry Pi 5 drawing has been checked.
6. Feed dimensions are formula values. Phase-centre position is assumed at the aperture.
7. Mesh type is not chosen. The 0.67 kg/m² figure is a placeholder.
8. No BOM prices or supplier links. Nothing has been sourced.
9. Not done: dimensioned PDF drawings, exploded view, assembly guide, commissioning plan, research package.
10. The side-view SVG crops one ground leg.
