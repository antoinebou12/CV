---
post_kind: conference
title: "GraphQuon 2025 — Université de Toronto"
date: 2025-11-15T10:00:00-05:00
lastmod: 2026-05-22T23:30:00-05:00
description: "Présentation Where to Wear? à l’atelier pré-SIGGRAPH Québec–Ontario à Toronto — usure frictionnelle, textures et diapositives GraphQuon 2025."
translationKey: graphquon-2025-university-of-toronto
tags:
  - Conference
  - GraphQuon
  - Université de Toronto
  - SIGGRAPH
  - Infographie
  - Friction
  - ÉTS
canonicalURL: "https://www.dgp.toronto.edu/graphquon/"
images:
  - featured.png
---

![Badge GraphQuon 2025 — Antoine Boucher, École de technologie supérieure, skyline de Toronto](./images/graphquon-name-badge.png)

**GraphQuon** est l’atelier annuel Québec–Ontario pré-SIGGRAPH. L’édition **2025** s’est tenue les **15 et 16 novembre 2025** à l’**Université de Toronto** ([page de la série](https://www.dgp.toronto.edu/graphquon/)). J’y ai **présenté** avec **Sheldon Andrews** (ÉTS) : **Where to Wear?** — comment le contact frictionnel écrit l’histoire d’une surface, et comment en faire un retour utile en infographie et en génie. **[English version]({{< ref "/posts/graphquon-2025-university-of-toronto/index.md" >}})**.

<!--more-->

## Ce que j’ai présenté

Titre : **Where to Wear?** (sous-titre sur la première diapo : *Every surface has a biography written by frictional contact*).

L’idée est simple à dire et exigeante à simuler : le **temps**, le **contact** et la **dissipation d’énergie** modifient l’apparence et le comportement d’une surface — des traces d’usure dans des salles de bain d’école d’ingénierie aux rayures sur outils, matériaux de jeu et préhenseurs robotiques. Les diapos vont de la motivation à la mécanique (usure d’Archard, lois énergétiques), puis à un **pipeline orienté rendu** (masque de contact, volumes orthographiques, champs de vitesse et de traction tangentiels, intégration en texture), et à des pistes de validation (**capture GelSight**, interpolation d’atlas de matériaux).

![Diapo d’ouverture — Where to Wear? Antoine Boucher et Sheldon Andrews, ÉTS](./images/slide-01.png)

### Pipeline (en un coup d’œil)

Rendu avec [uml-mcp](https://github.com/antoinebou12/uml-mcp) depuis [`wear-pipeline-flow.mmd`](./images/wear-pipeline-flow.mmd) :

![Pipeline de simulation d’usure — contact, vitesse, traction, texture, atlas](./images/wear-pipeline-flow.svg)

![Diapo pipeline — des entrées de contact à l’usure en texture](./images/slide-15.png)

![Diapo exemple](./images/slide-22.png)

### Pourquoi GraphQuon

GraphQuon, c’est l’endroit où les **labos d’infographie du Québec et de l’Ontario** partagent leurs travaux avant la saison SIGGRAPH — exposés courts, affiches et retours francs de gens qui construisent simulateurs et moteurs de rendu. Après avoir contribué au site **[GraphQuon 2024]({{< ref "/posts/graphquon-2024-ets" >}})** à l’ÉTS, présenter à Toronto en 2025, c’était la même communauté, de l’autre côté du trajet.

Ce fil de recherche rejoint mon travail à l’**ÉTS** sur la **fabrication et validation de surfaces 3D avec frottement** ([description du projet](https://www.etsmtl.ca/recherche/etudes-superieures-et-recherche/projets-de-recherche-pour-etudiants/3d-fabrication-and-validation-of-frictional-su-1)).

## Diapositives et téléchargements

| Format | Fichier | Notes |
|--------|---------|--------|
| **PDF** | [graphquon-2025-where-to-wear.pdf](./graphquon-2025-where-to-wear.pdf) | Export complet (28 diapos). Idéal pour lecture dans le navigateur. |
| **PowerPoint** | [graphquon-final.pptx](./graphquon-final.pptx) | Présentation éditable d’origine (~116 Mo). Téléchargement ci-dessous ; aperçu : préférer le PDF. |

**PowerPoint (.pptx)** — présentation complète avec actifs embarqués :

{{< deck src="graphquon-final.pptx" title="GraphQuon 2025 — Where to wear" label="Télécharger les diapositives GraphQuon (.pptx)" size="~116 Mo" viewer="false" >}}

## Toronto, novembre 2025

Quelques photos du séjour — badge, architecture près du campus, et promenades en centre-ville entre les sessions.

![Centre-ville de Toronto la nuit — Tour CN et immeuble Bell Media](./images/toronto-cn-tower-night.png)

![Sharp Centre for Design (OCAD) la nuit — bâtiment « table » sur pilotis colorés](./images/ocad-sharp-centre-night.png)

![Place Yonge–Dundas la nuit — écrans publicitaires et trottoir mouillé](./images/yonge-dundas-square-night.png)

![Murale musique — secteur Yonge Street](./images/toronto-music-mural.png)

![Rencontre informelle avec d’autres participant·es](./images/graphquon-social-gathering.png)

![Bord de l’eau en Ontario — maisons reliées par une passerelle au crépuscule](./images/ontario-waterfront-bridge.png)

## Liens

- [GraphQuon 2025 — DGP, Université de Toronto](https://www.dgp.toronto.edu/graphquon/)
- [GraphQuon 2024 à l’ÉTS (Montréal)]({{< ref "/posts/graphquon-2024-ets" >}}) · [graphquon.github.io](https://graphquon.github.io/)
- [ÉTS — projet surfaces à frottement](https://www.etsmtl.ca/recherche/etudes-superieures-et-recherche/projets-de-recherche-pour-etudiants/3d-fabrication-and-validation-of-frictional-su-1)
