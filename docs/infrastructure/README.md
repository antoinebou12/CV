# Infrastructure Documentation

Infrastructure documentation for Docker, Nginx, and related technologies used in this project.

## Overview

The CV/resume website infrastructure includes:

- **Docker**: Containerization and local development
- **Nginx**: Web server for static content
- **Traefik**: Reverse proxy and load balancer

## Components

### Docker
- **Purpose**: Containerization, local development, testing
- **Files**: `Dockerfile.nginx`, `Dockerfile.cv`, `docker-compose.yml`
- **Documentation**: [Docker Setup](./docker.md)

### Nginx
- **Purpose**: Web server for static files
- **Files**: `configs/nginx/*.conf`
- **Documentation**: [Nginx Configuration](./nginx.md)

### Traefik
- **Purpose**: Reverse proxy, load balancing, routing
- **Files**: `configs/traefik/*.yml`
- **Configuration**: Integrated in docker-compose.yml

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Traefik   │  (Reverse Proxy)
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌─────┐ ┌──────────┐
│ CV  │ │ Linktree │
│Site │ │  Site    │
└─────┘ └──────────┘
```

## Quick Reference

### Docker Commands
```bash
docker-compose up -d          # Start services
docker-compose down           # Stop services
docker-compose logs -f        # View logs
docker-compose restart        # Restart services
```

### Nginx Commands
```bash
nginx -t                      # Test config
nginx -s reload               # Reload config
nginx -s stop                 # Stop server
```

## Configuration Files

### Docker
- `docker-compose.yml` - Service definitions
- `Dockerfile.nginx` - Nginx image
- `Dockerfile.cv` - LaTeX compiler image

### Nginx
- `configs/nginx/cv-site.conf` - CV site configuration
- `configs/nginx/linktree-site.conf` - Linktree configuration

### Traefik
- `configs/traefik/traefik.yml` - Main configuration
- `configs/traefik/dynamic.yml` - Dynamic routing

## Networking

### Docker Network
- **Name**: `cv-network`
- **Type**: Bridge
- **Purpose**: Service communication

## Monitoring

### Health Checks
- **CV Site**: `/health` endpoint
- **Nginx Status**: `/nginx_status` (internal)
- **Traefik Dashboard**: `/api` endpoint

### Logs
- **Docker**: `docker-compose logs`
- **Nginx**: `/var/log/nginx/`

## Security

### Headers
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection

### Access Control
- Nginx status endpoints restricted
- Traefik dashboard access controlled

## Next Steps

- [Docker Setup](./docker.md) - Detailed Docker documentation
- [Nginx Configuration](./nginx.md) - Nginx setup
