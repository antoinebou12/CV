---
title: "WearBlender: Blender scenes for wear effects"
date: 2026-11-05T12:00:00-05:00
description: "Example Blender files showing edge wear, scratches, rotated normal maps, flow maps and painted wear with shaders and geometry nodes."
translationKey: repository-note-wearblender
repository_note: "WearBlender"
---

# WearBlender

<div class="repo-status-row"><span class="repo-badge kind">Blender scenes</span></div>

<div class="repo-tech-badges"><span class="tag tool">Blender</span><span class="tag tool">Shader nodes</span><span class="tag tool">Geometry nodes</span></div>

WearBlender is a set of Blender scenes, published under [ETSim](https://github.com/ETSim), for learning and teaching how artists usually fake wear: worn edges, scratches, rotated normal maps, painted marks and proximity effects. It sits beside the [ÉTS master's research on wear in texture space]({{< ref "/posts/thesis-wear-texture-space/index.md" >}}), where wear comes from simulated contact rather than hand-built masks.

## Overview {#overview}

The repository holds only `.blend` files, a README and an MIT licence. The README lists five themes. The node types stored in each file show how the scenes cover them:

- `Edge wear.blend`: a worn-edge mask from **Bevel** and **Geometry** nodes, a color ramp and a roughness image texture on a plane.
- `Scratched.blend`: procedural micro-scratches on a Suzanne mesh from **Voronoi** and **Noise** textures, color ramps and **Bump** nodes.
- `NormalRotation.blend`: an image normal map whose vectors are turned with **Vector Rotate** and **Vector Math** nodes.
- `WeightPainting.blend`: geometry-node trees that read a painted attribute with **Named Attribute**, and a material that mixes shaders through an **Attribute** node.
- `flowmap.blend`: vector nodes that split and recombine coordinates to push a texture along a flow image.
- `SurfaceCameraProjection.blend`: a second camera, a `CameraProjectionMaterial` with an emission shader and a rigid-body world.

Three more scenes, `Sliding_cube.blend`, `Wrapping project.blend` and `flowmap_vector field.blend`, are larger files. Their names suggest a sliding-cube setup, a wrapping test and a vector-field flowmap variant. The README does not describe them separately.

## Getting started {#installation}

Nothing needs to be built. Clone the repository and open any file in Blender; the README says the scenes were tested in Blender 4.5 LTS.

```bash
git clone https://github.com/ETSim/WearBlender
blender "WearBlender/Edge wear.blend"
```

Then, as the README suggests, look at the Shader Editor or Geometry Nodes editor, toggle visibility or play the animation, and reuse the node setups in your own materials.

## Repository guide {#reader-guide}

- `Edge wear.blend` covers curvature and bevel-based edge wear.
- `Scratched.blend` covers procedural scratches with bump.
- `NormalRotation.blend` covers rotating normal maps in a shader.
- `WeightPainting.blend` covers wear driven by painted attributes and geometry nodes.
- `flowmap.blend` and `flowmap_vector field.blend` cover texture flow maps.
- `SurfaceCameraProjection.blend` covers projecting a camera texture onto a surface.
- `Sliding_cube.blend` and `Wrapping project.blend` are additional scenes named after a sliding cube and a wrapping project.
- `README.md` lists the themes and how to use the files.

## Features {#features}

- Edge wear from curvature, bevel and color ramps.
- Procedural scratches from Voronoi and noise textures.
- Rotated normal maps for dynamic surface detail.
- Wear driven by painted attributes and geometry nodes.
- Flow-map texture offsets.
- Camera texture projection onto a surface.

## Limits {#limits}

- The repository contains scenes only: no scripts, add-on or rendered previews.
- The README describes five themes but does not map them to file names, and it mentions a dynamic-paint scene without naming the file.
- The scenes reproduce artist-driven wear looks. They are not physical wear models.
- The files were saved by Blender 4.4 and 4.5, so older Blender versions may not open them.

## Sources {#sources}

- [GitHub repository](https://github.com/ETSim/WearBlender)
- [README](https://github.com/ETSim/WearBlender/blob/main/README.md)
- [`Edge wear.blend`](https://github.com/ETSim/WearBlender/blob/main/Edge%20wear.blend)
- [`Scratched.blend`](https://github.com/ETSim/WearBlender/blob/main/Scratched.blend)
- [`WeightPainting.blend`](https://github.com/ETSim/WearBlender/blob/main/WeightPainting.blend)
