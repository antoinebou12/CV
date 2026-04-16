---
# hugo new content <path>/index.md  (fallback when no section archetype matches)
title: "{{ replace .File.ContentBaseName `-` ` ` | title }}"
date: {{ now.Format "2006-01-02T15:04:05Z07:00" }}
lastmod: {{ now.Format "2006-01-02T15:04:05Z07:00" }}
draft: true
description: ""
# slug: "{{ .File.ContentBaseName }}"
# weight: 0
# aliases:
#   - /old-url/
# translationKey: "{{ .File.ContentBaseName }}"
---

Summary paragraph. For blog posts prefer `hugo new posts/<slug>/index.md` (see `archetypes/posts.md`). For recipes use `hugo new recipes/<slug>/index.md`.
