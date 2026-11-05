# Dimension : Du stockage matriciel à la scène affichée

> Dimension est mon espace de travail Rust pour les mathématiques et l’infographie. mathlib fournit les outils numériques; render les utilise pour les…

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/dimension/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/dimension/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-10-23
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/antoinebou12/Dimension
- Licence: MIT
- Révision inspectée: 5281d0932aa99ea0d2c43e64c388b9256c75b126

## Résumé

Dimension est mon espace de travail Rust pour les mathématiques et l’infographie. mathlib fournit les outils numériques; render les utilise pour les transformations et les caméras côté CPU avant de soumettre le travail graphique à wgpu.

**Pourquoi il existe:** Pipeline graphique wgpu haute performance et moteur d'algèbre linéaire implémentés en Rust à partir des fondamentaux.

**Cas d’usage:** Rendu 3D de cartes de relief accéléré matériellement, transformations spatiales et apprentissage de l'infographie.

## Cas d’utilisation

Un espace de travail Rust autour de mathlib : algèbre linéaire, rendu wgpu, analyseurs, physique et géométrie, avec démos WASM.

- **Calculer en dense et creux** (Développeur Rust): Le crate mathlib fournit matrices denses et creuses, vecteurs, SVD et outils 3D ; cd mathlib && cargo test et cargo bench les mettent à l’épreuve.
- **Rendre une scène 3D avec wgpu** (Développeur Rust, GPU via wgpu): Le crate render dessine une scène mathlib Tree avec wgpu ; cargo run -p render-demo --example render_native ouvre une fenêtre avec un cube, un manipulateur et la sélection.
- **Charger maillages et fichiers** (Développeur Rust): Le crate parse lit JSON, XML, OBJ, MTL, BVH, glTF, PLY, PNG, JPEG, ZIP et TAR, chacun derrière une fonctionnalité Cargo comme json ou obj.
- **Simuler physique et collisions** (Développeur Rust): physics implémente PBD/XPBD avec les exemples particles_2d, rigid_bodies_3d et softbody_3d ; collision ajoute les requêtes AABB, OBB, BVH, BSP, rayon et frustum.
- **Publier le site de démos WASM** (Développeur Rust, Navigateur WASM/WebGPU): just website-build compile en WASM les démos mathlib, render, kinematics, physics, geometry et neural dans website/ ; pages.yml les déploie sur GitHub Pages.

### Scénario : Essayer les démos en local avant de pousser

1. Lancer cd mathlib && cargo test pour vérifier la bibliothèque de base.
2. Lancer just run-render pour ouvrir la scène wgpu native et déplacer le manipulateur.
3. Lancer just website-build pour compiler chaque démo en WASM dans website/.
4. Lancer just website-serve et ouvrir http://localhost:3000/ pour parcourir /mathlib/, /render/ et /physics/.
5. Pousser sur main ; le flux Pages reconstruit website/ et le publie.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Rust | 63.95 |
| JavaScript | 31.84 |
| HTML | 2.57 |
| Just | 0.52 |
| CSS | 0.51 |
| WGSL | 0.4 |
| TypeScript | 0.13 |
| Python | 0.04 |
| Shell | 0.02 |
| Dockerfile | 0.01 |

## Démarrage (commandes du dépôt, non exécutées ici)

### kinematics/README.md · Build, test, bench

```bash
cd kinematics
cargo build
cargo test
cargo bench
cargo run --example forward_kinematics
cargo run --example jacobian_ik
```

### mathlib/demo/README.md · Build and serve

```bash
just wasm-build      # or just wasm-build-gpu for GPU support
just wasm-serve
```

### mathlib/demo/wasm-demo/README.md · Build

```bash
wasm-pack build --target web --features wasm
```

### neural/README.md · Downloading ONNX models

```bash
cargo run -p neural --bin download_models -- --all
```

### neural/README.md · Precomputing embeddings for the WASM recommendation demo

```bash
cargo run -p neural --example precompute_demo_embeddings --features precompute -- mathlib/demo/wasm-demo/recommendation/data.json
```

### render/README.md · Build and run

```bash
cargo run -p render-demo --example render_native
```

### render/README.md · Build and run

```bash
just render-wasm         # build + serve; open http://localhost:3000/wasm-demo/
```

### website/README.md · Build and serve (local)

```bash
just website-build        # Build all WASM demos and populate website/
just website-build-gpu    # Same, but with GPU-enabled mathlib (WebGPU init, async matmul, etc.)
just website-build-simd   # Same as website-build, but render demo built with SIMD (can improve frame rate)
just website-serve        # Serve website/ (e.g. http://localhost:3000)
```


## Fonctions et composants

- **Données et opérations numériques** — mathlib expose du stockage dense et creux, des vues matricielles, des vecteurs et des méthodes numériques. L’appelant choisit la représentation adaptée au problème. Les fonctions d’exécution optionnelles sont distinctes de l’API de stockage de base.
- **Scène et frontière de plateforme** — render expose World, EntityId et Transform ainsi que des relations parent-enfant dans la scène. Les fenêtres natives et le canevas WebAssembly entourent le moteur de rendu. L’espace de travail contient aussi des crates de géométrie, collision, cinématique et physique.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- Application ou démo → Données et transformations mathlib
- Données et transformations mathlib → Hiérarchie de scène et caméra
- Hiérarchie de scène et caméra → Ressources et passes wgpu
- Ressources et passes wgpu → Fenêtre native ou canevas web

```mermaid
flowchart LR
  n0["Application ou démo"]
  n1["Données et transformations mathlib"]
  n2["Hiérarchie de scène et caméra"]
  n3["Ressources et passes wgpu"]
  n4["Fenêtre native ou canevas web"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
```

**Un parcours dans le code:** Pour une mise à jour de scène, partez du Transform local et de son parent. Suivez la scène vers le moteur sans supposer qu’un calcul matriciel s’exécute sur le GPU. wgpu est le moteur graphique; l’exécution GPU optionnelle de mathlib est une fonction différente.

## Limites et points à vérifier

La présence des modules ne prouve ni un moteur physique terminé ni des performances mesurées. Un benchmark doit préciser sa charge, ses options et le matériel.

## Fichiers à lire

- [Cargo.toml](https://github.com/antoinebou12/Dimension/blob/main/Cargo.toml)
- [mathlib/src/lib.rs](https://github.com/antoinebou12/Dimension/blob/main/mathlib/src/lib.rs)
- [render/src/lib.rs](https://github.com/antoinebou12/Dimension/blob/main/render/src/lib.rs)


