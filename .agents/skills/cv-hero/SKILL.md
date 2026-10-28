---
name: cv-hero
description: >-
  Edits the static CV hero and editorial date badges: name, role, place,
  portrait, actions, particles, and Experience/Education .year capsules.
  Use when changing #photo-header, butter-name motion, hero CSS,
  cv-interactions.js, .year / .year-range / .year-duration, or the top of
  index-en.html / index-fr.html.
---

# CV hero

The hero is `#photo-header` at the top of `index-en.html` and `index-fr.html`. Screen styling is `css/cv-editorial.css` inside `@media screen` (load after `css/design-tokens.css` and `css/cv-main.css`). Motion and the particle field are `js/cv-interactions.js`.

`index-en.html` and `index-fr.html` are canonical. After an English hero change, run `python scripts/html/sync_index_html.py` so `index.html` matches English. Mirror French in the same edit.

There are no standalone About HTML pages (`about-en.html` / `about-fr.html`).

## Date badges (Experience / Education)

Each job and education row uses one Apple-style capsule (HIG secondary fill, not Liquid Glass):

```html
<div class="year" aria-label="…full spoken range and duration…">
  <span class="year-range">Mon YYYY – Mon YYYY</span>
  <span class="year-duration">N mo</span>
</div>
```

- Show **how long** in `.year-duration` (EN `3 mo` / `1 yr 5 mo`; FR `3 mois` / `1 an 5 mois`). Count months inclusively.
- Mark ongoing roles with `cv-job--current` on the `<details class="cv-job">` so the capsule picks up the accent tint.
- Keep FR months abbreviated consistently (`sept.`, `janv.`, `fév.`, `avr.`, `déc.`). Clean dual seasons as `mai–août 2017 · mai–août 2018`.
- Styles: `css/cv-editorial.css` (screen) and matching capsule rules in `css/cv-main.css` (print / fallback). Documented in `DESIGN.md` under **CV date badges**.

## Markup

Keep this order inside `#text-header`:

1. `h1` with `.butter-name` (given name, family name) and `.butter-role` on the second line.
2. `.hero-place` — `Montréal, Québec`.
3. `.hero-actions` — primary download of the language PDF only.

Role line, in the hero and in letters:

- English: `Software Engineer · Platform and graphics`
- French: `Ingénieur logiciel · Plateforme et infographie`

Each animated word is `<span class="butter-word" style="--i:N">`. The early inline script sets `document.documentElement.dataset.motion = 'paused'` when `prefers-reduced-motion: reduce` or `localStorage` `cv-motion-paused` is true. Content must read correctly in that state and with JavaScript off.

Portrait: `antoine-portrait.png`, 160×160, `fetchpriority="high"`. Desktop frame is 208px; at `max-width: 767px` the photo drops to 104px and stacks above the name.

## What not to put in the hero

- No cover-letter links. The page stays PDF- and contact-oriented.
- No About-page secondary CTA.
- No open-source maintainer line. GitHub stats stay in Contact if present.
- No long tool list. Breadth belongs in the About section and the body.
- Site nav on the CV is the Blog pill plus EN | FR.

## Motion

- Butter glow and portrait settle live in `cv-editorial.css` and only run for `prefers-reduced-motion: no-preference` and `html:not([data-motion='paused'])`.
- `#particles-js` is `pointer-events: none`, behind `main`. `cv-editorial.css` hides it under `prefers-reduced-motion: reduce`. `cv-print.css` hides it in print.
- Pages load self-hosted `js/vendor/particles.min.js` (SRI) with `defer`; `cv-interactions.js` skips init when motion is reduced and exposes the Pause control. Do not start particles from a second copy of the config in the HTML.
- `forced-colors` and `[data-motion='paused']` kill the butter animation. Do not remove those blocks.

## Layout contract

Desktop (`css/cv-editorial.css`): two columns, text left, 208px photo right, paper panel on the slate canvas (`--editorial-canvas`). The header is left-aligned. `h1 br` is hidden; the role is a block under the name.

Below 768px: one column, photo then text, actions wrap, hit targets stay at least 44px.

Tokens already in `:root`: `--editorial-canvas`, `--editorial-paper`, `--editorial-ink`, `--editorial-muted`, `--editorial-accent`, Fraunces for the name, Open Sans for the role. Do not introduce a second display face.

`cv-main.css` still has older `#photo-header` rules. Screen hero changes belong in `cv-editorial.css`, which loads later. Change `cv-main.css` only when print or a no-editorial path must match.

## Verify

Open `index-en.html` and `index-fr.html` locally. Check reduced-motion, mobile width, and that the PDF download still works.
