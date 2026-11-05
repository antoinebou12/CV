# Artemis-N3DS: Streaming within a dual-screen client

> Artemis-N3DS adapts Moonlight Embedded to the Nintendo 3DS family. It combines host discovery and pairing with a console-specific interface, input…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/artemis-n3ds/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/artemis-n3ds/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Repository: https://github.com/antoinebou12/Artemis-N3DS
- License: GPL-3.0
- Inspected revision: c5eb0205ba4eb00f4fff96097d987b3267a7be08

## Summary

Artemis-N3DS adapts Moonlight Embedded to the Nintendo 3DS family. It combines host discovery and pairing with a console-specific interface, input handling and video presentation. The New 3DS hardware path is a particular concern.

**Why it exists:** Constrained systems engineering streaming 60fps video over 802.11n Wi-Fi to a dual-screen ARM11 device.

**Best fit:** Remote desktop and gaming on legacy Nintendo New 3DS hardware.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| C++ | 76.05 |
| C | 15.71 |
| CMake | 4.36 |
| Makefile | 2.84 |
| Shell | 0.64 |
| Dockerfile | 0.4 |

## Getting started (repository commands, not run here)

### README.md · Docker (easiest)

```bash
docker build --network=host -t moonlight-n3ds .
docker run --rm -it -v .:/moonlight-N3DS -w /moonlight-N3DS moonlight-n3ds:latest
make
```

### README.md · Local (devkitPro)

```bash
make
```


## Features and components

- **Control plane** — n3ds_main.cpp brings together host discovery, pair records, profiles and connection state. The selected host and application determine the stream request. Graphics lifecycle state is tracked separately from stream configuration.
- **Media and interaction** — Audio, input and video live in separate src modules. Hardware capabilities influence the guidance shown to the user. The UI can return from a stream, while explicit system-close handling must unwind the application instead.

## Architecture

Components and connections verified in the repository.

- Host discovery and pairing → Selected app and profile
- Selected app and profile → GameStream connection
- GameStream connection → Video and audio backends
- Video and audio backends → 3DS screens and controls
- 3DS screens and controls → GameStream connection

```mermaid
flowchart LR
  n0["Host discovery and pairing"]
  n1["Selected app and profile"]
  n2["GameStream connection"]
  n3["Video and audio backends"]
  n4["3DS screens and controls"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
  n4 --> n2
```

**One path through the code:** Follow SelectedHost and stream-profile selection before entering the media path. System close and a normal return to the menu are different transitions; the explicit close flag exists to keep those paths apart.

## Constraints and checks

The original and New 3DS have different decoding capabilities. Suggested presets in code are not measured guarantees of frame rate or network performance.

## Files to read

- [src/n3ds_main.cpp](https://github.com/antoinebou12/Artemis-N3DS/blob/n3ds-main/src/n3ds_main.cpp)
- [src/hardware_capabilities.cpp](https://github.com/antoinebou12/Artemis-N3DS/blob/n3ds-main/src/hardware_capabilities.cpp)
- [src/video/video.hpp](https://github.com/antoinebou12/Artemis-N3DS/blob/n3ds-main/src/video/video.hpp)

