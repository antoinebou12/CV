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
| JSON Resume (canonical) | [`data/resume.en.json`](../../data/resume.en.json), [`data/resume.fr.json`](../../data/resume.fr.json) |
| Plain Markdown CV (generated) | [`resume.md`](../../resume.md), [`resume-fr.md`](../../resume-fr.md) |
| JSON Resume (deployed) | [`resume.json`](../../resume.json), [`resume-fr.json`](../../resume-fr.json) |

Hugo copies `hugo/static/**` into the blog output directory. GitHub Actions then **promotes** `robots.txt`, `sitemap.xml`, `.well-known/**`, `_headers`, and root `llms.txt` to the **site root** so `https://antoineboucher.info/robots.txt` and `https://antoineboucher.info/.well-known/...` resolve. See [`.github/workflows/deploy.yml`](../../.github/workflows/deploy.yml).

`hugo.toml` sets `enableRobotsTXT = false` so Hugo does not overwrite the custom `robots.txt`.

## URL rewrite (GitHub Pages project sites)

When `vars.HUGO_BASE_URL` is **unset**, the default Hugo `baseURL` is `https://antoineboucher.info/<repo>/blog/`. Static discovery JSON uses `https://antoineboucher.info/blog/` placeholders; the deploy workflow rewrites those to include `<repo>/` for root copies.

If you set `HUGO_BASE_URL` to a custom value in GitHub **Variables**, that rewrite is skipped—keep URLs in `hugo/static` consistent with that base.

## Link headers

If the host honors `_headers` (e.g. Cloudflare Pages), the homepage exposes combined `Link` headers for `api-catalog`, `service-doc`, and `describedby`.

On Cloudflare **without** `_headers` support, mirror the same values with a **Transform Rule** (response headers) or a small Worker.

## Cloudflare proxy in front of GitHub Pages

GitHub Pages **does not** interpret [`hugo/static/_headers`](../../hugo/static/_headers). With the **orange-cloud** proxy, add the following in the Cloudflare dashboard (or Terraform) so scanners see the same behavior as a native Pages deploy.

### 1) Ship the repo artifact first

Merge to `main` / `master`, ensure [`.github/workflows/deploy.yml`](../../.github/workflows/deploy.yml) succeeds, then **purge cache** for the zone (Caching → Configuration → Purge Everything, or custom purge: `/robots.txt`, `/sitemap.xml`, `/.well-known/*`, `/`).

**Production spot-check** (Windows PowerShell): `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\verify-agent-ready-production.ps1 -SitePrefix /CV`

After deploy and Cloudflare cache purge, verify these resolve (apex paths are promoted from `_site`; CV static pages live under `/CV/`):

| URL | Expected |
|-----|----------|
| `https://antoineboucher.info/robots.txt` | Custom robots with `Sitemap:` → `/CV/sitemap.xml` |
| `https://antoineboucher.info/llms.txt` | Identity block + machine-readable resume links |
| `https://antoineboucher.info/.well-known/api-catalog` | JSON linkset (not 404) |
| `https://antoineboucher.info/CV/resume.md` / `resume.json` | Deployed artifacts |
| `https://antoineboucher.info/CV/about-en.html` | English FAQ (AEO answer target) |

If `/.well-known/api-catalog` still returns **404** or HTML, the promoted artifact is not live yet or orange-cloud cache/rules need the Transform Rules in §3 below.

### 2) Response header Transform Rules (Link on homepage)

Rules → Transform Rules → **Modify response header** (or Response Header Transform Rules, product wording varies).

| Rule name | When (expression) | Set header | Value |
|-----------|-------------------|------------|--------|
| `AgentLinkHome` | `(http.host eq "antoineboucher.info" and (http.request.uri.path eq "/" or http.request.uri.path eq "/index.html"))` | `Link` | `</.well-known/api-catalog>; rel="api-catalog"; type="application/linkset+json", </.well-known/agent-skills/index.json>; rel="service-doc"; type="application/json", </llms.txt>; rel="describedby"; type="text/plain"` |

Use **one** `Link` header value (comma-separated relations per RFC 8288). Adjust `http.host` if you use `www`.

### 3) Response Content-Type for discovery JSON

Add separate **Modify response header** rules (or one rule with a map in a Worker) so paths under `/.well-known/` return JSON types instead of `text/html`:

| When | Set `Content-Type` |
|------|---------------------|
| `http.request.uri.path eq "/.well-known/api-catalog"` | `application/linkset+json; charset=utf-8` |
| `http.request.uri.path eq "/.well-known/openid-configuration"` or `.../oauth-authorization-server` or `.../oauth-protected-resource` or `.../mcp/server-card.json` | `application/json; charset=utf-8` |

### 4) Markdown for Agents

Either:

- Enable **Markdown for Agents** on the zone (Cloudflare dashboard: see [Markdown for Agents](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/) in current docs for the exact menu path), **or**
- Deploy the Worker in [`cloudflare/workers/agent-ready-home/`](../../cloudflare/workers/agent-ready-home/README.md) on a route that runs **before** the origin, with `SITE_REPO` matching the GitHub Pages path segment (e.g. `CV`).

## Markdown negotiation (edge)

Static hosting alone cannot vary `Content-Type` by `Accept` for `/`. Use the Worker in [`cloudflare/workers/agent-ready-home/`](../../cloudflare/workers/agent-ready-home/README.md): it serves `/<SITE_REPO>/blog/agent/home.md` when `GET /` requests `text/markdown`.

## WebMCP (browser)

[`index.html`](../../index.html) (homepage before redirect), [`index-en.html`](../../index-en.html), and [`index-fr.html`](../../index-fr.html) register a minimal `open_cv_pdf` tool when `navigator.modelContext.provideContext` is available (Chrome WebMCP early preview). The API may change; registration is wrapped in `try`/`catch`.

## AEO readiness (answer engines)

- **Copy source:** [`data/aeo.yaml`](../../data/aeo.yaml) (lead, FAQ, `lastUpdated`).
- **Regenerate:** `python scripts/build/generate_aeo_content.py --all` → [`about-en.html`](../../about-en.html), [`about-fr.html`](../../about-fr.html), patches CV lead/freshness/nav.
- **JSON-LD:** FAQPage on About pages; Person/WebSite/Speakable on CV via `generate_person_jsonld.py --all`.
- **Tracker UI:** see [`aeo-tracker.md`](aeo-tracker.md). Off-site alignment: [`offsite-entity-alignment.md`](offsite-entity-alignment.md).

## Machine-readable resume and SEO

- **Source of truth:** edit `data/resume.en.json` / `data/resume.fr.json`, then run:
  - `python scripts/build/render_resume_md.py --all`
  - `python scripts/build/generate_aeo_content.py --all`
  - `python scripts/build/generate_person_jsonld.py --all`
- **English default:** `resume.md`, `resume.json`, `hreflang` `x-default` → `index-en.html`; French parallels: `resume-fr.md`, `resume-fr.json`, `index-fr.html`.
- **Person JSON-LD** is injected between `<!-- PERSON_JSONLD:BEGIN -->` / `END` in `index-en.html` and `index-fr.html` (`jobTitle`, `knowsAbout`, `alumniOf`, `worksFor`, selected projects).
- **Sitemap:** `scripts/deploy/merge_root_sitemap.py` appends CV static URLs and `xhtml:link` alternates for EN/FR HTML and resume pairs; `robots.txt` already references `Sitemap:` (rewritten in deploy).

## CI guards

The deploy workflow validates root `robots.txt`, `sitemap.xml`, JSON parse for `api-catalog` and `agent-skills/index.json`, required fields on the skills index, and presence of `resume.md` / `resume.json` in `_site` and the merged sitemap.

## Deferred (optional)

- Web Bot Auth (`/.well-known/http-message-signatures-directory`)
- Full OIDC/OAuth authorization server metadata (beyond “not supported” stubs) if you add token APIs
