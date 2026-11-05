# uml-mcp

> Serveur MCP open source pour diagrammes UML et d'architecture — Mermaid, PlantUML et Kroki depuis le chat dans Cursor et ChatGPT.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/uml-mcp/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/uml-mcp/index.md
- Publié: 2026-09-02
- Mis à jour: 2026-09-02
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)# uml-mcp

[![Étoiles GitHub](https://img.shields.io/github/stars/antoinebou12/uml-mcp)](https://github.com/antoinebou12/uml-mcp/stargazers)
[![Dernier commit GitHub](https://img.shields.io/github/last-commit/antoinebou12/uml-mcp)](https://github.com/antoinebou12/uml-mcp)

[Dépôt](https://github.com/antoinebou12/uml-mcp) · [Licence MIT](https://github.com/antoinebou12/uml-mcp/blob/main/LICENSE) · [Documentation](https://antoinebou12.github.io/uml-mcp/) · [MCP hébergé](https://uml-mcp.vercel.app/mcp)

**uml-mcp** est un serveur **Model Context Protocol** open source qui produit des diagrammes **Mermaid**, **PlantUML** et **Kroki** à partir de prompts en langage naturel ou de source explicite. Utilisable dans **Cursor** (outils MCP) ou **ChatGPT** via un [GPT personnalisé](https://github.com/antoinebou12/D2COpenAIPlugin).

Article : [uml-mcp — diagrammes depuis le chat](https://antoineboucher.info/CV/blog/fr/posts/uml-mcp/).

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

- [D2COpenAIPlugin](https://antoineboucher.info/CV/blog/fr/projects/d2copenaiplugin/) — voie plugin ChatGPT antérieure
- [PlantUMLAPI](https://antoineboucher.info/CV/blog/fr/projects/plantumlapi/) — client Python PlantUML prédécesseur
