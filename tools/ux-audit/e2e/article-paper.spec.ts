import { test, expect } from '@playwright/test';
import { readFileSync } from 'node:fs';
const sources = JSON.parse(readFileSync(new URL('../../../hugo/data/article_sources.json', import.meta.url), 'utf8'));
const prefix = process.env.E2E_PREFIX || '';

for (const theme of ['light', 'dark'] as const) {
  test(`all article paper structure ${theme}`, async ({ page }) => {
    test.setTimeout(360_000);
    await page.route('**/*', route => new URL(route.request().url()).hostname === '127.0.0.1' ? route.continue() : route.abort());
    await page.setViewportSize({ width: theme === 'light' ? 390 : 1280, height: 1000 });
    await page.emulateMedia({ colorScheme: theme, reducedMotion: 'reduce' });
    await page.addInitScript(dark => localStorage.setItem('dark', String(dark)), theme === 'dark');
    for (const file of Object.keys(sources)) {
      const slug = file.split('/')[1];
      const lang = file.endsWith('index.fr.md') ? 'fr/' : '';
      await page.goto(`${prefix}/blog/${lang}posts/${slug}/`, { waitUntil: 'domcontentloaded' });
      await expect(page.locator('article h1'), file).toHaveCount(1);
      expect(await page.locator('.article-topic-badges a').count(), file).toBeGreaterThan(0);
      expect(await page.locator('article img').count(), file).toBeGreaterThan(0);
      const numbers = await page.locator('.single-post-content h2 .article-section-number').allTextContents();
      expect(numbers.length, file).toBe(await page.locator('.single-post-content h2').count());
      expect(numbers, file).toEqual(numbers.map((_, n) => `${n + 1}.`));
      await expect(page.locator('.article-references'), file).toHaveCount(1);
      expect(await page.locator('.article-references li').count(), file).toBe(sources[file].length);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 2), file).toBe(true);
    }
  });
  test(`AINewsTracker paper navigation and images ${theme}`, async ({ page }, info) => {
    await page.setViewportSize({ width: theme === 'light' ? 390 : 1280, height: 1000 });
    await page.emulateMedia({ colorScheme: theme });
    await page.addInitScript(dark => localStorage.setItem('dark', String(dark)), theme === 'dark');
    for (const lang of ['', 'fr/']) {
      await page.goto(`${prefix}/blog/${lang}posts/ainewstracker-financial-news/`);
      const contents = page.locator('.article-contents');
      await contents.locator('summary').click();
      expect(await contents.locator('ol > li').count()).toBe(5);
      await expect(contents.locator('ol').first()).toHaveCSS('list-style-type', 'decimal');
      await expect(contents.locator('ol a').first()).toHaveCSS('display', 'inline');
      const destination = await contents.locator('a').first().getAttribute('href');
      await contents.locator('a').first().click();
      expect(decodeURIComponent(new URL(page.url()).hash)).toBe(decodeURIComponent(destination!));
      await page.locator('article img').evaluateAll(items => items.forEach(img => (img as HTMLImageElement).loading = 'eager'));
      await expect.poll(() => page.locator('article img').evaluateAll(items => items.every(i => (i as HTMLImageElement).complete && (i as HTMLImageElement).naturalWidth > 0))).toBe(true);
      await page.evaluate(() => scrollTo(0, 0));
      await page.screenshot({ path: info.outputPath(`${lang ? 'fr' : 'en'}-paper-top.png`) });
      await page.locator('.article-references').screenshot({ path: info.outputPath(`${lang ? 'fr' : 'en'}-references.png`) });
    }
  });
}
