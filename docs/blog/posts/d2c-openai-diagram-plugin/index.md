# D2C OpenAI plugin — diagrams with PlantUML, Mermaid, and D2

> ChatGPT plugin for PlantUML, Mermaid, and D2 diagrams — why I built it, install path, example prompts, and limits vs AIPRM templates.

- HTML page: https://antoineboucher.info/CV/blog/posts/d2c-openai-diagram-plugin/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/posts/d2c-openai-diagram-plugin/index.md
- Published: 2022-09-06
- Updated: 2026-05-22
- Tags: ChatGPT, OpenAI, Plugin, PlantUML, Mermaid, D2
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)**D2COpenAIPlugin** is a ChatGPT plugin that turns conversation into **PlantUML**, **Mermaid**, or **D2** without leaving the thread. I built it when OpenAI plugins were the main extension story — useful for architecture sketches, lab docs, and “draw this flow” moments in chat.

## User story

A teammate describes a flow in chat; I need a **sequence diagram in the repo** ten minutes later. Before the plugin, that meant exporting a whiteboard photo or hand-typing PlantUML from memory. With **D2C**, the model emits syntax, the plugin renders it, and I paste the result into Markdown — same loop I use today with MCP, different host.

## Why not only screenshots?

Whiteboards do not paste into Markdown repos. I wanted **text-native diagrams** I could drop into Hugo posts, GitHub READMEs, and design reviews — the same motivation as later **[Diagram prompts with ChatGPT and AIPRM](https://antoineboucher.info/CV/blog/posts/chatgpt-airprm-sequence-diagrams/)**, but wired as a **plugin action** instead of a pasted template.

## Original workflow

In the original plugin workflow, the request named the diagram type explicitly, for example a PlantUML sequence for React, an API, Redis, and a database. The [project documentation](https://antoineboucher.info/CV/blog/projects/notes/d2copenaiplugin/) covers the service and its setup.

The model still hallucinates syntax sometimes; the plugin’s job is to **route** to the right renderer, not to guarantee perfect UML.

## Demo

Static capture of the plugin surface in ChatGPT:

![Plugin screenshot — diagram output in the ChatGPT thread](https://antoineboucher.info/CV/blog/posts/d2c-openai-diagram-plugin/images/1692387139389.jpeg)

Animated walkthrough:

![Demo animation — generating UML from chat](https://antoineboucher.info/CV/blog/posts/d2c-openai-diagram-plugin/images/1682544541386.gif)

## What it supports

| Format | Good for |
|--------|----------|
| **PlantUML** | UML sequences, classes, deployments in docs |
| **Mermaid** | GitHub-native diagrams, quick flows |
| **D2** | Modern declarative system sketches |

## Example prompts that worked

```text
Sequence diagram in PlantUML: user, React app, FastAPI, Postgres — include login and cache miss path.
```

```text
Mermaid flowchart: CI pipeline from git push to deploy on AWS — lint, test, build image, ECR, ECS.
```

```text
D2 diagram: homelab — Caddy on EC2, CloudWatch logs, Lambda alerts (keep boxes readable).
```

## Limits

- **Plugin platform churn** — OpenAI’s plugin story moved; treat this as historical tooling plus repo reference.
- **Validation** — always render locally (PlantUML server, Mermaid live editor) before publishing.
- **Secrets** — never ask the model to diagram production credentials inline.

Successor-style work for editors: **[uml-mcp](https://github.com/antoinebou12/uml-mcp)** for Cursor and MCP hosts.

## Related posts

- [GitHub Copilot session at Cédille](https://antoineboucher.info/CV/blog/posts/github-copilot-cedille-session/) — same era of AI dev tooling talks
- [Diagram prompts with ChatGPT and AIPRM](https://antoineboucher.info/CV/blog/posts/chatgpt-airprm-sequence-diagrams/)
