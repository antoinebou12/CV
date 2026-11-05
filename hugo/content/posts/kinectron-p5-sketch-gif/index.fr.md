---
post_kind: article
title: "Kinectron + p5.js — gestes, contrôle du sketch et export GIF"
date: 2024-03-15T10:00:00-04:00
lastmod: 2026-11-05T12:00:00-05:00
description: Recevoir les squelettes Kinect v2 de Kinectron dans p5.js, détecter des gestes simples à partir des articulations, rejouer des images enregistrées, arrêter / relancer le sketch et enregistrer le canvas en GIF.
translationKey: kinectron-p5-sketch-gif
tags:
    - Kinect
    - Kinectron
    - p5.js
    - JavaScript
    - Creative Coding
    - Tutorial
images:
    - images/mySketch.gif
---

Pour un cours de creative coding, j’avais besoin des données squelette **Kinectron** dans **p5.js**, avec **lecture / pause** et un export **GIF** court pour les démos. Le sketch dessine chaque articulation suivie sous forme de point, teste six gestes à chaque image du corps et y répond avec des particules : feux d’artifice sur un clap, bulles qui montent quand une main est au-dessus des hanches, étoiles qui tombent quand elle est en dessous. En expérience annexe, un clap pouvait aussi basculer un appareil connecté via un petit serveur Node local. Les notes ci-dessous suivent le code que j’ai utilisé.

<!--more-->

### Prérequis
- Bases JavaScript et p5.js.
- Une **Kinect v2** et une machine qui fait tourner le serveur **Kinectron**. Le sketch s’y connecte sur le réseau local par adresse IP.
- Le build **client** de Kinectron (`kinectron-client.js`) et p5.js chargés dans la page.
- Optionnel : Node.js pour le pont « clap → appareil » à la fin.

Les indices d’articulations de mon sketch suivent l’ordre de la **Kinect v2** (25 articulations). Le suivi corporel de l’Azure Kinect DK utilise une autre liste : avec ce capteur, il faut remapper les constantes avant que le moindre geste fonctionne.

### Étape 1 : la page
Charger **un seul** build de p5.js, puis le client Kinectron, puis le sketch. Ma première version avait à la fois `p5.min.js` et `p5.js` dans le head, ce qui est une erreur : la deuxième copie redéfinit les globales. Le sketch n’utilise pas `p5.sound`, on peut donc l’enlever aussi.

```html
<html>
  <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
    <!-- le chemin dépend de l’emplacement du sketch par rapport au build client de Kinectron -->
    <script src="./client/dist/kinectron-client.js"></script>
    <script src="sketch.js"></script>
  </head>
  <body></body>
</html>
```

### Étape 2 : table des articulations et variables
Dans `sketch.js`, je garde un petit objet qui associe les noms d’articulations aux indices Kinect v2 (`SPINEBASE = 0` … `THUMBRIGHT = 24`). Ne l’appelez pas `Kinectron` : la bibliothèque client définit déjà un constructeur `Kinectron`, et une fonction du même nom le masquerait. Le mien s’appelle `Kinectron2`.

```javascript
function Kinectron2() {
  this.SPINEBASE = 0;
  this.HEAD = 3;
  this.HANDLEFT = 7;
  this.HANDRIGHT = 11;
  // ... les 25 articulations Kinect v2, jusqu’à THUMBRIGHT = 24
}

let kinectron = new Kinectron2();       // remplacé par le vrai client en mode direct
const liveData = true;                  // false = rejouer un fichier JSON enregistré
const recorded_data_file = '../shared/recorded_skeleton.json';
let recorded_skeleton, stopButton, playButton, saveGifButton;
let currentFrame = 0;

function preload() {
  if (!liveData) recorded_skeleton = loadJSON(recorded_data_file);
}
```

### Étape 3 : canvas, connexion et boutons
En mode direct, le sketch ouvre la connexion et enregistre `bodyTracked` comme callback pour chaque corps suivi. En mode enregistré, il ajoute plutôt des boutons **Stop** et **Play**. **Save as GIF** est créé dans les deux modes. Tous les boutons sont placés juste sous le canvas 640×480 (`height + 10`).

```javascript
function setup() {
  createCanvas(640, 480);
  background(0);
  if (liveData) {
    kinectron = new Kinectron("192.0.2.10"); // adresse réseau local du serveur Kinectron
    kinectron.makeConnection();
    kinectron.startTrackedBodies(bodyTracked);
  } else {
    // createButton('Stop') -> stopSketch, createButton('Play') -> playSketch
  }
  saveGifButton = createButton('Save as GIF');
  saveGifButton.position(90, height + 10);
  saveGifButton.mousePressed(startCreatingGif);
}
```

### Étape 4 : boucle draw et callback du corps
Les deux modes alimentent la même fonction. Les données en direct arrivent par le callback Kinectron. Les données enregistrées sont un objet JSON indexé par numéro d’image, et `draw()` en joue une par tick, avec un modulo pour boucler l’extrait. Ensuite, `draw()` met à jour les trois listes de particules et retire celles qui ont disparu ou quitté le canvas.

```javascript
function draw() {
  if (!liveData && recorded_skeleton) {
    currentFrame = currentFrame % Object.keys(recorded_skeleton).length;
    bodyTracked(recorded_skeleton[currentFrame]);
    currentFrame++;
  }
  // mise à jour + affichage des feux, bulles, étoiles ; splice des particules finies
}

function bodyTracked(body) {
  background(0);
  drawSkeleton(body);    // un point par articulation en (depthX * width, depthY * height)
  checkForGestures(body);
}
```

Les positions arrivent en `depthX` / `depthY` normalisés entre 0 et 1 : tous les seuils ci-dessous sont des fractions de l’image, pas des pixels.

### Étape 5 : détection des gestes
Chaque geste est une simple fonction qui prend le corps et renvoie un booléen. Plutôt qu’une longue chaîne de `if`, le sketch construit le nom de la fonction à partir d’une étiquette, la cherche sur `window`, puis affiche les étiquettes détectées en haut du canvas :

```javascript
function checkForGestures(body) {
  let detected = [];
  const gestures = ["Clapping", "OK Sign", "Hand Up", "Hand Down",
                    "Hands Crossed", "Both Hands Raised"];
  gestures.forEach(gesture => {
    let fn = `is${gesture.replace(/\s/g, '')}`;   // "OK Sign" -> isOKSign
    if (typeof window[fn] === 'function' && window[fn](body)) {
      detected.push(gesture);
    }
  });
  if (detected.length > 0) displayText(detected.join(", "));
}
```

Ça ne marche que parce que les tests sont des déclarations de fonctions au premier niveau d’un script classique, ce qui les place sur `window`. Si vous passez le sketch en modules ES, utilisez plutôt un objet de correspondance explicite.

Ce que compare chaque test :

| Geste | Règle dans le code | Effet |
|-------|--------------------|-------|
| Clapping | distance entre les deux mains < 0,05 | 50 particules de feu d’artifice à la main droite |
| OK Sign | distances main–pouce et main–index < 0,03 | texte seulement |
| Hand Up | une des mains au-dessus de `SPINEBASE` | 10 bulles par main |
| Hand Down | une des mains sous `SPINEBASE` | 15 étoiles par main |
| Both Hands Raised | les deux mains au-dessus de `HEAD` | texte seulement |
| Hands Crossed | x de la main gauche plus grand que x de la main droite | texte seulement |

Le clap est le seul test avec un état. Il lève un drapeau, lance les feux d’artifice et programme une requête une seconde plus tard :

```javascript
if (distance < 0.05 && !isClapped) {
  isClapped = true;
  triggerFireworks(rightHand.depthX * width, rightHand.depthY * height);
  if (clapTimeout) clearTimeout(clapTimeout);
  clapTimeout = setTimeout(() => {
    const req = new XMLHttpRequest();
    req.open("GET", "http://localhost:3000/toggleDevice");
    req.send();
    isClapped = false;
  }, clapWaitTime);   // 1000 ms
  return true;
} else {
  isClapped = false;
}
```

Comme chaque nouveau déclenchement annule le timeout en attente, la requête ne part qu’une fois, une seconde après la dernière image de clap. Par contre, la branche `else` remet le drapeau à `false` dès l’image suivante : tant que les mains restent collées, les feux d’artifice partent une image sur deux. Un vrai délai de récupération laisserait le drapeau tranquille jusqu’à ce que le timeout le remette à zéro.

### Étape 6 : stop, play et GIF

```javascript
function stopSketch() { noLoop(); }
function playSketch() { loop(); }

function startCreatingGif() {
  saveGif('mySketch', 5);   // enregistre 5 secondes du canvas, puis télécharge mySketch.gif
}
```

`saveGif` enregistre et lance le téléchargement tout seul. Ma première version appelait en plus `downloadGif()`, qui n’existe nulle part et ne faisait que lever une erreur une fois l’enregistrement lancé.

### Optionnel : un clap pour basculer un appareil
La requête du test de clap arrive sur un petit serveur Express qui utilise **tuyapi** pour basculer un appareil connecté Tuya sur le réseau local. Il lit l’état de l’appareil, inverse le booléen du point de données `1`, puis se déconnecte :

```javascript
async function toggleDevice(deviceId, deviceKey) {
  const device = new TuyAPI({ id: deviceId, key: deviceKey });
  try {
    await device.find();
    await device.connect();
    const status = await device.get({ schema: true });
    await device.set({ set: !status.dps['1'] });
  } finally {
    device.disconnect();
  }
}
app.get('/toggleDevice', (req, res) => {
  toggleDevice('<device-id>', '<local-key>');
  res.send('ok');
});
```

Les dépendances sont `express`, `cors` et `tuyapi`. CORS est nécessaire parce que la page du sketch et le serveur n’ont pas la même origine. Ma version acceptait toutes les origines et répondait avant la fin de la bascule : acceptable pour une démo sur un bureau, pas au-delà. L’identifiant de l’appareil et sa clé locale sont ce dont tuyapi a besoin pour le joindre en local ; gardez-les hors du dépôt.

### Étape 7 : lancer le sketch
1. Démarrer le serveur Kinectron sur la machine reliée à la Kinect et noter son adresse sur le réseau local.
2. Servir le dossier du sketch en HTTP (n’importe quel serveur statique). Ouvrir `index.html` depuis le disque casse `loadJSON` en mode enregistré.
3. Optionnel : `npm install` puis `node server.js` pour le pont vers l’appareil.
4. Se placer devant le capteur, ou mettre `liveData = false` pour rejouer un fichier de squelette enregistré.

## Quand utiliser Kinectron + p5

| Cas d’usage | Adéquation |
|-------------|------------|
| Démo de cours sur les données squelette | Forte |
| Suivi corporel en production | Préférer le SDK du fabricant et une pile maintenue |
| Performance enregistrée hors ligne | Mettre `liveData = false` |
| Navigateurs mobiles | Faible — labo sur poste de travail |

## Pièges

- **Balises p5 en double** dans le HTML — charger un seul build de p5.
- **Masquer le client** — une fonction du sketch nommée `Kinectron` cache le constructeur de la bibliothèque. Donnez un autre nom à votre table d’articulations.
- **Serveur Kinectron arrêté** — le client ne se connecte à rien, sans bruit, tant qu’on ne regarde pas la console.
- **Articulations qui n’existent pas** — mon test « OK » demande `INDEXLEFT` / `INDEXRIGHT`, qui ne font pas partie des articulations Kinect v2. La garde renvoie `false`, donc ce geste ne se déclenche jamais. `HANDTIPLEFT` / `HANDTIPRIGHT` sont les articulations les plus proches que le capteur fournit.
- **Tests qui se chevauchent** — « Hand Up » et « Hand Down » testent l’une ou l’autre main : une main levée et une main baissée déclenchent les deux. Le test des mains croisées compare deux fois la même paire de x, c’est en réalité une seule comparaison.
- **Effacement du canvas en mode direct** — `background(0)` est appelé dans `bodyTracked`, donc le canvas n’est effacé qu’à l’arrivée d’une image de squelette. Sans personne devant le capteur, les particules laissent des traînées.
- **Durée de `saveGif`** — les captures longues figent les vieux portables ; restez sous ~5 s pour les démos.

## Articles liés

- [Collection de démos CodePen]({{< ref "/posts/codepen-demos-antoinebou13/index.fr.md" >}}) — même période creative coding
- [Snapchat Lens Creator]({{< ref "/posts/snapchat-lens-creator/index.fr.md" >}}) — un autre pipeline de suivi du visage

À partir de là, vous pouvez brancher vos propres gestes ou basculer `liveData` pour rejouer des extraits enregistrés. Les boutons, la détection des gestes par nom de fonction et le hook `saveGif` sont les morceaux que je réutilisais d’un devoir à l’autre.
