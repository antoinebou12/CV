# ChitUI: A local bridge to resin printers

> ChitUI places a browser interface in front of SDCP resin printers. A Python process serves the web assets, discovers printers on the local network and…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/chitui/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/chitui/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/antoinebou12/ChitUI
- Inspected revision: a4236172836c65116a88dcd39a934441691be34c

## Summary

ChitUI places a browser interface in front of SDCP resin printers. A Python process serves the web assets, discovers printers on the local network and translates browser actions into printer communication.

**Why it exists:** Full-featured web control interface for Chitubox SDCP 3.0 resin printers with LAN UDP discovery.

**Best fit:** Headless remote management and real-time print monitoring for SLA 3D printers.

## Use cases

Flask web UI that finds Chitubox SDCP 3.0 resin printers on the LAN, uploads files and starts prints.

- **Discover printers on the LAN** (Printer operator, SDCP resin printer): At start-up, discover_printers in main.py broadcasts M99999 over UDP port 3000, saves the replies and opens a WebSocket to each printer at ws://<ip>:3030/websocket.
- **Watch printer status** (Printer operator, SDCP resin printer): The browser asks over Socket.IO; main.py sends SDCP commands 0 (status) and 1 (attributes) and relays printer messages to web/js/chitui.js and sdcp.js.
- **Upload a print file** (Printer operator, SDCP resin printer): POST /upload accepts .ctb, .goo and .prz files, computes an MD5 and sends 1 MB parts to http://<ip>:3030/uploadFile/upload; /progress streams the percentage.
- **List and delete files** (Printer operator, SDCP resin printer): printer_files sends SDCP command 258 with a storage path; action_delete sends command 259 with the file list.
- **Start a print** (Printer operator, SDCP resin printer): action_print sends SDCP command 128 with the file name and StartLayer 0.

### Scenario: Send a sliced model to a resin printer from a browser

1. Install requirements.txt in a virtualenv and run python main.py, or use docker run --net=host so UDP broadcast works.
2. At start-up, ChitUI broadcasts M99999 on UDP port 3000 and connects to each printer’s WebSocket on port 3030.
3. Open http://127.0.0.1:54780/ to see the discovered printers and their status.
4. Upload a .ctb file; ChitUI saves it to /tmp and sends it in 1 MB parts with an MD5 check.
5. Pick the file in the printer’s file list and start the print.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| JavaScript | 48.61 |
| HTML | 24.57 |
| Python | 22.86 |
| CSS | 3.51 |
| Dockerfile | 0.45 |

## Verified technologies

- SDCP 3.0 — README title
- Docker — README Docker section
- Browser UI — README Usage, default port 54780
- Local network — README Docker host networking for UDP discovery

## Getting started (repository commands, not run here)

### README.md · Setup

```bash
python -mvenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### README.md · Usage

```bash
python main.py
```


### Docker

```bash
docker build -t chitui:latest .
docker run --rm --name chitui --net=host chitui:latest
```

## Features and components

- **Browser and local server** — main.py builds a Flask application with web as its static folder and attaches Flask-SocketIO. Printer and WebSocket registries live in process memory. Discovery uses the local network, which explains the README’s Docker host-network requirement.
- **File transfer** — The upload route validates the extension and saves the incoming file temporarily. The printer upload helper calculates an MD5 checksum and sends one-megabyte parts with offsets. A separate event-stream route reports upload progress.

## Architecture

Components and connections verified in the repository.

- Browser UI → Flask and SocketIO
- Flask and SocketIO → Printer discovery and session
- Printer discovery and session → SDCP printer
- SDCP printer → Printer discovery and session

```mermaid
flowchart LR
  n0["Browser UI"]
  n1["Flask and SocketIO"]
  n2["Printer discovery and session"]
  n3["SDCP printer"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n2
```

**One path through the code:** Follow /upload through the temporary file and the printer transfer helper. Transfer progress is global in this implementation, so simultaneous uploads would need per-job state to avoid mixing their percentages.

## Workflow

1. **Choose a file** — Select a supported print file for a discovered printer. The upload handler accepts multipart fields named file and printer.
2. **Validate the request** — The handler checks missing file or printer fields and the allowed extensions ctb, goo and prz before continuing.
3. **Store temporarily** — The server receives the file into temporary storage before starting transfer to the printer.
4. **Transfer to printer** — The helper sends chunks to the selected printer on the local network. Progress events are available on GET /progress as text/event-stream.
5. **Confirm the outcome** — Check the response and verify the file on the printer. The helper may report success after a failed part; treat the success body alone as incomplete proof of delivery.

## API


- `POST /upload`
- `GET /upload`
- `GET /progress`

## Constraints and checks

Treat this fork as a local-network prototype. A reachable web interface does not confirm compatibility with a particular printer firmware or safe remote access.

## Files to read

- [main.py](https://github.com/antoinebou12/ChitUI/blob/master/main.py)
- [Dockerfile](https://github.com/antoinebou12/ChitUI/blob/master/Dockerfile)
- [requirements.txt](https://github.com/antoinebou12/ChitUI/blob/master/requirements.txt)


