---
title: "D2COpenAIPlugin"
linkTitle: "D2COpenAIPlugin"
date: 2021-09-06T22:42:23+08:00
draft: false
description: "A plugin for ChatGPT that enables users to generate diagrams using PlantUML or Mermaid."
tags:
    - ChatGPT
    - OpenAI
    - Plugin
    - PlantUML
    - Mermaid
---

This is a historical ChatGPT plugin. Read the [project documentation]({{< ref "/projects/notes/d2copenaiplugin/index.md" >}}) for its implementation and API routes, or consult the [source repository](https://github.com/antoinebou12/D2COpenAIPlugin).

D2COpenAIPlugin is a ChatGPT plugin that generates diagrams with PlantUML or Mermaid from the conversation.

![Diagram generator plugin demo](https://raw.githubusercontent.com/antoinebou12/UMLOpenAIPlugin/main/docs/DiagramGeneratorPlugin.gif)
![image](https://github.com/antoinebou12/D2COpenAIPlugin/assets/13888068/638e6ef6-b006-4f63-a7b8-b765fc0d8a41)

## Features
- Generate diagrams using PlantUML or Mermaid
- Works as a ChatGPT plugin
- Diagram-oriented UI

## Original local setup

These instructions describe the original plugin environment.
Before using the plugin, make sure to have the following prerequisites installed:

- Python 3.6+
- FastAPI
- uvicorn

1. Install Python 3.10, if not already installed.
2. Clone the repository: `git clone https://github.com/antoinebou12/D2COpenAIPlugin.git`
3. Navigate to the cloned repository directory: `cd /path/to/D2COpenAIPlugin`
4. Install poetry: `pip install poetry`
5. Create a new virtual environment with Python 3.10: `poetry env use python3.10`
6. Activate the virtual environment: `poetry shell`
7. Install app dependencies: `poetry install`
8. Consult the repository README for authentication and environment configuration.

## Setup

To install the required packages for this plugin, run the following command:

```bash
pip install -r requirements-dev.txt
```

To run the plugin, enter the following command:

```bash
python app.py
```

The original local server command was:

```bash
uvicorn app:app --host 127.0.0.1 --port 5003
```

The original manifest and configuration remain in the source repository.
