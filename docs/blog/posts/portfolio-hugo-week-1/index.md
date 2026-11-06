# Create a portfolio with Hugo (week 1)

> Week one of a Hugo portfolio — what the old repository held, a first Hugo links page, HBTheme tradeoffs, data embeds, Substack split, iframe shortcode, and what I would do differently today.

- HTML page: https://antoineboucher.info/CV/blog/posts/portfolio-hugo-week-1/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/posts/portfolio-hugo-week-1/index.md
- Published: 2024-01-06
- Updated: 2026-11-05
- Tags: Hugo, Portfolio, Static Site, Substack
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)Week one of moving my site to **Hugo** (January 2024): pick a theme, ship something fast, and prove the repo could carry more than a PDF résumé. This post is the log — where I started from, **HBTheme**, a data story embed, **Substack** in parallel, and a reusable **iframe** shortcode.

## Why Hugo and not a CMS

| Choice | Reason |
|--------|--------|
| **Static generation** | Cheap hosting, fast builds, no database to patch |
| **Markdown source** | Posts and projects live in git — reviewable diffs |
| **Modules** | Pull theme + partials without vendoring everything |

As an engineer I wanted the **repo as source of truth**: Markdown in, HTML out, deploy to GitHub Pages or similar. WordPress-style admin was overhead I would ignore after week two.

## Where I started from

Before week one, the repository behind my old site was a set of separate pieces, each with its own toolchain:

| Piece | How it was built | How it shipped |
|-------|------------------|----------------|
| **Web résumé** | `resume.json` (JSON Resume) exported with `resume-cli` and the *elegant* theme, plus a dark variant with *kendall* | The only GitHub Actions workflow: on every push, `npm ci`, `npm run build`, copy `index.html` to `dist/`, publish with `JamesIves/github-pages-deploy-action`. A Dockerfile could also serve it from `nginx:alpine` |
| **PDF CV** | LaTeX on the Russell class | PDF committed next to the source, no CI build |
| **Papers** | Two research PDFs in a folder | Static files |
| **Links page** | Hugo, built from the Lynx theme with Tailwind CSS | A Dockerfile running `hugo server`, no CI build |
| **Blog** | A git submodule pointing to a third-party Hugo theme (blist) | The blog content itself was no longer in the repository |

The last commit, a week before this post, deleted the old site folder. Week one started from that cleared ground: four toolchains (npm, LaTeX, Hugo, Docker) and only one of them deployed automatically.

## The first Hugo piece: a links page

The links page was my first real Hugo site, and it explains a lot of the choices I made later.

**Theme setup.** I had copied the Lynx theme into the site instead of using it as a theme: `theme.toml`, `layouts/` and `assets/` sat at the root. The theme’s own scaffolding came along too. A `netlify.toml` and a Lighthouse CI config both pointed at an `exampleSite` folder that did not exist in my copy. That is the main reason the table above says **Modules**: I wanted the next theme pulled in, not pasted in.

**Config.** Everything visible came from `config.toml`. `enableEmoji = true`, `disableKinds = ["taxonomy", "term"]` (no tag pages for a one-page site), and a `[module.hugoVersion]` block with `extended = false` and `min = "0.86.1"`. The links are a list of one-key tables, and the key does double duty:

```toml
[author]
  name = "Antoine Boucher"
  image = "profile.jpg"   # in static/
  links = [
    { github = "https://github.com/<user>" },
    { linkedin = "https://linkedin.com/in/<user>" },
    { email = "mailto:<user>@example.com" },
  ]
```

The home template loops over that list. The key (`github`) picks the icon `assets/icons/github.svg` and the label `link.github` from the i18n files. A value can also be a table with `href`, `icon`, `text`, `target` or `title` to override the defaults. The avatar is resized to 288×288 when Hugo can find it as a resource.

**CSS without Hugo extended.** Tailwind runs from an npm script and writes `assets/css/compiled/main.css`, which is committed. Hugo only has to bundle files, so the standard (non-extended) binary is enough. The head partial chains the steps:

```go-html-template
{{ $bundleCSS := $assets.Get "css" | resources.Concat "css/main.bundle.css" | resources.Minify | resources.Fingerprint "sha512" }}
```

The fingerprint also gives an `integrity` attribute on the `<link>` tag. An optional `assets/css/custom.css` is appended to the bundle when it exists.

**Content structure and i18n.** No posts, no sections: one home page, a `single.html` layout with a back link, and two translation files (`en.yaml`, `fr.yaml`) for link labels, the “Home” link and the footer (“Powered by” / “Propulsé par”). That was my first bilingual Hugo file, long before bilingual posts.

**Shortcodes.** Two small ones. `` inlines an SVG from `assets/icons/`. `…` wraps an intro paragraph in larger, muted text. The icon shortcode falls back to the i18n key `shortcode.icon_none` when the SVG is missing, but neither translation file defines that key, so a typo in an icon name rendered as an empty `<em>`. Small, but it taught me to grep i18n keys before trusting a theme’s fallback.

**Deployment.** The Dockerfile used `klakegg/hugo:0.101.0` and ran `server`, which is Hugo’s development server, not a static build. The Compose file mounted the project at `/app` while the image had copied the site into a different working directory, so edits on the host never reached the running container. Static HTML from `hugo --minify`, built in CI like the résumé, would have been simpler and faster.

## HBTheme in week one

**HBTheme** gave comments, npm-friendly assets, and Hugo modules so I did not rebuild layouts from zero.

Tradeoffs I noticed immediately:

- **Opinionated structure** — fast start, later fights when you want custom post types
- **Asset pipeline** — npm steps add CI time but keep SCSS/JS sane
- **Docs depth** — theme docs matter more than Hugo docs for week-one velocity

I would still pick a batteries-included theme for a personal site; I would budget time to **peel modules** once the site outgrows the defaults.

## Data on the page (not only posts)

Early experiment: embed a Montreal **car-theft** analysis (friend’s Substack project) inside Hugo pages — proof the stack could carry charts and longform, not only short posts like this one.

[Étude des vols de voitures à Montréal](https://mohamedilias.substack.com/p/etude-des-vols-de-voitures-a-montreal)

Lesson: **iframe or link-out** is fine for guest content you do not want to mirror; native Hugo charts would come later with page bundles and static assets.

## Substack in parallel

**Substack** for longer essays and a newsletter-shaped audience. Hugo for the portfolio shell and project index; Substack when the piece needs comments/email delivery without me running mail servers.

That split still makes sense: Hugo = canonical professional home; Substack = optional longform channel.

## Iframe shortcode

Posts can embed HTTPS pages with the site `iframe` shortcode (`src` required; optional `title`, `height`, `loading`, etc.):

```text

```

Example — old **FlashGames** demo still hosted on GitHub Pages:

Use iframes sparingly — accessibility, mobile height, and third-party cookie rules break more often than Hugo builds fail.

**Rationale in one line:** legacy demos (Flash-era games) still live on GitHub Pages; Hugo wraps them with a stable URL and my typography instead of maintaining two full front-ends.

## What I would do differently

Looking back at that repository with what the site became:

- **Pull themes as modules.** A copied theme brings its demo scaffolding and makes upstream fixes a manual merge.
- **Build static HTML in CI for every piece.** One workflow that runs `hugo --minify` and the résumé export, instead of a dev server in a container for one part and a workflow for another.
- **Keep translation files complete.** Every i18n key a template calls should exist in each language, including fallbacks.
- **Commit generated CSS only when it buys something.** Here it did: it let plain Hugo build without Node. With Hugo Pipes and a Node step in CI, it becomes noise in diffs.

## What changed since week one

The current site grew modules, bilingual posts, conference notes, and MCP-era tooling posts. Full log: **[Website refonte with Hugo (part 2)](https://antoineboucher.info/CV/blog/posts/portfolio-hugo-website-refonte/)**. Also **[professional résumé + JSON Resume](https://antoineboucher.info/CV/blog/posts/professional-resume-json-resume/)** and the blog index.

## Related posts

- [Website refonte with Hugo (part 2)](https://antoineboucher.info/CV/blog/posts/portfolio-hugo-website-refonte/) — Paper, bilingual model, MCP editorial loop
- [Software engineering journey](https://antoineboucher.info/CV/blog/posts/software-engineering-journey/) — career context the portfolio supports
- [Diagram prompts with ChatGPT and AIPRM](https://antoineboucher.info/CV/blog/posts/chatgpt-airprm-sequence-diagrams/) — documentation habits that feed the blog
