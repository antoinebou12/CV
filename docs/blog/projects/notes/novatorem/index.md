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

## Use cases

Flask service that renders a Spotify or Last.fm now-playing card as an SVG for a GitHub profile README.

- **Show the now-playing card** (Profile owner, Spotify Web API): The catch-all route in api/orchestrator.py fetches the current track, extracts colours from the album art and returns an image/svg+xml card; vercel.json maps /api/spotify to it.
- **Customize card colours** (Profile owner): Query parameters background_color, border_color, background_type, show_status and compact are validated in api/config.py before rendering the Jinja2 template chosen in api/templates.json.
- **Use Last.fm as a source** (Profile owner, Last.fm API): When only LAST_FM_API_KEY and LAST_FM_USERNAME are set, or Spotify auth fails, get_now_playing switches to api/lastfm.py, which can pull album art from Deezer.
- **Open the current song** (Profile owner, Spotify Web API): GET /redirect sends the visitor to the track URL, or to the upstream repository when nothing is playing.
- **Renew the refresh token** (Profile owner, Spotify Web API): scripts/spotify_local_auth.py captures the OAuth code on http://127.0.0.1:8000/callback and writes a new refresh token, optionally pushing it to Vercel with --update-vercel.
- **Preview the card locally** (Profile owner): python start.py creates .venv, installs requirements, starts Flask on port 5000 and opens /preview; docker-compose.yml runs the same app with a /health check.

### Scenario: Add a Spotify card to a GitHub profile

1. Create a Spotify app with the redirect URI http://127.0.0.1:8000/callback.
2. Copy .env.example to .env and fill SPOTIFY_CLIENT_ID and SPOTIFY_SECRET_ID.
3. Run python scripts/spotify_local_auth.py to obtain SPOTIFY_REFRESH_TOKEN.
4. Run python start.py and check the card at http://127.0.0.1:5000/preview.
5. Deploy to Vercel and embed <deployment>/api/spotify as an image linked to /redirect in the profile README.

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


