# JavaScript unit tests

Run from `tools/ux-audit`:

```sh
npm ci
npx playwright install chromium
npm run test:unit
```

On this Windows workstation, use the existing browser cache if needed:

```powershell
$env:PLAYWRIGHT_BROWSERS_PATH='C:/Users/antoi/AppData/Local/ms-playwright'
npm run test:unit
```

These tests execute the production scripts against small DOM fixtures in Chromium.
They need no Hugo build, local server, external services, or new dependencies.
Each case gets a fresh page and storage. Network requests are intercepted, uncaught
script errors fail the test, and the typewriter test advances a controlled clock.

- `hero.spec.js`: bilingual themes, storage failures, reduced motion, typewriter
  cancellation, job disclosures, language links, skip-link focus, and widget prefetch.
- `blog.spec.js`: accent-insensitive glossary search, empty results, nested fragment
  disclosure, malformed fragments, and image-dialog behavior and keyboard focus.

These complement the `e2e/` suite. Real-page layout, contrast, Hugo templates, search
indexes, and external widget availability still need the end-to-end checks.
