import { test, expect } from '@playwright/test';
import { readFileSync } from 'node:fs';

const data = JSON.parse(readFileSync(new URL('../../../hugo/data/repository_notes.json', import.meta.url), 'utf8'));
const prefix = process.env.E2E_PREFIX || '';

for (const theme of ['light', 'dark'] as const) {
  test(`all project layouts and C4 levels ${theme}`, async ({ page }) => {
    test.setTimeout(360_000);
    await page.route('**/*', route => new URL(route.request().url()).hostname === '127.0.0.1' ? route.continue() : route.abort());
    await page.setViewportSize({ width: 390, height: 900 });
    await page.emulateMedia({ colorScheme: theme, reducedMotion: 'reduce' });
    await page.addInitScript(dark => localStorage.setItem('dark', String(dark)), theme === 'dark');
    for (const note of data.notes) {
      await page.goto(`${prefix}/blog/projects/notes/${note.slug}/`, { waitUntil: 'domcontentloaded' });
      await expect(page.locator('h1')).toHaveCount(1);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 2), note.repo).toBe(true);
      const c4 = page.locator('#dossier-c4');
      if (await c4.count()) {
        expect(await c4.locator('.repo-uml-details, > p.repo-evidence-label').count(), note.repo).toBe(5);
      }
    }
  });
  test(`Mitsuba article assets and pipeline ${theme}`, async ({ page }) => {
    await page.emulateMedia({ colorScheme: theme });
    for (const lang of ['', 'fr/']) {
      await page.goto(`${prefix}/blog/${lang}posts/mistubavideo-rendered-video/`);
      const images = page.locator('article img');
      await images.evaluateAll(items => items.forEach(img => (img as HTMLImageElement).loading = 'eager'));
      await expect.poll(() => images.evaluateAll(items => items.every(img => (img as HTMLImageElement).complete && (img as HTMLImageElement).naturalWidth > 0))).toBe(true);
      await expect(page.locator('article')).toContainText('ManifestWriter');
      await expect(page.locator('article')).toContainText('render_config.json');
    }
  });
}
