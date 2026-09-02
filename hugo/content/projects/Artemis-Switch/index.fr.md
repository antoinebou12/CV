---
title: "Artemis-Switch"
date: 2026-09-02T12:00:00-04:00
description: "Streaming de jeux Apollo/Sunshine sur Nintendo Switch — fork de Moonlight-Switch avec surcouche et stats performance."
draft: false
---

# Artemis-Switch

[![Étoiles GitHub](https://img.shields.io/github/stars/antoinebou12/Artemis-Switch)](https://github.com/antoinebou12/Artemis-Switch/stargazers)
[![Dernier commit GitHub](https://img.shields.io/github/last-commit/antoinebou12/Artemis-Switch)](https://github.com/antoinebou12/Artemis-Switch)

[Dépôt](https://github.com/antoinebou12/Artemis-Switch) · [GPL-3.0](https://github.com/antoinebou12/Artemis-Switch/blob/main/LICENSE)

**Artemis-Switch** est mon fork maintenu de [XITRIX/Moonlight-Switch](https://github.com/XITRIX/Moonlight-Switch) pour hôtes **Apollo** (Sunshine) en homebrew **Nintendo Switch**. Stream d'un PC Windows ou Linux (Steam Big Picture, applications bureau) avec décode compatible Moonlight sur Switch, plus une surcouche pour raccourcis hôte et stats débit/latence.

Article : [Streaming portable et homebrew]({{< ref "/posts/handheld-streaming-homebrew/index.fr.md" >}}).

## Pile

- Homebrew C++ (lignée devkitA64 / libnx depuis Moonlight-Switch)
- Appairage Apollo / Sunshine
- Menus **Quick** et **Performance** pendant le stream

## Amont

Fork de [XITRIX/Moonlight-Switch](https://github.com/XITRIX/Moonlight-Switch). Entrée CV distincte : correctifs toolchain fusionnés sur Moonlight-Switch amont pour devkitPro récent.

## Démarrage

Voir le [README](https://github.com/antoinebou12/Artemis-Switch) pour prérequis de build, installation `.nro` et appairage avec un hôte Apollo sur le LAN.
