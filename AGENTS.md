## Learned User Preferences

- For French cover letters, prefer a natural, direct, human register over stiff or AI-sounding prose.
- Structure cover letters with an early value or role hook, concrete proof and metrics, and optional short employer-specific tailoring; complement the CV instead of repeating it as a credential list.
- Position the profile around **platform and graphics** (header line and letters); keep breadth (backend, security, cloud, teaching, open source) in body copy without leading with a long CI/CD tool chain.
- When mentioning teaching, lead with the role or outcome and put course identifiers such as LOG8100 in parentheses rather than opening with the course code alone.
- When merging user-supplied French prose into LaTeX, keep tailoring macros (`\RoleTitle`, `\WhyCompany`, `\CompanyName`, `\LetterSubject` where used) and fix typography (spaces around names like uml-mcp, hyphenation, no duplicated opening hooks).

## Learned Workspace Facts

- English and French cover letters live at `letters/en/cover-letter.tex` and `letters/fr/cover-letter.tex`, using `\documentclass[11pt, a4paper]{../../cv-en/russell}` and `../../cv-fr/russell` respectively (French layout uses `\fontdir[../../cv-fr/fonts/]`).
- Typical build from headers: PowerShell `Set-Location letters/en` or `letters/fr`, then `latexmk -xelatex -interaction=nonstopmode cover-letter.tex` (variants may add `-halt-on-error`).
- The russell class `\makelettertitle` errors if `\recipient`'s second argument is empty; use `\vphantom{A}` or a conditional on `\CompanyName` so the address line is never an empty break.
- Letters support per-posting `\renewcommand` overrides for addressee, company line, role title, optional `\WhyCompany`, and French subject lines via `\lettertitle` / `\LetterSubject` as implemented in the repo.
- If French `latexmk`/biber fails locally, finishing the PDF has used copying `letters/en/cover-letter.bbl` into `letters/fr` and/or running `xelatex` twice in `letters/fr`.
- Public CV entry points include `index-en.html` and `index-fr.html` at the repository root.
- Continual-learning transcript processing state is stored at `.cursor/hooks/state/continual-learning-index.json` in this workspace.
