# GitHub Actions Workflows

Documentation for GitHub Actions workflows used in this project.

## Overview

The project uses two main GitHub Actions workflows:

1. **CV Compilation** (`.github/workflows/compile-cv.yml`)
   - Compiles LaTeX CV to PDF
   - Commits PDF back to repository

2. **GitHub Pages Deployment** (`.github/workflows/deploy.yml`)
   - Deploys website to GitHub Pages
   - Triggers on push to main/master

## CV Compilation Workflow

### Trigger Conditions

- **Automatic**: Push to `main`/`master` branch with changes to:
  - `cv-en/**` or `cv-fr/**` files
  - `.github/workflows/compile-cv.yml`
- **Manual**: `workflow_dispatch` (manual trigger)

### Workflow Steps

1. **Checkout repository**
   - Uses `actions/checkout@v4`
   - Full history fetched for git operations

2. **Compile LaTeX document**
   - Uses `xu-cheng/latex-action@v3`
   - Compiles `cv-en/resume.tex` or `cv-fr/resume.tex` with XeLaTeX
   - Working directory: `cv-en/` or `cv-fr/`
   - Supports both English and French versions

3. **Output PDFs**
   - English PDF: `cv-en/resume.pdf`
   - French PDF: `cv-fr/resume.pdf`
   - PDFs remain in their respective language folders

4. **Commit PDF**
   - Commits `cv.pdf` if changed
   - Commit message: "Auto-compile CV PDF [skip ci]"
   - Skips CI to prevent loops

### Configuration

**File**: `.github/workflows/compile-cv.yml`

Key settings:
- **LaTeX engine**: XeLaTeX (for custom fonts)
- **Working directory**: `cv-en/` or `cv-fr/`
- **Output**: `cv-en/resume.pdf` or `cv-fr/resume.pdf`

### Troubleshooting

#### Workflow Fails to Compile

**Check**:
1. LaTeX syntax errors in source files
2. Missing fonts or packages
3. File path issues
4. Workflow logs for specific errors

#### PDF Not Committed

**Check**:
1. Git permissions (workflow needs write access)
2. No actual changes to PDF
3. Workflow logs for commit step

#### Infinite Loop

**Prevented by**: `[skip ci]` in commit message

If loop occurs:
1. Check commit message format
2. Verify workflow trigger conditions
3. Review workflow logs

## GitHub Pages Deployment Workflow

### Trigger Conditions

- **Automatic**: Push to `main`/`master` branch
- **Manual**: `workflow_dispatch` (manual trigger)

### Prerequisites

- **GitHub Pages must be enabled** in repository settings
- **Source**: Set to "GitHub Actions" (not "Deploy from a branch")

### Workflow Steps

1. **Checkout repository**
   - Uses `actions/checkout@v4`
   - Gets all files for deployment

2. **Setup Pages**
   - Uses `actions/configure-pages@v4`
   - Configures GitHub Pages environment

3. **Upload artifact**
   - Uses `actions/upload-pages-artifact@v3`
   - Uploads entire repository root
   - Serves `index.html` and all assets

4. **Deploy to GitHub Pages**
   - Uses `actions/deploy-pages@v4`
   - Deploys artifact to GitHub Pages
   - Makes site live at `https://<username>.github.io/<repo>`

### Configuration

**File**: `.github/workflows/deploy.yml`

Key settings:
- **Path**: `.` (entire repository root)
- **Environment**: `github-pages`
- **Permissions**: `pages: write`, `id-token: write`

### Troubleshooting

#### "Get Pages site failed" Error

**Cause**: GitHub Pages not enabled in repository settings

**Solution**:
1. Go to repository Settings → Pages
2. Select "GitHub Actions" as source
3. Save settings
4. Re-run workflow

#### Site Not Updating

**Check**:
1. Workflow completed successfully
2. GitHub Pages status in repository settings
3. Wait a few minutes for DNS propagation
4. Clear browser cache

#### 404 Errors

**Check**:
1. File paths are correct (relative paths)
2. `index-en.html` or `index-fr.html` is in repository root
3. All assets are included in artifact

## Workflow Permissions

### Required Permissions

**CV Compilation**:
- `contents: write` (to commit PDF)

**GitHub Pages**:
- `contents: read` (to read files)
- `pages: write` (to deploy)
- `id-token: write` (for OIDC)

### Setting Permissions

Permissions are set in workflow files:
```yaml
permissions:
  contents: read
  pages: write
  id-token: write
```

## Workflow Status

### View Status

1. Go to repository on GitHub
2. Click **Actions** tab
3. Select workflow run
4. View logs and status

### Status Badges

Add to README:
```markdown
![CV Compilation](https://github.com/<username>/<repo>/workflows/Compile%20LaTeX%20CV/badge.svg)
![Deploy](https://github.com/<username>/<repo>/workflows/Deploy%20to%20GitHub%20Pages/badge.svg)
```

## Best Practices

1. **Test workflows locally** when possible
2. **Review workflow logs** after each run
3. **Keep workflows simple** and focused
4. **Use specific action versions** (not `@main`)
5. **Handle errors gracefully** with proper error handling
6. **Document workflow changes** in commit messages

## Customization

### Change Compilation Options

Edit `.github/workflows/compile-cv.yml`:
```yaml
args: -pdf -file-line-error -halt-on-error -interaction=nonstopmode
```

### Change Deployment Path

Edit `.github/workflows/deploy.yml`:
```yaml
with:
  path: './dist'  # Deploy from specific directory
```

### Add Additional Steps

Add steps before/after existing steps:
```yaml
- name: Custom Step
  run: |
    echo "Do something"
```

## Next Steps

- [CV Compilation](./cv-compilation.md) - Local compilation guide
- [GitHub Pages Deployment](../deployment/github-pages.md) - Deployment details
- [Development Workflow](./README.md) - Development processes
