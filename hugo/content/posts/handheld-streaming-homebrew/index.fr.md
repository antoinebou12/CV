---
post_kind: article
title: "Streaming portable et homebrew — Artemis-Switch, moonlight-N3DS, sm64coopdx-switch"
date: 2026-09-02T12:00:00-04:00
lastmod: 2026-09-02T12:00:00-04:00
description: "Streaming PC sur Nintendo Switch avec Artemis (Apollo/Sunshine), Moonlight sur New 3DS, et un port Switch de sm64coopdx — trois dépôts homebrew et leur rôle."
translationKey: handheld-streaming-homebrew
tags:
  - Nintendo Switch
  - Nintendo 3DS
  - Moonlight
  - Homebrew
  - C++
images:
  - artemis-performance.png
---

Trois dépôts que je maintiens à côté : **[Artemis-Switch](https://github.com/antoinebou12/Artemis-Switch)** pour le streaming Apollo/Sunshine sur Switch, **[moonlight-N3DS](https://github.com/antoinebou12/moonlight-N3DS)** pour GameStream sur New 3DS, et **[sm64coopdx-switch](https://github.com/antoinebou12/sm64coopdx-switch)** comme build Switch du Mario 64 coopératif. Même motivation — faire tourner quelque chose d'intéressant sur du matériel qui n'était pas prévu pour — mais piles et contraintes différentes. **[English version]({{< ref "/posts/handheld-streaming-homebrew/index.md" >}})**.

<!--more-->

## Artemis-Switch — streaming PC sur Switch

[Artemis-Switch](https://github.com/antoinebou12/Artemis-Switch) est mon fork de [XITRIX/Moonlight-Switch](https://github.com/XITRIX/Moonlight-Switch), orienté hôtes **Apollo** (Sunshine) plutôt que l'ancien GameStream NVIDIA. Je stream Steam Big Picture depuis mon bureau (`AntoinePC`) et j'utilise la surcouche in-app pour les raccourcis hôte et le panneau performance.

![Menu rapide Artemis — raccourcis hôte et presets clavier pendant le stream Steam Big Picture](./images/artemis-quick-menu.png)

L'onglet **Quick** expose les raccourcis fenêtre (`Win+Shift+Left` / `Right`), les presets clavier et les scripts Apollo sans quitter le stream — pratique quand l'hôte est Windows et la Switch ne sert que d'écran.

![Surcouche performance Artemis — débit, Wi-Fi, latences receive/decode/render](./images/artemis-performance.png)

**Performance** affiche le débit (~12 Mbps sur cette capture), les barres Wi-Fi Switch, et les temps receive / decode / render. Le render est souvent le goulot sur Switch ; receive et decode sous la milliseconde indiquent un réseau et un décodeur sains, le budget frame étant surtout la composition.

Dépôt : **[github.com/antoinebou12/Artemis-Switch](https://github.com/antoinebou12/Artemis-Switch)** (★ 12). Le travail amont Moonlight-Switch apparaît aussi sur mon CV : [correctifs toolchain fusionnés](https://github.com/XITRIX/Moonlight-Switch) pour devkitPro récent — distinct du fork Artemis, même lignée Moonlight.

## moonlight-N3DS — GameStream sur New 3DS

[moonlight-N3DS](https://github.com/antoinebou12/moonlight-N3DS) suit [zoeyjodon/moonlight-N3DS](https://github.com/zoeyjodon/moonlight-N3DS), client GameStream pour **New 3DS**. Mon fork sert aux essais de build et d'intégration ; les étoiles sur **mon** dépôt restent faibles — l'intérêt communautaire est en amont (~300★), là où chercher installs et issues.

Contraintes sévères : écran 400×240, décode logiciel, Wi-Fi d'une portable 2015. Bitrate et latence inférieurs à la Switch ; le gain est d'avoir une voie Moonlight sur 3DS.

Dépôt : **[github.com/antoinebou12/moonlight-N3DS](https://github.com/antoinebou12/moonlight-N3DS)**.

## sm64coopdx-switch — Mario 64 coop sur Switch

[sm64coopdx-switch](https://github.com/antoinebou12/sm64coopdx-switch) porte [coop-deluxe/sm64coopdx](https://github.com/coop-deluxe/sm64coopdx) en homebrew Switch. sm64coopdx prolonge sm64ex-coop : co-op en ligne, mods Lua, QoL accumulée par la scène decomp.

**Note légale :** comme tout port SM64, il faut fournir sa propre **ROM obtenue légalement**. Le dépôt build le port ; il ne distribue pas les assets du jeu.

Dépôt : **[github.com/antoinebou12/sm64coopdx-switch](https://github.com/antoinebou12/sm64coopdx-switch)**.

## Vue d'ensemble

| Projet | Plateforme | Amont | Rôle |
|--------|------------|-------|------|
| Artemis-Switch | Switch | XITRIX/Moonlight-Switch | Streaming Apollo/Sunshine + UX overlay |
| moonlight-N3DS | New 3DS | zoeyjodon/moonlight-N3DS | Expérimentations client GameStream |
| sm64coopdx-switch | Switch | coop-deluxe/sm64coopdx | Port homebrew du SM64 coop |

Pages projet : [Artemis-Switch]({{< ref "/projects/Artemis-Switch" >}}), [moonlight-N3DS]({{< ref "/projects/moonlight-N3DS" >}}), [sm64coopdx-switch]({{< ref "/projects/sm64coopdx-switch" >}}).

## Voir aussi

- Diagrammes pour la doc : **[uml-mcp]({{< ref "/posts/uml-mcp/index.md" >}})** et la [page projet uml-mcp]({{< ref "/projects/uml-mcp" >}}).
