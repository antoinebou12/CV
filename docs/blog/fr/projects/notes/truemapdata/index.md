# TrueMapData : des cartes de hauteur pour la métrologie et l’infographie

> TrueMapData lit des cartes de hauteur TrueMap et GelSight, les traite et exporte des résultats visuels, surfaciques et orientés maillage.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/truemapdata/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/truemapdata/index.md
- Publié: 2026-10-24
- Mis à jour: 2026-11-06
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/ETSim/TrueMapData
- Révision inspectée: 8e44bd4e57ad46eba45c46c997bd6b51d7622956


## Cas d’utilisation

Bibliothèque Python et CLI tmd-process pour les cartes de hauteur .tmd TrueMap et GelSight : métrologie, usure, 3D.

- **Charger une carte .tmd** (Chercheur tribologie, TrueMap / GelSight): TMD.load("fichier.tmd") dans tmd/core/tmd.py décode les en-têtes v1 ou v2 et renvoie height_map, un tableau float32 (hauteur, largeur), avec un dictionnaire metadata.
- **Exporter des cartes de texture** (Chercheur tribologie): tmd-process maps all|normal|ao|bump|hillshade|displacement écrit des cartes PNG via les générateurs de tmd/image/maps/, et maps batch traite un dossier entier.
- **Exporter un maillage 3D** (Chercheur tribologie): tmd-process mesh generate exporte en STL, OBJ, PLY, glTF ou USD avec une triangulation adaptative ou quadtree ; mesh apply pose les cartes sur un gabarit OBJ/MTL comme tmd/fixtures/templates/plane.
- **Mesurer la rugosité ISO 25178** (Chercheur tribologie, Surfalize (ISO 25178)): tmd-process roughness file <chemin> --quick calcule les paramètres surfaciques via l'extra optionnel truemapdata[roughness], qui installe Surfalize sous GPL-3.0.
- **Suivre l'usure entre scans** (Chercheur tribologie, TrueMap / GelSight): tmd-wear (équivalent de tmd-process wear) calcule courbes de portance, séries de volume d'usure, axe de glissement et évolution des rayures sur des séquences alignées, via tmd/sequence/wear_analysis.py.
- **Tracer surfaces et profils** (Chercheur tribologie): tmd-process visualize basic <fichier> trace cartes de chaleur 2D, surfaces 3D et profils X/Y avec les traceurs matplotlib, plotly, seaborn ou Polyscope (optionnel) ; tribology plot produit un tableau de bord PNG.

### Scénario : Comparer deux captures GelSight d'un échantillon usé

1. Installer le paquet avec pip install truemapdata, ou pip install -e . depuis un clone.
2. Lancer tmd-wear bearing curve examples/gelsight/circle_0mm_100g_heightmap_linear_detrend.tmd --json pour obtenir la courbe d'Abbott de la première capture.
3. Lancer tmd-wear volume-series avec ce fichier et tests/fixtures/gelsight_wear_volume_second_frame.tmd pour mesurer le volume perdu entre les deux images.
4. Exporter les textures avec tmd-process maps all <fichier> -o ./maps_out.
5. Construire un maillage avec tmd-process mesh generate <fichier> --format stl --method adaptive --quality high pour voir la zone usée en 3D.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Jupyter Notebook | 94.36 |
| Python | 5.64 |

## Démarrage (commandes du dépôt, non exécutées ici)

### README.md · Installation

```bash
pip install truemapdata
```

### README.md · Installation

```bash
pip install "truemapdata[mesh,viz,advanced]"
pip install "truemapdata[roughness]"   # Surfalize (GPL-3.0); Python 3.10+ only
```

### README.md · Installation

```bash
pip install -r requirements.txt
pip install -e .
```



