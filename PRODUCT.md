# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

People opening the public project catalog and an individual project page: they need to understand what a repository does, how to start it, and where the architecture, API, and limits are documented. Antoine maintains the pages from repository READMEs and source.

## Product Purpose

The project pages are bilingual technical case studies for the public repositories. Success means a reader can say what the software does, who it is for, and how to start it, then reach source-backed architecture, permissions, and deployment without reading the repository as a raw dump.

## Positioning

Each page keeps one visual system for documentation pages, then follows that repository’s README and verified source. Sections that the repository does not have, such as an HTTP API or an algorithm walkthrough, are omitted.

## Operating Context

Pages are generated in the Hugo site under `hugo/` and published with the CV blog. English and French notes share `hugo/data/repository_notes.json`, `repository_analysis.json`, `repository_handbooks.json`, `repository_api_guides.json`, and `repository_profiles.json`. Facts that are not in those files or in a named source file are not added.

## Capabilities and Constraints

- Fixed opening order on every project page: title, technology badges, GitHub Linguist language percentages, introduction, Getting Started.
- After that, README excerpts stay in their extracted order, then features, architecture, optional workflow, API, deployment, and developer references.
- Language percentages come from measured language bytes. If GitHub reports none, the page says so.
- API permissions distinguish a check found in a handler from a role name that appears only in a README.
- Example passwords from a README stay labeled as local-development samples.
- Docker pages show services, published ports, volumes, and network mode only from Compose or the README. `depends_on` is startup order, not readiness.
- Workflow steppers and algorithm panels render only when a profile records verified steps or a verified problem statement.
- The catalog lists every repository in static HTML. Search, language filters, and sorting run in the browser without a search service.
- Inferred and still open: whether employers or collaborators are the primary audience. The page job above is taken from the requested redesign.

## Brand Commitments

Bilingual EN/FR copy. Shared spine tokens in `design/tokens.json` (focus, accent, spacing) sync into CV and Hugo; density differs by surface. Blog posts keep the journal theme (Fraunces, Open Sans, cream and teal). Project pages with `repository_note` and the projects catalog use the documentation shell from DESIGN.md (system UI, panel cards, ChitUI-preview palette; no Fraunces). Agents follow `.cursor/skills/project-docs/SKILL.md` when editing those pages. Playwright UX gates live under `tools/ux-audit/`.

## Evidence on Hand

- Repository note template: `hugo/layouts/shortcodes/repository-note.html`
- Catalog: `hugo/layouts/projects/list.html`
- Shell styles: `hugo/assets/repository-notes.css`, `hugo/assets/projects-directory.css`
- Linguist bytes and install excerpts: `hugo/data/repository_analysis.json`
- TCH099 routes and handlers inspected at commit `a7323c88b2ae6c12d89ef685c6a4cf4325218afc`, including `routes.php`, `docker-compose.yml`, and `api/utils/utils.php`
- ChitUI README commands: virtualenv setup, `python main.py`, port `54780`, and `docker run --net=host`
- Do not invent language percentages, live demo status, benchmarks, or production credentials.

## Product Principles

- The README and the handler are the sources. The template only arranges them.
- The same opening structure on every project, then only the sections that repository supports.
- A diagram is readable at its default size, with a text alternative.
- Permissions and deployment claims name the file that justifies them.
- The catalog works before JavaScript; filtering improves it.

## Accessibility & Inclusion

Project pages and the catalog target WCAG AA contrast for text, keyboard access to diagram controls, tabs, steppers, and filters, and a text alternative for every architecture diagram. Information is not conveyed by color alone.
