---
# hugo new content projects/<slug>/index.md
title: "{{ replace .File.ContentBaseName `-` ` ` | title }}"
date: {{ now.Format "2006-01-02T15:04:05Z07:00" }}
lastmod: {{ now.Format "2006-01-02T15:04:05Z07:00" }}
draft: true
description: One or two sentences for project cards and SEO (repo, problem, stack).
translationKey: "{{ .File.ContentBaseName }}"
# weight: 0
# slug: "{{ .File.ContentBaseName }}"
# tags:
#   - Rust
# images:
#   - featured.png
# aliases: []
---

## {{ replace .File.ContentBaseName `-` ` ` | title }}

Link the canonical repo or demo in the first paragraph.

### Features

- One
- Two

### Related

- Optional related project or doc link
