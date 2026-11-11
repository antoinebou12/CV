---
name: pick-ui-library
description: >-
  Picks the right component or library for a frontend task on this site (static
  CV pages and the Hugo blog) so nothing is rebuilt from scratch: buttons, chips,
  stats, hero, cards, audio player, live demos, 3D models, diagrams, charts,
  tables, toasts, drawers, command menus, animated numbers. Use before adding
  any new UI element, widget, animation or third-party script, or when asked
  which library to use.
---

# Pick the UI library

Adapted from Emil Kowalski's `pick-ui-library` skill (MIT,
https://github.com/emilkowalski/skills) and the three-tier approach in Griffin
Wooldridge's "UI Libraries for Claude Code (Ban the AI Look)". His list assumes
React. This site has no React and no bundler: static HTML for the CV, Hugo
templates for the blog. So the order here is different.

## How to use this

1. **Name the task**, not the library. "Show the newest post at the top" is a
   hero-panel task. "Let people copy the command" is a button task.
2. **Check tier 1 first.** If the site already has the component, use it. Do
   not write a second button, chip or card style.
3. **Then tier 2**: a script the site already loads or a small vanilla library
   from the list. Recommend one, say what it is for in one sentence.
4. **Tier 3 is a look, not a dependency.** Design-component sites are a source
   of ideas to rebuild in plain CSS. Never copy React code from them.
5. If nothing fits, say so and recommend from your own knowledge, stating that
   you left the list.

Every new third-party script needs: a pinned version, an `integrity` hash, and
its host added to the CSP in `hugo/static/_headers`, `vercel.json` and
`cloudflare/workers/agent-ready-home/worker.mjs`.

## Tier 1: what the site already has

Reference: `docs/development/ui-library.md`.

| Task | Use | Where |
| --- | --- | --- |
| Button, link styled as a button | `.ui-btn`, `.ui-btn--primary`, `.ui-btn--quiet` | `hugo/assets/ui.css` |
| Small label, status, count | `.ui-chip`, `.ui-chip--accent` | `hugo/assets/ui.css` |
| Row of headline numbers | `dl.ui-stats` with `data-count` | `ui.css`, `ui.js` |
| Flat bordered surface | `.ui-panel` | `hugo/assets/ui.css` |
| Home page hero | `partials/home-hero.html` | `hugo/layouts/partials/` |
| Section intro (eyebrow, h1, lede) | `.journal-intro`, `.journal-eyebrow` | `hugo/assets/editorial.css` |
| Post or project card | `partials/post-list-item.html` | `hugo/layouts/partials/` |
| Featured repositories | `partials/home-featured-projects.html` | `hugo/layouts/partials/` |
| Audio episode player | `partials/podcast-player.html` | see `docs/development/podcasts.md` |
| Running web demo in a page | `demos` shortcode | see `docs/development/blog-embeds.md` |
| 3D model | `modelviewer` shortcode (model-viewer) | see `docs/development/blog-embeds.md` |
| Diagram | Mermaid fence, `partials/mermaid.html` | Hugo |
| Sortable or wide table | `dynamic-tables.js` | `hugo/assets/` |
| Scroll reveal | `data-reveal`, `data-reveal-group` | `hugo/assets/motion.js` |
| Reading tools, table of contents | `reader-tools.js`, `article-toc.js` | `hugo/assets/` |
| Colour, spacing, radius, easing | tokens from `design/tokens.json` | `scripts/build/sync_design_tokens.py` |
| CV hero and date badges | the `cv-hero` skill | `css/cv-editorial.css` |

## Tier 2: specialists that work without React

| Task | Library | Note |
| --- | --- | --- |
| Dialog, drawer, popover, menu | native `<dialog>`, `popover` attribute, `<details>` | The browser handles focus and Escape. No library. |
| Toast or notification | a `role="status"` region plus one CSS transition | Sonner is React only. Copy its restraint: one line, bottom corner, auto-dismiss, pause on hover. |
| Command menu or search | the existing search page (`layouts/_default/search.html`) | cmdk is React only. Extend the search page first. |
| Animated number | `data-count` in `ui.js` | For digit-by-digit rolls, NumberFlow ships a vanilla web component (`number-flow`). |
| Animation with springs or exits | CSS transitions first, then [Motion](https://motion.dev) vanilla `animate()` | A hover or fade never needs a library. |
| Syntax highlighting | the bundled highlight.js | Shiki only if a build step is added. |
| Charts | inline SVG written by the build script | No chart runtime on a static page. |
| 3D globe | [Cobe](https://cobe.vercel.app) | Vanilla, about 5 kB. |
| Particles background | the bundled `particles.min.js` | Already skipped under reduced motion. |
| Social preview images | [Satori](https://github.com/vercel/satori) in a build script | Never at runtime. |

For a React project elsewhere, use Emil's original list: Base UI, cmdk, Sonner,
Vaul, input-otp, Motion, NumberFlow, recharts, dnd kit, Virtuoso, zustand,
clsx, cva, next-themes.

## Tier 3: design components, as reference only

Magic UI, Aceternity UI, 21st.dev, Beautiful UI, RareUI. Open them for a
specific pattern, then rebuild it with the site's tokens.

**One standout per screen.** A page gets one element that draws the eye: the
latest-post panel in the home hero, the running demo on the Dimension post, the
3D model on the WearMachine note. Everything around it stays flat.

## The AI look to avoid

- A gradient headline, glow, or blurred blob behind the hero.
- Default shadcn greys with a purple or indigo accent.
- Three identical cards with an icon, a title and two lines each.
- Shadows stacked on borders stacked on rounded corners.
- Every element fading in on scroll.
- A generic placeholder image where a real one is missing. Drop the image.

## Common mismatches to catch

- A new `.something-button` class → `.ui-btn`.
- A hand-built modal `<div>` with focus code → `<dialog>`.
- A number set with `setInterval` → `data-count`.
- A React component pasted from a design-component site → rebuild in CSS.
- A new CDN script with no `integrity` and no CSP entry → add both, or do not add the script.
- A second accent colour → use `--brand-accent`.
