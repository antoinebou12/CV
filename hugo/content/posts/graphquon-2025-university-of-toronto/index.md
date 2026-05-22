---
post_kind: conference
title: "GraphQuon 2025 — University of Toronto"
date: 2025-11-15T10:00:00-05:00
lastmod: 2026-05-22T23:30:00-05:00
description: "Presented Where to Wear? at the Quebec–Ontario pre-SIGGRAPH workshop in Toronto—frictional wear, texture updates, and slides from GraphQuon 2025."
translationKey: graphquon-2025-university-of-toronto
tags:
  - Conference
  - GraphQuon
  - University of Toronto
  - SIGGRAPH
  - Computer Graphics
  - Friction
  - ÉTS
canonicalURL: "https://www.dgp.toronto.edu/graphquon/"
images:
  - featured.png
---

![GraphQuon 2025 name badge — Antoine Boucher, École de technologie supérieure, Toronto skyline](./images/graphquon-name-badge.png)

**GraphQuon** is the annual Quebec–Ontario pre-SIGGRAPH workshop. The **2025** edition ran **15–16 November 2025** at the **University of Toronto** ([series page](https://www.dgp.toronto.edu/graphquon/)). I **presented** there with **Sheldon Andrews** (ÉTS): **Where to Wear?** — how frictional contact leaves a readable history on surfaces, and how we can turn that into graphics and engineering feedback. **[Version française]({{< ref "/posts/graphquon-2025-university-of-toronto/index.fr.md" >}})**.

<!--more-->

## What I presented

Talk title: **Where to Wear?** (subtitle on the opening slide: *Every surface has a biography written by frictional contact*).

The story is simple to state and hard to simulate: **time**, **contact**, and **energy dissipation** change how a surface looks and behaves—from bathroom tile wear patterns at an engineering school to scratches on tools, gaming materials, and robotics grippers. The deck walks from motivation through mechanics (Archard wear, energy-based wear laws), a **graphics-oriented pipeline** (contact mask, orthographic volumes, tangential velocity and traction, texture integration), and validation ideas (**GelSight** capture, materials atlas interpolation).

![Opening slide — Where to Wear? Antoine Boucher and Sheldon Andrews, ÉTS](./images/slide-01.png)

### Pipeline (one glance)

Rendered with [uml-mcp](https://github.com/antoinebou12/uml-mcp) from [`wear-pipeline-flow.mmd`](./images/wear-pipeline-flow.mmd):

![Wear simulation pipeline — contact, velocity, traction, texture integration, atlas](./images/wear-pipeline-flow.svg)

![Pipeline slide from the deck — inputs from contact through texture wear](./images/slide-15.png)

![Example slide from the deck](./images/slide-22.png)

### Why it fit GraphQuon

GraphQuon is where **Quebec and Ontario graphics labs** share work before SIGGRAPH season—short talks, posters, and honest feedback from people who build simulators and renderers. After helping with the **[GraphQuon 2024]({{< ref "/posts/graphquon-2024-ets" >}})** site at ÉTS, presenting in Toronto in 2025 felt like the same community on the other side of the drive.

The research line connects to my **ÉTS** work on **3D fabrication and validation of frictional surfaces** ([project description](https://www.etsmtl.ca/recherche/etudes-superieures-et-recherche/projets-de-recherche-pour-etudiants/3d-fabrication-and-validation-of-frictional-su-1)).

## Slides and downloads

| Format | File | Notes |
|--------|------|--------|
| **PDF** | [graphquon-2025-where-to-wear.pdf](./graphquon-2025-where-to-wear.pdf) | Full deck export (28 slides). Best for reading and sharing. |
| **PowerPoint** | `GraphQuon Final.pptx` | Original editable deck (~116 MB with embedded assets—too large to host in this repo). Use the PDF above, or [email me](mailto:antoine@antoineboucher.info) if you need the `.pptx`. |

## Toronto, November 2025

A few photos from the trip—badge, campus-adjacent architecture, and the usual downtown walks between sessions.

![Downtown Toronto at night — CN Tower and Bell Media building](./images/toronto-cn-tower-night.png)

![OCAD Sharp Centre for Design at night — table-top building on coloured stilts](./images/ocad-sharp-centre-night.png)

![Yonge–Dundas Square at night — digital billboards and wet pavement](./images/yonge-dundas-square-night.png)

![Toronto music-history mural — Yonge Street area](./images/toronto-music-mural.png)

![Informal gathering with other attendees](./images/graphquon-social-gathering.png)

![Ontario waterfront — houses linked by a footbridge at dusk](./images/ontario-waterfront-bridge.png)

## Links

- [GraphQuon 2025 — DGP, University of Toronto](https://www.dgp.toronto.edu/graphquon/)
- [GraphQuon 2024 at ÉTS (Montréal)]({{< ref "/posts/graphquon-2024-ets" >}}) · [graphquon.github.io](https://graphquon.github.io/)
- [ÉTS — frictional surfaces research project](https://www.etsmtl.ca/recherche/etudes-superieures-et-recherche/projets-de-recherche-pour-etudiants/3d-fabrication-and-validation-of-frictional-su-1)
