# Development Guide

Development workflows, processes, and best practices for the CV/resume website project.

## Overview

This project includes:
- **HTML Resume** (`index-en.html`, `index-fr.html`) - Main website (English and French versions)
- **Linktree** (`linktree/index.html`) - Social links page
- **LaTeX CV** (`cv-en/resume.tex`, `cv-fr/resume.tex`) - PDF resume source (English and French versions)

## Development Workflows

### HTML Website Development

1. **Edit files**: Modify `index-en.html` (English), `index-fr.html` (French), or `linktree/index.html`
2. **Test locally**: Use local HTTP server (see [Local Development](../setup/local-development.md))
3. **Commit changes**: `git add . && git commit -m "Update resume"`
4. **Push**: `git push` (triggers GitHub Actions)

### LaTeX CV Development

1. **Edit LaTeX files**: Modify files in `cv-en/` (English) or `cv-fr/` (French) directory
2. **Compile locally**: Use XeLaTeX or Docker
3. **Review PDF**: Check `cv.pdf` output
4. **Commit changes**: Push to trigger auto-compilation

See [CV Compilation](./cv-compilation.md) for detailed instructions.

## GitHub Actions Workflows

The project uses two main workflows:

### 1. CV Compilation Workflow
- **Trigger**: Changes to `cv-en/**` or `cv-fr/**` files
- **Action**: Compiles LaTeX to PDF
- **Output**: Commits `cv.pdf` to repository

### 2. GitHub Pages Deployment
- **Trigger**: Push to `main`/`master` branch
- **Action**: Deploys website to GitHub Pages
- **Output**: Live website at `https://<username>.github.io/<repo>`

See [GitHub Actions](./github-actions.md) for detailed documentation.

## File Structure

```
CV/
├── index-en.html          # English resume website
├── index-fr.html          # French resume website
├── linktree/              # Linktree website
│   └── index.html
├── cv-en/                 # English LaTeX CV source
│   ├── resume.tex        # Main CV file
│   ├── latex/            # CV sections (renamed from cv/ for clarity)
│   │   ├── summary.tex
│   │   ├── experience.tex
│   │   ├── education.tex
│   │   ├── projects.tex
│   │   └── ...
│   └── fonts/            # Custom fonts
├── cv-fr/                 # French LaTeX CV source (same structure)
├── papers/                # Publications
├── configs/              # Configuration files
├── k8s/                  # Kubernetes manifests
├── .github/              # GitHub Actions
│   └── workflows/
└── docs/                 # Documentation
```

## Best Practices

### HTML Development
- ✅ Keep HTML semantic and accessible
- ✅ Use relative paths for local resources
- ✅ Test on multiple browsers
- ✅ Validate HTML before committing
- ✅ Keep CSS organized and maintainable

### LaTeX Development
- ✅ Use consistent formatting
- ✅ Keep sections modular (separate `.tex` files)
- ✅ Test compilation before committing
- ✅ Document custom commands or packages
- ✅ Keep font paths relative

### Git Workflow
- ✅ Write clear commit messages
- ✅ Test changes locally before pushing
- ✅ Review GitHub Actions results
- ✅ Keep `main` branch deployable

## Testing

### Local Testing
- Test HTML in multiple browsers
- Verify all links work
- Check mobile responsiveness
- Validate LaTeX compilation

### Automated Testing
- GitHub Actions compiles CV automatically
- GitHub Actions deploys website automatically
- Check workflow status after pushing

## Debugging

### HTML Issues
- Use browser developer tools
- Check console for errors
- Validate HTML/CSS
- Test with different browsers

### LaTeX Issues
- Check compilation logs
- Verify font paths
- Check package availability
- Review LaTeX error messages

### GitHub Actions Issues
- Check workflow logs
- Verify file paths
- Check permissions
- Review workflow configuration

## Next Steps

- [CV Compilation](./cv-compilation.md) - LaTeX compilation process
- [GitHub Actions](./github-actions.md) - Workflow documentation
- [Local Development](../setup/local-development.md) - Setup guide
