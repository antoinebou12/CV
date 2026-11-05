# MistubaVideo

> MistubaVideo est un dépôt ETSim consacré à un travail vidéo avec Mitsuba.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/mistubavideo/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/mistubavideo/index.md
- Publié: 2026-10-24
- Mis à jour: 2026-10-24
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/ETSim/MistubaVideo


## Cas d’utilisation

Outils Mitsuba 3 d'ETSim qui rendent par lancer de rayons des suites OBJ et des enregistrements d'usure en images, MP4 et GIF.

- **Rendre une suite d'OBJ** (Chercheur (simulation), Mitsuba 3 et FFmpeg): python main.py multi --folder exports --regex "\d+\.obj" crée une scène XML par OBJ trouvé, la rend sur CPU ou CUDA avec le spp et la résolution voulus, puis encode MP4 et GIF avec FFmpeg.
- **Rendre plusieurs vues** (Chercheur (simulation)): --view front --view top ou --all-views rend chaque image depuis les caméras avant, arrière, gauche, droite, dessus, dessous ou perspective de src/mitsuba/camera.py, avec le nom de la vue dans le fichier.
- **Débruiter et extraire les AOV** (Chercheur (simulation), Mitsuba 3 et FFmpeg): python main.py denoise <chemin> applique le débruiteur OptiX de src/mitsuba/denoising.py aux images rendues, et python main.py aov <fichier.exr> extrait les couches AOV d'un EXR dans des fichiers séparés.
- **Produire une vidéo de champ** (Chercheur (simulation), Mitsuba 3 et FFmpeg): mitsuba-video render <manifest.json> -q paper rend les corps rigides à leurs poses enregistrées avec un mélange de matériaux piloté par le champ et une carte de chaleur, ajoute l'atlas UV et un graphique d'aire couverte, puis encode un MP4.
- **Rendre un essai d'usure** (Chercheur (simulation), Essais TextureFriction): python main.py wear render simulation_<ts> ou tf-render lit un dossier --record ou un fichier .h5 de TextureFriction via la source texturefriction.
- **Écrire et valider un manifeste** (Chercheur (simulation)): Tout projet peut produire un manifest.json versionné avec ManifestWriter ; mitsuba-video validate le vérifie avec manifest-v1.schema.json, et mitsuba-video fixture crée un petit exemple synthétique.

### Scénario : Rendre la vidéo de champ de démonstration

1. Installer FFmpeg et Mitsuba 3, puis lancer pip install -e "packages/mitsuba_video[texturefriction]" pour obtenir mitsuba-video et tf-render.
2. Créer une entrée synthétique avec mitsuba-video fixture demo.
3. Vérifier rapidement le cadrage avec mitsuba-video preview demo.
4. Lancer mitsuba-video render demo -q preview pour rendre les images et encoder le MP4.
5. Pour des données réelles, lancer python main.py wear render sur un dossier simulation_<ts> de TextureFriction avec -q paper.


