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

## Mes contributions

Le fork [antoinebou12/ipc-toolkit](https://github.com/antoinebou12/ipc-toolkit) sert à préparer les changements avant de les proposer en amont. Les demandes de fusion ci-dessous sont le registre public (GitHub, relevé du 2026-11-05) ; le statut est celui que GitHub indique.

| Demande de fusion | Ouverte | Statut |
| --- | --- | --- |
| [ipc-sim/ipc-toolkit #210 — Friction anisotrope](https://github.com/ipc-sim/ipc-toolkit/pull/210) | 2026-02 | Fusionnée le 2026-04-16 |
| [ipc-sim/ipc-toolkit #208 — Paramètres transmis à la phase fine de Scalable CCD](https://github.com/ipc-sim/ipc-toolkit/pull/208) | 2026-01 | Fusionnée le 2026-01-26 |
| [ipc-sim/ipc-toolkit #144 — Brouillon de documentation sur l’adhésion](https://github.com/ipc-sim/ipc-toolkit/pull/144) | 2024-11 | Fusionnée le 2024-12-11 |
| [ipc-sim/ipc-toolkit #139 — Coefficients statique et cinétique dans la force tangentielle de collision](https://github.com/ipc-sim/ipc-toolkit/pull/139) | 2024-11 | Fermée sans fusion |
| [ipc-sim/ipc-toolkit #128 — Friction statique et cinétique par paire de matériaux](https://github.com/ipc-sim/ipc-toolkit/pull/128) | 2024-11 | Fermée sans fusion |
| [Continuous-Collision-Detection/Scalable-CCD #5 — Retrait de `-fpic` pour la compilation CUDA Windows (vcpkg)](https://github.com/Continuous-Collision-Detection/Scalable-CCD/pull/5) | 2024-09 | Fusionnée le 2024-09-27 |
| [Continuous-Collision-Detection/Scalable-CCD #6 — Tests sur plusieurs versions de CUDA](https://github.com/Continuous-Collision-Detection/Scalable-CCD/pull/6) | 2024-09 | Fermée sans fusion |

Deux demandes de préparation restent ouvertes sur le fork : [#3 — extraire la tolérance et le nombre maximal d’itérations de TightInclusionCCD pour la CCD GPU](https://github.com/antoinebou12/ipc-toolkit/pull/3) et [#4 — friction anisotrope](https://github.com/antoinebou12/ipc-toolkit/pull/4), la branche derrière la #210 en amont.

Le fil conducteur : une friction qui dépend de la direction et de la paire de matériaux, ce dont mon travail de mémoire sur l’usure de surface avait besoin dans le modèle de contact, plus le chemin de détection continue de collision sur GPU (Scalable CCD) que la compilation Windows et la transmission des paramètres ont débloqué.

## Consulter le code et compiler

La [documentation du projet]({{< ref "/projects/notes/ipc-toolkit/index.fr.md" >}}) présente la structure du dépôt. Le [README amont](https://github.com/ipc-sim/ipc-toolkit) contient les instructions de compilation. Le [fork contributeur](https://github.com/antoinebou12/ipc-toolkit) permet de consulter les changements de ce fork.
