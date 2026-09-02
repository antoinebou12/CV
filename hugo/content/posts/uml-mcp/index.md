---
post_kind: article
title: "uml-mcp — UML diagrams from chat via MCP"
date: 2026-09-02T14:00:00-04:00
lastmod: 2026-09-02T14:00:00-04:00
description: "Open-source MCP server for Mermaid, PlantUML, and Kroki diagrams in Cursor and ChatGPT — why I built it, how to install, and links to earlier diagram tooling."
translationKey: uml-mcp-post
tags:
  - MCP
  - UML
  - Mermaid
  - PlantUML
  - Cursor
  - Open source
---

[![GitHub stars](https://img.shields.io/github/stars/antoinebou12/uml-mcp?style=social)](https://github.com/antoinebou12/uml-mcp)

**[uml-mcp](https://github.com/antoinebou12/uml-mcp)** is an open-source Model Context Protocol server that turns architecture prompts into **Mermaid**, **PlantUML**, or **Kroki** diagrams. Describe a system in chat; the tool renders syntax you can paste into Hugo posts, GitHub READMEs, or design reviews. It runs in **Cursor** today and pairs with a [Custom GPT](https://github.com/antoinebou12/D2COpenAIPlugin) for ChatGPT. The repo sits at about **★ 97** and is the diagram path I reach for most often. **[Version française]({{< ref "/posts/uml-mcp/index.fr.md" >}})**.

<!--more-->

## Why MCP instead of copy-paste templates?

I started with ChatGPT plugins ([D2C OpenAI diagram plugin]({{< ref "/posts/d2c-openai-diagram-plugin/index.md" >}})) and [AIPRM sequence templates]({{< ref "/posts/chatgpt-airprm-sequence-diagrams/index.md" >}}). Both work, but editors wanted **native tools**: enable a server once, call `generate_uml` from the agent, save `.mmd` + SVG beside the post. MCP is that layer — same idea as the plugin, different host.

## What it supports

| Backend | Good for |
|---------|----------|
| **Mermaid** | GitHub-native flows, quick sequences |
| **PlantUML** | Classic UML, deployments, strict notation |
| **Kroki** | Unified render path when you mix formats |

Hosted endpoint: [uml-mcp.vercel.app/mcp](https://uml-mcp.vercel.app/mcp). Docs site: [antoinebou12.github.io/uml-mcp](https://antoinebou12.github.io/uml-mcp/).

## Cursor setup (short)

1. Clone or install from **[github.com/antoinebou12/uml-mcp](https://github.com/antoinebou12/uml-mcp)** (README has the MCP config block).
2. Add the server to Cursor MCP settings.
3. Ask for a diagram type explicitly — e.g. "Mermaid sequence: user, React, FastAPI, Postgres, login with cache miss."

I use it across this blog for pipeline and career diagrams; see [AI figurines post]({{< ref "/posts/ai-figurines-3d-printing/index.md" >}}) or [software engineering journey]({{< ref "/posts/software-engineering-journey/index.md" >}}) for examples.

## Limits

- Models still hallucinate syntax sometimes — always render locally before publishing.
- Secrets belong out of prompts; diagram user/service names, not production credentials.
- OpenAI plugin churn moved the ChatGPT story toward Custom GPT + MCP; treat the D2C plugin post as historical context with a live successor.

## Project page

More badges and links: **[uml-mcp project page]({{< ref "/projects/uml-mcp" >}})**.

## Related posts

- [D2C OpenAI plugin — PlantUML, Mermaid, D2]({{< ref "/posts/d2c-openai-diagram-plugin/index.md" >}})
- [Diagram prompts with ChatGPT and AIPRM]({{< ref "/posts/chatgpt-airprm-sequence-diagrams/index.md" >}})
- [Handheld homebrew repos]({{< ref "/posts/handheld-streaming-homebrew/index.md" >}}) (unrelated stack, same "side project" bucket)
