---
post_kind: article
title: "Dimension — a Rust math stack around mathlib"
date: 2026-04-13T10:00:00-04:00
description: Notes on the Dimension monorepo and its mathlib crate — linear algebra, sparse matrices, WASM demos, and optional GPU paths.
translationKey: dimension-mathlib-rust
tags:
    - Rust
    - Linear Algebra
    - WebAssembly
    - Scientific Computing
    - Open Source
---

## What it is

[Dimension](https://github.com/antoinebou12/Dimension) is a monorepo I use to experiment with numerical code in Rust. The piece that holds most of the public API is **mathlib**: a linear-algebra-focused crate with dense and sparse matrices, vectors, standard decompositions (SVD, Cholesky, LU, PCA), solvers, and a large set of building blocks for graphics-style math (3D types, quaternions, dual quaternions, cameras, easing, curves).

The repo also pulls in related crates for simulation and tooling—kinematics, physics, geometry, rendering demos, neural bits, and a small site that packages some of the WASM demos—so mathlib stays the shared numeric core while other folders explore how that core feels in real programs.

## Why Rust here

Rust gives a single codebase that can target native binaries, tests, and benchmarks, then compile the same numerics to **WebAssembly** for an interactive demo layer. mathlib is organized by domain (linear, structure, ML-style clustering and distances, graphs and pathfinding, transforms, noise, and so on), which keeps features discoverable as the crate grows.

Optional **SIMD** and **WebGPU/wgpu** paths exist for heavier workloads; the design doc in the repo spells out when iterative sparse solvers (for example conjugate gradient on CRS matrices) are preferable to turning a sparse problem into a dense factorization.

## Try it

From the repo, the usual loop is:

```bash
cd mathlib && cargo build
cd mathlib && cargo test
```

Published API reference: [docs.rs/mathlib](https://docs.rs/mathlib). For architecture, type tables, and usage notes, the repo’s `docs/DOCS.md` is the long-form map.

## Closing

Dimension is as much a workspace for learning and benchmarking as it is a library. If you care about Rust numerics, WASM demos, or GPU-backed primitives, the repository is the place to watch; pull requests and issues are welcome on [GitHub](https://github.com/antoinebou12/Dimension).
