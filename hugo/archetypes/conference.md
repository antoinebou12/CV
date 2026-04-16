---
# hugo new content posts/<slug>/index.md --kind conference
# post_kind: conference (or conference-recap; both render as conference)
post_kind: conference
title: "{{ replace .File.ContentBaseName `-` ` ` | title }}"
date: {{ now.Format "2006-01-02T15:04:05Z07:00" }}
lastmod: {{ now.Format "2006-01-02T15:04:05Z07:00" }}
draft: true
description: Event name, role, and one-line takeaway for cards and SEO.
translationKey: "{{ .File.ContentBaseName }}"
tags:
  - Conference
# images:
#   - featured.jpg
# canonicalURL: ""
# aliases: []
---

Opening: event, date, venue or format, and why it mattered to you.

## Highlights

- Takeaway one
- Takeaway two

## Closing thoughts

Short wrap-up.
