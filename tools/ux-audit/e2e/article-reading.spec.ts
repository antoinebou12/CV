import { test, expect } from '@playwright/test';
const prefix = process.env.E2E_PREFIX || '';

for (const width of [390, 768, 1280]) for (const theme of ['light', 'dark'] as const) {
  test(`article reading ${width} ${theme}`, async ({ page }, info) => {
    await page.context().grantPermissions(['clipboard-read', 'clipboard-write']);
    await page.setViewportSize({ width, height: 1000 });
    await page.emulateMedia({ colorScheme: theme, reducedMotion: 'reduce' });
    await page.addInitScript(dark => localStorage.setItem('dark', String(dark)), theme === 'dark');
    for (const lang of ['', 'fr/']) {
      await page.goto(`${prefix}/blog/${lang}posts/mistubavideo-rendered-video/`);
      await expect(page.locator('.article-single-hero')).toHaveCount(0);
      await expect(page.locator('.single-post-content figure').filter({ has: page.locator('img') })).toHaveCount(2);
      const lead = page.locator('.single-post-content > p').first();
      expect((await lead.boundingBox())!.y).toBeLessThan(950);
      expect(await page.locator('.article-heading .repo-article-guides').count()).toBe(1);
      const contents = page.locator('.article-contents');
      await contents.locator('summary').click();
      await expect(contents.locator('nav')).toBeVisible();
      await expect(contents.locator('a').first()).toHaveAttribute('href', /^#/);
      await contents.locator('summary').click();
      const caption = page.locator('figcaption').first();
      await expect(caption).toHaveCSS('font-style', 'normal');
      await expect(caption).toHaveCSS('font-size', '14px');
      const copy = page.locator('pre').filter({ has: page.locator('code.language-bash') }).first().locator('.repo-copy');
      await copy.click();
      await expect(copy).toHaveText(lang ? 'Copié' : 'Copied');
      expect(await page.evaluate(() => navigator.clipboard.readText())).toContain('mitsuba-video inspect');
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 2)).toBe(true);
      await page.evaluate(() => scrollTo(0, 0));
      await page.screenshot({ path: info.outputPath(`${lang ? 'fr' : 'en'}-top.png`) });
      await caption.scrollIntoViewIfNeeded();
      await page.screenshot({ path: info.outputPath(`${lang ? 'fr' : 'en'}-caption.png`) });
    }
  });
}

test('diagram source stays available when the renderer cannot load', async ({ page }) => {
  await page.route('https://cdn.jsdelivr.net/**', route => route.abort());
  const errors: string[] = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.goto(`${prefix}/blog/posts/mistubavideo-rendered-video/`);
  const fallback = page.locator('.article-diagram-loading');
  await expect(fallback.locator('summary')).toContainText('unavailable');
  await expect(fallback.locator('code')).not.toBeVisible();
  await fallback.locator('summary').click();
  await expect(fallback.locator('code')).toBeVisible();
  expect(errors).toEqual([]);
});
