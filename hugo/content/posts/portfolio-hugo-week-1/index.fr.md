---
post_kind: article
title: "Créer un portfolio avec Hugo (semaine 1)"
date: 2024-01-06T10:00:00-04:00
lastmod: 2026-05-22T16:00:00-04:00
description: "Semaine 1 portfolio Hugo — compromis HBTheme, embeds data, Substack, shortcode iframe, ce que je ferais autrement aujourd’hui."
translationKey: portfolio-hugo-week-1
tags:
  - Hugo
  - Portfolio
  - Static Site
  - Substack
images:
  - featured.png
---

Semaine 1 de migration vers **Hugo** (janvier 2024) : thème, déploiement rapide, prouver que le dépôt peut porter plus qu’un PDF de CV. **HBTheme**, embed data, **Substack** à côté, shortcode **iframe**. **[English version]({{< ref "/posts/portfolio-hugo-week-1/index.md" >}})**.

<!--more-->

![Aperçu du site après premier déploiement](./featured.png)

## Pourquoi Hugo sans CMS

| Choix | Raison |
|-------|--------|
| **Génération statique** | Hébergement peu coûteux, builds rapides |
| **Markdown** | Articles et projets versionnés dans git |
| **Modules** | Thème + partials sans tout copier |

Le **dépôt = source de vérité** : Markdown → HTML → GitHub Pages ou équivalent.

## HBTheme semaine 1

Commentaires, assets npm, modules Hugo — pas tout recoder.

Compromis :

- **Structure opinionated** — démarrage vite, friction plus tard pour des types de contenu custom
- **Pipeline assets** — étapes npm en CI mais SCSS/JS propres
- **Doc du thème** — plus utile que la doc Hugo en semaine 1

## Données dans la page

Test : intégrer l’étude des **vols de voitures à Montréal** (Substack d’un ami) — preuve que Hugo peut porter longform et graphiques, pas seulement des billets courts.

[Étude des vols de voitures à Montréal](https://mohamedilias.substack.com/p/etude-des-vols-de-voitures-a-montreal)

Leçon : **iframe ou lien** pour du contenu invité ; graphiques natifs plus tard avec page bundles.

## Substack en parallèle

Essais longs et audience newsletter. Hugo = shell pro ; Substack = format email/commentaires sans serveur mail maison.

## Shortcode iframe

```text
{{</* iframe src="https://example.com/" title="Exemple" height="480" */>}}
```

Exemple **FlashGames** :

{{< iframe src="https://antoinebou12.github.io/FlashGames/" title="FlashGames" height="420" referrerpolicy="no-referrer-when-downgrade" >}}

À utiliser avec parcimonie (accessibilité, mobile, cookies tiers).

## Depuis la semaine 1

Site actuel : bilingue, notes de conférence, posts MCP. Voir **[CV JSON Resume]({{< ref "/posts/professional-resume-json-resume/index.fr.md" >}})**.

## Articles liés

- [Parcours en génie logiciel]({{< ref "/posts/software-engineering-journey/index.fr.md" >}})
- [Prompts diagrammes ChatGPT et AIPRM]({{< ref "/posts/chatgpt-airprm-sequence-diagrams/index.fr.md" >}})
