import { test, expect } from '@playwright/test';
for (const width of [390, 768, 1440, 2560]) for (const theme of ['light', 'dark'] as const) {
  test(`article composition ${width} ${theme}`, async ({ page }, info) => {
    await page.setViewportSize({ width, height: 1100 });
    await page.emulateMedia({ colorScheme: theme, reducedMotion: 'reduce' });
    await page.addInitScript(dark => localStorage.setItem('dark', String(dark)), theme === 'dark');
    for (const lang of ['', 'fr/']) {
      await page.goto(`${process.env.E2E_PREFIX || ''}/blog/${lang}posts/ipc-toolkit-contact-library/`);
      await expect(page.locator('.single-post-content h2')).toHaveCount(3);
      await expect(page.locator('.single-post-content tbody tr')).toHaveCount(4);
      const bounds = await page.evaluate(() => {
        const box = selector => document.querySelector(selector).getBoundingClientRect().toJSON();
        return { body: box('.single-post-surface'), head: box('.article-heading'), refs: box('.article-references'), article: box('.journal-article'), figure: box('.article-diagram-figure img') };
      });
      expect(bounds.refs.top).toBeGreaterThanOrEqual(bounds.body.bottom);
      expect(Math.abs(bounds.head.left - bounds.body.left)).toBeLessThan(2);
      expect(bounds.article.width).toBeLessThanOrEqual(961);
      expect(bounds.figure.height).toBeLessThanOrEqual(421);
      expect(bounds.body.top - bounds.head.bottom).toBeLessThan(65);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
      await page.screenshot({ path: info.outputPath(`${lang ? 'fr' : 'en'}-article.png`), fullPage: true });
    }
  });
}
test('long inline code stays inside the mobile article column', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 1000 });
  await page.goto(`${process.env.E2E_PREFIX || ''}/blog/posts/blender-python-packages/`);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  await expect(page.locator('.single-post-content p code').first()).toHaveCSS('overflow-wrap', 'anywhere');
});
test('responsive comparison tables fit a phone screen', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 1000 });
  await page.goto(`${process.env.E2E_PREFIX || ''}/blog/posts/predicting-stock-prices-monte-carlo/`);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
});
