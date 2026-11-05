---
title: "WearTrailsExperiments : des traces d’usure pilotées par le contact, dans le navigateur"
date: 2026-11-05T12:00:00-05:00
description: "Expériences three.js et Ammo.js qui transforment contact, traction et glissement de corps rigides en cartes d’usure, de distance glissée et de flux."
translationKey: repository-note-weartrailsexperiments
repository_note: "WearTrailsExperiments"
---

# WearTrailsExperiments

<div class="repo-status-row"><span class="repo-badge kind">Expériences web</span></div>

<div class="repo-tech-badges"><span class="tag tool">JavaScript</span><span class="tag tool">three.js</span><span class="tag tool">Ammo.js</span><span class="tag tool">WebGL</span><span class="tag tool">glTF / GLB</span></div>

WearTrailsExperiments regroupe des prototypes web qui transforment le contact entre un corps qui glisse et le sol en cartes persistantes d’usure et de flux. Ils explorent en JavaScript l’idée de la [recherche de maîtrise à l’ÉTS sur l’usure dans l’espace texture]({{< ref "/posts/thesis-wear-texture-space/index.fr.md" >}}) : zones de contact, vitesse tangentielle et traction écrites dans une texture, là où le contact a réellement eu lieu. Le dépôt est publié sous [ETSim](https://github.com/ETSim) pour les chercheurs en rendu qui veulent essayer ces idées sans construire de simulateur natif.

## Aperçu {#overview}

Le dépôt a deux parties.

**`docs/`, l’application modulaire.** `docs/index.html` charge three.js 0.158 et Ammo.js depuis un CDN et lance `js/main-clean-complete.js`. Un corps (cube, cube mou volumique, sphère, palet torique, palet cylindrique, cône ou GLB personnalisé) tombe sur un plan avec gravité, frottement, restitution, vitesse et force réglables. À chaque image :

- `js/contacts.js` échantillonne les points de contact et leur centre ;
- `js/bounding-box/` ajuste la zone de contact par AABB, OBB par ACP, OMBB par calipers tournants, KDOP-8 ou une méthode hybride ;
- `js/pip/` affiche huit vignettes : masques du dessus, du dessous et d’intersection, vitesse tangentielle, traction instantanée (τ = μ σ<sub>n</sub>), distance de glissement cumulée, distance de glissement locale avec vecteurs de direction, et usure locale ;
- `js/managers/flow-accumulation-manager.js` cumule l’usure au sol sous la forme K × traction × vitesse, garde une direction de glissement lissée dans le temps et encode le tout en HSVA ou RGBA ;
- `js/managers/ground-variant-manager.js` charge un sol GLB à variantes de matériaux et les mélange selon la carte d’usure, en faisant pivoter les textures dans le sens du flux ;
- `js/shaders/wear-map-shader.js` colore la carte de distance glissée, avec une échelle logarithmique en option.

**`experiments/`, des prototypes en un seul fichier.** Neuf pages HTML autonomes, nommées d’après leur contenu : masques de contact, dynamic paint avec traces UV et enveloppes OBB, champs vectoriels de glissement, peinture multicouche avec prise en charge des GLB, simulations d’usure directionnelle et selon la dureté, et mélange GLB/champ de flux. `docs/glb_khr_variants_blend.html` est un test plus court de mélange de variantes de matériaux glTF avec une carte en niveaux de gris.

## Démarrage {#installation}

Les pages utilisent des modules ES et ont donc besoin d’un serveur web local. D’après le README de `docs/` :

```bash
cd docs
python -m http.server 8000
# ouvrir http://localhost:8000
```

Cliquer sur **Start**, régler les contrôles du panneau de gauche et observer les vignettes. **Pause**, **Step Frame** et **Apply Angular Impulse** aident à suivre un contact, et **Export Wear Map** ou **Save Stamps** enregistrent les cartes du sol en PNG. Les pages de `experiments/` s’ouvrent de la même façon. Une connexion Internet est nécessaire pour les bibliothèques chargées par CDN.

## Guide du dépôt {#reader-guide}

- `docs/index.html` : page principale avec son panneau de contrôle.
- `docs/js/main-clean-complete.js` : module d’entrée. `docs/js/main.js` est un autre module d’entrée que `index.html` ne charge pas.
- `docs/js/bodies/` crée les corps physiques, `docs/js/body-manager.js` gère leur cycle de vie.
- `docs/js/bounding-box/` : algorithmes d’ajustement de la zone de contact.
- `docs/js/pip/` : les huit rendus en vignette.
- `docs/js/managers/` : gestionnaires de scène, de physique, de sol, de tamponnage, de champ et flux, d’accumulation d’usure et de variantes GLB.
- `docs/js/shaders/wear-map-shader.js` : shader GLSL de la carte d’usure.
- `experiments/` : les prototypes HTML autonomes.

## Fonctionnalités {#features}

- Corps rigides et mous sur la physique Ammo.js, y compris des modèles GLB personnalisés.
- Cinq méthodes d’ajustement de la zone de contact, avec alignement de l’OBB sur la vitesse.
- Vues en direct des masques de contact, de la vitesse tangentielle, de la traction, de la distance glissée et de l’usure.
- Usure cumulée au sol de façon persistante, effacée seulement sur demande, avec une direction de glissement lissée dans le temps.
- Mélange de variantes de matériaux GLB piloté par l’usure cumulée.
- Export PNG des tampons et des cartes d’usure et de flux.

## Limites {#limits}

- Ce sont des prototypes de recherche : le modèle d’usure est une heuristique visuelle dans des tampons de canevas, pas un modèle tribologique calibré.
- `docs/README.md` décrit une ancienne organisation (`stamp/`, `field-flow/`, six vignettes) qui ne correspond plus aux fichiers, et le README principal tient en une phrase.
- Les bibliothèques viennent de CDN, dont Ammo.js tiré d’une branche mouvante (`@HEAD` ou `@main`) dans plusieurs pages ; le comportement peut donc changer sans modification du code.
- La plupart des expériences utilisent three.js 0.160, l’application la version 0.158.
- Le README signale que l’angle de l’OBB peut trembler à basse vitesse et que les GLB personnalisés devraient être convexes.
- Ni tests ni étape de build.

## Sources {#sources}

- [Dépôt GitHub](https://github.com/ETSim/WearTrailsExperiments)
- [README](https://github.com/ETSim/WearTrailsExperiments/blob/main/README.md)
- [`docs/README.md`](https://github.com/ETSim/WearTrailsExperiments/blob/main/docs/README.md)
- [`docs/js/main-clean-complete.js`](https://github.com/ETSim/WearTrailsExperiments/blob/main/docs/js/main-clean-complete.js)
- [`docs/js/managers/flow-accumulation-manager.js`](https://github.com/ETSim/WearTrailsExperiments/blob/main/docs/js/managers/flow-accumulation-manager.js)
- [`docs/js/managers/ground-variant-manager.js`](https://github.com/ETSim/WearTrailsExperiments/blob/main/docs/js/managers/ground-variant-manager.js)
