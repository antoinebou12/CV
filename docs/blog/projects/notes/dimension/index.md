# Dimension: From matrix storage to a rendered scene

> Dimension is my Rust workspace for mathematics and graphics experiments. mathlib provides numerical building blocks; render uses them for CPU-side…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/dimension/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/dimension/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)

- Repository: https://github.com/antoinebou12/Dimension
- License: MIT
- Inspected revision: 5281d0932aa99ea0d2c43e64c388b9256c75b126

## Summary

Dimension is my Rust workspace for mathematics and graphics experiments. mathlib provides numerical building blocks; render uses them for CPU-side transforms and cameras before submitting graphics work through wgpu.

**Why it exists:** High-performance wgpu graphics pipeline and linear algebra math engine built entirely in Rust from first principles.

**Best fit:** Hardware-accelerated 3D heightmap rendering, spatial transformation pipelines, and graphics education.

## Use cases

A Rust workspace around mathlib: linear algebra, wgpu rendering, parsers, physics and geometry, with WASM demos.

- **Compute with dense and sparse** (Rust developer): The mathlib crate provides dense and sparse matrices, vectors, SVD and 3D helpers; cd mathlib && cargo test and cargo bench exercise them.
- **Render a 3D scene with wgpu** (Rust developer, GPU via wgpu): The render crate draws a mathlib Tree scene through wgpu; cargo run -p render-demo --example render_native opens a window with a cube, gizmo and picking.
- **Load meshes and data files** (Rust developer): The parse crate reads JSON, XML, OBJ, MTL, BVH, glTF, PLY, PNG, JPEG, ZIP and TAR behind Cargo features such as json and obj.
- **Simulate physics, collisions** (Rust developer): physics implements PBD/XPBD with examples particles_2d, rigid_bodies_3d and softbody_3d; collision adds AABB, OBB, BVH, BSP, ray and frustum queries.
- **Publish the WASM demo site** (Rust developer, Browser (WASM/WebGPU)): just website-build compiles the mathlib, render, kinematics, physics, geometry and neural demos to WASM into website/; pages.yml deploys it to GitHub Pages.

### Scenario: Trying the demos locally before a push

1. Run cd mathlib && cargo test to check the core library.
2. Run just run-render to open the native wgpu scene and move the gizmo.
3. Run just website-build to compile every demo to WASM into website/.
4. Run just website-serve and open http://localhost:3000/ to browse /mathlib/, /render/ and /physics/.
5. Push to main; the Pages workflow rebuilds website/ and publishes it.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Rust | 63.95 |
| JavaScript | 31.84 |
| HTML | 2.57 |
| Just | 0.52 |
| CSS | 0.51 |
| WGSL | 0.4 |
| TypeScript | 0.13 |
| Python | 0.04 |
| Shell | 0.02 |
| Dockerfile | 0.01 |

## Getting started (repository commands, not run here)

### kinematics/README.md · Build, test, bench

```bash
cd kinematics
cargo build
cargo test
cargo bench
cargo run --example forward_kinematics
cargo run --example jacobian_ik
```

### mathlib/demo/README.md · Build and serve

```bash
just wasm-build      # or just wasm-build-gpu for GPU support
just wasm-serve
```

### mathlib/demo/wasm-demo/README.md · Build

```bash
wasm-pack build --target web --features wasm
```

### neural/README.md · Downloading ONNX models

```bash
cargo run -p neural --bin download_models -- --all
```

### neural/README.md · Precomputing embeddings for the WASM recommendation demo

```bash
cargo run -p neural --example precompute_demo_embeddings --features precompute -- mathlib/demo/wasm-demo/recommendation/data.json
```

### render/README.md · Build and run

```bash
cargo run -p render-demo --example render_native
```

### render/README.md · Build and run

```bash
just render-wasm         # build + serve; open http://localhost:3000/wasm-demo/
```

### website/README.md · Build and serve (local)

```bash
just website-build        # Build all WASM demos and populate website/
just website-build-gpu    # Same, but with GPU-enabled mathlib (WebGPU init, async matmul, etc.)
just website-build-simd   # Same as website-build, but render demo built with SIMD (can improve frame rate)
just website-serve        # Serve website/ (e.g. http://localhost:3000)
```


## Features and components

- **Data and numerical operations** — mathlib exports dense and sparse storage, matrix views, vectors and numerical methods. A caller chooses the representation that fits its problem. Optional executor features are separate from the basic storage API.
- **Scene and platform boundary** — render exports World, EntityId and Transform, with parent-child scene relationships. Native windowing and WebAssembly canvas support sit around the renderer. The root workspace also contains geometry, collision, kinematics and physics crates.

## Architecture

Components and connections verified in the repository.

- Application or demo → mathlib data and transforms
- mathlib data and transforms → Scene hierarchy and camera
- Scene hierarchy and camera → wgpu resources and passes
- wgpu resources and passes → Native window or web canvas

```mermaid
flowchart LR
  n0["Application or demo"]
  n1["mathlib data and transforms"]
  n2["Scene hierarchy and camera"]
  n3["wgpu resources and passes"]
  n4["Native window or web canvas"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
```

**One path through the code:** For a scene update, start with a local Transform and its parent relationship. Follow the scene representation toward the renderer rather than assuming a matrix calculation executes on the GPU. wgpu is the graphics backend; mathlib’s optional GPU executor is a different feature.

## Constraints and checks

Workspace membership shows available modules, not a completed physics engine or measured performance. Benchmarks need a specified workload, feature set and target device.

## Files to read

- [Cargo.toml](https://github.com/antoinebou12/Dimension/blob/main/Cargo.toml)
- [mathlib/src/lib.rs](https://github.com/antoinebou12/Dimension/blob/main/mathlib/src/lib.rs)
- [render/src/lib.rs](https://github.com/antoinebou12/Dimension/blob/main/render/src/lib.rs)


