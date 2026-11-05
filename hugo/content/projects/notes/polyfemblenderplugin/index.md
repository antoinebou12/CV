---
title: "PolyFEMBlenderPlugin: PolyFEM simulations from a Blender scene"
date: 2026-11-05T12:00:00-05:00
description: "Blender 4.2 add-on that exports meshes and physics settings to a PolyFEM JSON file, runs PolyFEM through Docker and imports the results."
translationKey: repository-note-polyfemblenderplugin
repository_note: "PolyFEMBlenderPlugin"
---

# PolyFEMBlenderPlugin

<div class="repo-status-row"><span class="repo-badge kind">Blender add-on</span><span class="repo-badge docker">Docker</span></div>

<div class="repo-tech-badges"><span class="tag tool">Python</span><span class="tag tool">Blender 4.2</span><span class="tag tool">PolyFEM</span><span class="tag tool">TetWild</span><span class="tag tool">meshio</span><span class="tag tool">GitHub Actions</span></div>

PolyFEMBlenderPlugin is an experimental Blender extension that turns selected objects, materials and contact settings into a [PolyFEM](https://polyfem.github.io/) JSON setup and runs the finite-element simulation without leaving Blender. It was written for the ÉTS lab's simulation work and is published under [ETSim](https://github.com/ETSim), for people who prepare scenes in Blender but solve them with PolyFEM.

## Overview {#overview}

`polyfem/__init__.py` registers one panel, the property groups and the operators. On registration it also installs `meshio` with pip into Blender's user modules folder.

- `polyfem/panels/polyfem_json.py` draws the **PolyFEM** panel in the Physics tab of the Properties editor: execution mode (Docker or executable) for PolyFEM and TetWild, the selected objects with their materials and export format, then collapsible sections for export, contact, time, space, boundary conditions, materials, solver and output settings.
- `polyfem/operators/create_polyfem_json.py` exports each mesh (STL, OBJ, or MSH through TetWild) and writes the PolyFEM JSON file with `geometry`, `materials`, `contact`, `time`, `boundary_conditions`, `solver` and `output` blocks.
- `polyfem/operators/run_polyfem.py` starts PolyFEM in a background thread, either `docker run antoinebou12/polyfem --json /data/<file>` with the project folder mounted on `/data`, or a local executable. Its **Render Animation** operator reads the `step_*.vtu` results, adds the `solution` displacement, converts each step to OBJ with meshio and keyframes the visibility of each imported mesh.
- `polyfem/properties/polyfem.py` holds the settings, including material presets (steel, copper, aluminium and others), integrators (implicit Euler, explicit Euler, implicit Newmark) and Eigen linear solvers.

## Getting started {#installation}

The README installs the add-on from a zip of the `polyfem/` folder: **Edit > Preferences > Add-ons > Install**, then enable **PolyFem**. Blender 4.2 or later is required by `blender_manifest.toml`. The default execution mode uses Docker:

```bash
docker pull yixinhu/tetwild:latest
docker pull antoinebou12/polyfem:latest
```

The CI workflow builds the extension package with Blender's own command:

```bash
blender --command extension build --source-dir polyfem --output-dir docs
blender --command extension server-generate --repo-dir=docs --html
```

## Repository guide {#reader-guide}

- `polyfem/` is the extension itself (`blender_manifest.toml`, `__init__.py`, `operators/`, `panels/`, `properties/`).
- `polyfem/operators/create_polyfem_json.py` handles mesh export, TetWild, materials, Docker image pulls and the JSON file.
- `polyfem/operators/run_polyfem.py` runs PolyFEM, imports results, opens the PolyFEM documentation and clears the cache.
- `polyfem/properties/polyfem.py` defines every panel field and preset.
- `.github/workflows/build.yml` builds the extension zip and an extension repository index (`docs/index.json`), then deploys `docs/` to the `gh-pages` branch.
- `docs/` holds built packages `polyfem-1.0.10.zip` and `polyfem-1.0.11.zip` with their index.
- `zip-plugin.py` and `download-wheels.py` are helper scripts to zip the add-on and download wheels for meshio, trimesh and tetgen.

## Features {#features}

- Assign elastic material properties (E, ν, ρ) to objects from presets or custom values.
- Export meshes to STL or OBJ, or tetrahedralize them to MSH with TetWild in Docker or as a local executable.
- Set contact (`dhat`, friction coefficient, `epsv`), time integration, boundary-condition method and right-hand side, linear solver and ParaView output options.
- Write a complete PolyFEM JSON file, with optional export of selected objects only.
- Run PolyFEM through Docker or a local executable without blocking the Blender interface.
- Import VTU time steps back as a keyframed mesh sequence.

## Limits {#limits}

- The README calls the add-on experimental and lists crashes with complex geometry and mesh-export edge cases as known issues.
- The panel is registered in the Properties editor's Physics tab, while the README describes a 3D Viewport sidebar tab.
- FBX and glTF appear in the export menu but the operator rejects them.
- `blender_manifest.toml` lists only `windows-x64` as a platform, and the add-on needs Docker or local PolyFEM and TetWild builds.
- The README states GPL-3.0, while `LICENSE` and the manifest state MIT.
- The README badges and file tree refer to an older repository name and to a `panels/poly_fem.py` file that is not in the tree.
- There are no tests. The workflow only builds and publishes the package.

## Sources {#sources}

- [GitHub repository](https://github.com/ETSim/PolyFEMBlenderPlugin)
- [README](https://github.com/ETSim/PolyFEMBlenderPlugin/blob/main/README.md)
- [`polyfem/blender_manifest.toml`](https://github.com/ETSim/PolyFEMBlenderPlugin/blob/main/polyfem/blender_manifest.toml)
- [`polyfem/operators/create_polyfem_json.py`](https://github.com/ETSim/PolyFEMBlenderPlugin/blob/main/polyfem/operators/create_polyfem_json.py)
- [`polyfem/operators/run_polyfem.py`](https://github.com/ETSim/PolyFEMBlenderPlugin/blob/main/polyfem/operators/run_polyfem.py)
- [`.github/workflows/build.yml`](https://github.com/ETSim/PolyFEMBlenderPlugin/blob/main/.github/workflows/build.yml)
