import { test, expect } from '@playwright/test';

for (const width of [390, 768, 1280]) for (const theme of ['light', 'dark'] as const) {
  test(`project keyboard and source layout ${width} ${theme}`, async ({ page }, info) => {
    await page.setViewportSize({ width, height: 900 });
    await page.emulateMedia({ colorScheme: theme, reducedMotion: 'reduce' });
    await page.addInitScript(dark => localStorage.setItem('dark', String(dark)), theme === 'dark');
    await page.goto(`${process.env.E2E_PREFIX || ''}/blog/projects/notes/chitui/`, { waitUntil: 'domcontentloaded' });
    const skip = page.locator('.site-skip-link');
    await expect(skip).toHaveCSS('clip-path', 'inset(50%)');
    await page.keyboard.press('Tab');
    await expect(skip).toBeFocused();
    await expect(skip).toHaveCSS('clip-path', 'none');
    await page.keyboard.press('Enter');
    await expect(page.locator('#main-content')).toBeFocused();
    const names = await page.locator('.repo-modules-table th[scope="row"] code').evaluateAll(elements => elements.map(element => {
      const range = document.createRange();
      range.selectNodeContents(element);
      return { name: element.textContent, lines: range.getClientRects().length };
    }));
    expect(names.length).toBeGreaterThan(0);
    expect(names.filter(name => name.lines !== 1)).toEqual([]);
    const source = page.locator('#dossier-public .repo-uml-source').first();
    await source.locator('summary').focus();
    await page.keyboard.press('Enter');
    const pre = source.locator('pre');
    await expect(pre.locator('.repo-copy')).toBeVisible();
    expect(await pre.evaluate(element => {
      const code = element.querySelector('code')!;
      const text = document.createTreeWalker(code, NodeFilter.SHOW_TEXT).nextNode()!;
      const range = document.createRange();
      range.selectNodeContents(text);
      return range.getBoundingClientRect().top >= element.querySelector('.repo-copy')!.getBoundingClientRect().bottom;
    })).toBe(true);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 2)).toBe(true);
    await source.screenshot({ path: info.outputPath('source-controls.png') });
  });
}
