---
title: "TrueMapData: from measured height maps to usable assets"
date: 2026-10-24T12:00:00-04:00
description: "TrueMapData connects TrueMap and GelSight files to visualisation, surface metrics, wear analysis and mesh export."
translationKey: truemapdata-height-maps
tags: [Python, Metrology, Graphics]
post_kind: article
---

TrueMapData starts with a measured height map and keeps the path to a useful output visible. **[Version française]({{< ref "/posts/truemapdata-height-maps/index.fr.md" >}})**.

<!--more-->

The project reads TrueMap v6-style and legacy files, plus GelSight-compatible layouts. Its `tmd-process` CLI and Python package cover filters, transforms, normal and displacement maps, defect detection, sequence export, compression and mesh formats.

The same repository reaches into surface analysis. Optional Surfalize support covers ISO 25178 roughness, while tribology and wear commands work with aligned captures, contact-style curves, wear volume series, scratches and debris-oriented maps. Mesh export can apply height-derived textures to a template using capture metadata.

That combination is useful across two neighbouring workflows: measured surfaces can feed metrology questions, or become visual assets for a graphics pipeline. The [TrueMapData project note]({{< ref "/projects/notes/truemapdata/index.md" >}}) links the repository and documentation.

- [TrueMapData repository](https://github.com/ETSim/TrueMapData)
- [Documentation](https://etsim.github.io/TrueMapData/)
