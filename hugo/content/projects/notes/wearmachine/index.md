---
title: "WearMachine: CAD files for a GelSight wear bench"
date: 2026-11-05T12:00:00-05:00
description: "STEP, STL, DXF and drawing files for a small sliding-wear rig: rail, pusher, weight holders and GelSight sample holders."
translationKey: repository-note-wearmachine
repository_note: "WearMachine"
---

# WearMachine

<div class="repo-status-row"><span class="repo-badge kind">Hardware / CAD</span></div>

<div class="repo-tech-badges"><span class="tag tool">STEP</span><span class="tag tool">STL</span><span class="tag tool">DXF</span><span class="tag tool">Inkscape SVG</span></div>

WearMachine collects the parts of the abrasion bench used in the [ÉTS master's research on wear in texture space]({{< ref "/posts/thesis-wear-texture-space/index.md" >}}): a sample slides on a rail under a chosen load, then is scanned with a GelSight sensor. The repository, published under [ETSim](https://github.com/ETSim), is for anyone who wants to rebuild or adapt the rig to evaluate wear, study friction or check simulations against measurements.

## Overview {#overview}

The README states the goal and the components: a GelSight bench, custom fixtures (the CAD files in the repository), load sensors, linear actuators and a control and acquisition system. Only the fixtures are in the repository. They are organised in three part families, each available in up to four formats:

- **Rail**: `Rail`, `Rail_Holder`, `Rail_Ski`, `Pusher`, `Seperator`, `Holder Berring`, plus a `Base` plate drawing, a `nema17bracket_v2` motor bracket and a `t8_nut` lead-screw nut. The names point to a stepper motor and lead screw moving the sample along the rail.
- **Weight**: `Weight Holder` parts for 10, 20, 50, 100, 200, 500 and 1000 g that set the normal load on the sample.
- **Gelsight_Holder**: `30mm Sample Holder`, `40mm Sample Holder` and `Benchtop Holder Square` to hold samples under the GelSight sensor.

`Picture/Assembly.png` is a 1:8 drawing sheet, dated March 2025, of the assembled frame: two rails and a crossbar with five sample holes of increasing size. `Drawing/Mold/20240430_16_Holes.svg` is an A4 Inkscape sheet with a 16-hole mold layout.

## Getting started {#installation}

There is nothing to run. Pick the folder that matches what you want to do:

- open the STEP files in `Raw/` with a CAD tool (FreeCAD, Fusion, SolidWorks…) to change dimensions;
- slice the STL files in `Print/` for 3D printing;
- use the DXF files in `Drawing/` for flat outlines or laser cutting, and the PNG sheets in `Picture/` as visual references.

```bash
git clone https://github.com/ETSim/WearMachine
ls WearMachine/Print/Rail WearMachine/Print/Weight WearMachine/Print/Gelsight_Holder
```

## Repository guide {#reader-guide}

- `Raw/` holds STEP solids for the GelSight holders, the rail parts and most weight holders.
- `Print/` holds STL meshes for printing, including the motor bracket and the T8 nut.
- `Drawing/` holds DXF outlines for the two round GelSight holders, the rail parts (including `Base.dxf`) and all weight holders, plus the mold SVG.
- `Picture/` holds PNG drawing sheets of individual parts and `Assembly.png`.
- `README.md` gives the purpose and the list of required components.

## Features {#features}

- Complete set of printable fixtures for a rail-guided sliding test.
- Seven weight holders from 10 g to 1000 g for repeatable normal loads.
- Two round sample holders (30 mm and 40 mm) and a square benchtop holder for GelSight capture.
- Editable STEP sources next to ready-to-print STL files.
- Measured surfaces from this kind of test are published in [WearSurfacesDatasets]({{< ref "/projects/notes/wearsurfacesdatasets/index.md" >}}), whose loads range from 10 to 200 g.

## Limits {#limits}

- The README says the repository provides detailed build instructions, but it contains no assembly steps, bill of materials or hardware list beyond the component names.
- No firmware, wiring or control software is included for the actuators, load sensors or acquisition system the README lists.
- Formats are uneven: `Base` exists only as DXF, `Holder Berring` and `Weight Holder 10g` have no STEP file, and the motor bracket and nut have no STEP or drawing.
- The drawing sheets have empty title, material and tolerance fields.
- The repository has a Python `.gitignore` but no code.

## Sources {#sources}

- [GitHub repository](https://github.com/ETSim/WearMachine)
- [README](https://github.com/ETSim/WearMachine/blob/main/README.md)
- [`Picture/Assembly.png`](https://github.com/ETSim/WearMachine/blob/main/Picture/Assembly.png)
- [`Raw/Rail/Rail.step`](https://github.com/ETSim/WearMachine/blob/main/Raw/Rail/Rail.step)
- [`Print/Rail/nema17bracket_v2.stl`](https://github.com/ETSim/WearMachine/blob/main/Print/Rail/nema17bracket_v2.stl)
- [`Drawing/Weight/Weight Holder 200g.dxf`](https://github.com/ETSim/WearMachine/blob/main/Drawing/Weight/Weight%20Holder%20200g.dxf)
