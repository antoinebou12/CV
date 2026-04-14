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

### Hugo blog (navigation and header)

The [`hugo/`](../../hugo/) site uses a customized Paper theme header (menus, language switcher, mobile drawer, dark mode). See **[Hugo navigation](./hugo-navigation.md)** for where to edit config, i18n, and behavior.

**Posts with images (page bundles):** Use a folder per post, e.g. `hugo/content/posts/<slug>/index.md`, and put assets in `hugo/content/posts/<slug>/images/`. Reference them in Markdown as `images/<file>.png`. In front matter, set `images:` to a list (first entry is used as the featured thumbnail in list views; see `hugo/layouts/partials/featured-image-resource.html`). Run `hugo` or `hugo --minify` from `hugo/` to confirm the site builds.

**Theme CSS (Tailwind):** After editing [`hugo/themes/paper/assets/app.css`](../../hugo/themes/paper/assets/app.css) or templates under `hugo/layouts/`, rebuild the compiled bundle so new utility classes are included: from [`hugo/`](../../hugo/), run `npm ci` then `npm run build:css` (writes `themes/paper/assets/main.css`). The lockfile is [`hugo/package-lock.json`](../../hugo/package-lock.json) in the main repo (the Paper theme is a submodule). GitHub Actions runs this before `hugo` on deploy.

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
- ✅ Test on multiple browsers (Chrome, Firefox, Safari, Edge)
- ✅ Validate HTML before committing (use W3C validator)
- ✅ Keep CSS organized and maintainable
- ✅ Ensure mobile responsiveness
- ✅ Test all links and interactive elements
- ✅ Maintain consistency between English and French versions

### LaTeX Development
- ✅ Use consistent formatting and style
- ✅ Keep sections modular (separate `.tex` files)
- ✅ Test compilation before committing
- ✅ Document custom commands or packages
- ✅ Keep font paths relative
- ✅ Use meaningful variable names
- ✅ Comment complex LaTeX code
- ✅ Maintain consistent date formats
- ✅ Keep both language versions in sync

### Git Workflow
- ✅ Write clear, descriptive commit messages
- ✅ Test changes locally before pushing
- ✅ Review GitHub Actions results after pushing
- ✅ Keep `main` branch deployable at all times
- ✅ Use feature branches for major changes
- ✅ Squash commits when merging
- ✅ Tag releases for important milestones

### Build Script Usage
- ✅ Always test builds locally before pushing
- ✅ Use `--verbose` flag when debugging
- ✅ Use `--clean` flag to remove auxiliary files
- ✅ Use `--all --parallel` for faster builds
- ✅ Check build statistics after compilation
- ✅ Review LaTeX warnings and fix when possible

## Testing

### Local Testing

**HTML Testing:**
- Test in multiple browsers (Chrome, Firefox, Safari, Edge)
- Verify all links work (internal and external)
- Check mobile responsiveness (use browser dev tools)
- Test print stylesheet
- Validate HTML using W3C validator
- Check accessibility (screen readers, keyboard navigation)

**LaTeX Testing:**
- Compile locally before committing
- Check for LaTeX warnings and errors
- Verify PDF output looks correct
- Test both English and French versions
- Check page breaks and formatting
- Verify all fonts render correctly

**Build Script Testing:**
```bash
# Test single language
python build_cv.py build --language en --verbose

# Test both languages
python build_cv.py build --all --verbose

# Test with warnings
python build_cv.py build --all --show-warnings
```

### Automated Testing

**GitHub Actions:**
- CV compilation runs automatically on changes to `cv-*/**`
- Website deployment runs automatically on push to `main`
- Check workflow status in GitHub Actions tab
- Review workflow logs for errors
- Verify PDFs are generated correctly
- Check deployment status

**CI/CD Pipeline:**
1. Push changes to repository
2. GitHub Actions triggers automatically
3. CV compilation runs (if LaTeX files changed)
4. Website deployment runs (if HTML files changed)
5. Verify deployment in browser

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
