# CAD workflow

[Project overview](../README.md) · [Assembly guide](assembly_guide.md)

Run commands from the repository root. Install dependencies in a virtual environment as described in the [README](../README.md#work-with-the-cad). Timing estimates below are from the supplied documentation and depend on the machine; they were not rebenchmarked during the documentation update.

## Regenerate

```
pip install -r requirements.txt
python3 cad/build.py --quick       # model and every check, writes analysis/assembly_report.md (about 10 min)
python3 cad/build.py               # the same plus all exports (about 30 min)
python3 cad/build.py --az 120 --el 30   # the assembly STEP at another pose
python3 cad/build_ribs.py          # rib audit against the supplied STL
```

After measuring the ribs and battens, edit `cad/parameters.yaml` and rebuild. The build removes outputs of parts
that no longer exist.

## Open it in Fusion 360 with a working joint

First run `python3 cad/build.py` to create `exports/stages/base.step` and `dish.step`.

1. Start a new empty design with **File > New Design**.
2. Open **Utilities > Add-Ins > Scripts and Add-Ins** (Shift+S). On the Scripts tab, click the green **+** and pick the folder `cad/fusion/telescope_joints`.
3. Select it and click **Run**. It imports `exports/stages/base.step` and `dish.step`, grounds the base and adds the
   **elevation** joint (the dish about the axle, 0° to 95° of tilt from zenith).
4. Drag the dish to move it, or right-click the joint and choose **Drive Joints**.

For a static view, use **File > Open** on `exports/telescope_revC_az0_el45.step`.


## Rib supports

| Parts | Fixing |
|---|---|
| `RIM-01` rim bay × 10, `SPC-01` mid-span spacer × 18 | M4 side bolts through flange, rib, flange (two per rib at the rim, one at mid span); plain front |
| `RIM-02` feed rim bay × 6 | The same side bolts, plus front pads with nut pockets for the feed anchors |
| `FLA-01` feed-leg anchor × 3 | Bolts to the two `RIM-02` bays beside ribs 60°, 180° and 300°; the feed legs bolt into it |
| `RIM-T` trunnion bay × 2 | Side bolts, plus the axle and lock-sector holes |
| `HUB-01` | One M4 cross pin per rib tip through the channel walls, below the reflector surface (no keeper ring) |

All rib supports have 2 mm filleted edges (`rib_support.fillet_radius`); bed faces stay sharp. Each rim bay and
spacer has a zip-tie hole for the mesh.


## Documentation references

The repository overview follows the purpose, status, usage and documentation-link structure described by [GitHub](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) and [Google's README guidance](https://google.github.io/styleguide/docguide/READMEs.html). [PICTOR](https://github.com/0xCoto/PICTOR) was reviewed as a radio-astronomy documentation example. Hardware documentation organization also draws on [OSHWA sharing practices](https://oshwa.org/resources/sharing-best-practices/). These references do not imply affiliation, certification or a license grant.
