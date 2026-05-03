## Learned User Preferences

- For French cover letters, prefer a natural, direct, human register over stiff or AI-sounding prose.
- Structure cover letters with an early value or role hook, concrete proof and metrics, and optional short employer-specific tailoring; complement the CV instead of repeating it as a credential list.
- Position the profile around **platform and graphics** (header `\position` and letters: e.g. English “Software Engineer --- Platform and graphics”, French “Ingénieur logiciel --- Plateforme et infographie”); keep breadth (backend, security, cloud, teaching, open source) in body copy without leading with a long CI/CD tool chain.
- When mentioning teaching, lead with the role or outcome and put course identifiers such as LOG8100 in parentheses rather than opening with the course code alone.
- When merging user-supplied French prose into LaTeX, keep tailoring macros (`\RecipientName`, `\RoleTitle`, `\WhyCompany`, `\CompanyName`, `\LetterSubject` where used) and fix typography (spaces around names like uml-mcp, hyphenation, no duplicated opening hooks).

## Learned Workspace Facts

- **LaTeX CVs**: Main files are `cv-en/resume.tex` and `cv-fr/resume.tex` (Russell class in each tree’s `russell.cls`, fonts under `cv-en/fonts/` and `cv-fr/fonts/` with `\fontdir[fonts/]` in those resumes). Section inputs live under `cv-en/latex/` and `cv-fr/latex/`. Detailed compile options: `docs/development/cv-compilation.md`.
- **CV build (Docker)**: From repo root, `python build_cv.py build -l en` or `-l fr`, or `build --all` (optional `--rebuild`, `--clean`, `--move-to-root`, `--parallel`). Requires Docker for that path; local XeLaTeX is `cd cv-en` or `cv-fr` then `latexmk -xelatex resume.tex` or `xelatex resume.tex` (often two passes for references).
- **Cover letters**: `letters/en/cover-letter.tex` and `letters/fr/cover-letter.tex` use `\documentclass[11pt, a4paper]{../../cv-en/russell}` and `../../cv-fr/russell` respectively; `\fontdir[../../cv-en/fonts/]` or `\fontdir[../../cv-fr/fonts/]`. File headers document PowerShell: `Set-Location letters/en` or `letters/fr`, then `latexmk -xelatex -interaction=nonstopmode cover-letter.tex` (add `-halt-on-error` if desired). Letter sources do not use a bibliography; no biber step is required for the current templates.
- **Letter tailoring**: `\RecipientName`, `\CompanyName`, `\LetterSubject`, `\RoleTitle`; optional `\WhyCompany` (empty omits that paragraph via `\ifdefempty`).
- **Russell letter title**: `\makelettertitle` fails if `\recipient`’s second argument is empty; the repo uses `\recipient{\RecipientName}{\ifdefempty{\CompanyName}{\vphantom{A}}{\CompanyName}}` so the address line is never an empty break.
- **Static HTML CV**: Public entry points at repo root include `index-en.html`, `index-fr.html`, and `index.html` (redirect). Social links page: `linktree/index.html`.
- **Hugo site**: Portfolio and posts live under `hugo/` (navigation and setup: `docs/development/hugo-navigation.md`, `docs/README.md`).
- **Agent-ready (robots, `.well-known`, Cloudflare proxy)**: Source under `hugo/static/` plus deploy promote in `.github/workflows/deploy.yml`; Cloudflare orange-cloud cannot use `hugo/static/_headers` — see `docs/development/agent-ready-baseline.md`. After deploy, run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\verify-agent-ready-production.ps1` against the public URL (pass **`-SitePrefix /CV`** when checks must follow URLs under `https://antoineboucher.info/CV/...`).
- **Root sitemap + Hugo SEO in CI**: Root `sitemap.xml` merges the Hugo sitemap with static CV entry pages via `scripts/merge_root_sitemap.py` in `.github/workflows/deploy.yml`. The Hugo build step sets **`HUGO_ENV=production`** so canonical, Open Graph, and Twitter metadata are emitted.
- **Continual-learning hook state**: `.cursor/hooks/state/continual-learning.json` and `.cursor/hooks/state/continual-learning-index.json`.
