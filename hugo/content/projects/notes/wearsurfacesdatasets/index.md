---
title: "WearSurfacesDatasets: measured wear-surface sequences"
date: 2026-11-05T12:00:00-05:00
description: "GelSight surface maps of materials worn under controlled grit, load and distance, packed as Parquet and WebDataset, with alignment tools and a WebGPU viewer."
translationKey: repository-note-wearsurfacesdatasets
repository_note: "WearSurfacesDatasets"
---

# WearSurfacesDatasets

<div class="repo-status-row"><span class="repo-badge kind">Dataset</span><span class="repo-badge api">API</span></div>

<div class="repo-tech-badges"><span class="tag tool">Python</span><span class="tag tool">Parquet</span><span class="tag tool">WebDataset</span><span class="tag tool">Git LFS</span><span class="tag tool">OpenCV</span><span class="tag tool">FastAPI</span><span class="tag tool">WebGPU</span></div>

WearSurfacesDatasets publishes the surface textures captured during controlled wear tests, organised by material, abrasive grit, load and sliding distance. It is the public dataset of the [ÉTS master's research on wear in texture space]({{< ref "/posts/thesis-wear-texture-space/index.md" >}}), where it serves to compare simulated wear patterns with measured microgeometry, and it is published under [ETSim](https://github.com/ETSim) for graphics and tribology researchers who need real wear progressions.

## Overview {#overview}

Each measured state is one Parquet leaf:

```text
data/parquet/<material>/<shape>/<direction>/S<grit>/<load>g/<distance>mm/data.parquet
```

For example `data/parquet/Cartboard/Raw/Normal/S60/200g/800mm/data.parquet`. Each row stores one map as JPEG bytes in `image_data`, labelled by `map_type`; `metadata.json` lists ambient occlusion, bump, displacement, height, hillshade and normal maps. The same records are also packed as WebDataset archives `data/shards/shard-0000.tar` to `shard-0839.tar`.

`data/parquet/sequences.json` lists 20 wear timelines: cardboard at five loads (10 to 200 g, grit S60), foam, MDF (circle and line paths), PLA at several grits in linear and non-linear directions, soft wood, and unworn sandpaper references from S40 to S240.

On top of the data, the repository has three layers of tooling:

- `generate_datasets.py`, `read_datasets.py` and `generate_metadata.py` (Typer CLIs) build Parquet and shards from a `wear/` folder of PNG maps, extract them back, and write per-leaf and index metadata.
- `alignment/` registers each sequence with a two-pass SIFT/ECC method (`align.py`), crops the common valid region, adds temporal Catmull-Rom midpoints (`interpolate.py`) and extrapolates future normal maps with an FFT plus SLERP model (`extrapolate.py`). `bake.py` runs it per sequence or for all of them and can repack the results.
- `docs/index.html` is a WebGPU material viewer that reads Parquet in the browser with parquet-wasm. `docs/serve_local.py` is a FastAPI server that serves the viewer and the data and exposes `/api/datasets`, `/api/sequences` and `/api/align/sequence`.

## Getting started {#installation}

From the README:

```bash
git clone https://github.com/ETSim/WearSurfacesDatasets
cd WearSurfacesDatasets
git lfs pull
pip install -r requirements.txt
python docs/serve_local.py
# open http://127.0.0.1:8080/docs/index.html
```

In the viewer, pick a sequence, click **Load sequence**, optionally **Align sequence**, then scrub the distance or press **Play**. To bake interpolated and extrapolated steps:

```bash
python -m alignment.bake --sequence-id cartboard-raw-normal-s60-200g --pack
python -m alignment.bake --all --pack
```

To rebuild the dataset from PNG maps or extract images:

```bash
python generate_datasets.py parquet --input-dir wear --output-dir data/parquet
python generate_datasets.py webdataset --input-dir wear --output-dir data/shards
python read_datasets.py decompress --shards-dir data/shards --output-dir data/images --workers 4
```

## Repository guide {#reader-guide}

- `data/parquet/` holds the Parquet leaves, `sequences.json` and `metadata.parquet`.
- `data/shards/` holds the WebDataset `.tar` shards.
- `metadata.json` describes the materials, grits, loads, distances, capture setup and map types.
- `alignment/` contains registration, warping, interpolation, extrapolation, baking and packing.
- `docs/index.html`, `docs/serve_local.py` and `docs/serve_app.py` are the viewer and its local servers. `docs/prepare_viewer_parquets.py` rebuilds `sequences.json`.
- `docs/package/` vendors the parquet-wasm build used by the viewer.
- `examples/Wear/powerpoint/` holds one PowerPoint deck per test series (cardboard, foam, MDF, PLA, sandpaper, soft wood).

## Features {#features}

- Wear sequences indexed by material, path shape, direction, grit, load and sliding distance.
- Two storage formats: nested Parquet for browsing and WebDataset shards for streaming.
- In-browser viewer with distance scrubbing, playback and prefetching of adjacent steps.
- Server-side SIFT/ECC alignment with cached results and a flat atlas download.
- Catmull-Rom interpolation and FFT plus SLERP extrapolation of normal maps.
- CLI tools to rebuild, extract and describe the dataset.

## Limits {#limits}

- Parquet and shard files are Git LFS objects: a plain clone only contains pointers until `git lfs pull` runs.
- The `wear/` PNG source tree used by `generate_datasets.py` is not in the repository, and `data/aligned/` and `data/wear_extrapolated/` are gitignored.
- The README and `metadata.json` name Alu and Resin, but the committed `sequences.json` has no Alu or Resin sequence.
- Extrapolated frames are model output, not measurements.
- Several sequences are short (two steps for some PLA and MDF series), and one foam folder is named `4000000mm`.
- `docs/README.md` and `metadata.json` give different capture figures (resolution, number of LEDs, temperature), so treat them as descriptive.
- On a static host the viewer still loads frames, but alignment is disabled because it needs the Python server.
- There are no automated tests.

## Sources {#sources}

- [GitHub repository](https://github.com/ETSim/WearSurfacesDatasets)
- [README](https://github.com/ETSim/WearSurfacesDatasets/blob/main/README.md)
- [`data/parquet/sequences.json`](https://github.com/ETSim/WearSurfacesDatasets/blob/main/data/parquet/sequences.json)
- [`alignment/align.py`](https://github.com/ETSim/WearSurfacesDatasets/blob/main/alignment/align.py)
- [`alignment/extrapolate.py`](https://github.com/ETSim/WearSurfacesDatasets/blob/main/alignment/extrapolate.py)
- [`docs/serve_local.py`](https://github.com/ETSim/WearSurfacesDatasets/blob/main/docs/serve_local.py)
