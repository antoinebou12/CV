import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
const prefix = process.env.E2E_PREFIX || '';
for (const width of [390, 1440]) for (const theme of ['light', 'dark'] as const) {
  test(`expanded sections ${width} ${theme}`, async ({ page }, info) => {
    test.setTimeout(600_000);
    await page.setViewportSize({ width, height: 950 });
    await page.emulateMedia({ colorScheme: theme, reducedMotion: 'reduce' });
    for (const route of ['/index-en.html', '/index-fr.html', '/blog/', '/blog/projects/', '/blog/projects/notes/chitui/', '/blog/recipes/']) {
      await page.goto(prefix + route);
      await page.evaluate(() => document.fonts.ready);
      const details = page.locator('details');
      let opened = 0;
      for (let i = 0; i < await details.count(); i++) {
        const item = details.nth(i);
        const summary = item.locator(':scope > summary');
        if (await summary.isVisible() && await item.getAttribute('open') === null) {
          await summary.focus();
          await summary.press('Enter');
          await expect(item).toHaveAttribute('open', '');
          opened++;
        }
      }
      const slug = route.replace(/\W/g, '-');
      await page.screenshot({ path: info.outputPath(`${slug}-top.png`) });
      const targets = route.includes('index-') ? ['#photo-header', '#job-la-caisse', '.cv-job[open]', '[data-expertise]', '.project-group[open]'] : ['main', 'details[open]'];
      for (const selector of targets) {
        const target = page.locator(selector).first();
        if (await target.isVisible()) {
          await target.scrollIntoViewIfNeeded();
          await page.screenshot({ path: info.outputPath(`${slug}-${selector.replace(/\W/g, '-')}.png`) });
        }
      }
      const layout = await page.evaluate(() => ({
        width: innerWidth, scroll: document.documentElement.scrollWidth,
        overflow: [...document.querySelectorAll('body *')].filter(e => e.getClientRects().length && e.getBoundingClientRect().right > innerWidth + 2).slice(0, 20).map(e => ({ tag: e.tagName, class: e.className, text: e.textContent?.slice(0, 80) }))
      }));
      const axe = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze();
      await info.attach(`${slug}-findings.json`, { body: JSON.stringify({ opened, layout, violations: axe.violations }, null, 2), contentType: 'application/json' });
      expect.soft(layout.scroll, route).toBeLessThanOrEqual(width + 2);
      expect.soft(axe.violations.filter(v => v.id === 'color-contrast').flatMap(v => v.nodes.map(n => ({ target: n.target, issue: n.failureSummary }))), route).toEqual([]);
    }
  });
}

for (const language of ['en', 'fr']) test(`expertise subsections ${language}`, async ({ page }, info) => {
  await page.setViewportSize({ width: 390, height: 950 });
  await page.emulateMedia({ colorScheme: 'dark', reducedMotion: 'reduce' });
  const errors: string[] = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(`${prefix}/index-${language}.html`);
  const domains = page.locator('.expertise-domain');
  expect(await domains.first().evaluate(el => parseFloat(getComputedStyle(el).fontSize))).toBeGreaterThanOrEqual(12);
  for (let i = 0; i < await domains.count(); i++) {
    const domain = domains.nth(i);
    await domain.click();
    await expect(domain).toHaveAttribute('aria-selected', 'true');
    const panel = page.locator('[data-domain-panel]:visible');
    await expect(panel).toHaveCount(1);
    const subs = panel.locator('.expertise-sub:visible');
    for (let j = 0; j < await subs.count(); j++) {
      await subs.nth(j).click();
      await expect(subs.nth(j)).toHaveAttribute('aria-selected', 'true');
    }
    await page.locator('[data-expertise]').scrollIntoViewIfNeeded();
    await page.screenshot({ path: info.outputPath(`domain-${i}.png`) });
  }
  expect(errors).toEqual([]);
});
