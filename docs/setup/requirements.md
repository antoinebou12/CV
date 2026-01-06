# System Requirements

System requirements and dependencies for the CV/resume website project.

## Minimum Requirements

### For Basic Website Viewing
- **Web Browser**: Modern browser (Chrome, Firefox, Safari, Edge)
- **HTTP Server**: Any simple HTTP server (Python, Node.js, or built-in)

### For Local Development
- **Git**: Version 2.0+
- **Text Editor**: Any code editor (VS Code, Sublime, Vim, etc.)
- **Web Browser**: For testing

### For LaTeX CV Compilation
- **LaTeX Distribution**: 
  - TeX Live (recommended)
  - MiKTeX (Windows)
  - MacTeX (macOS)
- **XeLaTeX**: Included in most LaTeX distributions
- **Fonts**: Roboto and FontAwesome (included in `cv-en/fonts/` or `cv-fr/fonts/`)

### For Docker Deployment
- **Docker**: Version 20.10+
- **Docker Compose**: Version 2.0+

### For Kubernetes Deployment
- **Kubernetes**: Version 1.20+
- **kubectl**: Matching Kubernetes version
- **Helm**: Version 3.0+ (optional, for Helm charts)

## Recommended Setup

### Development Machine
- **OS**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 20.04+)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Internet**: For GitHub Actions and package downloads

### CI/CD (GitHub Actions)
- **GitHub Account**: With repository access
- **GitHub Pages**: Enabled in repository settings
- **Actions**: Enabled (default)

## Software Installation

### Python (for simple HTTP server)
```bash
# Check if installed
python --version

# Install from python.org or package manager
```

### Node.js (optional, for http-server)
```bash
# Check if installed
node --version

# Install from nodejs.org or package manager
```

### Docker
- **Windows/macOS**: [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: Install via package manager
  ```bash
  # Ubuntu/Debian
  sudo apt-get update
  sudo apt-get install docker.io docker-compose
  ```

### LaTeX Distribution
- **Windows**: [MiKTeX](https://miktex.org/download)
- **macOS**: [MacTeX](https://www.tug.org/mactex/)
- **Linux**: 
  ```bash
  # Ubuntu/Debian
  sudo apt-get install texlive-xetex texlive-fonts-extra
  ```

## Font Requirements

The LaTeX CV uses custom fonts located in `cv-en/fonts/` or `cv-fr/fonts/`:
- **Roboto**: Various weights (Regular, Bold, Light, etc.)
- **FontAwesome**: Icon font

These fonts are included in the repository and don't require separate installation.

## Browser Compatibility

The website is tested and works on:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## GitHub Requirements

- **Repository**: Public or private (Pages works with both)
- **GitHub Pages**: Enabled in repository settings
- **Actions**: Enabled (default for most repositories)
- **Permissions**: Write access to repository (for PDF commits)

## Optional Tools

- **VS Code**: With LaTeX Workshop extension (for LaTeX editing)
- **Git GUI**: GitHub Desktop, SourceTree, or GitKraken
- **Docker Desktop**: For easier Docker management
- **kubectl**: For Kubernetes deployments

## Verification

### Check Python
```bash
python --version
# Should show Python 3.x.x
```

### Check Docker
```bash
docker --version
docker-compose --version
```

### Check LaTeX
```bash
xelatex --version
# Should show XeTeX version
```

### Check Git
```bash
git --version
# Should show Git version
```

## Next Steps

- [Local Development](./local-development.md) - Set up your development environment
- [Setup Overview](./README.md) - Return to setup guide
