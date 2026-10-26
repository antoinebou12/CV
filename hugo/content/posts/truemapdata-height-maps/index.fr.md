---
title: "TrueMapData : des cartes mesurées aux ressources utilisables"
date: 2026-10-24T12:00:00-04:00
description: "TrueMapData relie les fichiers TrueMap et GelSight à la visualisation, aux métriques de surface, à l’analyse d’usure et à l’export de maillages."
translationKey: truemapdata-height-maps
tags: [Python, Métrologie, Infographie]
post_kind: article
---

TrueMapData part d’une carte de hauteur mesurée et garde visible le chemin vers un résultat utilisable. **[English version]({{< ref "/posts/truemapdata-height-maps/index.md" >}})**.

<!--more-->

Le projet lit les fichiers de style TrueMap v6 et les anciens formats, ainsi que les dispositions compatibles avec GelSight. Sa CLI `tmd-process` et sa bibliothèque Python couvrent filtres, transformations, cartes normales et de déplacement, détection de défauts, export de séquences, compression et formats de maillage.

Le même dépôt va vers l’analyse des surfaces. Le support optionnel de Surfalize couvre la rugosité ISO 25178; les commandes de tribologie et d’usure traitent des captures alignées, des courbes de contact, des séries de volume usé, des rayures et des cartes liées aux débris. L’export de maillage peut appliquer des textures dérivées de la hauteur à un modèle en utilisant les métadonnées de capture.

Cette combinaison sert deux parcours voisins : une surface mesurée peut alimenter une question de métrologie ou devenir une ressource visuelle pour une chaîne graphique. La [note TrueMapData]({{< ref "/projects/notes/truemapdata/index.fr.md" >}}) rassemble le dépôt et la documentation.

- [Dépôt TrueMapData](https://github.com/ETSim/TrueMapData)
- [Documentation](https://etsim.github.io/TrueMapData/)
