# UI audit — Hugo blog and project pages (2026-11-05)

Method: the audit follows the *Making UX Decisions* framework (tommygeoco/ui-audit): weigh institutional knowledge (DESIGN.md, PRODUCT.md, AGENTS.md), user familiarity (documentation-site and portfolio conventions), then measurements. Evidence: Playwright screenshots at 390, 1440 and 1920 px in light and dark, axe-core (WCAG 2.1 A/AA) on four page types, Lighthouse 12 on seven pages, and a DOM measurement pass (heading outline, type sizes, target sizes, landmarks, horizontal overflow). Checks marked *fixed* were corrected in the same change set.

Pages: home, posts list, article, projects catalog, project note (uml-mcp, FlashGames, HDR-10bpp-Display-Test), recipes, search, tag page, footer.

## Macro bets and jobs to be done

- **Accuracy** (strong): every project page is generated from repository data and says so; copy never adds facts the data does not hold.
- **Efficiency** (strong): one shared design spine (tokens, header chrome, card system) across the CV and the blog.
- **Velocity** (moderate): familiar patterns (documentation shell, catalog with facets, sticky TOC) over novel ones.

| User | Situation | Motivation | Outcome |
| --- | --- | --- | --- |
| Hiring manager | opens a project from the CV | see what it does and how it is built in two minutes | judge depth without reading a repository |
| Collaborator | lands on a repository page from GitHub | find the start commands and the architecture | run or extend the project |
| Answer engine / agent | crawls the site | get structured, source-backed facts | cite the right page with the right facts |

## Visual hierarchy

| Check | Status | Notes |
| --- | --- | --- |
| One h1 per page, no skipped levels | pass | Measured on all eight page types, both widths. |
| Display versus section ratio | pass | Fraunces h1 40px on lists, h2 16–22px; article h1 32px (phone) versus h2 30px: ratio 1.1 on phones — see priority 5. |
| Primary action clarity | pass | Project note: one filled button (View source), outlined secondaries; catalog cards: Documentation (filled soft) and GitHub (outline). |
| Grouping and proximity | pass (fixed) | Post cards: media → date → title → teaser → tag footer; the tag disclosure was replaced by an inline footer. |
| Reading flow on wide screens | pass (fixed) | Lists use a two-column intro (title left, lead baseline-aligned right); articles and notes keep a 15–17rem rail plus a bounded column. |
| Colour hierarchy | pass | Accent (teal) reserved for links, current states and primary actions; muted ink for metadata. |
| Whitespace scale | warn | Section rhythm is consistent (3.5rem between numbered sections); a few components still use off-scale values (22px card padding, 14px gaps). |
| Featured content | pass (fixed) | Home now opens with three flagship repositories (stars from the inventory); their styles had been lost in a later edit and are restored. |

## Visual style

| Check | Status | Notes |
| --- | --- | --- |
| Spacing base unit | warn | Mostly 4/8px multiples; `22px` card padding and `14px` gaps remain in the catalog. |
| Colour contrast (text) | pass (fixed) | axe reports 0 violations on home, catalog, note and article after the footer labels were lightened (4.16:1 → >4.5:1). |
| Dark mode parity | pass | Header, footer, rails and cards defined with tokens for both schemes; project notes keep the documentation palette. |
| Elevation | pass | Flat panels with hairline rules; shadows only on hover lift, popover and drawer. |
| Typography system | pass | Fraunces for titles, Open Sans for prose, system UI for documentation, monospace for commands; 2 weights per face. |
| Line length | pass | Prose capped at 76–78ch; project lede at 78ch. |
| Motion | pass | 180–640ms, ease-out entrances, transform/opacity only, `prefers-reduced-motion` honoured everywhere, pause control for the particle background. |
| Imagery | pass (fixed) | Consistent 16:9 media frames; diagrams and logos sit on a soft panel with padding, photos fill; bloc article cover replaced (it showed an unrelated render). |
| Loading states | pass (fixed) | Navigation progress bar, spinner on lazy demo frames, loading label on diagrams. |

## Accessibility

| Check | Status | Notes |
| --- | --- | --- |
| Keyboard operability | pass | Filters, tabs (arrow keys, Home/End), options popover, drawer with focus trap and Escape, diagram viewer shortcuts. |
| Visible focus | pass | 2–3px outlines with offset on every control; white outline on the slate header. |
| Contrast 4.5:1 | pass (fixed) | See visual style. |
| Touch targets | warn (fixed) | Phone TOC links were 19px tall, catalog "On the blog" links 20px, note reference links 20–22px; now ≥32–44px. Remaining: inline citation superscripts are 24px. |
| Landmarks | fail (fixed) | 63 `<nav>` landmarks on list pages (one per card); card tags are now `<ul>` lists; nav count drops to the header, breadcrumbs, pagers and footer columns. |
| Language | pass (fixed) | `<html lang>` was `en-us`; now `en` and `fr`, matching hreflang and sitemap alternates. |
| Alternative text | pass | Card thumbnails are decorative (`alt=""`), hero images carry the article alt, diagrams have text versions. |
| Reduced motion | pass | Reveals, transitions, particles and the progress bar are disabled under `prefers-reduced-motion`. |
| Semantic structure | pass | `main`, skip link, breadcrumbs, `dl` snapshot cards (fixed structure), tables with scoped headers and `aria-sort`. |

## Navigation

| Check | Status | Notes |
| --- | --- | --- |
| Where am I | pass | Current pill in the header, breadcrumb on notes, highlighted TOC entry that follows scrolling. |
| Where can I go | pass | Five sections + CV + Stars (when data exists) in one pill group; footer directory repeats them with profiles and agent files. |
| Mobile pattern | pass | Hamburger + drawer with the same pill groups; Options popover stays visible. |
| Deep linking | pass | Section anchors, tag links, Markdown twins per page; filter state is not in the URL (see priority 6). |
| Consistency | pass (fixed) | Tag pages and recipes now share the list intro; the back link is a quiet breadcrumb. |

## Usability

| Check | Status | Notes |
| --- | --- | --- |
| Catalog filtering | pass (fixed) | The chosen type leads and opens; other groups follow collapsed as secondary matches; search matches every word, accent-insensitively; counts per group. |
| Feedback on actions | pass | Live counts, copy confirmations, sort announcements (`aria-sort` + status), progress bar. |
| Empty states | pass | Catalog, stars, search and table filters each explain and offer a reset. |
| Error prevention | pass | Demo frames load only on request with an open-in-new-tab fallback; commands are labelled "not run during this review". |
| Cognitive load | warn | Project notes carry 12–14 numbered sections; the rail and "Explore this page" dialog mitigate it, and the section order is identical on every project. |

## Priority fixes

1. **Restore the featured projects styles** — the home strip rendered as plain text after the TOC rewrite. *Fixed.* (`12-checklist-visual-style.md` → Visual Style Audit)
2. **Landmark overuse** — one `<nav>` per card; replaced by lists. *Fixed.* (`27-patterns-accessibility.md` → ARIA Attributes, Screen Reader Testing)
3. **Touch targets on phones** — TOC, card and reference links under 24px; raised to 32–44px. *Fixed.* (`27-patterns-accessibility.md` → Interactive Elements; `11-checklist-fidelity.md` → Component States)
4. **Language code** — `en-us` versus `en` alternates; aligned. *Fixed.* (`27-patterns-accessibility.md` → Screen Reader Testing)
5. **Article heading scale on phones** — h1 32px against h2 30px; raise the phone h1 to 36px or lower h2 to 26px. *Open.* (`23-patterns-visual-hierarchy.md` → Typography Hierarchy)
6. **Filter state in the URL** — catalog and stars filters reset on reload and cannot be shared; encode type/domain/query in the hash. *Open.* (`31-patterns-navigation.md` → Navigation Audit; `11-checklist-fidelity.md` → Navigation)
7. **Off-scale spacing** — move 22px/14px values in the catalog onto the 4/8 scale. *Open.* (`12-checklist-visual-style.md` → Spacing)

## Scores after the fixes (Lighthouse 12, mobile emulation, local static server)

| Page | Performance | Accessibility | Best practices | SEO | CLS |
| --- | --- | --- | --- | --- | --- |
| Blog home | 83 | 100 | 100 | 100 | 0.000 |
| Posts list | 77 | 100 | 100 | 100 | 0.000 |
| Article (uml-mcp) | 83 | 100 | 96* | 100 | 0.022 |
| Projects catalog | 78 | 100 | 100 | 100 | 0.000 |
| Project note (uml-mcp) | 70 | 100 | 100 | 100 | 0.000 |
| CV (index-en.html) | 73 | 100 | 96* | 100 | 0.060 |

Before this work the same pages measured 63–75 performance, 90–96 accessibility and a 0.42 layout shift on project notes (phone). *Console errors in the sandbox come from blocked third-party hosts (mermaid CDN, shields.io), not from the pages. Project notes are bounded by page weight (open diagrams, ~3,600 DOM nodes); diagrams render only near the viewport.

```json
{
  "title": "Antoine Boucher — blog and project pages",
  "project": "antoinebou12/CV (Hugo)",
  "date": "2026-11-05",
  "macro_bets": [
    {"category": "accuracy", "description": "Source-backed project documentation", "alignment": "strong"},
    {"category": "efficiency", "description": "One design spine for CV and blog", "alignment": "strong"},
    {"category": "velocity", "description": "Familiar documentation and catalog patterns", "alignment": "moderate"}
  ],
  "jtbd": [
    {"user": "Hiring manager", "situation": "opening a project from the CV", "motivation": "understand purpose and construction quickly", "outcome": "judge depth without reading the repository"},
    {"user": "Collaborator", "situation": "arriving from GitHub", "motivation": "find start commands and architecture", "outcome": "run or extend the project"},
    {"user": "Agent", "situation": "crawling the site", "motivation": "structured, source-backed facts", "outcome": "cite the right page"}
  ],
  "visual_hierarchy": {"title": "Visual Hierarchy", "checks": [
    {"label": "Heading outline", "status": "pass", "notes": "One h1, no skipped levels on 8 page types"},
    {"label": "Primary action clarity", "status": "pass", "notes": "One filled button per card or hero"},
    {"label": "Grouping", "status": "pass", "notes": "Card order media, date, title, teaser, tags"},
    {"label": "Wide-screen reading flow", "status": "pass", "notes": "Rail + bounded column; two-column list intro"},
    {"label": "Whitespace scale", "status": "warn", "notes": "22px and 14px values remain in the catalog"},
    {"label": "Phone heading ratio", "status": "warn", "notes": "Article h1 32px vs h2 30px"}
  ]},
  "visual_style": {"title": "Visual Style", "checks": [
    {"label": "Spacing base unit", "status": "warn", "notes": "Mostly 4/8px; a few off-scale values"},
    {"label": "Contrast", "status": "pass", "notes": "axe 0 violations after footer label fix"},
    {"label": "Dark mode", "status": "pass", "notes": "Tokens for both schemes"},
    {"label": "Typography system", "status": "pass", "notes": "Fraunces, Open Sans, system UI, monospace"},
    {"label": "Motion", "status": "pass", "notes": "180–640ms, reduced-motion honoured"},
    {"label": "Imagery", "status": "pass", "notes": "16:9 frames; misleading cover replaced"},
    {"label": "Loading states", "status": "pass", "notes": "Progress bar, frame spinner, diagram label"}
  ]},
  "accessibility": {"title": "Accessibility", "checks": [
    {"label": "Keyboard", "status": "pass", "notes": "Tabs, popover, drawer, diagram shortcuts"},
    {"label": "Focus visible", "status": "pass", "notes": "Outlines with offset everywhere"},
    {"label": "Contrast 4.5:1", "status": "pass", "notes": "Fixed footer labels"},
    {"label": "Touch targets", "status": "pass", "notes": "Fixed TOC, card and reference links"},
    {"label": "Landmarks", "status": "pass", "notes": "Fixed per-card nav elements"},
    {"label": "Language attribute", "status": "pass", "notes": "en / fr"},
    {"label": "Alt text", "status": "pass", "notes": "Decorative thumbnails, described heroes, diagram text versions"},
    {"label": "Reduced motion", "status": "pass", "notes": "All motion gated"}
  ]},
  "navigation": {"title": "Navigation", "checks": [
    {"label": "Current location", "status": "pass", "notes": "Header pill, breadcrumb, TOC spy"},
    {"label": "Destinations", "status": "pass", "notes": "Pill group + footer directory"},
    {"label": "Mobile pattern", "status": "pass", "notes": "Drawer with the same groups"},
    {"label": "Deep linking", "status": "warn", "notes": "Filters not encoded in the URL"}
  ]},
  "usability": {"title": "Usability", "checks": [
    {"label": "Filter focus", "status": "pass", "notes": "Chosen type leads; secondary matches follow"},
    {"label": "Feedback", "status": "pass", "notes": "Live counts, aria-sort, copy states"},
    {"label": "Empty states", "status": "pass", "notes": "Explain and reset"},
    {"label": "Cognitive load", "status": "warn", "notes": "12–14 sections per note, mitigated by rail and search"}
  ]},
  "priority_fixes": [
    {"rank": 1, "title": "Restore featured projects styles", "description": "Home strip rendered unstyled", "framework_reference": "12-checklist-visual-style.md → Visual Style Audit"},
    {"rank": 2, "title": "Remove per-card nav landmarks", "description": "63 nav elements on list pages", "framework_reference": "27-patterns-accessibility.md → ARIA Attributes"},
    {"rank": 3, "title": "Raise small touch targets", "description": "TOC, card and reference links under 24px", "framework_reference": "27-patterns-accessibility.md → Interactive Elements"},
    {"rank": 4, "title": "Align language codes", "description": "html lang en-us vs hreflang en", "framework_reference": "27-patterns-accessibility.md → Screen Reader Testing"},
    {"rank": 5, "title": "Phone article heading scale", "description": "h1 32px vs h2 30px", "framework_reference": "23-patterns-visual-hierarchy.md → Typography Hierarchy"},
    {"rank": 6, "title": "Encode filter state in the URL", "description": "Shareable catalog and stars filters", "framework_reference": "31-patterns-navigation.md → Navigation Audit"},
    {"rank": 7, "title": "Spacing scale clean-up", "description": "22px/14px values in the catalog", "framework_reference": "12-checklist-visual-style.md → Spacing"}
  ],
  "notes": "Fixes 1–4 ship with this audit; 5–7 are queued."
}
```
