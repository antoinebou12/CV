import { test, expect, type Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
const prefix = (process.env.E2E_PREFIX || '').replace(/\/$/, '');
const route = (p: string) => prefix + p;
const entries = ['/index-en.html', '/index-fr.html', ...['', 'fr/'].flatMap(lang => ['', 'posts/', 'projects/', 'recipes/', 'search/'].map(p => `/blog/${lang}${p}`))];

async function inspect(page: Page) {
  return page.evaluate(() => {
    const ids = [...document.querySelectorAll('[id]')].map(e => e.id);
    const visible = (e: Element) => e.getClientRects().length > 0;
    return {
      title: document.title, lang: document.documentElement.lang,
      headings: document.querySelectorAll('h1').length,
      overflow: document.documentElement.scrollWidth > innerWidth + 2,
      overflowElements: [...document.querySelectorAll('body *')].filter(e => visible(e) && e.getBoundingClientRect().right > innerWidth + 2).slice(0, 12).map(e => `${e.tagName}.${e.className}`),
      duplicateIds: [...new Set(ids.filter((id, i) => ids.indexOf(id) !== i))],
      brokenImages: [...document.images].filter(i => visible(i) && i.currentSrc && i.complete && !i.naturalWidth).map(i => i.currentSrc),
      // Code samples may show Hugo syntax on purpose; residue in prose or attributes is a template bug.
      templateResidue: (() => {
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
          acceptNode: n => n.parentElement?.closest('pre, code, script, style') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT,
        });
        let text = '';
        while (walker.nextNode()) text += walker.currentNode.nodeValue;
        return /\{\{[<%]|ZgotmplZ/.test(text) || document.body.innerHTML.includes('ZgotmplZ');
      })(),
    };
  });
}

for (const width of [390, 768, 1440]) for (const theme of ['light', 'dark'] as const) {
  test(`entry pages ${width}px ${theme}`, async ({ page }, info) => {
    test.setTimeout(600_000);
    await page.setViewportSize({ width, height: 900 });
    await page.emulateMedia({ colorScheme: theme, reducedMotion: 'reduce' });
    const errors: string[] = [];
    page.on('pageerror', e => errors.push(`${page.url()}: ${e.message}`));
    for (const path of entries) {
      const response = await page.goto(route(path));
      expect.soft(response?.status(), path).toBe(200);
      await page.evaluate(() => document.fonts.ready);
      const findings = await inspect(page);
      await info.attach(`${path}-${width}-${theme}.json`, { body: JSON.stringify(findings, null, 2), contentType: 'application/json' });
      expect.soft(findings.title, path).toBeTruthy();
      expect.soft(findings.lang, path).toMatch(/^(en|fr)/);
      expect.soft(findings.headings, path).toBeGreaterThan(0);
      expect.soft(findings.overflow, `${path}: ${findings.overflowElements}`).toBe(false);
      expect.soft(findings.duplicateIds, path).toEqual([]);
      expect.soft(findings.brokenImages, path).toEqual([]);
      expect.soft(findings.templateResidue, path).toBe(false);
      await info.attach(`${path}-${width}-${theme}.png`, { body: await page.screenshot(), contentType: 'image/png' });
    }
    expect(errors).toEqual([]);
  });
}

for (const lang of ['', 'fr/']) {
  test(`search and empty state ${lang || 'en'}`, async ({ page }) => {
    await page.goto(route(`/blog/${lang}search/`));
    const input = page.locator('#site-search-input');
    await input.fill('Rust');
    await expect(page.locator('#site-search-results a').first()).toBeVisible();
    await input.fill('zzzznonexistent987654321');
    await expect(page.locator('#site-search-results li')).toHaveCount(0);
    await expect(page.locator('#site-search-status')).not.toBeEmpty();
    await input.fill('Rust');
    await page.locator('#site-search-results a').first().click();
    await expect(page.locator('h1').first()).toBeVisible();
  });
  test(`project search and reset ${lang || 'en'}`, async ({ page }) => {
    await page.goto(route(`/blog/${lang}projects/`));
    const count = page.locator('[data-repo-count]');
    const initial = await count.innerText();
    await page.locator('[data-repo-search]').fill('zzzznonexistent987654321');
    await expect(count).toHaveText('0');
    await expect(page.locator('[data-repo-empty]')).toBeVisible();
    await page.locator('[data-repo-reset]').click();
    await expect(count).toHaveText(initial);
    for (const filter of ['origin', 'style', 'domain']) {
      const button = page.locator(`[data-repo-${filter}]`).nth(1);
      await button.click();
      await expect(button).toHaveAttribute('aria-pressed', 'true');
      await page.locator('[data-repo-reset]').click();
      await expect(count).toHaveText(initial);
    }
  });
  test(`mobile menu and theme ${lang || 'en'}`, async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(route(`/blog/${lang}`));
    const menu = page.locator('.btn-menu');
    await menu.click();
    await expect(menu).toHaveAttribute('aria-expanded', 'true');
    await page.locator('.site-nav-main a').first().click();
    await expect(page).toHaveURL(/\/posts\//);
    const before = await page.locator('html').getAttribute('class');
    await page.locator('.btn-dark').click();
    await expect(page.locator('html')).not.toHaveAttribute('class', before || '');
  });
  test(`recipes open and accessibility ${lang || 'en'}`, async ({ page }, info) => {
    await page.goto(route(`/blog/${lang}recipes/`));
    const link = page.locator(`main a[href*="/recipes/"]`).filter({ hasText: /\S/ }).first();
    await link.click();
    await expect(page.locator('h1').first()).toBeVisible();
    const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa']).analyze();
    await info.attach('accessibility.json', { body: JSON.stringify(result.violations, null, 2), contentType: 'application/json' });
    expect(result.violations).toEqual([]);
  });
}

test('open every sitemap page', async ({ page, request, baseURL }, info) => {
  test.setTimeout(3_600_000);
  const discovered = new Set<string>();
  const maps = new Set<string>();
  async function sitemap(url: string) {
    if (maps.has(url)) return;
    maps.add(url);
    const response = await request.get(url);
    expect(response.ok(), url).toBeTruthy();
    const xml = await response.text();
    expect(xml, url).toMatch(/<urlset|<sitemapindex/);
    for (const match of xml.matchAll(/<loc>(.*?)<\/loc>/g)) {
      const original = new URL(match[1].replaceAll('&amp;', '&'));
      const target = new URL(original.pathname + original.search, baseURL).href;
      if (/<sitemapindex/.test(xml)) await sitemap(target);
      else discovered.add(target);
    }
  }
  await sitemap(new URL(route('/blog/sitemap.xml'), baseURL).href);
  expect(discovered.size).toBeGreaterThan(0);
  const limit = process.env.E2E_LIMIT ? Number(process.env.E2E_LIMIT) : Infinity;
  const results: unknown[] = [];
  try {
    for (const url of [...discovered].sort().slice(0, limit)) {
      try {
        const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30_000 });
        const findings = await inspect(page);
        results.push({ url, status: response?.status(), ...findings });
        expect.soft(response?.status(), url).toBe(200);
        expect.soft(findings.duplicateIds, url).toEqual([]);
        expect.soft(findings.templateResidue, url).toBe(false);
        expect.soft(findings.overflow, url).toBe(false);
      } catch (error) { results.push({ url, error: String(error) }); expect.soft(String(error), url).toBe(''); }
    }
  } finally {
    await info.attach('crawl-inventory.json', { body: JSON.stringify({ discovered: [...discovered], visited: results, limited: Number.isFinite(limit) }, null, 2), contentType: 'application/json' });
  }
});
