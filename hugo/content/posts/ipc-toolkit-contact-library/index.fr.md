---
project_docs: ipc-toolkit
story_kind: introduction
title: "IPC Toolkit : collisions et friction dans une simulation"
date: 2026-10-24T12:00:00-04:00
description: "Comment IPC Toolkit fournit la détection de collisions, les dérivées de distance et les calculs de friction à une simulation."
translationKey: ipc-toolkit-contact-library
tags: [C++, Simulation, Logiciel libre]
post_kind: article
images: ["images/architecture.png"]
show_hero: false
---

IPC Toolkit est une bibliothèque C++ de calculs de contact. Elle fournit la détection de collisions, les dérivées de distance et les potentiels de friction. L’application gère la boucle temporelle et le solveur.

<!--more-->

## Sa place dans la simulation

La simulation transmet la géométrie de collision et le mouvement des sommets à la bibliothèque. Le schéma suit cette requête : sélection des candidats en phase large, détection continue de collisions (CCD) en phase étroite, puis retour du résultat à l’application.

{{< figure src="images/architecture.png" alt="Parcours d’une requête de contact depuis la simulation, à travers les phases large et étroite de détection continue de collisions, jusqu’au résultat" caption="La simulation lance la requête et reçoit le résultat. Elle conserve la gestion du temps et de la résolution." class="article-diagram-figure" >}}

## Les calculs disponibles

Les routines couvrent plusieurs aspects du traitement des contacts :

| Domaine | Calculs disponibles |
| --- | --- |
| Détection de collisions | Détection continue de collisions en phases large et étroite. |
| Distance | Dérivées de distance pour les arêtes et les triangles. |
| Barrières de contact | Fonctions barrière et dérivées, potentiels de barrière de distance et raideur adaptative. |
| Friction | Potentiels de friction dissipative lisse ou retardée. |

IPC Toolkit n’est pas un moteur physique complet. Le projet amont cite PolyFEM et Rigid IPC comme implémentations complètes qui utilisent la bibliothèque.

## Consulter le code et compiler

La [documentation du projet]({{< ref "/projects/notes/ipc-toolkit/index.fr.md" >}}) présente la structure du dépôt. Le [README amont](https://github.com/ipc-sim/ipc-toolkit) contient les instructions de compilation. Le [fork contributeur](https://github.com/antoinebou12/ipc-toolkit) permet de consulter les changements de ce fork.
