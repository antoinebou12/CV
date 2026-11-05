# IPC Toolkit: collision and friction inside a simulation

> How IPC Toolkit supplies collision detection, distance derivatives and friction calculations to a simulation.

- HTML page: https://antoineboucher.info/CV/blog/posts/ipc-toolkit-contact-library/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/posts/ipc-toolkit-contact-library/index.md
- Published: 2026-10-24
- Updated: 2026-10-24
- Tags: C++, Simulation, Open Source
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)IPC Toolkit is a C++ library for contact calculations. It provides collision detection, distance derivatives and friction potentials. The application supplies the time-stepping loop and solver.

## Where it fits

A simulation passes collision geometry and vertex motion to the contact library. The diagram follows that query through broad-phase candidates and narrow-phase continuous collision detection (CCD), then back to the application.

![Contact query flow from an external simulation through broad-phase candidates and narrow-phase continuous collision detection to the result](https://antoineboucher.info/CV/blog/posts/ipc-toolkit-contact-library/images/architecture.png)

## What it computes

The routines cover several parts of contact handling:

| Area | Available calculations |
| --- | --- |
| Collision detection | Broad- and narrow-phase continuous collision detection. |
| Distance | Distance derivatives for edges and triangles. |
| Contact barriers | Barrier functions and derivatives, distance barrier potentials, and adaptive barrier stiffness. |
| Friction | Smooth or lagged dissipative friction potentials. |

IPC Toolkit is not a complete physics engine. The upstream project points to PolyFEM and Rigid IPC as complete simulation implementations that use the library.

## My contributions

The fork at [antoinebou12/ipc-toolkit](https://github.com/antoinebou12/ipc-toolkit) is where I stage changes before proposing them upstream. The pull requests below are the public record (GitHub, retrieved 2026-11-05); status is as GitHub reports it.

| Pull request | Opened | Status |
| --- | --- | --- |
| [ipc-sim/ipc-toolkit #210 — Anisotropic friction](https://github.com/ipc-sim/ipc-toolkit/pull/210) | 2026-02 | Merged 2026-04-16 |
| [ipc-sim/ipc-toolkit #208 — Option to pass parameters to the Scalable CCD narrow phase](https://github.com/ipc-sim/ipc-toolkit/pull/208) | 2026-01 | Merged 2026-01-26 |
| [ipc-sim/ipc-toolkit #144 — Draft adhesion documentation](https://github.com/ipc-sim/ipc-toolkit/pull/144) | 2024-11 | Merged 2024-12-11 |
| [ipc-sim/ipc-toolkit #139 — Static and kinetic coefficients in the tangential collision force](https://github.com/ipc-sim/ipc-toolkit/pull/139) | 2024-11 | Closed without merge |
| [ipc-sim/ipc-toolkit #128 — Pairwise kinetic and static friction for different materials](https://github.com/ipc-sim/ipc-toolkit/pull/128) | 2024-11 | Closed without merge |
| [Continuous-Collision-Detection/Scalable-CCD #5 — Remove `-fpic` for the Windows CUDA build (vcpkg)](https://github.com/Continuous-Collision-Detection/Scalable-CCD/pull/5) | 2024-09 | Merged 2024-09-27 |
| [Continuous-Collision-Detection/Scalable-CCD #6 — Multiple CUDA version tests](https://github.com/Continuous-Collision-Detection/Scalable-CCD/pull/6) | 2024-09 | Closed without merge |

Two staging pull requests remain open on the fork: [#3 — extract tolerance and max iterations from TightInclusionCCD for GPU CCD](https://github.com/antoinebou12/ipc-toolkit/pull/3) and [#4 — anisotropic friction](https://github.com/antoinebou12/ipc-toolkit/pull/4), the branch behind upstream #210.

The thread through these changes is friction that depends on direction and material pair, which is what my thesis work on surface wear needed from the contact model, plus the GPU continuous-collision-detection path (Scalable CCD) that the Windows build and the parameter pass-through unblocked.

## Read the code and build instructions

The [project documentation](https://antoineboucher.info/CV/blog/projects/notes/ipc-toolkit/) covers the repository structure. Use the [upstream README](https://github.com/ipc-sim/ipc-toolkit) for build instructions and the [contributor fork](https://github.com/antoinebou12/ipc-toolkit) for changes in that fork.
