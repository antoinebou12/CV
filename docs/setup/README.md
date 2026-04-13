# Setup Guide

This section covers the initial setup and installation of the CV/resume website project.

## Overview

The CV website consists of:
- **HTML Resume** (`index-en.html`, `index-fr.html`) - Main resume website (English and French versions)
- **Linktree** (`linktree/index.html`) - Social links page
- **LaTeX CV** (`cv-en/resume.tex`, `cv-fr/resume.tex`) - PDF resume source (English and French versions)

## Prerequisites

Before starting, ensure you have:

- **Python 3.8+** - For the build script
- **Docker** - For LaTeX compilation (recommended)
- **Git** - For version control
- **Text Editor** - For editing files (VS Code, Vim, etc.)

Optional but recommended:
- **LaTeX Distribution** - For local LaTeX compilation (alternative to Docker)
- **Node.js** - For alternative HTTP server

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CV
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Docker is running** (for LaTeX compilation)
   ```bash
   docker --version
   docker info
   ```

4. **Build CVs** (optional, for initial setup)
   ```bash
   python build_cv.py build --all
   ```

5. **Start local server**
   ```bash
   python -m http.server 8000
   ```
   Then visit `http://localhost:8000`

## Setup Options

### Option 1: Simple Local Server (Recommended for Quick Testing)

Use a simple HTTP server to view the website locally:

```bash
# Python 3
python -m http.server 8000

# Python 2 (if needed)
python -m SimpleHTTPServer 8000

# Node.js (with http-server)
npx http-server -p 8000

# PHP (if available)
php -S localhost:8000
```

**Pros**: Simple, no dependencies, fast startup
**Cons**: No LaTeX compilation, basic features only

### Option 2: Docker (Recommended for Full Features)

Use Docker Compose for a complete setup with Nginx and Traefik:

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

See [Docker Deployment](../deployment/docker.md) for details.

**Pros**: Full features, production-like environment, includes Nginx
**Cons**: Requires Docker, more setup

### Option 3: Kubernetes (For Production)

Deploy to a Kubernetes cluster:

```bash
# Apply manifests
kubectl apply -f k8s/

# Check status
kubectl get pods -n cv-stack

# View logs
kubectl logs -f <pod-name> -n cv-stack
```

See [Kubernetes Deployment](../deployment/kubernetes.md) for details.

**Pros**: Scalable, production-ready, cloud-native
**Cons**: Requires Kubernetes cluster, complex setup

## Initial Configuration

### 1. Verify Installation

Check that all tools are installed:

```bash
# Python
python --version  # Should be 3.8+

# Docker
docker --version
docker info

# Git
git --version
```

### 2. Test Build Script

Test the CV build script:

```bash
# Build English CV
python build_cv.py build --language en

# Check output
ls cv-en/resume.pdf
```

### 3. Verify File Structure

Ensure the project structure is correct:

```bash
# Check main files exist
ls index-en.html index-fr.html
ls cv-en/resume.tex cv-fr/resume.tex
ls build_cv.py requirements.txt
```

## Common Setup Issues

### Python Not Found

**Problem**: `python` command not found
- **Solution (Windows)**: Use `py` or `python3`
- **Solution (Linux/Mac)**: Install Python or use `python3`
- **Solution**: Add Python to PATH

### Docker Not Running

**Problem**: Docker daemon not running
- **Solution (Windows)**: Start Docker Desktop
- **Solution (Linux)**: Start Docker service: `sudo systemctl start docker`
- **Solution (Mac)**: Start Docker Desktop

### Permission Errors

**Problem**: Permission denied errors
- **Solution (Linux/Mac)**: Use `sudo` or add user to docker group
- **Solution**: Check file permissions
- **Solution**: Verify Docker permissions

### Missing Dependencies

**Problem**: Python packages not found
- **Solution**: Run `pip install -r requirements.txt`
- **Solution**: Use virtual environment: `python -m venv venv && source venv/bin/activate`
- **Solution**: Check Python version compatibility

## Next Steps

- [Local Development](./local-development.md) - Detailed local setup guide
- [Requirements](./requirements.md) - Complete system requirements
- [Development Workflow](../development/README.md) - Development processes and best practices
- [CV Compilation](../development/cv-compilation.md) - LaTeX compilation guide
