# GitHub Actions Workflows

Documentation for GitHub Actions workflows used in this project.

## Overview

The project uses three GitHub Actions workflows:

1. **CV Compilation** (`.github/workflows/compile-cv.yml`)
   - Builds CV and cover letter PDFs via Docker and `build_cv.py`
   - Commits PDFs back to the repository

2. **GitHub Pages Deployment** (`.github/workflows/deploy.yml`)
   - Deploys the static site and Hugo blog to GitHub Pages
   - Triggers on push to `main`/`master`

3. **Link check** (`.github/workflows/link-check.yml`)
   - Runs Lychee on Hugo content, docs, and static HTML (PR, push, weekly schedule)

## CV Compilation Workflow

### Trigger Conditions

- **Automatic**: Push to `main`/`master` branch with changes to:
  - `cv-en/**` or `cv-fr/**` files
  - `.github/workflows/compile-cv.yml`
- **Manual**: `workflow_dispatch` (manual trigger)

### Workflow Steps

1. **Checkout repository**
   - Uses `actions/checkout@v6`
   - Full history fetched for git operations

2. **Set up Python**
   - Uses `actions/setup-python@v6` with **Python 3.14**
   - Installs dependencies from `requirements.txt` (pip cache enabled)

3. **Build PDFs**
   - Uses `docker/setup-buildx-action@v4` and `python build_cv.py --all --rebuild --verbose --ci` (XeLaTeX in Docker)
   - Cover letters: `texlive/texlive` container with `latexmk -xelatex` under `letters/en` and `letters/fr`
   - Lychee link check on CV and letter sources before build

4. **Output PDFs**
   - `cv-en/resume.pdf`, `cv-fr/resume.pdf`
   - `letters/en/cover-letter.pdf`, `letters/fr/cover-letter.pdf`

5. **Commit PDFs**
   - Commits the four PDFs when changed
   - Commit message: `Auto-compile CV and cover letter PDFs [skip ci]`
   - Skips CI to prevent loops

6. **Upload artifacts**
   - Uses `actions/upload-artifact@v7` (retention 7 days, `if: always()`)

### Configuration

**File**: `.github/workflows/compile-cv.yml`

Key settings:
- **Python**: 3.14 (CI)
- **LaTeX engine**: XeLaTeX (Docker image from `Dockerfile.cv` / TeX Live for letters)
- **Output**: `cv-en/resume.pdf`, `cv-fr/resume.pdf`, and cover letter PDFs under `letters/`

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
   - Uses `actions/checkout@v6` (recursive submodules for Hugo theme)
   - Gets all files for deployment

2. **Set up Python**
   - Uses `actions/setup-python@v6` with **Python 3.14**
   - Runs `scripts/test_merge_root_sitemap.py` before the Hugo build

3. **Setup Pages**
   - Uses `actions/configure-pages@v6`
   - Configures GitHub Pages environment

4. **Setup Hugo and Node**
   - Uses `peaceiris/actions-hugo@v3` (extended, pinned version)
   - Uses `actions/setup-node@v6` with **Node 24**; `npm ci` and `npm run build:css` in `hugo/`

5. **Prepare `_site`, build Hugo, merge sitemap, verify**
   - Copies root static files (`index.html`, assets, `linktree/`, `papers/`) into `_site/`
   - Copies committed CV PDFs into `_site/cv-en` and `_site/cv-fr`
   - Runs `hugo` with output directory `_site/blog/` and a production `baseURL` of **`https://antoineboucher.info/<repo>/blog/`** (canonical custom domain on GitHub Pages). Override with repository variable **`HUGO_BASE_URL`** if the canonical URL changes.
   - Promotes agent-ready assets; merges static URLs into root `sitemap.xml` via `scripts/merge_root_sitemap.py`
   - Validates the deploy tree with `scripts/verify_deploy_build.py` (Python 3.14)

6. **Upload artifact**
   - Uses `actions/upload-pages-artifact@v5`
   - Uploads the **`_site`** directory (not the raw repository root)
   - Published site root contains `index.html`, copied folders, and **`blog/`** (Hugo output)

7. **Deploy to GitHub Pages**
   - Uses `actions/deploy-pages@v5`
   - Deploys that artifact to GitHub Pages
   - Makes the site live at `https://<username>.github.io/<repo>` (project site)

8. **Advisory link check**
   - Lychee on `_site` after deploy (`continue-on-error: true` so publish is not blocked)

### Configuration

**File**: `.github/workflows/deploy.yml`

Key settings:
- **Python**: 3.14 (sitemap merge and deploy verification scripts)
- **Node**: 24 (Tailwind build in `hugo/`)
- **Artifact path**: `_site` (built on the runner; includes `blog/` from Hugo)
- **Hugo `baseURL`**: defaults to `https://antoineboucher.info/<repo>/blog/`; set repository variable **`HUGO_BASE_URL`** (e.g. for forks) to override
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

#### 404 Errors (e.g. `/CV/blog/`)

**Check**:
1. **Pages build type**: Repository **Settings → Pages** must use **GitHub Actions** (API: `build_type: workflow`), not **Deploy from a branch**. Branch deployment serves only files committed on `main`; the Hugo blog exists only inside the CI-built `_site/blog`, so `/blog/` 404s if Pages is still `legacy` branch mode.
2. The latest **Deploy to GitHub Pages** workflow finished successfully (including **Deploy to GitHub Pages** step).
3. The URL path matches the **exact GitHub repository name** (e.g. `https://<user>.github.io/CV/blog/` for repo `CV`).
4. Root HTML and assets are copied into `_site` in the workflow; Hugo output is under `_site/blog/`.

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

Edit `.github/workflows/compile-cv.yml` (e.g. `build_cv.py` flags, Docker image, or letter `latexmk` options).

### Change Deployment Path

Edit `.github/workflows/deploy.yml` (keep `upload-pages-artifact` in sync with wherever the workflow gathers files, currently `_site`).

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
