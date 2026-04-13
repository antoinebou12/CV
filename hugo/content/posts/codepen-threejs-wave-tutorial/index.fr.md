---
post_kind: tutorial
title: "Animation de vague 3D Three.js (tutoriel CodePen)"
date: 2016-01-07T12:00:00-04:00
description: Grille de cubes avec un mouvement de vague simple dans Three.js — tutoriel CodePen pas à pas, typique des billets WebGL ~2016.
translationKey: codepen-threejs-wave-tutorial
tags:
    - Three.js
    - WebGL
    - Animation
    - CodePen
    - JavaScript
    - Tutorial
---

## Démo CodePen

{{< codepen antoinebou13 rNoqVOj >}}

### Introduction

Ce tutoriel construit une **animation de vague 3D** avec **Three.js** : scène, caméra, renderer WebGL, grille de cubes et un mouvement ondulant simple — le genre de démo « regardez, du WebGL dans le navigateur » des articles Three.js + CodePen de 2016. Utilisez l’intégration ci-dessus pour modifier en direct.

#### Mise en place de la scène
Scène, caméra perspective et renderer WebGL :

```js

let cubes = [];
let noiseOffset = 0;
const size = 20;
const step = 2;

// Initialisation scène, caméra, renderer
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

// Position de la caméra
camera.position.z = 50;
camera.position.y = 20;
camera.lookAt(0, 0, 0);

```

#### Cubes avec bruit type Perlin

```markdown
// Fonction simplifiant un bruit de type Perlin
function noise(x, y, z) {
  return Math.sin(x) * Math.cos(y) * Math.sin(z);
}

// Création des cubes
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

```markdown
// Boucle d’animation
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

Le code anglais original ajoute écouteurs pour faire tourner la caméra, la déplacer et zoomer — voir la [version anglaise]({{< ref "/posts/codepen-threejs-wave-tutorial/index.md" >}}) pour le bloc complet.

### Conclusion
Vous avez une vague animée de base dans Three.js. Forkez le pen et poussez le mouvement, les matériaux ou la caméra — le pipeline est le même depuis ces tutoriels d’intro WebGL.
