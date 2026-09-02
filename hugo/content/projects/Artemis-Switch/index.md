---
title: "Artemis-Switch"
date: 2026-09-02T12:00:00-04:00
description: "Apollo/Sunshine game streaming on Nintendo Switch — fork of Moonlight-Switch with in-app overlay and performance stats."
draft: false
---

# Artemis-Switch

[![GitHub stars](https://img.shields.io/github/stars/antoinebou12/Artemis-Switch)](https://github.com/antoinebou12/Artemis-Switch/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/antoinebou12/Artemis-Switch)](https://github.com/antoinebou12/Artemis-Switch)

[Repository](https://github.com/antoinebou12/Artemis-Switch) · [GPL-3.0](https://github.com/antoinebou12/Artemis-Switch/blob/main/LICENSE)

**Artemis-Switch** is my maintained fork of [XITRIX/Moonlight-Switch](https://github.com/XITRIX/Moonlight-Switch) for **Apollo** (Sunshine) hosts on **Nintendo Switch** homebrew. Stream a Windows or Linux PC (Steam Big Picture, desktop apps) with Moonlight-compatible decode on Switch, plus an overlay for host shortcuts and live bitrate/latency stats.

Blog write-up: [Handheld streaming and homebrew]({{< ref "/posts/handheld-streaming-homebrew/index.md" >}}).

## Stack

- C++ homebrew (devkitA64 / libnx lineage from Moonlight-Switch)
- Apollo / Sunshine pairing (Artemis host path)
- In-app **Quick** and **Performance** menus while streaming

## Upstream

Forked from [XITRIX/Moonlight-Switch](https://github.com/XITRIX/Moonlight-Switch). Separate CV entry: merged toolchain fixes on upstream Moonlight-Switch for newer devkitPro releases.

## Quick start

See the [README](https://github.com/antoinebou12/Artemis-Switch) for build prerequisites, `.nro` install, and pairing with an Apollo host on your LAN.
