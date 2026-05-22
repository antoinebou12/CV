---
post_kind: article
title: "Kinectron + p5.js — contrôle du sketch et export GIF"
date: 2024-03-15T10:00:00-04:00
lastmod: 2026-05-23T00:30:00-04:00
description: Brancher Kinectron sur p5.js, arrêter / relancer le sketch et enregistrer la sortie en GIF (Kinect v2 ou Azure Kinect DK).
translationKey: kinectron-p5-sketch-gif
tags:
    - Kinect
    - Kinectron
    - p5.js
    - JavaScript
    - Creative Coding
    - Tutorial
images:
    - mySketch.gif
---

Pour un cours de creative coding, j’avais besoin des données squelette **Kinectron** dans **p5.js**, avec **lecture / pause** et un export **GIF** court pour les démos. Ci-dessous le squelette utilisé (Kinect v2 ou Azure Kinect DK, serveur Kinectron actif). **[English version]({{< ref "/posts/kinectron-p5-sketch-gif/index.md" >}})**.

<!--more-->

### Prérequis
- Bases JavaScript et p5.js.
- Bibliothèque Kinectron installée.
- Bibliothèque p5.js installée.
- **Kinect v2** ou **Azure Kinect DK**.
- Serveur **Kinectron** en marche.
- Environnement local ou en ligne compatible JavaScript et p5.js.

### Étape 1 : environnement
Inclure p5.js et Kinectron dans le HTML.

```html
<html>
  <head>
    <script
      src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"
      type="text/javascript"
    ></script>
    <script
      type="text/javascript"
    ></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/addons/p5.sound.min.js"></script>
    <script
      src="./client/dist/kinectron-client.js"
      type="text/javascript"
    ></script>
    <script src="sketch.js" type="text/javascript"></script>
  </head>
  <body></body>
</html>
```

### Étape 2 : variables
Dans `sketch.js`, définir les variables nécessaires.

```javascript
// Kinectron setup function
function Kinectron() {
  // Types d’articulations Kinectron
}

let kinectron = new Kinectron();

const liveData = false;
let stopButton, playButton, saveGifButton;
let recorded_skeleton;

function preload() {
  // Charger les données enregistrées si liveData est false
}
```

### Étape 3 : canvas et boutons
```javascript
function setup() {
  createCanvas(640, 480);
  background(0);

  if (liveData) {
    // Kinectron en direct
  } else {
    // Données préenregistrées et boutons
  }
}
```

### Étape 4 : draw
```javascript
function draw() {
  // Données live ou enregistrées
}
```

### Étape 5 : gestes
```javascript
function checkForGestures(body) {
  // Détecter et afficher les gestes
}

function isClapping(body) { /* ... */ }
function isOKSign(body) { /* ... */ }
// Autres fonctions de gestes
```

### Étape 6 : boutons
```javascript
function stopSketch() {
  noLoop();
  console.log("Sketch stopped.");
}

function playSketch() {
  loop();
  console.log("Sketch playing.");
}

function startCreatingGif() {
  saveGif('mySketch', 5);
  // Téléchargement du GIF, etc.
}
```

### Étape 7 : lancer le sketch
Exécuter dans un environnement compatible p5.js.

---

Ensuite, remplacez les gestes ou basculez `liveData` vers des enregistrements — les boutons et le hook `saveGif` sont ce que je réutilisais d’un devoir à l’autre.
