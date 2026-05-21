# GitHub Actions Workflows

Documentation for GitHub Actions workflows used in this project.

## Overview

The project uses five GitHub Actions workflows:

1. **CV Compilation** (`.github/workflows/compile-cv.yml`)
   - Validates `data/cv.yaml` → LaTeX (`generate_cv.py --check`)
   - Builds CV and cover letter PDFs via Docker and `build_cv.py`
   - PDF text smoke test (`verify_cv_pdf_text.py`)
   - Commits PDFs back to the repository

2. **GitHub Pages Deployment** (`.github/workflows/deploy.yml`)
   - Deploys the static site and Hugo blog to GitHub Pages
   - `verify_deploy_build.py`, `verify_meta_descriptions.py`, **blocking** Lychee on `_site`
   - Triggers on push to `main`/`master`

3. **Link check** (`.github/workflows/link-check.yml`)
   - Runs Lychee on Hugo content, docs, static HTML, CSS, linktree, letters, papers (PR, push, weekly schedule)

4. **Quality checks** (`.github/workflows/quality.yml`)
   - Locale spellcheck: **codespell** (English paths) and **aspell-fr** (French paths) via `scripts/ci/spellcheck.py`
   - `html-validate` on static HTML entry pages
   - `validate_cv_data.py`, `check_en_fr_parity.py`, `generate_cv.py --check`

5. **Lighthouse CI** (`.github/workflows/lighthouse.yml`)
   - Builds minimal `_site`, runs Lighthouse on `/CV/index-en.html` and `/CV/index-fr.html` (warn thresholds in `lighthouserc.json`)

## CV Compilation Workflow

### Trigger Conditions

- **Automatic**: Push to `main`/`master` branch with changes to:
  - `cv-en/**` or `cv-fr/**` files
  - `data/**`, `templates/**`, `scripts/build/generate_cv.py`
  - `.github/workflows/compile-cv.yml`
- **Manual**: `workflow_dispatch` (manual trigger)

### Workflow Steps

1. **Checkout repository**
2. **Set up Python 3.14** — `requirements.txt` + `requirements-ci.txt`
3. **`generate_cv.py --check`** — `cv-en/latex/skills.tex` and `cv-fr/latex/skills.tex` must match `data/cv.yaml`
4. **Lychee** on CV and letter sources
5. **Docker `build_cv.py --all --rebuild --verbose --ci`**
6. **PDF size checks** + **`verify_cv_pdf_text.py --lang all`** (poppler `pdftotext`)
7. **Cover letters** via `texlive/texlive` + `latexmk`
8. **Commit PDFs** when changed (`[skip ci]`)

### Local parity

```powershell
pip install -r requirements.txt -r requirements-ci.txt
python scripts/build/generate_cv.py --check
python build_cv.py --all --rebuild --verbose --ci
python scripts/verify/verify_cv_pdf_text.py --lang all
```

## GitHub Pages Deployment Workflow

### Workflow Steps (quality gates before upload)

1. Checkout, Python 3.14, `pip install -r requirements-ci.txt`, sitemap unit tests
2. Hugo + Node 24 Tailwind build
3. Resume/AEO artifacts (`render_resume_md.py`, `generate_aeo_content.py`, `generate_person_jsonld.py`)
4. Assemble `_site` (static HTML, `css/`, `papers/`, CV PDFs, Hugo `blog/`)
5. Agent-ready promote + sitemap merge
6. **`verify_deploy_build.py`** (blocking)
7. **`verify_meta_descriptions.py`** (blocking)
8. **Lychee on `_site`** (advisory — `fail: false`; broken links are logged but do not block upload)
9. Upload artifact and deploy

PR/push link checks in **link-check.yml** remain blocking on source trees (no `index-en.htm`; that path is a Vercel redirect only).

## Quality Workflow

Runs on every push/PR to `main`/`master`:

| Step | Tool |
|------|------|
| Spellcheck | `scripts/ci/spellcheck.py` — EN: codespell + `.codespell-ignore-words`; FR: aspell + `.aspell.fr.pws` (French paths are not run through codespell) |
| HTML validate | `html-validate --config .htmlvalidate.json` on `index-*.html`, `about-*.html`, `404.html`, `linktree/index.html` |
| AEO output | `generate_aeo_content.py --all` + `sync_index_html.py`; committed HTML must match (`git diff --exit-code`) |
| Data schema | `scripts/verify/validate_cv_data.py` |
| EN/FR parity | `scripts/verify/check_en_fr_parity.py` |
| Generated LaTeX | `scripts/build/generate_cv.py --check` |

## Lighthouse Workflow

Serves `_site` with `/CV/` prefix symlinks and audits EN/FR CV pages. Thresholds are **warnings** (not hard fails) in `lighthouserc.json` so CI stays usable while regressions are visible in artifacts.

## Data-driven CV content

| Source | Outputs |
|--------|---------|
| `data/cv.yaml` | `cv-en/latex/skills.tex`, `cv-fr/latex/skills.tex` via `python scripts/build/generate_cv.py` |
| `data/resume.en.json`, `data/resume.fr.json` | Markdown + JSON-LD (see `scripts/build/render_resume_md.py`, `scripts/build/generate_person_jsonld.py`) |
| `index-en.html`, `index-fr.html` | Hand-maintained; shared styles in `css/cv-main.css`, `css/cv-print.css` |

After editing `data/cv.yaml`, run `python scripts/build/generate_cv.py` and commit generated `.tex` files.

## Local smoke test

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\test-pipeline-local.ps1
```

Optional `-SkipCompile` for deploy-only. The script runs sitemap tests, Hugo build, `_site` assembly, `verify_deploy_build.py`, `verify_meta_descriptions.py`, parity/validate/generate checks, and optional Docker compile + PDF text verification.

## Pre-commit

```bash
pip install pre-commit
pre-commit install
```

Hooks: locale spellcheck (`scripts/ci/spellcheck.py`), `validate_cv_data.py`, `generate_cv.py --check`, `check_en_fr_parity.py` (on relevant file changes).

## Workflow Permissions

**CV Compilation**: `contents: write`

**GitHub Pages**: `contents: read`, `pages: write`, `id-token: write`

**Quality / Link check / Lighthouse**: `contents: read`

## Next Steps

- [CV Compilation](./cv-compilation.md)
- [GitHub Pages Deployment](../deployment/github-pages.md)
- [Development Workflow](./README.md)
