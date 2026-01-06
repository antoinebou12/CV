# Docker Deployment

Deploy the CV/resume website using Docker and Docker Compose.

## Overview

The Docker setup includes:
- **cv-site**: Main resume website (Nginx)
- **linktree-site**: Linktree page (Nginx)
- **traefik**: Reverse proxy and load balancer

## Prerequisites

- Docker 20.10+
- Docker Compose 2.0+

## Quick Start

### 1. Start All Services

```bash
docker-compose up -d
```

This will:
- Build Nginx images
- Start all services
- Set up networking

### 2. Access the Websites

- **CV Site**: http://localhost:8080
- **Linktree**: http://localhost:8081
- **Traefik Dashboard**: http://localhost:8080/api

### 3. Stop Services

```bash
docker-compose down
```

## Service Details

### CV Site
- **Port**: 8080
- **Config**: `configs/nginx/cv-site.conf`
- **Content**: Root directory (serves `index.html`)

### Linktree Site
- **Port**: 8081
- **Config**: `configs/nginx/linktree-site.conf`
- **Content**: `linktree/` directory

### Traefik
- **Port**: 80 (main), 8080 (dashboard)
- **Config**: `configs/traefik/`
- **Purpose**: Reverse proxy and routing

## Configuration

### Nginx Configuration

Edit Nginx configs in `configs/nginx/`:
- `cv-site.conf` - Main CV site configuration
- `linktree-site.conf` - Linktree site configuration

After changes, restart services:
```bash
docker-compose restart
```

### Traefik Configuration

Edit Traefik configs in `configs/traefik/`:
- `traefik.yml` - Main Traefik configuration
- `dynamic.yml` - Dynamic routing rules

## Building Images

### Build Nginx Image

```bash
docker build -f Dockerfile.nginx -t cv-nginx .
```

### Build CV Compiler Image

```bash
docker build -f Dockerfile.cv -t cv-builder .
```

## Volume Mounts

The `docker-compose.yml` uses volume mounts for:
- **Static files**: Mounted from repository root
- **Configs**: Nginx and Traefik configurations
- **Docker socket**: For Traefik service discovery

## Networking

All services are on the `cv-network` bridge network, allowing:
- Service discovery via Traefik
- Internal communication
- Isolated network environment

## Health Checks

Services include health check endpoints:
- **CV Site**: `/health`
- **Nginx Status**: `/nginx_status` (internal only)

Check health:
```bash
curl http://localhost:8080/health
```

## Logs

### View All Logs

```bash
docker-compose logs -f
```

### View Specific Service Logs

```bash
docker-compose logs -f cv-site
docker-compose logs -f linktree-site
docker-compose logs -f traefik
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
# Windows
netstat -ano | findstr :8080

# Change port in docker-compose.yml
ports:
  - "8082:80"  # Use different host port
```

### Permission Issues

```bash
# Ensure Docker has permissions
# Linux: Add user to docker group
sudo usermod -aG docker $USER
```

### Container Won't Start

```bash
# Check logs
docker-compose logs cv-site

# Verify configs are valid
docker-compose config
```

## Production Considerations

For production deployment:

1. **Use specific image tags** instead of `latest`
2. **Set resource limits** in docker-compose.yml
3. **Enable HTTPS** via Traefik with Let's Encrypt
4. **Use secrets** for sensitive configuration
5. **Set up monitoring** (Prometheus, Grafana)
6. **Configure backups** for persistent data

## Environment Variables

You can customize deployment with environment variables:

```bash
# Create .env file
NGINX_WORKER_PROCESSES=4
TRAEFIK_DASHBOARD=true

# Use in docker-compose.yml
environment:
  - NGINX_WORKER_PROCESSES=${NGINX_WORKER_PROCESSES}
```

## Next Steps

- [Kubernetes Deployment](./kubernetes.md) - Deploy to Kubernetes
- [GitHub Pages](./github-pages.md) - Alternative deployment method
- [Infrastructure Docs](../infrastructure/docker.md) - Detailed Docker documentation
