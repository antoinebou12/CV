---
# hugo new content recipes/<slug>/index.md
title: "{{ replace .File.ContentBaseName `-` ` ` | title }}"
description: One or two sentences for listings and SEO.
date: {{ now.Format "2006-01-02T15:04:05Z07:00" }}
lastmod: {{ now.Format "2006-01-02T15:04:05Z07:00" }}
draft: true
translationKey: "{{ .File.ContentBaseName }}"
# tags:
#   - Vegetarian
# images:
#   - featured.jpg
---

<!-- Add featured.jpg (or .png) in this folder and list it under images: in front matter for cards. -->

## Category

- **Type:**
- **Main ingredient:**
- **Preparation time:**
- **Cooking time:**
- **Total time:**
- **Servings:**

## Ingredients

- Item one
- Item two

## Instructions

1. Step one
2. Step two

## Notes

Optional tips or substitutions.

## Review

Optional tasting note.
