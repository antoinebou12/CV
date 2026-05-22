---
title: "MediaBoxDockerCompose"
linkTitle: "MediaBoxDockerCompose"
date: 2024-01-01T12:00:00Z
description: "Docker Compose homelab stack—downloads, *Arr automation, Plex/Jellyfin, VPN, Samba, and ops dashboards—with paths driven from the repo."
draft: false
tags:
    - Docker
    - Docker Compose
    - Homelab
    - Plex
    - Sonarr
    - Radarr
---

[![GitHub last commit](https://img.shields.io/github/last-commit/antoinebou12/MediaBoxDockerCompose)](https://github.com/antoinebou12/MediaBoxDockerCompose)

[Repository](https://github.com/antoinebou12/MediaBoxDockerCompose) · [MIT License](https://github.com/antoinebou12/MediaBoxDockerCompose/blob/master/LICENSE)

Compose-first homelab media stack: fetch content (torrents and Usenet), route it through *Arr apps, add subtitles where needed, then serve libraries with **Plex** or **Jellyfin**, with request UIs and monitoring. Configuration is meant to live under a shared `ROOT` tree on disk as in the repo’s `docker-compose.yml`.

**Blog:** port catalog for 86 tracked services (implemented vs spreadsheet-only) plus [Proxmox VE Helper-Scripts](https://github.com/community-scripts/ProxmoxVE) — [MediaBox homelab Docker catalog]({{< ref "/posts/mediabox-homelab-docker-catalog/index.md" >}}).

For hosts that are not ready for the full stack yet, the companion [**another-install-script**](https://github.com/antoinebou12/another-install-script) repo offers menu-driven bash installers to pull up individual containers (and related dashboards) on a fresh Linux machine before you adopt this compose file.

## What’s in the stack

Grouped by role (see the [compose file](https://github.com/antoinebou12/MediaBoxDockerCompose/blob/master/docker-compose.yml) for images, ports, and volumes):

- **Download clients & indexers** — Deluge, NZBGet, Jackett, NZBHydra2, Prowlarr  
- **Automation** — Sonarr, Radarr, Lidarr, Bazarr, CouchPotato; Readarr (books); Whisparr; Tdarr (transcoding)  
- **Libraries & requests** — Plex, Jellyfin, Ombi, Jellyseerr, Tautulli  
- **Network & files** — WireGuard (VPN), Samba shares  
- **Extras** — Stash (specialized library organizer)  
- **Ops** — Netdata, Dashmachine, Filebrowser  

## Quick start

1. Install [Docker](https://docs.docker.com/get-docker/) and Compose on the host.  
2. Clone the repo and configure environment variables (see the repo `.env` and paths like `ROOT`).  
3. From the project directory:

```bash
git clone https://github.com/antoinebou12/MediaBoxDockerCompose.git
cd MediaBoxDockerCompose
docker compose up -d
```

If your setup still uses the older CLI, `docker-compose up -d` matches what the [README](https://github.com/antoinebou12/MediaBoxDockerCompose#readme) describes.

## Documentation

Default **ports**, **credentials**, **backup/restore** notes, and **contributing** are maintained in the [README](https://github.com/antoinebou12/MediaBoxDockerCompose#readme) so this page stays a short overview rather than a second copy of the manual.
