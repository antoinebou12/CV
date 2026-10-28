import { test, expect } from '@playwright/test';
const prefix = process.env.E2E_PREFIX || '';

for (const language of ['en', 'fr']) {
  test(`CV logos are local and load ${language}`, async ({ page }) => {
    await page.goto(`${prefix}/index-${language}.html`);
    const icons = page.locator('img.expertise-pill-icon, .expertise-cert img, img[src*="tech-icons"]');
    expect(await icons.count()).toBeGreaterThan(30);
    const report = await page.evaluate(async () => {
      const images = [...document.querySelectorAll<HTMLImageElement>('img[src*="tech-icons"], img[src*="org-logos"]')];
      // Lazy images below the fold have not been requested yet; load each one explicitly.
      await Promise.all(images.map(img => { img.loading = 'eager'; return img.decode().catch(() => undefined); }));
      return {
        remote: [...document.querySelectorAll('img')].map(i => i.getAttribute('src') || '').filter(src => /cdn\.simpleicons\.org|devicons\/devicon/.test(src)),
        broken: images.filter(img => !img.naturalWidth).map(img => img.getAttribute('src')),
        mcp: document.querySelector('[data-skill="MCP"] img.expertise-pill-icon')?.getAttribute('src'),
      };
    });
    expect(report.remote).toEqual([]);
    expect(report.broken).toEqual([]);
    expect(report.mcp).toContain('modelcontextprotocol');
  });

  test(`CV stats widgets load and are prefetched ${language}`, async ({ page }) => {
    const requested: string[] = [];
    page.on('request', request => requested.push(request.url()));
    await page.goto(`${prefix}/index-${language}.html`, { waitUntil: 'load' });
    // The idle prefetch fetches the stats cards before any panel is opened.
    await expect.poll(() => requested.filter(url => url.includes('images/widgets/github-stats.svg')).length, { timeout: 8000 }).toBeGreaterThan(0);
    // English uses one toggle button per section; French groups two <details> disclosures in one section.
    for (const toggle of await page.locator('.cv-live-widgets-section .clustrmaps-toggle').all()) {
      await toggle.scrollIntoViewIfNeeded();
      await toggle.click();
    }
    for (const details of await page.locator('.cv-live-widgets-panel details.cv-live-widget').all()) {
      if (await details.getAttribute('open') === null) await details.locator(':scope > summary').click();
    }
    const stats = page.locator('.cv-live-widgets-panel img[src*="images/widgets/"]');
    await expect(stats).toHaveCount(7);
    await expect.poll(() => stats.evaluateAll(images => images.filter(img => (img as HTMLImageElement).naturalWidth > 0).length)).toBe(7);
    expect(await page.locator('.cv-live-widgets-panel img[src*="readme-stats"], .cv-live-widgets-panel img[data-src*="readme-stats"]').count()).toBe(0);
  });
}
