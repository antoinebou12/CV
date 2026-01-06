# Infrastructure Documentation

Infrastructure documentation for Docker, Kubernetes, Nginx, and related technologies used in this project.

## Overview

The CV/resume website infrastructure includes:

- **Docker**: Containerization and local development
- **Kubernetes**: Container orchestration for production
- **Nginx**: Web server for static content
- **Traefik**: Reverse proxy and load balancer

## Components

### Docker
- **Purpose**: Containerization, local development, testing
- **Files**: `Dockerfile.nginx`, `Dockerfile.cv`, `docker-compose.yml`
- **Documentation**: [Docker Setup](./docker.md)

### Kubernetes
- **Purpose**: Production deployment, scaling, orchestration
- **Files**: `k8s/*.yaml`, `helm/cv-stack/`
- **Documentation**: [Kubernetes Configuration](./kubernetes.md)

### Nginx
- **Purpose**: Web server for static files
- **Files**: `configs/nginx/*.conf`
- **Documentation**: [Nginx Configuration](./nginx.md)

### Traefik
- **Purpose**: Reverse proxy, load balancing, routing
- **Files**: `configs/traefik/*.yml`
- **Configuration**: Integrated in docker-compose.yml and k8s/

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

### Kubernetes Commands
```bash
kubectl apply -f k8s/         # Deploy all
kubectl get pods -n cv-stack  # Check pods
kubectl logs <pod> -n cv-stack # View logs
kubectl delete -f k8s/        # Remove all
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

### Kubernetes
- `k8s/namespace.yaml` - Namespace definition
- `k8s/*-deployment.yaml` - Deployment manifests
- `k8s/services.yaml` - Service definitions
- `k8s/ingress.yaml` - Ingress configuration
- `k8s/configmaps.yaml` - Configuration maps
- `k8s/volumes.yaml` - Volume definitions

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

### Kubernetes Network
- **Namespace**: `cv-stack`
- **Services**: ClusterIP (internal)
- **Ingress**: External access

## Monitoring

### Health Checks
- **CV Site**: `/health` endpoint
- **Nginx Status**: `/nginx_status` (internal)
- **Traefik Dashboard**: `/api` endpoint

### Logs
- **Docker**: `docker-compose logs`
- **Kubernetes**: `kubectl logs`
- **Nginx**: `/var/log/nginx/`

## Security

### Headers
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection

### Access Control
- Nginx status endpoints restricted
- Traefik dashboard access controlled
- Kubernetes network policies (optional)

## Next Steps

- [Docker Setup](./docker.md) - Detailed Docker documentation
- [Kubernetes Configuration](./kubernetes.md) - K8s setup
- [Nginx Configuration](./nginx.md) - Nginx setup
