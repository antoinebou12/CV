---
title: "PolyFEMBlenderPlugin : des simulations PolyFEM depuis une scène Blender"
date: 2026-11-05T12:00:00-05:00
description: "Extension Blender 4.2 qui exporte maillages et réglages physiques en JSON PolyFEM, lance PolyFEM avec Docker et réimporte les résultats."
translationKey: repository-note-polyfemblenderplugin
repository_note: "PolyFEMBlenderPlugin"
---

# PolyFEMBlenderPlugin

<div class="repo-status-row"><span class="repo-badge kind">Extension Blender</span><span class="repo-badge docker">Docker</span></div>

<div class="repo-tech-badges"><span class="tag tool">Python</span><span class="tag tool">Blender 4.2</span><span class="tag tool">PolyFEM</span><span class="tag tool">TetWild</span><span class="tag tool">meshio</span><span class="tag tool">GitHub Actions</span></div>

PolyFEMBlenderPlugin est une extension Blender expérimentale qui transforme les objets sélectionnés, leurs matériaux et les réglages de contact en configuration JSON [PolyFEM](https://polyfem.github.io/), puis lance la simulation par éléments finis sans quitter Blender. Elle a été écrite pour les travaux de simulation du laboratoire de l’ÉTS et est publiée sous [ETSim](https://github.com/ETSim), pour qui prépare ses scènes dans Blender et les résout avec PolyFEM.

## Aperçu {#overview}

`polyfem/__init__.py` enregistre un panneau, les groupes de propriétés et les opérateurs. À l’enregistrement, il installe aussi `meshio` avec pip dans le dossier de modules utilisateur de Blender.

- `polyfem/panels/polyfem_json.py` dessine le panneau **PolyFEM** dans l’onglet Physics de l’éditeur Properties : mode d’exécution (Docker ou exécutable) pour PolyFEM et TetWild, objets sélectionnés avec leur matériau et leur format d’export, puis sections repliables pour l’export, le contact, le temps, l’espace, les conditions aux limites, les matériaux, le solveur et les sorties.
- `polyfem/operators/create_polyfem_json.py` exporte chaque maillage (STL, OBJ, ou MSH avec TetWild) et écrit le JSON PolyFEM avec les blocs `geometry`, `materials`, `contact`, `time`, `boundary_conditions`, `solver` et `output`.
- `polyfem/operators/run_polyfem.py` lance PolyFEM dans un fil d’arrière-plan, soit `docker run antoinebou12/polyfem --json /data/<fichier>` avec le dossier du projet monté sur `/data`, soit un exécutable local. Son opérateur **Render Animation** lit les résultats `step_*.vtu`, ajoute le déplacement `solution`, convertit chaque pas en OBJ avec meshio et anime la visibilité de chaque maillage importé.
- `polyfem/properties/polyfem.py` regroupe les réglages, dont des matériaux prédéfinis (acier, cuivre, aluminium, etc.), les intégrateurs (Euler implicite, Euler explicite, Newmark implicite) et les solveurs linéaires Eigen.

## Démarrage {#installation}

Le README installe l’extension à partir d’un zip du dossier `polyfem/` : **Edit > Preferences > Add-ons > Install**, puis activer **PolyFem**. `blender_manifest.toml` exige Blender 4.2 ou plus récent. Le mode d’exécution par défaut passe par Docker :

```bash
docker pull yixinhu/tetwild:latest
docker pull antoinebou12/polyfem:latest
```

Le workflow de CI construit le paquet avec la commande de Blender :

```bash
blender --command extension build --source-dir polyfem --output-dir docs
blender --command extension server-generate --repo-dir=docs --html
```

## Guide du dépôt {#reader-guide}

- `polyfem/` contient l’extension elle-même (`blender_manifest.toml`, `__init__.py`, `operators/`, `panels/`, `properties/`).
- `polyfem/operators/create_polyfem_json.py` gère l’export des maillages, TetWild, les matériaux, le téléchargement des images Docker et le fichier JSON.
- `polyfem/operators/run_polyfem.py` lance PolyFEM, importe les résultats, ouvre la documentation PolyFEM et vide le cache.
- `polyfem/properties/polyfem.py` définit chaque champ du panneau et les préréglages.
- `.github/workflows/build.yml` construit le zip et un index de dépôt d’extensions (`docs/index.json`), puis déploie `docs/` sur la branche `gh-pages`.
- `docs/` contient les paquets `polyfem-1.0.10.zip` et `polyfem-1.0.11.zip` avec leur index.
- `zip-plugin.py` et `download-wheels.py` sont des scripts d’appoint pour zipper l’extension et télécharger les wheels de meshio, trimesh et tetgen.

## Fonctionnalités {#features}

- Assigner des propriétés élastiques (E, ν, ρ) aux objets à partir de préréglages ou de valeurs saisies.
- Exporter les maillages en STL ou OBJ, ou les tétraédriser en MSH avec TetWild, en Docker ou en exécutable local.
- Régler le contact (`dhat`, coefficient de frottement, `epsv`), l’intégration temporelle, la méthode et le second membre des conditions aux limites, le solveur linéaire et les sorties ParaView.
- Écrire un fichier JSON PolyFEM complet, avec option d’export des objets sélectionnés seulement.
- Lancer PolyFEM par Docker ou par un exécutable local sans bloquer l’interface de Blender.
- Réimporter les pas de temps VTU sous forme de séquence de maillages animée.

## Limites {#limits}

- Le README qualifie l’extension d’expérimentale et signale des plantages avec des géométries complexes ainsi que des cas limites d’export.
- Le panneau est enregistré dans l’onglet Physics de l’éditeur Properties, alors que le README décrit un onglet dans la barre latérale du 3D Viewport.
- FBX et glTF figurent dans le menu d’export, mais l’opérateur les refuse.
- `blender_manifest.toml` ne déclare que la plateforme `windows-x64`, et l’extension a besoin de Docker ou de builds locaux de PolyFEM et TetWild.
- Le README annonce la GPL-3.0, alors que `LICENSE` et le manifeste indiquent MIT.
- Les badges et l’arborescence du README renvoient à un ancien nom de dépôt et à un fichier `panels/poly_fem.py` absent.
- Aucun test : le workflow se contente de construire et de publier le paquet.

## Sources {#sources}

- [Dépôt GitHub](https://github.com/ETSim/PolyFEMBlenderPlugin)
- [README](https://github.com/ETSim/PolyFEMBlenderPlugin/blob/main/README.md)
- [`polyfem/blender_manifest.toml`](https://github.com/ETSim/PolyFEMBlenderPlugin/blob/main/polyfem/blender_manifest.toml)
- [`polyfem/operators/create_polyfem_json.py`](https://github.com/ETSim/PolyFEMBlenderPlugin/blob/main/polyfem/operators/create_polyfem_json.py)
- [`polyfem/operators/run_polyfem.py`](https://github.com/ETSim/PolyFEMBlenderPlugin/blob/main/polyfem/operators/run_polyfem.py)
- [`.github/workflows/build.yml`](https://github.com/ETSim/PolyFEMBlenderPlugin/blob/main/.github/workflows/build.yml)
