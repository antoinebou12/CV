# Site end-to-end test plan

1. Reuse the installed Playwright runtime. Build Hugo into a separate ignored staging directory and serve the CV and blog together.
2. Test English and French entry pages at 390, 768, and 1440 pixels, in light and dark modes. Check headings, document language, horizontal overflow, broken images, duplicate IDs, template residue, and browser exceptions. Save screenshots and structured findings.
3. Exercise search results and empty states, project filtering/reset, mobile navigation, theme switching, recipe/article links, and native disclosures.
4. Read the sitemap recursively and open every listed HTML page once on desktop. Keep an explicit discovered/visited inventory. Use E2E_LIMIT only for smoke runs; omit it for full coverage.
5. Run the same read-only checks against https://antoineboucher.info. Configure E2E_PREFIX=/CV if production is served below that prefix. Do not submit forms or follow external action links.
6. Review failures and screenshots before changing templates. Automated DOM and accessibility checks cannot establish visual correctness or complete HTML standards compliance.
7. Open every project note (`projects.spec.ts`) at 390 and 1280 pixels in light and dark, with every disclosure expanded. Check colour contrast, horizontal overflow, copy buttons that escape their code block, and text touching the edge of a box that has its own border or background. Text inside a deliberate horizontal scroller or `.sr-only` is skipped. Full-page screenshots and `project-audit.json` land in the test output folder.
8. Check the CV assets (`cv-assets.spec.ts`): technology logos come from `images/tech-icons/` and all load, the MCP chip shows the Model Context Protocol logo, the stats widgets load from `images/widgets/` after their panels open, and the idle prefetch requests them before any click.

## Spec files

| File | Covers |
| --- | --- |
| `e2e/site.spec.ts` | Entry-page matrix, search, project filters, mobile menu and theme, recipes with axe, sitemap crawl |
| `e2e/expanded.spec.ts` | CV and blog pages with every disclosure open, colour contrast, expertise domains and subcategories |
| `e2e/projects.spec.ts` | Every project note: spacing, overflow, contrast, copy buttons; `E2E_PROJECTS=a,b` limits the run, `E2E_PROJECT_SHOTS=0` skips screenshots |
| `e2e/cv-assets.spec.ts` | Local logos and stats widgets on the CV, widget prefetch |
| `e2e/hero.spec.ts` | CV hero and blog home: load timing, CLS, weight, images, structure, screenshots |
| `e2e/content.spec.ts` | Every sitemap page: repetition, residue, empty or duplicate headings, duplicate titles |

## Commands

Run from tools/ux-audit:

```powershell
node scripts/serve-e2e.mjs
# In another terminal:
$env:E2E_URL='http://127.0.0.1:8765'
npx playwright test --config playwright.e2e.config.ts
$env:E2E_URL='https://antoineboucher.info'
$env:E2E_PREFIX='/CV'
npx playwright test --config playwright.e2e.config.ts
```

Reports: e2e-report and e2e-results. Each run replaces these; copy them before running a second target when preserving evidence. The crawl is sequential to limit production load. Failure traces and screenshots are retained. Browser coverage currently uses Chromium; Firefox/WebKit require their browser binaries.

`node scripts/run-local-e2e.mjs` builds, serves and runs the suite in one step (default port 8891). Run production checks from PowerShell: Git Bash rewrites `E2E_PREFIX=/CV` into a Windows path.

Set E2E_PORT when 8765 is occupied, and set E2E_URL to the same port. E2E_CHANNEL can select an installed Chrome or Edge channel. On this Windows machine, the installed Chromium cache is at C:/Users/antoi/AppData/Local/ms-playwright; set PLAYWRIGHT_BROWSERS_PATH to that directory if the sandbox resolves a different cache. Browser and server processes must have access to the same network environment.

Analyse any run with `node scripts/analyze-results.mjs e2e-results/<run> report.md`.

## What the runs found and fixed (2026-10-27/28)

- Project notes: Tailwind's reset in the paper theme is boosted to two-ID specificity, so it zeroed the padding, margins and borders that `repository-notes.css` sets with plain classes. Project notes now get the reset at normal specificity (`head.html`); other pages keep the theme bundle. Typography-plugin rules (backticks around inline code, table cell and `dt`/`dd` spacing, link styles) carry four-ID boosts and are overridden with five.
- Project notes: link rows became badges, the mobile on-page navigation became pills, the breadcrumb no longer ends in a dangling `/`, PlantUML source blocks keep their copy button inside, and wide tables scroll or drop a column on phones.
- CV: dark-mode contrast for project notes and Snap lens links, a light tile behind brand logos in dark mode, local technology logos (Karma was a 404, MCP showed the Anthropic logo), local stats widgets (the github-readme-stats-fast deployment returns 402), Spotify preconnect and idle prefetch.
- Blog: recipe cards fill their image frame; the template-residue check ignores Hugo syntax shown inside code samples.
- Production (before deploy): recipe pages render an empty `<div aria-label>` for topics, which fails axe `aria-prohibited-attr`; the local template already emits a `<nav>` only when a post has tags.
