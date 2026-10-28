# UX baseline — Portfolio shared spine

Recorded: 2026-10-24  
Branch: `feature/portfolio-ux-shared-spine`  
Repo: `antoinebou12/CV` (`d:\Code\cv`)

## Source map

| Public route | Source | Build |
|--------------|--------|-------|
| `/` / `index-en.html` | Static CV + `css/cv-*.css` | Deploy copies root HTML; no Hugo |
| `/blog/` | `hugo/` Paper theme | `hugo --minify -s hugo -d _site/blog` |
| `/blog/projects/` | `hugo/layouts/projects/list.html` | Same Hugo build |
| `/blog/projects/notes/<slug>/` | `repository-note` shortcode + `hugo/data/repository_*.json` | Same Hugo build |

**Not used:** `antoinebou12/blog` HB Stack; standalone ChitUI HTML prototype (reference only).

## Shared vs separate

- Before this work: CV hero (Fraunces/editorial) and Hugo journal/docs shells had no shared token file.
- Target: `design/tokens.json` → `css/design-tokens.css` + `hugo/assets/design-tokens.css` (spine focus/accent/spacing). Hero remains expressive; `.repo-doc` stays system UI (no Fraunces).

## Fixture matrix (real routes)

| Surface | EN path (local Hugo base `/blog/`) |
|---------|-------------------------------------|
| CV hero | `/index-en.html` (static server at repo root) |
| Catalog | `/blog/projects/` |
| App + Docker | `/blog/projects/notes/chitui/` |
| API + Compose | `/blog/projects/notes/tch099/` |
| Infra | `/blog/projects/notes/mediaboxdockercompose/` |
| Algorithm pilot | `/blog/projects/notes/ipc-toolkit/` |
| Journal article | first available `posts/` single |

Viewports: 390 / 768 / 1440. Themes: light + dark (Hugo); CV is light editorial.

## Confirmed defects (pre-change)

1. No `design/tokens.json` or shared focus contract across CV and Hugo.
2. Status badges precede `h1` visually (acceptable as metadata; title must remain primary).
3. Docker deployment is tabular only — no Compose topology Mermaid from services.
4. `algorithm` profile key unused (zero repositories).
5. `scripts/verify/repository-notes.test.mjs` not wired into CI.
6. No Playwright UX audit harness under `tools/ux-audit/`.
7. CV index nav intentionally Blog-only (AGENTS.md); About pages should use Blog | About | Home.

## Screenshot protocol

Baseline captures land in `docs/ux-review/baseline/` via `tools/ux-audit` (`PHASE=baseline npm run capture`). Golden Playwright snapshots stay separate under `tools/ux-audit/test-results` / snapshot dirs.
