/* Run with CODEX_NODE_MODULES pointing to the Playwright runtime, if needed. */
const assert = require('node:assert/strict');
const { createRequire } = require('node:module');
const { resolve } = require('node:path');
const { mkdirSync } = require('node:fs');
const { chromium } = process.env.CODEX_NODE_MODULES
  ? createRequire(resolve(process.env.CODEX_NODE_MODULES, 'package.json'))('playwright')
  : require('playwright');
const inventory = require('../../hugo/data/github_inventory.json').repositories;
const types = require('../../hugo/data/repository_styles.json');
const base = process.env.HUGO_PREVIEW || 'http://localhost:1313/blog';
const out = resolve('tmp/project-catalog-check');

(async () => {
  mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ headless: true, channel: 'chrome' });
  let states = 0;
  try {
    for (const lang of ['en', 'fr']) for (const theme of ['light', 'dark']) for (const width of [390, 768, 1440]) {
      const context = await browser.newContext({ viewport: { width, height: 960 }, colorScheme: theme, reducedMotion: 'reduce' });
      await context.addInitScript(t => { localStorage.setItem('dark', String(t === 'dark')); localStorage.setItem('cv-theme', t); }, theme);
      const page = await context.newPage();
      const errors = [];
      page.on('pageerror', e => errors.push(e.message));
      const response = await page.goto(`${base}/${lang === 'fr' ? 'fr/' : ''}projects/`, { waitUntil: 'domcontentloaded' });
      assert.equal(response.status(), 200);
      await page.evaluate(() => document.fonts.ready);
      assert.equal(await page.locator('.repo-reading').count(), 0);
      assert.equal(await page.locator('h1').count(), 1);
      assert.equal(await page.locator('#project-particles').count(), 1);
      assert.equal(await page.locator('#project-particles canvas').count(), 0, 'Reduced motion must skip the particle canvas');
      assert.equal(await page.locator('.repo-kind--fork').count(), inventory.filter(r => r.fork).length);
      const visible = () => page.locator('.repo-directory-card:visible').count();
      assert.equal(await visible(), inventory.length);
      assert.equal(await page.locator('.repo-directory-card').count(), inventory.length, 'Repositories must not be duplicated across types');
      assert.deepEqual(await page.locator('[data-project-type] > summary h2').allTextContents(), types.styles.map(t => t.label[lang === 'fr' ? 1 : 0]));
      assert.equal(await page.evaluate(mapping => [...document.querySelectorAll('.repo-directory-card')].every(card => card.closest('[data-project-type]').dataset.projectType === mapping[card.dataset.name][0]), types.repositories), true);
      assert.equal(await page.locator('[data-name="FlashGames"] .repo-technology-badge').textContent(), 'Flash');
      assert.equal(await page.locator('[data-project-type="teaching"] [data-name="TCH099"]').count(), 1);
      assert.equal(await page.locator('.repo-source svg').count(), inventory.length);
      await page.locator('[data-repo-style="teaching"]').click();
      assert.equal(await visible(), 1);
      assert.equal(await page.locator('.repo-directory-card:visible').getAttribute('data-name'), 'TCH099');
      await page.locator('[data-repo-reset]').click();
      const actionSizes = await page.locator('[data-name="Artemis-Switch"] .repo-card-actions a').evaluateAll(links => links.map(a => ({height:a.getBoundingClientRect().height,top:a.getBoundingClientRect().top})));
      assert.equal(actionSizes.length, 2);
      assert.ok(actionSizes.every(s => s.height >= 44));
      assert.ok(Math.abs(actionSizes[0].height - actionSizes[1].height) <= 1, 'Card actions must have equal heights');
      assert.ok(Math.abs(actionSizes[0].top - actionSizes[1].top) <= 1, 'Card actions must align');
      assert.ok(await page.locator('[data-name="Artemis-Switch"] .repo-card-actions').evaluate(el => parseFloat(getComputedStyle(el).marginBottom) >= 24));
      assert.ok(await page.locator('[data-name="Artemis-Switch"] .repo-card-posts').evaluate(el => {
        const style = getComputedStyle(el);
        return parseFloat(style.paddingTop) >= 20 && parseFloat(style.marginBottom) >= 24;
      }));
      assert.ok(await page.locator('.repo-explorer-search').evaluate(el => el.getBoundingClientRect().height >= 44));
      assert.ok(await page.locator('.repo-origin-filters button').first().evaluate((el, compact) => el.getBoundingClientRect().height >= (compact ? 36 : 44), width >= 760));
      assert.equal(await page.locator('.repo-directory-card').first().evaluate((el, mobile) => {
        const style = getComputedStyle(el);
        return style.borderRadius === '5px' && parseFloat(style.paddingLeft) === (mobile ? 20 : 28);
      }, width <= 600), true);
      if (width === 1440) assert.ok(await page.locator('.repo-explorer').evaluate(el => el.getBoundingClientRect().height <= 360), 'Desktop explorer should stay compact');
      if (width === 1440 && lang === 'en') {
        await page.locator('[data-name="Artemis-Switch"]').screenshot({path:resolve(out, `github-card-${theme}.png`)});
      }
      for (const origin of ['fork', 'original']) {
        await page.locator(`[data-repo-origin="${origin}"]`).click();
        assert.equal(await visible(), inventory.filter(r => origin === 'fork' ? r.fork : !r.fork).length);
        assert.equal(await page.locator(`[data-repo-origin="${origin}"]`).getAttribute('aria-pressed'), 'true');
      }
      await page.locator('[data-repo-origin="fork"]').click();
      await page.locator('[data-repo-search]').fill('nova-backtest');
      assert.equal(await visible(), 1);
      await page.locator('[data-repo-origin="original"]').click();
      assert.equal(await visible(), 0);
      assert.equal(await page.locator('[data-repo-empty]').isVisible(), true);
      await page.locator('[data-repo-reset]').click();
      assert.equal(await visible(), inventory.length);
      assert.equal(await page.locator('[data-repo-origin=""]').getAttribute('aria-pressed'), 'true');
      await page.locator('[data-repo-style]:not([data-repo-style=""])').first().click();
      await page.locator('[data-repo-domain]:not([data-repo-domain=""])').nth(1).click();
      await page.locator('[data-repo-origin="fork"]').click();
      assert.equal(await page.evaluate(() => {
        const style = document.querySelector('[data-repo-style][aria-pressed="true"]').dataset.repoStyle;
        const domain = document.querySelector('[data-repo-domain][aria-pressed="true"]').dataset.repoDomain;
        return [...document.querySelectorAll('.repo-directory-card')].every(c => c.hidden === !(c.dataset.origin === 'fork' && c.dataset.styles.split(' ').includes(style) && c.dataset.domains.split(' ').includes(domain)));
      }), true);
      assert.equal(await page.locator('.repo-group-count').count(), 0, 'Group headings stay uncluttered');
      assert.equal(Number(await page.locator('[data-repo-count]').textContent()), await visible(), 'The global result count reports matching cards');
      await page.locator('[data-repo-reset]').click();
      await page.locator('[data-repo-sort]').selectOption('name');
      assert.equal(await page.evaluate(() => [...document.querySelectorAll('.repo-directory-grid')].every(g => [...g.children].every((c,i,all) => !i || all[i-1].dataset.name.localeCompare(c.dataset.name) <= 0))), true);
      assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), true, `${lang}/${theme}/${width}: overflow`);
      assert.equal(await page.locator('html').evaluate(e => e.classList.contains('dark')), theme === 'dark');
      await page.evaluate(() => scrollTo(0, 0));
      await page.screenshot({ path: resolve(out, `${lang}-${theme}-${width}.png`) });
      assert.deepEqual(errors, []);
      await context.close();
      states++;
    }
    console.log(`Passed ${states} catalog states: EN/FR, light/dark, 390/768/1440px; origin filters, combined filters, search, reset, sorting, group counts and overflow.`);
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });
