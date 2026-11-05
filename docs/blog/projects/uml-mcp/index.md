# uml-mcp

> Open-source MCP server for UML and architecture diagrams — Mermaid, PlantUML, and Kroki from chat in Cursor and ChatGPT.

- HTML page: https://antoineboucher.info/CV/blog/projects/uml-mcp/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/uml-mcp/index.md
- Published: 2026-09-02
- Updated: 2026-09-02
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)# uml-mcp

[![GitHub stars](https://img.shields.io/github/stars/antoinebou12/uml-mcp)](https://github.com/antoinebou12/uml-mcp/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/antoinebou12/uml-mcp)](https://github.com/antoinebou12/uml-mcp)

[Repository](https://github.com/antoinebou12/uml-mcp) · [MIT License](https://github.com/antoinebou12/uml-mcp/blob/main/LICENSE) · [Docs](https://antoinebou12.github.io/uml-mcp/) · [Hosted MCP](https://uml-mcp.vercel.app/mcp)

**uml-mcp** is an open-source **Model Context Protocol** server that generates **Mermaid**, **PlantUML**, and **Kroki** diagrams from natural-language prompts or explicit diagram source. Use it in **Cursor** (MCP tools) or **ChatGPT** via a [Custom GPT](https://github.com/antoinebou12/D2COpenAIPlugin).

Blog write-up: [uml-mcp — diagrams from chat](https://antoineboucher.info/CV/blog/posts/uml-mcp/).

## Features

- `generate_uml` and related MCP tools for sequence, class, flow, and deployment sketches
- Multiple render backends (Mermaid, PlantUML, Kroki)
- Used across this portfolio blog for inline `.mmd` + SVG diagrams

## Quick start

```bash
git clone https://github.com/antoinebou12/uml-mcp.git
cd uml-mcp
```

Follow the README for Python dependencies and Cursor MCP configuration.

## Related

- [D2COpenAIPlugin](https://antoineboucher.info/CV/blog/projects/d2copenaiplugin/) — earlier ChatGPT plugin path
