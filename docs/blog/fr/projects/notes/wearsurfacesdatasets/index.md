# WearSurfacesDatasets : des séquences mesurées de surfaces usées

> Cartes GelSight de matériaux usés selon le grain, la charge et la distance, en Parquet et WebDataset, avec outils d’alignement et visionneuse WebGPU.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/wearsurfacesdatasets/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/wearsurfacesdatasets/index.md
- Publié: 2026-11-05
- Mis à jour: 2026-11-05
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/ETSim/WearSurfacesDatasets


## Cas d’utilisation

Séquences de cartes de surfaces usées (matériau, grain, charge, distance) avec outils Python et visionneuse WebGPU.

- **Télécharger les séquences** (Chercheur en rendu, Stockage Git LFS): Les feuilles Parquet et les shards WebDataset sont des objets Git LFS : git lfs pull remplace les pointeurs dans data/parquet et data/shards.
- **Parcourir une usure** (Chercheur en rendu, Navigateur WebGPU): docs/serve_local.py sert docs/index.html, qui lit le Parquet avec parquet-wasm et affiche les cartes en WebGPU pendant qu'on fait défiler la distance ou qu'on lance la lecture.
- **Aligner une séquence** (Chercheur en rendu, Navigateur WebGPU): POST /api/align/sequence lance un recalage SIFT/ECC en deux passes des normal maps sur la première image, recadre la zone commune et met les PNG en cache dans data/aligned.
- **Interpoler et extrapoler** (Chercheur en rendu): python -m alignment.bake ajoute des points milieux Catmull-Rom et des normal maps extrapolées par FFT et SLERP après la dernière mesure.
- **Empaqueter Parquet et shards** (Chercheur en rendu): generate_datasets.py parquet et webdataset transforment un arbre wear/ de cartes PNG en feuilles Parquet imbriquées et en fichiers shard-*.tar.
- **Extraire les cartes en PNG** (Chercheur en rendu): read_datasets.py decompress et generate_datasets.py extract réécrivent en fichiers image les octets JPEG stockés par map_type.

### Scénario : Examiner l'usure d'un carton sous 200 g

1. Cloner le dépôt, lancer git lfs pull et pip install -r requirements.txt.
2. Démarrer python docs/serve_local.py et ouvrir http://127.0.0.1:8080/docs/index.html.
3. Choisir Cartboard / Raw / Normal · S60 · 200 g et cliquer sur Load sequence.
4. Cliquer sur Align sequence, puis faire défiler la distance de 0 mm à 2400 mm ou lancer Play.
5. Lancer python -m alignment.bake --sequence-id cartboard-raw-normal-s60-200g --pack pour ajouter les étapes interpolées et extrapolées.


