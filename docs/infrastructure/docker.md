# Docker Infrastructure

Detailed documentation for Docker setup and configuration.

## Overview

Docker is used for:
- **Local development** environment
- **Testing** deployments
- **Containerization** of services
- **CI/CD** integration

## Dockerfiles

### Dockerfile.nginx

**Purpose**: Nginx web server for serving static content

**Base Image**: `nginx:alpine`

**Features**:
- Removes default Nginx config
- Copies custom Nginx configurations
- Exposes port 80
- Includes health check

**Build**:
```bash
docker build -f Dockerfile.nginx -t cv-nginx .
```

### Dockerfile.cv

**Purpose**: LaTeX CV compiler

**Base Image**: `texlive/texlive:latest`

**Features**:
- Installs Roboto fonts
- Sets working directory to `/cv`
- Compiles CV with XeLaTeX
- Outputs PDF to volume

**Build**:
```bash
docker build -f Dockerfile.cv -t cv-builder .
```

## Docker Compose

### Services

#### cv-site
- **Image**: Built from `Dockerfile.nginx`
- **Port**: 8080:80
- **Volumes**:
  - `./:/usr/share/nginx/html:ro` - Static files
  - `./configs/nginx/cv-site.conf:/etc/nginx/conf.d/cv-site.conf:ro` - Config
- **Network**: `cv-network`
- **Depends on**: `traefik`

#### linktree-site
- **Image**: Built from `Dockerfile.nginx`
- **Port**: 8081:80
- **Volumes**:
  - `./:/usr/share/nginx/html:ro` - Static files
  - `./configs/nginx/linktree-site.conf:/etc/nginx/conf.d/linktree-site.conf:ro` - Config
- **Network**: `cv-network`
- **Depends on**: `traefik`

#### traefik
- **Image**: `traefik:v2.10`
- **Ports**: 80:80, 8080:8080
- **Volumes**:
  - `/var/run/docker.sock:/var/run/docker.sock:ro` - Docker socket
  - `./configs/traefik/traefik.yml:/etc/traefik/traefik.yml:ro` - Config
  - `./configs/traefik/dynamic.yml:/etc/traefik/dynamic/dynamic.yml:ro` - Dynamic config
- **Network**: `cv-network`
- **Purpose**: Reverse proxy and routing

### Network

**Name**: `cv-network`
**Type**: Bridge
**Purpose**: Isolated network for services

### Volumes

**cv-output**: Named volume for CV compilation output (if needed)

## Usage

### Start Services

```bash
docker-compose up -d
```

### Stop Services

```bash
docker-compose down
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f cv-site
```

### Restart Services

```bash
docker-compose restart
```

### Rebuild Images

```bash
docker-compose build
docker-compose up -d
```

## Configuration

### Environment Variables

Create `.env` file:
```env
NGINX_WORKER_PROCESSES=4
TRAEFIK_DASHBOARD=true
```

### Port Customization

Edit `docker-compose.yml`:
```yaml
ports:
  - "8082:80"  # Change host port
```

### Resource Limits

Add to service definition:
```yaml
deploy:
  resources:
    limits:
      cpus: '1'
      memory: 512M
    reservations:
      cpus: '0.5'
      memory: 256M
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs cv-site

# Verify config
docker-compose config

# Check port availability
netstat -ano | findstr :8080
```

### Permission Issues

```bash
# Linux: Add user to docker group
sudo usermod -aG docker $USER

# Windows: Run Docker Desktop as administrator
```

### Volume Mount Issues

```bash
# Check volume mounts
docker-compose config

# Verify file paths
ls -la configs/nginx/
```

## Production Considerations

1. **Use specific image tags** (not `latest`)
2. **Set resource limits**
3. **Enable HTTPS** via Traefik
4. **Use secrets** for sensitive data
5. **Set up monitoring** (Prometheus, Grafana)
6. **Configure backups**
7. **Use health checks**
8. **Set restart policies**

## Next Steps

- [Kubernetes Configuration](./kubernetes.md) - K8s setup
- [Nginx Configuration](./nginx.md) - Nginx details
- [Docker Deployment](../deployment/docker.md) - Deployment guide
