---
post_kind: article
title: "MediaBox homelab — what I run in Docker (and what stayed a bookmark)"
date: 2024-03-15T10:00:00-04:00
lastmod: 2026-05-22T22:00:00-04:00
description: "How MediaBoxDockerCompose grew out of a homelab port map — what I actually wired up, and where Proxmox helper-scripts fit."
translationKey: mediabox-homelab-docker-catalog
tags:
  - Homelab
  - Docker
  - Docker Compose
  - Proxmox
  - Self-Hosted
  - MediaBoxDockerCompose
images:
  - featured.jpeg
---

I kept a private list of self-hosted apps I wanted to try — mostly so I would stop assigning random ports and forgetting what lived on `:8096`. That list turned into **[MediaBoxDockerCompose](https://github.com/antoinebou12/MediaBoxDockerCompose)** on GitHub. This post is the short version: what I wired up, how I install on Proxmox when compose is not the right shape, and where the full port map lives so this page does not become a spreadsheet with SEO. **[Version française]({{< ref "/posts/mediabox-homelab-docker-catalog/index.fr.md" >}})**.

<!--more-->

![Homelab wall stack — switch, modem, router, server, UPS](./images/featured.jpeg)

Same chapter as **[networking evolution]({{< ref "/posts/home-networking-evolution/index.md" >}})** — cables on the wall, then services in git. The photo is from when I was still labeling ports with tape; the compose file is what survived.

## What MediaBox is

One `docker-compose.yml`, shared `ROOT` paths on disk, and opinions I earned from breaking things locally. I use it when I want **one host, many containers, shared volumes** — Jellyfin next to Deluge next to FreshRSS without spinning up a new LXC per hobby.

The repo README has **default ports, credentials, backup notes**, and the install path I actually follow. Treat this post as context; treat the [README](https://github.com/antoinebou12/MediaBoxDockerCompose#readme) as the manual.

## What I wired up (by job, not by checkbox)

These are the services that made it into compose long enough to matter. Ports are how I reached them on the LAN (`:800x` families on purpose — easier behind Caddy).

### Media and files

| Service | Port | Why I kept it |
|---------|------|----------------|
| [Jellyfin](https://jellyfin.org/) | :8096 | Library playback without Plex account drama |
| [Airsonic](https://github.com/linuxserver/docker-airsonic) | :4040 | Music and podcasts in one place |
| [Deluge](https://github.com/deluge-torrent/deluge) | :8112 | Torrent client I could automate around |
| [Cloud torrent](https://github.com/jpillora/cloud-torrent) | :6889 | Remote queue when I was away from the box |
| [Mylar](https://hub.docker.com/r/linuxserver/mylar) | :8090 | Comics without manual hunting |
| [Piwigo](https://hub.docker.com/r/linuxserver/piwigo/) | :8049 | Photo gallery for family stuff |
| [Lychee](https://github.com/electerious/Lychee) | :8035 | Lighter photo sharing experiments |

I still bookmark **Plex, Sonarr, Radarr, *arr-adjacent tools** — same homelab aisle, not in my compose file today. When I want them on Proxmox I use helper-scripts (below) instead of hand-writing another stack.

### Dashboards, remote access, ops

| Service | Port | Why I kept it |
|---------|------|----------------|
| [Dashmachine](https://github.com/rmountjoy92/DashMachine) | :5000 | One page of links when I forgot URLs |
| [Netdata](https://github.com/netdata/netdata) | :19999 | “Is the disk full again?” at a glance |
| [Guacamole](https://github.com/oznu/docker-guacamole) | :8012 | Browser RDP/VNC without installing clients |
| [KDE in Docker](https://github.com/ms-jpq/kde-in-docker) | :8100 | Full desktop in a tab (debugging habit) |
| [Ubuntu XRDP](https://github.com/danielguerra69/ubuntu-xrdp) | :3389 | Pairs with Guacamole for a real desktop session |
| [TeamSpeak](https://github.com/solidnerd/docker-teamspeak) | — | Voice with friends during lockdown-era gaming |
| [Linkd](https://github.com/HexF/linkd) | — | Short links on my domain |

### Notes, RSS, money, diagrams

| Service | Port | Why I kept it |
|---------|------|----------------|
| [BookStack](https://www.bookstackapp.com/) | :6875 | Homelab docs that are not random Markdown files |
| [Wallabag](https://github.com/wallabag/wallabag) | :8899 | Read-it-later without a subscription |
| [FreshRSS](https://hub.docker.com/r/linuxserver/freshrss) | :8007 | Feeds in one place |
| [DailyNotes](https://github.com/m0ngr31/DailyNotes) | :5001 | Daily log when I actually used it |
| [Firefly III](https://www.firefly-iii.org/) | :8006 | Personal finance tracking (repo sync still catching up) |
| [Grocy](https://github.com/linuxserver/docker-grocy) | :9283 | Pantry ERP — more fun than useful, still educational |
| [draw.io](https://hub.docker.com/r/fjudith/draw.io) | :8005 | Diagrams without leaving the network |
| [Gitea](https://gitea.io/) | :8008 | Git for experiments before pushing to GitHub |
| [Calibre](https://github.com/kovidgoyal/calibre) | :8001, :8002 | E-books |
| [Huginn](https://github.com/huginn/huginn) | :8013 | “If this then that” I host myself |

### Oddballs I still like

| Service | Port | Note |
|---------|------|------|
| [Neko](https://github.com/nurdism/neko) | :8032 | Shared browser room — rabbit-hole energy |
| [Deezloader Remix](https://notabug.org/RemixDevs/DeezloaderRemix) | :1730 | Legacy stack; kept for history more than daily use |
| [OpenTogetherTube](https://github.com/antoinebou13/opentogethertube/tree/docker) | :6666 | My fork — watch party experiments |

## Proxmox when compose is the wrong tool

On **[Proxmox]({{< ref "/posts/home-networking-evolution/index.md" >}})** I often use **[Proxmox VE Helper-Scripts](https://github.com/community-scripts/ProxmoxVE)** — community-maintained one-liners (built on [tteck](https://github.com/tteck)'s work). Search on **[community-scripts.org](https://community-scripts.org/)**, paste into the Proxmox shell, pick default or advanced, get an LXC plus a post-install menu for updates.

Same names as my old wish list — Jellyfin, Vaultwarden, AdGuard, Home Assistant — different packaging. I have run **compose on one VM** and **separate CTs from helper-scripts** on the same rack depending on whether I wanted shared volumes or hard isolation.

## Host tools (not in compose)

**Ansible**, **Cockpit** (:9090), **Dokku**, and **Lynk** install on the host when the job is “manage the metal” or “expose a TCP service safely,” not “run another container row.”

## The long wish list

The original tracking sheet had **86 Docker names** and dozens more I never wired up — Nextcloud, Vaultwarden, mail stacks, game servers, the full *Arr parade. I am not pasting that grid here; it ages badly and reads like a status dashboard.

If you want the exhaustive map, open the [MediaBoxDockerCompose](https://github.com/antoinebou12/MediaBoxDockerCompose) repo and issues, or browse [community-scripts.org/categories](https://community-scripts.org/) for the Proxmox side. For one container on a fresh Linux box before full compose, I used **[another-install-script](https://github.com/antoinebou12/another-install-script)** — menu-driven bash, same era as the homelab.

## What stuck with me

- **Plan ports in families** — `:800x` saved my firewall rules and my sanity.
- **Running something once ≠ operating it** — LAN-only experiments are still valuable.
- **Forks are where ideas go** — [OpenTogetherTube](https://github.com/antoinebou13/opentogethertube/tree/docker), [wireguardweb](https://github.com/antoinebou13/wg-access-server/tree/update).
- **Pick compose or Proxmox scripts for the shape of the problem**, not because a blog post said one is cooler.

## Related posts

- [Networking evolution — home lab]({{< ref "/posts/home-networking-evolution/index.md" >}}) — physical network, Proxmox, Caddy/WireGuard
- [Renpho + Home Assistant]({{< ref "/posts/renpho-health-api-blueprint/index.md" >}}) — another “own your data at home” project
- [Caddy on AWS]({{< ref "/posts/caddy-ec2-cloudwatch-lambda/index.md" >}}) — when the reverse proxy leaves the basement
