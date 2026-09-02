---
post_kind: article
title: "uml-mcp — diagrammes UML depuis le chat via MCP"
date: 2026-09-02T14:00:00-04:00
lastmod: 2026-09-02T14:00:00-04:00
description: "Serveur MCP open source pour diagrammes Mermaid, PlantUML et Kroki dans Cursor et ChatGPT — genèse, installation, liens vers les outils diagrammes antérieurs."
translationKey: uml-mcp-post
tags:
  - MCP
  - UML
  - Mermaid
  - PlantUML
  - Cursor
  - logiciel libre
---

[![Étoiles GitHub](https://img.shields.io/github/stars/antoinebou12/uml-mcp?style=social)](https://github.com/antoinebou12/uml-mcp)

**[uml-mcp](https://github.com/antoinebou12/uml-mcp)** est un serveur Model Context Protocol open source qui transforme des prompts d'architecture en diagrammes **Mermaid**, **PlantUML** ou **Kroki**. On décrit un système en chat ; l'outil rend du syntaxe collable dans Hugo, GitHub ou une revue de design. Il tourne dans **Cursor** et s'apparie à un [GPT personnalisé](https://github.com/antoinebou12/D2COpenAIPlugin) pour ChatGPT. Le dépôt est autour de **★ 97** — la voie diagramme que j'utilise le plus. **[English version]({{< ref "/posts/uml-mcp/index.md" >}})**.

<!--more-->

## Pourquoi MCP plutôt que des gabarits copiés-collés ?

J'ai commencé avec les plugins ChatGPT ([plugin D2C OpenAI]({{< ref "/posts/d2c-openai-diagram-plugin/index.fr.md" >}})) et les [gabarits AIPRM]({{< ref "/posts/chatgpt-airprm-sequence-diagrams/index.fr.md" >}}). Les deux marchent, mais les éditeurs voulaient des **outils natifs** : activer un serveur une fois, appeler `generate_uml` depuis l'agent, sauver `.mmd` + SVG à côté de l'article. MCP est cette couche — même idée que le plugin, autre hôte.

## Formats supportés

| Backend | Usage |
|---------|--------|
| **Mermaid** | Flux GitHub-native, séquences rapides |
| **PlantUML** | UML classique, déploiements |
| **Kroki** | Rendu unifié quand on mélange les formats |

Point de terminaison : [uml-mcp.vercel.app/mcp](https://uml-mcp.vercel.app/mcp). Site doc : [antoinebou12.github.io/uml-mcp](https://antoinebou12.github.io/uml-mcp/).

## Cursor (résumé)

1. Cloner ou installer depuis **[github.com/antoinebou12/uml-mcp](https://github.com/antoinebou12/uml-mcp)** (bloc config MCP dans le README).
2. Ajouter le serveur dans les réglages MCP de Cursor.
3. Demander le type de diagramme explicitement — ex. « séquence Mermaid : utilisateur, React, FastAPI, Postgres, login avec cache miss ».

J'utilise uml-mcp sur ce blog pour pipelines et parcours ; voir [figurines IA]({{< ref "/posts/ai-figurines-3d-printing/index.fr.md" >}}) ou [parcours ingénierie]({{< ref "/posts/software-engineering-journey/index.fr.md" >}}).

## Limites

- Le modèle invente encore parfois la syntaxe — toujours valider le rendu localement.
- Pas de secrets dans les prompts ; noms de services, pas de credentials prod.
- L'histoire plugin OpenAI a migré vers GPT personnalisé + MCP ; le post D2C reste le contexte historique.

## Page projet

Badges et liens : **[page projet uml-mcp]({{< ref "/projects/uml-mcp" >}})**.

## Articles liés

- [Plugin D2C OpenAI]({{< ref "/posts/d2c-openai-diagram-plugin/index.fr.md" >}})
- [Prompts diagrammes ChatGPT et AIPRM]({{< ref "/posts/chatgpt-airprm-sequence-diagrams/index.fr.md" >}})
- [Homebrew portable]({{< ref "/posts/handheld-streaming-homebrew/index.fr.md" >}})
