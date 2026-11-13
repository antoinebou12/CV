---
title: "Dimension (mathlib)"
date: 2026-04-13T12:00:00Z
description: "Rust monorepo centered on mathlib — linear algebra, sparse matrices, WASM, optional GPU."
draft: false
---

# Dimension

[![GitHub last commit](https://img.shields.io/github/last-commit/antoinebou12/Dimension)](https://github.com/antoinebou12/Dimension)

[Repository](https://github.com/antoinebou12/Dimension) · [mathlib on docs.rs](https://docs.rs/mathlib)

**mathlib** is a Rust crate for dense and sparse linear algebra, decompositions, 3D math, clustering, graph algorithms, transforms, and more—with **WebAssembly** demos and optional **SIMD** / **GPU** features. The Dimension repo wraps that crate alongside kinematics, physics, rendering experiments, and documentation.

## Live demos

{{< demos title="Dimension running in your browser" height="640" note="WebAssembly; the 3D demos need a browser with WebGPU." >}}
Render | https://antoinebou12.github.io/Dimension/render/ | A cube, a tetrahedron and a cylinder drawn by the wgpu renderer, with a transform gizmo and object picking.
Geometry | https://antoinebou12.github.io/Dimension/geometry/ | Mesh demos from the geometry crate.
Mathlib | https://antoinebou12.github.io/Dimension/mathlib/ | Linear algebra, graphs, optimization, noise, transforms and camera maths from mathlib.
{{< /demos >}}

The repository also publishes a [kinematics demo](https://antoinebou12.github.io/Dimension/kinematics/) (a three-joint arm solved with inverse kinematics) and a [physics demo](https://antoinebou12.github.io/Dimension/physics/) (rigid bodies with XPBD). Both need a browser with WebGPU and open in their own tab.

## Quick start

```bash
cd mathlib && cargo build
cd mathlib && cargo test
```

See the root [README](https://github.com/antoinebou12/Dimension#readme) and [docs/DOCS.md](https://github.com/antoinebou12/Dimension/blob/main/docs/DOCS.md) for architecture and examples.
