# Maestro: Sheet music through an external conversion pipeline

> This Maestro fork connects a React upload interface to a Spring backend and external music-conversion tools. Turning a score image into MIDI passes…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/maestro/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/maestro/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/antoinebou12/Maestro
- License: AGPL-3.0
- Inspected revision: 6dca488e6e0e6bc444d3e57d6d3d62bad4ca4783

## Summary

This Maestro fork connects a React upload interface to a Spring backend and external music-conversion tools. Turning a score image into MIDI passes through an optical-recognition stage and an intermediate score representation.

**Why it exists:** Optical Music Recognition (OMR) pipeline translating sheet music scans into MIDI score sequences.

**Best fit:** Digitization of physical sheet music for playback and editing.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Java | 47.34 |
| TypeScript | 32.3 |
| Python | 16.02 |
| Dockerfile | 3.14 |
| HTML | 1 |
| Shell | 0.2 |

## Getting started (repository commands, not run here)

### README.md · Getting Started

```bash
  git clone https://github.com/PrimePhil/PFE008
```

### README.md · Frontend

```bash
  cd maestro-app
```

### README.md · Frontend

```bash
  npm install
```

### README.md · Frontend

```bash
  npm run start
```

### README.md · Tests

```bash
gradle test
```


## Features and components

- **Upload boundary** — ConvertController accepts multipart uploads at /convert. It rejects empty files, checks the 10 MiB size limit and calls a file-signature validator before saving the input. Optional tempo input travels with the conversion request.
- **External processes** — AudiverisController builds an OS-dependent command and waits for the Audiveris process. The backend also includes MxlToMidi.py. Process startup, intermediate files and the returned download are separate failure points.

## Architecture

Components and connections verified in the repository.

- React file upload → Spring validation
- Spring validation → Audiveris recognition
- Audiveris recognition → MusicXML conversion stage
- MusicXML conversion stage → MIDI download

```mermaid
flowchart LR
  n0["React file upload"]
  n1["Spring validation"]
  n2["Audiveris recognition"]
  n3["MusicXML conversion stage"]
  n4["MIDI download"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
```

**One path through the code:** Follow /convert into the file checks, then inspect how AudiverisController chooses its executable and output directory. A successful HTTP upload is only the start; conversion also depends on the external tool and generated files.

## Constraints and checks

Recognition accuracy depends on the score image and recognition engine. Shared output paths and shell commands deserve review before supporting concurrent public uploads.

## Files to read

- [backend/src/main/java/PFE008/backend/ConvertController.java](https://github.com/antoinebou12/Maestro/blob/main/backend/src/main/java/PFE008/backend/ConvertController.java)
- [backend/src/main/java/PFE008/backend/AudiverisController.java](https://github.com/antoinebou12/Maestro/blob/main/backend/src/main/java/PFE008/backend/AudiverisController.java)
- [backend/src/main/MxlToMidi.py](https://github.com/antoinebou12/Maestro/blob/main/backend/src/main/MxlToMidi.py)
- [maestro-app/package.json](https://github.com/antoinebou12/Maestro/blob/main/maestro-app/package.json)


