# TrueMapData: height maps for metrology and graphics

> TrueMapData reads TrueMap and GelSight height maps, processes them and exports visual, surface and mesh-oriented results.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/truemapdata/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/truemapdata/index.md
- Published: 2026-10-24
- Updated: 2026-11-06
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/ETSim/TrueMapData
- Inspected revision: 8e44bd4e57ad46eba45c46c997bd6b51d7622956


## Use cases

Python library and tmd-process CLI that read TrueMap and GelSight .tmd height maps for metrology, wear and 3D export.

- **Load a .tmd height map** (Tribology researcher, TrueMap / GelSight): TMD.load("file.tmd") in tmd/core/tmd.py decodes v1 or v2 headers and returns height_map as a float32 (height, width) array plus a metadata dict.
- **Export texture maps** (Tribology researcher): tmd-process maps all|normal|ao|bump|hillshade|displacement writes PNG maps through the generators in tmd/image/maps/, and maps batch processes a whole folder.
- **Export a 3D mesh** (Tribology researcher): tmd-process mesh generate exports STL, OBJ, PLY, glTF or USD with adaptive or quadtree triangulation; mesh apply puts the maps on a template OBJ/MTL such as tmd/fixtures/templates/plane.
- **Measure ISO 25178 roughness** (Tribology researcher, Surfalize (ISO 25178)): tmd-process roughness file <path> --quick computes areal parameters through the optional truemapdata[roughness] extra, which installs Surfalize under GPL-3.0.
- **Track wear across scans** (Tribology researcher, TrueMap / GelSight): tmd-wear (same as tmd-process wear) computes bearing curves, wear-volume series, slip axis and scratch evolution on aligned sequences, using tmd/sequence/wear_analysis.py.
- **Plot surfaces and profiles** (Tribology researcher): tmd-process visualize basic <file> draws 2D heatmaps, 3D surfaces and X/Y profiles with the matplotlib, plotly, seaborn or optional Polyscope plotters; tribology plot writes a PNG dashboard.

### Scenario: Compare two GelSight captures of a worn sample

1. Install the package with pip install truemapdata, or pip install -e . from a clone.
2. Run tmd-wear bearing curve examples/gelsight/circle_0mm_100g_heightmap_linear_detrend.tmd --json to get the Abbott curve of the first capture.
3. Run tmd-wear volume-series with that file and tests/fixtures/gelsight_wear_volume_second_frame.tmd to measure the volume lost between frames.
4. Export textures with tmd-process maps all <file> -o ./maps_out.
5. Build a mesh with tmd-process mesh generate <file> --format stl --method adaptive --quality high for a 3D view of the worn area.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Jupyter Notebook | 94.36 |
| Python | 5.64 |

## Getting started (repository commands, not run here)

### README.md · Installation

```bash
pip install truemapdata
```

### README.md · Installation

```bash
pip install "truemapdata[mesh,viz,advanced]"
pip install "truemapdata[roughness]"   # Surfalize (GPL-3.0); Python 3.10+ only
```

### README.md · Installation

```bash
pip install -r requirements.txt
pip install -e .
```



