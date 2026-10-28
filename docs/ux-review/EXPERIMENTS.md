# UX experiments log

Evaluator frozen before changes: hard gates in `tools/ux-audit/fixtures.json` + `scripts/verify/repository-notes.test.mjs` + Playwright smoke. Scoring weights: evidence 25 · structure 20 · diagrams 20 · a11y/responsive 15 · task completion 10 · maintainability 10.

| # | Hypothesis | Edit | Gates | Score delta | Decision |
|---|------------|------|-------|-------------|----------|
| A | Shared tokens + masthead reduce CV/Hugo fragmentation | `design/tokens.json`, `sync_design_tokens.py`, wire into CV + Hugo; About nav Blog\|About\|Home; Hugo CV home link | tokens `--check`; builds green | +8 structure / +5 maintainability | **keep** |
| B | Title-first hero + install-before-arch improves first 15s | `repository-note.html` h1 before status chips; structure test | 54/54 notes tests | +6 structure | **keep** |
| C | Catalog live count + keyboard filters improve discovery | `projects/list.html` toolbar, arrow keys on filter groups | smoke catalog search pass | +5 discoverability | **keep** |
| D | Compose topology Mermaid clarifies Docker ops | `repository-runtime.html` flowchart from `services` | TCH099 `#deployment` + `.repo-topology` smoke | +8 diagrams | **keep** |
| E | Algorithm panel for simulation libs | `ipc-toolkit` profile.algorithm + runtime partial | `#algorithm` smoke | +7 evidence/structure | **keep** |
| F | Light docs header/footer contrast vs journal white-on-dark | `.repo-doc` header/footer ink overrides in `repository-notes.css` | smoke pass; axe color-contrast still mixed on chrome → documented; a11y non-contrast rules pass | +4 a11y (partial) | **keep** (chrome contrast follow-up) |
| G | Playwright harness + CI structure job prevent regressions | `tools/ux-audit/*`, quality.yml `project-docs-structure` + tokens check | smoke 7/7, a11y 2/2, notes 54/54 | +10 maintainability | **keep** |

Stopped after seven kept experiments; no revert cycle. Remaining: full axe color-contrast on mixed journal/docs chrome without disabling the rule; optional diagram split for dense Mermaid beyond default 100% viewer.
