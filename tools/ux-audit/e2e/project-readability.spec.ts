import { test, expect } from '@playwright/test';

for (const theme of ['light', 'dark'] as const) {
  test(`project navigation and readable diagrams ${theme}`, async ({ page }, info) => {
    await page.setViewportSize({ width: 390, height: 900 });
    await page.emulateMedia({ colorScheme: theme, reducedMotion: 'reduce' });
    await page.addInitScript(dark => localStorage.setItem('dark', String(dark)), theme === 'dark');
    await page.goto(`${process.env.E2E_PREFIX || ''}/blog/projects/notes/uml-mcp/`);
    const navigation = page.locator('.repo-sidenav-disclosure');
    await expect(navigation).not.toHaveAttribute('open');
    await navigation.locator(':scope > summary').click();
    await expect(navigation).toHaveAttribute('open', '');
    await navigation.locator('a[href="#overview"]').click();
    await expect(navigation).not.toHaveAttribute('open');
    await page.evaluate(() => scrollTo(0, 0));
    await page.screenshot({ path: info.outputPath('mobile-navigation.png') });
    await page.setViewportSize({ width: 1280, height: 900 });
    await expect(navigation).toHaveAttribute('open', '');
    const diagram = page.locator('#dossier-c4 .repo-uml-details').nth(2);
    await diagram.locator(':scope > summary').click();
    await expect(diagram.locator('.diagram-tools output')).toHaveText('100%');
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 2)).toBe(true);
    await diagram.locator('.diagram-interactive').screenshot({ path: info.outputPath('readable-components.png') });
    await diagram.locator('[data-diagram-action="fit"]').click();
    await expect(diagram.locator('.diagram-tools output')).not.toHaveText('100%');
  });
}
