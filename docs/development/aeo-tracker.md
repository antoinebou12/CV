# AEO tracker configuration (external product)

After deploying CV changes, update the **AEO / Answer Engine** product settings for `https://antoineboucher.info/` so scores match your real positioning.

## Industry and services

| Field | English value |
|-------|----------------|
| **Industry** | Software engineering — platform, graphics, and secure cloud systems |
| **Products / services** | Platform and backend engineering, interactive graphics, GitLab/Kubernetes delivery, DevSecOps teaching and lab infrastructure |

Do **not** use generic “multi-cloud consulting firm” unless that is the brand you want models to cite.

## Suggested key prompts

Replace enterprise consulting prompts with prompts aligned to public content:

- Who is Antoine Boucher platform graphics engineer Montréal?
- What is uml-mcp MCP UML diagrams?
- DevSecOps LOG8100 teaching assistant Polytechnique
- IMC2 secure cloud platforms GitLab GKE Terraform

## On-site signals (repo)

| Artifact | Path |
|----------|------|
| Snippet lead | `index-en.html` / `index-fr.html` (`.aeo-lead.aeo-agent-only` at end of `<main>`) |
| About pages (hero, summary cards, nested FAQ) | `about-en.html` / `about-fr.html`; styles `css/cv-about-page.css` |
| FAQ + FAQPage JSON-LD | Same About pages; `Person.knowsAbout` in JSON-LD |
| Freshness | `article:modified_time`, `<time datetime>`, JSON-LD `dateModified` |
| Source data | `data/aeo.yaml` (`lead`, `hero`, `summaryCards`, `faq`, `recognition`, `technicalProfile`, `personKnowsAbout`) → `python scripts/build/generate_aeo_content.py --all` |

## After deploy

1. Merge to `main` and wait for the GitHub Actions deploy workflow (runs `generate_aeo_content.py` and `generate_person_jsonld.py`).
2. Purge Cloudflare cache (`/CV/`, `/.well-known/*`, `/llms.txt`, `/robots.txt`, `/CV/about-en.html`).
3. Run `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\verify-agent-ready-production.ps1 -SitePrefix /CV` — all checks should pass.
4. Re-run **AEO Readiness** on the tracker URL.

Until step 1–2 complete, production may still return **404** for `/.well-known/api-catalog` and stale `llms.txt` (missing `resume.md` links).
