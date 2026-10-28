# UX loop experiments

## Baseline

Captured 2026-10-24 against `_site_loop` at `http://127.0.0.1:8765`.

- Matrix: 6 routes × 3 viewports × 2 themes = 36 states
- Hard failures: 0
- Diagram initial zoom: 100% on tch099
- Screenshots: `.cursor/ux-loop/baseline/`

Measured design-system debt (not hard failures):

1. Hero canvas/paper/ink/accent duplicated as `--editorial-*` in `css/cv-editorial.css` and `--journal-*` in `hugo/assets/editorial.css` instead of consuming `--hero-*` from `design/tokens.json`.
2. Motion easings (`--butter-*`, `--editorial-ease`) are local literals, not spine tokens.
3. `butter-ignite` uses `color: transparent` for ~300ms (readable name briefly invisible).
4. Hugo `editorial.css` carries 259 `!important` overrides.


## Experiment 1: Shared hero tokens + safer butter ignite

Hypothesis: Changing CV/Hugo surface aliases to consume `--hero-*` / `--motion-*` from `design/tokens.json`, and replacing butter-ignite `color: transparent` with ink+glow, should improve design-system coherence and name readability during entrance, measured by resolved token equality and non-transparent computed name color.

Files: `design/tokens.json`, `scripts/build/sync_design_tokens.py`, `css/design-tokens.css`, `hugo/assets/design-tokens.css`, `css/cv-editorial.css`, `hugo/assets/editorial.css`

Before: duplicated oklch literals for canvas/paper/ink/accent in CV and Hugo; butter words used transparent color for ~300ms.

Checks: token sync `--check`; browser resolve `--editorial-canvas === --hero-canvas` and `--journal-canvas === --hero-canvas`; reduced-motion sets animation `none` and solid ink; Playwright matrix (structural: h1=1, no overflow); `node --test scripts/verify/repository-notes.test.mjs`; `check_en_fr_parity.py`.

Result: **kept**. Score +10 maintainability (shared spine), +3 a11y (no transparent name flash). Console ERR_CONNECTION_REFUSED/404 on CV pages are third-party/local asset noise present with the correct `_site_loop` server, not introduced by CSS.

## Experiment 2: Catalog and repo-note motion on shared tokens

Hypothesis: Changing projects-directory and repository-notes transition/animation timings to `--motion-duration-*` / `--motion-ease-*` should align Hugo motion with the CV hero curve, measured by CSS using token vars (with fallbacks) while reduced-motion still forces `animation: none` / `transition: 0s`.

Files: `hugo/assets/projects-directory.css`, `hugo/assets/repository-notes.css`

Before: hardcoded `.18s` / `.2s` / `.4s` / `.45s` easings independent of the spine.

Checks: Hugo rebuild; Playwright matrix (no overflow/h1 regressions on blog/projects/notes); reduced-motion on catalog disables rise animation; repository-notes tests + EN/FR parity.

Result: **kept**. Score +5 maintainability / motion coherence.


## Handoff notes

- Local serve: `uv python -m http.server 8765 --directory _site_loop --bind 127.0.0.1` (absolute Hugo `-d`).
- Do not use relative `-d _site_loop/blog` with `-s hugo` — it writes under `hugo/_site_loop/`.
- CV console errors in the audit script are third-party `ERR_CONNECTION_REFUSED` / asset 404s; structural gates (h1, overflow, status 200) pass.
- Not run: `verify_deploy_build.py` (would touch `docs/`); no deploy/push.
- Remaining backlog: further `!important` reduction in `editorial.css`, dark journal tokens in `tokens.json`, diagram/project-template work.


## Experiment 3: Recipes index journal header + single heading hygiene

Hypothesis: Adding a journal-intro `h1` on `/blog/recipes/` and removing duplicate markdown `#` titles on champignon should fix hard-gate heading counts (list h1=0, single h1=3), measured by Playwright visible `h1 === 1`.

Files: `hugo/layouts/_default/list.html`, `hugo/layouts/_default/single.html`, `hugo/content/recipes/champignon/index.md`, `hugo/content/recipes/champignon/index.fr.md`, `hugo/assets/editorial.css`

Before: recipes index had 0 visible h1; champignon had 3 (template + body `#` + `# Prices`).

Checks: focused audit 28 states → 0 structural fails; FR recipes + back link “Toutes les recettes”; EN/FR parity.

Result: **kept**. Score +20 structure/discoverability, +5 a11y.

## Experiment 4: Posts section title + recipe reading shell

Hypothesis: Using `.Title`/description on non-home grouped lists and recipe-specific ingredient styling should improve blog/posts identity and recipe readability without breaking h1 gates.

Files: `hugo/layouts/_default/list.html`, `hugo/assets/editorial.css`

Before: `/blog/posts/` reused home “Projects and notes.” copy; recipe lists had no distinct reading chrome.

Checks: `/blog/posts/` h1=“Posts”; recipe ingredient flex rows; audit 0 structural fails.

Result: **kept** after fixing a vertical-text regression (grid + anonymous text nodes). Re-verified ingredient line height ~51px and horizontal labels.

