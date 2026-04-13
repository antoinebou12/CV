---
post_kind: tutorial
title: "Three.js 3D wave animation (CodePen tutorial)"
date: 2016-01-07T12:00:00-04:00
description: Grid of cubes with a simple wave motion in Three.js — step-by-step CodePen tutorial, typical of the WebGL curiosity posts from ~2016.
translationKey: codepen-threejs-wave-tutorial
tags:
    - Three.js
    - WebGL
    - CodePen
    - JavaScript
    - Tutorial
---

## CodePen demo

{{< codepen antoinebou13 rNoqVOj >}}

### Introduction

This walkthrough builds a **3D wave animation** with **Three.js**: scene, camera, WebGL renderer, a grid of cubes, and a simple undulating motion — the sort of “look, WebGL in the browser” demo that fit right in with 2016 Three.js + CodePen articles. Use the embed above to tweak it live.

#### Setting Up the Scene
First, let's set up the basic components of any Three.js scene: the scene itself, a camera, and a WebGL renderer. Add the following code to initialize these components:

```js

let cubes = [];
let noiseOffset = 0;
const size = 20;
const step = 2;

// Initialize Three.js Scene, Camera, Renderer
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

// Position the Camera
camera.position.z = 50;
camera.position.y = 20;
camera.lookAt(0, 0, 0);

```
This code creates a 3D scene, adds a perspective camera, and sets up the WebGL renderer to display our graphics.

#### Adding Cubes with Perlin Noise
Now, let's add cubes to our scene. We'll use Perlin noise to vary the Y-position of each cube, creating a wave-like effect. Here's how you can do it:

```markdown
// Function to simulate Perlin noise
function noise(x, y, z) {
  return Math.sin(x) * Math.cos(y) * Math.sin(z);
}

// Create cubes using Perlin noise
for (let x = -size; x <= size; x += step) {
  for (let z = -size; z <= size; z += step) {
    const y = noise(x * 0.1, noiseOffset, z * 0.1) * 10;
    const geometry = new THREE.BoxGeometry();
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const cube = new THREE.Mesh(geometry, material);
    cube.position.set(x, y, z);
    scene.add(cube);
    cubes.push(cube); // Store the cube
  }
  noiseOffset += 0.1;
}
```

In this snippet, we create multiple cubes and position them based on Perlin noise, giving us the initial setup for our wave animation.

#### Animating the Cubes

To animate our cubes, we'll update their Y-position in an animation loop. This continuous update creates the illusion of a moving wave. Here's the code for our animation loop:

```markdown
// Animation Loop with Wave Animation
let waveOffset = 0;
function animate() {
  requestAnimationFrame(animate);
  updateCameraPosition();

  // Update each cube's Y position for the wave effect
  cubes.forEach((cube, i) => {
    cube.position.y =
      noise(cube.position.x * 0.1, waveOffset, cube.position.z * 0.1) * 10;
  });
  waveOffset += 0.01; // Change this value to control the speed of the wave

  renderer.render(scene, camera);
}
animate();
```


The `animate` function is called repeatedly, updating the position of each cube to simulate a wave.

#### Adding Interaction

To make our scene interactive, we'll add event listeners for mouse and keyboard inputs. This allows users to control the camera and explore the 3D space.

```markdown
// Mouse Controls
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

// Gamepad Controls
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

// Keyboard event listeners
document.addEventListener("keydown", function (event) {
  keyStates[event.code] = true;
});

document.addEventListener("keyup", function (event) {
  keyStates[event.code] = false;
});

// Update camera position based on keyboard input
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

// Mouse Scroll Control
document.addEventListener("wheel", function (e) {
  camera.position.z += e.deltaY * 0.01;
});
```

These event listeners enable users to rotate the camera and zoom in and out, enhancing the interactive experience.

Wrap up the tutorial with a conclusion that encourages readers to experiment with the code and learn more about Three.js.

You now have a basic animated wave in Three.js. Fork the pen and push the motion, materials, or camera — same pipeline people have been iterating on since these kinds of tutorials were the default intro to WebGL in the browser.