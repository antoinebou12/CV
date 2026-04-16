---
title: "RetroArch Web Games"
date: 2024-01-01T12:00:00Z
description: "A self-hosted RetroArch web player with a collection of classic games."
draft: false
---

## RetroArch Web Games

[retroarch-web-games](https://github.com/antoinebou12/retroarch-web-games): Docker Retroarch Web with pre-downloaded games.

This repository offers a self-hosted RetroArch web player, allowing you to enjoy classic NES, SNES, Genesis, and Gameboy games right in your browser. Set up is a breeze with our Docker container.

### Features

- **Pre-loaded Games**: Enjoy a variety of games for NES, SNES, Genesis, and Gameboy.
- **Self-hosted Web Player**: Easily host the RetroArch player on your own server.
- **Easy Deployment**: Utilize Docker for straightforward setup and deployment.

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

The RetroArch Web Games setup includes sophisticated scripting to streamline the download and organization of game files. Here's a breakdown of how these scripts function:

1. **Batch Downloading of Game Archives:**
   The `download_7z_files` bash function and Python script work together to efficiently download game archives from various sources.

2. **Simplifying and Sorting Games:**
   Using both bash and Python, the scripts simplify game filenames and sort them into appropriate directories. This ensures easy navigation and selection within the RetroArch interface.

3. **Efficiency and Error Handling:**
   The use of parallel processing in bash and Python's ThreadPoolExecutor maximizes efficiency. Additionally, error handling ensures stability and provides feedback in case of issues during the download process.

## Acknowledgements

This Docker image is based on:

- [Inglebard/dockerfiles (retroarch-web branch)](https://github.com/Inglebard/dockerfiles/tree/retroarch-web)
- [libretro/RetroArch (master/pkg/emscripten)](https://github.com/libretro/RetroArch/tree/master/pkg/emscripten)

### License

Licensed under the MIT License, ensuring open and unrestricted use to the community.

I have put a lot of work into making this project both powerful and accessible. Whether you're a seasoned gamer or just nostalgic for the classics.

### Source

"https://archive.org/download/nointro.gb"
"https://archive.org/download/nointro.gbc"
"https://archive.org/download/nointro.gba"
"https://archive.org/download/nointro.snes"
"https://archive.org/download/nointro.md"
"https://archive.org/download/nointro.nes-headered"
