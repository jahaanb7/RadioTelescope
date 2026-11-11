# Graph Report - RadioTelescope  (2026-11-10)

## Corpus Check
- 5 files · ~31,617 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 82 file(s) not represented in the graph (top: .step 41, .stl 28, .csv 6)
- WARNING: 82 of 146 files seen (56%) have no supported extractor and are missing from this graph entirely. It may look complete while representing only part of the codebase.

## Summary
- 612 nodes · 889 edges · 48 communities (46 shown, 2 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7aac66ac`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- rib
- tolerances
- feed_can
- mount
- build_dish
- build_ribs.py
- petg
- softwood
- hub_disc_radius
- parameters.yaml
- loads
- lazy_susan
- feed_support
- electronics
- battens
- printer
- Frame
- telescope_joints.py
- dish
- brace_offset
- rib_support
- elevation_range
- flange_r_range
- flange_thickness
- hub_floor
- hub_ring
- hub_wall
- keeper_bolt_radius
- keeper_ring
- lock_radius
- rim_chord_height
- rim_diagonal_width
- rim_panel_radial
- sector_thickness
- spacer_flange_r
- spacer_section
- trunnion_block
- feed_socket_depth
- foot_node_bottom
- foot_radius
- ground_leg_angles
- pivot_clearance
- plate_disc_diameter
- plate_disc_thickness
- socket_bolts_from_mouth
- socket_depth
- socket_floor
- socket_wall

## God Nodes (most connected - your core abstractions)
1. `build_dish()` - 28 edges
2. `build_mount()` - 21 edges
3. `export_all()` - 21 edges
4. `dish` - 19 edges
5. `main()` - 18 edges
6. `rim_panel()` - 16 edges
7. `hub()` - 15 edges
8. `hole()` - 14 edges
9. `mount` - 14 edges
10. `bolt()` - 13 edges

## Surprising Connections (you probably didn't know these)
- `run()` --calls--> `math`  [EXTRACTED]
  cad/fusion/telescope_joints/telescope_joints.py →   _Bridges community 17 → community 4_
- `rotation_to_down()` --calls--> `numpy`  [EXTRACTED]
  cad/print_prep.py →   _Bridges community 5 → community 4_

## Import Cycles
- None detected.

## Communities (48 total, 2 thin omitted)

### Community 0 - "rib"
Cohesion: 0.04
Nodes (45): source, status, value, source, status, value, source, status (+37 more)

### Community 1 - "tolerances"
Cohesion: 0.05
Nodes (41): source, status, value, source, status, value, source, status (+33 more)

### Community 2 - "feed_can"
Cohesion: 0.08
Nodes (25): source, status, value, source, status, value, source, status (+17 more)

### Community 3 - "mount"
Cohesion: 0.40
Nodes (5): source, status, value, mount, arm_half_spread

### Community 4 - "build_dish"
Cohesion: 0.06
Nodes (59): add(), analyse(), lumped(), bar(), bay_wedge(), bb_overlap(), bolt(), build_dish() (+51 more)

### Community 5 - "build_ribs.py"
Cohesion: 0.10
Nodes (16): array(), build_outline_rib(), extrude_profile(), load_params(), main(), pair_overlaps(), parabola(), stl_stats() (+8 more)

### Community 6 - "petg"
Cohesion: 0.05
Nodes (37): source, status, value, source, status, value, source, status (+29 more)

### Community 7 - "softwood"
Cohesion: 0.10
Nodes (23): source, status, value, source, status, value, source, status (+15 more)

### Community 8 - "hub_disc_radius"
Cohesion: 0.50
Nodes (4): hub_disc_radius, source, status, value

### Community 9 - "parameters.yaml"
Cohesion: 0.05
Nodes (43): source, status, value, source, status, value, source, status (+35 more)

### Community 10 - "loads"
Cohesion: 0.10
Nodes (21): source, status, value, source, status, value, source, status (+13 more)

### Community 11 - "lazy_susan"
Cohesion: 0.10
Nodes (21): lazy_susan, plate_thickness, recess_clearance, ring_mean_radius, size, thickness, source, status (+13 more)

### Community 12 - "feed_support"
Cohesion: 0.12
Nodes (17): source, status, value, source, status, value, source, status (+9 more)

### Community 13 - "electronics"
Cohesion: 0.12
Nodes (17): source, status, value, source, status, value, electronics, ebox_mass (+9 more)

### Community 14 - "battens"
Cohesion: 0.15
Nodes (13): battens, beam_section, feed_leg_section, section, source, status, value, source (+5 more)

### Community 15 - "printer"
Cohesion: 0.15
Nodes (13): source, status, value, source, status, value, source, status (+5 more)

### Community 18 - "dish"
Cohesion: 0.40
Nodes (5): source, status, value, dish, anchor_rib_angles

### Community 19 - "brace_offset"
Cohesion: 0.50
Nodes (4): source, status, value, brace_offset

### Community 20 - "rib_support"
Cohesion: 0.15
Nodes (13): source, status, value, rib_support, fillet_radius, slot_lead_in, spacer_radius, source (+5 more)

### Community 22 - "elevation_range"
Cohesion: 0.50
Nodes (4): elevation_range, source, status, value

### Community 23 - "flange_r_range"
Cohesion: 0.50
Nodes (4): flange_r_range, source, status, value

### Community 24 - "flange_thickness"
Cohesion: 0.50
Nodes (4): flange_thickness, source, status, value

### Community 25 - "hub_floor"
Cohesion: 0.50
Nodes (4): hub_floor, source, status, value

### Community 26 - "hub_ring"
Cohesion: 0.50
Nodes (4): hub_ring, source, status, value

### Community 27 - "hub_wall"
Cohesion: 0.50
Nodes (4): hub_wall, source, status, value

### Community 28 - "keeper_bolt_radius"
Cohesion: 0.50
Nodes (4): keeper_bolt_radius, source, status, value

### Community 29 - "keeper_ring"
Cohesion: 0.50
Nodes (4): keeper_ring, source, status, value

### Community 30 - "lock_radius"
Cohesion: 0.50
Nodes (4): lock_radius, source, status, value

### Community 31 - "rim_chord_height"
Cohesion: 0.50
Nodes (4): rim_chord_height, source, status, value

### Community 32 - "rim_diagonal_width"
Cohesion: 0.50
Nodes (4): rim_diagonal_width, source, status, value

### Community 33 - "rim_panel_radial"
Cohesion: 0.50
Nodes (4): rim_panel_radial, source, status, value

### Community 34 - "sector_thickness"
Cohesion: 0.50
Nodes (4): sector_thickness, source, status, value

### Community 35 - "spacer_flange_r"
Cohesion: 0.50
Nodes (4): spacer_flange_r, source, status, value

### Community 36 - "spacer_section"
Cohesion: 0.50
Nodes (4): spacer_section, source, status, value

### Community 37 - "trunnion_block"
Cohesion: 0.50
Nodes (4): trunnion_block, source, status, value

### Community 39 - "feed_socket_depth"
Cohesion: 0.50
Nodes (4): source, status, value, feed_socket_depth

### Community 41 - "foot_node_bottom"
Cohesion: 0.50
Nodes (4): source, status, value, foot_node_bottom

### Community 42 - "foot_radius"
Cohesion: 0.50
Nodes (4): source, status, value, foot_radius

### Community 43 - "ground_leg_angles"
Cohesion: 0.50
Nodes (4): source, status, value, ground_leg_angles

### Community 47 - "pivot_clearance"
Cohesion: 0.50
Nodes (4): pivot_clearance, source, status, value

### Community 48 - "plate_disc_diameter"
Cohesion: 0.50
Nodes (4): plate_disc_diameter, source, status, value

### Community 49 - "plate_disc_thickness"
Cohesion: 0.50
Nodes (4): plate_disc_thickness, source, status, value

### Community 50 - "socket_bolts_from_mouth"
Cohesion: 0.50
Nodes (4): socket_bolts_from_mouth, source, status, value

### Community 51 - "socket_depth"
Cohesion: 0.50
Nodes (4): socket_depth, source, status, value

### Community 52 - "socket_floor"
Cohesion: 0.50
Nodes (4): socket_floor, source, status, value

### Community 53 - "socket_wall"
Cohesion: 0.50
Nodes (4): socket_wall, source, status, value

## Knowledge Gaps
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `dish` connect `dish` to `rim_diagonal_width`, `rim_panel_radial`, `sector_thickness`, `spacer_flange_r`, `spacer_section`, `trunnion_block`, `hub_disc_radius`, `parameters.yaml`, `elevation_range`, `flange_r_range`, `flange_thickness`, `hub_floor`, `hub_ring`, `hub_wall`, `keeper_bolt_radius`, `keeper_ring`, `lock_radius`, `rim_chord_height`?**
  _High betweenness centrality (0.161) - this node is a cross-community bridge._
- **Should `rib` be split into smaller, more focused modules?**
  _Cohesion score 0.044444444444444446 - nodes in this community are weakly interconnected._
- **Why does `mount` connect `mount` to `feed_socket_depth`, `parameters.yaml`, `foot_radius`, `foot_node_bottom`, `ground_leg_angles`, `pivot_clearance`, `plate_disc_diameter`, `plate_disc_thickness`, `socket_bolts_from_mouth`, `brace_offset`, `socket_depth`, `socket_floor`, `socket_wall`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Should `tolerances` be split into smaller, more focused modules?**
  _Cohesion score 0.04878048780487805 - nodes in this community are weakly interconnected._
- **Why does `rib` connect `rib` to `parameters.yaml`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Should `feed_can` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `build_dish` be split into smaller, more focused modules?**
  _Cohesion score 0.05678346810422282 - nodes in this community are weakly interconnected._