---
title: "WearTrailsExperiments: contact-driven wear trails in the browser"
date: 2026-11-05T12:00:00-05:00
description: "three.js and Ammo.js experiments that turn rigid-body contact, traction and sliding into wear, sliding-distance and flow maps on a ground texture."
translationKey: repository-note-weartrailsexperiments
repository_note: "WearTrailsExperiments"
---

# WearTrailsExperiments

<div class="repo-status-row"><span class="repo-badge kind">Web experiments</span></div>

<div class="repo-tech-badges"><span class="tag tool">JavaScript</span><span class="tag tool">three.js</span><span class="tag tool">Ammo.js</span><span class="tag tool">WebGL</span><span class="tag tool">glTF / GLB</span></div>

WearTrailsExperiments gathers browser prototypes that turn the contact between a sliding body and the ground into persistent wear and flow maps. They explore, in JavaScript, the idea behind the [ÉTS master's research on wear in texture space]({{< ref "/posts/thesis-wear-texture-space/index.md" >}}): contact patches, tangential velocity and traction written into a texture where contact actually happened. The repository is published under [ETSim](https://github.com/ETSim) for graphics researchers who want to try those ideas without building a native simulator.

## Overview {#overview}

There are two parts.

**`docs/`, the modular application.** `docs/index.html` loads three.js 0.158 and Ammo.js from a CDN and starts `js/main-clean-complete.js`. A body (cube, soft volumetric cube, sphere, torus puck, cylinder puck, cone or custom GLB) is dropped on a plane with chosen gravity, friction, restitution, speed and force. Each frame:

- `js/contacts.js` samples contact points and their centre;
- `js/bounding-box/` fits the contact patch with AABB, PCA-based OBB, rotating-calipers OMBB, KDOP-8 or a hybrid method;
- `js/pip/` renders eight picture-in-picture views: top, bottom and intersection masks, tangential velocity, instant traction (τ = μ σ<sub>n</sub>), accumulated sliding distance, local sliding distance with direction vectors, and local wear;
- `js/managers/flow-accumulation-manager.js` accumulates wear as K × traction × velocity on the ground, keeps a time-smoothed sliding direction and encodes both as HSVA or RGBA;
- `js/managers/ground-variant-manager.js` loads a GLB ground with material variants and blends them with the wear map, rotating textures along the flow direction;
- `js/shaders/wear-map-shader.js` colours the sliding-distance map with optional logarithmic scaling.

**`experiments/`, single-file prototypes.** Nine standalone HTML pages named after their content: contact masks, dynamic paint with UV trails and OBB hulls, slip vector fields, multi-layer paint with GLB support, directional and hardness-based wear simulations, and GLB/flow-field blending. `docs/glb_khr_variants_blend.html` is a smaller test of blending glTF material variants with a grayscale map.

## Getting started {#installation}

The pages use ES modules, so they need a local web server. From the README in `docs/`:

```bash
cd docs
python -m http.server 8000
# open http://localhost:8000
```

Click **Start**, adjust the controls in the left panel and watch the PiP views. **Pause**, **Step Frame** and **Apply Angular Impulse** help follow one contact, and **Export Wear Map** or **Save Stamps** save the ground maps as PNG. The pages in `experiments/` open the same way. An internet connection is required for the CDN libraries.

## Repository guide {#reader-guide}

- `docs/index.html` is the main application page with its control panel.
- `docs/js/main-clean-complete.js` is the entry module. `docs/js/main.js` is an alternative entry module that `index.html` does not load.
- `docs/js/bodies/` creates the physics bodies, `docs/js/body-manager.js` handles their lifecycle.
- `docs/js/bounding-box/` holds the contact-patch fitting algorithms.
- `docs/js/pip/` holds the eight picture-in-picture renderers.
- `docs/js/managers/` holds the scene, physics, ground, stamping, field/flow, wear accumulation and GLB variant managers.
- `docs/js/shaders/wear-map-shader.js` is the GLSL wear-map shader.
- `experiments/` holds the standalone HTML prototypes.

## Features {#features}

- Rigid and soft bodies on Ammo.js physics, including custom GLB models.
- Five contact-patch fitting methods, with velocity-based OBB alignment.
- Live views of contact masks, tangential velocity, traction, sliding distance and wear.
- Persistent wear accumulation on the ground, cleared only on demand, with a time-smoothed sliding direction.
- GLB material-variant blending driven by accumulated wear.
- PNG export of stamps, wear and flow maps.

## Limits {#limits}

- These are research prototypes: the wear model is a visual heuristic in canvas buffers, not a calibrated tribology model.
- `docs/README.md` describes an older layout (`stamp/`, `field-flow/`, six PiP views) that no longer matches the files, and the top-level README is one sentence.
- Libraries are loaded from CDNs, including Ammo.js from a moving branch (`@HEAD` or `@main`) in several pages, so results can change without a code change.
- Most experiments use three.js 0.160 while the application uses 0.158.
- The README notes that the OBB angle can jitter at low speed and that custom GLB models should be convex.
- There are no tests or build step.

## Sources {#sources}

- [GitHub repository](https://github.com/ETSim/WearTrailsExperiments)
- [README](https://github.com/ETSim/WearTrailsExperiments/blob/main/README.md)
- [`docs/README.md`](https://github.com/ETSim/WearTrailsExperiments/blob/main/docs/README.md)
- [`docs/js/main-clean-complete.js`](https://github.com/ETSim/WearTrailsExperiments/blob/main/docs/js/main-clean-complete.js)
- [`docs/js/managers/flow-accumulation-manager.js`](https://github.com/ETSim/WearTrailsExperiments/blob/main/docs/js/managers/flow-accumulation-manager.js)
- [`docs/js/managers/ground-variant-manager.js`](https://github.com/ETSim/WearTrailsExperiments/blob/main/docs/js/managers/ground-variant-manager.js)
