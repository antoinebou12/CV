# PolyFEMBlenderPlugin : des simulations PolyFEM depuis une scène Blender

> Extension Blender 4.2 qui exporte maillages et réglages physiques en JSON PolyFEM, lance PolyFEM avec Docker et réimporte les résultats.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/polyfemblenderplugin/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/polyfemblenderplugin/index.md
- Publié: 2026-11-05
- Mis à jour: 2026-11-05
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/ETSim/PolyFEMBlenderPlugin
- Révision inspectée: 70794d3107843eeaa55210ff899d1f86a9ba5cf5


## Cas d’utilisation

Extension Blender qui transforme une scène en configuration JSON PolyFEM et lance la simulation depuis Blender.

- **Assigner un matériau MEF** (Utilisateur Blender): L'opérateur Apply Material enregistre module de Young, coefficient de Poisson et densité sur les objets sélectionnés à partir de préréglages comme Steel ou Aluminum.
- **Créer le JSON PolyFEM** (Utilisateur Blender): Create PolyFEM JSON exporte chaque maillage et écrit géométrie, matériaux, contact, temps, conditions aux limites, solveur et sorties dans un fichier JSON.
- **Tétraédriser avec TetWild** (Utilisateur Blender, Images Docker): Avec le type MSH, l'objet est écrit en STL puis converti en .msh par l'image yixinhu/tetwild ou un exécutable TetWild local.
- **Lancer la simulation** (Utilisateur Blender, Images Docker, Solveur PolyFEM): Run PolyFem Simulation appelle docker run antoinebou12/polyfem --json avec le dossier du projet monté sur /data, ou un exécutable PolyFEM local, dans un fil d'arrière-plan.
- **Importer l'animation** (Utilisateur Blender, Solveur PolyFEM): Render Animation lit les fichiers step_*.vtu, ajoute le déplacement solution, convertit chaque pas en OBJ avec meshio et anime sa visibilité.
- **Télécharger les images** (Utilisateur Blender, Images Docker): Les boutons Pull Docker Image vérifient que Docker est installé et exécutent docker pull pour l'image TetWild ou PolyFEM configurée.

### Scénario : Simuler une scène de contact et la rejouer dans Blender

1. Installer le dossier polyfem zippé par Edit > Preferences > Add-ons et activer PolyFem.
2. Dans Properties > Physics > PolyFEM, choisir l'exécution Docker et télécharger antoinebou12/polyfem et yixinhu/tetwild.
3. Sélectionner les maillages, appliquer un matériau prédéfini et régler contact, pas de temps et temps final.
4. Cliquer sur Create JSON Configuration pour écrire les maillages et le JSON dans le dossier d'export.
5. Cliquer sur Run PolyFem Simulation, puis Render Animation pour importer les résultats step_*.vtu en maillages animés.

## Langages (octets GitHub Linguist)

| Langage | % |
| --- | ---: |
| Python | 100 |


