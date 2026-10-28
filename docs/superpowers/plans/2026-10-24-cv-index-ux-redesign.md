# CV index UX redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (inline; user requested immediate implementation). Steps use checkbox syntax.

**Goal:** Ship the approved editorial CV index UX redesign (section nav, two-level accordions, domain competence cards, paper surfaces, discoverable personal projects, WCAG 2.2 AA basics).

**Architecture:** Keep two-column `index-en.html` / `index-fr.html`. Extend fixed nav; flatten nested `<details>`; replace skill meters with domain cards; retarget evidence JS; polish CSS tokens.

**Tech Stack:** Static HTML, `css/cv-*.css`, `js/cv-interactions.js`, design tokens.

**Spec:** [`docs/superpowers/specs/2026-10-24-cv-index-ux-redesign-design.md`](../specs/2026-10-24-cv-index-ux-redesign-design.md)

## Global Constraints

- EN/FR parity on all structural and copy changes.
- No LaTeX/PDF changes; no cover-letter links; no About pages.
- Max accordion depth: section → item.
- No skill meters / percentage bars.
- Personal projects always visible when Selected Projects is open.
- Contrast ≥ 4.5:1; visible `:focus-visible`; `scroll-margin-top` for anchors.

---

### Task 1: Section nav + anchors + scroll-spy

**Files:** `index-en.html`, `index-fr.html`, `css/cv-site-nav.css`, `css/cv-editorial.css`, `js/cv-interactions.js`

- [ ] Add `id="work"|"projects"|"skills"|"contact"` on section details
- [ ] Add nav links Work/Projects/Skills/Contact (FR: Travail/Projets/Compétences/Contact)
- [ ] Style section links; scroll-margin; scroll-spy `aria-current`

### Task 2: Flatten nests + expose personal projects

**Files:** `index-en.html`, `index-fr.html`, CSS for removed nest classes

- [ ] Promote project-group/subgroup to `h3`; personal list always open
- [ ] Flatten cv-course and project-preview nests
- [ ] Optional single details only for Other accepted contributions

### Task 3: Domain competence cards + evidence JS

**Files:** both indexes, `js/cv-interactions.js`, CSS

- [ ] Replace major/subgroup details + meters with domain cards + chip groups
- [ ] Certifications as static h3 + list
- [ ] Retarget evidence aggregation to domain cards

### Task 4: Visual density + job rows

**Files:** `css/cv-editorial.css`, `css/cv-main.css`

- [ ] Paper + border cards; remove mint slabs; shared spacing/radius
- [ ] Wider `.year`; full-row job summary affordance

### Task 5: Sync, docs, verify

- [ ] `python scripts/html/sync_index_html.py`
- [ ] Update `AGENTS.md` nav note
- [ ] Manual/visual check EN+FR mobile/desktop; keyboard nav
