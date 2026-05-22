---
post_kind: article
title: "D2C OpenAI plugin — diagrams with PlantUML, Mermaid, and D2"
date: 2022-09-06T10:00:00-04:00
lastmod: 2026-05-23T00:30:00-04:00
description: "ChatGPT plugin to generate PlantUML, Mermaid, and D2 diagrams from conversation — repo and demo."
translationKey: d2c-openai-diagram-plugin
tags:
  - ChatGPT
  - OpenAI
  - Plugin
  - PlantUML
  - Mermaid
  - D2
images:
  - featured.gif
---

**D2COpenAIPlugin** is a ChatGPT plugin that turns chat into **PlantUML**, **Mermaid**, or **D2** diagrams without leaving the thread. I built it when plugins were the hot path for extending GPT — useful for architecture sketches and teaching. **[Version française]({{< ref "/posts/d2c-openai-diagram-plugin/index.fr.md" >}})**.

<!--more-->

For a **prompt-in-chat** workflow (AIPRM templates, cache hit/miss sequences, canvas tips), see **[Diagram prompts with ChatGPT and AIPRM]({{< ref "/posts/chatgpt-airprm-sequence-diagrams" >}})** — complementary to this plugin route.

## Links

- **Repository:** [github.com/antoinebou12/D2COpenAIPlugin](https://github.com/antoinebou12/D2COpenAIPlugin)
- **Plugin listing:** [ChatGPT plugin / short link](https://lnkd.in/exVNZMnT)

## Demo

![Plugin screenshot](./images/1692387139389.jpeg)

**ChatGPT UML plugins — demo**

![Demo animation](./images/1682544541386.gif)

## What it does

- Generate **UML and system diagrams** from natural language in ChatGPT.
- Support **PlantUML**, **Mermaid**, and **D2** in one plugin surface.
- Ship with docs from install to first diagram (README on GitHub).

Feedback and PRs welcome on the repo. Related later work: **[uml-mcp](https://github.com/antoinebou12/uml-mcp)** for diagram generation from Cursor and other MCP hosts.
