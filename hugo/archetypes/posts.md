---
# hugo new content posts/<slug>/index.md
# Tutorial or conference templates: use --kind tutorials or --kind conference (see archetypes/tutorials.md, conference.md).
# post_kind: article | tutorial | conference (conference-recap is normalized like conference)
post_kind: article
title: "{{ replace .File.ContentBaseName `-` ` ` | title }}"
date: {{ now.Format "2006-01-02T15:04:05Z07:00" }}
lastmod: {{ now.Format "2006-01-02T15:04:05Z07:00" }}
draft: true
description: Short summary for cards, listings, and SEO (1–2 sentences).
translationKey: "{{ .File.ContentBaseName }}"
# weight: 0
# slug: "{{ .File.ContentBaseName }}"
# canonicalURL: "https://example.com/original"
# aliases:
#   - /posts/old-slug/
# author: ""
# comments: false
# math: true
# tags:
#   - Topic
# images:
#   - featured.png
---

Opening paragraph: what this post is for and who it helps.

<!--more-->

## Section

Body.
