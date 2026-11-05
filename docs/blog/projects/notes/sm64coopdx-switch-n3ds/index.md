# sm64coopdx-switch-N3DS: Keeping a port behind platform interfaces

> This fork explores Switch and New 3DS targets for sm64coopdx. Shared game and co-op code sit above platform-specific graphics, audio and input. The…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/sm64coopdx-switch-n3ds/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/sm64coopdx-switch-n3ds/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Repository: https://github.com/antoinebou12/sm64coopdx-switch-N3DS
- Inspected revision: 567fd71a962d44e006461f3085a3a7ca3a063eb4

## Summary

This fork explores Switch and New 3DS targets for sm64coopdx. Shared game and co-op code sit above platform-specific graphics, audio and input. The platform probe is a smaller executable with a narrower purpose than the full game.

**Why it exists:** Low-level C systems port optimizing multi-threaded networking and memory layout for embedded handheld consoles.

**Best fit:** Co-op multiplayer emulation and custom embedded gaming on Switch & N3DS.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| C | 82.89 |
| C++ | 10.86 |
| Lua | 4 |
| Python | 1.44 |
| Assembly | 0.49 |
| Shell | 0.13 |
| Pawn | 0.11 |
| Go Template | 0.04 |
| Makefile | 0.03 |
| Dockerfile | 0 |
| Linker Script | 0 |
| PHP | 0 |
| BitBake | 0 |

## Features and components

- **Shared runtime and backends** — src/pc separates controller, audio, graphics, networking and platform code. Porting work can replace a backend while keeping shared game behavior. Build flags and target makefiles determine which implementations are linked.
- **The platform probe** — Makefile.switch-platform compiles a probe with Switch lifecycle, input and crash-log code, then packages an NRO using devkitPro tools. Its source list is deliberately smaller than the full game’s build.

## Architecture

Components and connections verified in the repository.

- Shared game and co-op code → Platform interfaces
- Platform interfaces → Graphics backend
- Platform interfaces → Controller and audio backends
- Graphics backend → Console runtime
- Controller and audio backends → Console runtime

```mermaid
flowchart LR
  n0["Shared game and co-op code"]
  n1["Platform interfaces"]
  n2["Graphics backend"]
  n3["Controller and audio backends"]
  n4["Console runtime"]
  n0 --> n1
  n1 --> n2
  n1 --> n3
  n2 --> n4
  n3 --> n4
```

**One path through the code:** Read the probe’s SOURCES list before interpreting a successful build. It exercises selected platform modules; it does not establish that every game subsystem, graphics path or co-op session works on the console.

## Constraints and checks

Full-game testing requires the user’s own legally obtained game assets and actual hardware validation. This fork retains the upstream game-project credit.

## Files to read

- [Makefile.switch-platform](https://github.com/antoinebou12/sm64coopdx-switch-N3DS/blob/main/Makefile.switch-platform)
- [src/pc/platform/switch/switch_platform.c](https://github.com/antoinebou12/sm64coopdx-switch-N3DS/blob/main/src/pc/platform/switch/switch_platform.c)
- [Makefile.new3ds](https://github.com/antoinebou12/sm64coopdx-switch-N3DS/blob/main/Makefile.new3ds)

