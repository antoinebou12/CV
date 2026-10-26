---
post_kind: article
title: "uml-mcp — diagrammes UML depuis le chat via MCP"
date: 2026-09-02T14:00:00-04:00
lastmod: 2026-10-20T10:00:00-04:00
mermaid: true
images: ["images/featured.png"]
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

**[uml-mcp](https://github.com/antoinebou12/uml-mcp)** fournit de vrais outils de diagrammes aux clients MCP : l’assistant transmet une source Mermaid, PlantUML ou un autre format pris en charge, puis le serveur renvoie un rendu et des liens. Le dépôt documente cinq outils et environ 37 types via Kroki. Ces chiffres décrivent l’interface, pas un benchmark. **[English version]({{< ref "/posts/uml-mcp/index.md" >}})**.

{{< repo_snapshot "antoinebou12/uml-mcp" >}}

![Séquence Mermaid client/serveur rendue dans le chat, tirée du dépôt](images/featured.png)

<!--more-->

## Du code Mermaid aux liens

```mermaid
sequenceDiagram
  participant C as Client MCP
  participant U as UML-MCP
  participant R as Moteur de rendu
  C->>U: generate_uml avec source et type
  U->>U: Vérifier la requête
  U->>R: Construire la demande de rendu
  R-->>U: Diagramme rendu
  U-->>C: URL, lien éditeur ou image
```

Le module [`tools/kroki/mermaid.py`](https://github.com/antoinebou12/uml-mcp/blob/main/tools/kroki/mermaid.py) construit un état JSON, le compresse avec zlib et l’encode en base64 compatible avec les URL. Cette source alimente un lien d’image et un lien d’édition mermaid.live.

Le code distingue le SVG, servi sous `/svg/`, des images PNG/JPEG/WebP sous `/img/?type=...`. Une erreur de chemin peut donc casser un diagramme même si la source Mermaid est correcte.

Le dépôt propose aussi `generate_uml_image`, `validate_uml`, `list_diagram_types` et `generate_uml_batch`. Le choix dépend du besoin : aperçu dans le chat, contrôle de la source ou plusieurs rendus.

## Le serveur a aussi une interface d’administration

Le README actuel documente `uml-mcp admin`, des métriques et un playground Kroki. Ces outils aident à distinguer une mauvaise source, un moteur indisponible et un problème de configuration. Ils ne remplacent pas la vérification du diagramme produit.

Pour un autre usage de la même idée, voir [ComfyUI-UML]({{< ref "/posts/comfyui-uml-diagram-workflows/index.fr.md" >}}).


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
