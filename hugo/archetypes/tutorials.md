---
# hugo new content posts/<slug>/index.md --kind tutorials
post_kind: tutorial
title: "{{ replace .File.ContentBaseName `-` ` ` | title }}"
date: {{ now.Format "2006-01-02T15:04:05Z07:00" }}
lastmod: {{ now.Format "2006-01-02T15:04:05Z07:00" }}
draft: true
description: What the reader will build or learn (1–2 sentences).
translationKey: "{{ .File.ContentBaseName }}"
# weight: 0
# slug: "{{ .File.ContentBaseName }}"
# canonicalURL: ""
# aliases: []
# tags:
#   - Tutorial
# images:
#   - featured.png
---

One paragraph: outcome and prerequisites in plain language.

<!--more-->

## Prerequisites

- Tool or version you assume

## Steps

### 1. First step

Content.

### 2. Next step

Content.

## Next steps

Optional follow-ups or related posts.
