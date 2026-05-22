---
post_kind: article
title: "MediaBox homelab — Docker service catalog (86 apps, 28 implemented)"
date: 2024-03-15T10:00:00-04:00
lastmod: 2026-05-22T21:00:00-04:00
description: "The spreadsheet behind MediaBoxDockerCompose — ports, roles, Proxmox helper-scripts, and which self-hosted apps are wired in compose."
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

Before my homelab was a tidy compose file, it was a **spreadsheet** — one row per self-hosted app I wanted to try, columns for Docker, ports, volumes, and an **Implemented** checkbox I had to earn. This post is that catalog on the blog: what each name does, which port I mapped, and how it relates to **[MediaBoxDockerCompose](https://github.com/antoinebou12/MediaBoxDockerCompose)** and **[Proxmox VE Helper-Scripts](https://github.com/community-scripts/ProxmoxVE)**. **[Version française]({{< ref "/posts/mediabox-homelab-docker-catalog/index.fr.md" >}})**.

<!--more-->

![Homelab wall stack — switch, modem, router, server, UPS](./images/featured.jpeg)

Same era as **[networking evolution]({{< ref "/posts/home-networking-evolution/index.md" >}})** — hardware on the wall first, port map in git second. The spreadsheet was never a uptime dashboard; it was a wish list with honest checkboxes.

## By the numbers

| Metric | Value |
|--------|------:|
| **Docker services catalogued** | 86 |
| **Implemented** (checked in compose or fork) | 28 |
| **Still bookmarked only** | 58 |
| **Host-native tools** (no container row) | 4 |

**Implemented** means I wired it in compose (or a fork I maintain), thought about volumes, and logged in at least once. It does not mean production-grade, patched monthly, or exposed to the internet.

## Proxmox: the other install path

On **[Proxmox]({{< ref "/posts/home-networking-evolution/index.md" >}})** hosts I often skip hand-rolling LXC configs. **[Proxmox VE Helper-Scripts](https://github.com/community-scripts/ProxmoxVE)** (community edition, built on [tteck](https://github.com/tteck)'s original work) installs services with a one-liner from the Proxmox shell — Jellyfin, *Arr apps, Vaultwarden, AdGuard Home, Home Assistant, and hundreds more. Pick a script on **[community-scripts.org](https://community-scripts.org/)**, paste the command, choose **Default** or **Advanced**, and you get an LXC (or VM) plus a post-install helper for updates.

That repo overlaps heavily with names in my spreadsheet. Same apps, different packaging: **compose on one Docker host** vs **Proxmox CT from community-scripts**. I keep both references because my rack has seen both patterns — a single VM running `docker compose up -d`, and separate CTs spawned from helper-scripts when I wanted isolation without writing YAML for every service.

## How to read the tables

| Column | Meaning |
|--------|---------|
| **Service** | Name in the catalog / compose folder |
| **Role** | Why I bothered bookmarking it |
| **Web** | Browser port on the host (`:8080` style) |

Sections marked **Implemented** match a checked row in the old sheet. **Spreadsheet only** means Docker ✅ in the catalog but not in my compose file yet. Install details: **[compose README](https://github.com/antoinebou12/MediaBoxDockerCompose#readme)** or the matching script on [community-scripts.org](https://community-scripts.org/).

---

## Implemented — media, downloads, and libraries

| Service | Role | Web |
|---------|------|-----|
| [jellyfin](https://jellyfin.org/) | Free Plex alternative — libraries and clients | :8096 |
| [airsonic](https://github.com/linuxserver/docker-airsonic) | Music and podcast server | :4040 |
| [deluge](https://github.com/deluge-torrent/deluge) | BitTorrent client | :8112 |
| [cloudtorrent](https://github.com/jpillora/cloud-torrent) | Remote torrent client in the browser | :6889 |
| [mylar](https://hub.docker.com/r/linuxserver/mylar) | Automated comic downloads | :8090 |
| [deezloaderremix](https://notabug.org/RemixDevs/DeezloaderRemix) | Deezer-backed music tool (legacy stack) | :1730 |
| [piwigo](https://hub.docker.com/r/linuxserver/piwigo/) | Self-hosted photo gallery | :8049 |
| [lychee](https://github.com/electerious/Lychee) | Photo management and sharing | :8035 |

**Spreadsheet only (same category):** [plex](https://www.plex.tv/) (:8050), [emby](https://hub.docker.com/r/linuxserver/emby) (:8096), [sonarr](https://sonarr.tv/) (:8059), [radarr](https://radarr.video/) (:7878), [jackett](https://github.com/Jackett/Jackett) (API, no web UI), [ombi](https://hub.docker.com/r/linuxserver/ombi/) (:3579), [tautulli](https://github.com/Tautulli/Tautulli) (:8063), [tdarr](https://github.com/HaveAGitGat/Tdarr) (:8265), [couchpotato](https://github.com/CouchPotato/CouchPotatoServer) (:5050), [medusa](https://github.com/pymedusa/Medusa) (:8038), [headphones](https://hub.docker.com/r/linuxserver/headphones/) (:8181), [htpcdownloadbox](https://github.com/sebgl/htpc-download-box) (:8112). Several of these also exist as [ProxmoxVE](https://github.com/community-scripts/ProxmoxVE) scripts if you prefer LXC.

---

## Implemented — dashboards, ops, and remote access

| Service | Role | Web |
|---------|------|-----|
| [dashmachine](https://github.com/rmountjoy92/DashMachine) | Bookmark dashboard with extras | :5000 |
| [netdata](https://github.com/netdata/netdata) | Real-time host monitoring | :19999 |
| [guacamole](https://github.com/oznu/docker-guacamole) | Clientless remote desktop gateway | :8012 |
| [kdedocker](https://github.com/ms-jpq/kde-in-docker) | KDE in the browser | :8100 |
| [ubuntuxrdp](https://github.com/danielguerra69/ubuntu-xrdp) | Ubuntu desktop + XRDP (pairs with Guacamole) | :3389 |
| [teamspeak](https://github.com/solidnerd/docker-teamspeak) | Voice chat server | — |
| [linkd](https://github.com/HexF/linkd) | Self-hosted link shortener (Deno) | — |

**Spreadsheet only:** [heimdall](https://hub.docker.com/r/linuxserver/heimdall/) (:8080), [portainer](https://www.portainer.io/) (:9001), [grafana](https://grafana.com/) (:8011), [statping](https://github.com/hunterlong/statping) (:8061), [meshcentral](https://github.com/Ylianst/MeshCentral) (:8001), [wireguardweb](https://github.com/antoinebou13/wg-access-server/tree/update) (:7676), [openvpn](https://github.com/kylemanna/docker-openvpn) (:1194).

---

## Implemented — knowledge, RSS, and money

| Service | Role | Web |
|---------|------|-----|
| [bookstack](https://www.bookstackapp.com/) | Wiki-style documentation | :6875 |
| [wallabag](https://github.com/wallabag/wallabag) | Read-it-later | :8899 |
| [freshrss](https://hub.docker.com/r/linuxserver/freshrss) | Self-hosted RSS reader | :8007 |
| [dailynotes](https://github.com/m0ngr31/DailyNotes) | Daily notes and tasks | :5001 |
| [fireflyiii](https://www.firefly-iii.org/) | Personal finance manager | :8006 |
| [grocy](https://github.com/linuxserver/docker-grocy) | Kitchen / pantry ERP | :9283 |
| [drawio](https://hub.docker.com/r/fjudith/draw.io) | Diagrams in the browser | :8005 |
| [gitea](https://gitea.io/) | Lightweight self-hosted Git | :8008 |
| [calibre](https://github.com/kovidgoyal/calibre) | E-book library | :8001, :8002 |
| [huginn](https://github.com/huginn/huginn) | Agent automation (“if this then that” you host) | :8013 |

**Firefly III** was marked “need to add to git” in the sheet — implemented in compose, repo hygiene still catching up.

**Spreadsheet only:** [bitwarden](https://github.com/bitwarden) (:8000), [paperless](https://github.com/the-paperless-project/paperless) (:8047), [recipes](https://github.com/vabene1111/recipes) (:8055), [gitlab](https://hub.docker.com/r/gitlab/gitlab-ce/) (:8009), [gogs](https://github.com/gogs/gogs) (:10080), [codeserver](https://github.com/cdr/code-server) (:8003), [jenkins](https://jenkins.io/) (:8015). [Vaultwarden](https://github.com/dani-garcia/vaultwarden) is a common pick on [ProxmoxVE](https://github.com/community-scripts/ProxmoxVE) if you want password management without my compose row.

---

## Implemented — fun, social, and experiments

| Service | Role | Web |
|---------|------|-----|
| [neko](https://github.com/nurdism/neko) | Shared virtual browser | :8032 |

**Spreadsheet only:** [opentogethertube](https://github.com/antoinebou13/opentogethertube/tree/docker) (:6666) — my fork for watch-together; [invidious](https://github.com/omarroth/invidious) (:8014), [cyberchef](https://github.com/gchq/CyberChef) (:8004), [osjs](https://github.com/os-js/OS.js) (:7999), [rocketchat](https://rocket.chat/) (:8056), [jitsi](https://github.com/jitsi/jitsi-meet) (:80), [minecraft](https://hub.docker.com/r/itzg/minecraft-server) (:25565), [mcmyadmin](https://www.mcmyadmin.com/) (:8037).

---

## Spreadsheet only — rest of the Docker catalog

Grouped for skimming; all had **Docker ✅** in the original sheet but **Implemented ⬜**.

### Files, sync, and backup

| Service | Role | Web |
|---------|------|-----|
| [nextcloud](https://github.com/nextcloud) | Files and collaboration | :9321 |
| [syncthing](https://github.com/syncthing/syncthing) | Continuous file sync | :8384 |
| [duplicati](https://hub.docker.com/r/linuxserver/duplicati/) | Encrypted backups | :8200 |
| [chevereto](https://github.com/Chevereto/Chevereto-Free) | Image hosting | :8999 |
| [youtransfer](https://github.com/YouTransfer/YouTransfer) | Self-hosted file send | :5004 |
| [privatebin](https://privatebin.info/) | Zero-knowledge pastebin | :8052 |

### Video, streaming, and creative

| Service | Role | Web |
|---------|------|-----|
| [open-streaming-platform](https://gitlab.com/Deamos/flask-nginx-rtmp-manager) | Self-hosted streaming | :8585 |
| [komga](https://github.com/gotson/komga) | Comics / manga server | :8031 |
| [mango](https://github.com/hkalexling/Mango) | Manga web reader | :8036 |
| [olaris](https://gitlab.com/olaris/olaris-server) | Media manager + transcoding | :8043 |

### Business, CRM, and misc apps

| Service | Role | Web |
|---------|------|-----|
| [odoo](https://github.com/odoo/odoo) | ERP / business apps | :8069 |
| [monica](https://github.com/monicahq/monica) | Personal CRM | :8039 |
| [onlyoffice](https://github.com/ONLYOFFICE/Docker-CommunityServer) | Docs + projects suite | :80 |
| [liberapay](https://en.liberapay.com/) | Donation platform | :8339 |
| [libresignage](https://github.com/eerotal/LibreSignage) | Digital signage | :8030 |
| [lodestone](https://github.com/AnalogJ/lodestone) | Personal document archive | :8034 |
| [n8n](https://n8n.io/) | Workflow automation | :5678 |
| [spiderfoot](https://github.com/smicallef/spiderfoot) | OSINT automation | — |
| [newspipe](https://github.com/cedricbonhomme/newspipe) | News aggregator | :5003 |

### Identity, mail, and infra-heavy

| Service | Role | Web |
|---------|------|-----|
| [keycloak](https://www.keycloak.org/) | IAM | :8050 |
| [openldap](https://github.com/osixia/docker-openldap) | LDAP directory | :389 |
| [mailcow](https://mailcow.email/) | Mail server bundle | — |
| [jitsi](https://github.com/jitsi/jitsi-meet) | Video conferences | :80 |

### Games and voice

| Service | Role | Web |
|---------|------|-----|
| [minecraft](https://hub.docker.com/r/itzg/minecraft-server) | Minecraft server | :25565 |
| [mcmyadmin](https://www.mcmyadmin.com/) | Minecraft admin UI | :8037 |
| [mumble](https://github.com/coppit/docker-mumble-server) | Voice chat | :64738 |

---

## Host tools (no Docker row)

Same spreadsheet, but installed **on the host** — all marked implemented there:

| Tool | Role | Web |
|------|------|-----|
| [ansible](https://www.ansible.com/integrations/containers/docker) | Server automation | — |
| [cockpit](https://cockpit-project.org/) | Web UI for Linux servers | :9090 |
| [dokku](https://github.com/dokku/dokku) | Docker-powered PaaS | — |
| [lynk](https://lynk.sh/docs) | Expose TCP services securely | — |

---

## What I learned from maintaining the sheet

- **Port planning beats port chaos** — `:800x` families made Caddy and firewall rules predictable.
- **Implemented ≠ production** — a checked box meant “I got it working on my LAN,” not “patched forever.”
- **33% was enough to learn** — comparing apps mattered more than running all 86.
- **Forks stay in the catalog** — [opentogethertube](https://github.com/antoinebou13/opentogethertube/tree/docker) and [wireguardweb](https://github.com/antoinebou13/wg-access-server/tree/update) are where I experiment before upstream.
- **Proxmox scripts vs compose** — use [ProxmoxVE](https://github.com/community-scripts/ProxmoxVE) when you want isolation per service; use **[MediaBoxDockerCompose](https://github.com/antoinebou12/MediaBoxDockerCompose)** when you want one file and shared volumes.

Starting out: one category at a time (RSS + dashboards, then media, then downloads). For single containers before full compose, **[another-install-script](https://github.com/antoinebou12/another-install-script)** is the menu-driven path I used on fresh Linux installs.

## Related posts

- [Networking evolution — home lab]({{< ref "/posts/home-networking-evolution/index.md" >}}) — physical network, Proxmox, Caddy/WireGuard
- [Renpho + Home Assistant]({{< ref "/posts/renpho-health-api-blueprint/index.md" >}}) — another self-hosted data project
- [Caddy on AWS]({{< ref "/posts/caddy-ec2-cloudwatch-lambda/index.md" >}}) — when the reverse proxy leaves the basement
