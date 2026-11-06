# WearTrailsExperiments: contact-driven wear trails in the browser

> three.js and Ammo.js experiments that turn rigid-body contact, traction and sliding into wear, sliding-distance and flow maps on a ground texture.

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/weartrailsexperiments/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/weartrailsexperiments/index.md
- Published: 2026-11-05
- Updated: 2026-11-05
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/ETSim/WearTrailsExperiments
- Inspected revision: 065ad38507733d951f35359059dd7d33c809c5b6


## Use cases

Browser experiments that turn rigid-body contact and sliding into wear and flow maps on a ground texture.

- **Slide a body on the ground** (Graphics researcher, Web browser (WebGL), three.js/Ammo.js CDN): docs/index.html loads three.js 0.158 and Ammo.js from a CDN, then main-clean-complete.js drops a cube, sphere, puck, cone, soft cube or custom GLB on a plane with set speed, force and friction.
- **Compare contact bounding boxes** (Graphics researcher, Web browser (WebGL)): docs/js/bounding-box/ fits the contact patch with AABB, PCA-based OBB, rotating-calipers OMBB, KDOP-8 or a hybrid method.
- **Inspect contact field views** (Graphics researcher, Web browser (WebGL)): Eight picture-in-picture canvases show top, bottom and intersection views, tangential velocity, instant traction, accumulated sliding distance and local wear.
- **Accumulate wear on the ground** (Graphics researcher, Web browser (WebGL)): FlowAccumulationManager adds K x traction x velocity into ground buffers and keeps the sliding direction, encoded as HSVA or RGBA.
- **Blend GLB material variants** (Graphics researcher, Web browser (WebGL)): GroundVariantManager loads a GLB ground with material variants and uses accumulated wear as the blend map and flow direction to rotate textures.
- **Export wear maps as PNG** (Graphics researcher, Web browser (WebGL)): Export Wear Map and Save Stamps write the ground canvases to PNG files through a download link.

### Scenario: Record the wear trail of a sliding cube

1. Serve the docs/ folder with python -m http.server 8000 and open http://localhost:8000.
2. Choose Cube (subdiv 10), the OBB (PCA-based) algorithm and a friction value, then click Start.
3. Use Pause, Step Frame and Apply Angular Impulse to follow the contact patch in the PiP views.
4. Switch the wear encoding between HSVA (Direction + Wear) and RGBA to read direction and amount.
5. Click Export Wear Map to save the accumulated ground map as a PNG.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| HTML | 100 |


