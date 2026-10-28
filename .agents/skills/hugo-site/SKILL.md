---
name: hugo-site
description: >-
  Edits the Hugo blog: conference posts, Paper theme overrides, bilingual
  articles, search and list templates, and project pages. Use when changing
  hugo/ layouts, assets, i18n, post_kind, conference recaps, the Paper
  template, blog copy, or the projects catalog.
---

# Hugo site

The blog lives in `hugo/` (Paper theme). It is not driven by `data/cv.yaml`. Static CV pages (`index-en.html`, `index-fr.html`) are a different skill.

## Where to edit

| Change | Edit |
| --- | --- |
| Markup that should differ from Paper | `hugo/layouts/` (overrides win) |
| Blog 404 | `hugo/themes/paper/layouts/404.html` only. Leave generated copies under `docs/` alone |
| Header, menu, dark mode | `hugo/layouts/partials/header.html`, `hugo/hugo.toml` menus, `hugo/i18n/en.toml` and `hugo/i18n/fr.toml` |
| Look that the precompiled theme cannot express | `hugo/assets/editorial.css`, then `hugo/assets/custom.css` |
| Conference / article / tutorial cards | `hugo/layouts/partials/post-list-item.html`, `hugo/layouts/_default/list.html`, `hugo/layouts/_default/single.html`, `hugo/layouts/_default/search.html` |
| Project notes and catalog | Follow [project-docs](../project-docs/SKILL.md). Do not restyle CV Selected Projects from a Hugo task |

Do not rename `btn-menu`, `nav-wrapper`, or the `open` class on `<html>`. The mobile drawer and desktop nav both break at Tailwind `lg` (**1024px**). Do not switch that breakpoint to `md` (768px).

Do not add Tailwind utilities that are not already in the precompiled theme CSS. New rules go in `editorial.css` or `custom.css`.

## Post kinds

`post_kind` defaults to `article`. `conference-recap` is treated as `conference` in list, single, and search.

| Kind | List treatment |
| --- | --- |
| `article` | Article group, zinc badge |
| `conference` | Conference group, orange badge (`searchPillConference`) |
| `tutorial` | Tutorial group |
| section `projects` | Project badge; notes use `.repo-doc` |
| section `recipes` | Recipe badge |

A conference single gets class `conference-post`, the orange kicker, and a hero from the bundle featured image (`images/featured.png` via `featured-image-resource.html`). The visible lead is the markdown body. Front-matter `description` is for Open Graph only; the single template does not print it again.

## Bilingual posts

Every public post is a pair:

- `hugo/content/posts/<slug>/index.md`
- `hugo/content/posts/<slug>/index.fr.md`

Same `translationKey`, same `post_kind`, same `date`. English body links French with `{{< ref "/posts/<slug>/index.fr.md" >}}` near the first paragraph (`**[Version française](...)**`). French links back the same way.

Write from the source the user gave or from the repo. Do not invent metrics, employers, attendance, or outcomes. Short quotes only. Link the original event or post. Skip reposts that have no original text, and skip posts that only point at an article already in the repo.

When the post is about a project that already has `hugo/content/projects/notes/`, add the article link on that note in both languages. Do not add a new project card.

`<!--more-->` splits the list teaser. Set `mermaid: true` when the body has a Mermaid fence. GLB models use `{{< modelviewer >}}`.

## Conference copy shape

Match `hugo/content/posts/graphquon-2024-ets/index.md`:

```yaml
post_kind: conference
title: "Event — place"
date: 2024-11-09T09:00:00-05:00
description: "One sentence for cards and social previews."
translationKey: event-slug
tags: [Conference]
images: ["images/featured.png"]
```

Put the photo in the bundle. The template crops the single hero (`object-cover`, max height `min(26rem, 50vh)`). Card thumbs use `post-list-thumb-url.html`.

## Template changes

1. Decide kind vs layout. A new badge or group must update list, single, search, and both i18n files together.
2. Keep `conference-recap` aliased to `conference`.
3. Repo notes (`repository_note: true`) use the back link to `/projects` and skip the conference hero and the article-guide partial.
4. 404 copy stays readable without JavaScript: short “Page not found” / “Page introuvable”, plus links to the blog home, posts, English CV, and French CV.

## Verify

From `hugo/`:

```bash
hugo --minify
```

Check the changed list and one single in both languages. Conference cards stay in the conference group. Reduced motion and a failed remote asset must not remove the way home on 404.
