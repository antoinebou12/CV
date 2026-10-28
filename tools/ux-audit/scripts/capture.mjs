import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from '@playwright/test';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = resolve(root, '../..');
const fixtures = JSON.parse(readFileSync(resolve(root, 'fixtures.json'), 'utf8'));
const phase = process.env.PHASE || 'baseline';
const outDir = resolve(repoRoot, 'docs/ux-review', phase === 'baseline' ? 'baseline' : phase);
const hugoBase = process.env.SITE_URL || fixtures.hugoBase;
const cvBase = process.env.CV_URL || fixtures.cvBase;

mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch();
const manifest = [];

for (const route of fixtures.routes) {
  const base = route.kind === 'cv' ? cvBase : hugoBase;
  for (const theme of route.themes) {
    for (const vp of fixtures.viewports) {
      const page = await browser.newPage({
        viewport: { width: vp.width, height: vp.height },
        colorScheme: theme === 'dark' ? 'dark' : 'light',
      });
      const url = `${base}${route.path}`;
      try {
        await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45_000 });
        if (route.kind === 'hugo') {
          await page.evaluate((mode) => {
            document.documentElement.classList.toggle('dark', mode === 'dark');
          }, theme);
        }
        const name = `${route.id}__${theme}__${vp.name}.png`;
        const path = resolve(outDir, name);
        await page.screenshot({ path, fullPage: true });
        const metrics = await page.evaluate(() => {
          const body = getComputedStyle(document.body);
          const p = document.querySelector(
            '.repo-doc .repo-note-lead, .repo-doc .repo-overview p, .repo-directory-lead, .repo-directory .repo-directory-card p, main.prose p, #text-header .hero-place, #text-header',
          );
          const prose = p ? getComputedStyle(p) : body;
          return {
            overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
            bodyFontSize: prose.fontSize,
            bodyColor: prose.color,
            title: document.title,
          };
        });
        manifest.push({ route: route.id, theme, viewport: vp.name, file: name, url, ...metrics });
        console.log(`captured ${name}`);
      } catch (error) {
        manifest.push({ route: route.id, theme, viewport: vp.name, url, error: String(error) });
        console.error(`FAIL ${route.id} ${theme} ${vp.name}: ${error}`);
      } finally {
        await page.close();
      }
    }
  }
}

await browser.close();
writeFileSync(resolve(outDir, 'manifest.json'), JSON.stringify(manifest, null, 2));
console.log(`Wrote ${manifest.length} entries to ${outDir}`);
