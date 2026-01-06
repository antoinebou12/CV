# Local Development Setup

Guide for setting up a local development environment for the CV/resume website.

## Prerequisites

- Git
- A text editor or IDE
- Web browser
- (Optional) Docker and Docker Compose
- (Optional) LaTeX distribution (for CV compilation)

## Basic Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd CV
```

### 2. View the Website Locally

#### Option A: Simple HTTP Server (Python)

```bash
# Python 3
python -m http.server 8000

# Then open http://localhost:8000
```

#### Option B: Simple HTTP Server (Node.js)

```bash
# Install http-server globally (optional)
npm install -g http-server

# Or use npx
npx http-server -p 8000

# Then open http://localhost:8000
```

#### Option C: Docker Compose

```bash
docker-compose up -d

# CV site: http://localhost:8080
# Linktree: http://localhost:8081
# Traefik dashboard: http://localhost:8080/api
```

## Editing the Resume

### HTML Resume (`index-en.html`, `index-fr.html`)

1. Open `index-en.html` (English) or `index-fr.html` (French) in your editor
2. Make changes to content, structure, or styling
3. Refresh your browser to see changes

### LaTeX CV (`cv-en/resume.tex`, `cv-fr/resume.tex`)

1. Edit LaTeX files in `cv-en/` (English) or `cv-fr/` (French) directory
2. Compile using XeLaTeX:
   ```bash
   # For English CV
   cd cv-en
   xelatex resume.tex
   
   # For French CV
   cd cv-fr
   xelatex resume.tex
   ```
3. Or use the Python build script (recommended):
   ```bash
   # Install dependencies
   pip install -r requirements.txt
   
   # Build English CV
   python build_cv.py
   
   # Build French CV
   python build_cv.py --language fr
   ```

4. Or use Docker directly:
   ```bash
   # For English CV
   docker build --build-arg LANG=en -f Dockerfile.cv -t cv-builder-en .
   docker run -v $(pwd)/cv-en:/cv/output cv-builder-en
   
   # For French CV
   docker build --build-arg LANG=fr -f Dockerfile.cv -t cv-builder-fr .
   docker run -v $(pwd)/cv-fr:/cv/output cv-builder-fr
   ```

See [CV Compilation](../development/cv-compilation.md) for detailed instructions.

## File Structure

```
CV/
├── index-en.html          # English resume website
├── index-fr.html          # French resume website
├── linktree/              # Linktree website
│   └── index.html
├── cv-en/                 # English LaTeX CV source
│   ├── resume.tex
│   ├── latex/            # CV sections (renamed from cv/ for clarity)
│   └── fonts/            # Custom fonts
├── cv-fr/                 # French LaTeX CV source (same structure)
├── papers/                # Publications
├── configs/              # Configuration files
└── docker-compose.yml    # Docker setup
```

## Development Workflow

1. **Make changes** to HTML or LaTeX files
2. **Test locally** using a local server
3. **Commit changes** to Git
4. **Push to repository** - GitHub Actions will:
   - Compile LaTeX CV to PDF
   - Deploy website to GitHub Pages

## Hot Reload (Optional)

For automatic browser refresh during development, consider:
- **Live Server** (VS Code extension)
- **BrowserSync**: `npx browser-sync start --server --files "*.html, *.css, *.js"`

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
# Windows
netstat -ano | findstr :8000

# Kill process or use different port
python -m http.server 8001
```

### LaTeX Compilation Errors
- Ensure XeLaTeX is installed
- Check font paths in `cv-en/resume.tex` or `cv-fr/resume.tex`
- Verify all required LaTeX packages are installed

## Next Steps

- [Requirements](./requirements.md) - System requirements
- [Development Workflow](../development/README.md) - Development processes
- [CV Compilation](../development/cv-compilation.md) - LaTeX compilation
