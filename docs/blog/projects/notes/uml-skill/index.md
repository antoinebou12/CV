# uml-skill: Instructions with a small encoding fallback

> uml-skill packages diagram-writing instructions and a small Python helper. It is a skill bundle, not an MCP server or an image-generation model. The…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/uml-skill/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/uml-skill/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Repository: https://github.com/antoinebou12/uml-skill
- License: MIT
- Inspected revision: 05b27cdbe68ea3a9543b8ce8f66586b62194892a

## Summary

uml-skill packages diagram-writing instructions and a small Python helper. It is a skill bundle, not an MCP server or an image-generation model. The helper can produce a Kroki URL from diagram source.

**Why it exists:** Agent skill bundle providing direct tool definitions and prompt guides for diagram generation.

**Best fit:** Drop-in diagram generation capabilities for LLM agent frameworks.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Python | 100 |

## Getting started (repository commands, not run here)

### scripts/README.md · Usage

```bash
python kroki_url.py --help
```

### scripts/README.md · Usage

```bash
python kroki_url.py -t mermaid diagram.mmd
python kroki_url.py -t plantuml -f png diagram.puml
```

### scripts/README.md · Usage

```bash
Get-Content diagram.puml -Raw | python kroki_url.py -t plantuml
```

### scripts/README.md · Usage

```bash
cat diagram.puml | python kroki_url.py -t plantuml
```


## Features and components

- **Instruction layer** — SKILL.md describes the workflow and points to diagram references. An agent can use those instructions with available diagram tools. References supply syntax guidance without becoming an application runtime.
- **Encoding helper** — scripts/kroki_url.py uses standard-library compression and encoding to construct a rendering URL. Generating that URL and requesting the rendered image are separate operations.

## Architecture

Components and connections verified in the repository.

- Diagram request → Skill and syntax references
- Skill and syntax references → Diagram source
- Diagram source → Kroki URL helper
- Kroki URL helper → Rendering endpoint

```mermaid
flowchart LR
  n0["Diagram request"]
  n1["Skill and syntax references"]
  n2["Diagram source"]
  n3["Kroki URL helper"]
  n4["Rendering endpoint"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
```

**One path through the code:** Read the encoder to see how source becomes a URL-safe payload. The helper transports the source; syntax validation and visual quality still depend on the diagram language and renderer.

## Constraints and checks

A URL payload is recoverable text, not encryption. The bundle’s instructions do not guarantee that a chosen external renderer is available.

## Files to read

- [scripts/kroki_url.py](https://github.com/antoinebou12/uml-skill/blob/main/scripts/kroki_url.py)
- [README.md](https://github.com/antoinebou12/uml-skill/blob/main/README.md)

