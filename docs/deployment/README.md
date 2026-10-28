# Deployment Guide

This section covers deploying the CV/resume website to various platforms and environments.

## Deployment Options

### 1. GitHub Pages (Recommended)
Automated deployment via GitHub Actions. See [GitHub Pages Deployment](./github-pages.md).

**Best for**: Public hosting, automatic updates, zero infrastructure cost

### 2. Docker
Deploy using Docker Compose for local or server deployment. See [Docker Deployment](./docker.md).

**Best for**: Local testing, self-hosting, containerized environments

## Quick Comparison

| Method | Setup Complexity | Cost | Automation | Best For |
|--------|-----------------|------|------------|----------|
| GitHub Pages | Low | Free | Full | Public websites |
| Docker | Medium | Low | Manual | Self-hosting |

## Prerequisites

Before deploying, ensure:
- ✅ All files are committed to Git
- ✅ GitHub Pages is enabled (for GitHub Pages deployment)
- ✅ Docker is installed (for Docker deployment)

## Deployment Workflow

1. **Make changes** to website files
2. **Test locally** (see [Local Development](../setup/local-development.md))
3. **Commit and push** to repository
4. **Monitor deployment** (GitHub Actions or deployment logs)
5. **Verify** the deployed site

## Post-Deployment

After deployment:
- ✅ Verify website loads correctly
- ✅ Check all links work
- ✅ Test on mobile devices
- ✅ Verify CV PDF is accessible
- ✅ Check GitHub Pages status (if applicable)

## Troubleshooting

### GitHub Pages Not Updating
- Check GitHub Actions workflow status
- Verify Pages is enabled in repository settings
- Check workflow logs for errors

### Docker Container Issues
- Check container logs: `docker-compose logs`
- Verify ports are not in use
- Check Docker daemon is running

## Next Steps

- [GitHub Pages](./github-pages.md) - Automated GitHub Pages deployment
- [Docker](./docker.md) - Docker-based deployment
