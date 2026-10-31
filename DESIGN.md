---
name: Antoine Boucher project documentation
description: Documentation shell for repository project pages and the project catalog.
colors:
  bg-dark: "#0a1019"
  panel-dark: "#111c2a"
  panel2-dark: "#172637"
  line-dark: "#334559"
  text-dark: "#edf4fb"
  muted-dark: "#b5c4d2"
  accent-dark: "#6fdbd0"
  accent2-dark: "#acd5ff"
  chip-dark: "#1b3040"
  code-dark: "#091824"
  warn-dark: "#ffdaa0"
  bg-light: "#f7f9fc"
  panel-light: "#ffffff"
  panel2-light: "#f0f5fa"
  line-light: "#becfdf"
  text-light: "#192a3c"
  muted-light: "#4e6070"
  accent-light: "#006a62"
  accent2-light: "#175fa0"
  chip-light: "#e9f3f4"
  code-light: "#eef5f8"
  warn-light: "#6b4504"
  journal-canvas: "oklch(0.398 0.047 248)"
  journal-page: "oklch(0.985 0.006 190)"
  text-strong: "oklch(0.31 0.035 240)"
  brand-accent: "oklch(0.445 0.073 181)"
typography:
  display:
    fontFamily: "system-ui, Segoe UI, sans-serif"
    fontSize: "clamp(34px, 4vw, 56px)"
    fontWeight: 700
    lineHeight: 1.09
    letterSpacing: "-0.055em"
  body:
    fontFamily: "system-ui, Segoe UI, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "normal"
  label:
    fontFamily: "system-ui, Segoe UI, sans-serif"
    fontSize: "11px"
    fontWeight: 700
    lineHeight: 1.4
    letterSpacing: "0.13em"
  code:
    fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace"
    fontSize: "12px"
    fontWeight: 400
    lineHeight: 1.75
    letterSpacing: "normal"
rounded:
  sm: "7px"
  md: "10px"
  lg: "14px"
spacing:
  sm: "8px"
  md: "16px"
  lg: "28px"
components:
  button-primary:
    backgroundColor: "{colors.accent-dark}"
    textColor: "{colors.bg-dark}"
    rounded: "{rounded.sm}"
    padding: "8px 13px"
    height: "38px"
  badge:
    backgroundColor: "{colors.chip-dark}"
    textColor: "{colors.text-dark}"
    rounded: "{rounded.sm}"
    padding: "4px 10px"
  card:
    backgroundColor: "{colors.panel-dark}"
    textColor: "{colors.text-dark}"
    rounded: "{rounded.lg}"
    padding: "19px"
---

## Projects aligned with the CV hero

The project directory and repository documentation inherit the CV hero's paper, ink, muted, accent, soft and rule tokens. `hugo/assets/projects-editorial.css` applies this shared identity after the documentation styles. Dark mode uses the CV's blue-gray paper and teal accent. Fraunces remains the title face; body copy and controls use the existing sans-serif stack.

Search uses the same eight-pixel field radius as the post controls, with a visible focus ring. Filter and metadata chips wrap with explicit spacing. Repository cards use the post grid's 28-pixel gap, five-pixel radius and 28-pixel desktop inset. Related articles sit below the actions with a clear rule and enough space to read as a separate block. An inline repository mark provides a dependable fallback symbol without implying that it is an official project logo. Documentation heroes use an open paper layout with a bottom rule, a numbered reading sequence and a slim table-of-contents rail. Language disclosures have a spaced summary row.

The project catalog uses the post index's outer canvas, centered paper surface, maximum width, page gutters and dark-mode treatment. The catalog must not replace those shared journal tokens with a flat white or black page. The introduction is a two-column editorial heading and lead at desktop widths, then one column on small screens. Its date sits below both columns. The explorer follows directly; featured stories are omitted. Repository cards show one language badge, one style, one competence domain, a short description, documentation and source links, related writing when available, and the page's last-modified date. Forks carry an outlined badge with a branch icon.

The projects index adds a low-density canvas animation behind the journal paper, based on the CV background treatment. It has no pointer interaction, pauses when the page is hidden and is not created when the user prefers reduced motion. The explorer keeps 44-pixel controls on narrow screens. From 760 pixels upward, it uses a compact grid with 36-pixel filter chips, an inline result count and sorting beside the repository filter.

Repository type (All / My repositories / Forks), style and domain filters combine with search. “My repositories” means non-forks in the existing inventory; it does not claim sole authorship. Reset clears every filter and restores star sorting. Group headings stay uncluttered; the global live result count reports filter changes. Filter buttons expose their selection through `aria-pressed`, with text labels and a 44px minimum target. Titles and leads reveal briefly using opacity and translation; do not clip heading glyphs or descenders. Reduced-motion users receive static content. Diagram controls offer zoom, fit, 100%, full screen, SVG export, and pointer or arrow-key panning. Diagrams fit the reader column when they open; text alternatives remain available if rendering fails, while raw Mermaid source stays out of the rendered interface. Keep bilingual copy and repository evidence consistent; a repository name alone is never evidence of its purpose.

## Overview

**Shared spine, different density.** Canonical tokens live in [`design/tokens.json`](design/tokens.json) and sync to [`css/design-tokens.css`](css/design-tokens.css) and [`hugo/assets/design-tokens.css`](hugo/assets/design-tokens.css) via `python scripts/build/sync_design_tokens.py`. The spine covers accent, focus rings, spacing, and badge/button radii across the static CV hero and Hugo. The CV hero uses Fraunces display type and an editorial paper surface. The posts and projects indexes share the journal canvas, paper surface and responsive gutters. Individual `repository_note` pages use the denser documentation shell. Fraunces appears on page titles while technical content stays in the sans-serif stack.

## Colors

On project pages, dark mode is the default shell: `--bg #0a1019`, `--panel #111c2a`, `--panel2 #172637`, `--text #edf4fb`, `--muted #c2d0de`, `--accent #6fdbd0`, `--accent2 #acd5ff`. Light mode swaps to `#f7f9fc` / `#192a3c` / `#3d4f5f` muted / `#006a62`. Every heading, paragraph, badge, and control sets `color` from `--text` or `--muted`. Links use `--accent2`. Warnings use `--warn` on a tinted fill. Language-bar segments alternate fills; each language is also named in the table.

## Typography

Titles use Fraunces around 1.75 to 2.35rem. Section headings are about 1.35rem with a bottom hairline. Body is 16px / 1.7 on a ~65ch measure. Labels and sidebar headings are small uppercase. Commands use monospace at about 13px.

## Layout

Two columns: sticky TOC (~13.5rem) and a reading column (~50rem). The former facts rail is intentionally omitted because it repeated hero metadata. Below 760px the TOC becomes a wrapped row without a nested scrollbar. Order: badges and actions, languages, overview prose, Getting Started, README excerpts, features definition list, architecture (Mermaid in details), optional workflow, API, deployment, code, limits, source files and references. The catalog opens with search and repository-origin, project-type and competence-domain filters. Cards are grouped once by their first type in `repository_styles.json`; secondary types remain searchable and filterable. Languages stay on the cards as badges. Teaching is a project type; Flash is a technology badge for FlashGames. Related articles remain on their owning cards. Documentation and GitHub actions use equal-height 44px targets on the same row, with a local inline GitHub icon and visible text.

## Elevation & Depth

Borders carry hierarchy; do not stack soft shadows on every block. Primary buttons fill `--accent`. Focus uses a 2px accent outline. Tabs are underline-style under a hairline rule.

## Shapes

Small radii (~0.35rem). Language bars are short tracks. Architecture context is an ordered flow list, not heavy nodes.

## Components

Hero: title first, then status chips, tech badges, last-updated metadata, Source and README actions. Git revisions are source data, not reader-facing metadata. Languages: segmented bar plus a compact table. Getting Started: Native / Docker tabs when both exist, terminal blocks with clear copy actions. Features: definition list. Architecture: Context / Components / Deployment views; Mermaid stays behind a details disclosure and fits the reading column when opened. Deployment: Compose service table plus topology Mermaid when `services` exist. Algorithm panel only when `profile.algorithm` is present (problem, I/O, pseudocode, steps). Workflow stepper only when a profile defines `workflow`. API table: method, path, purpose, verified access. Each page ends with GitHub, README and any related blog links. Catalog: search with live count, repository-origin, project-type and competence-domain filters (keyboard arrows), with cards grouped by primary project type.

## Project documentation maintenance plan

1. Treat `hugo/layouts/shortcodes/repository-note.html` and `hugo/assets/projects-editorial.css` as the shared project-note system. Change those files before patching a single generated note.
2. Keep English and French labels together in the template. Verify both routes after every shared change.
3. Use `Page.Lastmod` for reader-facing freshness. Keep commit identifiers and fetch timestamps in source data only.
4. Add a project image only when it is an actual repository asset with a recorded source path and meaningful alt text. Do not add stock imagery or inferred diagrams.
5. Preserve GitHub, README, documentation and blog links. Add a reference entry only when its target is verified.
6. Build with `hugo --minify` and run `node --test scripts/verify/repository-notes.test.mjs` with `CV_NOTES_SITE=hugo/public`. Check both light and dark themes and the 760px navigation breakpoint before shipping.

### CV date badges (Experience / Education)

On `index-en.html` / `index-fr.html`, each `.year` is one compact Apple-style capsule (fully rounded, soft fill, inset hairline)—not Liquid Glass in the content layer. Markup:

```html
<div class="year" aria-label="March 2025 to February 2026, 1 year">
  <span class="year-range">Mar 2025 – Feb 2026</span>
  <span class="year-duration">1 yr</span>
</div>
```

- Single-line layout: range then a middot-prefixed duration (`Mar 2025 – Jan 2026 · 11 mo`).
- `.year-range` — primary label (date span, tabular nums).
- `.year-duration` — secondary label after the range (`3 mo`, `1 yr 5 mo` / FR `3 mois`, `1 an 5 mois`), inclusive month count.
- Current roles (`.cv-job--current`) tint the capsule with the editorial accent.
- Screen polish lives in `css/cv-editorial.css`; `css/cv-main.css` carries the same capsule for print and no-editorial fallback.
- Keep EN/FR month abbreviations clean (FR: `sept.`, `janv.`, `fév.`, …). Do not leave English month stubs in `index-fr.html`.
- Long org names on the index use a short display label plus `title` for the full name (e.g. IMC2).

## Article reading and slide previews

Project documentation owns setup, API contracts, deployment, architecture details, and terminology. Blog posts introduce a project or describe a substantial change, with an explicit `project_docs` slug linking to the reference. `story_kind: introduction` labels an introduction without implying a release; `progress` is reserved for an evidenced update. Keep original dates and describe decisions without inventing outcomes.

Project glossaries use bilingual definitions from `hugo/data/documentation_glossary.yaml`, selected by terms present in the project evidence. Definitions expand with native details controls; search is a JavaScript enhancement. Architecture components expand to show the directed connections already recorded in the project data. Term and component fragments reveal their target disclosures. Do not imply live repository synchronization or running software.

Use only real project assets for covers and figures. Do not generate conceptual illustrations as substitutes. Set `cover_none: true` when no suitable real asset is available, keeping the article and its list/search entries text-only. Show a cover once; preserve its original descriptive alt text when removing a duplicate inline placement.

Article images can open in a focused native-dialog preview. Keep captions and AI-image disclosures visible, provide Close and Escape dismissal, restore keyboard focus to the opening image, and leave ordinary images readable without JavaScript. Slide controls and interactive diagrams retain their own viewers.

Article headers show one content-kind badge, the title, publication date, reading time and topic links. The header language switcher handles translations; do not repeat translation links in article introductions. Long articles expose a collapsible contents list. Keep one visible introduction and preserve the original publication date when updating content.

Figures display their complete contents with captions where scale, provenance or interpretation matters. A math fixture is not a renderer screenshot. Set `show_hero: false` when the article is better served by its inline figures or interactive diagram.

Slide previews use local images exported from the original presentation, with a PDF and PowerPoint download. Previous, next, slide selection and arrow keys expose the same slides; without JavaScript, the horizontal gallery remains scrollable. Resolve shared bundle resources through Hugo so French download links use the real asset URL. Avoid external viewers that need access to localhost.

## Do's and Don'ts

- Do paint every project-page text node from `--text` or `--muted`.
- Do keep Getting Started above architecture.
- Do omit API, deployment, workflow, and algorithm sections when the repository has no evidence.
- Do fit Mermaid to the reading column on open and keep a text alternative.
- Apply Fraunces to project titles and share the CV paper tokens inside `.repo-doc`; use sans-serif for technical content.
- Do not invent language percentages, ports, or permission claims.
- Do not use color alone to distinguish languages, services, or permissions.
- Do not put Liquid Glass on CV content-layer date badges; use the filled capsule pattern above.

## Reading controls for projects and posts

Project notes and posts share a progressive reading toolbar (`reader-tools.html`,
`reader-tools.css`, `reader-tools.js`). The inline split control opens page search
or copies the current URL. The floating Page tools button opens a native popover
with section search, copy, back-to-top, and a checkbox for expanding text panels.
The search dialog filters headings and diagrams locally, with All / Sections /
Diagrams scopes, an empty state, Escape dismissal, and keyboard focus return.
Press `/` outside a text field to open it. On phones, it uses a bottom sheet.

Copy actions report success or an actionable error in a polite status message.
The top reading indicator is decorative and does not announce every scroll event.
Diagrams remain lazy. Without the script, the original content, source links,
numbered contents, and native disclosures remain available.

Repository snapshot cards use existing language, component, and document counts.
Language meters show GitHub Linguist byte percentages, alongside the exact table;
they do not indicate test coverage or project progress.

## Article composition

Articles use one centered reading column (up to 960px). Titles, body content and
references share its left edge. References follow the article instead of floating
beside its first paragraph. Technical diagram figures have a neutral image surface,
a bounded image height and a caption inside the frame. Inline code wraps on phones;
code blocks scroll within their container. Mobile comparison tables stay within the
reading column and keep their accessible header labels.
