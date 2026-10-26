---
post_kind: article
title: "Website refonte with Hugo (part 2)"
date: 2026-10-24T14:30:00-04:00
description: "Hugo portfolio refonte after week 1 — Paper theme, bilingual posts, post_kind and projects catalog, then MCP as the faster editorial loop."
translationKey: portfolio-hugo-website-refonte
tags:
  - Hugo
  - Portfolio
  - Paper
  - MCP
images:
  - images/featured.png
---

Week 1 proved the repo could carry more than a PDF résumé. This is the **refonte** log: same Hugo root, different product — **Paper** instead of HBTheme, **EN/FR** pairs, typed posts, a projects catalog, and **MCP** when a diagram or draft needs to land in git faster. Sequel to **[Create a portfolio with Hugo (week 1)]({{< ref "/posts/portfolio-hugo-week-1/index.md" >}})**. **[Version française]({{< ref "/posts/portfolio-hugo-website-refonte/index.fr.md" >}})**.

<!--more-->

## From HBTheme to Paper

HBTheme got the site online. Opinionated modules and an npm asset path were fine for week one; they fought custom layouts later.

The blog now runs on **[Paper](https://github.com/nanxiaobei/hugo-paper)** with project overrides: bilingual header and language switcher, dark mode, menus in `hugo.toml`, strings in `i18n`. The static HTML résumés stay at the site root (`index-en.html` / `index-fr.html`); the Hugo tree is the editorial shell, not a second CV renderer.

Lesson that stuck: pick a thin theme and own the partials you care about, instead of peeling a batteries-included stack for years.

## Bilingual posts as the default

Every public article is a pair:

- `hugo/content/posts/<slug>/index.md`
- `hugo/content/posts/<slug>/index.fr.md`

Same `translationKey`, same `date`, same `post_kind`. English links French near the top (and the reverse). That discipline beats a late “we should translate the blog” rewrite.

## `post_kind` and the projects catalog

List and search templates group content by kind — **article**, **conference**, **tutorial** — instead of one flat chronological dump. Conference posts get a distinct treatment (kicker, featured image from the page bundle); project work lives under `projects/` with repository notes so a repo can have a stable local write-up without stuffing everything into `/posts`.

The site stopped being “a theme with posts” and became a small content model: posts for narrative, projects for inventory, kinds for how cards and singles render.

## What the stack looks like now

Source of truth is still Markdown in git. The shape around it changed — static PNG below (light-theme capture; live Mermaid contrast is weak in dark mode). Source: [`site-refonte-flow.mmd`](./images/site-refonte-flow.mmd).

![Content in git → Paper site → static deploy, with uml-mcp and Cursor feeding Markdown](images/site-refonte-flow.png)

## MCP as the faster editorial loop

Week 1 embeds were iframes and link-outs. Diagrams for systems and pipelines now start in chat: **[uml-mcp]({{< ref "/posts/uml-mcp/index.md" >}})** turns Mermaid (or other Kroki-backed types) into something you save beside the post — `.mmd` in the page bundle, often with an SVG — then Hugo (or the Mermaid fence) shows it.

That is the improvement that matters for shipping posts: less copy-paste from a plugin playground, more “agent writes the diagram source into the repo.” When the live renderer fights dark mode, I keep the `.mmd` and ship a **light-theme PNG** in the page bundle (this post’s stack diagram). Cursor agents also draft and edit bilingual Markdown against the same tree, so the portfolio stays reviewable diffs instead of a CMS draft queue.

I still treat agent output as a first draft. The publish bar is the same as week 1: readable English and French, working links, diagrams that match the text.

## What did not change

| Still true | Why |
|------------|-----|
| **Repo as source of truth** | Markdown in, HTML out |
| **Static hosting** | Cheap, fast, no admin to patch |
| **Substack optional** | Longform / email when needed; Hugo remains the professional home |
| **Iframes sparingly** | Demos and guest embeds — not the core content model |

JSON Resume and the HTML CV sit next to this shell; see **[professional résumé + JSON Resume]({{< ref "/posts/professional-resume-json-resume/index.md" >}})**.

## Related posts

- [Create a portfolio with Hugo (week 1)]({{< ref "/posts/portfolio-hugo-week-1/index.md" >}}) — HBTheme, Substack split, iframe shortcode
- [uml-mcp — diagrams from chat via MCP]({{< ref "/posts/uml-mcp/index.md" >}}) — the diagram tooling this loop uses
- [Software engineering journey]({{< ref "/posts/software-engineering-journey/index.md" >}}) — career context the portfolio supports
