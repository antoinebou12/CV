---
title: "MistubaVideo"
date: 2026-10-24T12:00:00-04:00
description: "MistubaVideo est un dépôt ETSim consacré à un travail vidéo avec Mitsuba."
translationKey: repository-note-mistubavideo
repository_note: "MistubaVideo"
---

# MistubaVideo

MistubaVideo effectue le rendu de sorties de simulation avec Mitsuba 3. La commande par lots traite des séquences OBJ; le module `mitsuba-video` lit les poses et champs de surface enregistrés grâce aux adaptateurs de manifeste et de TextureFriction.

## De la simulation à la vidéo

Le module applique les poses, mélange les apparences des matériaux selon le champ enregistré et produit chaque image. Une carte de chaleur, un panneau d’atlas UV et une courbe de surface couverte permettent d’examiner les changements. FFmpeg assemble la vidéo.

`inspect` vérifie les entrées, `preview` permet de vérifier la caméra et `render` produit la séquence. `encode` peut réassembler les images existantes. Les sorties conservent paramètres et temps de calcul dans `render_config.json`, ainsi que les mesures de surface dans un CSV.

## Stack et tests

Python coordonne Mitsuba 3 et FFmpeg. La documentation du module décrit des tests pytest pour les transformations, le mélange des matériaux, les lecteurs OBJ/MTL et les manifestes. Aucun rapport chiffré de couverture n’est cité ici.

[Sources et utilisation](https://github.com/ETSim/MistubaVideo) · [Module de rendu](https://github.com/ETSim/MistubaVideo/tree/main/packages/mitsuba_video)

[Lire la présentation du projet]({{< ref "/posts/mistubavideo-rendered-video/index.fr.md" >}}).
