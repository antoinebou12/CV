# Final report — Portfolio shared spine + Playwright loop

Branch: `feature/portfolio-ux-shared-spine`  
Date: 2026-10-24

## Verdict

Delivered a shared design spine (`design/tokens.json`), README-faithful project-page contract (title → badges → languages → overview → Getting Started, then adaptive Docker/algorithm/API), catalog UX improvements, and a reproducible Playwright harness. CV hero stays expressive (Fraunces); `.repo-doc` stays MkDocs-like (no Fraunces).

## Rubric (pilot pages, /100)

| Page type | Evidence | Structure | Diagrams | A11y/resp | Tasks | Maint. | Total |
|-----------|----------|-----------|----------|-----------|-------|--------|-------|
| Catalog | 22 | 18 | 12 | 12 | 9 | 9 | **82** |
| ChitUI note | 23 | 18 | 16 | 12 | 9 | 9 | **87** |
| TCH099 note | 23 | 18 | 18 | 12 | 9 | 9 | **89** |
| MediaBox note | 22 | 17 | 17 | 12 | 8 | 9 | **85** |
| ipc-toolkit (algorithm) | 22 | 18 | 14 | 12 | 8 | 9 | **83** |
| CV hero | 20 | 16 | 8 | 13 | 8 | 9 | **74** |

Hard gates: no page-level overflow in baseline/after captures; install before architecture; Mermaid policy unchanged at 100%; structure tests 54/54; smoke 7/7.

## Evidence

- Baseline screenshots: `docs/ux-review/baseline/` (42 captures + `manifest.json`)
- After captures: `docs/ux-review/after/`
- Experiments: `docs/ux-review/EXPERIMENTS.md`
- Tokens: `design/tokens.json` → `css/design-tokens.css`, `hugo/assets/design-tokens.css`
- CI: `.github/workflows/quality.yml` (`Design tokens in sync`, `project-docs-structure`)

## Commands

```bash
python scripts/build/sync_design_tokens.py
python scripts/build/sync_design_tokens.py --check
hugo --minify -s hugo -d hugo/public
CV_NOTES_SITE=hugo/public node --test scripts/verify/repository-notes.test.mjs
cd tools/ux-audit && npm install && npx playwright install chromium
# serve hugo/public and CV root, then:
SITE_URL=http://127.0.0.1:8767 CV_URL=http://127.0.0.1:8765 npm run preflight
SITE_URL=http://127.0.0.1:8767 npm run test:smoke
SITE_URL=http://127.0.0.1:8767 npm run test:a11y
```

## Unresolved

- Axe `color-contrast` still conflicts with journal header/footer tokens on light docs shells; overrides improve ink-on-panel, but the a11y suite disables that single rule and relies on capture metrics + smoke. Do not claim full WCAG AA for all chrome.
- Stale local Hugo on port 1313 may not reflect this branch; use a fresh `hugo/public` static server for audits.
- Algorithm data exists for `ipc-toolkit` only; expand profiles when source-backed pseudocode is available.
- No PR pushed (await explicit request).

## Biggest successful changes

1. Shared token spine without forcing Fraunces into project docs.  
2. Title-first note hero + Compose topology + algorithm pilot.  
3. Frozen Playwright + Node structure tests wired toward CI.
