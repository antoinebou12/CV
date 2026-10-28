# Implementation backlog

Work in this order. Stop when the requested scope is complete.

## 1. Baseline and tokens

- Capture the six required URLs in both themes and three widths.
- Measure text contrast, page overflow, diagram initial scale, and interaction failures.
- Compare CV and Hugo tokens. Consolidate shared color, focus, radius, spacing, and display-type roles in `design/tokens.json`.
- Regenerate token CSS with `scripts/build/sync_design_tokens.py`.

## 2. Project template hierarchy

- Keep title, status, technology badges, language percentages, overview, and Getting started above architecture.
- Preserve README chapters and source links.
- Keep the table of contents usable as a sticky rail on wide screens and a scrollable row on compact screens.
- Remove duplicated summaries and decorative labels.

## 3. Adaptive documentation

- Docker and infrastructure: service topology, ports, volumes, networks, boundaries, health caveats.
- APIs: routes, methods, request and response examples, authentication, verified authorization, errors.
- Algorithms: problem, inputs, outputs, pseudocode, walkthrough, complexity, tests.
- Graphics and simulation: model, parameters, update pipeline, rendering path, validation.
- CLI and libraries: quick start, commands or public API, configuration, integration examples.

## 4. Diagrams

- Keep primary diagrams between 5 and 12 nodes.
- Split context, components, deployment, sequence, and data views.
- Start at 100 percent with scroll, Fit, zoom, fullscreen, SVG export, image fallback, source, and text alternative.
- Correct edge-label contrast in both themes.

## 5. Project explorer

- Keep featured projects above the catalog.
- Search descriptions and technical metadata.
- Filter by primary language and project style.
- Group results by primary language.
- Support sorting by activity, name, and stars.
- Keep all controls keyboard operable and announce the result count.

## 6. CSS consolidation

- Map repeated literals and high-specificity overrides to shared tokens and scoped components.
- Remove obsolete rules only after computed-style and screenshot comparisons.
- Avoid adding another stylesheet unless it owns a distinct surface.
- Check 200 percent zoom and long English/French labels.

## 7. Verification and handoff

- Run the local and production builds.
- Run repository tests, parity, deployment verification, and browser checks.
- Record every retained experiment.
- Report limits honestly. Do not call a screenshot-tested prototype deployed.
