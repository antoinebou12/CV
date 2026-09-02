---
title: "uml-mcp"
date: 2026-09-02T14:00:00-04:00
description: "Serveur MCP open source pour diagrammes UML et d'architecture — Mermaid, PlantUML et Kroki depuis le chat dans Cursor et ChatGPT."
draft: false
---

# uml-mcp

[![Étoiles GitHub](https://img.shields.io/github/stars/antoinebou12/uml-mcp)](https://github.com/antoinebou12/uml-mcp/stargazers)
[![Dernier commit GitHub](https://img.shields.io/github/last-commit/antoinebou12/uml-mcp)](https://github.com/antoinebou12/uml-mcp)

[Dépôt](https://github.com/antoinebou12/uml-mcp) · [Licence MIT](https://github.com/antoinebou12/uml-mcp/blob/main/LICENSE) · [Documentation](https://antoinebou12.github.io/uml-mcp/) · [MCP hébergé](https://uml-mcp.vercel.app/mcp)

**uml-mcp** est un serveur **Model Context Protocol** open source qui produit des diagrammes **Mermaid**, **PlantUML** et **Kroki** à partir de prompts en langage naturel ou de source explicite. Utilisable dans **Cursor** (outils MCP) ou **ChatGPT** via un [GPT personnalisé](https://github.com/antoinebou12/D2COpenAIPlugin).

Article : [uml-mcp — diagrammes depuis le chat]({{< ref "/posts/uml-mcp/index.fr.md" >}}).

## Fonctions

- Outils MCP `generate_uml` et apparentés pour séquences, classes, flux, déploiements
- Plusieurs moteurs de rendu (Mermaid, PlantUML, Kroki)
- Utilisé sur ce blog pour diagrammes `.mmd` + SVG inline

## Démarrage

```bash
git clone https://github.com/antoinebou12/uml-mcp.git
cd uml-mcp
```

Suivre le README pour les dépendances Python et la config MCP Cursor.

## Voir aussi

- [D2COpenAIPlugin]({{< ref "/projects/D2COpenAIPlugin" >}}) — voie plugin ChatGPT antérieure
- [PlantUMLAPI]({{< ref "/projects/PlantUMLAPI" >}}) — client Python PlantUML prédécesseur
