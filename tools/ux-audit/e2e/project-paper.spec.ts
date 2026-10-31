import { test, expect } from '@playwright/test';
import { readFileSync } from 'node:fs';
const sources = JSON.parse(readFileSync(new URL('../../../hugo/data/project_sources.json', import.meta.url), 'utf8'));
const prefix = process.env.E2E_PREFIX || '';

for (const theme of ['light', 'dark'] as const) {
  test(`all project sections and references ${theme}`, async ({ page }) => {
    test.setTimeout(360_000);
    await page.route('**/*', route => new URL(route.request().url()).hostname === '127.0.0.1' ? route.continue() : route.abort());
    await page.setViewportSize({ width: theme === 'light' ? 390 : 1280, height: 1000 });
    await page.emulateMedia({ colorScheme: theme, reducedMotion: 'reduce' });
    await page.addInitScript(dark => localStorage.setItem('dark', String(dark)), theme === 'dark');
    for (const file of Object.keys(sources)) {
      const slug = file.split('/')[2];
      const lang = file.endsWith('index.fr.md') ? 'fr/' : '';
      await page.goto(`${prefix}/blog/${lang}projects/notes/${slug}/`, { waitUntil: 'domcontentloaded' });
      const numbers = await page.locator('.repo-doc-content h2 > .project-section-number').allTextContents();
      expect(numbers.length, file).toBeGreaterThan(0);
      expect(numbers, file).toEqual(numbers.map((_, n) => `${n + 1}.`));
      expect(await page.locator('.repo-sidenav ol > li').count(), file).toBe(numbers.length);
      const broken = await page.locator('.repo-sidenav a').evaluateAll(links => links.filter(link => { const id = (link as HTMLAnchorElement).hash.slice(1); return !document.getElementById(id) && !document.getElementById(decodeURIComponent(id)); }).map(link => link.getAttribute('href')));
      expect(broken, file).toEqual([]);
      expect(await page.locator('.project-reference-entries > li').count(), file).toBe(sources[file].length);
      expect(sources[file].length, file).toBeGreaterThan(0);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 2), file).toBe(true);
    }
  });
  test(`project paper screenshots and navigation ${theme}`, async ({ page }, info) => {
    await page.setViewportSize({ width: theme === 'light' ? 390 : 1280, height: 1000 });
    await page.emulateMedia({ colorScheme: theme });
    await page.addInitScript(dark => localStorage.setItem('dark', String(dark)), theme === 'dark');
    await page.goto(`${prefix}/blog/projects/notes/chitui/`);
    const contents = page.locator('.repo-sidenav-disclosure');
    if (theme === 'light') await contents.locator(':scope > summary').click();
    await page.screenshot({ path: info.outputPath('numbered-project-contents.png') });
    const reference = page.locator('.project-paper-references');
    await reference.scrollIntoViewIfNeeded();
    await page.waitForTimeout(1000);
    await reference.scrollIntoViewIfNeeded();
    await reference.screenshot({ path: info.outputPath('project-references.png') });
    await expect(reference.locator('ol')).toHaveCSS('list-style-type', 'decimal');
  });
}
