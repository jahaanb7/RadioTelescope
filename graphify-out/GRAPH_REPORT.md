# Graph Report - RadioTelescope  (2026-11-10)

## Corpus Check
- 4 files · ~25,707 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 83 file(s) not represented in the graph (top: .step 42, .stl 29, .csv 5)
- WARNING: 83 of 102 files seen (81%) have no supported extractor and are missing from this graph entirely. It may look complete while representing only part of the codebase.

## Summary
- 604 nodes · 867 edges · 62 communities (60 shown, 2 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `84b25770`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- rib
- tolerances
- feed_can
- mount
- build_dish
- build.py
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
- count
- depth_d
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
- drill_clearance
- feed_socket_depth
- focal_length_f
- foot_node_bottom
- foot_radius
- ground_leg_angles
- material
- mid_hole_radius
- mid_hole_z
- pivot_clearance
- plate_disc_diameter
- plate_disc_thickness
- socket_bolts_from_mouth
- socket_depth
- socket_floor
- socket_wall
- outline_line_width
- profile_shape
- radius_R
- reference_stl
- rim_hole_radius
- rim_hole_z
- thickness_board
- tip_relief_radius

## God Nodes (most connected - your core abstractions)
1. `build_dish()` - 26 edges
2. `build_mount()` - 21 edges
3. `export_all()` - 21 edges
4. `dish` - 19 edges
5. `main()` - 18 edges
6. `hole()` - 17 edges
7. `rib` - 17 edges
8. `hub()` - 15 edges
9. `rim_panel()` - 14 edges
10. `mount` - 14 edges

## Surprising Connections (you probably didn't know these)
- `export_all()` --calls--> `zpar()`  [EXTRACTED]
  cad/build.py → cad/build.py  _Bridges community 4 → community 5_
- `run()` --calls--> `math`  [EXTRACTED]
  cad/fusion/telescope_joints/telescope_joints.py →   _Bridges community 17 → community 4_

## Import Cycles
- None detected.

## Communities (62 total, 2 thin omitted)

### Community 0 - "rib"
Cohesion: 0.40
Nodes (5): source, status, value, rib, body_style

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
Cohesion: 0.09
Nodes (31): add(), bar(), bay_wedge(), bolt(), build_dish(), build_mount(), bx(), collar() (+23 more)

### Community 5 - "build.py"
Cohesion: 0.07
Nodes (36): analyse(), lumped(), bb_overlap(), dish_drop(), dish_points(), export_all(), scene(), stage_assy() (+28 more)

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

### Community 20 - "count"
Cohesion: 0.50
Nodes (4): source, status, value, count

### Community 21 - "depth_d"
Cohesion: 0.50
Nodes (4): source, status, value, depth_d

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

### Community 38 - "drill_clearance"
Cohesion: 0.50
Nodes (4): source, status, value, drill_clearance

### Community 39 - "feed_socket_depth"
Cohesion: 0.50
Nodes (4): source, status, value, feed_socket_depth

### Community 40 - "focal_length_f"
Cohesion: 0.50
Nodes (4): source, status, value, focal_length_f

### Community 41 - "foot_node_bottom"
Cohesion: 0.50
Nodes (4): source, status, value, foot_node_bottom

### Community 42 - "foot_radius"
Cohesion: 0.50
Nodes (4): source, status, value, foot_radius

### Community 43 - "ground_leg_angles"
Cohesion: 0.50
Nodes (4): source, status, value, ground_leg_angles

### Community 44 - "material"
Cohesion: 0.50
Nodes (4): source, status, value, material

### Community 45 - "mid_hole_radius"
Cohesion: 0.50
Nodes (4): source, status, value, mid_hole_radius

### Community 46 - "mid_hole_z"
Cohesion: 0.50
Nodes (4): source, status, value, mid_hole_z

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

### Community 54 - "outline_line_width"
Cohesion: 0.50
Nodes (4): source, status, value, outline_line_width

### Community 55 - "profile_shape"
Cohesion: 0.50
Nodes (4): source, status, value, profile_shape

### Community 56 - "radius_R"
Cohesion: 0.50
Nodes (4): source, status, value, radius_R

### Community 57 - "reference_stl"
Cohesion: 0.50
Nodes (4): source, status, value, reference_stl

### Community 58 - "rim_hole_radius"
Cohesion: 0.50
Nodes (4): rim_hole_radius, source, status, value

### Community 59 - "rim_hole_z"
Cohesion: 0.50
Nodes (4): rim_hole_z, source, status, value

### Community 60 - "thickness_board"
Cohesion: 0.50
Nodes (4): thickness_board, source, status, value

### Community 61 - "tip_relief_radius"
Cohesion: 0.50
Nodes (4): tip_relief_radius, source, status, value

## Knowledge Gaps
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `dish` connect `dish` to `rim_diagonal_width`, `rim_panel_radial`, `sector_thickness`, `spacer_flange_r`, `spacer_section`, `trunnion_block`, `hub_disc_radius`, `parameters.yaml`, `elevation_range`, `flange_r_range`, `flange_thickness`, `hub_floor`, `hub_ring`, `hub_wall`, `keeper_bolt_radius`, `keeper_ring`, `lock_radius`, `rim_chord_height`?**
  _High betweenness centrality (0.168) - this node is a cross-community bridge._
- **Should `tolerances` be split into smaller, more focused modules?**
  _Cohesion score 0.04878048780487805 - nodes in this community are weakly interconnected._
- **Why does `rib` connect `rib` to `drill_clearance`, `focal_length_f`, `parameters.yaml`, `material`, `mid_hole_radius`, `mid_hole_z`, `count`, `depth_d`, `outline_line_width`, `profile_shape`, `radius_R`, `reference_stl`, `rim_hole_radius`, `rim_hole_z`, `thickness_board`, `tip_relief_radius`?**
  _High betweenness centrality (0.151) - this node is a cross-community bridge._
- **Should `feed_can` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Why does `mount` connect `mount` to `feed_socket_depth`, `parameters.yaml`, `foot_radius`, `foot_node_bottom`, `ground_leg_angles`, `pivot_clearance`, `plate_disc_diameter`, `plate_disc_thickness`, `socket_bolts_from_mouth`, `brace_offset`, `socket_depth`, `socket_floor`, `socket_wall`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Should `build_dish` be split into smaller, more focused modules?**
  _Cohesion score 0.09096045197740113 - nodes in this community are weakly interconnected._
- **Should `build.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06778846153846153 - nodes in this community are weakly interconnected._