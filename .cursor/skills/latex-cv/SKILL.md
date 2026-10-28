---
name: latex-cv
description: >-
  Edits and builds the two-page XeLaTeX resume in English and French. Use
  when changing cv-en, cv-fr, russell.cls, experience, education, skills,
  certifications, the header date, or when the user asks for the PDF CV.
---

# LaTeX CV

English source is `cv-en/resume.tex`. French is `cv-fr/resume.tex`. Both use Russell (`russell.cls`) and XeLaTeX. Fonts sit in `cv-en/fonts/` and `cv-fr/fonts/`. Sections are `cv-en/latex/` and `cv-fr/latex/`.

Cover letters are separate: `letters/en/cover-letter.tex` and `letters/fr/cover-letter.tex`. Do not copy letter PDFs into the site.

## Page budget

Both PDFs stay **exactly two pages**.

`resume.tex` includes summary, skills, experience, and education. Leave projects, languages, and interests commented out. Selected projects stay on the HTML CV.

Header date is `\cvFooterDate` passed as the center footer argument. The left and right footer arguments stay empty (no page numbers, no “Page X of Y”).

If a build is not two pages, shorten the longest experience bullets. Do not drop employer, role, place, or dates. Do not drop numbers already in the bullets (pipelines, risks, image counts). Do not turn projects back on.

## What goes where

| Fact | Edit |
| --- | --- |
| Skill rows and certifications | `data/cv.yaml`, then `python scripts/build/generate_cv.py`. Do not hand-edit `skills.tex` except to pull a generated diff back into the template |
| Experience, education, summary | The `.tex` twins by hand, and the matching HTML (`index-en.html` / `index-fr.html`) when the public page should match. Machine-readable copy starts in `data/resume.en.json` and `data/resume.fr.json` |
| Header name, phone, links | `resume.tex` |
| Label column width, section color, entry spacing | `russell.cls` in the language you are fixing; keep EN and FR class behavior aligned |

Position, in `\position` and in letters:

- English: `Software Engineer --- Platform and graphics`
- French: `Ingénieur logiciel --- Plateforme et infographie`

Teaching lines lead with the role. Course codes such as LOG8100 go in parentheses, not at the start of the line.

Experience bullets are outcomes. Do not add a Technical Skills line or a Soft Skills line under a job; those rows belong in skills. Do not import extra certifications (Udemy CLF-C02, a second GDPR line, or a second copy of each Cloud Quest track). HTML may keep Sentry and MCP; `skills.tex` does not.

Certifications stay one compact Cloud Quest cluster inside the skills certifications row. Security and certifications must stay inside the `cvskills` label column. No standalone “API REST” row.

`\hyphenation{observability}` in `resume.tex` is intentional. Do not remove it.

## Build

```bash
python build_cv.py build --all
```

One language: `python build_cv.py build -l en` or `-l fr`. Docker is the script’s compiler. A machine with XeLaTeX can also run `latexmk -xelatex resume.tex` inside `cv-en` or `cv-fr`.

After a successful build, confirm the script’s page count is 2 for each language. When `pdftotext` is on `PATH`:

```bash
python scripts/verify/verify_cv_pdf_text.py --lang all
```

`python scripts/build/generate_cv.py --check` must pass after any `cv.yaml` skill change.

## Parity

Change both languages in the same task unless the user asked for one. French typography: no duplicated opening hooks, no space missing around names such as uml-mcp. Thesis lines use `Thesis:` / `Mémoire :`, a comma, and `with` / `avec` for friction and plural textures.

Escapes that break XeLaTeX if missed: `\#` in C#, `\&` in URLs, `~` for a non-breaking space before a course code (`LOG~8100`).
