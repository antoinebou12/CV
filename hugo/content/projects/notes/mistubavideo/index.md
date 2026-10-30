---
title: "MistubaVideo"
date: 2026-10-24T12:00:00-04:00
description: "MistubaVideo is an ETSim repository for video-related work with Mitsuba."
translationKey: repository-note-mistubavideo
repository_note: "MistubaVideo"
---

# MistubaVideo

MistubaVideo renders simulation exports with Mitsuba 3. The batch command processes OBJ sequences, while the `mitsuba-video` helper reads recorded body poses and surface fields through manifest and TextureFriction source adapters.

## Simulation to video

The helper applies poses, blends material appearances from the recorded field, and renders each frame. Optional heatmaps, a UV-atlas panel and a covered-area chart help inspect the surface changes. FFmpeg assembles the result into video.

Use `inspect` to check input data, `preview` to check the camera, and `render` to produce a sequence. `encode` can assemble existing frames again. The output records settings and timings in `render_config.json` and field-area measurements in CSV.

## Stack and tests

Python coordinates Mitsuba 3 and FFmpeg. The render-helper documentation describes pytest tests for transforms, material blending, OBJ/MTL readers and manifests. No measured coverage report is quoted here.

[Source and usage](https://github.com/ETSim/MistubaVideo) · [Render helper](https://github.com/ETSim/MistubaVideo/tree/main/packages/mitsuba_video)

[Read the project introduction]({{< ref "/posts/mistubavideo-rendered-video/index.md" >}}).
