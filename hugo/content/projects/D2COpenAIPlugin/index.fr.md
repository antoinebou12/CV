---
title: "D2COpenAIPlugin"
linkTitle: "D2COpenAIPlugin"
date: 2021-09-06T22:42:23+08:00
draft: false
description: "Extension ChatGPT pour générer des diagrammes PlantUML ou Mermaid."
tags:
    - ChatGPT
    - OpenAI
    - Plugin
    - PlantUML
    - Mermaid
---

Cette page présente une ancienne extension ChatGPT. La [documentation du projet]({{< ref "/projects/notes/d2copenaiplugin/index.fr.md" >}}) détaille son implémentation et ses routes API. Le [dépôt source](https://github.com/antoinebou12/D2COpenAIPlugin) conserve le code d’origine.

D2COpenAIPlugin est une extension ChatGPT qui génère des diagrammes PlantUML ou Mermaid depuis la conversation.

![Diagram generator plugin demo](https://raw.githubusercontent.com/antoinebou12/UMLOpenAIPlugin/main/docs/DiagramGeneratorPlugin.gif)
![image](https://github.com/antoinebou12/D2COpenAIPlugin/assets/13888068/638e6ef6-b006-4f63-a7b8-b765fc0d8a41)

## Fonctionnalités

- Diagrammes PlantUML ou Mermaid
- Intégration avec ChatGPT
- Interface orientée création de schémas

## Installation d’origine (aperçu)

Prérequis typiques : Python 3.10+, FastAPI, uvicorn. Cloner le dépôt, installer les dépendances (poetry ou `requirements-dev.txt`), configurer les variables d’environnement et un jeton bearer, puis lancer l’API (par ex. `uvicorn app:app --host 127.0.0.1 --port 5003`).

Les étapes détaillées (ChatGPT, manifeste, tests locaux) sont documentées en anglais dans le [README du dépôt](https://github.com/antoinebou12/D2COpenAIPlugin).

## Aide

Pour les questions sur le développement d’extensions : [forum développeurs OpenAI](https://community.openai.com/c/chat-plugins/20).
