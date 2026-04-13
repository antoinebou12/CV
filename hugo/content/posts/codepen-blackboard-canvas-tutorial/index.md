---
post_kind: tutorial
title: "HTML5 Canvas blackboard (CodePen tutorial)"
date: 2016-01-07T11:00:00-04:00
description: Interactive canvas blackboard with drawing, image import, and erase — CodePen demo, in the spirit of 2016-era Canvas tutorials.
translationKey: codepen-blackboard-canvas-tutorial
tags:
    - Canvas
    - JavaScript
    - CodePen
    - Tutorial
    - Frontend
---

## CodePen demo

{{< codepen antoinebou13 MLEdxr >}}


## Introduction

This tutorial walks through a simple interactive blackboard with **HTML5 Canvas** and plain JavaScript: drawing, pulling in images via the File API, and clearing the board. It matches the kind of step-by-step CodePen write-up that was everywhere around 2016. Use the embed above to see the finished behavior.


## Setting Up the Canvas

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

## Adding Controls

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

## Implementing the Drawing Logic

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

In this section, explain how to initialize the canvas, set up the context, and handle different mouse events for drawing lines on the canvas.

## Adding Image Loading and Erasing Features

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

Describe how to use the File Reader API to load images and draw them on the canvas, as well as how to clear the canvas when the erase button is clicked.


Wrap up the tutorial by encouraging readers to experiment with the code and explore more features they can add. Mention that the tutorial provides a basic foundation for creating interactive canvas-based web applications.

You now have a working blackboard on Canvas. Fork it on CodePen and extend it — extra brushes, undo, or pressure sensitivity are natural next steps; the APIs are the same ones we have been using since this style of tutorial was current.

