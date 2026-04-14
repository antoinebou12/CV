---
title: "{{ replace .File.ContentBaseName `-` ` ` | title }}"
description: One or two sentences for listings and SEO.
date: {{ .Date.Format "2006-01-02T15:04:05-07:00" }}
translationKey: {{ .File.ContentBaseName }}
images:
  - featured.jpg
tags:
  - Vegetarian
---

![Hero photo](./featured.jpg)

# {{ replace .File.ContentBaseName `-` ` ` | title }}

## Category

- **Type:** Vegetarian
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

⭐⭐⭐⭐ — Short tasting note.
