# MistubaVideo

> MistubaVideo is an ETSim repository for video-related work with Mitsuba.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/mistubavideo/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/mistubavideo/index.md
- Published: 2026-10-24
- Updated: 2026-10-24
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/ETSim/MistubaVideo
- Inspected revision: 87b180b9f03333b773fecd7708be86c75b1f822d


## Use cases

Mitsuba 3 tools from ETSim that path-trace OBJ sequences and wear-field recordings into frames, MP4 videos and GIFs.

- **Render an OBJ sequence** (Simulation researcher, Mitsuba 3 and FFmpeg): python main.py multi --folder exports --regex "\d+\.obj" builds a scene XML per matching OBJ, renders it on CPU or CUDA at the chosen spp and resolution, then encodes MP4 and GIF with FFmpeg.
- **Render several camera views** (Simulation researcher): --view front --view top or --all-views renders each frame from the front, back, left, right, top, bottom or perspective camera defined in src/mitsuba/camera.py, with the view name in the file name.
- **Denoise and split AOVs** (Simulation researcher, Mitsuba 3 and FFmpeg): python main.py denoise <path> runs the OptiX denoiser from src/mitsuba/denoising.py on rendered images, and python main.py aov <file.exr> extracts the AOV layers of an EXR into separate files.
- **Make a field video** (Simulation researcher, Mitsuba 3 and FFmpeg): mitsuba-video render <manifest.json> -q paper path-traces rigid bodies at their recorded poses with a field-driven material blend and heatmap, adds a UV atlas panel and a covered-area chart, and encodes an MP4.
- **Render a wear recording** (Simulation researcher, TextureFriction runs): python main.py wear render simulation_<ts> or tf-render reads a TextureFriction --record folder or .h5 file through the texturefriction source.
- **Write and check a manifest** (Simulation researcher): Any project can emit a versioned manifest.json with ManifestWriter; mitsuba-video validate checks it against manifest-v1.schema.json, and mitsuba-video fixture creates a small synthetic example.

### Scenario: Render the demo field video

1. Install FFmpeg and Mitsuba 3, then run pip install -e "packages/mitsuba_video[texturefriction]" to get mitsuba-video and tf-render.
2. Create a synthetic input with mitsuba-video fixture demo.
3. Check the framing quickly with mitsuba-video preview demo.
4. Run mitsuba-video render demo -q preview to path-trace the frames and encode the MP4.
5. For real data, point python main.py wear render at a TextureFriction simulation_<ts> folder with -q paper.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Python | 99.67 |
| Dockerfile | 0.33 |

## Getting started (repository commands, not run here)

### README.md · Basic Usage

```bash
python main.py multi --folder exports --regex "\d+\.obj"
```

### README.md · Command-line Options

```bash
Options:
  -f, --folder TEXT               Folder containing OBJ files  [required]
  -r, --regex TEXT                Regex pattern for OBJ filenames  [default: \d+\.obj]
  -n, --name TEXT                 Base name for output files  [default: multi_obj]
  -t, --threaded                  Enable multi-threading
  -w, --workers INTEGER           Max worker threads (if threaded)
  --video / --no-video            Enable video creation  [default: video]
  --gif / --no-gif                Enable GIF creation  [default: gif]
  -d, --device TEXT               Rendering device (cpu/cuda)  [default: cpu]
  -s, --spp INTEGER               Samples per pixel  [default: 256]
  --width INTEGER                 Output image width  [default: 1920]
  --height INTEGER                Output image height  [default: 1080]
```

### README.md · Additional Commands

```bash
python main.py info
```

### README.md · Command-line Usage

```bash
python main.py multi --folder models --view front --view top --view right
```

### README.md · Command-line Usage

```bash
python main.py multi --folder models --all-views
```

### packages/mitsuba_video/README.md · Install and run

```bash
pip install -e "packages/mitsuba_video[texturefriction]"   # drop the extra if you don't need h5py
mitsuba-video fixture demo                                   # synthetic manifest to try things on
mitsuba-video inspect demo
mitsuba-video preview demo                                   # 960x540, 16 spp, every 8th frame
mitsuba-video render  demo -q paper --camera orbit --title "Wear on a plane" --ramp 0.2
mitsuba-video encode  demo/render_heatmap --fps 15 --hold 4  # new fps/title without re-rendering
mitsuba-video render  demo --resume                          # continue an interrupted render
```



