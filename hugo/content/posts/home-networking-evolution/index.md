---
post_kind: article
title: "Networking evolution — building a home network lab"
date: 2021-09-06T10:00:00-04:00
lastmod: 2026-05-22T14:00:00-04:00
description: "Homelab notes — Docker on old hardware, bash automation, Caddy, WireGuard, Proxmox, and diagrams of the setup."
translationKey: home-networking-evolution
tags:
  - Networking
  - Homelab
  - Docker
  - WireGuard
  - Proxmox
  - Caddy
images:
  - featured.png
---

Cloud bills pushed me toward a **home lab**: old PCs, Docker instead of SaaS where possible, and enough scripting to rebuild after a bad weekend. This post is how that network grew — not a perfect design, but one that taught routing, VPNs, and virtualization by breaking things locally. **[Version française]({{< ref "/posts/home-networking-evolution/index.fr.md" >}})**.

<!--more-->

## Why a home lab

University courses covered IP, VPNs, and routing on paper. Running services at home made the tradeoffs real: power, noise, backups, and “who has SSH when the router dies.”

## Docker first

I mapped **free container stacks** to jobs I was paying for in the cloud — media, dashboards, small utilities. Docker was the on-ramp to treating the homelab as composable services instead of one giant pet server.

## Bash and two servers

Core hardware: a cheap **Dell** box plus an older 2004-era machine. **Bash** scripts for **Ubuntu**, **CentOS**, and **Proxmox** installs — repeatable enough that reinstalling after experiments hurt less.

![Homelab overview](./images/featured.png)

### Physical rack (October 2022)

Before the Lucidchart diagrams, the lab was literally **closets and shelves** — cable nest included. I cropped these from old story posts; they are the real wiring, not a render.

**Wall stack** — switch, modem, router, **enterprise server (2010-era)**, and UPS, labeled while I was still learning what plugged into what:

![Home lab network stack labeled — switch, modem, router, server, UPS](./images/homelab-wall-stack-labeled.jpeg)

**Dell PowerEdge R710** — dual **Xeon X5667** (~3 GHz quad-core), **24 GB RAM**, running headless beside acoustic foam. The handwritten tape on the bezel was my inventory system:

![Dell PowerEdge R710 homelab server with Xeon X5667 and 24 GB RAM](./images/dell-poweredge-r710-homelab.jpeg)

**Closet shelf build** — rack server horizontal, yellow switch, monitor for local installs, and enough blue patch cables to teach patience:

![Homelab server closet — rack server, switch, monitor, and cabling](./images/homelab-closet-server-setup.jpeg)

Virtualization matters when you snapshot before trying something dumb. A dedicated hypervisor host beat bare-metal churn.

![Network diagram (Lucidchart)](./images/lucidchart.jpeg)

## Remote access and edge

**Caddy** as reverse proxy; public exposure through an **OVH** front so home IP is not the only line of defense. Remote admin and health checks became part of the same story as “make the service reachable.”

**WireGuard** for VPN — annoying to configure the first time, fast once up. I contributed small setup helpers so friends could connect without reading man pages for a week.

## Growth after moving

New apartment, more VLAN curiosity, **Proxmox** VMs for club projects. **Lucidchart** for the wall diagram; **C4**-style views when explaining the stack to someone else.

![C4-style view](./images/c4.jpeg)

Later I moved public sites toward **static hosting** (S3/GitHub Pages) to cut always-on cost — the lab stayed for private services.

## Where it landed

A homelab is a sandbox for **platform instincts**: automate installs, document topology, assume failure. Related today: **[MediaBoxDockerCompose](https://github.com/antoinebou12/MediaBoxDockerCompose)** and install scripts on the main CV project list.
