# WearTrailsExperiments : des traces d’usure pilotées par le contact, dans le navigateur

> Expériences three.js et Ammo.js qui transforment contact, traction et glissement de corps rigides en cartes d’usure, de distance glissée et de flux.

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/weartrailsexperiments/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/weartrailsexperiments/index.md
- Publié: 2026-11-05
- Mis à jour: 2026-11-05
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Dépôt: https://github.com/ETSim/WearTrailsExperiments


## Cas d’utilisation

Expériences web qui transforment le contact et le glissement de corps rigides en cartes d'usure et de flux sur une texture de sol.

- **Faire glisser un corps** (Chercheur en rendu, Navigateur (WebGL), CDN three.js/Ammo.js): docs/index.html charge three.js 0.158 et Ammo.js depuis un CDN, puis main-clean-complete.js lâche un cube, une sphère, un palet, un cône, un cube mou ou un GLB sur un plan avec vitesse, force et frottement réglés.
- **Comparer les boîtes de contact** (Chercheur en rendu, Navigateur (WebGL)): docs/js/bounding-box/ ajuste la zone de contact par AABB, OBB par ACP, OMBB par calipers tournants, KDOP-8 ou une méthode hybride.
- **Examiner les vues de contact** (Chercheur en rendu, Navigateur (WebGL)): Huit vignettes montrent les vues du dessus, du dessous et d'intersection, la vitesse tangentielle, la traction instantanée, la distance de glissement cumulée et l'usure locale.
- **Accumuler l'usure au sol** (Chercheur en rendu, Navigateur (WebGL)): FlowAccumulationManager ajoute K x traction x vitesse dans des tampons du sol et conserve la direction de glissement, encodée en HSVA ou RGBA.
- **Mélanger des variantes GLB** (Chercheur en rendu, Navigateur (WebGL)): GroundVariantManager charge un sol GLB à variantes de matériaux et utilise l'usure cumulée comme carte de mélange et la direction du flux pour pivoter les textures.
- **Exporter les cartes en PNG** (Chercheur en rendu, Navigateur (WebGL)): Export Wear Map et Save Stamps enregistrent les canevas du sol en PNG par un lien de téléchargement.

### Scénario : Enregistrer la trace d'usure d'un cube qui glisse

1. Servir le dossier docs/ avec python -m http.server 8000 et ouvrir http://localhost:8000.
2. Choisir Cube (subdiv 10), l'algorithme OBB (PCA-based) et une valeur de frottement, puis cliquer sur Start.
3. Utiliser Pause, Step Frame et Apply Angular Impulse pour suivre la zone de contact dans les vignettes.
4. Basculer l'encodage d'usure entre HSVA (Direction + Wear) et RGBA pour lire direction et quantité.
5. Cliquer sur Export Wear Map pour enregistrer en PNG la carte cumulée du sol.


