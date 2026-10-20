# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

- Recruiters and hiring managers evaluating Antoine Boucher for software engineering roles, especially platform, reliability, backend/cloud, and graphics or simulation work.
- Technical collaborators evaluating concrete projects, research, teaching, and open-source contributions.
- Human readers, ATS systems, search engines, and AI agents that need the same professional record in accessible, structured formats.

## Product Purpose

Present Antoine Boucher's professional profile and evidence in English and French, help visitors understand the combination of platform engineering and interactive graphics, and make it easy to inspect relevant work, download a CV, or make contact. Success means a visitor can quickly establish fit and credibility without reconstructing the story from disconnected profiles.

## Positioning

The site combines a concise bilingual CV, a deeper technical blog and project record, and machine-readable resume and discovery formats. Its distinguishing professional thread is **platform and graphics**: production systems, cloud delivery, security, teaching, and open source remain visible without displacing the graphics and simulation specialization.

## Operating Context

- The static CV pages are the fast evaluation surface; About pages add context without duplicating the full CV.
- The Hugo blog provides long-form posts, project pages, recipes, search, and bilingual navigation.
- PDF resumes support applications and printing; JSON Resume, Markdown, JSON-LD, `llms.txt`, and `.well-known` assets support automated readers.
- GitHub is the source of truth and GitHub Pages is the primary public deployment path. Docker and Kubernetes deployment assets are also maintained.
- Contact paths include email, GitHub, LinkedIn, and a Cal.com introduction call.

## Capabilities and Constraints

- English and French content must remain equivalent in structure and meaning.
- `index-en.html` and `index-fr.html` are canonical static CV pages; `index.html` is synchronized from English.
- About pages are generated from `data/aeo.yaml`; machine-readable resumes are generated from `data/resume.en.json` and `data/resume.fr.json`.
- The Hugo site under `hugo/` is built separately and merged into the deploy artifact.
- Public CV pages remain PDF- and contact-oriented and do not expose cover-letter links.
- Thesis descriptions may be public, but thesis PDF files must remain hidden from the public repository and deploy artifact.
- Existing factual claims, dates, metrics, links, and project ownership must not be invented or silently changed.

## Brand Commitments

- Use the name Antoine Boucher and lead with “Software Engineer — Platform and graphics” in English and “Ingénieur logiciel — Plateforme et infographie” in French.
- Keep the voice natural, direct, technically credible, and human rather than corporate or AI-sounding.
- Preserve the breadth of backend, security, cloud, teaching, and open-source work without leading with a long tool list.
- Treat the current portrait and published project assets as identity and evidence, not disposable decoration.

## Evidence on Hand

- Canonical resume data: `data/resume.en.json`, `data/resume.fr.json`, and `data/cv.yaml`.
- About and answer-engine content: `data/aeo.yaml`.
- Bilingual HTML CV and About pages at the repository root.
- Bilingual LaTeX CV sources and compiled resume artifacts under `cv-en/` and `cv-fr/`.
- Hugo posts and project pages under `hugo/content/`, including public project demonstrations and accepted contributions.
- Public GitHub repositories, certifications, teaching experience, recommendations, and employment history linked from the site.
- No future work may fabricate employers, clients, testimonials, benchmarks, awards, or usage metrics.

## Product Principles

1. Establish role fit quickly, then provide concrete evidence for deeper evaluation.
2. Keep English, French, printable, and machine-readable representations aligned.
3. Preserve factual precision and privacy over promotional embellishment.
4. Make technical breadth navigable while maintaining a clear platform-and-graphics narrative.
5. Prefer durable, progressively enhanced pages that remain useful without animation or client-side effects.

## Accessibility & Inclusion

The site must remain keyboard accessible, responsive from narrow mobile screens through desktop layouts, readable with reduced motion enabled, and usable with sufficient contrast and appropriately sized interactive targets. English and French visitors should receive equivalent navigation, content hierarchy, and contact paths.
