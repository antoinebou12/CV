---
post_kind: article
title: "CodePen demos (collection)"
date: 2017-01-10T10:00:00-04:00
description: CodePen embeds plus frontend tutorials in one place—Canvas, Three.js, jQuery UI patterns, screen capture (getDisplayMedia), countdown timer, date range picker, step progress bar, and Messenger-style bubbles.
translationKey: codepen-demos-antoinebou13
aliases:
  - /posts/codepen-blackboard-canvas-tutorial/
  - /fr/posts/codepen-blackboard-canvas-tutorial/
  - /posts/codepen-threejs-wave-tutorial/
  - /fr/posts/codepen-threejs-wave-tutorial/
  - /posts/tutorial-jquery-step-progress-bar/
  - /fr/posts/tutorial-jquery-step-progress-bar/
  - /posts/tutorial-webrtc-screen-capture/
  - /fr/posts/tutorial-webrtc-screen-capture/
  - /posts/tutorial-custom-countdown-timer/
  - /fr/posts/tutorial-custom-countdown-timer/
  - /posts/tutorial-date-range-picker-component/
  - /fr/posts/tutorial-date-range-picker-component/
  - /posts/tutorial-jquery-messenger-image-bubbles/
  - /fr/posts/tutorial-jquery-messenger-image-bubbles/
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

Small experiments on **CodePen** (live embeds below) plus standalone write-ups that used to be separate posts—jQuery/CSS patterns, `getDisplayMedia`, and other front-end notes—gathered here for one bookmark.

## Small pens

### BMdzwx

{{< codepen antoinebou13 BMdzwx 420 >}}

[Open on CodePen](https://codepen.io/antoinebou13/pen/BMdzwx)

### Details view (xMXNyy)

{{< codepen antoinebou13 xMXNyy 420 >}}

[Open on CodePen](https://codepen.io/antoinebou13/details/xMXNyy)

### JxrqQx

{{< codepen antoinebou13 JxrqQx 420 >}}

[Open on CodePen](https://codepen.io/antoinebou13/pen/JxrqQx)

### byVQKJ

{{< codepen antoinebou13 byVQKJ 420 >}}

[Open on CodePen](https://codepen.io/antoinebou13/pen/byVQKJ)

### jjzxER

{{< codepen antoinebou13 jjzxER 420 >}}

[Open on CodePen](https://codepen.io/antoinebou13/pen/jjzxER)

### qzQpYg

{{< codepen antoinebou13 qzQpYg 420 >}}

[Open on CodePen](https://codepen.io/antoinebou13/pen/qzQpYg)

### ZEENwWB

{{< codepen antoinebou13 ZEENwWB 420 >}}

[Open on CodePen](https://codepen.io/antoinebou13/pen/ZEENwWB)

---

## HTML5 Canvas blackboard (tutorial)

{{< codepen antoinebou13 MLEdxr 520 >}}

### Introduction

This tutorial walks through a simple interactive blackboard with **HTML5 Canvas** and plain JavaScript: drawing, pulling in images via the File API, and clearing the board. It matches the kind of step-by-step CodePen write-up that was common in the mid-2010s. Use the embed above to see the finished behavior.

### Setting Up the Canvas

First, we need to set up the HTML5 canvas element. This is where all the drawing will take place.

```html
<canvas id="drawingCanvas"></canvas>
```

In your CSS, make sure the canvas takes the full screen and has a dark background to mimic a blackboard:

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

### Adding Controls

We'll add some basic controls for color selection, pen size, saving the canvas as an image, and an option to erase the canvas.

```html
<input type="color" id="colorPicker" value="#FFFFFF">
<input type="range" id="penSize" min="1" max="20" value="5">
<button id="saveImage">Save Image</button>
<button id="eraseCanvas">Erase</button>
<input type="file" id="imageLoader" name="imageLoader" accept="image/*">
```

Style these controls so they are easily accessible:

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

### Implementing the Drawing Logic

Now, let's write the JavaScript to handle drawing on the canvas. We'll set up event listeners to handle mouse movements and draw on the canvas.

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

    // Check if an image is being clicked
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

On load we size the canvas to the viewport, grab the 2D context, and wire `mousedown` / `mousemove` / `mouseup`. Each stroke is a path object in `drawingObjects`; `redrawCanvas` paints imported images first, then connects the points for each path.

### Adding Image Loading and Erasing Features

Next, we add the functionality to load images onto the canvas and erase the contents of the canvas.

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

    // Draw all image objects
    imageObjects.forEach(imgObj => {
        ctx.drawImage(imgObj.img, imgObj.x, imgObj.y);
    });

    // Draw all drawing paths
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

`FileReader.readAsDataURL` decodes the picked file into a data URL; when the image loads we push a draggable object into `imageObjects`. `eraseCanvas` clears the bitmap and resets both arrays.

### Conclusion

You now have a working blackboard on Canvas. Fork it on CodePen and extend it—extra brushes, undo, or pressure sensitivity are natural next steps; the APIs are the same ones we have been using since this style of tutorial was current.

---

## Three.js wave (tutorial)

{{< codepen antoinebou13 rNoqVOj 560 >}}

### Introduction

This walkthrough builds a **3D wave animation** with **Three.js**: scene, camera, WebGL renderer, a grid of cubes, and a simple undulating motion—the sort of “look, WebGL in the browser” demo that fit right in with mid-2010s Three.js + CodePen articles. Use the embed above to tweak it live.

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

```js
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

```js
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

```js
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

### Conclusion

You now have a basic animated wave in Three.js. Fork the pen and push the motion, materials, or camera—same pipeline people have been iterating on since these kinds of tutorials were the default intro to WebGL in the browser.

---

## More frontend tutorials (non-CodePen)

These were originally separate posts; they are plain Markdown and code samples (no CodePen iframe).

### Responsive step progress bar (jQuery + CSS)

This code creates a responsive progress bar with four steps. It uses jQuery for dynamic text changes and CSS for styling. Here's a breakdown of its functionality:

#### HTML Structure

- The progress bar is wrapped inside a `div` with the class `progressbar_container`.
- An unordered list (`ul`) with the class `progressbar` represents the progress bar.
- Each step in the progress bar is an `li` element with the class `progressbar_node`.
- The current step is highlighted by adding the class `current_node`.

#### CSS Styling

- The `.progressbar_container` is styled to position the progress bar, manage its size, and center it.
- Each `.progressbar_node` represents a step in the progress bar.
- The `:before` pseudo-element of `.progressbar_node` creates circular step indicators with numbers.
- The `:after` pseudo-element creates connecting lines between the steps.
- The current and completed steps are highlighted with a darker color and a solid border.

#### JavaScript Functionality

- On document ready (`$(document).ready`), the previous steps to the current step are marked as completed using the class `activated_node`.
- A resize event listener (`$(window).resize`) changes the text of the first step based on the window's width. It toggles between "PASSENGER" and "PASSENGER DETAILS".

#### Notes

- Ensure you have included the jQuery library to use the jQuery syntax.
- The resizing functionality helps maintain responsiveness, providing a better experience on different screen sizes.

#### Example Usage

To use this progress bar, include the provided HTML in your document. Ensure your CSS is properly linked, and the jQuery library is included for the JavaScript to work correctly.

#### Enhancements

- You can modify the number of steps by adjusting the HTML and potentially tweaking the CSS.
- Consider adding ARIA attributes for accessibility, making the progress bar usable for screen readers.
- You could enhance the responsiveness further by using CSS media queries instead of JavaScript for text changes.

This progress bar is a great way to visually represent progress through a multi-step process, such as a checkout or registration flow.

### Screen capture in the browser (`getDisplayMedia`)

#### Tutorial: Building a Screen Capture Utility with HTML, CSS, and JavaScript

##### Introduction

This tutorial demonstrates how to create a screen capture utility in a web application. We will use HTML for the structure, CSS for styling, and JavaScript for functionality.

##### Prerequisites

- Basic understanding of HTML, CSS, and JavaScript
- A modern web browser with support for `getDisplayMedia`

##### HTML Setup

First, we create the HTML structure with buttons for starting and stopping the screen capture and a section to display the video.

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

##### CSS Styling

Next, style the elements for a better user interface.

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

##### JavaScript Functionality

Implement the JavaScript to handle screen capture and logging.

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
    // Handle different types of errors here
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

##### Error Handling

Add appropriate error handling in the `catch` block of the `startCapture` function for different types of errors.

##### Conclusion

With this setup, you can start and stop screen capture in your web application. The log section will display information about the screen capture and any errors encountered. This utility can be useful in various applications like tutorials, presentations, or remote assistance tools.

### Custom countdown timer (HTML, CSS, JavaScript)

This is a straight DOM-and-`setInterval` countdown: minutes in, tick down, start and reset, and a short audio clip when it hits zero — the sort of thing that showed up in every "learn JavaScript" blog around 2016 before frameworks swallowed the front page.

#### Tutorial: Building a Custom Countdown Timer

##### Step 1: Setting Up the HTML Structure

First, we'll create the basic structure of the timer. This includes input fields for minutes, a display for the countdown, and buttons to start and reset the timer.

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

##### Step 2: Adding CSS for Styling

Next, we'll add CSS to style our timer. This will make the timer more user-friendly and visually appealing.

```css
/* Add your CSS styling here */
/* Example: */
.Time {
  font-size: 2em;
  font-weight: 300;
}
/* Add styles for inputs, labels, and buttons */
```

##### Step 3: JavaScript Functionality

Now, we'll add JavaScript to make the timer functional. This includes the countdown logic and the reset functionality.

```javascript
$(function() {
  // Add your jQuery and JavaScript code here
  // Example:
  $('#input').keypress(function(e) {
    if (e.which == 13) { // Enter key pressed
      CheckTick();
    }
  });
});

// Add functions for countdown, CheckTick, and Reset
```

##### Step 4: Testing and Debugging

- Test the timer by entering a value and seeing if it counts down correctly.
- Ensure the audio plays when the timer reaches zero.
- Test the reset functionality to see if it stops and resets the timer as expected.

##### Step 5: Additional Features and Improvements

- Add error handling for non-numeric inputs.
- Implement a visual indicator for when the timer is running.
- Style the timer to be responsive for better mobile device compatibility.

##### Step 6: Deployment

- If you're using this timer on a website, embed the HTML, CSS, and JavaScript into the appropriate sections of your webpage.
- Test the timer in different browsers to ensure cross-browser compatibility.

#### Conclusion

You end up with a working countdown, start/reset, and optional alarm. The pattern is old but transparent: easy to adapt, and still fine for static sites or embedded widgets without a build step.

### Date range picker web component (jQuery + plugin)

This walkthrough is from the jQuery-and-Moment era: you wrap two text inputs in a custom element `<daterangepicker-two-input>`, register it with `customElements.define`, and hand the container off to the Date Range Picker plugin. Newer stacks usually reach for native `<input type="date">`, flatpickr, or framework date components — but plenty of dashboards shipped in the mid-2010s (and many still in maintenance) look exactly like this.

#### Tutorial: Creating a Custom Date Range Picker Element

##### Introduction

You end up with a small reusable tag that opens the familiar range calendar UI (check-in / check-out style) while keeping the markup consistent across pages.

##### Prerequisites

- Basic knowledge of HTML, CSS, and JavaScript
- jQuery and jQuery UI libraries
- Date Range Picker plugin

##### Step 1: Setup Basic HTML

First, include the necessary libraries in your HTML file's head section:

```html
<head>
  <!-- jQuery and jQuery UI -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>

  <!-- Date Range Picker plugin -->
  <script src="https://cdn.jsdelivr.net/momentjs/latest/moment.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.min.js"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/daterangepicker/daterangepicker.css" />
  <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css" />
</head>
```

##### Step 2: Define Custom Element Structure

Create the custom element class in JavaScript:

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
    // Initialization code for the Date Range Picker
  }
}

window.customElements.define('daterangepicker-two-input', DaterangepickerDoubleInput);
```

##### Step 3: Initialize Date Range Picker

In the `initDateRangePicker` method, initialize the date range picker:

```javascript
initDateRangePicker() {
  $('#combine-input-container').daterangepicker({
    // Date Range Picker options here
  });

  // Event handlers for apply and cancel actions
}
```

##### Step 4: Style the Custom Element

Use CSS to style your custom element:

```css
.combine-input-container {
  /* Your styles here */
}

.c-input-container {
  /* Styles for input containers */
}

.c-label {
  /* Styles for labels */
}

.c-input {
  /* Styles for input fields */
}
```

##### Step 5: Add Custom Element to HTML

Use your custom element in the HTML body:

```html
<body>
  <daterangepicker-two-input></daterangepicker-two-input>
</body>
```

##### Step 6: Test and Debug

Test your custom element in various browsers to ensure compatibility and fix any bugs that arise.

#### Conclusion

That's the skeleton: one custom element, the plugin bound to the inner container, and CSS however your product needs it.

#### Further Enhancements

- Expose picker options as attributes or properties on the element.
- Tighten validation and locale-specific formats (Moment still handled most of that in this stack).
- Match whatever design system the rest of the app used in 2019–2021.

If you're maintaining something built this way, the moving parts are still the same: jQuery for DOM/plugin glue, Moment for parsing (the plugin depended on it for years), and the range picker for the actual UI.

### Draggable, sortable image bubbles (Messenger-style)

#### Tutorial: Creating Draggable and Sortable Images with jQuery

##### Introduction

This walkthrough uses jQuery and jQuery UI to build circular "bubble" avatars you can drag and reorder — the same ingredients that showed up in countless demos when Messenger-style circles and sortable lists were everywhere (roughly the ES5 + jQuery era, ~2016). Handy for legacy pages or if you want the recipe in one place.

##### Prerequisites

- Basic knowledge of HTML, CSS, and JavaScript
- jQuery and jQuery UI library

##### HTML Structure

We start by setting up our HTML structure with two unordered lists (`ul`) and list items (`li`) containing images.

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

##### CSS Styling

Next, we style the unordered lists and images. We remove the default list styling and set some basic styles for the images.

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

##### jQuery Function

We create a jQuery function to apply the rounded shape and make images either draggable or default based on the option passed.

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

##### Applying the Function

Finally, we apply the jQuery function to our images and enable sorting and dragging functionalities.

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

Following these steps gives you draggable, sortable circular images on a page — jQuery UI all the way, but it still behaves the same in any browser where you include the libraries.
