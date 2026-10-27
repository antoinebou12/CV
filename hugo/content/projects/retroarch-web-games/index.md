---
title: "RetroArch Web Games"
date: 2024-01-01T12:00:00Z
description: "A self-hosted RetroArch web player with a collection of classic games."
draft: false
---

## RetroArch Web Games

[retroarch-web-games](https://github.com/antoinebou12/retroarch-web-games): Docker Retroarch Web with pre-downloaded games.

Self-hosted RetroArch in the browser with NES, SNES, Genesis, and Game Boy games packaged in a Docker image.

### Features

- Pre-loaded games for NES, SNES, Genesis, and Game Boy
- Self-hosted web player
- Docker / Docker Compose deploy

### Related project

- [FlashGames](https://antoinebou12.github.io/FlashGames/) — A small collection of legacy Flash games preserved for modern browsers with Ruffle.
- Source: [antoinebou12/FlashGames](https://github.com/antoinebou12/FlashGames)

### How to Use

To get started, run the Docker image with the following command:

```bash
docker-compose up -d
```

### Download HERE

[https://hub.docker.com/r/antoinebou13/retroarch-web-games](https://hub.docker.com/r/antoinebou13/retroarch-web-games)

### Image Size Warning

_Note: The Docker image is approximately 10GB due to the inclusion of various games._

### Script Explanation

```markdown
### Behind the Scenes: Scripting for Game Downloads

Scripts in the image download and organize game archives:

1. **Batch downloading of game archives:**
   The `download_7z_files` bash function and a Python script fetch archives from several sources.

2. **Renaming and sorting games:**
   Bash and Python rename files and sort them into directories so RetroArch can list them cleanly.

3. **Parallel downloads and errors:**
   Bash jobs and Python's ThreadPoolExecutor run downloads in parallel; failures are reported instead of failing silently.

## Acknowledgements

This Docker image is based on:

- [Inglebard/dockerfiles (retroarch-web branch)](https://github.com/Inglebard/dockerfiles/tree/retroarch-web)
- [libretro/RetroArch (master/pkg/emscripten)](https://github.com/libretro/RetroArch/tree/master/pkg/emscripten)

### License

MIT License.

### Source

"https://archive.org/download/nointro.gb"
"https://archive.org/download/nointro.gbc"
"https://archive.org/download/nointro.gba"
"https://archive.org/download/nointro.snes"
"https://archive.org/download/nointro.md"
"https://archive.org/download/nointro.nes-headered"
