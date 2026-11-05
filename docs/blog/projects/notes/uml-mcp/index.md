# uml-mcp: From an MCP tool call to a diagram

> uml-mcp exposes diagram tools to MCP clients. The client supplies diagram source and options; the server validates and routes the request to rendering…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/uml-mcp/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/uml-mcp/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/antoinebou12/uml-mcp
- License: MIT
- Inspected revision: ebaeac6eb6737639cd1fd5e92967408309a9a64d

## Summary

uml-mcp exposes diagram tools to MCP clients. The client supplies diagram source and options; the server validates and routes the request to rendering services, then returns diagram results and useful editor links.

**Why it exists:** Flagship Model Context Protocol (MCP) server generating PlantUML, Mermaid, and Kroki directly from LLMs (Claude, Cursor, ChatGPT) with zero local dependencies.

**Best fit:** Interactive architectural diagram generation for AI pair programming and automated design docs.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Python | 90.9 |
| TypeScript | 7.99 |
| Shell | 0.31 |
| CSS | 0.26 |
| Go Template | 0.23 |
| Makefile | 0.14 |
| Dockerfile | 0.11 |
| JavaScript | 0.03 |
| HTML | 0.02 |

## Getting started (repository commands, not run here)

### README.md · Quick start

```bash
git clone https://github.com/antoinebou12/uml-mcp.git
cd uml-mcp
uv sync
uv run python server.py
```

### README.md · Quick start

```bash
git remote add origin https://github.com/antoinebou12/uml-mcp.git
```

### tests/mcp-rig/README.md · Running

```bash
make mcp-rig
```

### tests/mcp-rig/README.md · Running

```bash
uvx mcp-rig@0.1.0 run tests/mcp-rig/
uvx mcp-rig@0.1.0 run tests/mcp-rig/ --tag smoke
uvx mcp-rig@0.1.0 run tests/mcp-rig/generate.yaml --case "batch*"
uvx mcp-rig@0.1.0 run tests/mcp-rig/ --server-logs   # show server stderr when debugging
```


## Features and components

- **A quiet entry point** — server.py delegates startup to mcp_core.core.server. It resolves the mcp object lazily through __getattr__, avoiding server construction and stdout output merely from importing the module. That matters when stdout carries the stdio protocol.
- **Transport and rendering** — The server supports stdio and HTTP entry paths. The core groups tool registration, configuration and Kroki integration. Rendering is a downstream operation: the MCP layer describes tools and carries their inputs and results.

## Architecture

Components and connections verified in the repository.

- MCP client → stdio or HTTP transport
- stdio or HTTP transport → FastMCP tools and validation
- FastMCP tools and validation → Kroki renderer
- Kroki renderer → Diagram result and links
- Diagram result and links → MCP client

```mermaid
flowchart LR
  n0["MCP client"]
  n1["stdio or HTTP transport"]
  n2["FastMCP tools and validation"]
  n3["Kroki renderer"]
  n4["Diagram result and links"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
  n4 --> n0
```

**One path through the code:** Start at server.py, follow main into mcp_core, then inspect the registered diagram tool before its renderer. A tool invocation supplies structured arguments; it does not make arbitrary prose valid Mermaid or PlantUML.

## API



## Constraints and checks

Remote rendering transmits the diagram source. Validate the renderer endpoint and data policy before using internal architecture or other confidential material.

## Files to read

- [server.py](https://github.com/antoinebou12/uml-mcp/blob/main/server.py)
- [mcp_core/core/server.py](https://github.com/antoinebou12/uml-mcp/blob/main/mcp_core/core/server.py)
- [README.md](https://github.com/antoinebou12/uml-mcp/blob/main/README.md)


