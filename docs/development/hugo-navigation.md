# Hugo blog: header and navigation

The static blog under [`hugo/`](../../hugo/) uses the **Paper** theme ([nanxiaobei/hugo-paper](https://github.com/nanxiaobei/hugo-paper)) with a **custom header** for bilingual language switching, the main menu, and dark mode. The repository still publishes standalone HTML résumés at the site root (`index-en.html`, `index-fr.html`); they are not linked from the blog header.

## Files to edit

| Concern | Location |
|--------|----------|
| Header markup, mobile menu script, theme toggle | [`hugo/layouts/partials/header.html`](../../hugo/layouts/partials/header.html) |
| Primary nav links (per language) | [`hugo/hugo.toml`](../../hugo/hugo.toml) — `[[languages.<lang>.menus.main]]` |
| Translatable strings (nav landmarks, a11y labels) | [`hugo/i18n/en.toml`](../../hugo/i18n/en.toml), [`hugo/i18n/fr.toml`](../../hugo/i18n/fr.toml) |

## Main menu (`hugo.toml`)

Entries use Hugo’s [menu system](https://gohugo.io/content-management/menus/). Each language block defines its own `main` menu:

- **`name`** — Link text (e.g. English “Posts”, French “Articles”).
- **`pageRef`** — Path to a section or page (e.g. `/posts`, `/search`).
- **`weight`** — Sort order (lower first).

Add or reorder items by duplicating an `[[languages.en.menus.main]]` (or `fr`) stanza and adjusting `name`, `pageRef`, and `weight`.

## `baseURL` (production)

Production `baseURL` is set in CI (see [GitHub Actions](./github-actions.md)) and must match the **canonical hostname** visitors use (for this site: `https://antoineboucher.info/<repo>/blog/`). If `baseURL` pointed only at `*.github.io` while pages are opened on a custom domain, stylesheets with Subresource Integrity and preloaded images would target `github.io` while inline CSS uses relative `./*.svg` URLs on the page origin—mixed origins break CSS and produce “preloaded but not used” warnings. Local default is in `hugo.toml`.

## Mobile menu (Paper theme)

The theme expects:

- **Hamburger** — Element with class **`btn-menu`** (now a `<button>`).
- **Panel** — Wrapper with class **`nav-wrapper`**.
- **State** — Class **`open`** on `<html>` (`document.documentElement`) toggles visibility/animation.

Do **not** rename `btn-menu`, `nav-wrapper`, or the `open` class without checking hugo-paper’s CSS (bundled `main.css`).

Behavior added in this project’s partial:

- **`aria-expanded`** and **open/close** labels on the menu button (from i18n).
- **Escape** closes the menu.
- **Activating any link** inside `.nav-wrapper` closes the menu (mainly for mobile).

## Dark mode

Also in `header.html`’s inline script:

- **`localStorage`** key: `dark` (`"true"` / `"false"`).
- **Class** `dark` on `<html>`.
- **`meta[name="theme-color"]`** updated for light/dark background.
- **`prefers-color-scheme`** — Listens for system theme changes; manual toggle still overrides via `localStorage`.

## Accessibility notes

- Language switcher uses `aria-label` from **`langCvNav`**.
- Primary section links use **`navMainSections`**; social icons use **`navSocial`**.
- Current location: **`aria-current="page"`** when `IsMenuCurrent` or `HasMenuCurrent` matches for that menu entry.

## Local preview

From the `hugo/` directory:

```bash
hugo server -D
```

Build only:

```bash
hugo --minify
```
