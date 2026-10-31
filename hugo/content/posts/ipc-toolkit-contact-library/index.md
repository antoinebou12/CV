---
project_docs: ipc-toolkit
story_kind: introduction
title: "IPC Toolkit: collision and friction inside a simulation"
date: 2026-10-24T12:00:00-04:00
description: "How IPC Toolkit supplies collision detection, distance derivatives and friction calculations to a simulation."
translationKey: ipc-toolkit-contact-library
tags: [C++, Simulation, Open source]
post_kind: article
images: ["images/architecture.png"]
show_hero: false
---

IPC Toolkit is a C++ library for contact calculations. It provides collision detection, distance derivatives and friction potentials. The application supplies the time-stepping loop and solver.

<!--more-->

## Where it fits

A simulation passes collision geometry and vertex motion to the contact library. The diagram follows that query through broad-phase candidates and narrow-phase continuous collision detection (CCD), then back to the application.

{{< figure src="images/architecture.png" alt="Contact query flow from an external simulation through broad-phase candidates and narrow-phase continuous collision detection to the result" caption="A contact query starts and ends in the calling simulation. Time stepping and solving remain the application’s responsibility." class="article-diagram-figure" >}}

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

The [project documentation]({{< ref "/projects/notes/ipc-toolkit/index.md" >}}) covers the repository structure. Use the [upstream README](https://github.com/ipc-sim/ipc-toolkit) for build instructions and the [contributor fork](https://github.com/antoinebou12/ipc-toolkit) for changes in that fork.
