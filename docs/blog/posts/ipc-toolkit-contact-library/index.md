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

## Read the code and build instructions

The [project documentation](https://antoineboucher.info/CV/blog/projects/notes/ipc-toolkit/) covers the repository structure. Use the [upstream README](https://github.com/ipc-sim/ipc-toolkit) for build instructions and the [contributor fork](https://github.com/antoinebou12/ipc-toolkit) for changes in that fork.
