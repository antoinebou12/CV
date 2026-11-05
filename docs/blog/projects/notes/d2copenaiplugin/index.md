# D2COpenAIPlugin: Routing text to diagram backends

> D2COpenAIPlugin is a FastAPI diagram service with a plugin manifest and an OpenAPI surface. Its implementation selects among PlantUML, Mermaid and Kroki…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/d2copenaiplugin/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/d2copenaiplugin/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Repository: https://github.com/antoinebou12/D2COpenAIPlugin
- License: MIT
- Inspected revision: 7d15ee155d5f392b1d90192dc2e21ec479a6291a

## Summary

D2COpenAIPlugin is a FastAPI diagram service with a plugin manifest and an OpenAPI surface. Its implementation selects among PlantUML, Mermaid and Kroki paths based on the request’s diagram language.

**Why it exists:** OpenAI ChatGPT plugin manifest and OpenAPI endpoint handler for text-to-diagram conversion.

**Best fit:** ChatGPT Plus GPT Store integration for software architects.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Python | 100 |

## Getting started (repository commands, not run here)

### README.md · Quick start

```bash
git clone https://github.com/antoinebou12/D2COpenAIPlugin.git
cd D2COpenAIPlugin
python -m venv .venv
```

### README.md · Quick start

```bash
.\.venv\Scripts\Activate.ps1
```

### README.md · Quick start

```bash
source .venv/bin/activate
```

### README.md · Quick start

```bash
pip install -r requirements-dev.txt
python -m pytest
uvicorn app:app --host 127.0.0.1 --port 5003
```

### README.md · Quick start

```bash
python app.py
```

### plantuml/README.md · Installation

```bash
pip install plantumlapi
```

### plantuml/README.md · Installation

```bash
pip install git+https://github.com/antoinebou12/plantumlapi
```

### plantuml/README.md · Command Line Usage

```bash
usage: plantuml.py [-h] [-o OUT] [-s SERVER] filename [filename ...]
Generate images from PlantUML defined files using PlantUML server
positional arguments: 
  filename            file(s) to generate images from
optional arguments: 
  -h, --help          show this help message and exit 
  -o OUT, --out OUT   directory to put the files into 
  -s SERVER, --server SERVER 
                      server to generate from; defaults to plantuml.com 
```


## Features and components

- **Request model** — DiagramRequest contains lang, type, code and theme. Validators check the language and source length. /generate_diagram rejects missing fields before dispatching to a backend; the code then builds result and playground links.
- **Backend adapters** — PlantUML uses its dedicated client, Mermaid builds an editor state, and D2 aliases are normalized to the Kroki d2 renderer. Other supported languages use the Kroki language registry. The adapters isolate differing URL and encoding conventions.

## Architecture

Components and connections verified in the repository.

- Structured diagram request → FastAPI model and route
- FastAPI model and route → PlantUML adapter
- FastAPI model and route → Mermaid state encoder
- FastAPI model and route → Kroki adapter
- PlantUML adapter → Result and playground links
- Mermaid state encoder → Result and playground links
- Kroki adapter → Result and playground links

```mermaid
flowchart LR
  n0["Structured diagram request"]
  n1["FastAPI model and route"]
  n2["PlantUML adapter"]
  n3["Mermaid state encoder"]
  n4["Kroki adapter"]
  n5["Result and playground links"]
  n0 --> n1
  n1 --> n2
  n1 --> n3
  n1 --> n4
  n2 --> n5
  n3 --> n5
  n4 --> n5
```

**One path through the code:** Compare the PlantUML and D2 branches in app.py. They accept the same request model but use different rendering adapters. The type validator logs an invalid type rather than raising, so it is not equivalent to strict language validation.

## Constraints and checks

The plugin manifest documents the original integration format. Its presence does not establish current availability in a third-party product or confidentiality of remote rendering.

## Files to read

- [app.py](https://github.com/antoinebou12/D2COpenAIPlugin/blob/main/app.py)
- [kroki/kroki.py](https://github.com/antoinebou12/D2COpenAIPlugin/blob/main/kroki/kroki.py)
- [mermaid/mermaid.py](https://github.com/antoinebou12/D2COpenAIPlugin/blob/main/mermaid/mermaid.py)

