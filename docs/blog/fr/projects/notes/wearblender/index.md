# WearBlender : des scènes Blender pour les effets d’usure

> Fichiers Blender d’exemple pour l’usure des arêtes, les rayures, les normal maps pivotées, les flowmaps et l’usure peinte, en shaders et geometry nodes.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/wearblender/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/wearblender/index.md
- Publié: 2026-11-05
- Mis à jour: 2026-11-05
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/ETSim/WearBlender
- Révision inspectée: 422ce0f0c2cf80045564859171ee26773ea4469f


## Cas d’utilisation

Scènes Blender d'exemple pour apprendre à simuler l'usure avec des shaders, des geometry nodes et de la peinture.

- **Étudier l'usure des arêtes** (Apprenant, enseignant, Blender 4.5): Edge wear.blend construit un masque d'arêtes usées dans l'éditeur de shaders avec les nœuds Bevel et Geometry, une rampe de couleur et une texture de rugosité.
- **Étudier des rayures** (Apprenant, enseignant, Blender 4.5): Scratched.blend combine textures Voronoi et Noise, rampes de couleur et nœuds Bump sur une Suzanne pour dessiner des micro-rayures.
- **Faire pivoter une normal map** (Apprenant, enseignant, Blender 4.5): NormalRotation.blend fait pivoter les vecteurs d'une normal map image avec les nœuds Vector Rotate et Vector Math.
- **Piloter l'usure par peinture** (Apprenant, enseignant, Blender 4.5): WeightPainting.blend lit un attribut peint avec des geometry nodes Named Attribute et un nœud Attribute pour mélanger des matériaux.
- **Déformer avec une flowmap** (Apprenant, enseignant, Blender 4.5): flowmap.blend sépare puis recombine des composantes vectorielles pour décaler les coordonnées de texture selon une image de flux.
- **Projeter une texture caméra** (Apprenant, enseignant, Blender 4.5): SurfaceCameraProjection.blend contient une seconde caméra, un CameraProjectionMaterial avec shader d'émission et un monde de corps rigides.

### Scénario : Décortiquer la scène d'usure des arêtes

1. Cloner le dépôt et ouvrir Edge wear.blend dans Blender 4.5 LTS.
2. Sélectionner le plan et ouvrir le Shader Editor pour suivre les nœuds Bevel et Geometry jusqu'à la rampe de couleur.
3. Déplacer les repères de la rampe et voir les arêtes usées grandir ou rétrécir dans la vue.
4. Ouvrir Scratched.blend et comparer comment les textures Voronoi et Noise alimentent le nœud Bump.
5. Copier le montage de nœuds dans son propre matériau comme point de départ.


