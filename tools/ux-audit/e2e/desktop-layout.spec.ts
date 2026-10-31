import { test, expect } from '@playwright/test';
for (const width of [390, 768, 1440, 2560]) for (const theme of ['light', 'dark'] as const) {
  test(`responsive canvas ${width} ${theme}`, async ({ page }, info) => {
    await page.setViewportSize({ width, height: 1100 });
    await page.emulateMedia({ colorScheme: theme, reducedMotion: 'reduce' });
    await page.addInitScript(dark => localStorage.setItem('dark', String(dark)), theme === 'dark');
    for (const route of ['projects/notes/cv/', 'posts/', 'tags/conference/', 'posts/ipc-toolkit-contact-library/']) {
      await page.goto(`${process.env.E2E_PREFIX || ''}/blog/${route}`);
      await expect(page.locator('main')).toBeVisible();
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
      if (width >= 1440) expect(await page.locator('main').evaluate(e => e.getBoundingClientRect().width / innerWidth)).toBeGreaterThan(.84);
      const grid = page.locator('.post-card-grid').first();
      if (width >= 1440 && await grid.count()) expect((await grid.evaluate(e => getComputedStyle(e).gridTemplateColumns)).split(' ').length).toBeGreaterThanOrEqual(3);
      await expect(page.locator('#project-particles canvas')).toHaveCount(0);
      await page.screenshot({ path: info.outputPath(route.replaceAll('/', '-') + '.png') });
    }
  });
}
test('background can be paused and remembers the preference', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'no-preference' });
  await page.goto(`${process.env.E2E_PREFIX || ''}/blog/posts/`);
  const control = page.locator('#background-motion');
  await expect(page.locator('#project-particles canvas')).toHaveCount(1);
  await control.click();
  await expect(page.locator('#project-particles canvas')).toHaveCount(0);
  await page.reload();
  await expect(control).toHaveAttribute('aria-pressed', 'false');
  await control.click();
  await expect(page.locator('#project-particles canvas')).toHaveCount(1);
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await expect(page.locator('#project-particles canvas')).toHaveCount(0);
});

test('source tables and code walkthrough have readable spacing', async ({ page }, info) => {
  await page.setViewportSize({ width: 1920, height: 1200 });
  await page.goto(`${process.env.E2E_PREFIX || ''}/blog/projects/notes/cv/`);
  await page.locator('.repo-guide-chapter').evaluateAll(items => items.forEach(e => e.setAttribute('open', '')));
  const table = page.locator('.repo-source-markdown table').first();
  await expect(table).toBeVisible();
  expect(await table.locator('td').first().evaluate(e => parseFloat(getComputedStyle(e).paddingLeft))).toBeGreaterThanOrEqual(12);
  const rows = await table.locator('tr').evaluateAll(items => items.map(row => row.children.length));
  expect(rows.every(count => count === rows[0])).toBe(true);
  await table.scrollIntoViewIfNeeded();
  await page.screenshot({ path: info.outputPath('source-table.png') });
  const trace = page.locator('.repo-trace').first();
  await trace.evaluate(e => e.setAttribute('open', ''));
  expect(await trace.evaluate(e => parseFloat(getComputedStyle(e).paddingTop))).toBeGreaterThanOrEqual(16);
  await trace.scrollIntoViewIfNeeded();
  await page.screenshot({ path: info.outputPath('code-walkthrough.png') });
});
