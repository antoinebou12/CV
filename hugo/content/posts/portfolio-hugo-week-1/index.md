---
post_kind: article
title: "Create a portfolio with Hugo (week 1)"
date: 2024-01-06T10:00:00-04:00
lastmod: 2026-05-23T00:30:00-04:00
description: "Week one of a Hugo portfolio — theme choice, embedding data stories, Substack, and an iframe shortcode."
translationKey: portfolio-hugo-week-1
tags:
  - Hugo
  - Portfolio
  - Static Site
  - Substack
images:
  - featured.png
---

Week one of moving my site to **Hugo**: pick a theme, ship something fast, and wire in content that is not just a résumé PDF. This post is what I tried first — theme (**HBTheme**), a data-heavy embed, **Substack** on the side, and a reusable **iframe** shortcode. **[Version française]({{< ref "/posts/portfolio-hugo-week-1/index.fr.md" >}})**.

<!--more-->

![Site preview](./featured.png)

## Why Hugo

Static generation, short build times, and modules without a heavy CMS. As an engineer I wanted the repo to be the source of truth — Markdown in, HTML out, deploy somewhere cheap.

**HBTheme** had comments, npm-friendly assets, and enough Hugo modules that I did not rebuild every layout from scratch.

## Data on the page

Early experiment: embed a Montreal **car-theft** analysis (friend’s Substack project) inside Hugo pages — proof the stack could carry charts and longform, not only posts like this one.

[Étude des vols de voitures à Montréal](https://mohamedilias.substack.com/p/etude-des-vols-de-voitures-a-montreal)

## Substack in parallel

**Substack** for longer essays and a different audience. Hugo for the portfolio shell; Substack when the piece needs a newsletter shape.

## Iframe shortcode

Posts can embed HTTPS pages with the site `iframe` shortcode (`src` required; optional `title`, `height`, `loading`, etc.):

```text
{{</* iframe src="https://example.com/" title="Example" height="480" */>}}
```

Example — old **FlashGames** demo:

{{< iframe src="https://antoinebou12.github.io/FlashGames/" title="FlashGames" height="420" referrerpolicy="no-referrer-when-downgrade" >}}

## Next weeks (then)

More posts on Hugo modules, aesthetics (particles.js experiments), and tying the blog to coursework and projects. The current site evolved from this starting point — see other posts under **Posts** on the blog.
