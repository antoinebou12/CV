---
post_kind: tutorial
title: "Barre de progression par étapes responsive (jQuery + CSS)"
date: 2024-02-12T10:00:00-04:00
description: Indicateur multi-étapes avec nœuds numérotés, connecteurs et libellés adaptés à la largeur.
translationKey: tutorial-jquery-step-progress-bar
tags:
    - jQuery
    - CSS
    - UI
    - Progress
    - Tutorial
    - Frontend
---

Ce code crée une barre de progression responsive en quatre étapes. Il utilise **jQuery** pour changer dynamiquement le texte et **CSS** pour le style. Voici le détail du fonctionnement.

### Structure HTML
- La barre est dans un `div` avec la classe `progressbar_container`.
- Une liste non ordonnée `ul` avec la classe `progressbar` représente la barre.
- Chaque étape est un `li` avec la classe `progressbar_node`.
- L’étape courante est mise en avant avec la classe `current_node`.

### Style CSS
- `.progressbar_container` positionne la barre, gère sa taille et la centre.
- Chaque `.progressbar_node` représente une étape.
- Le pseudo-élément `:before` de `.progressbar_node` dessine les pastilles numérotées.
- Le pseudo-élément `:after` trace les traits entre les étapes.
- Les étapes courantes et complétées ont une couleur plus foncée et une bordure pleine.

### Comportement JavaScript
- Au `$(document).ready`, les étapes précédant la courante sont marquées complétées avec `activated_node`.
- Un écouteur `$(window).resize` modifie le texte de la première étape selon la largeur de la fenêtre, en basculant entre « PASSENGER » et « PASSENGER DETAILS ».

### Remarques
- Incluez la bibliothèque **jQuery** pour utiliser cette syntaxe.
- Le redimensionnement aide la responsivité sur différentes largeurs d’écran.

### Utilisation
Incluez le HTML fourni, liez le CSS et chargez jQuery pour que le script fonctionne.

### Améliorations possibles
- Ajuster le nombre d’étapes en modifiant le HTML et éventuellement le CSS.
- Ajouter des attributs **ARIA** pour l’accessibilité et les lecteurs d’écran.
- Remplacer le JS par des **media queries** pour certains changements de texte.

Cette barre convient bien pour représenter visuellement une suite d’étapes (paiement, inscription, etc.).
