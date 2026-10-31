import { test, expect } from '@playwright/test';

for (const width of [390, 768, 1440]) for (const theme of ['light', 'dark'] as const) {
  test(`repository guide gaps ${width} ${theme}`, async ({ page }, info) => {
    await page.setViewportSize({ width, height: 1000 });
    await page.emulateMedia({ colorScheme: theme, reducedMotion: 'reduce' });
    await page.addInitScript(dark => localStorage.setItem('dark', String(dark)), theme === 'dark');
    for (const lang of ['', 'fr/']) {
      await page.goto(`${process.env.E2E_PREFIX || ''}/blog/${lang}projects/notes/cv/`);
      const stack = page.locator('.repo-guide-chapters');
      const rows = stack.locator(':scope > .repo-guide-chapter');
      expect(await rows.count()).toBeGreaterThan(1);
      await expect(rows.last().locator('summary')).toHaveText(lang ? 'Documentation source' : 'Source documentation');
      const gaps = () => rows.evaluateAll(items => items.slice(1).map((item, n) => item.getBoundingClientRect().top - items[n].getBoundingClientRect().bottom));
      const closedGaps = await gaps();
      expect(closedGaps.every(gap => gap >= 9 && gap <= 14)).toBe(true);
      await stack.screenshot({ path: info.outputPath(`${lang ? 'fr' : 'en'}-closed-stack.png`) });
      await rows.nth((await rows.count()) - 2).locator(':scope > summary').focus();
      await page.keyboard.press('Enter');
      expect((await gaps()).every(gap => gap >= 9 && gap <= 14)).toBe(true);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 2)).toBe(true);
    }
  });
}
