---
post_kind: tutorial
title: "Screen capture in the browser (getDisplayMedia)"
date: 2024-02-10T10:00:00-04:00
description: Start/stop screen sharing with the Screen Capture API, a video element, and simple logging.
tags:
    - WebRTC
    - getDisplayMedia
    - JavaScript
    - HTML
    - Tutorial
    - Frontend
---

### Tutorial: Building a Screen Capture Utility with HTML, CSS, and JavaScript

#### Introduction
This tutorial demonstrates how to create a screen capture utility in a web application. We will use HTML for the structure, CSS for styling, and JavaScript for functionality.

#### Prerequisites
- Basic understanding of HTML, CSS, and JavaScript
- A modern web browser with support for `getDisplayMedia`

#### HTML Setup
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

#### CSS Styling
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

#### JavaScript Functionality
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
console.warn = msg => $logElem.append(`<span class="warn">${msg}<span><br>`);
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

#### Error Handling
Add appropriate error handling in the `catch` block of the `startCapture` function for different types of errors.

#### Conclusion
With this setup, you can start and stop screen capture in your web application. The log section will display information about the screen capture and any errors encountered. This utility can be useful in various applications like tutorials, presentations, or remote assistance tools.