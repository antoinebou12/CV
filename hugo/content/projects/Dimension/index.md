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

## Quick start

```bash
cd mathlib && cargo build
cd mathlib && cargo test
```

See the root [README](https://github.com/antoinebou12/Dimension#readme) and [docs/DOCS.md](https://github.com/antoinebou12/Dimension/blob/main/docs/DOCS.md) for architecture and examples.

**Blog:** [Dimension — a Rust math stack around mathlib]({{< ref "/posts/dimension-mathlib-rust" >}})
