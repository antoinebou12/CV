import { test, expect } from '@playwright/test';
for (const width of [390, 768, 1440]) for (const theme of ['light', 'dark'] as const) {
  test(`project sidebar polish ${width} ${theme}`, async ({ page }, info) => {
    await page.setViewportSize({ width, height: 1100 });
    await page.emulateMedia({ colorScheme: theme, reducedMotion: 'reduce' });
    await page.addInitScript(dark => localStorage.setItem('dark', String(dark)), theme === 'dark');
    for (const slug of ['cv', 'chitui']) {
      await page.goto(`${process.env.E2E_PREFIX || ''}/blog/projects/notes/${slug}/`);
      const contents = page.locator('.repo-sidenav-disclosure');
      if (width > 760) await expect(contents.locator(':scope > summary')).toBeHidden();
      else {
        await expect(contents).not.toHaveAttribute('open');
        await contents.locator(':scope > summary').click();
        await expect(contents.locator('.repo-sidenav-label')).toBeHidden();
      }
      expect(await contents.evaluate(e => e.scrollWidth <= e.clientWidth + 1)).toBe(true);
      const labels = await contents.locator('ol a > span:last-child').evaluateAll(items => items.map(e => e.getBoundingClientRect().left));
      expect(Math.max(...labels) - Math.min(...labels)).toBeLessThan(1);
      await expect(contents.locator('ol a').first()).toHaveCSS('text-align', 'left');
      await expect(contents.locator('ol a').first()).toHaveCSS('display', 'grid');
      if (slug === 'cv') await expect(contents.locator('ol a').filter({ hasText: 'Features and components' })).not.toContainText('2');
      await expect(page.locator('.repo-tech-badges a').first()).toHaveCSS('text-decoration-line', 'none');
      await page.evaluate(() => scrollTo(0, 0));
      await page.screenshot({ path: info.outputPath(`${slug}-polished.png`) });
    }
  });
}
