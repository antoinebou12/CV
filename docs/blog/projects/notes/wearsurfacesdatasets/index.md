# WearSurfacesDatasets: measured wear-surface sequences

> GelSight surface maps of materials worn under controlled grit, load and distance, packed as Parquet and WebDataset, with alignment tools and a WebGPU viewer.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/wearsurfacesdatasets/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/wearsurfacesdatasets/index.md
- Published: 2026-11-05
- Updated: 2026-11-05
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/ETSim/WearSurfacesDatasets
- Inspected revision: 6841dff6be997b20c0ec288fd1f2f36a9d8bd8fe


## Use cases

Measured wear-surface map sequences (material, grit, load, distance) with Python tools and a WebGPU viewer.

- **Download the map sequences** (Graphics researcher, Git LFS storage): Parquet leaves and WebDataset shards are Git LFS objects, so git lfs pull replaces the pointers under data/parquet and data/shards.
- **Scrub a wear timeline** (Graphics researcher, WebGPU browser): docs/serve_local.py serves docs/index.html, which reads Parquet with parquet-wasm and renders the maps with WebGPU while the user scrubs distance or presses Play.
- **Align a sequence** (Graphics researcher, WebGPU browser): POST /api/align/sequence runs a two-pass SIFT/ECC registration of the normal maps to frame 0, crops the common region and caches PNGs in data/aligned.
- **Interpolate and extrapolate** (Graphics researcher): python -m alignment.bake adds Catmull-Rom midpoints and FFT plus SLERP extrapolated normal maps after the last measured step.
- **Pack Parquet and shards** (Graphics researcher): generate_datasets.py parquet and webdataset turn a wear/ tree of PNG maps into nested Parquet leaves and shard-*.tar files.
- **Extract maps as PNG** (Graphics researcher): read_datasets.py decompress and generate_datasets.py extract write the JPEG bytes stored per map_type back to image files.

### Scenario: Inspect cardboard wear under 200 g

1. Clone the repository, run git lfs pull and pip install -r requirements.txt.
2. Start python docs/serve_local.py and open http://127.0.0.1:8080/docs/index.html.
3. Pick Cartboard / Raw / Normal · S60 · 200 g and click Load sequence.
4. Click Align sequence, then scrub the distance from 0 mm to 2400 mm or press Play.
5. Run python -m alignment.bake --sequence-id cartboard-raw-normal-s60-200g --pack to add interpolated and extrapolated steps.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Python | 100 |

## Getting started (repository commands, not run here)

### README.md · Quick start — WebGPU wear viewer

```bash
git clone https://github.com/ETSim/WearSurfacesDatasets
cd WearSurfacesDatasets
git lfs pull
pip install -r requirements.txt
python docs/serve_local.py
```

### README.md · Quick start — WebGPU wear viewer

```bash
python -m alignment.bake --sequence-id cartboard-raw-normal-s60-200g --pack
python -m alignment.bake --all --pack
python -m alignment.bake_extrapolate_all
```

### README.md · Quick start — WebGPU wear viewer

```bash
python docs/prepare_viewer_parquets.py --source data/parquet --dest data/parquet
```

### README.md · Install (Python pipeline)

```bash
pip install -r requirements.txt
```

### data/parquet/README.md · Sync / rebuild sequences

```bash
python docs/prepare_viewer_parquets.py --source data/parquet --dest data/parquet
```



