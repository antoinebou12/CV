---
title: "WearBlender : des scènes Blender pour les effets d’usure"
date: 2026-11-05T12:00:00-05:00
description: "Fichiers Blender d’exemple pour l’usure des arêtes, les rayures, les normal maps pivotées, les flowmaps et l’usure peinte, en shaders et geometry nodes."
translationKey: repository-note-wearblender
repository_note: "WearBlender"
---

# WearBlender

<div class="repo-status-row"><span class="repo-badge kind">Scènes Blender</span></div>

<div class="repo-tech-badges"><span class="tag tool">Blender</span><span class="tag tool">Nœuds de shader</span><span class="tag tool">Geometry nodes</span></div>

WearBlender est un ensemble de scènes Blender, publié sous [ETSim](https://github.com/ETSim), pour apprendre et enseigner les façons habituelles de simuler l’usure à la main : arêtes usées, rayures, normal maps pivotées, marques peintes et effets de proximité. Il accompagne la [recherche de maîtrise à l’ÉTS sur l’usure dans l’espace texture]({{< ref "/posts/thesis-wear-texture-space/index.fr.md" >}}), où l’usure découle du contact simulé plutôt que de masques construits à la main.

## Aperçu {#overview}

Le dépôt ne contient que des fichiers `.blend`, un README et une licence MIT. Le README annonce cinq thèmes. Les types de nœuds enregistrés dans chaque fichier montrent comment les scènes les couvrent :

- `Edge wear.blend` : un masque d’arêtes usées construit avec les nœuds **Bevel** et **Geometry**, une rampe de couleur et une texture de rugosité sur un plan.
- `Scratched.blend` : des micro-rayures procédurales sur une Suzanne, à partir de textures **Voronoi** et **Noise**, de rampes de couleur et de nœuds **Bump**.
- `NormalRotation.blend` : une normal map image dont les vecteurs pivotent avec les nœuds **Vector Rotate** et **Vector Math**.
- `WeightPainting.blend` : des arbres de geometry nodes qui lisent un attribut peint avec **Named Attribute**, et un matériau qui mélange des shaders par un nœud **Attribute**.
- `flowmap.blend` : des nœuds vectoriels qui séparent puis recombinent les coordonnées pour faire glisser une texture selon une image de flux.
- `SurfaceCameraProjection.blend` : une seconde caméra, un `CameraProjectionMaterial` avec shader d’émission et un monde de corps rigides.

Trois autres scènes plus lourdes, `Sliding_cube.blend`, `Wrapping project.blend` et `flowmap_vector field.blend`, évoquent par leur nom un cube qui glisse, un essai d’enveloppement et une variante de flowmap en champ vectoriel. Le README ne les décrit pas séparément.

## Démarrage {#installation}

Rien à compiler. Il suffit de cloner le dépôt et d’ouvrir un fichier dans Blender ; selon le README, les scènes ont été testées dans Blender 4.5 LTS.

```bash
git clone https://github.com/ETSim/WearBlender
blender "WearBlender/Edge wear.blend"
```

Ensuite, comme le propose le README, on explore le Shader Editor ou l’éditeur de Geometry Nodes, on bascule la visibilité ou on lance l’animation, puis on réutilise les montages de nœuds dans ses propres matériaux.

## Guide du dépôt {#reader-guide}

- `Edge wear.blend` : usure des arêtes par courbure et biseau.
- `Scratched.blend` : rayures procédurales avec relief.
- `NormalRotation.blend` : rotation d’une normal map dans un shader.
- `WeightPainting.blend` : usure pilotée par attributs peints et geometry nodes.
- `flowmap.blend` et `flowmap_vector field.blend` : flowmaps de texture.
- `SurfaceCameraProjection.blend` : projection d’une texture caméra sur une surface.
- `Sliding_cube.blend` et `Wrapping project.blend` : scènes supplémentaires, nommées d’après un cube glissant et un projet d’enveloppement.
- `README.md` : liste des thèmes et mode d’emploi.

## Fonctionnalités {#features}

- Usure des arêtes par courbure, biseau et rampes de couleur.
- Rayures procédurales à partir de textures Voronoi et de bruit.
- Normal maps pivotées pour des détails de surface dynamiques.
- Usure pilotée par attributs peints et geometry nodes.
- Décalage de texture par flowmap.
- Projection d’une texture caméra sur une surface.

## Limites {#limits}

- Le dépôt ne contient que des scènes : ni script, ni extension, ni rendu d’aperçu.
- Le README décrit cinq thèmes sans les associer aux fichiers, et mentionne une scène de dynamic paint sans nommer le fichier.
- Les scènes reproduisent des looks d’usure créés par l’artiste, pas un modèle physique d’usure.
- Les fichiers ont été enregistrés avec Blender 4.4 et 4.5 ; des versions plus anciennes risquent de ne pas les ouvrir.

## Sources {#sources}

- [Dépôt GitHub](https://github.com/ETSim/WearBlender)
- [README](https://github.com/ETSim/WearBlender/blob/main/README.md)
- [`Edge wear.blend`](https://github.com/ETSim/WearBlender/blob/main/Edge%20wear.blend)
- [`Scratched.blend`](https://github.com/ETSim/WearBlender/blob/main/Scratched.blend)
- [`WeightPainting.blend`](https://github.com/ETSim/WearBlender/blob/main/WeightPainting.blend)
