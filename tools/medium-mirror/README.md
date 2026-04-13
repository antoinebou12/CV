# Medium → Hugo importer

Fetches public Medium story HTML with Playwright, downloads images into a [Hugo page bundle](https://gohugo.io/content-management/page-bundles/), and writes Markdown (via Turndown).

## Setup

```bash
cd tools/medium-mirror
npm install
npx playwright install chromium
```

## Run

From `tools/medium-mirror`:

```bash
npm run import
```

This writes to `../../hugo/content/posts/<slug>/` (see `urls.json`).

Then verify the site:

```bash
cd ../../hugo
hugo --gc
```

## Adjusting selectors

If extraction returns empty or truncated text, edit `SELECTORS` in `import.mjs` to match Medium’s current DOM. Use Playwright Inspector: `PWDEBUG=1 node import.mjs` (run one URL first by temporarily trimming `urls.json`).

## Paywalled stories

If a story only loads when logged in, create a storage state once (`await context.storageState({ path: 'auth.json' })`) and load it in the script — **do not commit** `auth.json`.

## CI

The generated Markdown and images are meant to be **committed**; this tool is not run in GitHub Actions by default.
