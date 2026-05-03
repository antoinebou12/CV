# Agent-ready home: markdown negotiation

This Worker sits **in front of** your static origin (GitHub Pages, R2, or another host) and implements **Markdown for Agents** for the site root: when `Accept` contains `text/markdown`, `/` returns the curated markdown snapshot instead of HTML.

## Behavior

1. If `GET /` and `Accept` includes `text/markdown`, fetch `/<SITE_REPO>/blog/agent/home.md` from the origin (same host).
2. Respond with `Content-Type: text/markdown; charset=utf-8`.
3. Otherwise pass the request through to the origin unchanged.

`SITE_REPO` must match your GitHub Pages project segment (for this repo, typically `CV`).

## Deploy (Cloudflare Dashboard)

1. Create a Worker.
2. Paste `worker.mjs` as the module entry.
3. Add variable **Environment → Variables**:
   - `SITE_REPO` = `CV` (or your repository name as used in `https://antoineboucher.info/<repo>/blog/`).
4. Route the Worker on `antoineboucher.info/*` **before** the Pages origin, or use **Workers for Platforms** / **Routes** as appropriate for your zone.

### Cloudflare Pages (recommended)

Use a **Pages Function** or attach this script as a **Worker in front of Pages** with an **ASSETS** binding so the final line forwards to your built site. Without `ASSETS`, `fetch(request)` must resolve to your real origin hostname (avoid infinite loops on the same Worker route).

## Optional

- Extend `worker.mjs` to read `/.well-known/markdown-map.json` from the origin and support multiple paths (see `hugo/static/.well-known/markdown-map.json` in this repository).

## Cloudflare dashboard (proxy + GitHub Pages)

If you proxy GitHub Pages, also add **Transform Rules** for `Link` and `Content-Type` on `/.well-known/*` because the origin ignores `hugo/static/_headers`. See [Agent-ready baseline — Cloudflare proxy](../../docs/development/agent-ready-baseline.md#cloudflare-proxy-in-front-of-github-pages).
