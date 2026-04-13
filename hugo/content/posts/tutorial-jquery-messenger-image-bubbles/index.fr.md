---
post_kind: tutorial
title: "Bulles d’images déplaçables et triables (style Messenger)"
date: 2016-01-07T10:00:00-04:00
description: Tuiles circulaires façon Messenger avec jQuery UI — glisser-déposer et listes triables, dans l’esprit des tutoriels jQuery d’environ 2016.
translationKey: tutorial-jquery-messenger-image-bubbles
tags:
    - jQuery
    - jQuery UI
    - CSS
    - Drag and drop
    - Tutorial
    - Frontend
---

### Tutoriel : images déplaçables et triables avec jQuery

#### Introduction
Ce guide utilise **jQuery** et **jQuery UI** pour des avatars « bulles » circulaires que l’on peut faire glisser et réordonner — les mêmes ingrédients que dans les démos à la mode quand les cercles façon Messenger et les listes triables étaient partout (ère ES5 + jQuery, ~2016). Pratique pour du legacy ou pour garder la recette au même endroit.

#### Prérequis
- Bases HTML, CSS et JavaScript
- Bibliothèques jQuery et jQuery UI

#### Structure HTML
Deux listes non ordonnées (`ul`) avec des éléments (`li`) contenant des images.

```html
<div id="draw">
    <ul id="ul1">
        <li class="li1"><img id="Logo" src="your-image-source-1.jpg"></li>
        <li class="li1"><img id="Logo2" src="your-image-source-2.jpg"></li>
    </ul>
    <ul id="ul2">
        <li class="li2"><img id="Logo3" src="your-image-source-3.jpg"></li>
        <li class="li2"><img id="Logo4" src="your-image-source-4.jpg"></li>
    </ul>
</div>
```

#### Style CSS
On retire le style de liste par défaut et on arrondit les images.

```css
ul, li {
  list-style: none;
}

img {
  border-radius: 50%;
  border: 0.5px solid #888;
  width: 60px;
  height: 60px;
  margin: 0px;
}
```

#### Fonction jQuery

Fonction jQuery pour appliquer la forme ronde et rendre les images déplaçables ou par défaut selon l’option.

```javascript
(function($) {
    $.fn.roundShape = function(option) {
        if (option === "default") {
            this.css({
                "border-radius": "50%",
                "border": "0.5px solid #888",
                "width": "60px",
                "height": "60px",
                "margin": "0px"
            });
        };
        if (option === "draggable") {
            this.css({
                "border-radius": "50%",
                "border": "0.5px solid #888",
                "width": "60px",
                "height": "60px",
                "margin": "0px"
            }).draggable({ scroll: true, scrollSensitivity: 100 });
        }
    };
}(jQuery));
```

#### Application

```javascript
$(document).ready(function() {
    $('#ul1').sortable({
        revert: true
    });

    $('#Logo, #Logo2').roundShape("default");
    $('#Logo3, #Logo4').roundShape("draggable");
    $('#draw').draggable({ axis: "x" });

    $("#ul1, .li1, .li2").disableSelection();
});
```

En suivant ces étapes, vous obtenez des images circulaires déplaçables et triables — 100 % jQuery UI, toujours valable là où les bibliothèques sont chargées.
