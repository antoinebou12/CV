import { mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(resolve('tools/ux-audit/package.json'));
const { chromium } = require('playwright');

const base = (process.argv[2] || 'http://127.0.0.1:8765').replace(/\/$/, '');
const out = resolve(process.argv[3] || '.cursor/ux-loop/exp3-baseline');
await mkdir(out, { recursive: true });

const routes = [
  '/blog/',
  '/blog/recipes/',
  '/blog/recipes/champignon/',
  '/blog/recipes/spinach-goat-cheese-walnut-tart/',
  '/blog/projects/',
  '/blog/projects/notes/chitui/',
  '/blog/posts/',
];
const viewports = [
  { name: 'mobile', width: 390, height: 844 },
  { name: 'desktop', width: 1440, height: 1000 },
];

const browser = await chromium.launch({ headless: true });
const report = [];

for (const theme of ['light', 'dark']) {
  for (const viewport of viewports) {
    const context = await browser.newContext({ viewport, colorScheme: theme });
    await context.addInitScript((selected) => localStorage.setItem('dark', String(selected === 'dark')), theme);
    for (const route of routes) {
      const page = await context.newPage();
      const errors = [];
      page.on('console', (message) => {
        if (message.type() === 'error') errors.push(message.text());
      });
      const response = await page.goto(`${base}${route}`, { waitUntil: 'networkidle' });
      const metrics = await page.evaluate(() => {
        const visible = (element) => {
          const style = getComputedStyle(element);
          const rect = element.getBoundingClientRect();
          return style.display !== 'none' && style.visibility !== 'hidden' && Number(style.opacity) > 0 && rect.width > 0 && rect.height > 0;
        };
        const h1s = [...document.querySelectorAll('h1')].filter(visible);
        const main = document.querySelector('main');
        return {
          title: document.title,
          h1: h1s.length,
          h1Text: h1s.map((node) => node.textContent.trim()).slice(0, 2),
          overflow: document.documentElement.scrollWidth > innerWidth + 1,
          mainOverflow: main ? main.scrollWidth > main.clientWidth + 1 : false,
          hasRecipeBadge: !!document.querySelector('[data-post-kind="recipe"], .search-pill-recipe, .post-kind-recipe'),
          filterCount: document.querySelectorAll('.post-list-filters, .repo-explorer').length,
        };
      });
      const slug = route.replace(/^\/+|\/+$/g, '').replaceAll('/', '-') || 'root';
      const screenshot = `${theme}-${viewport.name}-${slug}.png`;
      await page.screenshot({ path: resolve(out, screenshot), fullPage: false });
      report.push({ route, theme, viewport: viewport.name, status: response?.status() ?? null, errors, screenshot, ...metrics });
      await page.close();
    }
    await context.close();
  }
}

await browser.close();
await writeFile(resolve(out, 'report.json'), `${JSON.stringify(report, null, 2)}\n`);
const fails = report.filter((item) => item.status !== 200 || item.h1 !== 1 || item.overflow);
console.log(`states=${report.length} structural_fails=${fails.length}`);
for (const item of fails) {
  console.log(`${item.route} ${item.theme} ${item.viewport}: status=${item.status} h1=${item.h1} overflow=${item.overflow} text=${JSON.stringify(item.h1Text)}`);
}
