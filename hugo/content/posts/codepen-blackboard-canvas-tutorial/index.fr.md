---
post_kind: tutorial
title: "Tableau noir HTML5 Canvas (tutoriel CodePen)"
date: 2016-01-07T11:00:00-04:00
description: Tableau interactif sur canvas — dessin, import d’image et effacement ; démo CodePen dans l’esprit des tutoriels Canvas ~2016.
translationKey: codepen-blackboard-canvas-tutorial
tags:
    - Canvas
    - JavaScript
    - CodePen
    - Tutorial
    - Frontend
---

## Démo CodePen

{{< codepen antoinebou13 MLEdxr >}}

## Introduction

Ce tutoriel parcourt un **tableau noir interactif** avec **Canvas HTML5** et JavaScript : dessin, import d’images via l’API File, effacement. C’est le style des pas-à-pas CodePen de 2016. L’intégration ci-dessus montre le résultat.

## Mise en place du canvas

```html
<canvas id="drawingCanvas"></canvas>
```

```css
html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
  margin: 0;
  padding: 0;
  background: hsla(0, 5%, 5%, 1);
}

canvas {
  background: hsla(0, 5%, 5%, 1);
}
```

## Contrôles

```html
<input type="color" id="colorPicker" value="#FFFFFF">
<input type="range" id="penSize" min="1" max="20" value="5">
<button id="saveImage">Save Image</button>
<button id="eraseCanvas">Erase</button>
<input type="file" id="imageLoader" name="imageLoader" accept="image/*">
```

```css

#colorPicker, #penSize, #saveImage, #eraseCanvas, #imageLoader {
  position: absolute;
  top: 10px;
  z-index: 1000;
}

#colorPicker {
  right: 40px;
}

#penSize {
  right: 120px;
}

#eraseCanvas {
  right: 275px;
}

#saveImage {
  right: 350px;
}

#imageLoader {
  right: 400px;
}
```

## Logique de dessin

Voir la [version anglaise]({{< ref "/posts/codepen-blackboard-canvas-tutorial/index.md" >}}) pour le JavaScript complet (`onMouseDown`, `onMouseMove`, `redrawCanvas`, `loadImage`, `saveImage`, `eraseCanvas`).

## Conclusion

Vous disposez d’un tableau fonctionnel sur Canvas. Forkez sur CodePen et étendez — autres pinceaux, annulation, pression : les API sont les mêmes.
