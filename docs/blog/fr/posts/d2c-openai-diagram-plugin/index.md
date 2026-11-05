# Plugin OpenAI D2C — diagrammes PlantUML, Mermaid et D2

> Plugin ChatGPT pour diagrammes PlantUML, Mermaid et D2 — genèse, installation, exemples de prompts, limites vs gabarits AIPRM.

- Page HTML: https://antoineboucher.info/CV/blog/fr/posts/d2c-openai-diagram-plugin/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/posts/d2c-openai-diagram-plugin/index.md
- Publié: 2022-09-06
- Mis à jour: 2026-05-22
- Tags: ChatGPT, OpenAI, Plugin, PlantUML, Mermaid, D2
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)**D2COpenAIPlugin** est un plugin ChatGPT qui produit du **PlantUML**, **Mermaid** ou **D2** dans la conversation. Je l’ai écrit quand les plugins OpenAI étaient la voie d’extension principale — pratique pour l’architecture, les labs et les « dessine ce flux » en chat.

## Pourquoi pas seulement des captures ?

Les tableaux blancs ne collent pas dans un dépôt Markdown. Je voulais des **diagrammes texte** pour Hugo, GitHub et les revues de design — même motivation que **[prompts AIPRM](https://antoineboucher.info/CV/blog/fr/posts/chatgpt-airprm-sequence-diagrams/)**, mais en **action plugin**.

## Fonctionnement d’origine

Dans le fonctionnement d’origine, la demande nommait explicitement le type de diagramme. La [documentation du projet](https://antoineboucher.info/CV/blog/fr/projects/notes/d2copenaiplugin/) décrit le service et son installation.

Le modèle peut encore inventer de la syntaxe ; le plugin **route** vers le bon rendu, il ne garantit pas l’UML parfait.

## Démo

![Capture du plugin dans ChatGPT](./images/1692387139389.jpeg)

![Animation de démo](./images/1682544541386.gif)

## Formats

| Format | Usage |
|--------|--------|
| **PlantUML** | Séquences UML, classes, déploiement |
| **Mermaid** | Diagrammes natifs GitHub |
| **D2** | Schémas système déclaratifs |

## Exemples de prompts

```text
Diagramme de séquence PlantUML : utilisateur, React, FastAPI, Postgres — login et cache miss.
```

```text
Flowchart Mermaid : CI de git push à déploiement AWS.
```

```text
Diagramme D2 : homelab Caddy, CloudWatch, Lambda — boîtes lisibles.
```

## Limites

- **Évolution plateforme** — traiter comme outillage historique + dépôt.
- **Validation** — toujours rendre localement avant publication.
- **Secrets** — ne jamais diagrammer des credentials prod dans le chat.

Suite éditeurs : **[uml-mcp](https://github.com/antoinebou12/uml-mcp)**.

## Articles liés

- [Session Copilot à Cédille](https://antoineboucher.info/CV/blog/fr/posts/github-copilot-cedille-session/)
- [Prompts diagrammes ChatGPT et AIPRM](https://antoineboucher.info/CV/blog/fr/posts/chatgpt-airprm-sequence-diagrams/)
