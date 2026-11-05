# PolyFEMBlenderPlugin: PolyFEM simulations from a Blender scene

> Blender 4.2 add-on that exports meshes and physics settings to a PolyFEM JSON file, runs PolyFEM through Docker and imports the results.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/polyfemblenderplugin/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/polyfemblenderplugin/index.md
- Published: 2026-11-05
- Updated: 2026-11-05
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/ETSim/PolyFEMBlenderPlugin


## Use cases

Blender add-on that turns a scene into a PolyFEM JSON setup and runs the simulation from Blender.

- **Assign FEM materials** (Simulation user): The Apply Material operator stores Young's modulus, Poisson's ratio and density on the selected objects from a preset list such as Steel or Aluminum.
- **Create PolyFEM JSON** (Simulation user): Create PolyFEM JSON exports each mesh and writes geometry, materials, contact, time, boundary-condition, solver and output blocks to one JSON file.
- **Tetrahedralize with TetWild** (Simulation user, Docker images): With the MSH export type, the object is written as STL and converted to .msh by the yixinhu/tetwild image or a local TetWild executable.
- **Run the simulation** (Simulation user, Docker images, PolyFEM solver): Run PolyFem Simulation calls docker run antoinebou12/polyfem --json with the project folder mounted on /data, or a local PolyFEM executable, in a background thread.
- **Import results as animation** (Simulation user, PolyFEM solver): Render Animation reads step_*.vtu files, adds the solution displacement, converts each step to OBJ with meshio and keyframes its visibility.
- **Pull solver images** (Simulation user, Docker images): The Pull Docker Image buttons check that Docker is installed and run docker pull for the configured TetWild or PolyFEM image.

### Scenario: Simulate a contact scene and play it back in Blender

1. Install the zipped polyfem folder through Edit > Preferences > Add-ons and enable PolyFem.
2. In Properties > Physics > PolyFEM, choose Docker execution and pull antoinebou12/polyfem and yixinhu/tetwild.
3. Select the meshes, apply a material preset and set contact, time step and end time.
4. Click Create JSON Configuration to write the meshes and the JSON file to the export path.
5. Click Run PolyFem Simulation, then Render Animation to import the step_*.vtu results as keyframed meshes.


