/* Run with CODEX_NODE_MODULES pointing to the Playwright runtime, if needed. */
const assert = require('node:assert/strict');
const { createRequire } = require('node:module');
const { mkdirSync } = require('node:fs');
const { resolve } = require('node:path');

const { chromium } = process.env.CODEX_NODE_MODULES
  ? createRequire(resolve(process.env.CODEX_NODE_MODULES, 'package.json'))('playwright')
  : require('playwright');

const base = process.env.HUGO_PREVIEW || 'http://localhost:1313/blog';
const output = resolve('tmp/project-notes-check');
const pages = [
  { slug: 'artemis-switch', markdown: true },
  { slug: 'tch099', api: true, deployment: true },
  { slug: 'sm64coopdx-switch-n3ds' },
];

(async () => {
  mkdirSync(output, { recursive: true });
  const browser = await chromium.launch({ headless: true, channel: 'chrome' });
  let states = 0;
  try {
    for (const width of [390, 1440]) {
      for (const project of pages) {
        const context = await browser.newContext({
          viewport: { width, height: 1000 },
          colorScheme: width === 390 ? 'dark' : 'light',
          reducedMotion: 'reduce',
        });
        const page = await context.newPage();
        const errors = [];
        page.on('pageerror', error => errors.push(error.message));
        const response = await page.goto(`${base}/projects/notes/${project.slug}/`, { waitUntil: 'networkidle' });
        assert.equal(response.status(), 200);
        assert.equal(await page.locator('h1').count(), 1, `${project.slug} has one page heading`);
        assert.equal(errors.length, 0, `${project.slug} has no page errors: ${errors.join('; ')}`);
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth + 2), true, `${project.slug} does not overflow at ${width}px`);

        const nav = await page.locator('.repo-sidenav a').allTextContents();
        assert.ok(nav.indexOf('Architecture') < nav.indexOf('Getting started'), 'Architecture precedes setup in the page navigation');
        assert.equal(await page.locator('.repo-mermaid-source:visible').count(), 0, 'Raw Mermaid source stays hidden');

        if (project.markdown) {
          const rendered = page.locator('.repo-source-markdown');
          assert.ok(await rendered.count() > 0, 'Repository excerpts render as Markdown');
          assert.ok(await rendered.locator('table, ul, ol, p').count() > 0, 'Rendered excerpts contain structured HTML');
        }
        if (project.api) {
          assert.ok(await page.locator('.repo-api-notes li').count() >= 8, 'API responses use readable bullet points');
        }
        if (project.deployment) {
          assert.equal(await page.getByText('Services described in').count(), 0, 'Redundant service caption is removed');
          await page.locator('.repo-deployment-diagram').scrollIntoViewIfNeeded();
          await page.locator('.repo-deployment-diagram .diagram-tools').waitFor({ state: 'visible' });
          assert.equal(await page.locator('.repo-deployment-diagram .diagram-tools button').count(), 6, 'Deployment diagram exposes all controls');
        } else {
          const primary = page.locator('.is-primary-diagram');
          if (await primary.count()) {
            await primary.locator(':scope > summary').click();
            await primary.locator('.diagram-tools').waitFor({ state: 'visible' });
          }
        }

        await page.screenshot({ path: resolve(output, `${project.slug}-${width}.png`), fullPage: true });
        await context.close();
        states += 1;
      }
    }
    console.log(`Passed ${states} project note states with responsive layout, rendered Markdown, API structure, and interactive diagrams.`);
  } finally {
    await browser.close();
  }
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
