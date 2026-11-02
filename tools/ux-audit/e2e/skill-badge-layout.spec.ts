import { test, expect } from '@playwright/test';
for (const width of [390, 768, 1024, 1440]) for (const lang of ['en', 'fr']) test(`skill labels stay readable ${width} ${lang}`, async ({ page }, info) => {
  await page.setViewportSize({ width, height: 1000 });
  await page.emulateMedia({ reducedMotion: 'reduce', colorScheme: 'dark' });
  await page.goto(`${process.env.E2E_PREFIX || ''}/index-${lang}.html`);
  const python = page.locator('.expertise-pill[data-skill="Python"]').first();
  await python.scrollIntoViewIfNeeded();
  const domains = page.locator('.expertise-domain');
  for (let i = 0; i < await domains.count(); i++) {
    await domains.nth(i).click();
    const bad = await page.locator('.expertise-panel:visible .expertise-pill-main > span').evaluateAll(items => items.filter(e => e.getBoundingClientRect().height > parseFloat(getComputedStyle(e).lineHeight) + 2).map(e => e.textContent));
    expect(bad).toEqual([]);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  }
  await domains.first().click();
  await python.scrollIntoViewIfNeeded();
  await page.locator('[data-expertise]').screenshot({ path: info.outputPath('skill-badges.png') });
  const button = python.locator('.expertise-evidence');
  await button.click();
  await expect(button).toHaveAttribute('aria-expanded', 'true');
  await expect(python.locator('.expertise-evidence-popover')).toBeVisible();
});
