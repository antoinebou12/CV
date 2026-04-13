# CV/Resume Website

A comprehensive, multilingual CV/resume website with automated LaTeX compilation, Docker support, and multiple deployment options.

## 🚀 Features

- **Multilingual Support**: English and French versions of both HTML and PDF CVs
- **Automated Builds**: Python-based build script with Docker for LaTeX compilation
- **Multiple Deployment Options**: GitHub Pages, Docker, Kubernetes
- **Modern Stack**: HTML5, LaTeX (XeLaTeX), Docker, Kubernetes, GitHub Actions
- **Linktree Integration**: Social links page included
- **CI/CD**: Automated compilation and deployment via GitHub Actions

## 📋 Quick Start

### Prerequisites

- Python 3.8+ (for build script)
- Docker (for LaTeX compilation)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CV
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Build CV PDFs**
   ```bash
   # Build English CV
   python build_cv.py build --language en

   # Build French CV
   python build_cv.py build --language fr

   # Build both
   python build_cv.py build --all
   ```

4. **View locally**
   ```bash
   # Simple HTTP server
   python -m http.server 8000
   # Then visit http://localhost:8000
   ```

## 📁 Project Structure

```
CV/
├── index-en.html          # English HTML resume
├── index-fr.html          # French HTML resume
├── index.html             # Default redirect
├── build_cv.py            # CV build script
├── requirements.txt       # Python dependencies
├── Dockerfile.cv          # LaTeX compilation Docker image
├── docker-compose.yml     # Docker Compose configuration
├── cv-en/                 # English LaTeX CV source
│   ├── resume.tex        # Main CV file
│   ├── latex/            # CV sections
│   │   ├── summary.tex
│   │   ├── experience.tex
│   │   ├── education.tex
│   │   ├── projects.tex
│   │   ├── skills.tex
│   │   └── ...
│   ├── fonts/            # Custom fonts
│   └── resume.pdf        # Compiled PDF (generated)
├── cv-fr/                 # French LaTeX CV source (same structure)
├── linktree/              # Linktree website
├── papers/                # Publications and papers
├── configs/               # Configuration files (nginx, traefik, etc.)
├── k8s/                   # Kubernetes manifests
├── helm/                  # Helm charts
├── docs/                  # Documentation
└── .github/              # GitHub Actions workflows
```

## 🛠️ Usage

### Building CVs

The `build_cv.py` script provides a convenient way to compile LaTeX CVs using Docker:

```bash
# Basic usage
python build_cv.py build --language en

# Build both languages
python build_cv.py build --all

# Build in parallel (faster)
python build_cv.py build --all --parallel

# Custom output location
python build_cv.py build --language en --output ./output/cv.pdf

# Clean auxiliary files after build
python build_cv.py build --language en --clean

# Verbose output
python build_cv.py build --language en --verbose

# CI mode (plain text output)
python build_cv.py build --all --ci
```

### Available Options

- `--language, -l`: Language to build (`en` or `fr`)
- `--all`: Build both English and French CVs
- `--output, -o`: Custom output path for PDF
- `--rebuild`: Force rebuild Docker image
- `--clean`: Clean auxiliary files after compilation
- `--verbose, -v`: Verbose output
- `--move-to-root`: Move PDF to root as `cv-{lang}.pdf`
- `--parallel`: Build both languages in parallel (when using `--all`)
- `--ci`: CI/Pipeline mode (plain text output)
- `--fail-on-warnings`: Fail build if LaTeX warnings are detected
- `--show-warnings`: Always show LaTeX warnings summary

### Editing CVs

#### HTML Resumes

Edit the HTML files directly:
- `index-en.html` - English version
- `index-fr.html` - French version

#### LaTeX CVs

Edit the modular LaTeX files:
- `cv-en/resume.tex` - Main English CV file
- `cv-fr/resume.tex` - Main French CV file
- `cv-{lang}/latex/*.tex` - Individual sections

After editing, rebuild:
```bash
python build_cv.py build --language en
```

## 🚢 Deployment

### GitHub Pages (Recommended)

Automated deployment via GitHub Actions. Simply push to the main branch:

```bash
git add .
git commit -m "Update CV"
git push
```

The GitHub Actions workflow will:
1. Compile LaTeX CVs to PDF
2. Deploy HTML files to GitHub Pages

See [GitHub Pages Deployment Guide](docs/deployment/github-pages.md) for details.

### Docker

Deploy using Docker Compose:

```bash
docker-compose up -d
```

See [Docker Deployment Guide](docs/deployment/docker.md) for details.

### Kubernetes

Deploy to a Kubernetes cluster:

```bash
kubectl apply -f k8s/
```

Or using Helm:

```bash
helm install cv-stack ./helm/cv-stack
```

See [Kubernetes Deployment Guide](docs/deployment/kubernetes.md) for details.

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Setup Guide](docs/setup/README.md)** - Installation and local development setup
- **[Development Guide](docs/development/README.md)** - Development workflows and best practices
- **[Deployment Guide](docs/deployment/README.md)** - Deployment options and instructions
- **[Infrastructure Guide](docs/infrastructure/README.md)** - Docker, Kubernetes, and Nginx configuration

## 🔧 Development

### Local Development

1. **Set up environment** (see [Local Development Guide](docs/setup/local-development.md))
2. **Make changes** to HTML or LaTeX files
3. **Test locally** using a local HTTP server
4. **Rebuild PDFs** if LaTeX files changed
5. **Commit and push** changes

### GitHub Actions

The project includes automated workflows:
- **CV Compilation**: Automatically compiles LaTeX CVs on changes
- **GitHub Pages Deployment**: Automatically deploys website

See [GitHub Actions Guide](docs/development/github-actions.md) for details.

## 🎨 Customization

### Adding New Sections

1. Create a new `.tex` file in `cv-{lang}/latex/`
2. Add content to the file
3. Include it in `resume.tex`:
   ```latex
   \input{latex/new-section.tex}
   ```

### Changing Styles

- **LaTeX**: Edit `cv-{lang}/resume.tex` or the `russell.cls` class file
- **HTML**: Edit the `<style>` section in `index-{lang}.html`

### Adding Languages

1. Copy `cv-en/` to `cv-{new-lang}/`
2. Translate all `.tex` files
3. Update `build_cv.py` to support the new language
4. Create `index-{new-lang}.html`

## 🐛 Troubleshooting

### LaTeX Compilation Issues

- **Missing fonts**: Ensure fonts are in `cv-{lang}/fonts/`
- **Package errors**: Check LaTeX log file (`cv-{lang}/resume.log`)
- **Build failures**: Use `--verbose` flag for detailed output

### Docker Issues

- **Docker not running**: Start Docker daemon
- **Permission errors**: Check Docker permissions
- **Build timeouts**: Increase timeout in `build_cv.py`

### Deployment Issues

- **GitHub Pages not updating**: Check GitHub Actions workflow status
- **Docker container issues**: Check logs with `docker-compose logs`
- **Kubernetes issues**: Check pod status with `kubectl get pods`

See [Troubleshooting Guide](docs/README.md#troubleshooting) for more details.

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Portfolio**: [antoineboucher.info](https://antoineboucher.info)
- **GitHub**: [github.com/antoinebou12](https://github.com/antoinebou12)
- **LinkedIn**: [linkedin.com/in/antoineboucher12](https://linkedin.com/in/antoineboucher12)

## 🤝 Contributing

This is a personal CV/resume project. For suggestions or improvements, please open an issue or submit a pull request.

## 📝 Changelog

### Recent Updates

- ✅ CV index: Conferences section with Graphquon logos (2024 + 2025); moved out of certifications list
- ✅ Added Graphquon 2024 and 2025 conference entries
- ✅ Updated Snapchat Lens statistics (6.21M plays, 12.11M views; blog post refreshed April 2026)
- ✅ Added DasherControl project
- ✅ Updated hass-renpho with dates
- ✅ Improved build script with parallel compilation support
- ✅ Enhanced documentation structure

---

**Built with ❤️ using LaTeX, Docker, and modern web technologies**
