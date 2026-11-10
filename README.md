# 1 m hydrogen-line radio telescope

Status: **Stage 3 of 6, provisional. NOT RELEASED FOR FABRICATION.**

The specification is `Radio_Telescope_Claude_Code_Master_Prompt.md`.

## Regenerate the CAD

```
python3 cad/build_ribs.py       # rib audit and centre-joint check
python3 cad/build_assembly.py   # full provisional assembly, checks, exports (about 1 minute)
```

Requires Python 3 with `cadquery`, `numpy` and `pyyaml` (`pip install -r requirements.txt`). All dimensions come from `cad/parameters.yaml`.

To open in Fusion: File > Open > Open from my computer, then pick `exports/telescope_assembly_PROVISIONAL_zenith.step`. STEP imports as bodies without feature history.

## What exists

| Path | Content |
|---|---|
| `cad/parameters.yaml` | Single parameter file, each value tagged with status and source |
| `cad/build_ribs.py` | Rib generator and centre-joint checks |
| `cad/build_assembly.py` | Full assembly generator, interference sweep, mass, RF and wind screening |
| `exports/telescope_assembly_PROVISIONAL_zenith.step` | 186 named solids: dish, feed, fork mount, base |
| `exports/parts/` | One STEP per manufactured part type |
| `print/` | STL for printed part types and the rib-slot fit coupon |
| `drawings/*_outline_PROVISIONAL.dxf` | 1:1 outlines of the flat plywood parts |
| `drawings/view_*_zenith.svg` | Hidden-line views |
| `bom/bom_PROVISIONAL.csv` | Part list with quantities and estimated masses; no prices yet |
| `analysis/assembly_report.md` | Results of the last assembly run |
| `design_brief.md` | Design decisions, alternatives and open items |
| `exports/reflector_skeleton_PROVISIONAL.step` | 18 ribs, rear hub disc, rim ring, focus marker |
| `exports/RIB_solid_wedge_as_cut.step` | One rib, untouched |
| `exports/RIB_solid_wedge_tip_relief_PROVISIONAL.step` | One rib with the proposed 60 mm tip cut |
| `exports/RIB_outline_reference_matches_STL.step` | Rebuild of the supplied STL outline |
| `drawings/RIB_profile_as_cut_1to1.dxf` | Rib profile at 1:1, mm |
| `analysis/rib_build_report.txt` | Raw output of the last generator run |
| `analysis/centre_joint.md` | Centre-joint options and provisional choice |
| `inputs_and_assumptions.md` | Input register and measurements needed |
| `inputs/Wood_Rib_Frame.stl` | Supplied rib outline, the only source of rib geometry |
| `inputs/RadioTelescope.step` | Original Fusion export, kept for the record. It contains no geometry; do not open this one |

## Stage checklist

- [x] 1. Input and geometry audit
- [x] 2. Centre-joint feasibility (provisional, awaiting owner decision)
- [x] 3. Provisional assembly: frame, mesh supports, feed support, fork mount, base, enclosure envelopes (open items in `design_brief.md`)
- [ ] 4. Structural and RF review
- [ ] 5. Fabrication package: drawings, BOM, print files, assembly guide
- [ ] 6. Commissioning and research package

Empty folders (`assembly/`, `commissioning/`, `research/`) are placeholders for later stages.
