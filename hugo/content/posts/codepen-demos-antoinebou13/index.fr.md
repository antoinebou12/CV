---
post_kind: article
title: "Démos CodePen (collection)"
date: 2017-01-10T10:00:00-04:00
description: Intégrations CodePen et tutoriels front-end regroupés — Canvas, Three.js, jQuery, capture d’écran (getDisplayMedia), minuteur, plage de dates, barre d’étapes, bulles Messenger.
translationKey: codepen-demos-antoinebou13
tags:
  - CodePen
  - Frontend
  - JavaScript
  - CSS
  - Canvas
  - Three.js
  - WebGL
  - jQuery
  - jQuery UI
  - WebRTC
  - HTML
  - Tutorial
  - Progress
  - Timer
  - Date Picker
---

Petites démos **CodePen** (intégrations ci-dessous) et anciens billets regroupés ici : jQuery/CSS, `getDisplayMedia`, et autres notes front-end — un seul favori à garder.

## Petites démos

### BMdzwx

{{< codepen antoinebou13 BMdzwx 420 >}}

[Ouvrir sur CodePen](https://codepen.io/antoinebou13/pen/BMdzwx)

### Vue détails (xMXNyy)

{{< codepen antoinebou13 xMXNyy 420 >}}

[Ouvrir sur CodePen](https://codepen.io/antoinebou13/details/xMXNyy)

### JxrqQx

{{< codepen antoinebou13 JxrqQx 420 >}}

[Ouvrir sur CodePen](https://codepen.io/antoinebou13/pen/JxrqQx)

### byVQKJ

{{< codepen antoinebou13 byVQKJ 420 >}}

[Ouvrir sur CodePen](https://codepen.io/antoinebou13/pen/byVQKJ)

### jjzxER

{{< codepen antoinebou13 jjzxER 420 >}}

[Ouvrir sur CodePen](https://codepen.io/antoinebou13/pen/jjzxER)

### qzQpYg

{{< codepen antoinebou13 qzQpYg 420 >}}

[Ouvrir sur CodePen](https://codepen.io/antoinebou13/pen/qzQpYg)

### ZEENwWB

{{< codepen antoinebou13 ZEENwWB 420 >}}

[Ouvrir sur CodePen](https://codepen.io/antoinebou13/pen/ZEENwWB)

---

## Tableau noir HTML5 Canvas (tutoriel)

{{< codepen antoinebou13 MLEdxr 520 >}}

### Introduction

Ce tutoriel parcourt un **tableau noir interactif** avec **Canvas HTML5** et JavaScript : dessin, import d’images via l’API File, effacement. C’est le style des pas-à-pas CodePen du milieu des années 2010. L’intégration ci-dessus montre le comportement final.

### Mise en place du canvas

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

### Contrôles

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

### Logique de dessin

```javascript
let canvas, ctx;
let isDrawing = false, isDragging = false;
let curColor = '#FFFFFF';
let lineWidth = 5;
let imageObjects = [], drawingObjects = [];
let currentDraggingImg = null;

window.onload = function() {
    canvas = document.getElementById('drawingCanvas');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    ctx = canvas.getContext("2d");
    ctx.lineWidth = lineWidth;

    canvas.addEventListener('mousedown', onMouseDown);
    canvas.addEventListener('mousemove', onMouseMove);
    canvas.addEventListener('mouseup', onMouseUp);

    document.getElementById('colorPicker').addEventListener('input', function(e) {
        curColor = e.target.value;
    });

    document.getElementById('penSize').addEventListener('input', function(e) {
        lineWidth = e.target.value;
    });

    document.getElementById('saveImage').addEventListener('click', saveImage);
    document.getElementById('imageLoader').addEventListener('change', loadImage);
};

function onMouseDown(e) {
    const mouseX = e.pageX - canvas.offsetLeft;
    const mouseY = e.pageY - canvas.offsetTop;
    currentDraggingImg = null;

    imageObjects.forEach(imgObj => {
        if (mouseX >= imgObj.x && mouseX <= imgObj.x + imgObj.width && mouseY >= imgObj.y && mouseY <= imgObj.y + imgObj.height) {
            imgObj.isDragging = true;
            currentDraggingImg = imgObj;
            isDragging = true;
        }
    });

    if (!currentDraggingImg) {
        isDrawing = true;
        const path = { color: curColor, lineWidth: lineWidth, points: [{x: mouseX, y: mouseY}] };
        drawingObjects.push(path);
    }
}

function onMouseMove(e) {
    const mouseX = e.pageX - canvas.offsetLeft;
    const mouseY = e.pageY - canvas.offsetTop;

    if (isDragging && currentDraggingImg) {
        currentDraggingImg.x = mouseX;
        currentDraggingImg.y = mouseY;
        redrawCanvas();
    } else if (isDrawing) {
        const currentPath = drawingObjects[drawingObjects.length - 1];
        currentPath.points.push({x: mouseX, y: mouseY});
        redrawCanvas();
    }
}

function onMouseUp() {
    if (isDragging && currentDraggingImg) {
        currentDraggingImg.isDragging = false;
    }
    isDrawing = isDragging = false;
}
```

Au chargement on dimensionne le canvas, on récupère le contexte 2D et on branche `mousedown` / `mousemove` / `mouseup`. Chaque trait est un objet dans `drawingObjects` ; `redrawCanvas` dessine d’abord les images importées, puis relie les points de chaque chemin.

### Import d’images et effacement

```javascript

function loadImage(e) {
    var reader = new FileReader();
    reader.onload = function(event) {
        var img = new Image();
        img.onload = function() {
            imageObjects.push({
                img: img,
                x: 0,
                y: 0,
                width: img.width,
                height: img.height,
                isDragging: false
            });
            redrawCanvas();
        };
        img.src = event.target.result;
    };
    reader.readAsDataURL(e.target.files[0]);
};

function redrawCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    imageObjects.forEach(imgObj => {
        ctx.drawImage(imgObj.img, imgObj.x, imgObj.y);
    });

    drawingObjects.forEach(path => {
        ctx.beginPath();
        ctx.strokeStyle = path.color;
        ctx.lineWidth = path.lineWidth;
        path.points.forEach((point, index) => {
            if (index === 0) {
                ctx.moveTo(point.x, point.y);
            } else {
                ctx.lineTo(point.x, point.y);
            }
        });
        ctx.stroke();
    });
}

function saveImage() {
    var image = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
    var link = document.createElement('a');
    link.download = 'canvas-drawing.png';
    link.href = image;
    link.click();
}

document.getElementById('eraseCanvas').addEventListener('click', eraseCanvas);

function eraseCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    imageObjects = [];
    drawingObjects = [];
}
```

`FileReader.readAsDataURL` décode le fichier choisi ; au chargement de l’image on pousse un objet déplaçable dans `imageObjects`. `eraseCanvas` vide le canvas et réinitialise les deux tableaux.

### Conclusion

Vous disposez d’un tableau fonctionnel sur Canvas. Forkez sur CodePen et étendez — autres pinceaux, annulation, pression : les API sont les mêmes.

---

## Vague Three.js (tutoriel)

{{< codepen antoinebou13 rNoqVOj 560 >}}

### Introduction

Ce tutoriel construit une **animation de vague 3D** avec **Three.js** : scène, caméra, renderer WebGL, grille de cubes et un mouvement ondulant simple — le genre de démo « regardez, du WebGL dans le navigateur » des articles Three.js + CodePen du milieu des années 2010. Utilisez l’intégration ci-dessus pour modifier en direct.

#### Mise en place de la scène

```js

let cubes = [];
let noiseOffset = 0;
const size = 20;
const step = 2;

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById("container").appendChild(renderer.domElement);

camera.position.z = 50;
camera.position.y = 20;
camera.lookAt(0, 0, 0);

```

#### Cubes avec bruit type Perlin

```js
function noise(x, y, z) {
  return Math.sin(x) * Math.cos(y) * Math.sin(z);
}

for (let x = -size; x <= size; x += step) {
  for (let z = -size; z <= size; z += step) {
    const y = noise(x * 0.1, noiseOffset, z * 0.1) * 10;
    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const cube = new THREE.Mesh(geometry, material);
    cube.position.set(x, y, z);
    scene.add(cube);
    cubes.push(cube);
  }
  noiseOffset += 0.1;
}
```

#### Animation

```js
let waveOffset = 0;
function animate() {
  requestAnimationFrame(animate);
  updateCameraPosition();

  cubes.forEach((cube, i) => {
    cube.position.y =
      noise(cube.position.x * 0.1, waveOffset, cube.position.z * 0.1) * 10;
  });
  waveOffset += 0.01;

  renderer.render(scene, camera);
}
animate();
```

#### Interaction (souris, clavier, manette, molette)

```js
let isDragging = false;
let prevX = 0;
let prevY = 0;

document.addEventListener("mousedown", function (e) {
  isDragging = true;
  prevX = e.clientX;
  prevY = e.clientY;
});

document.addEventListener("mouseup", function () {
  isDragging = false;
});

document.addEventListener("mousemove", function (e) {
  if (isDragging) {
    const dx = e.clientX - prevX;
    const dy = e.clientY - prevY;
    camera.rotation.y += dx * 0.01;
    camera.rotation.x += dy * 0.01;
    prevX = e.clientX;
    prevY = e.clientY;
  }
});

function gamepadControl() {
  const gamepads = navigator.getGamepads();
  if (gamepads[0]) {
    const gp = gamepads[0];
    camera.position.z -= gp.buttons[0].value * 0.1;
    camera.position.z += gp.buttons[1].value * 0.1;
    camera.position.x -= gp.buttons[2].value * 0.1;
    camera.position.x += gp.buttons[3].value * 0.1;
  }
  requestAnimationFrame(gamepadControl);
}
gamepadControl();

let keyStates = {};

document.addEventListener("keydown", function (event) {
  keyStates[event.code] = true;
});

document.addEventListener("keyup", function (event) {
  keyStates[event.code] = false;
});

function updateCameraPosition() {
  if (keyStates["ArrowUp"]) camera.position.z -= 0.1;
  if (keyStates["ArrowDown"]) camera.position.z += 0.1;
  if (keyStates["ArrowLeft"]) camera.position.x -= 0.1;
  if (keyStates["ArrowRight"]) camera.position.x += 0.1;
  if (keyStates["KeyW"]) camera.rotation.x -= 0.01;
  if (keyStates["KeyS"]) camera.rotation.x += 0.01;
  if (keyStates["KeyA"]) camera.rotation.y += 0.01;
  if (keyStates["KeyD"]) camera.rotation.y -= 0.01;
}

document.addEventListener("wheel", function (e) {
  camera.position.z += e.deltaY * 0.01;
});
```

### Conclusion

Vous avez une vague animée de base dans Three.js. Forkez le pen et poussez le mouvement, les matériaux ou la caméra — le pipeline est le même depuis ces tutoriels d’intro WebGL.

---

## Autres tutoriels front-end (hors CodePen)

Anciens articles fusionnés ici : texte et extraits de code uniquement (pas d’iframe CodePen).

### Barre de progression par étapes responsive (jQuery + CSS)

Ce code crée une barre de progression responsive en quatre étapes. Il utilise **jQuery** pour changer dynamiquement le texte et **CSS** pour le style. Voici le détail du fonctionnement.

#### Structure HTML

- La barre est dans un `div` avec la classe `progressbar_container`.
- Une liste non ordonnée `ul` avec la classe `progressbar` représente la barre.
- Chaque étape est un `li` avec la classe `progressbar_node`.
- L’étape courante est mise en avant avec la classe `current_node`.

#### Style CSS

- `.progressbar_container` positionne la barre, gère sa taille et la centre.
- Chaque `.progressbar_node` représente une étape.
- Le pseudo-élément `:before` de `.progressbar_node` dessine les pastilles numérotées.
- Le pseudo-élément `:after` trace les traits entre les étapes.
- Les étapes courantes et complétées ont une couleur plus foncée et une bordure pleine.

#### Comportement JavaScript

- Au `$(document).ready`, les étapes précédant la courante sont marquées complétées avec `activated_node`.
- Un écouteur `$(window).resize` modifie le texte de la première étape selon la largeur de la fenêtre, en basculant entre « PASSENGER » et « PASSENGER DETAILS ».

#### Remarques

- Incluez la bibliothèque **jQuery** pour utiliser cette syntaxe.
- Le redimensionnement aide la responsivité sur différentes largeurs d’écran.

#### Utilisation

Incluez le HTML fourni, liez le CSS et chargez jQuery pour que le script fonctionne.

#### Améliorations possibles

- Ajuster le nombre d’étapes en modifiant le HTML et éventuellement le CSS.
- Ajouter des attributs **ARIA** pour l’accessibilité et les lecteurs d’écran.
- Remplacer le JS par des **media queries** pour certains changements de texte.

Cette barre convient bien pour représenter visuellement une suite d’étapes (paiement, inscription, etc.).

### Capture d’écran dans le navigateur (`getDisplayMedia`)

#### Tutoriel : utilitaire de capture d’écran avec HTML, CSS et JavaScript

##### Introduction

Ce tutoriel montre comment ajouter une capture d’écran dans une appli web : HTML pour la structure, CSS pour le style, JavaScript pour le comportement.

##### Prérequis

- Bases HTML, CSS et JavaScript
- Navigateur récent avec support de `getDisplayMedia`

##### Structure HTML

Boutons pour démarrer / arrêter la capture et zone pour la vidéo.

```html
<p>
  <button id="start">Start Capture</button>
  <button id="stop" class="hidden">Stop Capture</button>
</p>

<div class="wrapper-video"></div>
<br>

<strong class="log-title">Log:</strong>
<br>
<pre id="log"></pre>
```

##### CSS

```css
#video {
  display: table-cell;
  border: 1px solid #999;
  width: 100%;
  max-width: 1080px;
}

.wrapper-video {
  display: table;
  width: 100%;
  max-width: 1082px;
}

.recording-border {
  border: 1px solid red;
}

.error-background-color {
  background-color: red;
}

.error {
  color: red;
}

.warn {
  color: orange;
}

.info {
  color: darkgreen;
}

.hidden {
  display: none;
}

.log-title {
  margin-top: 8px;
}
```

##### JavaScript

```javascript
const $logElem = $("#log");
const $startElem = $("#start");
const $stopElem = $("#stop");

var displayMediaOptions = {
  video: {
    cursor: 'never',
    displaySurface: 'browser'
  },
  audio: false
};

$startElem.on('click', function(evt) {
  startCapture();
});

$stopElem.on('click', function(evt) {
  stopCapture();
});

console.log = msg => $logElem.append(`${msg}<br>`);
console.error = msg => $logElem.append(`<span class="error">${msg}</span><br>`);
console.warn = msg => $logElem.append(`<span class="warn">${msg}</span><br>`);
console.info = msg => $logElem.append(`<span class="info">${msg}</span><br>`);

async function startCapture() {
  $logElem.text('');
  try {
    $('.wrapper-video').addClass("recording-border").append('<video id="video" autoplay></video>');
    $stopElem.removeClass('hidden');
    $startElem.addClass('hidden');
    $('#video').removeClass('error-background-color');
    
    document.getElementById("video").srcObject = await navigator.mediaDevices.getDisplayMedia(displayMediaOptions);
    dumpOptionsInfo();
  } catch(err) {
    $('#video').addClass('error-background-color');
    // Gestion des erreurs
  }
}

function stopCapture(evt) {  
  let tracks = document.getElementById('video').srcObject.getTracks();
  tracks.forEach(track => track.stop());
  document.getElementById("video").srcObject = null;
  
  $stopElem.addClass("hidden");
  $startElem.removeClass("hidden");
  $(".wrapper-video").removeClass("recording-border").text("");
  $logElem.text("");
}

function dumpOptionsInfo() {
  const videoTrack = document.getElementById("video").srcObject.getVideoTracks()[0];
  console.info("Track settings:");
  console.info(JSON.stringify(videoTrack.getSettings(), null, 2));
  console.info("Track constraints:");
  console.info(JSON.stringify(videoTrack.getConstraints(), null, 2));
}
```

##### Gestion d’erreurs

Complétez le bloc `catch` de `startCapture` selon les cas à gérer.

##### Conclusion

Vous pouvez démarrer et arrêter la capture d’écran ; la zone de log affiche les infos de piste et les erreurs. Utile pour tutoriels, présentations ou assistance à distance.

### Minuteur décompte personnalisé (HTML, CSS, JavaScript)

Un décompte classique DOM + `setInterval` : saisie en minutes, tick, démarrage et reset, et un court fichier audio à l’arrivée à zéro — le genre d’exemple qu’on trouvait partout dans les blogs « apprendre JavaScript » vers 2016, avant que les frameworks ne dominent la une.

#### Tutoriel : construire un minuteur décompte

##### Étape 1 : structure HTML

On pose la base : champ pour les minutes, affichage du décompte, boutons démarrer et réinitialiser.

```html
<div class="Time-option">
  <div class="input-group">
    <input id="input" autocomplete="off" type="text"/>
    <label>minutes</label>
    <button onclick="Reset()" class="btn btn-lg button-refresh">
      <span id="refresh" class="glyphicon refresh-animate glyphicon-refresh glyphicon-refresh-animate"/>
    </button>
  </div>
</div>

<div class="Time">
  <span id="minutes">00</span>
  <span class="min">min</span>
  <span id="seconds">00</span>
  <span class="sec">sec</span>
</div>
<audio></audio>
```

##### Étape 2 : CSS

Ajoutez des styles pour rendre le minuteur lisible et agréable visuellement.

```css
/* Ajoutez vos styles ici */
/* Exemple : */
.Time {
  font-size: 2em;
  font-weight: 300;
}
/* Styles pour champs, labels, boutons */
```

##### Étape 3 : JavaScript

Logique de décompte et de réinitialisation.

```javascript
$(function() {
  // jQuery / JS ici
  // Exemple :
  $('#input').keypress(function(e) {
    if (e.which == 13) { // Entrée
      CheckTick();
    }
  });
});

// Fonctions décompte, CheckTick, Reset
```

##### Étape 4 : tests

- Tester la saisie et le décompte.
- Vérifier le son à zéro.
- Vérifier le reset.

##### Étape 5 : améliorations possibles

- Gestion d’erreur pour entrées non numériques.
- Indicateur visuel « en cours ».
- Mise en page responsive.

##### Étape 6 : déploiement

- Intégrer HTML, CSS et JS aux bons endroits du site.
- Tester sur plusieurs navigateurs.

#### Conclusion

Vous obtenez un décompte fonctionnel, démarrage/reset et alarme optionnelle. Le modèle est ancien mais limpide : facile à adapter, toujours adapté aux sites statiques ou widgets sans étape de build.

### Composant web de sélection de plage de dates (jQuery + plugin)

Ce tutoriel date de l’ère **jQuery + Moment** : on enveloppe deux champs texte dans un élément `<daterangepicker-two-input>`, on l’enregistre avec `customElements.define`, et on confie le conteneur au plugin **Date Range Picker**. Les stacks récentes préfèrent souvent `<input type="date">`, flatpickr ou des composants de date du framework — mais beaucoup de tableaux de bord des années 2010 (et en maintenance) ressemblent encore à ça.

#### Tutoriel : créer un élément personnalisé de plage de dates

##### Introduction

Vous obtenez une petite balise réutilisable qui ouvre le calendrier de plage familier (style arrivée / départ) avec un balisage homogène entre pages.

##### Prérequis

- Bases HTML, CSS et JavaScript
- jQuery et jQuery UI
- Plugin Date Range Picker

##### Étape 1 : HTML de base — librairies

```html
<head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>

  <script src="https://cdn.jsdelivr.net/momentjs/latest/moment.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.min.js"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.css" />
  <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css" />
</head>
```

##### Étape 2 : classe de l’élément personnalisé

```javascript
class DaterangepickerDoubleInput extends HTMLElement {
  constructor() {
    super();
    this.innerHTML = `
    <div class="combine-input-container" id="combine-input-container">
      <div class="c-input-container c1-container">
        <input type='text' class="c-input c1-input" id="c1">
        <label alt='Departure' class="c-label c1-label"></label>
      </div>
      <div class="c-input-container c2-container">
        <input type='text' class="c-input c2-input" id="c2">
        <label alt='Return' class="c-label c2-label"></label>
      </div>
    </div>`;
    this.initDateRangePicker();
  }

  initDateRangePicker() {
    // Initialisation du Date Range Picker
  }
}

window.customElements.define('daterangepicker-two-input', DaterangepickerDoubleInput);
```

##### Étape 3 : initialiser le plugin

```javascript
initDateRangePicker() {
  $('#combine-input-container').daterangepicker({
    // options
  });

  // gestionnaires apply / cancel
}
```

##### Étape 4 : CSS

```css
.combine-input-container { /* … */ }
.c-input-container { /* … */ }
.c-label { /* … */ }
.c-input { /* … */ }
```

##### Étape 5 : utiliser l’élément

```html
<body>
  <daterangepicker-two-input></daterangepicker-two-input>
</body>
```

##### Étape 6 : tests

Tester sur plusieurs navigateurs.

#### Conclusion

Squelette : un élément personnalisé, le plugin sur le conteneur interne, CSS selon le produit.

#### Pistes d’amélioration

- Exposer les options du picker en attributs ou propriétés.
- Renforcer validation et formats locaux (Moment gérait souvent ça).
- Aligner le design sur le reste de l’app.

En maintenance, les pièces restent les mêmes : jQuery pour coller le DOM au plugin, Moment pour l’analyse (longtemps une dépendance du plugin), et le range picker pour l’UI.

### Bulles d’images déplaçables et triables (style Messenger)

#### Tutoriel : images déplaçables et triables avec jQuery

##### Introduction

Ce guide utilise **jQuery** et **jQuery UI** pour des avatars « bulles » circulaires que l’on peut faire glisser et réordonner — les mêmes ingrédients que dans les démos à la mode quand les cercles façon Messenger et les listes triables étaient partout (ère ES5 + jQuery, ~2016). Pratique pour du legacy ou pour garder la recette au même endroit.

##### Prérequis

- Bases HTML, CSS et JavaScript
- Bibliothèques jQuery et jQuery UI

##### Structure HTML

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

##### Style CSS

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

##### Fonction jQuery

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

##### Application

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
