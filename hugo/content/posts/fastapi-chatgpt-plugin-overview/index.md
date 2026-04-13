---
post_kind: article
title: "ChatGPT plugin with FastAPI — implementation outline"
date: 2024-06-01T10:00:00-04:00
description: Checklist for a minimal ChatGPT plugin — FastAPI service, OpenAPI schema, auth, and hosting.
translationKey: fastapi-chatgpt-plugin-overview
tags:
    - ChatGPT
    - OpenAI
    - FastAPI
    - Python
    - Plugin
    - Tutorial
---

OpenAI-style **plugins** expose an HTTP API described by an **OpenAPI** document so ChatGPT can call your tools safely. **FastAPI** generates OpenAPI for you, which fits this model well.

## 1. Define the API in FastAPI

- Routes return **JSON** with stable shapes (no ambiguous free text where structure matters).
- Add **summaries and descriptions** on paths and fields — they help the model choose the right tool.

## 2. Publish `openapi.json`

- FastAPI serves **`/openapi.json`** by default; the plugin manifest points at this URL (or a static copy you version).
- Keep schemas **tight**: enums, required fields, and examples reduce bad calls.

## 3. Plugin manifest

- Host **`ai-plugin.json`** (or the format required by the current OpenAI developer docs) over **HTTPS**.
- Manifest references your API base URL and OpenAPI location.

## 4. Auth

- Prefer **OAuth** or **API keys** as documented for your integration; never commit secrets.
- Validate tokens inside FastAPI dependencies or middleware.

## 5. Deploy

- **HTTPS** endpoint reachable from OpenAI’s servers.
- Logging and **idempotency** for side-effecting routes.

## 6. Test manually

- Call routes with `curl` or HTTPie using the same payloads the model will send.
- Iterate on descriptions and constraints before exposing wide traffic.

> Details change with OpenAI’s platform updates — always follow the latest **plugin / tools / actions** documentation when wiring production apps.
