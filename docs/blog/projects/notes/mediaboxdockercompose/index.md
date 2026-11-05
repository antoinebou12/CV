# MediaBoxDockerCompose: A media stack connected by volumes and networks

> MediaBoxDockerCompose brings several homelab services together in Docker Compose. Its architecture lives mainly in service definitions, shared…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/mediaboxdockercompose/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/mediaboxdockercompose/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Repository: https://github.com/antoinebou12/MediaBoxDockerCompose
- License: MIT
- Inspected revision: 57d930a836819f7fd3a3421ee5ece5efe3e41778

## Summary

MediaBoxDockerCompose brings several homelab services together in Docker Compose. Service definitions, shared filesystem paths and network connections describe how they work together.

**Why it exists:** Comprehensive GitOps container stack combining WireGuard VPN tunnel networking with 15+ homelab automation services.

**Best fit:** Automated, isolated private cloud media server with remote access and encrypted traffic routing.

## Verified technologies

- Docker Compose — docker-compose.yml multi-service stack
- WireGuard VPN — Secure VPN tunnel integration
- Whisper AI — Automated audio transcription worker
- Portainer — Container management interface

## Getting started (repository commands, not run here)

### README.md · Usage

```bash
docker-compose up -d
```


### Docker

```bash
docker-compose up -d
```

## Features and components

- **Service roles** — The compose file includes download clients and media-management services such as Deluge, Jackett, Sonarr and Radarr. Each container has its own image and configuration. README service links should be distinguished from services actually enabled in Compose.
- **Persistent paths** — Volume mappings connect container paths to host storage. A path used by one service must agree with the path seen by another when files move between them. Networking and persistence solve different integration problems.

## Architecture

Components and connections verified in the repository.

- Compose service definitions → Download containers
- Compose service definitions → Media-management containers
- Download containers → Shared host storage
- Media-management containers → Shared host storage

```mermaid
flowchart LR
  n0["Compose service definitions"]
  n1["Download containers"]
  n2["Media-management containers"]
  n3["Shared host storage"]
  n0 --> n1
  n0 --> n2
  n1 --> n3
  n2 --> n3
```

**One path through the code:** Choose one service and compare its mounted download and library paths with the service that consumes them. Then check its network and port settings. Two healthy containers can still disagree about where a file exists.

## Compose services

| Service | Runtime | Ports | Depends on |
| --- | --- | --- | --- |
| plex | plexinc/pms-docker | 32400:32400 |  |
| wireguard | linuxserver/wireguard | 51820:51820/udp |  |
| whisper | local build / compose | 9000:9000 |  |
| portainer | portainer/portainer-ce | 9443:9443 |  |
| samba | dperson/samba | 139:139, 445:445 |  |

## Constraints and checks

Image tags and external services age independently. Review credentials, published ports and host permissions before starting this personal stack elsewhere.

## Files to read

- [docker-compose.yml](https://github.com/antoinebou12/MediaBoxDockerCompose/blob/master/docker-compose.yml)
- [README.md](https://github.com/antoinebou12/MediaBoxDockerCompose/blob/master/README.md)

