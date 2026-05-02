# Agent-ready baseline

Reproducible baseline for machine discovery, Cloudflare “Agent-Ready” style checks, and markdown negotiation.

## Source files (canonical)

| Artifact | Location |
|----------|----------|
| `robots.txt` | [`hugo/static/robots.txt`](../../hugo/static/robots.txt) |
| `llms.txt` | [`hugo/static/llms.txt`](../../hugo/static/llms.txt) |
| API catalog (RFC 9727-style JSON) | [`hugo/static/.well-known/api-catalog`](../../hugo/static/.well-known/api-catalog) |
| Markdown negotiation map | [`hugo/static/.well-known/markdown-map.json`](../../hugo/static/.well-known/markdown-map.json) |
| Agent skills index | [`hugo/static/.well-known/agent-skills/index.json`](../../hugo/static/.well-known/agent-skills/index.json) |
| Skill markdown | [`hugo/static/.well-known/agent-skills/*.md`](../../hugo/static/.well-known/agent-skills/) |
| Curated homepage markdown | [`hugo/static/agent/home.md`](../../hugo/static/agent/home.md) |
| HTTP headers (Cloudflare Pages / Netlify-style) | [`hugo/static/_headers`](../../hugo/static/_headers) |
| OAuth protected resource (RFC 9728, informational) | [`hugo/static/.well-known/oauth-protected-resource`](../../hugo/static/.well-known/oauth-protected-resource) |
| MCP server card (SEP-style stub) | [`hugo/static/.well-known/mcp/server-card.json`](../../hugo/static/.well-known/mcp/server-card.json) |
| OIDC / OAuth “not supported” stubs | [`hugo/static/.well-known/openid-configuration`](../../hugo/static/.well-known/openid-configuration), [`hugo/static/.well-known/oauth-authorization-server`](../../hugo/static/.well-known/oauth-authorization-server) |

Hugo copies `hugo/static/**` into the blog output directory. GitHub Actions then **promotes** `robots.txt`, `sitemap.xml`, `.well-known/**`, `_headers`, and root `llms.txt` to the **site root** so `https://antoineboucher.info/robots.txt` and `https://antoineboucher.info/.well-known/...` resolve. See [`.github/workflows/deploy.yml`](../../.github/workflows/deploy.yml).

`hugo.toml` sets `enableRobotsTXT = false` so Hugo does not overwrite the custom `robots.txt`.

## URL rewrite (GitHub Pages project sites)

When `vars.HUGO_BASE_URL` is **unset**, the default Hugo `baseURL` is `https://antoineboucher.info/<repo>/blog/`. Static discovery JSON uses `https://antoineboucher.info/blog/` placeholders; the deploy workflow rewrites those to include `<repo>/` for root copies.

If you set `HUGO_BASE_URL` to a custom value in GitHub **Variables**, that rewrite is skipped—keep URLs in `hugo/static` consistent with that base.

## Link headers

If the host honors `_headers` (e.g. Cloudflare Pages), the homepage exposes combined `Link` headers for `api-catalog`, `service-doc`, and `describedby`.

On Cloudflare **without** `_headers` support, mirror the same values with a **Transform Rule** (response headers) or a small Worker.

## Markdown negotiation (edge)

Static hosting alone cannot vary `Content-Type` by `Accept` for `/`. Use the Worker in [`cloudflare/workers/agent-ready-home/`](../../cloudflare/workers/agent-ready-home/README.md): it serves `/<SITE_REPO>/blog/agent/home.md` when `GET /` requests `text/markdown`.

## WebMCP (browser)

[`index-en.html`](../../index-en.html) and [`index-fr.html`](../../index-fr.html) register a minimal `open_cv_pdf` tool when `navigator.modelContext.provideContext` is available (Chrome WebMCP early preview). The API may change; registration is wrapped in `try`/`catch`.

## CI guards

The deploy workflow validates root `robots.txt`, `sitemap.xml`, JSON parse for `api-catalog` and `agent-skills/index.json`, and required fields on the skills index.

## Deferred (optional)

- Web Bot Auth (`/.well-known/http-message-signatures-directory`)
- OAuth/OIDC beyond explicit “not supported” placeholders under `hugo/static/.well-known/`
- MCP server card at `/.well-known/mcp/server-card.json`
- WebMCP browser tools
