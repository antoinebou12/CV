---
title: "Media center (Docker Compose)"
linkTitle: "MediaBoxDockerCompose"
date: 2024-01-01T12:00:00Z
description: "Stack Docker Compose pour téléchargements, suite *Arr, Plex/Jellyfin et supervision — la config est dans le dépôt."
draft: false
tags: ["Docker", "Docker Compose", "Homelab", "Plex", "Sonarr", "Radarr", "Jellyfin"]
---

[![GitHub last commit](https://img.shields.io/github/last-commit/antoinebou12/MediaBoxDockerCompose)](https://github.com/antoinebou12/MediaBoxDockerCompose)

[Dépôt](https://github.com/antoinebou12/MediaBoxDockerCompose) · [Licence MIT](https://github.com/antoinebou12/MediaBoxDockerCompose/blob/master/LICENSE)

Stack média en Docker Compose : récupération (torrents et Usenet), chaîne *Arr, sous-titres, lecture avec **Plex** ou **Jellyfin**, demandes et supervision. Les volumes et chemins suivent le `docker-compose.yml` du dépôt (variable `ROOT`, etc.).

## Contenu de la stack

Regroupement par rôle (détails dans le [fichier compose](https://github.com/antoinebou12/MediaBoxDockerCompose/blob/master/docker-compose.yml)) :

- **Clients et indexeurs** — Deluge, NZBGet, Jackett, NZBHydra2, Prowlarr  
- **Automatisation** — Sonarr, Radarr, Lidarr, Bazarr, CouchPotato ; Readarr (livres) ; Whisparr ; Tdarr (transcodage)  
- **Bibliothèques et demandes** — Plex, Jellyfin, Ombi, Jellyseerr, Tautulli  
- **Complément** — Stash (organisateur de bibliothèque spécialisé)  
- **Exploitation** — Netdata, Dashmachine, Filebrowser  

## Démarrage rapide

1. Installer [Docker](https://docs.docker.com/get-docker/) et Compose sur la machine.  
2. Cloner le dépôt et renseigner les variables d’environnement (fichier `.env` du dépôt, chemins type `ROOT`).  
3. Depuis le dossier du projet :

```bash
git clone https://github.com/antoinebou12/MediaBoxDockerCompose.git
cd MediaBoxDockerCompose
docker compose up -d
```

L’ancienne commande `docker-compose up -d` reste valable ; le [README](https://github.com/antoinebou12/MediaBoxDockerCompose#readme) du dépôt décrit la procédure en anglais.

## Documentation

**Ports**, **identifiants par défaut**, **sauvegarde / restauration** et **contribution** sont documentés dans le [README](https://github.com/antoinebou12/MediaBoxDockerCompose#readme) pour éviter de dupliquer le manuel sur ce site.
