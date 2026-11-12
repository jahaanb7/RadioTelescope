<div align="center">

# RadioTelescope

**A 1 m dish for exploring the 21 cm hydrogen line.**

Parametric CAD · Plywood structure · PETG joints · Manual pointing

[Build guide](docs/assembly_guide.md) · [Bill of materials](bom/README.md) · [Print guide](docs/printing.md) · [CAD gallery](docs/gallery.md)

</div>

![Rev C.2 radio telescope CAD perspective](images/screenshots/perspective.png)

<p align="center"><em>Revision C.2 CAD model. This is a design preview, not a photograph of a completed telescope.</em></p>

## Overview

RadioTelescope is a build-in-progress prime-focus dish designed for neutral hydrogen observations near **1420.405 MHz**. Eighteen plywood ribs define the reflector, while printed PETG joints connect the dish, feed supports and timber base. A bearing-supported fork provides elevation adjustment; azimuth is set by turning the whole base.

This repository contains the editable CAD generator, printable parts, wood cut lists, hardware BOMs, drawings and illustrated assembly documentation. The current package focuses on the mechanical design. **The RF feed, receiver integration and observing workflow are still under development.**

> [!IMPORTANT]
> **Rev C.2 — not released for fabrication.** Measure the actual ribs and battens, print the `FIT-01` coupon and update the [input register](docs/inputs_and_assumptions.md) before committing to the full build. Saved model checks have not been independently reproduced or physically validated.

## At a glance

| Specification | Rev C.2 design |
|---|---|
| Reflector | 1,000 mm diameter; 18 plywood ribs and conductive mesh |
| Target frequency | 1420.405 MHz, approximately 21 cm wavelength |
| Focal geometry | 400.641 mm focal length; f/D = 0.4006 |
| Pointing | −5° to 90° elevation; manual base rotation for azimuth |
| Structure | Plywood ribs, softwood battens and PETG joints |
| Estimated model mass | 10.9 kg |
| Estimated printing | About 5.35 kg PETG and 173 hours; verify in the slicer |
| Print envelope | Designed for a 300 × 300 × 330 mm build volume |
| Mechanical purchase budget | **CAD $510.57** |
| With provisional RF and computing hardware | **CAD $1,232.93**, before tax and shipping |

Geometry comes from the [input register](docs/inputs_and_assumptions.md); model results are recorded in the [assembly report](analysis/assembly_report.md). Costs combine supplier-listed prices with explicit allowances. See the [itemized BOM](bom/README.md) for sources, quantities, exclusions and reuse deductions.

## Start building

1. **Review the fit requirements.** Measure your plywood, battens and feed can using the [input register](docs/inputs_and_assumptions.md).
2. **Check the budget and materials.** Use the [priced BOM](bom/README.md) and [shopping specifications](docs/shopping_list.md).
3. **Print the fit coupon.** Follow the [printing guide](docs/printing.md), adjust `cad/parameters.yaml` and regenerate if dimensions change.
4. **Prepare the wood and printed parts.** Follow the [cut list](bom/cut_list.csv), [rib modifications](bom/rib_modifications.csv) and [print list](print/print_list.csv).
5. **Assemble and inspect.** Work through the [illustrated assembly guide](docs/assembly_guide.md), then record results in the [inspection checklist](docs/inspection.md).

You will need access to a suitable 3D printer and basic woodworking tools. The [shopping list](docs/shopping_list.md#5-ballast-and-tools) includes the tool list. Receiver installation and first-light observations are future stages, not completed instructions.

## Build documentation

| I want to… | Open |
|---|---|
| Assemble the telescope | [Assembly guide](docs/assembly_guide.md) |
| Price the build | [BOM and cost breakdown](bom/README.md) |
| Buy materials and fasteners | [Shopping list](docs/shopping_list.md) |
| Print the parts | [Print settings and quantities](docs/printing.md) |
| Inspect the CAD from different angles | [CAD gallery](docs/gallery.md) |
| Regenerate the model or use Fusion | [CAD workflow](docs/cad_workflow.md) |
| Understand the design choices | [Design brief](docs/design_brief.md) |
| Check assumptions and physical fit | [Inputs and assumptions](docs/inputs_and_assumptions.md) |
| Review model checks or record build results | [Analysis report](analysis/assembly_report.md) · [Inspection checklist](docs/inspection.md) |
| See revision history | [Changelog](CHANGELOG.md) |

## Cost breakdown

**CAD · researched November 11, 2026 · one reference build**

| Category | Budget |
|---|---:|
| Materials, bearings and ballast | $390.65 |
| Fasteners, including spare quantities | $119.92 |
| **Mechanical build** | **$510.57** |
| Provisional RF, Pi 5 and storage setup | $722.36 |
| **Complete reference build** | **$1,232.93** |

The estimate assumes purchasing all listed stock and hardware. Reusing the existing ribs, Pi 5, microSD and SSD reduces the remaining listed purchases to **$748.43**. Tools, labour, electricity, tax and shipping are excluded. The [full BOM](bom/README.md) distinguishes supplier prices from estimates and includes an optional contingency.

## Work with the CAD

Clone the repository and create an isolated Python environment:

```bash
git clone https://github.com/jahaanb7/RadioTelescope.git
cd RadioTelescope
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

Run from the repository root:

```bash
# Build geometry and run checks without generating the full export set
python cad/build.py --quick

# Build geometry, run checks and regenerate fabrication exports
python cad/build.py
```

Edit [cad/parameters.yaml](cad/parameters.yaml) to match measured materials. The full build writes STEP exports locally, including the base and dish stages used by the Fusion joint script. See the [CAD workflow](docs/cad_workflow.md) for poses, rib audits, generated outputs and Fusion setup.

Dependencies are not pinned to exact versions, so identical results across environments are not guaranteed. Record Python and package versions when reporting a build issue.

## Repository map

| Directory | Contents |
|---|---|
| [cad/](cad/) | Parametric model, configuration and Fusion joint script |
| [inputs/](inputs/) | Source rib geometry |
| [print/](print/) | Bed-oriented STLs and print list |
| [bom/](bom/) | Priced BOM, model parts, fasteners and wood cut lists |
| [drawings/](drawings/) | Full-scale rib drilling template |
| [docs/](docs/) | Assembly, printing, CAD and inspection guides |
| [images/](images/) | CAD screenshots, assembly stages and part renders |
| [analysis/](analysis/) | Saved geometry and engineering analysis results |

Large STEP files are generated into `exports/` locally. Keep generated CAD, BOMs and reports from the same revision together.

## Rib-joint redesign

An [experimental quarter-turn rib-lock design](experiments/rib_locks/README.md) explores replacing 40 M4 sets with 40 printed locks while retaining the hub, feed-anchor and trunnion connections. It includes printable fit coupons, STEP geometry and a separate dish generator. **Prototype only:** fit, stiffness and load testing are required before adoption; the Rev C.2 fabrication package remains the baseline.

## Project status

| Area | Status |
|---|---|
| Parametric mechanical design | Rev C.2 source and fabrication outputs included |
| Model checks | Saved report included; results not independently reproduced |
| Physical fit and assembly | Measurements and build validation pending |
| RF feed and receiver | Provisional dimensions and budget; integration pending |
| Dimensioned drawing set | Rib template included; complete drawing set pending |
| Observations and commissioning | Not yet included |

The analysis report contains model predictions, including clearance, strength and wind stability. They are not measured performance or a certified outdoor operating limit.

## Contributing

[Open an issue](https://github.com/jahaanb7/RadioTelescope/issues) for a fit problem, unclear instruction or proposed improvement. Include the revision, affected part IDs, measured dimensions and photographs or screenshots. For CAD errors, include the command, traceback and Python/dependency versions.

Changes to geometry should include the corresponding regenerated fabrication files and an updated cost sheet when quantities change. Physical build reports and measured RF results are especially useful.

## License

No license file is currently included in this repository. Public access does not by itself grant an open-source or open-hardware license. Contact [Jahaan Bhavsar](https://github.com/jahaanb7) about reuse permissions.

