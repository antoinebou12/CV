# Hugo blog: header and navigation

The static blog under [`hugo/`](../../hugo/) uses the [hugo-paper](https://github.com/nanxiaobei/hugo-paper) theme with a **custom header** that wires the blog to the root HTML CVs and bilingual content.

## Files to edit

| Concern | Location |
|--------|----------|
| Header markup, mobile menu script, theme toggle | [`hugo/layouts/partials/header.html`](../../hugo/layouts/partials/header.html) |
| Primary nav links (per language) | [`hugo/hugo.toml`](../../hugo/hugo.toml) — `[[languages.<lang>.menus.main]]` |
| Translatable strings (CV label, nav landmarks, a11y labels) | [`hugo/i18n/en.toml`](../../hugo/i18n/en.toml), [`hugo/i18n/fr.toml`](../../hugo/i18n/fr.toml) |

## Main menu (`hugo.toml`)

Entries use Hugo’s [menu system](https://gohugo.io/content-management/menus/). Each language block defines its own `main` menu:

- **`name`** — Link text (e.g. English “Posts”, French “Articles”).
- **`pageRef`** — Path to a section or page (e.g. `/posts`, `/search`).
- **`weight`** — Sort order (lower first).

Add or reorder items by duplicating an `[[languages.en.menus.main]]` (or `fr`) stanza and adjusting `name`, `pageRef`, and `weight`.

## CV link and `baseURL`

The header builds a URL to the **repository root** HTML CV (`index-en.html` / `index-fr.html`), not under `/blog/`.

Logic (see `header.html`):

1. Start from `site.BaseURL`.
2. Strip trailing `blog`, `/blog/`, etc., so the root matches the GitHub Pages site root next to the `blog/` subtree.
3. Append `index-en.html` or `index-fr.html` according to `site.Language.Lang`.

Production `baseURL` is set in CI (see [GitHub Actions](./github-actions.md)); local default is in `hugo.toml`. If you change hosting paths, keep this trim logic in sync with where the CV files are published.

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

- Language + CV cluster uses `aria-label` from **`langCvNav`**.
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
