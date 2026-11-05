# Create a portfolio with Hugo (week 1)

> Week one of a Hugo portfolio — HBTheme tradeoffs, data embeds, Substack split, iframe shortcode, and what I would do differently today.

- HTML page: https://antoineboucher.info/CV/blog/posts/portfolio-hugo-week-1/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/posts/portfolio-hugo-week-1/index.md
- Published: 2024-01-06
- Updated: 2026-05-22
- Tags: Hugo, Portfolio, Static Site, Substack
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)Week one of moving my site to **Hugo** (January 2024): pick a theme, ship something fast, and prove the repo could carry more than a PDF résumé. This post is the log — **HBTheme**, a data story embed, **Substack** in parallel, and a reusable **iframe** shortcode.

## Why Hugo and not a CMS

| Choice | Reason |
|--------|--------|
| **Static generation** | Cheap hosting, fast builds, no database to patch |
| **Markdown source** | Posts and projects live in git — reviewable diffs |
| **Modules** | Pull theme + partials without vendoring everything |

As an engineer I wanted the **repo as source of truth**: Markdown in, HTML out, deploy to GitHub Pages or similar. WordPress-style admin was overhead I would ignore after week two.

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

## What changed since week one

The current site grew modules, bilingual posts, conference notes, and MCP-era tooling posts. Full log: **[Website refonte with Hugo (part 2)](https://antoineboucher.info/CV/blog/posts/portfolio-hugo-website-refonte/)**. Also **[professional résumé + JSON Resume](https://antoineboucher.info/CV/blog/posts/professional-resume-json-resume/)** and the blog index.

## Related posts

- [Website refonte with Hugo (part 2)](https://antoineboucher.info/CV/blog/posts/portfolio-hugo-website-refonte/) — Paper, bilingual model, MCP editorial loop
- [Software engineering journey](https://antoineboucher.info/CV/blog/posts/software-engineering-journey/) — career context the portfolio supports
- [Diagram prompts with ChatGPT and AIPRM](https://antoineboucher.info/CV/blog/posts/chatgpt-airprm-sequence-diagrams/) — documentation habits that feed the blog
