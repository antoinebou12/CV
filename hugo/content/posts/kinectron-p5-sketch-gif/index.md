---
post_kind: article
title: "Kinectron + p5.js — sketch controls and GIF export"
date: 2024-03-15T10:00:00-04:00
description: Wire up Kinectron with p5.js, play/stop the sketch, and save output as a GIF (Kinect v2 or Azure Kinect DK).
tags:
    - Kinect
    - Kinectron
    - p5.js
    - JavaScript
    - Creative coding
    - Tutorial
images:
    - mySketch.gif
---

### Introduction

This tutorial will guide you through setting up a Kinectron sketch in p5.js, which includes functionality for stopping and playing the sketch, as well as saving it as a GIF.

### Prerequisites
- Basic knowledge of JavaScript and p5.js.
- Kinectron library installed.
- p5.js library installed.
- Have a Kinect v2 or Azure Kinect DK.
- Have a Kinectron server running.
- Have a local or online environment that supports JavaScript and p5.js.

### Step 1: Set Up Your Environment
Ensure you have the p5.js and Kinectron libraries included in your HTML file.

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

### Step 2: Initialize Variables
In your `sketch.js` file, start by defining the necessary variables.

```javascript
// Kinectron setup function
function Kinectron() {
  // Define Kinectron joint types
}

let kinectron = new Kinectron();

const liveData = false;
let stopButton, playButton, saveGifButton;
let recorded_skeleton;

function preload() {
  // Load recorded data if liveData is false
}
```

### Step 3: Setup the Canvas and Buttons
Create the canvas and buttons for controlling the sketch.

```javascript
function setup() {
  createCanvas(640, 480);
  background(0);

  if (liveData) {
    // Initialize Kinectron for live data
  } else {
    // Setup for pre-recorded data and buttons
  }
}
```

### Step 4: Draw Function
Implement the `draw` function to handle live and recorded data.

```javascript
function draw() {
  // Handle live or recorded data
}
```

### Step 5: Implement Gesture Checking
Create functions to check for specific gestures in the Kinectron data.

```javascript
function checkForGestures(body) {
  // Check and display each gesture
}

function isClapping(body) { /* ... */ }
function isOKSign(body) { /* ... */ }
// Implement other gesture functions
```

### Step 6: Create Button Functions
Define functions for stop, play, and save GIF buttons.

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
  // Additional code for downloading the GIF
}
```

### Step 7: Run Your Sketch
Run your sketch in a local or online environment that supports JavaScript and p5.js.



This tutorial guided you through setting up a Kinectron sketch in p5.js with additional features for controlling the sketch playback and saving it as a GIF. Experiment with different gestures and functionalities to enhance your sketch further.