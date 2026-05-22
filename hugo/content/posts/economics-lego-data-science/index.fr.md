---
post_kind: article
title: "Économie des boîtes LEGO avec science des données"
date: 2024-05-30T12:00:00-04:00
lastmod: 2026-05-22T16:00:00-04:00
description: "Tendances Rebrickable, prix BrickEconomy, scraping Playwright, régression sur le set 001-1 — récit avec graphiques, code dans LegosTracker."
translationKey: economics-lego-data-science
tags:
  - LEGO
  - Data Science
  - Pandas
  - Scraping
  - Playwright
canonicalURL: "https://medium.com/@antoine.boucher012/economics-of-lego-sets-with-data-science-a4ca07d613fb"
---

Je collectionne le LEGO et j’écris du Python — croisement des exports **Rebrickable** avec un scraper **BrickEconomy** pour voir l’évolution des sets, couleurs et thèmes, et tester une régression simple sur le **001-1**. Récit et graphiques ici ; notebooks complets dans **[AlgoETS/LegosTracker](https://github.com/AlgoETS/LegosTracker)**. **[English version]({{< ref "/posts/economics-lego-data-science/index.md" >}})**.

<!--more-->

## Sources

| Source | Apport |
|--------|--------|
| **CSV Rebrickable** | sets, thèmes, pièces, couleurs, inventaires |
| **BrickEconomy (scrapé)** | prix secondaire que Rebrickable ne fournit pas |

![Vue d’ensemble des tables](./img-001.png)

## Sets dans le temps

1. **Nombre de sets par an** augmente.
2. **Pièces moyennes par set** monte — modèles plus denses.

![Sets par année](./img-002.png)

![Pièces moyennes par année](./img-003.png)

## Thèmes dominants

Jointure `theme_id`, thèmes racine, top 10 par volume.

![Top 10 thèmes](./img-004.png)

## Scraper BrickEconomy

**Playwright + asyncio**, validation **pydantic** — code et garde-fous dans le dépôt `LegosTracker`.

![Workflow scraper](./img-005.png)

## Prix du 001-1

Charger `001-1_history.csv` / `001-1_new.csv`, nettoyer, tracer dans le temps.

![Série de prix 001-1](./img-006.png)

## Régression linéaire

Modèle simple pour pratiquer l’interprétation — pas de « alpha » boursier sur la brique.

![Ajustement et résidus](./img-010.png)

![Prédit vs observé](./img-011.png)

Détails : [Medium](https://medium.com/@antoine.boucher012/economics-of-lego-sets-with-data-science-a4ca07d613fb) et notebooks GitHub.

## Extraits notebook

Les one-liners pandas restent dans le dépôt — pas recollés ici.

![Graphiques exploratoires](./img-012.png)

## Limites

Scraper cassé, sets disparus du catalogue, hype collector, confusion MSRP / revente.

## Bilan

Données LEGO = pandas + scraping + humilité sur les prix secondaires.

## Articles liés

- [Bases vectorielles / films]({{< ref "/posts/vector-databases-similar-movies/index.fr.md" >}})
- [Bibliothèque MarketWatch]({{< ref "/posts/marketwatch-python-trading/index.fr.md" >}})

## Références

- [Rebrickable](https://rebrickable.com/downloads/)
- [BrickEconomy](https://www.brickeconomy.com)
- [AlgoETS/LegosTracker](https://github.com/AlgoETS/LegosTracker)

---

*Publié d’abord sur [Medium](https://medium.com/@antoine.boucher012/economics-of-lego-sets-with-data-science-a4ca07d613fb).*
