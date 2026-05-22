---
post_kind: article
title: "Créer un portfolio avec Hugo (semaine 1)"
date: 2024-01-06T10:00:00-04:00
lastmod: 2026-05-23T00:30:00-04:00
description: "Semaine 1 d’un portfolio Hugo — thème, données embarquées, Substack et shortcode iframe."
translationKey: portfolio-hugo-week-1
tags:
  - Hugo
  - Portfolio
  - Static Site
  - Substack
images:
  - featured.png
---

Semaine 1 de migration vers **Hugo** : choisir un thème, publier vite, et brancher du contenu au-delà du PDF de CV. Thème (**HBTheme**), embed d’une histoire data, **Substack** en parallèle, shortcode **iframe**. **[English version]({{< ref "/posts/portfolio-hugo-week-1/index.md" >}})**.

<!--more-->

![Aperçu du site](./featured.png)

## Pourquoi Hugo

Génération statique, builds courts, modules sans CMS lourd. Le dépôt comme source de vérité — Markdown → HTML → déploiement peu coûteux.

**HBTheme** : commentaires, assets npm, modules Hugo — pas tout recoder à la main.

## Données dans la page

Premier test : intégrer une analyse des **vols de voitures à Montréal** (projet Substack d’un ami) — preuve que Hugo peut porter graphiques et longform, pas seulement des billets courts.

[Étude des vols de voitures à Montréal](https://mohamedilias.substack.com/p/etude-des-vols-de-voitures-a-montreal)

## Substack à côté

**Substack** pour les essais longs et une autre audience. Hugo pour le portfolio ; Substack quand le format newsletter convient mieux.

## Shortcode iframe

Pages HTTPS via le shortcode `iframe` du site (`src` obligatoire ; `title`, `height`, etc. optionnels) :

```text
{{</* iframe src="https://example.com/" title="Exemple" height="480" */>}}
```

Exemple — démo **FlashGames** :

{{< iframe src="https://antoinebou12.github.io/FlashGames/" title="FlashGames" height="420" referrerpolicy="no-referrer-when-downgrade" >}}

## Suite

Modules Hugo, esthétique (tests particles.js), lien blog ↔ projets. Le site actuel part de cette base — voir **Articles** sur le blog.
