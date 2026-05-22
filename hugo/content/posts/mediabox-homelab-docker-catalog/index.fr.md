---
post_kind: article
title: "MediaBox homelab — ce que je fais tourner en Docker (et le reste en signet)"
date: 2024-03-15T10:00:00-04:00
lastmod: 2026-05-22T22:00:00-04:00
description: "Comment MediaBoxDockerCompose est né d’une carte de ports homelab — ce qui est câblé, et où entrent les scripts Proxmox."
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

Je gardais une liste perso d’apps auto-hébergées à essayer — surtout pour arrêter d’assigner des ports au hasard et d’oublier ce qui vivait sur `:8096`. Cette liste est devenue **[MediaBoxDockerCompose](https://github.com/antoinebou12/MediaBoxDockerCompose)** sur GitHub. Ce billet est la version courte : ce que j’ai câblé, comment j’installe sur Proxmox quand le compose n’est pas le bon format, et où vit la carte complète des ports pour ne pas transformer la page en tableur avec du SEO. **[English version]({{< ref "/posts/mediabox-homelab-docker-catalog/index.md" >}})**.

<!--more-->

![Pile réseau maison — switch, modem, routeur, serveur, onduleur](./images/featured.jpeg)

Même chapitre que **[l’évolution réseau]({{< ref "/posts/home-networking-evolution/index.fr.md" >}})** — câbles au mur, services dans git. La photo date de l’époque où je labelais encore les ports au ruban adhésif ; le fichier compose, lui, a survécu.

## C’est quoi MediaBox

Un `docker-compose.yml`, des chemins `ROOT` partagés sur disque, et des opinions acquises en cassant des choses chez moi. Je l’utilise quand je veux **un hôte, plusieurs conteneurs, volumes communs** — Jellyfin à côté de Deluge à côté de FreshRSS sans un LXC par hobby.

Le README du dépôt a **ports par défaut, identifiants, sauvegarde** et la procédure d’install que je suis vraiment. Ce billet donne le contexte ; le [README](https://github.com/antoinebou12/MediaBoxDockerCompose#readme) est le manuel.

## Ce que j’ai câblé (par métier, pas par case à cocher)

Services restés assez longtemps dans le compose pour compter. Les ports sont comment je les joignais sur le LAN (familles `:800x` volontaires — plus simple derrière Caddy).

### Média et fichiers

| Service | Port | Pourquoi je l’ai gardé |
|---------|------|------------------------|
| [Jellyfin](https://jellyfin.org/) | :8096 | Lecture sans drama de compte Plex |
| [Airsonic](https://github.com/linuxserver/docker-airsonic) | :4040 | Musique et podcasts au même endroit |
| [Deluge](https://github.com/deluge-torrent/deluge) | :8112 | Client torrent scriptable |
| [Cloud torrent](https://github.com/jpillora/cloud-torrent) | :6889 | File d’attente à distance |
| [Mylar](https://hub.docker.com/r/linuxserver/mylar) | :8090 | BD sans chasse manuelle |
| [Piwigo](https://hub.docker.com/r/linuxserver/piwigo/) | :8049 | Galerie famille |
| [Lychee](https://github.com/electerious/Lychee) | :8035 | Partage photo plus léger |

**Plex, Sonarr, Radarr** et la suite *Arr restent en signet — même rayon homelab, pas dans mon compose aujourd’hui. Sur Proxmox j’utilise plutôt les helper-scripts (ci-dessous).

### Tableaux de bord, accès distant, ops

| Service | Port | Pourquoi je l’ai gardé |
|---------|------|------------------------|
| [Dashmachine](https://github.com/rmountjoy92/DashMachine) | :5000 | Une page de liens quand j’oubliais les URL |
| [Netdata](https://github.com/netdata/netdata) | :19999 | « Le disque est plein encore ? » en un coup d’œil |
| [Guacamole](https://github.com/oznu/docker-guacamole) | :8012 | RDP/VNC dans le navigateur |
| [KDE in Docker](https://github.com/ms-jpq/kde-in-docker) | :8100 | Bureau complet dans un onglet |
| [Ubuntu XRDP](https://github.com/danielguerra69/ubuntu-xrdp) | :3389 | Avec Guacamole pour une vraie session bureau |
| [TeamSpeak](https://github.com/solidnerd/docker-teamspeak) | — | Vocal avec des amis à l’ère lockdown |
| [Linkd](https://github.com/HexF/linkd) | — | Raccourcis sur mon domaine |

### Notes, RSS, argent, schémas

| Service | Port | Pourquoi je l’ai gardé |
|---------|------|------------------------|
| [BookStack](https://www.bookstackapp.com/) | :6875 | Doc homelab structurée |
| [Wallabag](https://github.com/wallabag/wallabag) | :8899 | Lire plus tard sans abonnement |
| [FreshRSS](https://hub.docker.com/r/linuxserver/freshrss) | :8007 | Flux centralisés |
| [DailyNotes](https://github.com/m0ngr31/DailyNotes) | :5001 | Journal quotidien quand je l’utilisais |
| [Firefly III](https://www.firefly-iii.org/) | :8006 | Finances perso (sync git en rattrapage) |
| [Grocy](https://github.com/linuxserver/docker-grocy) | :9283 | Garde-manger — ludique plus qu’utile |
| [draw.io](https://hub.docker.com/r/fjudith/draw.io) | :8005 | Diagrammes sans sortir du réseau |
| [Gitea](https://gitea.io/) | :8008 | Git pour essais avant GitHub |
| [Calibre](https://github.com/kovidgoyal/calibre) | :8001, :8002 | E-books |
| [Huginn](https://github.com/huginn/huginn) | :8013 | Automatisation maison |

### Bricolages

| Service | Port | Note |
|---------|------|------|
| [Neko](https://github.com/nurdism/neko) | :8032 | Navigateur partagé — expériences watch-party |
| [Deezloader Remix](https://notabug.org/RemixDevs/DeezloaderRemix) | :1730 | Stack legacy |
| [OpenTogetherTube](https://github.com/antoinebou13/opentogethertube/tree/docker) | :6666 | Mon fork — watch party |

## Proxmox quand le compose n’est pas le bon outil

Sur **[Proxmox]({{< ref "/posts/home-networking-evolution/index.fr.md" >}})** j’utilise souvent **[Proxmox VE Helper-Scripts](https://github.com/community-scripts/ProxmoxVE)** — one-liners maintenus par la communauté (suite au travail de [tteck](https://github.com/tteck)). Chercher sur **[community-scripts.org](https://community-scripts.org/)**, coller dans le shell Proxmox, mode par défaut ou avancé, obtenir un CT et un menu post-install.

Mêmes noms que ma vieille liste — Jellyfin, Vaultwarden, AdGuard, Home Assistant — autre empaquetage. J’ai eu **compose sur une VM** et **CT séparés via helper-scripts** sur le même rack selon volumes partagés ou isolation stricte.

## Outils sur l’hôte (hors compose)

**Ansible**, **Cockpit** (:9090), **Dokku** et **Lynk** quand le travail c’est « gérer le métal » ou « exposer du TCP proprement », pas « une ligne de plus dans compose ».

## La longue liste de souhaits

L’ancien tableur avait **86 noms Docker** et plein d’entrées jamais câblées — Nextcloud, Vaultwarden, piles mail, serveurs de jeux, tout le cortège *Arr. Je ne colle pas cette grille ici ; elle vieillit mal et ressemble à un tableau de bord de statut.

Pour la carte exhaustive : dépôt [MediaBoxDockerCompose](https://github.com/antoinebou12/MediaBoxDockerCompose), ou [community-scripts.org/categories](https://community-scripts.org/) côté Proxmox. Un conteneur isolé sur Linux frais avant le compose complet : **[another-install-script](https://github.com/antoinebou12/another-install-script)**.

## Ce qui m’est resté

- **Des familles de ports** — `:800x` a sauvé pare-feu et tête.
- **Faire tourner une fois ≠ exploiter** — des essais LAN-only restent utiles.
- **Les forks accueillent les idées** — [OpenTogetherTube](https://github.com/antoinebou13/opentogethertube/tree/docker), [wireguardweb](https://github.com/antoinebou13/wg-access-server/tree/update).
- **Choisir compose ou scripts Proxmox selon la forme du problème**, pas selon la mode du moment.

## Articles connexes

- [Évolution réseau — homelab]({{< ref "/posts/home-networking-evolution/index.fr.md" >}})
- [Renpho + Home Assistant]({{< ref "/posts/renpho-health-api-blueprint/index.fr.md" >}})
- [Caddy sur AWS]({{< ref "/posts/caddy-ec2-cloudwatch-lambda/index.fr.md" >}})
