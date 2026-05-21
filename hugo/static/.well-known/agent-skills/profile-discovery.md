# Profile discovery

Use this skill when you need a compact machine-readable overview of Antoine Boucher's public work and contact entry points.

## Inputs

- Site root: `https://antoineboucher.info/`
- CV root: `https://antoineboucher.info/CV/`
- Blog root: `https://antoineboucher.info/blog/`

## Recommended retrieval order

1. `/.well-known/api-catalog`
2. `/llms.txt` (or `/blog/llms.txt` before root promotion)
3. `/CV/about-en.html` or `/CV/about-fr.html` (FAQ and entity summary)
4. `/CV/resume.md` (English default) or `/CV/resume.json`
5. `/CV/index-en.html` or `/CV/index-fr.html`
6. `/blog/index.json`
7. `/blog/index.xml`

## Notes

- Public static content only.
- English Markdown/JSON resume is the default for international agents; French parallels use `resume-fr.md` and `resume-fr.json`.
- No authenticated API is currently exposed.
