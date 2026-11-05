# WearMachine: CAD files for a GelSight wear bench

> STEP, STL, DXF and drawing files for a small sliding-wear rig: rail, pusher, weight holders and GelSight sample holders.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/wearmachine/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/wearmachine/index.md
- Published: 2026-11-05
- Updated: 2026-11-05
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/ETSim/WearMachine


## Use cases

CAD, print and drawing files for a small sliding-wear bench whose samples are scanned with a GelSight sensor.

- **Print the bench parts** (Bench builder, 3D printer or cutter): Print/ holds STL files for the rail, rail holder, ski, pusher, separator, bearing holder, motor bracket, lead-screw nut, sample holders and weight holders.
- **Modify parts in CAD** (Bench builder): Raw/ keeps STEP solids of the sample holders, rail parts and most weight holders so dimensions can be changed before printing.
- **Cut flat parts from DXF** (Bench builder, 3D printer or cutter): Drawing/ provides DXF outlines, including a Base plate that exists only as DXF, plus an Inkscape A4 sheet with 16 holes for a mold.
- **Set the normal load** (Bench builder): Weight Holder parts come in 10, 20, 50, 100, 200, 500 and 1000 g versions to press the sample with a chosen load.
- **Hold samples under GelSight** (Bench builder, GelSight scanner): The 30 mm and 40 mm sample holders and a square benchtop holder position worn samples for GelSight capture, as the README describes.

### Scenario: Build the bench and run a loaded sliding test

1. Open Picture/Assembly.png to see the frame with two rails and the crossbar holding five sample holes.
2. Print Rail, Rail_Holder, Rail_Ski, Pusher, Seperator, Holder Berring, nema17bracket_v2 and t8_nut from Print/Rail/.
3. Cut the Base plate from Drawing/Rail/Base.dxf and assemble the rail with a NEMA 17 motor and T8 lead screw.
4. Print the weight holder for the target load, for example Weight Holder 200g.stl, and place it on the sample.
5. After each sliding distance, move the sample to the 30 mm or 40 mm holder and scan it with the GelSight.


