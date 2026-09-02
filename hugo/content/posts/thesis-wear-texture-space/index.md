---
post_kind: article
title: "Master's thesis — contact–appearance coupling for wear in texture space"
date: 2026-08-14T14:00:00-04:00
lastmod: 2026-09-02T16:00:00-04:00
description: "ÉTS master's thesis on real-time surface wear in interactive simulation — frictional dissipation, GPU texture atlases, GelSight validation, WearPaper and TextureFriction."
translationKey: thesis-wear-texture-space
tags:
  - Thesis
  - ÉTS
  - Computer Graphics
  - Friction
  - Wear
  - GelSight
  - OpenGL
images:
  - images/wear-pipeline-flow.svg
---

**Couplage contact-apparence pour l'usure de surfaces microstructurées en simulation interactive** — my ÉTS master's thesis (English abstract title: *Visual Appearance Evolution from Wear on Microstructured Surfaces in Texture Space*). Directed by **Sheldon Andrews**, defended **14 August 2026**. The core idea: give material maps a **persistent local memory** of contact. Body travel alone cannot predict where wear shows up. **[Version française]({{< ref "/posts/thesis-wear-texture-space/index.fr.md" >}})**.

<!--more-->

## The gap

Real surfaces keep a trace of friction and slip. Interactive simulators usually throw that away at the end of each timestep. The contact solver already computes impulses, relative velocity, tangential traction, and dissipation — then updates rigid-body motion and stops. Material maps (albedo, roughness, normals) stay fixed unless an artist paints wear by hand.

The thesis closes that loop: mechanical contact resolution feeds **texture-space** appearance evolution at the places contact actually happened.

## Pipeline (one glance)

Sparse contacts are grouped into local patches, projected into material atlases, and reconstructed as tangential velocity, effective traction, and frictional dissipation on a GPU patch grid. Those fields drive accumulation of sliding distance, dominant direction, and wear — then progressive map updates **without global remeshing**.

![Wear pipeline — contact, velocity, traction, texture integration, atlas and GelSight validation](./images/wear-pipeline-flow.svg)

Source: [`wear-pipeline-flow.mmd`](./images/wear-pipeline-flow.mmd) (same chain as [GraphQuon 2025]({{< ref "/posts/graphquon-2025-university-of-toronto/index.md" >}})). The interactive implementation in **TextureFriction** adds a stricter runtime order: pre-solve FBO passes → PGS or AVBD solve → post-solve velocity/traction → sliding/wear/direction deposit → rendering.

![Real contact mask — from simulated contact to patch grid](./images/real-contact-mask.svg)

![Traction reconstruction on the patch (WLS) — local field before texture deposit](./images/traction-reconstruction-wls.svg)

## Three contributions

1. **Dissipation-based local accumulation** — links sliding, reconstructed traction, and visual surface evolution in texture space.
2. **Contact-to-atlas projection architecture** — patch clustering, GPU buffers, persistent material memory on a fixed mesh; sliding, direction, and wear written where overlap says contact occurred.
3. **GelSight acquisition and comparison** — controlled wear bench captures build the **Wear Surface Texture Datasets** and calibrate simulated patterns against measured microgeometry.

## Two codebases

| Repo | Role |
|------|------|
| [**WearPaper**](https://github.com/ETSim/WearPaper) | LaTeX thesis (`Thesis/main.tex` → `Thesis/build/main.pdf`), ACM article, Beamer defense slides; canonical manuscript and bibliography. |
| **TextureFriction** (local, `E:\master\TextureFriction`) | Qt6 + OpenGL 4.3+ simulator: PGS/AVBD contact, cluster FBO passes, GPU deposition into sliding/wear/direction atlases. Build: `just build`, run: `just run-build`. See `docs/architecture/14-thesis-pipeline-and-rationale.md` in the repo. |

WearPaper is the **paper trail**; TextureFriction is where the loop runs at interactive rates.

## Validation

Acquisitions on a reciprocal abrasion bench ([`banc-abrasion-reciproque`](./images/banc-abrasion-reciproque.pdf)) feed measured normal maps and staged wear progression. Public dataset: [ETSim/WearSurfacesDatasets](https://github.com/ETSim/WearSurfacesDatasets). Surface metrology tooling connects to my CV work on [**TrueMapData**](https://github.com/ETSim/TrueMapData) and **surfalize** integration.

## Results (snapshot)

In tested scenarios, **written texels** track cumulative wear more closely than body travel alone; contact topology changes the deposit pattern. A cube or torus on a plane stays within an **interactive budget**; cost rises sharply when several contact groups are processed together. The method is a physically motivated **appearance model**, not a full tribology simulator — limits remain around effective-field reconstruction, calibration, and UV parameterization.

## Full thesis PDF

The manuscript, article, and defense slides live in [**ETSim/WearPaper**](https://github.com/ETSim/WearPaper). CI builds the complete thesis to `Thesis/build/main.pdf` from `Thesis/main.tex`.

## Related

- [GraphQuon 2025 — Where to Wear?]({{< ref "/posts/graphquon-2025-university-of-toronto/index.md" >}}) — conference talk on the same research line
- [Software engineering journey]({{< ref "/posts/software-engineering-journey/index.md" >}}) — ÉTS master's thread (rendering, physics, wear)
- CV education line: *Thesis: real-time surface wear in interactive physics simulations, with dynamic friction and textures*
