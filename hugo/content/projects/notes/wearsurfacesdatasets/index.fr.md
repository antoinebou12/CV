---
title: "WearSurfacesDatasets : des séquences mesurées de surfaces usées"
date: 2026-11-05T12:00:00-05:00
description: "Cartes de surface GelSight de matériaux usés selon le grain, la charge et la distance, en Parquet et WebDataset, avec outils d’alignement et visionneuse WebGPU."
translationKey: repository-note-wearsurfacesdatasets
repository_note: "WearSurfacesDatasets"
---

# WearSurfacesDatasets

<div class="repo-status-row"><span class="repo-badge kind">Jeu de données</span><span class="repo-badge api">API</span></div>

<div class="repo-tech-badges"><span class="tag tool">Python</span><span class="tag tool">Parquet</span><span class="tag tool">WebDataset</span><span class="tag tool">Git LFS</span><span class="tag tool">OpenCV</span><span class="tag tool">FastAPI</span><span class="tag tool">WebGPU</span></div>

WearSurfacesDatasets publie les textures de surface capturées pendant des essais d’usure contrôlés, classées par matériau, grain abrasif, charge et distance de glissement. C’est le jeu de données public de la [recherche de maîtrise à l’ÉTS sur l’usure dans l’espace texture]({{< ref "/posts/thesis-wear-texture-space/index.fr.md" >}}), où il sert à comparer les motifs d’usure simulés à la microgéométrie mesurée. Il est publié sous [ETSim](https://github.com/ETSim) pour les chercheurs en rendu et en tribologie qui ont besoin de vraies progressions d’usure.

## Aperçu {#overview}

Chaque état mesuré correspond à une feuille Parquet :

```text
data/parquet/<matériau>/<forme>/<direction>/S<grain>/<charge>g/<distance>mm/data.parquet
```

Par exemple `data/parquet/Cartboard/Raw/Normal/S60/200g/800mm/data.parquet`. Chaque ligne stocke une carte en octets JPEG dans `image_data`, étiquetée par `map_type` ; `metadata.json` liste les cartes d’occlusion ambiante, de bump, de déplacement, de hauteur, d’ombrage (hillshade) et de normales. Les mêmes enregistrements existent aussi en archives WebDataset, de `data/shards/shard-0000.tar` à `shard-0839.tar`.

`data/parquet/sequences.json` répertorie 20 chronologies d’usure : carton sous cinq charges (10 à 200 g, grain S60), mousse, MDF (trajets en cercle et en ligne), PLA à plusieurs grains en direction linéaire et non linéaire, bois tendre, et des références de papier abrasif non usé de S40 à S240.

Par-dessus les données, le dépôt ajoute trois couches d’outils :

- `generate_datasets.py`, `read_datasets.py` et `generate_metadata.py` (CLI Typer) construisent le Parquet et les shards à partir d’un dossier `wear/` de cartes PNG, les réextraient et écrivent les métadonnées par feuille et l’index.
- `alignment/` recale chaque séquence par une méthode SIFT/ECC en deux passes (`align.py`), recadre la zone valide commune, ajoute des points milieux Catmull-Rom dans le temps (`interpolate.py`) et extrapole les normal maps futures avec un modèle FFT et SLERP (`extrapolate.py`). `bake.py` enchaîne le tout pour une séquence ou pour toutes, et peut réempaqueter les résultats.
- `docs/index.html` est une visionneuse de matériaux WebGPU qui lit le Parquet dans le navigateur avec parquet-wasm. `docs/serve_local.py` est un serveur FastAPI qui sert la visionneuse et les données et expose `/api/datasets`, `/api/sequences` et `/api/align/sequence`.

## Démarrage {#installation}

D’après le README :

```bash
git clone https://github.com/ETSim/WearSurfacesDatasets
cd WearSurfacesDatasets
git lfs pull
pip install -r requirements.txt
python docs/serve_local.py
# ouvrir http://127.0.0.1:8080/docs/index.html
```

Dans la visionneuse, on choisit une séquence, on clique sur **Load sequence**, au besoin sur **Align sequence**, puis on fait défiler la distance ou on lance **Play**. Pour calculer les étapes interpolées et extrapolées :

```bash
python -m alignment.bake --sequence-id cartboard-raw-normal-s60-200g --pack
python -m alignment.bake --all --pack
```

Pour reconstruire le jeu de données à partir des PNG ou extraire les images :

```bash
python generate_datasets.py parquet --input-dir wear --output-dir data/parquet
python generate_datasets.py webdataset --input-dir wear --output-dir data/shards
python read_datasets.py decompress --shards-dir data/shards --output-dir data/images --workers 4
```

## Guide du dépôt {#reader-guide}

- `data/parquet/` : feuilles Parquet, `sequences.json` et `metadata.parquet`.
- `data/shards/` : shards WebDataset `.tar`.
- `metadata.json` : matériaux, grains, charges, distances, montage de capture et types de cartes.
- `alignment/` : recalage, déformation, interpolation, extrapolation, calcul et empaquetage.
- `docs/index.html`, `docs/serve_local.py` et `docs/serve_app.py` : la visionneuse et ses serveurs locaux. `docs/prepare_viewer_parquets.py` reconstruit `sequences.json`.
- `docs/package/` : la version de parquet-wasm embarquée pour la visionneuse.
- `examples/Wear/powerpoint/` : une présentation PowerPoint par série d’essais (carton, mousse, MDF, PLA, papier abrasif, bois tendre).

## Fonctionnalités {#features}

- Séquences d’usure indexées par matériau, forme du trajet, direction, grain, charge et distance de glissement.
- Deux formats de stockage : Parquet imbriqué pour la consultation et shards WebDataset pour la lecture en flux.
- Visionneuse dans le navigateur avec défilement de la distance, lecture et préchargement des étapes voisines.
- Alignement SIFT/ECC côté serveur, avec résultats en cache et téléchargement d’un atlas à plat.
- Interpolation Catmull-Rom et extrapolation FFT et SLERP des normal maps.
- Outils en ligne de commande pour reconstruire, extraire et décrire le jeu de données.

## Limites {#limits}

- Les fichiers Parquet et les shards sont des objets Git LFS : un simple clone ne contient que des pointeurs tant que `git lfs pull` n’a pas été lancé.
- L’arbre PNG source `wear/` utilisé par `generate_datasets.py` n’est pas dans le dépôt, et `data/aligned/` et `data/wear_extrapolated/` sont ignorés par Git.
- Le README et `metadata.json` citent Alu et Resin, mais le `sequences.json` versionné ne contient aucune séquence Alu ni Resin.
- Les images extrapolées sont produites par un modèle, ce ne sont pas des mesures.
- Plusieurs séquences sont courtes (deux étapes pour certaines séries PLA et MDF), et un dossier de mousse s’appelle `4000000mm`.
- `docs/README.md` et `metadata.json` donnent des valeurs de capture différentes (résolution, nombre de DEL, température) ; mieux vaut les lire comme descriptives.
- Sur un hébergement statique, la visionneuse charge toujours les images, mais l’alignement est désactivé parce qu’il exige le serveur Python.
- Aucun test automatisé.

## Sources {#sources}

- [Dépôt GitHub](https://github.com/ETSim/WearSurfacesDatasets)
- [README](https://github.com/ETSim/WearSurfacesDatasets/blob/main/README.md)
- [`data/parquet/sequences.json`](https://github.com/ETSim/WearSurfacesDatasets/blob/main/data/parquet/sequences.json)
- [`alignment/align.py`](https://github.com/ETSim/WearSurfacesDatasets/blob/main/alignment/align.py)
- [`alignment/extrapolate.py`](https://github.com/ETSim/WearSurfacesDatasets/blob/main/alignment/extrapolate.py)
- [`docs/serve_local.py`](https://github.com/ETSim/WearSurfacesDatasets/blob/main/docs/serve_local.py)
