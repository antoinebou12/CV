# novatorem: Music-provider data into an SVG widget

> This novatorem fork builds music-status widgets from provider data. A Flask orchestrator handles rendering, while Spotify and Last.fm have separate…

- HTML page: https://antoineboucher.info/CV/blog/projects/notes/novatorem/
- Language: en
- Translation (fr): https://antoineboucher.info/CV/blog/fr/projects/notes/novatorem/index.md
- Published: 2026-10-23
- Updated: 2026-10-23
- Author: Antoine Boucher (https://antoineboucher.info/CV/index-en.html)
- Repository: https://github.com/antoinebou12/novatorem
- License: Unlicense
- Inspected revision: 5496fe08e19da0da1042236b2600e77b6df39f5d

## Summary

This novatorem fork builds music-status widgets from provider data. A Flask orchestrator handles rendering, while Spotify and Last.fm have separate modules. Album artwork supplies both an image and colors for the SVG.

**Why it exists:** Real-time dynamic GitHub profile README updater streaming live Spotify listening status.

**Best fit:** Live GitHub profile personalization and webhook integration.

## Languages (GitHub Linguist bytes)

| Language | % |
| --- | ---: |
| Python | 81.61 |
| Jinja | 16.06 |
| HTML | 1.64 |
| Dockerfile | 0.64 |
| Procfile | 0.04 |

## Features and components

- **Provider and presentation** — api/orchestrator.py owns the Flask application and rendering helpers. Provider modules sit alongside it. Configuration controls templates and palettes, keeping service-specific data access separate from SVG appearance.
- **Artwork processing** — ImageData fetches artwork once per object and reuses the bytes for base64 output and ColorThief palettes. load_image_with_fallback tries artwork, then a placeholder, then default colors when image processing fails.

## Architecture

Components and connections verified in the repository.

- Spotify or Last.fm → Provider data
- Provider data → Flask orchestrator
- Flask orchestrator → Artwork and palette fallback
- Artwork and palette fallback → SVG template response

```mermaid
flowchart LR
  n0["Spotify or Last.fm"]
  n1["Provider data"]
  n2["Flask orchestrator"]
  n3["Artwork and palette fallback"]
  n4["SVG template response"]
  n0 --> n1
  n1 --> n2
  n2 --> n3
  n3 --> n4
```

**One path through the code:** Follow ImageData._fetch into get_base64 and get_palette. Reusing bytes avoids repeated image downloads within that object; it is not a persistent cross-request cache.

## Constraints and checks

The image fetch currently disables TLS verification with verify=False. That deserves correction before relying on remote artwork in a deployed instance.

## Files to read

- [api/orchestrator.py](https://github.com/antoinebou12/novatorem/blob/master/api/orchestrator.py)
- [api/spotify.py](https://github.com/antoinebou12/novatorem/blob/master/api/spotify.py)
- [api/lastfm.py](https://github.com/antoinebou12/novatorem/blob/master/api/lastfm.py)

