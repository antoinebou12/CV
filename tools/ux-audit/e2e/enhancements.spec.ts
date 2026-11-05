import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

// Covers the 2026-11 improvements: SEO tags, the hero-aligned header and options popover,
// dynamic tables, reduced-motion-safe reveals, the article side rail, open project diagrams,
// and the Markdown context twins. Run against the local staging server (see E2E-PLAN.md).
const prefix = (process.env.E2E_PREFIX || '').replace(/\/$/, '');
const route = (p: string) => prefix + p;
const jsonLd = async (page: import('@playwright/test').Page) =>
  page.$$eval('script[type="application/ld+json"]', nodes => nodes.map(n => JSON.parse(n.textContent || '{}')));

test.describe('SEO metadata', () => {
  for (const path of ['/blog/posts/uml-mcp/', '/blog/projects/notes/uml-mcp/', '/blog/fr/projects/notes/uml-mcp/']) {
    test(`hreflang, canonical and structured data on ${path}`, async ({ page }) => {
      await page.goto(route(path));
      const alternates = await page.$$eval('link[rel="alternate"][hreflang]', links => links.map(l => l.getAttribute('hreflang')));
      expect(alternates.sort()).toEqual(['en', 'fr', 'x-default']);
      expect(await page.getAttribute('link[rel="canonical"]', 'href')).toContain(path.replace('/blog/', '/blog/'));
      const data = await jsonLd(page);
      const types = data.map(d => d['@type']);
      expect(types).toContain('BreadcrumbList');
      expect(types.some(t => ['BlogPosting', 'TechArticle', 'Article'].includes(t))).toBeTruthy();
      const article = data.find(d => ['BlogPosting', 'TechArticle'].includes(d['@type']));
      expect(article.author['@id']).toContain('#person');
      if (path.includes('/projects/notes/')) expect(article.about['@type']).toBe('SoftwareSourceCode');
      expect(await page.$$eval('meta[name="description"]', m => m.length)).toBe(1);
    });
  }
  test('Markdown context twins exist for pages and sections', async ({ request }) => {
    for (const path of ['/blog/projects/notes/uml-mcp/index.md', '/blog/posts/uml-mcp/index.md', '/blog/projects/index.md']) {
      const response = await request.get(route(path));
      expect(response.ok(), path).toBeTruthy();
      const body = await response.text();
      expect(body.startsWith('# ')).toBeTruthy();
      expect(body).toContain('HTML page:');
    }
    const brief = await (await request.get(route('/blog/projects/notes/uml-mcp/index.md'))).text();
    expect(brief).toContain('## Architecture');
    expect(brief).toContain('```mermaid');
  });
});

test.describe('Header chrome', () => {
  test('options popover holds theme and background controls; CV pill is short', async ({ page }) => {
    await page.goto(route('/blog/'));
    await expect(page.locator('.site-pill-cv')).toHaveText('CV');
    const toggle = page.locator('.site-options-toggle');
    await toggle.click();
    await expect(toggle).toHaveAttribute('aria-expanded', 'true');
    const theme = page.locator('#site-settings .btn-dark');
    await expect(theme).toBeVisible();
    const label = await theme.innerText();
    await theme.click();
    await expect(page.locator('html')).toHaveClass(/dark/);
    expect(await theme.innerText()).not.toBe(label);
    await expect(page.locator('#site-settings .site-profiles a').first()).toBeVisible();
  });
  test('mobile drawer opens with pills and language group', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(route('/blog/'));
    await page.locator('.btn-menu').click();
    await expect(page.locator('.btn-menu')).toHaveAttribute('aria-expanded', 'true');
    await expect(page.locator('.nav-drawer .site-nav-main .site-pill').first()).toBeVisible();
    await expect(page.locator('.nav-drawer .site-lang-switch .site-pill')).toHaveCount(2);
    await page.keyboard.press('Escape');
    await expect(page.locator('.btn-menu')).toHaveAttribute('aria-expanded', 'false');
  });
});

test.describe('Dynamic tables', () => {
  test('article tables sort by column and announce the order', async ({ page }) => {
    await page.goto(route('/blog/posts/uml-mcp/'));
    const table = page.locator('table.is-dynamic').first();
    await expect(table).toBeVisible();
    const header = table.locator('th').first();
    const firstCell = () => table.locator('tbody tr td').first().innerText();
    const original = await firstCell();
    await header.locator('button').click();
    await expect(header).toHaveAttribute('aria-sort', 'ascending');
    await header.locator('button').click();
    await expect(header).toHaveAttribute('aria-sort', 'descending');
    await header.locator('button').click();
    await expect(header).toHaveAttribute('aria-sort', 'none');
    expect(await firstCell()).toBe(original);
  });
  test('large project tables get a filter with a live count', async ({ page }) => {
    await page.goto(route('/blog/projects/notes/uml-mcp/'));
    await page.locator('details').evaluateAll(items => items.forEach(e => e.setAttribute('open', '')));
    const tools = page.locator('.table-tools').first();
    await expect(tools).toBeVisible();
    const input = tools.locator('input[type="search"]');
    await input.fill('zzzz-no-such-row');
    await expect(tools.locator('output')).toHaveText(/No rows match|Aucune ligne/);
    await input.fill('');
    await expect(tools.locator('output')).toHaveText(/rows shown|lignes affichées/);
  });
});

test.describe('Motion and reading tools', () => {
  test('reduced motion shows everything immediately', async ({ page }) => {
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto(route('/blog/projects/'));
    const hidden = await page.$$eval('[data-reveal]', nodes => nodes.filter(n => getComputedStyle(n).opacity !== '1').length);
    expect(hidden).toBe(0);
  });
  test('reveals appear as the reader scrolls', async ({ page }) => {
    await page.emulateMedia({ reducedMotion: 'no-preference' });
    await page.goto(route('/blog/projects/'));
    const card = page.locator('[data-reveal]').last();
    await card.scrollIntoViewIfNeeded();
    await expect(card).toHaveClass(/is-visible/);
  });
  test('article table of contents becomes a sticky rail that tracks the section', async ({ page }) => {
    await page.setViewportSize({ width: 1366, height: 860 });
    await page.goto(route('/blog/posts/marketwatch-python-trading/'));
    const rail = page.locator('.article-toc-rail');
    await expect(rail).toBeVisible();
    expect(await rail.evaluate(e => getComputedStyle(e).position)).toBe('sticky');
    const last = rail.locator('a').last();
    const id = (await last.getAttribute('href'))!.slice(1);
    await page.locator(`[id="${decodeURIComponent(id)}"]`).evaluate(node => node.scrollIntoView({ block: 'start' }));
    await expect(last).toHaveAttribute('aria-current', 'true');
  });
  test('phones keep the table of contents as a collapsed disclosure', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(route('/blog/posts/marketwatch-python-trading/'));
    await expect(page.locator('.article-toc-rail')).toHaveCount(0);
    await expect(page.locator('[data-article-toc]')).not.toHaveAttribute('open', '');
  });
  test('project diagrams are open by default with a text alternative', async ({ page }) => {
    await page.goto(route('/blog/projects/notes/uml-mcp/'));
    const lazy = page.locator('details[data-mermaid-lazy]');
    expect(await lazy.count()).toBeGreaterThan(0);
    expect(await lazy.evaluateAll(items => items.every(e => e.hasAttribute('open')))).toBeTruthy();
    await expect(page.locator('.repo-diagram-text').first()).toBeAttached();
  });
});

test('home, catalog and a project note pass WCAG 2.1 AA checks', async ({ page }, info) => {
  const violations: Record<string, unknown[]> = {};
  // Reveal transitions are skipped so axe measures final colours, not mid-animation opacity.
  await page.emulateMedia({ reducedMotion: 'reduce' });
  for (const path of ['/blog/', '/blog/projects/', '/blog/projects/notes/uml-mcp/', '/blog/posts/uml-mcp/']) {
    await page.goto(route(path));
    const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).disableRules(['region']).analyze();
    violations[path] = result.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.slice(0, 3).map(n => n.target) }));
  }
  await info.attach('axe.json', { body: JSON.stringify(violations, null, 2), contentType: 'application/json' });
  const serious = Object.entries(violations).flatMap(([path, list]) => (list as { impact?: string; id: string }[]).filter(v => ['serious', 'critical'].includes(v.impact || '')).map(v => `${path} ${v.id}`));
  expect(serious).toEqual([]);
});
