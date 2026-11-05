# Artemis-Switch: A streamed frame from host to screen

> Artemis-Switch is a fork in the Moonlight streaming family. The host runs the game; the client receives compressed video and audio while sending…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/artemis-switch/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/artemis-switch/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Repository: https://github.com/antoinebou12/Artemis-Switch
- License: GPL-3.0
- Inspected revision: 33e6854781a47e86ae349e0a7646ff00bd924ddd

## Summary

Artemis-Switch is a fork in the Moonlight streaming family. The host runs the game. The client receives compressed video and audio, renders frames and sends controller input back.

**Why it exists:** Hardware-accelerated GameStream/Moonlight client in C++ with custom NVN display frame pacing for zero-stutter video.

**Best fit:** Ultra-low latency PC game streaming directly to Nintendo Switch handheld mode.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| C++ | 53.78 |
| C | 33.23 |
| Java | 5.69 |
| CMake | 3.51 |
| Objective-C++ | 1.95 |
| Shell | 0.75 |
| Swift | 0.38 |
| Python | 0.35 |
| GLSL | 0.34 |
| Makefile | 0.02 |
| PowerShell | 0.01 |

## Getting started (repository commands, not run here)

### README.md · Developer build

```bash
git clone --recursive https://github.com/antoinebou12/Artemis-Switch.git
cd Artemis-Switch
cmake -B build/switch -DCMAKE_BUILD_TYPE=Release -DPLATFORM_SWITCH=ON -DUSE_DEKO3D=ON
cmake --build build/switch --target Moonlight.nro --parallel
```

### README.md · Developer validation

```bash
python tests/i18n_consistency_test.py
python tests/release_contract_test.py
cmake -S tests -B build/tests -DCMAKE_BUILD_TYPE=Debug
cmake --build build/tests --parallel
ctest --test-dir build/tests --output-on-failure
```

### README.md · Developer validation

```bash
python -m pip install ruff==0.12.10
python scripts/lint.py
cmake -S tests -B build/lint -DCMAKE_BUILD_TYPE=Debug -DARTEMIS_STRICT_WARNINGS=ON -DARTEMIS_ENABLE_CLANG_TIDY=ON
cmake --build build/lint --parallel
```

### README.md · Developer validation

```bash
cmake -S ci/integration -B build/integration -DCMAKE_BUILD_TYPE=Debug
cmake --build build/integration --parallel
ctest --test-dir build/integration --output-on-failure
```

### app/platforms/android-project/README.md · Building

```bash
cd android-project
```

### app/platforms/android-project/README.md · Building

```bash
./build_libromfs_generator.sh
```

### app/platforms/android-project/README.md · Building

```bash
export JAVA_HOME=/Applications/Android\ Studio.app/Contents/jbr/Contents/Home
export ANDROID_SDK_ROOT=~/Library/Android/sdk
./gradlew assembleDebug
./gradlew installDebug
```


## Features and components

- **Session and interface** — The Borealis interface handles host selection and settings. MoonlightSession coordinates streaming, while the Switch decoder-and-render provider chooses concrete video and audio implementations. UI state and media processing have different lifecycles.
- **Platform-specific output** — The provider constructs FFmpegVideoDecoder. With BOREALIS_USE_DEKO3D it selects ArtemisDKVideoRenderer, while other build flags select other renderers. Switch audio uses AudrenAudioRenderer. These are explicit build-time choices.

## Architecture

Components and connections verified in the repository.

- GameStream host → Streaming session
- Streaming session → FFmpeg video decoder
- FFmpeg video decoder → deko3d renderer
- deko3d renderer → Switch display
- Controller input → Streaming session
- Streaming session → GameStream host

```mermaid
flowchart LR
  n0["GameStream host"]
  n1["Streaming session"]
  n2["FFmpeg video decoder"]
  n3["deko3d renderer"]
  n4["Switch display"]
  n5["Controller input"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
  n5 --> n1
  n1 --> n0
```

**One path through the code:** Read the provider methods to see which backend is actually compiled, then follow the session’s decoded frames into that renderer. Network, decode and presentation delays need separate measurements to explain a slow stream.

## Constraints and checks

A successful build does not establish hardware latency, codec support or stability on every target. Upstream Moonlight authorship remains credited.

## Files to read

- [app/src/main.cpp](https://github.com/antoinebou12/Artemis-Switch/blob/main/app/src/main.cpp)
- [app/src/streaming/MoonlightSession.cpp](https://github.com/antoinebou12/Artemis-Switch/blob/main/app/src/streaming/MoonlightSession.cpp)
- [app/src/streaming/switch/SwitchMoonlightSessionDecoderAndRenderProvider.cpp](https://github.com/antoinebou12/Artemis-Switch/blob/main/app/src/streaming/switch/SwitchMoonlightSessionDecoderAndRenderProvider.cpp)

