import { test, expect } from '@playwright/test';
const prefix = process.env.E2E_PREFIX || '';
for (const width of [390, 768, 1440]) for (const theme of ['light', 'dark'] as const) {
  test(`reader components ${width} ${theme}`, async ({ page }, info) => {
    await page.setViewportSize({ width, height: 1000 });
    await page.emulateMedia({ colorScheme: theme, reducedMotion: 'reduce' });
    await page.addInitScript(dark => localStorage.setItem('dark', String(dark)), theme === 'dark');
    const errors: string[] = [];
    page.on('pageerror', error => errors.push(error.message));
    for (const lang of ['', 'fr/']) {
      await page.goto(`${prefix}/blog/${lang}projects/notes/artemis-switch/`);
      await expect(page.locator('.reader-launch')).toBeVisible();
      await expect(page.locator('.repo-snapshot-cards > div')).toHaveCount(3);
      await page.screenshot({ path: info.outputPath(`${lang ? 'fr' : 'en'}-overview.png`) });
      await page.locator('.reader-launch [data-reader-search]').click();
      const sheet = page.locator('#reader-search');
      await expect(sheet).toBeVisible();
      await expect(page.locator('#reader-query')).toBeFocused();
      await page.locator('#reader-query').fill('zzzz-no-section');
      await expect(page.locator('#reader-results li')).toHaveCount(0);
      await expect(page.locator('#reader-result-count')).not.toBeEmpty();
      await page.locator('[data-reader-clear]').click();
      await page.locator('[data-reader-filter=diagram]').click();
      await expect(page.locator('[data-reader-filter=diagram]')).toHaveAttribute('aria-pressed', 'true');
      expect(await page.locator('#reader-results li').count()).toBeGreaterThan(0);
      await page.screenshot({ path: info.outputPath(`${lang ? 'fr' : 'en'}-search-sheet.png`) });
      await page.keyboard.press('Escape');
      await expect(sheet).toBeHidden();
      await page.locator('.reader-fab').click();
      await expect(page.locator('#reader-actions')).toBeVisible();
      await page.locator('#reader-expand').check();
      await expect(page.locator('.repo-language-disclosure')).toHaveAttribute('open', '');
      const meter = page.locator('.repo-language-card meter').first();
      await expect(meter).toHaveAttribute('max', '100');
      expect(Number(await meter.getAttribute('value'))).toBeGreaterThan(0);
      await page.locator('#reader-expand').uncheck();
      await expect(page.locator('.repo-language-disclosure')).not.toHaveAttribute('open');
      await page.keyboard.press('Escape');
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
    }
    expect(errors).toEqual([]);
  });
}
test('article search navigates and restores focus; copy gives feedback', async ({ page, context }) => {
  await context.grantPermissions(['clipboard-read', 'clipboard-write']);
  await page.goto(`${prefix}/blog/posts/ainewstracker-financial-news/`);
  await page.keyboard.press('/');
  await expect(page.locator('#reader-search')).toBeVisible();
  await page.locator('#reader-query').fill('analysis');
  const result = page.locator('#reader-results a').first();
  const hash = await result.getAttribute('href');
  await result.click();
  await expect(page.locator('#reader-search')).toBeHidden();
  expect(new URL(page.url()).hash).toBe(hash);
  await page.locator('.reader-fab').click();
  await page.locator('#reader-actions [data-reader-copy]').click();
  await expect(page.locator('#reader-feedback')).toHaveText('Link copied');
  expect(await page.evaluate(() => navigator.clipboard.readText())).toBe(page.url());
});
test('copy failure explains recovery', async ({ page }) => {
  await page.addInitScript(() => Object.defineProperty(navigator, 'clipboard', { value: { writeText: () => Promise.reject(new Error('Denied')) } }));
  await page.goto(`${prefix}/blog/projects/notes/artemis-switch/`);
  await page.locator('.reader-launch [data-reader-copy]').click();
  await expect(page.locator('#reader-feedback')).toContainText('Copy unavailable');
});
import AxeBuilder from '@axe-core/playwright';
for (const theme of ['light', 'dark'] as const) test(`reader sheet accessibility ${theme}`, async ({ page }) => {
  await page.emulateMedia({ colorScheme: theme });
  await page.addInitScript(dark => localStorage.setItem('dark', String(dark)), theme === 'dark');
  await page.goto(`${prefix}/blog/projects/notes/artemis-switch/`);
  await page.locator('.reader-launch [data-reader-search]').click();
  const audit = await new AxeBuilder({ page }).include('#reader-search').withTags(['wcag2a', 'wcag2aa']).analyze();
  expect(audit.violations).toEqual([]);
  await page.keyboard.press('Escape');
  await expect(page.locator('.reader-launch [data-reader-search]')).toBeFocused();
});
test('source content works if reader controls fail to load', async ({ page }) => {
  await page.route('**/reader-tools*.js', route => route.abort());
  await page.goto(`${prefix}/blog/projects/notes/artemis-switch/`);
  await expect(page.locator('#reader-tools')).toBeHidden();
  await expect(page.locator('#single-post-title')).toBeVisible();
  await expect(page.locator('.repo-actions a').first()).toBeVisible();
});
test('language colors and page navigation remain meaningful', async ({ page }) => {
  await page.goto(`${prefix}/blog/projects/notes/artemis-switch/`);
  await page.locator('.repo-language-disclosure > summary').click();
  const colors = await page.locator('.repo-language-track > span').evaluateAll(items => items.slice(0, 2).map(e => getComputedStyle(e).backgroundColor));
  expect(colors[0]).not.toBe(colors[1]);
  await page.locator('.reader-fab').click();
  await page.locator('[data-reader-top]').click();
  await expect(page.locator('#single-post-title')).toBeFocused();
  await page.keyboard.press('/');
  await page.locator('[data-reader-filter=diagram]').click();
  await expect(page.locator('#reader-results')).not.toContainText('model 436');
});
test('summary card opens the language breakdown', async ({ page }) => {
  await page.goto(`${prefix}/blog/projects/notes/artemis-switch/`);
  await page.locator('.repo-snapshot-cards a[href="#languages-panel"]').click();
  await expect(page.locator('#languages-panel')).toHaveAttribute('open', '');
  await expect(page.locator('.repo-language-card').first()).toBeVisible();
});
