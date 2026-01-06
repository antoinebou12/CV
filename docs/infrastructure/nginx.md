# Nginx Configuration

Detailed documentation for Nginx configuration and setup.

## Overview

Nginx is used as the web server for serving static content (HTML, CSS, JS, images, PDFs).

## Configuration Files

### CV Site Configuration

**File**: `configs/nginx/cv-site.conf`

**Purpose**: Main resume website server configuration

**Key Features**:
- Serves root directory (`/usr/share/nginx/html`)
- Gzip compression enabled
- Security headers configured
- Static asset caching (1 year)
- Health check endpoint (`/health`)
- Nginx status endpoint (`/nginx_status`)

### Linktree Site Configuration

**File**: `configs/nginx/linktree-site.conf`

**Purpose**: Linktree website server configuration

**Key Features**:
- Serves `linktree/` directory
- Similar configuration to CV site
- Path-based routing

## Configuration Details

### Server Block

```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;
}
```

### Gzip Compression

```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript 
           application/javascript application/xml+rss application/json;
```

### Security Headers

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
```

### Static Asset Caching

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### Health Check

```nginx
location /health {
    access_log off;
    return 200 "healthy\n";
    add_header Content-Type text/plain;
}
```

### Nginx Status

```nginx
location /nginx_status {
    stub_status on;
    access_log off;
    allow 127.0.0.1;
    allow 172.16.0.0/12;  # Docker network
    allow 10.0.0.0/8;     # Kubernetes network
    deny all;
}
```

## Customization

### Change Root Directory

Edit configuration file:
```nginx
root /custom/path/to/html;
```

### Add Custom Headers

```nginx
add_header Custom-Header "value" always;
```

### Modify Cache Settings

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
    expires 30d;  # Change cache duration
    add_header Cache-Control "public";
}
```

### Add Redirects

```nginx
location /old-path {
    return 301 /new-path;
}
```

## Testing Configuration

### Test Nginx Config

```bash
# Docker
docker exec <container> nginx -t

# Kubernetes
kubectl exec <pod-name> -n cv-stack -- nginx -t

# Local
nginx -t
```

### Reload Configuration

```bash
# Docker
docker exec <container> nginx -s reload

# Kubernetes
kubectl exec <pod-name> -n cv-stack -- nginx -s reload

# Local
nginx -s reload
```

## Logs

### Access Logs

**Location**: `/var/log/nginx/cv-site-access.log`

**Format**: Combined log format

**View**:
```bash
# Docker
docker exec <container> tail -f /var/log/nginx/cv-site-access.log

# Kubernetes
kubectl logs <pod-name> -n cv-stack | grep access
```

### Error Logs

**Location**: `/var/log/nginx/cv-site-error.log`

**Level**: Warning and above

**View**:
```bash
# Docker
docker exec <container> tail -f /var/log/nginx/cv-site-error.log

# Kubernetes
kubectl logs <pod-name> -n cv-stack | grep error
```

## Performance Tuning

### Worker Processes

```nginx
worker_processes auto;
worker_connections 1024;
```

### Keepalive

```nginx
keepalive_timeout 65;
keepalive_requests 100;
```

### Buffer Sizes

```nginx
client_body_buffer_size 128k;
client_max_body_size 10m;
client_header_buffer_size 1k;
large_client_header_buffers 4 4k;
```

## Security

### Hide Nginx Version

```nginx
server_tokens off;
```

### Restrict Access

```nginx
location /admin {
    allow 192.168.1.0/24;
    deny all;
}
```

### Rate Limiting

```nginx
limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;

location / {
    limit_req zone=one burst=5;
}
```

## Troubleshooting

### 403 Forbidden

**Check**:
1. File permissions
2. Root directory path
3. Index file exists

### 404 Not Found

**Check**:
1. File paths are correct
2. Root directory is correct
3. try_files directive

### 502 Bad Gateway

**Check**:
1. Upstream service is running
2. Network connectivity
3. Service endpoints

### Configuration Not Loading

**Check**:
1. Config file syntax (`nginx -t`)
2. File is in correct location
3. Volume mounts (Docker/K8s)

## Best Practices

1. **Test config** before applying
2. **Use relative paths** where possible
3. **Enable gzip** for text files
4. **Set cache headers** appropriately
5. **Monitor logs** regularly
6. **Keep configs simple** and maintainable
7. **Document custom rules**
8. **Use health checks** for monitoring

## Next Steps

- [Docker Setup](./docker.md) - Docker integration
- [Kubernetes Configuration](./kubernetes.md) - K8s integration
- [Infrastructure Overview](./README.md) - Infrastructure docs
