# Dimension (mathlib)

> Monorepo Rust centré sur mathlib — algèbre linéaire, matrices creuses, WASM, GPU optionnel.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/dimension/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/dimension/index.md
- Publié: 2026-04-13
- Mis à jour: 2026-04-13
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)# Dimension

[![GitHub last commit](https://img.shields.io/github/last-commit/antoinebou12/Dimension)](https://github.com/antoinebou12/Dimension)

[Dépôt](https://github.com/antoinebou12/Dimension) · [mathlib sur docs.rs](https://docs.rs/mathlib)

**mathlib** est une crate Rust pour l’algèbre linéaire dense et creuse, les décompositions, la mathématique 3D, le clustering, les graphes, les transformations, et plus encore — avec des démos **WebAssembly** et des fonctionnalités **SIMD** / **GPU** optionnelles. Le dépôt Dimension regroupe cette crate avec de la cinématique, de la physique, des expériences de rendu et de la documentation.

## Démos en direct

Rendu | https://antoinebou12.github.io/Dimension/render/ | Un cube, un tétraèdre et un cylindre dessinés par le moteur wgpu, avec un gizmo de transformation et la sélection d’objets.
Géométrie | https://antoinebou12.github.io/Dimension/geometry/ | Démos de maillages de la crate geometry.
Mathlib | https://antoinebou12.github.io/Dimension/mathlib/ | Algèbre linéaire, graphes, optimisation, bruit, transformations et calculs de caméra de mathlib.

Le dépôt publie aussi une [démo de cinématique](https://antoinebou12.github.io/Dimension/kinematics/) (un bras à trois articulations résolu par cinématique inverse) et une [démo de physique](https://antoinebou12.github.io/Dimension/physics/) (corps rigides avec XPBD). Elles demandent un navigateur avec WebGPU et s’ouvrent dans leur propre onglet.

## Démarrage rapide

```bash
cd mathlib && cargo build
cd mathlib && cargo test
```

Voir le [README](https://github.com/antoinebou12/Dimension#readme) à la racine et [docs/DOCS.md](https://github.com/antoinebou12/Dimension/blob/main/docs/DOCS.md) pour l’architecture et des exemples.
