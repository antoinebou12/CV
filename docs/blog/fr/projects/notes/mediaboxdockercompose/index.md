# MediaBoxDockerCompose : Une pile média reliée par volumes et réseaux

> MediaBoxDockerCompose rassemble des services homelab avec Docker Compose. Son architecture réside surtout dans les définitions, chemins partagés et…

- Page HTML: https://antoineboucher.info/CV/blog/fr/projects/notes/mediaboxdockercompose/
- Langue: fr
- Traduction (en): https://antoineboucher.info/CV/blog/projects/notes/mediaboxdockercompose/index.md
- Publié: 2026-10-23
- Mis à jour: 2026-10-23
- Auteur: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Dépôt: https://github.com/antoinebou12/MediaBoxDockerCompose
- Licence: MIT
- Révision inspectée: 57d930a836819f7fd3a3421ee5ece5efe3e41778

## Résumé

MediaBoxDockerCompose rassemble des services homelab avec Docker Compose. Les définitions de services, chemins partagés et connexions réseau décrivent leur fonctionnement commun.

**Pourquoi il existe:** Stack GitOps complète combinant réseau sécurisé WireGuard VPN et plus de 15 microservices d'automatisation homelab.

**Cas d’usage:** Serveur multimédia privé conteneurisé avec accès distant chiffré et routage sécurisé.

## Technologies vérifiées

- Docker Compose — docker-compose.yml multi-service stack
- WireGuard VPN — Secure VPN tunnel integration
- Whisper AI — Automated audio transcription worker
- Portainer — Container management interface

## Démarrage (commandes du dépôt, non exécutées ici)

### README.md · Usage

```bash
docker-compose up -d
```


### Docker

```bash
docker-compose up -d
```

## Fonctions et composants

- **Rôles des services** — Le fichier Compose contient des clients de téléchargement et gestionnaires comme Deluge, Jackett, Sonarr et Radarr. Chaque conteneur a son image et sa configuration. Les liens du README doivent être distingués des services réellement activés.
- **Chemins persistants** — Les volumes relient les chemins des conteneurs au stockage hôte. Les services doivent s’accorder sur les chemins lors d’un déplacement de fichiers. Réseau et persistance résolvent deux problèmes d’intégration différents.

## Architecture

Composants et connexions vérifiés dans le dépôt.

- Définitions Compose → Conteneurs de téléchargement
- Définitions Compose → Gestionnaires média
- Conteneurs de téléchargement → Stockage hôte partagé
- Gestionnaires média → Stockage hôte partagé

```mermaid
flowchart LR
  n0["Définitions Compose"]
  n1["Conteneurs de téléchargement"]
  n2["Gestionnaires média"]
  n3["Stockage hôte partagé"]
  n0 --> n1
  n0 --> n2
  n1 --> n3
  n2 --> n3
```

**Un parcours dans le code:** Choisissez un service et comparez ses volumes de téléchargement et bibliothèque à ceux du consommateur. Vérifiez ensuite réseau et ports. Deux conteneurs en bon état peuvent ne pas partager la même vue des fichiers.

## Services Compose

| Service | Runtime | Ports | Dépend de |
| --- | --- | --- | --- |
| plex | plexinc/pms-docker | 32400:32400 |  |
| wireguard | linuxserver/wireguard | 51820:51820/udp |  |
| whisper | local build / compose | 9000:9000 |  |
| portainer | portainer/portainer-ce | 9443:9443 |  |
| samba | dperson/samba | 139:139, 445:445 |  |

## Limites et points à vérifier

Les images et services externes évoluent séparément. Vérifiez identifiants, ports publiés et permissions hôte avant de lancer cette pile personnelle ailleurs.

## Fichiers à lire

- [docker-compose.yml](https://github.com/antoinebou12/MediaBoxDockerCompose/blob/master/docker-compose.yml)
- [README.md](https://github.com/antoinebou12/MediaBoxDockerCompose/blob/master/README.md)

