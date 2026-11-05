# WearSurfacesDatasets: measured wear-surface sequences

> GelSight surface maps of materials worn under controlled grit, load and distance, packed as Parquet and WebDataset, with alignment tools and a WebGPU viewer.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/wearsurfacesdatasets/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/wearsurfacesdatasets/index.md
- Published: 2026-11-05
- Updated: 2026-11-05
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/ETSim/WearSurfacesDatasets


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


