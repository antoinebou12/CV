---
post_kind: article
title: "Dimension — une pile math en Rust autour de mathlib"
date: 2026-04-13T10:00:00-04:00
description: Notes sur le monorepo Dimension et sa crate mathlib — algèbre linéaire, matrices creuses, démos WASM et chemins GPU optionnels.
translationKey: dimension-mathlib-rust
tags:
    - Rust
    - Linear algebra
    - WebAssembly
    - Scientific computing
    - Open source
---

## De quoi il s’agit

[Dimension](https://github.com/antoinebou12/Dimension) est un monorepo avec lequel j’expérimente le code numérique en Rust. La partie qui porte la plupart de l’API publique est **mathlib** : une crate centrée sur l’algèbre linéaire, avec matrices denses et creuses, vecteurs, décompositions classiques (SVD, Cholesky, LU, PCA), solveurs, et beaucoup de briques pour le style « graphiques » (types 3D, quaternions, quaternions duaux, caméras, easing, courbes).

Le dépôt regroupe aussi des crates liées à la simulation et aux outils — cinématique, physique, géométrie, démos de rendu, briques « neurales », et un petit site qui empaquette certaines démos WASM — de sorte que **mathlib** reste le noyau numérique partagé pendant que d’autres dossiers explorent comment ce noyau se comporte dans de vrais programmes.

## Pourquoi Rust ici

Rust permet une seule base de code pour les binaires natifs, les tests et les benchmarks, puis de compiler les mêmes calculs en **WebAssembly** pour une couche de démo interactive. mathlib est organisée par domaine (linéaire, structure, clustering et distances façon ML, graphes et pathfinding, transformations, bruit, etc.), ce qui garde les fonctionnalités repérables quand la crate grossit.

Des chemins optionnels **SIMD** et **WebGPU/wgpu** existent pour les charges plus lourdes ; le document de conception du dépôt précise quand les solveurs itératifs creux (par exemple gradient conjugué sur matrices CRS) valent mieux que de densifier le problème pour une factorisation dense.

## Essayer

Depuis le dépôt, la boucle habituelle :

```bash
cd mathlib && cargo build
cd mathlib && cargo test
```

Référence API publiée : [docs.rs/mathlib](https://docs.rs/mathlib). Pour l’architecture, les tableaux de types et les notes d’usage, le `docs/DOCS.md` du dépôt fait office de carte longue.

## En bref

Dimension est autant un espace de travail pour apprendre et benchmarker qu’une bibliothèque. Si vous vous intéressez au numérique en Rust, aux démos WASM ou aux primitives accélérées GPU, le dépôt [GitHub](https://github.com/antoinebou12/Dimension) est l’endroit à suivre ; les PR et les issues sont les bienvenues.
