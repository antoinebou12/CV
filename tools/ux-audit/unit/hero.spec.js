import { test, expect, fixture, script, nav } from './helpers.js';

const load = page => script(page, 'js/cv-interactions.js');

for (const lang of ['en', 'fr']) {
  for (const dark of [false, true]) {
    test(`hero theme toggles and persists: ${lang}, initially ${dark ? 'dark' : 'light'}`, async ({ page }) => {
      await fixture(page, nav, lang);
      await page.evaluate(dark => document.documentElement.classList.toggle('dark', dark), dark);
      await load(page);
      const button = page.locator('.cv-theme-toggle');
      await expect(button).toHaveCount(1);
      await expect(button).toHaveAttribute('aria-pressed', String(dark));
      await button.click();
      await expect(page.locator('html')).toHaveAttribute('data-theme', dark ? 'light' : 'dark');
      await expect(button).toHaveText(lang === 'fr' ? (dark ? 'Sombre' : 'Clair') : (dark ? 'Dark' : 'Light'));
      expect(await page.evaluate(() => localStorage.getItem('cv-theme'))).toBe(dark ? 'light' : 'dark');
    });
  }
  test(`reduced motion keeps the hero text complete: ${lang}`, async ({ page }) => {
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await fixture(page, `${nav}<h1 data-typewriter data-typewriter-on="load" aria-label="Antoine Boucher">Antoine Boucher</h1>`, lang);
    await load(page);
    await expect(page.locator('h1')).toHaveText('Antoine Boucher');
    await expect(page.locator('.cv-motion-toggle')).toBeDisabled();
    await expect(page.locator('.cv-motion-toggle')).toHaveText(lang === 'fr' ? 'Animations réduites' : 'Reduced motion');
    await expect(page.locator('html')).toHaveAttribute('data-motion', 'paused');
  });
}

test('saved motion choice survives initialization and can be resumed', async ({ page }) => {
  await fixture(page, nav);
  await page.evaluate(() => localStorage.setItem('cv-motion-paused', 'true'));
  await load(page);
  await expect(page.locator('.cv-motion-toggle')).toHaveText('Animate background');
  await page.locator('.cv-motion-toggle').click();
  await expect(page.locator('html')).toHaveAttribute('data-motion', 'playing');
  expect(await page.evaluate(() => localStorage.getItem('cv-motion-paused'))).toBe('false');
});

test('changing the system motion preference updates the control', async ({ page }) => {
  await fixture(page, nav);
  await load(page);
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await expect(page.locator('.cv-motion-toggle')).toBeDisabled();
  await page.emulateMedia({ reducedMotion: 'no-preference' });
  await expect(page.locator('.cv-motion-toggle')).toBeEnabled();
});

test('blocked storage does not break theme or motion controls', async ({ page }) => {
  await fixture(page, nav);
  await page.evaluate(() => Object.defineProperty(window, 'localStorage', { get() { throw new DOMException('Blocked', 'SecurityError'); } }));
  await load(page);
  await page.locator('.cv-theme-toggle').click();
  await expect(page.locator('html')).toHaveClass('dark');
  await page.locator('.cv-motion-toggle').click();
  await expect(page.locator('html')).toHaveAttribute('data-motion', 'paused');
});

test('missing optional components are safe', async ({ page }) => {
  await fixture(page, '<main>Content</main>');
  await load(page);
  await expect(page.locator('main')).toHaveText('Content');
});

test('fallback navigation buttons are inserted only when absent', async ({ page }) => {
  await fixture(page, '<nav class="cv-site-nav"><span class="cv-nav-lang"></span></nav>');
  await load(page);
  await expect(page.locator('.cv-theme-toggle')).toHaveCount(1);
  await expect(page.locator('.cv-motion-toggle')).toHaveCount(1);
});

test('language links identify their language and current page', async ({ page }) => {
  await fixture(page, nav);
  await load(page);
  await expect(page.getByRole('link', { name: 'Français' })).toHaveAttribute('hreflang', 'fr');
  await expect(page.getByRole('link', { name: 'English' })).toHaveAttribute('aria-current', 'page');
});

test('skip link moves keyboard focus to main content', async ({ page }) => {
  await fixture(page, nav);
  await load(page);
  await page.locator('.skip-link').click();
  await expect(page.locator('main')).toBeFocused();
});

test('pausing during a typewriter reveal restores the complete accessible text', async ({ page }) => {
  await page.clock.install();
  await fixture(page, `${nav}<h1 data-typewriter data-typewriter-on="load" aria-label="Platform and graphics">Platform and graphics</h1>`);
  await load(page);
  await page.clock.runFor(350);
  await page.locator('.cv-motion-toggle').click();
  await page.clock.runFor(20);
  await expect(page.locator('h1')).toHaveText('Platform and graphics');
  await expect(page.locator('h1')).toHaveAttribute('aria-label', 'Platform and graphics');
  await expect(page.locator('h1')).not.toHaveClass(/is-typing/);
});

test('opening a job reveals its lead without animation under reduced motion', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await fixture(page, `${nav}<details class="cv-job"><summary>Job</summary><p class="job-lead"><span data-typewriter>Built the service</span></p></details>`);
  await load(page);
  await page.locator('summary').click();
  await expect(page.locator('[data-typewriter]')).toHaveAttribute('data-typed', '1');
  await expect(page.locator('[data-typewriter]')).toHaveText('Built the service');
});

for (const trigger of ['pointerenter', 'focusin', 'idle']) {
  test(`widgets prefetch once on ${trigger} without opening the panel`, async ({ page }) => {
    await fixture(page, `${nav}<section class="cv-live-widgets-section"><button class="clustrmaps-toggle">Stats</button><div class="cv-live-widgets-panel" hidden><img data-src="/stats.svg"><img data-src="/stats.svg"></div></section>`);
    await page.evaluate(() => {
      window.prefetched = [];
      window.Image = class { set src(value) { window.prefetched.push(value); } };
      window.requestIdleCallback = callback => { window.idleWarm = callback; };
    });
    await load(page);
    if (trigger === 'idle') await page.evaluate(() => window.idleWarm());
    else await page.locator('.clustrmaps-toggle').dispatchEvent(trigger);
    await page.locator('.clustrmaps-toggle').dispatchEvent('focusin');
    await page.locator('.clustrmaps-toggle').dispatchEvent('pointerenter');
    expect(await page.evaluate(() => window.prefetched)).toEqual(['/stats.svg']);
    await expect(page.locator('.cv-live-widgets-panel')).toBeHidden();
  });
}

test('data saver disables widget prefetch', async ({ page }) => {
  await fixture(page, `${nav}<section class="cv-live-widgets-section"><button class="clustrmaps-toggle">Stats</button><div class="cv-live-widgets-panel"><img data-src="/stats.svg"></div></section>`);
  await page.evaluate(() => {
    Object.defineProperty(navigator, 'connection', { value: { saveData: true } });
    window.prefetched = [];
    window.Image = class { set src(value) { window.prefetched.push(value); } };
  });
  await load(page);
  await page.locator('.clustrmaps-toggle').dispatchEvent('pointerenter');
  expect(await page.evaluate(() => window.prefetched)).toEqual([]);
});
