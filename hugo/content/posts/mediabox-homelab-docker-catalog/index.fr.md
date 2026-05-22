---
post_kind: article
title: "MediaBox homelab — catalogue Docker (86 apps, 28 implémentées)"
date: 2024-03-15T10:00:00-04:00
lastmod: 2026-05-22T21:00:00-04:00
description: "Le tableur derrière MediaBoxDockerCompose — ports, rôles, scripts Proxmox community-scripts, et apps câblées dans le compose."
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

Avant que mon homelab soit un fichier compose propre, c’était un **tableur** — une ligne par app auto-hébergée à tester, colonnes Docker, ports, volumes, et une case **Implémenté** à mériter. Ce billet reprend ce catalogue : rôle de chaque nom, port mappé, et liens avec **[MediaBoxDockerCompose](https://github.com/antoinebou12/MediaBoxDockerCompose)** et **[Proxmox VE Helper-Scripts](https://github.com/community-scripts/ProxmoxVE)**. **[English version]({{< ref "/posts/mediabox-homelab-docker-catalog/index.md" >}})**.

<!--more-->

![Pile réseau maison — switch, modem, routeur, serveur, onduleur](./images/featured.jpeg)

Même époque que **[l’évolution réseau]({{< ref "/posts/home-networking-evolution/index.fr.md" >}})** — le matériel au mur d’abord, la carte des ports dans git ensuite. Le tableur n’était pas un tableau de bord de disponibilité ; c’était une liste de souhaits avec des cases honnêtes.

## En chiffres

| Indicateur | Valeur |
|------------|-------:|
| **Services Docker catalogués** | 86 |
| **Implémentés** (case cochée dans compose ou fork) | 28 |
| **Encore en signet seulement** | 58 |
| **Outils sur l’hôte** (sans ligne conteneur) | 4 |

**Implémenté** = câblé dans compose (ou fork que je maintiens), volumes réfléchis, au moins une connexion réussie. Pas « production », patch mensuel, ou exposé sur Internet.

## Proxmox : l’autre façon d’installer

Sur des hôtes **[Proxmox]({{< ref "/posts/home-networking-evolution/index.fr.md" >}})** j’évite souvent de bricoler chaque LXC à la main. **[Proxmox VE Helper-Scripts](https://github.com/community-scripts/ProxmoxVE)** (édition communautaire, suite au travail de [tteck](https://github.com/tteck)) installe des services en une commande dans le shell Proxmox — Jellyfin, suite *Arr, Vaultwarden, AdGuard Home, Home Assistant, et des centaines d’autres. Choisir un script sur **[community-scripts.org](https://community-scripts.org/)**, coller la commande, mode **Default** ou **Advanced**, et obtenir un CT (ou VM) plus un helper post-install pour les mises à jour.

Ce dépôt recoupe beaucoup de noms de mon tableur. Mêmes apps, empaquetage différent : **compose sur un hôte Docker** vs **CT Proxmox via community-scripts**. Je garde les deux références parce que mon rack a connu les deux — une VM avec `docker compose up -d`, et des CT lancés par helper-scripts quand je voulais l’isolation sans YAML par service.

## Lire les tableaux

| Colonne | Signification |
|---------|----------------|
| **Service** | Nom dans le catalogue / dossier compose |
| **Rôle** | Pourquoi je l’ai mis en signet |
| **Web** | Port navigateur sur l’hôte (style `:8080`) |

Les sections **Implémenté** correspondent à une case cochée dans l’ancien tableur. **Tableur seulement** = Docker ✅ au catalogue mais pas encore dans mon compose. Détails d’install : **[README compose](https://github.com/antoinebou12/MediaBoxDockerCompose#readme)** ou le script équivalent sur [community-scripts.org](https://community-scripts.org/).

---

## Implémenté — média, téléchargements, bibliothèques

| Service | Rôle | Web |
|---------|------|-----|
| [jellyfin](https://jellyfin.org/) | Alternative libre à Plex | :8096 |
| [airsonic](https://github.com/linuxserver/docker-airsonic) | Musique et podcasts | :4040 |
| [deluge](https://github.com/deluge-torrent/deluge) | Client BitTorrent | :8112 |
| [cloudtorrent](https://github.com/jpillora/cloud-torrent) | Client torrent dans le navigateur | :6889 |
| [mylar](https://hub.docker.com/r/linuxserver/mylar) | BD en téléchargement auto | :8090 |
| [deezloaderremix](https://notabug.org/RemixDevs/DeezloaderRemix) | Outil musique Deezer (legacy) | :1730 |
| [piwigo](https://hub.docker.com/r/linuxserver/piwigo/) | Galerie photo | :8049 |
| [lychee](https://github.com/electerious/Lychee) | Photos — gestion et partage | :8035 |

**Tableur seulement (même catégorie) :** [plex](https://www.plex.tv/) (:8050), [emby](https://hub.docker.com/r/linuxserver/emby) (:8096), [sonarr](https://sonarr.tv/) (:8059), [radarr](https://radarr.video/) (:7878), [jackett](https://github.com/Jackett/Jackett), [ombi](https://hub.docker.com/r/linuxserver/ombi/) (:3579), [tautulli](https://github.com/Tautulli/Tautulli) (:8063), [tdarr](https://github.com/HaveAGitGat/Tdarr) (:8265), [couchpotato](https://github.com/CouchPotato/CouchPotatoServer) (:5050), [medusa](https://github.com/pymedusa/Medusa) (:8038), [headphones](https://hub.docker.com/r/linuxserver/headphones/) (:8181), [htpcdownloadbox](https://github.com/sebgl/htpc-download-box) (:8112). Plusieurs existent aussi en scripts [ProxmoxVE](https://github.com/community-scripts/ProxmoxVE).

---

## Implémenté — tableaux de bord, ops, accès distant

| Service | Rôle | Web |
|---------|------|-----|
| [dashmachine](https://github.com/rmountjoy92/DashMachine) | Tableau de liens | :5000 |
| [netdata](https://github.com/netdata/netdata) | Monitoring hôte | :19999 |
| [guacamole](https://github.com/oznu/docker-guacamole) | Bureau à distance sans client lourd | :8012 |
| [kdedocker](https://github.com/ms-jpq/kde-in-docker) | KDE dans le navigateur | :8100 |
| [ubuntuxrdp](https://github.com/danielguerra69/ubuntu-xrdp) | Ubuntu + XRDP (avec Guacamole) | :3389 |
| [teamspeak](https://github.com/solidnerd/docker-teamspeak) | Serveur vocal | — |
| [linkd](https://github.com/HexF/linkd) | Raccourcisseur d’URL (Deno) | — |

**Tableur seulement :** [heimdall](https://hub.docker.com/r/linuxserver/heimdall/) (:8080), [portainer](https://www.portainer.io/) (:9001), [grafana](https://grafana.com/) (:8011), [statping](https://github.com/hunterlong/statping) (:8061), [meshcentral](https://github.com/Ylianst/MeshCentral) (:8001), [wireguardweb](https://github.com/antoinebou13/wg-access-server/tree/update) (:7676), [openvpn](https://github.com/kylemanna/docker-openvpn) (:1194).

---

## Implémenté — docs, RSS, finances

| Service | Rôle | Web |
|---------|------|-----|
| [bookstack](https://www.bookstackapp.com/) | Documentation type wiki | :6875 |
| [wallabag](https://github.com/wallabag/wallabag) | Lire plus tard | :8899 |
| [freshrss](https://hub.docker.com/r/linuxserver/freshrss) | Lecteur RSS | :8007 |
| [dailynotes](https://github.com/m0ngr31/DailyNotes) | Notes et tâches quotidiennes | :5001 |
| [fireflyiii](https://www.firefly-iii.org/) | Finances personnelles | :8006 |
| [grocy](https://github.com/linuxserver/docker-grocy) | ERP cuisine | :9283 |
| [drawio](https://hub.docker.com/r/fjudith/draw.io) | Diagrammes web | :8005 |
| [gitea](https://gitea.io/) | Git auto-hébergé léger | :8008 |
| [calibre](https://github.com/kovidgoyal/calibre) | E-books | :8001, :8002 |
| [huginn](https://github.com/huginn/huginn) | Automatisation par agents | :8013 |

**Firefly III** — noté « à ajouter au git » dans le tableur ; implémenté dans compose, dépôt en rattrapage.

**Tableur seulement :** [bitwarden](https://github.com/bitwarden) (:8000), [paperless](https://github.com/the-paperless-project/paperless) (:8047), [recipes](https://github.com/vabene1111/recipes) (:8055), [gitlab](https://hub.docker.com/r/gitlab/gitlab-ce/) (:8009), [gogs](https://github.com/gogs/gogs) (:10080), [codeserver](https://github.com/cdr/code-server) (:8003), [jenkins](https://jenkins.io/) (:8015). [Vaultwarden](https://github.com/dani-garcia/vaultwarden) est fréquent sur [ProxmoxVE](https://github.com/community-scripts/ProxmoxVE) pour la gestion de mots de passe.

---

## Implémenté — fun et expériences

| Service | Rôle | Web |
|---------|------|-----|
| [neko](https://github.com/nurdism/neko) | Navigateur virtuel partagé | :8032 |

**Tableur seulement :** [opentogethertube](https://github.com/antoinebou13/opentogethertube/tree/docker) (:6666), [invidious](https://github.com/omarroth/invidious) (:8014), [cyberchef](https://github.com/gchq/CyberChef) (:8004), [osjs](https://github.com/os-js/OS.js) (:7999), [rocketchat](https://rocket.chat/) (:8056), [jitsi](https://github.com/jitsi/jitsi-meet) (:80).

---

## Tableur seulement — reste du catalogue Docker

Docker ✅ dans l’ancien tableur, **Implémenté ⬜**.

### Fichiers, sync, sauvegarde

| Service | Rôle | Web |
|---------|------|-----|
| [nextcloud](https://github.com/nextcloud) | Fichiers et collaboration | :9321 |
| [syncthing](https://github.com/syncthing/syncthing) | Sync continue | :8384 |
| [duplicati](https://hub.docker.com/r/linuxserver/duplicati/) | Sauvegardes chiffrées | :8200 |
| [chevereto](https://github.com/Chevereto/Chevereto-Free) | Images | :8999 |
| [youtransfer](https://github.com/YouTransfer/YouTransfer) | Envoi de fichiers | :5004 |
| [privatebin](https://privatebin.info/) | Pastebin | :8052 |

### Vidéo, streaming, créatif

| Service | Rôle | Web |
|---------|------|-----|
| [open-streaming-platform](https://gitlab.com/Deamos/flask-nginx-rtmp-manager) | Streaming | :8585 |
| [komga](https://github.com/gotson/komga) | BD / manga | :8031 |
| [mango](https://github.com/hkalexling/Mango) | Lecteur manga | :8036 |
| [olaris](https://gitlab.com/olaris/olaris-server) | Média + transcodage | :8043 |

### Business et divers

| Service | Rôle | Web |
|---------|------|-----|
| [odoo](https://github.com/odoo/odoo) | ERP | :8069 |
| [monica](https://github.com/monicahq/monica) | CRM personnel | :8039 |
| [onlyoffice](https://github.com/ONLYOFFICE/Docker-CommunityServer) | Suite bureautique | :80 |
| [n8n](https://n8n.io/) | Workflows | :5678 |
| [spiderfoot](https://github.com/smicallef/spiderfoot) | OSINT | — |

### Identité et mail lourd

| Service | Rôle | Web |
|---------|------|-----|
| [keycloak](https://www.keycloak.org/) | IAM | :8050 |
| [openldap](https://github.com/osixia/docker-openldap) | LDAP | :389 |
| [mailcow](https://mailcow.email/) | Mail | — |

---

## Outils sur l’hôte (hors Docker)

Même tableur, install **sur l’hôte** — tous marqués implémentés :

| Outil | Rôle | Web |
|-------|------|-----|
| [ansible](https://www.ansible.com/integrations/containers/docker) | Automatisation | — |
| [cockpit](https://cockpit-project.org/) | Interface web Linux | :9090 |
| [dokku](https://github.com/dokku/dokku) | PaaS Docker | — |
| [lynk](https://lynk.sh/docs) | Exposition TCP | — |

---

## Leçons du tableur

- **Planifier les ports** — familles `:800x`, règles Caddy et pare-feu plus simples.
- **Implémenté ≠ production** — case cochée = « ça marche sur mon LAN ».
- **33 % suffisait pour apprendre** — comparer comptait plus que tout lancer.
- **Les forks restent au catalogue** — [opentogethertube](https://github.com/antoinebou13/opentogethertube/tree/docker), [wireguardweb](https://github.com/antoinebou13/wg-access-server/tree/update).
- **Scripts Proxmox vs compose** — [ProxmoxVE](https://github.com/community-scripts/ProxmoxVE) pour isoler par service ; **[MediaBoxDockerCompose](https://github.com/antoinebou12/MediaBoxDockerCompose)** pour un fichier et des volumes partagés.

Pour démarrer : une catégorie à la fois. Conteneur isolé avant le compose complet : **[another-install-script](https://github.com/antoinebou12/another-install-script)**.

## Articles connexes

- [Évolution réseau — homelab]({{< ref "/posts/home-networking-evolution/index.fr.md" >}})
- [Renpho + Home Assistant]({{< ref "/posts/renpho-health-api-blueprint/index.fr.md" >}})
- [Caddy sur AWS]({{< ref "/posts/caddy-ec2-cloudwatch-lambda/index.fr.md" >}})
