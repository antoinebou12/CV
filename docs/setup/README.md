# Setup Guide

This section covers the initial setup and installation of the CV/resume website project.

## Overview

The CV website consists of:
- **HTML Resume** (`index-en.html`, `index-fr.html`) - Main resume website (English and French versions)
- **Linktree** (`linktree/index.html`) - Social links page
- **LaTeX CV** (`cv-en/resume.tex`, `cv-fr/resume.tex`) - PDF resume source (English and French versions)

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CV
   ```

2. **Review requirements**: See [Requirements](./requirements.md)

3. **Set up local development**: See [Local Development](./local-development.md)

## Setup Options

### Option 1: Simple Local Server
Use a simple HTTP server to view the website locally:
```bash
# Python 3
python -m http.server 8000

# Node.js (with http-server)
npx http-server -p 8000
```

### Option 2: Docker
Use Docker Compose for a complete setup with Nginx and Traefik:
```bash
docker-compose up -d
```
See [Docker Deployment](../deployment/docker.md) for details.

### Option 3: Kubernetes
Deploy to a Kubernetes cluster:
```bash
kubectl apply -f k8s/
```
See [Kubernetes Deployment](../deployment/kubernetes.md) for details.

## Next Steps

- [Local Development](./local-development.md) - Detailed local setup
- [Requirements](./requirements.md) - System requirements
- [Development Workflow](../development/README.md) - Development processes
