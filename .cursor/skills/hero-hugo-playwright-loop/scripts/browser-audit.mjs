import { mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const args = process.argv.slice(2);
const value = (flag, fallback) => {
  const index = args.indexOf(flag);
  return index >= 0 && args[index + 1] ? args[index + 1] : fallback;
};

const baseUrl = value('--base-url', 'http://127.0.0.1:8765').replace(/\/$/, '');
const outputDir = resolve(value('--out-dir', '.cursor/ux-loop/latest'));
const routes = [
  '/index-en.html',
  '/index-fr.html',
  '/blog/',
  '/blog/projects/',
  '/blog/projects/notes/chitui/',
  '/blog/projects/notes/tch099/',
];
const viewports = [
  { name: 'mobile', width: 390, height: 844 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1440, height: 1000 },
];

let chromium;
try {
  ({ chromium } = await import('playwright'));
} catch {
  console.error('Playwright is not installed. Use Cursor browser tools with EVALUATION.md, or ask before adding the dependency.');
  process.exit(2);
}

await mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const report = [];

for (const theme of ['light', 'dark']) {
  for (const viewport of viewports) {
    const context = await browser.newContext({ viewport, colorScheme: theme });
    await context.addInitScript(selected => localStorage.setItem('dark', String(selected === 'dark')), theme);
    for (const route of routes) {
      const page = await context.newPage();
      const errors = [];
      page.on('console', message => {
        if (message.type() === 'error') errors.push(message.text());
      });
      page.on('pageerror', error => errors.push(error.message));
      const response = await page.goto(`${baseUrl}${route}`, { waitUntil: 'networkidle' });
      const metrics = await page.evaluate(() => {
        const root = document.documentElement;
        const main = document.querySelector('main');
        const visible = element => {
          const style = getComputedStyle(element);
          const rect = element.getBoundingClientRect();
          return style.display !== 'none' && style.visibility !== 'hidden' && Number(style.opacity) > 0 && rect.width > 0 && rect.height > 0;
        };
        return {
          title: document.title,
          h1: [...document.querySelectorAll('h1')].filter(visible).length,
          pageOverflow: root.scrollWidth > innerWidth + 1,
          mainOverflow: main ? main.scrollWidth > main.clientWidth + 1 : false,
          diagramControls: document.querySelectorAll('[aria-label="Diagram controls"], [aria-label="Commandes du diagramme"]').length,
          initialZoom: [...document.querySelectorAll('.diagram-tools output')].map(node => node.textContent.trim()),
          focusable: document.querySelectorAll('a[href], button, input, select, summary, [tabindex="0"]').length,
        };
      });
      const slug = route.replace(/^\/+|\/+$/g, '').replaceAll('/', '-') || 'root';
      const screenshot = `${theme}-${viewport.name}-${slug}.png`;
      await page.screenshot({ path: resolve(outputDir, screenshot), fullPage: true });
      report.push({ route, theme, viewport, status: response?.status() ?? null, errors, screenshot, ...metrics });
      await page.close();
    }
    await context.close();
  }
}

await browser.close();
await writeFile(resolve(outputDir, 'report.json'), `${JSON.stringify(report, null, 2)}\n`);

const failures = report.filter(item => item.status !== 200 || item.errors.length || item.h1 !== 1 || item.pageOverflow);
console.log(`Audited ${report.length} page states. ${failures.length} hard failures.`);
if (failures.length) {
  for (const item of failures) console.error(`${item.route} ${item.theme} ${item.viewport.name}: status=${item.status} h1=${item.h1} overflow=${item.pageOverflow} errors=${item.errors.length}`);
  process.exitCode = 1;
}
