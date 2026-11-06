# Kinectron + p5.js — gestures, sketch controls and GIF export

> Stream Kinect v2 skeletons from Kinectron into p5.js, detect simple gestures from joint positions, replay recorded frames, stop/play the sketch, and save the canvas as a GIF.

- HTML page: https://antoineboucher.info/CV/blog/posts/kinectron-p5-sketch-gif/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/posts/kinectron-p5-sketch-gif/index.md
- Published: 2024-03-15
- Updated: 2026-11-05
- Tags: Kinect, Kinectron, P5.js, JavaScript, Creative Coding, Tutorial
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)For a creative-coding class I needed **Kinectron** skeleton data inside **p5.js**, with simple **play / stop** controls and a way to export a short **GIF** for demos. The sketch draws every tracked joint as a dot, checks six gestures on each body frame, and answers them with particle effects: fireworks on a clap, rising bubbles when a hand is above the hips, falling stars when it is below. As a side experiment, a clap could also toggle a smart device through a tiny local Node server. Notes below follow the code I used.

### Prerequisites
- Basic knowledge of JavaScript and p5.js.
- A **Kinect v2** and a machine running the **Kinectron** server. The sketch connects to it over the LAN by IP address.
- The Kinectron **client** build (`kinectron-client.js`) and p5.js loaded in the page.
- Optional: Node.js if you want the clap-to-toggle bridge at the end.

The joint indices in my sketch follow the **Kinect v2** order (25 joints). Azure Kinect DK body tracking uses a different joint list, so with that sensor you would have to remap the constants before any gesture check works.

### Step 1: Set up the page
Load **one** p5.js build, then the Kinectron client, then your sketch. My first version had both `p5.min.js` and `p5.js` in the head, which is a mistake: the second copy redefines the globals. The sketch does not use `p5.sound`, so it can go too.

```html
<html>
  <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
    <!-- path depends on where your sketch sits relative to the Kinectron client build -->
    <script src="./client/dist/kinectron-client.js"></script>
    <script src="sketch.js"></script>
  </head>
  <body></body>
</html>
```

### Step 2: Joint map and variables
In `sketch.js` I keep a small object that maps joint names to Kinect v2 indices (`SPINEBASE = 0` … `THUMBRIGHT = 24`). Name it something other than `Kinectron`: the client library already defines a `Kinectron` constructor, and a function with the same name would shadow it. Mine is `Kinectron2`.

```javascript
function Kinectron2() {
  this.SPINEBASE = 0;
  this.HEAD = 3;
  this.HANDLEFT = 7;
  this.HANDRIGHT = 11;
  // ... the 25 Kinect v2 joints, up to THUMBRIGHT = 24
}

let kinectron = new Kinectron2();       // replaced by the real client in live mode
const liveData = true;                  // false = replay a recorded JSON file
const recorded_data_file = '../shared/recorded_skeleton.json';
let recorded_skeleton, stopButton, playButton, saveGifButton;
let currentFrame = 0;

function preload() {
  if (!liveData) recorded_skeleton = loadJSON(recorded_data_file);
}
```

### Step 3: Canvas, connection and buttons
In live mode the sketch opens the connection and registers `bodyTracked` as the callback for each tracked body. In recorded mode it adds **Stop** and **Play** buttons instead. **Save as GIF** is created in both modes. All buttons sit just under the 640×480 canvas (`height + 10`).

```javascript
function setup() {
  createCanvas(640, 480);
  background(0);
  if (liveData) {
    kinectron = new Kinectron("192.0.2.10"); // your Kinectron server's LAN address
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

### Step 4: Draw loop and body callback
The two modes feed the same function. Live data arrives through the Kinectron callback. Recorded data is a JSON object keyed by frame index, and `draw()` plays one frame per tick, wrapping around with a modulo so the clip loops. After that, `draw()` updates the three particle lists and removes the ones that faded out or left the canvas.

```javascript
function draw() {
  if (!liveData && recorded_skeleton) {
    currentFrame = currentFrame % Object.keys(recorded_skeleton).length;
    bodyTracked(recorded_skeleton[currentFrame]);
    currentFrame++;
  }
  // update + show fireworks, bubbles, stars; splice the finished ones
}

function bodyTracked(body) {
  background(0);
  drawSkeleton(body);    // one dot per joint at (depthX * width, depthY * height)
  checkForGestures(body);
}
```

Joint positions come as `depthX` / `depthY` values normalized to 0–1, so every threshold below is a fraction of the frame, not pixels.

### Step 5: Gesture checks
Each gesture is a plain function that takes the body and returns a boolean. Instead of a long `if` chain, the sketch builds the function name from a label and looks it up on `window`, then prints the matching labels at the top of the canvas:

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

This only works because the checks are top-level function declarations in a classic script, which puts them on `window`. If you move the sketch to ES modules, use an explicit lookup object instead.

What each check compares:

| Gesture | Rule in the code | Effect |
|---------|------------------|--------|
| Clapping | distance between both hands < 0.05 | 50 firework particles at the right hand |
| OK Sign | hand–thumb and hand–index distances < 0.03 | text only |
| Hand Up | either hand above `SPINEBASE` | 10 bubbles per hand |
| Hand Down | either hand below `SPINEBASE` | 15 stars per hand |
| Both Hands Raised | both hands above `HEAD` | text only |
| Hands Crossed | left hand's x greater than right hand's x | text only |

The clap check is the only one with state. It sets a flag, spawns fireworks, and schedules a request one second later:

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

Because each new trigger clears the pending timeout, the toggle request goes out once, a second after the last clap frame. The `else` branch, though, resets the flag on the very next frame, so while the hands stay together the fireworks fire every other frame. A real cooldown would leave the flag alone until the timeout clears it.

### Step 6: Stop, play and GIF

```javascript
function stopSketch() { noLoop(); }
function playSketch() { loop(); }

function startCreatingGif() {
  saveGif('mySketch', 5);   // records 5 seconds of the canvas, then downloads mySketch.gif
}
```

`saveGif` records and triggers the download by itself. My first version called an extra `downloadGif()` after it, which does not exist anywhere and only threw an error once the recording had started.

### Optional: clap to toggle a device
The request in the clap check goes to a small Express server that uses **tuyapi** to flip a Tuya smart device on the local network. It reads the device state, inverts the boolean at data point `1`, and disconnects:

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

The dependencies are `express`, `cors` and `tuyapi`. CORS is needed because the sketch page and the server run on different origins. My version allowed every origin and answered before the toggle finished, which is fine for a desk demo and not for anything else. The device ID and local key are what tuyapi needs to reach the device locally; keep them out of the repository.

### Step 7: Run it
1. Start the Kinectron server on the Kinect machine and note its LAN address.
2. Serve the sketch folder over HTTP (any static server). Opening `index.html` from disk breaks `loadJSON` in recorded mode.
3. Optional: `npm install` then `node server.js` for the device bridge.
4. Stand in front of the sensor, or set `liveData = false` to replay a recorded skeleton file.

## When to use Kinectron + p5

| Use case | Fit |
|----------|-----|
| Class demo of skeleton data | Strong |
| Production body tracking | Prefer vendor SDK + maintained stack |
| Offline recorded performance | Set `liveData = false` |
| Mobile browsers | Poor — desktop lab |

## Pitfalls

- **Duplicate p5 script tags** in HTML — load one p5 build only.
- **Shadowing the client** — a sketch-side function named `Kinectron` hides the library's constructor. Use another name for your joint map.
- **Kinectron server not running** — the client connects to nothing silently until you check the console.
- **Joints that do not exist** — my OK-sign check asks for `INDEXLEFT` / `INDEXRIGHT`, which are not in the Kinect v2 joint list. The guard returns `false`, so that gesture never fires. `HANDTIPLEFT` / `HANDTIPRIGHT` are the closest joints the sensor provides.
- **Checks that overlap** — "Hand Up" and "Hand Down" test either hand, so one hand up and one hand down reports both. The crossed-hands test compares the same pair of x values twice, so it is really a single comparison.
- **Canvas clearing in live mode** — `background(0)` runs in `bodyTracked`, so the canvas is only cleared when a skeleton frame arrives. With nobody in view, particles leave trails.
- **`saveGif` duration** — long captures freeze older laptops; keep clips under ~5 s for demos.

## Related posts

- [CodePen demos collection](https://antoineboucher.info/CV/blog/posts/codepen-demos-antoinebou13/) — same creative-coding era
- [Snapchat Lens Creator](https://antoineboucher.info/CV/blog/posts/snapchat-lens-creator/) — another tracked-face pipeline

From there you can swap in your own gesture checks or flip `liveData` to replay recorded clips. The buttons, the name-based gesture dispatch and the `saveGif` hook are the parts I kept reusing across assignments.
