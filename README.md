# 1 m hydrogen-line radio telescope

A parametric design and build package for a 1 m prime-focus dish tuned for the neutral hydrogen line near **1420.405751 MHz**. It reuses 18 existing plywood ribs and combines a wood-batten frame, PETG printed parts, conductive reflector mesh, and a manual alt-azimuth mount.

![Rev C telescope at 45° elevation](images/assembly_iso_el45.png)

> [!CAUTION]
> **Rev C is modelled and checked, but is not released for fabrication.** Measure the physical ribs, battens, lazy-susan bearing, and feed can, then print and fit-check `FIT-01` before producing the full set of parts. The CAD checks are not a substitute for physical proof testing or RF commissioning.

## Start here

1. Read the [input and assumptions register](docs/inputs_and_assumptions.md) and [design brief](docs/design_brief.md).
2. Install the Python dependencies with `pip install -r requirements.txt`.
3. Check the measured inputs against `cad/parameters.yaml`, update the values that need correction, and run:
   ```bash
   python3 cad/build.py --quick
   ```
4. Print `FIT-01` first, set the fit tolerances in `cad/parameters.yaml`, then rebuild.
5. Follow the [assembly guide](docs/assembly_guide.md), [printing guide](docs/printing.md), and [shopping list](docs/shopping_list.md).

Run `python3 cad/build.py` for the full set of generated exports. Use `python3 cad/build.py --az 120 --el 30` to export the assembly at another pose. The full assembly and per-part STEP exports are generated locally and intentionally not stored in Git; the source and printable STLs remain in the repository.

## Design snapshot

| Item | Rev C model |
|---|---|
| Reflector | 1 m dish; 18 existing ribs with conductive mesh |
| Motion | Unlimited azimuth; elevation −5° to 90° |
| Structure | PETG printed joints and fittings with straight softwood battens |
| Total model mass | About 14.5 kg |
| PETG estimate | About 7.2 kg and 235 print hours |
| CAD checks | 601 solids; no invalid solids or modelled clashes in the checked configurations |
| Fabrication status | **Not released**; measurements and physical fit checks remain |

These are model estimates, not measured build results. See `analysis/assembly_report.md` for the assumptions and checks.

## Repository map

| Path | What it contains |
|---|---|
| `cad/` | Parametric generator, measured parameters, print preparation, and Fusion 360 joint script |
| `inputs/` | Supplied rib STL and original CAD export retained as source material |
| `docs/` | Design rationale, input register, assembly and printing instructions, and shopping list |
| `bom/` | Bill of materials, hardware, wood cut list, and rib modifications |
| `print/` | Bed-oriented STL files and print settings/list |
| `drawings/` | 1:1 rib drilling template |
| `exports/stages/` | Fixed stand, turning base, and dish STEP files for the Fusion joint script |
| `images/` | Assembly, build-stage, motion, and part images |
| `analysis/` | Latest model-check report and supporting design notes |

## Open the movable model in Fusion 360

1. Start a new empty design.
2. Open **Utilities → Add-Ins → Scripts and Add-Ins** (Shift+S). On the Scripts tab, click **+** and choose `cad/fusion/telescope_joints`.
3. Select the script and click **Run**. It imports the three files in `exports/stages/`, grounds the stand, and creates azimuth and elevation joints.
4. Drag the dish or use **Drive Joints** to inspect its movement.

To regenerate the model and exports after changing inputs, run `python3 cad/build.py` from the repository root.

## Build and safety notes

- All model dimensions are controlled in `cad/parameters.yaml`; each value includes its status and source.
- The receiver chain and RF performance are not fully designed. LNA, SDR, feed, power, and site details still need to be selected and checked.
- The stand needs ballast in wind. Review the analysis and do not leave the telescope unattended in windy conditions.
- The design has not been physically tested. Verify printed fits, fasteners, wood condition, balance, stability, and pointing before use.
- The project is a receiving instrument for radio astronomy; it does not produce optical-like images of distant galaxies.

## Development history

See [CHANGELOG.md](CHANGELOG.md) for revision history.
