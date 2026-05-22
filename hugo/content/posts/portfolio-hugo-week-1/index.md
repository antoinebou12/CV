---
post_kind: article
title: "Create a portfolio with Hugo (week 1)"
date: 2024-01-06T10:00:00-04:00
lastmod: 2026-05-22T16:00:00-04:00
description: "Week one of a Hugo portfolio — HBTheme tradeoffs, data embeds, Substack split, iframe shortcode, and what I would do differently today."
translationKey: portfolio-hugo-week-1
tags:
  - Hugo
  - Portfolio
  - Static Site
  - Substack
images:
  - featured.png
---

Week one of moving my site to **Hugo** (January 2024): pick a theme, ship something fast, and prove the repo could carry more than a PDF résumé. This post is the log — **HBTheme**, a data story embed, **Substack** in parallel, and a reusable **iframe** shortcode. **[Version française]({{< ref "/posts/portfolio-hugo-week-1/index.fr.md" >}})**.

<!--more-->

![Site preview after first deploy — HBTheme defaults with minimal overrides](./featured.png)

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
{{</* iframe src="https://example.com/" title="Example" height="480" */>}}
```

Example — old **FlashGames** demo still hosted on GitHub Pages:

{{< iframe src="https://antoinebou12.github.io/FlashGames/" title="FlashGames" height="420" referrerpolicy="no-referrer-when-downgrade" >}}

Use iframes sparingly — accessibility, mobile height, and third-party cookie rules break more often than Hugo builds fail.

**Rationale in one line:** legacy demos (Flash-era games) still live on GitHub Pages; Hugo wraps them with a stable URL and my typography instead of maintaining two full front-ends.

## What changed since week one

The current site grew modules, bilingual posts, conference notes, and MCP-era tooling posts. See **[professional résumé + JSON Resume]({{< ref "/posts/professional-resume-json-resume/index.md" >}})** and the blog index for how far the same Hugo root went.

## Related posts

- [Software engineering journey]({{< ref "/posts/software-engineering-journey/index.md" >}}) — career context the portfolio supports
- [Diagram prompts with ChatGPT and AIPRM]({{< ref "/posts/chatgpt-airprm-sequence-diagrams/index.md" >}}) — documentation habits that feed the blog
