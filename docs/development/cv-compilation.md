# CV Compilation Guide

Guide for compiling the LaTeX CV to PDF.

## Overview

The CV is written in LaTeX using the Russell class and compiled with XeLaTeX to support custom fonts (Roboto, FontAwesome).

## Prerequisites

- **LaTeX Distribution**: TeX Live, MiKTeX, or MacTeX
- **XeLaTeX**: Included in most distributions
- **Fonts**: Roboto and FontAwesome (included in `cv-en/fonts/` or `cv-fr/fonts/`)

## Local Compilation

### Method 1: Direct XeLaTeX

```bash
# For English CV
cd cv-en
xelatex resume.tex

# For French CV
cd cv-fr
xelatex resume.tex
```

This will generate `resume.pdf` in the respective `cv-en/` or `cv-fr/` directory.

### Method 2: Using latexmk

```bash
# For English CV
cd cv-en
latexmk -xelatex resume.tex

# For French CV
cd cv-fr
latexmk -xelatex resume.tex
```

### Method 3: Multiple Passes (for references)

```bash
# For English CV
cd cv-en
xelatex resume.tex
xelatex resume.tex  # Second pass for references

# For French CV
cd cv-fr
xelatex resume.tex
xelatex resume.tex  # Second pass for references
```

## Python Build Script (Recommended)

The easiest way to build the CV is using the Python build script:

### Installation

```bash
pip install -r requirements.txt
```

### Usage

```bash
# Build English CV (default)
python build_cv.py

# Build French CV
python build_cv.py --language fr
# or
python build_cv.py -l fr

# Rebuild Docker image and compile
python build_cv.py --rebuild

# Clean auxiliary files after compilation
python build_cv.py --clean

# Move PDF to root directory
python build_cv.py --move-to-root

# Verbose output
python build_cv.py --verbose

# Combine options
python build_cv.py -l fr --rebuild --clean --move-to-root
```

The script uses:
- **Typer** for a modern CLI interface
- **Rich** for beautiful terminal output
- **tqdm** for progress bars

## Docker Compilation (Manual)

### Build Image

```bash
# Build for English CV
docker build --build-arg LANG=en -f Dockerfile.cv -t cv-builder-en .

# Build for French CV
docker build --build-arg LANG=fr -f Dockerfile.cv -t cv-builder-fr .
```

### Compile CV

```bash
# Compile English CV and output to current directory
docker run --rm -v ${PWD}/cv-en:/cv/output cv-builder-en

# Compile French CV and output to current directory
docker run --rm -v ${PWD}/cv-fr:/cv/output cv-builder-fr
```

## File Structure

The CV is organized into language-specific folders:

```
cv-en/                  # English CV
├── resume.tex          # Main CV file
├── latex/              # CV sections (renamed from cv/ for clarity)
│   ├── summary.tex
│   ├── experience.tex
│   ├── education.tex
│   ├── skills.tex
│   ├── projects.tex
│   ├── achievements.tex
│   ├── references.bib
│   └── ...
├── fonts/              # Custom fonts
│   ├── Roboto-*.ttf
│   └── FontAwesome.ttf
├── profile.png          # Profile image
└── russell.cls         # CV class file

cv-fr/                  # French CV (same structure)
└── ...
```

## Editing the CV

### Update Experience

Edit `cv-en/latex/experience.tex` or `cv-fr/latex/experience.tex`:
```latex
\cventry
{Job Title} % Job title
{Company} % Organisation
{Location} % Location
{Date Range} % Date(s)
{
\begin{cvitems}
\item {Description of work}
\item {Another point}
\end{cvitems}
}
```

### Update Skills

Edit `cv-en/latex/skills.tex` or `cv-fr/latex/skills.tex`:
```latex
\cvskill
{Category} % Category
{Skill1, Skill2, Skill3} % Skills
```

### Update Education

Edit `cv-en/latex/education.tex` or `cv-fr/latex/education.tex`:
```latex
\cventry
{Degree} % Degree
{Institution} % Institution
{Location} % Location
{Date Range} % Date(s)
{
\begin{cvitems}
\item {Details}
\end{cvitems}
}
```

## Font Configuration

Fonts are configured in `cv-en/resume.tex` or `cv-fr/resume.tex`:
```latex
\fontdir[fonts/]
```

Ensure fonts are in `cv-en/fonts/` or `cv-fr/fonts/` directory:
- Roboto family (Regular, Bold, Light, etc.)
- FontAwesome.ttf

## Common Issues

### Font Not Found

**Error**: `Font [FontName] not found`

**Solution**:
1. Verify fonts are in `cv-en/fonts/` or `cv-fr/fonts/` directory
2. Check font paths in `resume.tex`
3. Ensure XeLaTeX is used (not pdfLaTeX)

### Missing Packages

**Error**: `File 'package.sty' not found`

**Solution**:
```bash
# TeX Live
tlmgr install <package>

# MiKTeX
miktex packages install <package>
```

### Compilation Errors

**Check**:
1. LaTeX syntax errors
2. Missing `\end{...}` tags
3. Incorrect file paths
4. Missing input files

**Debug**:
```bash
# Compile with verbose output
xelatex -interaction=nonstopmode resume.tex
```

## GitHub Actions Compilation

The CV is automatically compiled via GitHub Actions when:
- Files in `cv-en/**` or `cv-fr/**` are changed
- Workflow is manually triggered

See [GitHub Actions](./github-actions.md) for details.

## Output

After compilation:
- **English PDF**: `cv-en/resume.pdf`
- **French PDF**: `cv-fr/resume.pdf`
- **Auxiliary files**: `.aux`, `.log`, `.out` (can be deleted)

## Best Practices

1. **Test locally** before committing
2. **Keep sections modular** (separate `.tex` files)
3. **Use consistent formatting** across sections
4. **Document custom commands** or packages
5. **Version control** LaTeX source, not PDF (PDF is auto-generated)

## Troubleshooting

### PDF Not Generating

```bash
# Check for errors
xelatex -interaction=nonstopmode resume.tex 2>&1 | grep -i error

# Check log file
cat resume.log | grep -i error
```

### Font Rendering Issues

- Ensure XeLaTeX is used (not pdfLaTeX)
- Verify font files are not corrupted
- Check font paths are correct

### Long Compilation Time

- First compilation may be slow (font loading)
- Subsequent compilations should be faster
- Consider using `latexmk` for automatic multiple passes

## Next Steps

- [GitHub Actions](./github-actions.md) - Automated compilation
- [Development Workflow](./README.md) - Development processes
- [Local Development](../setup/local-development.md) - Setup guide
