---
title: "IPC Toolkit : une bibliothèque de contacts pour les simulations"
date: 2026-10-24T12:00:00-04:00
description: "IPC Toolkit fournit des routines réutilisables de collision, CCD, distance et friction sans posséder la boucle de simulation."
translationKey: ipc-toolkit-contact-library
tags: [C++, Simulation, Logiciel libre]
post_kind: article
---

La frontière d’IPC Toolkit est simple : la bibliothèque fournit les routines de contact, tandis que la simulation appelante gère le temps et la résolution. **[English version]({{< ref "/posts/ipc-toolkit-contact-library/index.md" >}})**.

<!--more-->

Le toolkit contient des fonctions barrière et leurs dérivées, une raideur barrière adaptative, la détection continue de collisions en phases large et étroite, les dérivées de distance pour arêtes et triangles, des potentiels de barrière et des potentiels de friction dissipative lisse ou retardée.

Cette liste précise aussi la limite : IPC Toolkit n’est pas un moteur physique complet et ne fournit ni boucle de simulation ni solveur. Le projet amont cite PolyFEM et Rigid IPC comme implémentations complètes qui l’utilisent.

Ma [note de projet]({{< ref "/projects/notes/ipc-toolkit/index.fr.md" >}}) garde la présentation du dépôt avec la documentation des autres projets. Le [README amont](https://github.com/ipc-sim/ipc-toolkit) et le [fork contributeur](https://github.com/antoinebou12/ipc-toolkit) restent les références pour la compilation et les changements actuels.
