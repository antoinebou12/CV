---
post_kind: tutorial
title: "Capture d’écran dans le navigateur (getDisplayMedia)"
date: 2024-02-10T10:00:00-04:00
description: Démarrer / arrêter le partage d’écran avec l’API Screen Capture, une balise vidéo et un journal simple.
translationKey: tutorial-webrtc-screen-capture
tags:
    - WebRTC
    - JavaScript
    - HTML
    - Tutorial
    - Frontend
---

### Tutoriel : utilitaire de capture d’écran avec HTML, CSS et JavaScript

#### Introduction
Ce tutoriel montre comment ajouter une capture d’écran dans une appli web : HTML pour la structure, CSS pour le style, JavaScript pour le comportement.

#### Prérequis
- Bases HTML, CSS et JavaScript
- Navigateur récent avec support de `getDisplayMedia`

#### Structure HTML
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

#### CSS
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

#### JavaScript
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

#### Gestion d’erreurs
Complétez le bloc `catch` de `startCapture` selon les cas à gérer.

#### Conclusion
Vous pouvez démarrer et arrêter la capture d’écran ; la zone de log affiche les infos de piste et les erreurs. Utile pour tutoriels, présentations ou assistance à distance.
