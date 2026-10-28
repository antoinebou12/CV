---
name: project-docs
description: Use when editing Hugo project pages, the projects catalog, repository-note templates, repository_profiles, repository_api_guides, or project documentation CSS/JS. Enforces the ChitUI-preview documentation shell, verified-content rules, and section order.
---

# Project documentation pages

## When to use

Editing `hugo/layouts/shortcodes/repository-note.html`, project partials, `hugo/layouts/projects/list.html`, `hugo/assets/repository-notes.css`, `hugo/assets/projects-directory.css`, `hugo/data/repository_*.json`, or bilingual `content/projects/notes/**`.

## Visual system

- Scope the shell under `.repo-doc` (notes) and `.repo-directory` (catalog). Blog posts keep the journal theme.
- Tokens and components are in root `DESIGN.md`. Prefer a MkDocs-like reading layout: TOC + ~65ch content, hairline rules, definition lists for features, Mermaid behind `<details>`.
- Dark defaults: `--bg #0a1019`, `--panel #111c2a`, `--text #edf4fb`, `--muted #c2d0de`, `--accent #6fdbd0`. Light muted stays ≥4.5:1 on `--bg`.
- Set `color` on every text node from `--text` or `--muted`. Never rely on inherited prose colors.
- Use Fraunces only for project and catalog titles, system UI for body text, and monospace for commands. Do not dump language-bar label text into the track.

## Required section order

1. Title (one `h1`, first in the hero panel)
2. Status chips (kind / fork / API / Docker — metadata, not display type)
3. Technology badges
4. Language percentages (Linguist bytes)
5. Introduction / overview
6. Getting Started (`#installation`)
7. README excerpts (`#reader-guide`)
8. Features
9. Architecture (`#architecture`) — Context / Components / Deployment when data exists; Mermaid at 100%
10. Optional workflow (`#workflow`) only if `repository_profiles.workflow` exists
11. API (`#api-contract`) only if an API guide exists
12. Deployment when Compose/Docker evidence exists (table + topology Mermaid from `services`)
13. Algorithm (`#algorithm`) only if `repository_profiles.algorithm` exists
14. Code structure, limits, sources

Keep test anchors: `languages`, `overview`, `installation`, `architecture`, `api-contract`, `code-structure`, `constraints`, `source-files`.

## Content rules

- Follow the repository README structure; enrich with source-verified details.
- Omit empty API, algorithm, or workflow sections.
- Permission claims name the handler check. README role labels alone are not enough.
- Local-dev passwords stay labeled as samples.
- `depends_on` is startup order, not readiness.
- Do not invent language percentages, ports, benchmarks, or live demos.

## Data sources

- `repository_notes.json` — intro, parts, nodes, edges, limits, sources
- `repository_analysis.json` — languages, installation, types
- `repository_handbooks.json` — README chapters
- `repository_api_guides.json` — endpoints and access wording
- `repository_profiles.json` — badges, Compose services, Docker commands, workflow steps

## Verification

- Hugo build succeeds.
- Light and dark: readable text, no page-level horizontal overflow at 390 / 768 / 1280.
- Getting Started appears above architecture; diagrams start at 100% and provide Fit, zoom, fullscreen, and SVG export controls.
- Catalog search and language filters work without a search service.
- Run `CV_NOTES_SITE=hugo/public node --test scripts/verify/repository-notes.test.mjs` after a local Hugo build when changing structure.
