# Content retrieval

Use this skill when you need post or project content from the public site in deterministic formats.

## Primary endpoints

- JSON listing: `https://antoineboucher.info/blog/index.json`
- RSS feed: `https://antoineboucher.info/blog/index.xml`
- Root sitemap (URL discovery): `https://antoineboucher.info/CV/sitemap.xml`
- Hugo sitemap (same graph, under blog output): `https://antoineboucher.info/CV/blog/sitemap.xml`

## Guidance

- Prefer JSON for indexing and feed-like scans.
- Use sitemap as the canonical URL discovery source.
- Use HTML pages for rendering-oriented extraction.
