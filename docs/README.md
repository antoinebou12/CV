# Documentation

Welcome to the CV/Resume website documentation. This folder contains comprehensive guides for setup, deployment, development, and infrastructure.

## 📚 Documentation Index

### [Setup](./setup/README.md)
Get started with the project - installation, requirements, and local development setup.

- [Local Development](./setup/local-development.md) - Set up your local environment
- [Requirements](./setup/requirements.md) - System requirements and dependencies

### [Deployment](./deployment/README.md)
Deploy the CV website to various platforms and environments.

- [GitHub Pages](./deployment/github-pages.md) - Deploy to GitHub Pages
- [Docker](./deployment/docker.md) - Docker-based deployment
- [Kubernetes](./deployment/kubernetes.md) - Kubernetes deployment

### [Development](./development/README.md)
Development workflows, processes, and best practices.

- [CV Compilation](./development/cv-compilation.md) - LaTeX CV compilation process
- [GitHub Actions](./development/github-actions.md) - GitHub Actions workflows
- [Hugo blog (Paper theme)](./development/hugo-navigation.md) - Header, menus, i18n, `baseURL`, mobile menu, dark mode

### [Infrastructure](./infrastructure/README.md)
Infrastructure documentation for Docker, Kubernetes, and Nginx.

- [Docker](./infrastructure/docker.md) - Docker setup and configuration
- [Kubernetes](./infrastructure/kubernetes.md) - Kubernetes configuration
- [Nginx](./infrastructure/nginx.md) - Nginx configuration and setup

## 🚀 Quick Start

1. **Local Development**: See [Setup Guide](./setup/README.md)
2. **Deploy to GitHub Pages**: See [GitHub Pages Deployment](./deployment/github-pages.md)
3. **Compile CV**: See [CV Compilation](./development/cv-compilation.md)

## 📝 Project Structure

```
CV/
├── index-en.html      # English HTML resume
├── index-fr.html      # French HTML resume
├── index.html         # Default redirect page
├── build_cv.py        # CV build script (Python)
├── requirements.txt   # Python dependencies
├── Dockerfile.cv      # LaTeX compilation Docker image
├── docker-compose.yml # Docker Compose configuration
├── cv-en/             # English LaTeX CV source files
│   ├── resume.tex    # Main CV file
│   ├── latex/        # CV sections (modular)
│   └── fonts/        # Custom fonts
├── cv-fr/             # French LaTeX CV source files (same structure)
├── linktree/          # Linktree website
├── papers/            # Publications and research papers
├── configs/           # Configuration files (nginx, traefik, etc.)
├── k8s/               # Kubernetes manifests
├── helm/              # Helm charts
├── .github/           # GitHub Actions workflows
└── docs/              # This documentation
```

## 🛠️ Common Tasks

### Building CVs

```bash
# Build English CV
python build_cv.py build --language en

# Build French CV
python build_cv.py build --language fr

# Build both
python build_cv.py build --all

# Build in parallel (faster)
python build_cv.py build --all --parallel
```

### Local Testing

```bash
# Simple HTTP server
python -m http.server 8000

# Or with Docker
docker-compose up -d
```

### Deployment

```bash
# GitHub Pages (automatic via GitHub Actions)
git push

# Docker
docker-compose up -d

# Kubernetes
kubectl apply -f k8s/
```

## 🐛 Troubleshooting

### LaTeX Compilation Issues

**Problem**: LaTeX compilation fails
- **Solution**: Check `cv-{lang}/resume.log` for errors
- **Solution**: Use `--verbose` flag for detailed output
- **Solution**: Ensure all fonts are in `cv-{lang}/fonts/`

**Problem**: Missing packages
- **Solution**: Check LaTeX log for missing package names
- **Solution**: Add packages to `resume.tex` or Dockerfile

**Problem**: Font issues
- **Solution**: Verify fonts exist in `cv-{lang}/fonts/`
- **Solution**: Check font paths in `resume.tex`

### Docker Issues

**Problem**: Docker build fails
- **Solution**: Check Docker daemon is running
- **Solution**: Verify Dockerfile syntax
- **Solution**: Check disk space

**Problem**: Permission errors
- **Solution**: Check Docker permissions
- **Solution**: Run with appropriate user permissions

### GitHub Actions Issues

**Problem**: Workflow fails
- **Solution**: Check workflow logs in GitHub Actions tab
- **Solution**: Verify file paths are correct
- **Solution**: Check Docker is available in GitHub Actions

**Problem**: PDF not generated
- **Solution**: Check LaTeX compilation logs
- **Solution**: Verify CV source files are correct
- **Solution**: Check workflow permissions

### Deployment Issues

**Problem**: GitHub Pages not updating
- **Solution**: Check GitHub Actions workflow status
- **Solution**: Verify Pages is enabled in repository settings
- **Solution**: Check workflow logs for errors

**Problem**: Docker container won't start
- **Solution**: Check container logs: `docker-compose logs`
- **Solution**: Verify ports are not in use
- **Solution**: Check Docker daemon is running

**Problem**: Kubernetes pods not running
- **Solution**: Check pod status: `kubectl get pods -n cv-stack`
- **Solution**: View logs: `kubectl logs <pod-name> -n cv-stack`
- **Solution**: Verify ingress is configured correctly

## 📖 Additional Resources

- [LaTeX Documentation](https://www.latex-project.org/help/documentation/)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🔗 External Resources

- **Portfolio**: [antoineboucher.info](https://antoineboucher.info)
- **GitHub**: [github.com/antoinebou12](https://github.com/antoinebou12)
- **LinkedIn**: [linkedin.com/in/antoineboucher12](https://linkedin.com/in/antoineboucher12)
