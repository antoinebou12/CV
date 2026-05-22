---
post_kind: conference
title: "Conférence Snowflake Data-for-Breakfast — notes"
date: 2022-09-06T10:00:00-04:00
lastmod: 2026-05-22T16:00:00-04:00
description: "Notes élargies — santé à l’échelle, fiscalité, clean rooms, keynote Infostrux, quand un entrepôt bat les feuilles."
translationKey: snowflake-data-for-breakfast
tags:
  - Conference
  - Snowflake
  - Data Analytics
images:
  - featured.jpeg
---

**Snowflake Data-for-Breakfast** : matinée sur l’entrepôt cloud, le partage, la gouvernance et des histoires clients qui rendent l’architecture concrète. J’y suis allé pour l’exploitation réelle, pas les goodies. Keynote **Infostrux**. **[English version]({{< ref "/posts/snowflake-data-for-breakfast/index.md" >}})**.

<!--more-->

## Pourquoi

Assez de SQL pour être dangereux, pas assez d’histoires de prod. Format petit-déjeuner = faible engagement, vocabulaire utile (**clean room**, **share**, politiques de lignes) avant midi.

## Matériel d’ouverture

![Supports — gouvernance et positionnement](./images/governed.jpeg)

Snowflake cadré comme **partage gouverné** d’abord, vitesse brute ensuite — pertinent quand la peur est « on ne peut pas exposer cette table ».

![Menu événement](./images/menu.jpeg)

### Santé mondiale

Client santé sur **trois continents** — partage partenaire sans sacrifier SLA.

| Leçon | Détail |
|-------|--------|
| **Réplication + gouvernance** | Conformité liée au partage live |
| **Budgets latence** | Pas seulement du batch nocturne |
| **Contrats de partage** | Juridique + objets techniques |

![Partage de données](./images/sharethrough.jpeg)

![Architecture multi-régions](./images/architecture.jpeg)

### Fiscalité à grande échelle

Gros volumes, questions ad hoc sans script fixe à l’avance.

![À propos](./images/aboutus.jpeg)

![Histoire client](./images/customer.jpeg)

Couche unique de consolidation = dépannage plus rapide, **lignée** expliquable aux auditeurs ; moins de CSV par courriel.

### Clean rooms

Due diligence : comparer des données qui se chevauchent sans tout fusionner.

![Sécurité et gouvernance](./images/security.jpeg)

Collaboration préservant la vie privée — pas qu’une case conformité.

## Tableau comparatif

| Pattern | Bon usage | Vigilance |
|---------|-----------|-----------|
| **Entrepôt central** | Dimensions partagées | Coût sans discipline requêtes |
| **Data sharing** | Partenaires live | Contrats + politiques |
| **Clean room** | Analyses sensibles | Temps de setup |
| **Montée compute** | Pics exploratoires | Entrepôts laissés allumés |

## Bilan

Vocabulaire plus clair même sans Snowflake au quotidien. Même saison que **[Run:ai sur AWS]({{< ref "/posts/runai-aws-inference-webinar/index.fr.md" >}})**.

## Articles liés

- [Bases vectorielles et films similaires]({{< ref "/posts/vector-databases-similar-movies/index.fr.md" >}})
- [Économie des LEGO et data science]({{< ref "/posts/economics-lego-data-science/index.fr.md" >}})
