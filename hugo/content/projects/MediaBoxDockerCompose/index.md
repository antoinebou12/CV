---
title: "MediaBoxDockerCompose"
date: 2024-01-01T12:00:00Z
description: "An all-in-one Docker Compose solution for your media management needs."
draft: false
---

## MediaBoxDockerCompose

MediaBoxDockerCompose is a comprehensive Docker Compose project that integrates various tools for downloading, organizing, and playing media content. It simplifies setting up a complete media center with automated processes for TV shows, movies, music, and more.

### Docker Containers

This project includes a suite of Docker containers for various media management tasks:

- **Deluge, Jackett, NZBGet**: For torrenting and NZB management.
- **Sonarr, Radarr, Lidarr, Bazarr**: For automatic downloading of TV shows, movies, music, and subtitles.
- **Plex, Jellyfin, Ombi, Tautulli**: Media servers and management tools.
- **Netdata, Dashmachine, Filebrowser**: Administration and monitoring tools.
- **Prowlarr, Readarr, Whisparr, Stash, Jellyseerr**: Additional utilities for media management.

### Installation

1. Ensure Docker and Docker Compose are installed on your system.
2. Clone or download this repository.

### Usage

1. Navigate to the cloned/downloaded directory.
2. Customize the configuration files.
3. Start the containers with `docker-compose up -d`.
4. Access the services via their web interfaces.

### Administration Tools

Monitor and manage your setup using tools like Netdata, FileBrowser, and Wireguard.

### Torrenting Tools

Deluge, NZBGet, and Jackett are included for handling torrent and NZB files.

### Automatic Downloaders

Automate your downloads with Sonarr, Radarr, Lidarr, and Bazarr.

### Media and Player Services

Manage and play your media with Plex, Jellyfin, Ombi, and Tautulli.

### Web Portal

Access everything through the Dashmachine portal for ease of use.

### Backup and Restore

Detailed steps for backing up and restoring configurations for each service.

### Contributing

Guidelines for contributing to the project and how to make pull requests.

### License

This project is licensed under the MIT License - with a link to the full license text.

---

With MediaBoxDockerCompose, setting up and managing a home media center becomes straightforward, automated, and efficient. It's the perfect solution for enthusiasts and professionals alike looking to streamline their media experience.
