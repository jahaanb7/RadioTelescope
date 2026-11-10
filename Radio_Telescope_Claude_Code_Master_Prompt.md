# Master build prompt: Jahaan’s 1 m hydrogen-line radio telescope

Copy the prompt below into Claude Code, or put this file in the project and ask Claude Code to follow it. Supply the four reference images and, if available, the original Fusion 360 design or an exported rib sketch. This is an instruction brief for creating and validating the design, not a completed or structurally certified telescope design.

---

## Your task and definition of success

Act as my mechanical designer, CAD automation engineer, radio-astronomy instrumentation adviser, and technical-documentation author. Design and actually generate the complete, editable 3D assembly and fabrication package for a practical radio telescope built around the 18 wooden ribs I have already cut. I will build this instrument and document its design and measured performance in a research article.

Do not stop at advice, a concept rendering, a parts list, or code that has never been run. Produce the CAD source, execute the generator where possible, export inspectable models and drawings, check the assembly, and document what still requires physical measurement or testing. Make a practical instrument that can be assembled with accessible workshop tools, disassembled, aligned, repaired, and used repeatably.

The primary science objective is detecting the Milky Way’s neutral atomic hydrogen emission near 1420.405751 MHz, then measuring spectra and performing drift scans. This is a receiving instrument. General radio reception is a secondary objective requiring compatible feeds and receiver configurations; do not promise that a hydrogen-band feed/filter receives every radio band. Do not assume a 1 m dish will resolve distant galaxies or produce optical-like images.

## 1. Fixed requirements and material constraints

- Reuse my **18 existing wooden ribs**. The drawing shows a **500 mm horizontal span** and **156 mm maximum rise**. Treat millimetres as provisional until confirmed from the drawing/export or my measurements. Rib material, thickness, and actual accuracy are unknown.
- The pointed end appears to be the centre/vertex end and the tall end the outer rim. Verify this against the original sketch before locking the model.
- Custom brackets, adapters, clamps, hubs, gussets, electronics supports, and mount structural parts must be **wood or 3D printed**. Use wood as the default primary structure and printed parts where their loads and environment are appropriate.
- Standard metal screws, through-bolts, nuts, washers, threaded rods, bearings/bushings, and necessary RF conductors/connectors are allowed. Reflector mesh and RF shielding must be conductive. Avoid custom machined or welded metal structural parts and metal extrusion frames in the baseline.
- Do not use printed threads or a small plastic bracket as the sole retention for a critical load without demonstrated capacity. Prefer captured nuts, broad washers/backing plates, replaceable bushings, and mechanically retained joints.
- All 18 ribs must appear in the assembly and BOM. Do not quietly replace them with a different profile or reduce their number.
- Preserve the cut profile wherever feasible. Do not silently trim ribs, shift them radially, change their height, or alter the dish diameter to make an attractive model. If a local tip relief or other modification is geometrically necessary, show exactly why, dimension it, offer alternatives, and obtain my decision before marking the affected fabrication drawings ready to build. Continue independent work meanwhile.
- Include a rigid reflector frame, conductive mesh, adjustable feed support, manual azimuth/elevation mount, stable base, LNA protection, Raspberry Pi 5 housing, SDR and storage accommodation, power routing, cable management, and assembly hardware.
- Prioritize rigidity, reproducibility, modest cost, and achievable fabrication over decorative complexity. Use the photographs as structural inspiration, not as dimensioned plans.

## 2. Establish inputs without inventing measurements

First inspect project files, supplied screenshots, existing CAD, and available local CAD software. Create an input register with each value classified as **confirmed, calculated, assumed, or requires measurement**, including its source and units.

Ask one concise batch of critical questions after inspecting the files:

1. Actual rib thickness, wood type/grade, measured span/rise, and whether local drilling or tip relief is acceptable. Ask for the original Fusion model or DXF if available; explain a short measurement method if it is not.
2. Available printer, bed dimensions, printable materials, and tools for drilling/cutting/clamping wood.
3. Exact LNA, SDR, feed if already owned, Pi cooler/case, SSD and adapter, power supply, and connector types. Request dimensions or model numbers only where needed for fit or power compatibility.
4. Budget in CAD, portability/storage constraints, and whether observations are supervised temporary outdoor sessions or a permanent outdoor installation.

Do not repeat questions answered in the files. Do not block initial layout, calculations, source setup, or clearly labelled provisional components while waiting. Parameters affecting hole patterns, structural capacity, or component fit must remain visibly unresolved until verified. Never label a guessed design fabrication-ready.

## 3. Recover and verify the dish geometry

Use a dish-local coordinate system: vertex at (0,0,0), opening toward +Z, radius r measured in XY, and reflector z(r)=r²/(4f). Keep this separate from the mount/world coordinate system.

If the existing profile is a parabola extending 500 mm from vertex to rim and rising 156 mm, independently verify these nominal values:

| Quantity | Nominal value | Status |
|---|---:|---|
| Radius R | 500 mm | Drawing, units/profile to verify |
| Diameter D | 1000 mm | Derived |
| Dish depth d | 156 mm | Drawing, units/profile to verify |
| Focal length f=R²/(4d) | 400.641 mm | Conditional on parabolic profile |
| Focal ratio f/D | 0.40064 | Derived |
| Focus above rim plane f−d | 244.641 mm | Derived |
| Rib angular spacing 360°/18 | 20° | Derived |
| Wavelength at 1420.405751 MHz | Approximately 211.06 mm | Derived |
| Angle from feed boresight to rim | Approximately 63.93° | Derived |

The focus is about **401 mm from the vertex**, not 401 mm beyond the rim. The rim subtends approximately 128° across the feed. Feed illumination must be compatible with this geometry.

Dimensions at two endpoints do not prove the curve is parabolic. Prefer the original sketch equation/curve. Otherwise produce a measurement table at several radial positions, fit the actual profile, and report residuals relative to the intended parabola. Screenshot tracing is only a provisional reconstruction. Define a reflector surface tolerance and explain how the wood, adhesive, mesh wire thickness, and clamping stack place the actual reflecting surface relative to the rib curve.

Distinguish the existing rib solid from the ideal reference surface. Include both in CAD, with the mathematical surface optionally hidden. Model real rib thickness rather than infinitely thin radial sheets. A finite-width rib with a curved centre profile does not reproduce the exact paraboloid across its entire width; quantify whether that discrepancy matters.

## 4. Solve the centre joint before designing around it

This is a mandatory design gate. Eighteen finite-thickness wooden ribs cannot all occupy the same vertex. The supplied shape also tapers to almost zero height there, so attaching screws near the tips is not credible.

For the nominal profile, the rib height at r=50 mm is only 1.56 mm. Even a 12 mm thick radial plate arrangement begins to crowd near a radius on the order of 35 mm; that estimate is only a screening calculation, not a sufficient clamp size or a validated clearance check. Derive exact clearances from the actual solids and thickness.

Compare at least two feasible connection strategies, such as a rear annular support/spider with distributed side saddles and a locally relieved centre, versus a mechanically retained hub arrangement requiring explicitly dimensioned tip modification. Explain whether any option can truly preserve all existing tips. A rear plate alone does not remove collisions among the tips.

Choose one baseline after checking:

- Actual solid intersections of all 18 ribs at 20° spacing.
- Sufficient rib height and wood edge/end distance at every fastener.
- Broad load transfer into sound wood, with no screws into thin tips or reliance on fragile sheet edges.
- Tool access for drilling, assembly, tightening, and replacement.
- The optical/RF consequence of any centre gap, replacement mesh support, or blockage.
- No radial translation that silently invalidates the original parabola.

Provide a detailed centre cross-section, enlarged joint view, and assembly sequence. Keep any required wood alteration visible in a separate drawing and revision note.

## 5. Design the complete structure

Develop a simple manual alt-az baseline: a wooden dish support frame, two-sided elevation support/yoke, and a broad braced wooden azimuth base. Compare this with one viable alternative and select using rigidity, part count, tools, portability, and cost. Motorization can be a future interface, not a dependency for first observations.

### Reflector frame and mesh

- Place all 18 ribs with repeatable assembly indexing.
- Add a segmented wooden perimeter ring and intermediate circumferential support where needed. Detail ring segment joints and how they resist twist; calculate polygonal approximation error if segments are straight.
- Provide rear bracing and a load path from reflector to mount that avoids distorting the RF surface when bolts are tightened.
- Specify mesh material, clear opening, wire diameter, mass, fastening pattern, overlap, and weather protection. Start by evaluating roughly 6–10 mm clear openings at 21 cm wavelength; confirm the choice using conductivity, wire geometry, weight, sag, and relevant references, not just a wavelength rule.
- Treat a doubly curved paraboloid honestly: design manageable mesh gores/panels and a fitting sequence. Do not present a perfectly developable flat template for a doubly curved surface. Label flattening approximations and leave trimming allowance where necessary.
- Check sag and faceting between ribs and rings, seam steps, and deformation caused by tensioning. Include a central mesh support if the chosen hub leaves a gap.
- Model mesh as a lightweight representative surface for normal CAD use, with an optional detailed region; document the physical specification rather than generating millions of wires.
- Supply an alignment jig, radial position template, and method to measure surface shape after assembly.

### Feed structure

- Evaluate a braced wooden feed support with printed saddles/clamps, balancing obstruction, rigidity, weight, and access. Do not assume one thin printed cantilever is sufficiently stiff.
- Support the feed’s **phase centre** at the focus, with its receiving direction toward the reflector. Do not equate the phase centre with the connector, probe, housing centre, or aperture without evidence.
- Provide axial and lateral adjustment, alignment marks, and a repeatable lock. Choose travel from component and geometry uncertainties; a provisional axial travel of ±25 mm may be evaluated, not treated as guaranteed sufficient.
- Put the first LNA very close to the feed, protect it from weather, and support both it and the coax mechanically. Do not use an SMA connector as a structural joint.
- Route cables along supports with clamps, strain relief, and bend radius appropriate to the selected coax.

### Pointing mount and base

- Include stiff two-sided elevation pivots, bushings/bearings as appropriate, a positive holding/locking system, adjustment controls, azimuth/elevation scales, mechanical stops, and a stable stow position.
- Estimate the centre of gravity with the feed, mesh, actual hardware, and cables. Locate elevation pivots accordingly; provide adjustment if mass uncertainties are significant.
- Prefer placing heavy digital electronics near the base. Include mounting variants only when cable loss, cooling, or access justifies them.
- Check full motion, nominally horizon to zenith where feasible: reflector, feed, yoke, base, box, handles, and cables must clear. Document the actual usable range.
- Prevent cable winding with limited azimuth travel and stops unless a properly engineered alternative is needed.
- Size feet, braces, ballast attachment, and anchoring provisions against overturning and sliding; do not assume mesh makes wind loads negligible.
- Make the assembly serviceable and transportable without losing the alignment datum.

## 6. Validate rigidity and joints quantitatively

Use analytical calculations first. Run FEA only if an appropriate solver and defensible material/connection data are available. Never claim a render or mesh generation is structural verification.

Maintain a load-case table covering self-weight at several elevations, feed and cable loads, adjustment/handling loads, clamp preload effects, operational wind, and stowed conditions. State wind speed, gust assumptions, air density, drag/projected-area assumptions, and support conditions. A solid-area drag estimate may serve as a conservative screening case, with limits explained.

Check rib/ring bending, frame twist, feed displacement, mount deflection, fastener shear/tension, wood bearing/splitting/pull-out, printed-part layer separation and creep, pivot retention, overturning, sliding, and lock capacity. Do not use generic wood or filament strength as if it were measured for my material.

For printed attachments, document material choice, print orientation, perimeter/wall thickness, infill role, fillets, bolt bearing surfaces, moisture/temperature/UV effects, and long-term creep. Evaluate PETG/ASA or other available materials from data and actual printing capability. Do not assume a material name or 100% infill guarantees capacity. Include a small fit coupon and a representative loaded joint test before a full production print.

Create a tolerance/error budget. Evaluate **≤5 mm reflector RMS error** as a preliminary construction objective and calculate its nominal Ruze surface-efficiency effect at 21 cm; this is not total aperture efficiency or a substitute for accounting for systematic shape errors. Derive compatible limits for feed displacement, mount pointing repeatability, and sag under load. Propose measurable limits, explain them, and mark them unverified until tested.

Choose and justify design margins for each failure mode. Distinguish material strength margin, resistance to overturning, and RF deflection limits. Provide an operational wind limit only when supported by the design inputs and validation; otherwise mark it unresolved and require supervised low-wind testing. Include simple, controlled deflection and joint-slip measurements with loads applied without people beneath the structure.

## 7. Integrate the actual radio receiver

Show both an RF block diagram and a separate DC power diagram. Baseline chain:

**1420 MHz feed → very short RF connection → appropriate LNA/filter arrangement → coax → compatible SDR → Raspberry Pi 5 → data storage.**

Do not automatically add a lossy passive filter before the first LNA. Evaluate receiver noise and strong-signal overload together. If the existing module integrates amplifiers and filtering, use its documented topology and specifications.

- Confirm SDR tuning range, frequency stability, usable sample rate, USB interface, current demand, bias-tee capability, and connector polarity/type.
- Identify the exact LNA version before choosing supply voltage or assuming an internal calibration load. Check its manual for permitted power paths, DC blocking, maximum input levels, and current consumption.
- Do not energize conflicting LNA power inputs. Include a DC block only where the selected arrangement requires one, and put it where it does not interrupt intended bias power.
- Estimate pre-LNA loss, cascaded receiver noise, post-LNA cable loss, total gain, and overload margin. State assumed values and their sources.
- Select a buildable feed compatible with f/D≈0.40. Compare plausible feed types, then fully dimension one baseline. If a conductive can/horn is used, distinguish its metal RF surface from its wood/printed mounting hardware. If a dipole is selected, specify matching/balun, support dielectric, backing structure if any, and polarization.
- A half-wavelength formula alone is not a validated feed. Explain tuning and, when available, VNA measurement. Impedance match alone does not verify illumination, spillover, or phase-centre location. Label calculated, simulated, and measured results separately.
- Design an interchangeable feed mount for future compatible bands, while explaining that a hydrogen filter restricts reception outside its passband.

## 8. Electronics boxes, thermal design, and interference

Provide a compact feed/LNA enclosure and a separate serviceable digital electronics enclosure near the base or an appropriately justified rear location.

Use verified Raspberry Pi 5 mechanical drawings. Include the chosen cooler, power plug, USB/Ethernet connectors, microSD access, SDR, SSD plus adapter, cable bend space, mounting bosses, lid retention, and access for replacement. If the exact SSD or SDR is unknown, model labelled envelopes with adjustable mounting, not invented connector positions.

Specify cooling/heat removal, rain shedding, cable glands, drip loops, condensation management, and drain/vent details consistent with the exposure requirement. Do not call an untested printed box waterproof or assign it an IP rating. Keep mains conversion in suitable protected equipment; do not invent a mains wiring assembly.

Budget power for Pi 5, SDR, storage, fans, and LNA, including supply/cable voltage drop and USB power limits. Verify current Raspberry Pi documentation rather than assuming any USB-C charger suffices.

Address interference from the Pi, USB 3, SSD, switching supplies, network radios, and fan wiring. Include separation, suitable conductive shielding/liners where needed, filtered cable entry where justified, and a test matrix comparing configurations. Plastic itself is not an RF shield. Account for thermal consequences of shielding. Prefer wired networking during sensitive measurements when practical.

## 9. CAD implementation and actual exports

Prefer an editable Fusion 360 assembly if the environment supports it. Inspect capabilities before claiming access. If Fusion cannot be driven directly, create a reproducible parametric model using an available solid CAD system such as FreeCAD or CadQuery, export STEP for Fusion import, and document the import process. Do not fabricate an .f3d file or promise native Fusion feature history from a STEP export.

Use one authoritative parameter/configuration file and separate named parts/subassemblies. Track the existing rib profile independently from new parts. Include component IDs, materials, quantities, coordinate datums, and reference geometry for vertex, rim, optical axis, focus, and pointing axes.

Model all custom structural parts, actual holes/slots, printed interfaces, fastener envelopes and washer/nut stack-ups, feed, electronics envelopes, and cable corridors. Thread detail may be cosmetic; fastener diameter, length, engagement, and access must be correct. Distinguish intentional contacts from interferences.

Deliver assembled and exploded models, front/side/top/isometric views, detailed joint sections, full-rotation or sampled interference checks, and an animation if the CAD tool supports it without delaying core deliverables. Keep realistic renders secondary to readable technical views.

Required output structure, adaptable only with an explanation:

```text
radio_telescope/
  README.md
  design_brief.md
  inputs_and_assumptions.md
  parameters.yaml
  cad/                  # native editable source and generation scripts
  exports/              # assembly STEP; individual manufactured part STEP
  print/                # STL/3MF parts, print settings, test coupons
  drawings/             # dimensioned PDFs and wood DXF/SVG templates
  bom/                  # BOM CSV, fasteners, cut list, mesh schedule
  assembly/             # illustrated build, alignment, wiring, service guide
  analysis/             # geometry, loads, RF budgets, validation outputs
  commissioning/        # mechanical and receiver test procedures
  research/             # methods framework, metadata, uncertainty register
  references.md
  CHANGELOG.md
```

Supply print/cut files at real scale with units, revision, datum marks, and a ruler/check dimension. Clearly mark any tiled template or approximated mesh pattern. Assign BOM IDs consistently across CAD, drawings, assembly guide, and filenames.

Run the generator and check successful solid creation, expected part counts, bounding dimensions, valid exported files, fastener lengths, fit allowances, accessible hardware, and principal motion clearances. Reopen exported CAD and inspect representative views if the tools permit. List any operation you could not run. Never report checks as passed merely because code contains them.

## 10. Manufacturing and assembly package

Provide a numbered build sequence from material inspection through commissioning. Include:

- All newly cut wood dimensions, material grades, grain/ply orientation considerations, and sealing of exposed edges.
- Printable-part quantities, orientation, slicer assumptions, support removal, fit coupons, and critical post-processing.
- Exact fastener sizes/lengths, washer/backing arrangements, nut type, pilot/clearance hole sizes, and minimum edge distances justified for the actual materials.
- Hardware stacking diagrams and practical tightening guidance that does not crush wood or plastic; do not invent torque values from unrelated materials.
- Mesh cutting, edge finishing, seam attachment, and controlled fitting/tensioning order.
- Jigs for rib spacing and alignment; checkpoints before irreversible drilling or adhesive curing.
- Feed alignment, mount balancing, cable installation, weather protection, and maintenance inspections.
- A BOM with owned/new status, quantity, material, estimated price in CAD, actual source link, date checked, and alternatives. Label estimates and include consumables and spare hardware. Do not invent supplier availability or buy anything.

## 11. Commissioning and research reproducibility

The research article must distinguish design expectations from measured performance. Do not invent data, successful hydrogen detections, FEA results, calibration accuracy, novelty, or publication claims.

Develop a staged test plan:

1. **Mechanical:** inspect joints; measure dimensions/profile; check motion/stops, balance, locks, deflection, feed position versus elevation, and pointing repeatability. Record before/after loading and any creep or slip.
2. **Receiver bench test:** check voltages and current, gain settings, bias/DC arrangement, clipping/overload, stability, sample drops, and temperature. Use compatible loads and avoid exposing the LNA to excessive test levels.
3. **Interference characterization:** compare terminated input and sky measurements; vary Pi/SSD/network/power configurations and receiver tuning. Do not treat a narrow peak alone as hydrogen evidence.
4. **First sky observation:** use fixed documented gain, warm-up, several integrations, and on/off sky pointings chosen to separate Galactic emission from instrumental bandpass. Explain that reference sky may contain hydrogen too.
5. **Detection validation:** test whether features remain at consistent sky frequencies when LO tuning changes, vary with pointing as expected, and repeat across sessions. Compare with a credible H I survey convolved or interpreted for the approximate beam. Separate RFI rejection and baseline fitting from the raw data.
6. **Calibration and uncertainty:** explain achievable relative calibration first; develop defensible absolute calibration if suitable hot/cold loads or references are available. Do not equate ground temperature to a calibrated antenna temperature without coupling assumptions. Use the radiometer equation for estimates and acknowledge gain drift and correlated channels.
7. **Spectra and velocity:** justify bandwidth, channel width, averaging, spectral window, and baseline treatment. Distinguish topocentric measurements from barycentric/LSR-corrected velocities and document the convention. Never fit away the astronomical line as a baseline.

Record UTC time, observation site, pointing, coordinate/reference frame, hardware revision, feed position, SDR settings, tuning/clock correction, sample rate, FFT/window/channel bandwidth, integration time, calibration method, environmental conditions, software commit, and RFI flags. Retain raw or minimally processed data where practical, derived spectra, processing scripts, and a clear storage budget. Label synthetic test data.

Provide an article methods outline, design-decision table, uncertainty budget, and publication-quality figure plan. Suitable scope is a reproducible low-cost telescope build and measured mechanical/receiver/sky performance; do not assert scientific novelty before a literature review.

## 12. Workflow and completion reporting

Work in stages: input/geometry audit → centre-joint feasibility → complete provisional assembly → structural/RF review → fabrication package → commissioning/research package. Keep a visible checklist and continue all independent work when inputs are missing.

In your first response, give the geometry interpretation, the few unresolved measurements, the chosen CAD route, and the centre-joint risk. Then create the project files and begin work. Do not end after proposing a plan.

When a decision depends on unmeasured hardware or material, make a conservative provisional model and mark the affected outputs **NOT RELEASED FOR FABRICATION**. Ask only for decisions that materially change fit, existing wood, cost, or safety. Resolve routine design choices yourself with rationale.

At completion, provide a deliverable manifest and concise evidence table: requirement, artifact/check, result, and remaining physical verification. Explicitly distinguish **modelled**, **analytically checked**, **simulated**, and **physically tested**. State exactly which dimensions I must confirm before cutting or printing and what to fabricate first for a fit/rigidity trial.

## 13. Starting references to verify and cite

Use primary technical documentation, observatory/university material, measured project reports, and manufacturer drawings. Record exact pages/versions and access dates. Verify current tools/APIs before implementing them. Reference images are not evidence of structural capacity.

- NRAO, Essential Radio Astronomy, Chapter 3: antenna/radiometer fundamentals and reflector surface errors: https://www.cv.nrao.edu/~sransom/web/Ch3.html
- NRAO, Essential Radio Astronomy, Chapter 7: spectral lines and the H I transition: https://www.cv.nrao.edu/~sransom/web/Ch7.html
- WVU RAIL / Green Bank DSPIRA hardware and receiver resources; these include horn telescopes, so adapt only applicable principles: https://rail.wvu.edu/dspira/hardware/
- DSPIRA LNA placement and options: https://dspira-lessons.github.io/LNA
- Nooelec SAWbird+ H1 manufacturer page, only if this is the actual module: https://www.nooelec.com/store/sdr/sdr-addons/sawbird/sawbird-h1.html
- Raspberry Pi 5 official drawings and product documents: https://pip.raspberrypi.com/categories/892-raspberry-pi-5
- Raspberry Pi official hardware/power documentation: https://www.raspberrypi.com/documentation/computers/raspberry-pi.html

These are starting references, not substitutes for the actual rib CAD, measured material properties, exact receiver datasheets, or physical validation.

---

End of prompt.
