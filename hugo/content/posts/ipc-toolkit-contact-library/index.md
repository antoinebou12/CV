---
project_docs: ipc-toolkit
story_kind: introduction
title: "IPC Toolkit: the contact library behind a simulation"
date: 2026-10-24T12:00:00-04:00
description: "IPC Toolkit provides reusable collision, CCD, distance and friction routines without owning the simulation loop."
translationKey: ipc-toolkit-contact-library
tags: [C++, Simulation, Open source]
post_kind: article
images: ["images/architecture.png"]
show_hero: false
---

The useful boundary in IPC Toolkit is clear: it provides contact routines, while the calling simulation owns time stepping and solving.

<!--more-->

The toolkit includes barrier functions and derivatives, adaptive barrier stiffness, broad- and narrow-phase continuous collision detection, distance derivatives for edges and triangles, distance barrier potentials, and smooth or lagged dissipative friction potentials.

That list also describes the limit. IPC Toolkit is not a complete physics engine and does not include a simulation loop or solver. The upstream project points to PolyFEM and Rigid IPC as full simulation implementations that use it.

My [project note]({{< ref "/projects/notes/ipc-toolkit/index.md" >}}) keeps the repository overview with the other project documentation. The [upstream README](https://github.com/ipc-sim/ipc-toolkit) and [contributor fork](https://github.com/antoinebou12/ipc-toolkit) are the references for build details and current changes.
