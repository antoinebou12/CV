import { readFile } from 'node:fs/promises';
import { test as base, expect } from '@playwright/test';

// Each test executes production JavaScript against a fresh, minimal DOM.
// The synthetic origin enables storage and fragments without a web server.
export const test = base.extend({
  page: async ({ page }, use) => {
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.route('**/*', route => route.fulfill({
      contentType: 'text/html', body: '<!doctype html><html lang="en"><head></head><body></body></html>',
    }));
    await page.goto('https://unit.test/');
    await use(page);
    expect(errors, 'uncaught production script errors').toEqual([]);
  },
});
export { expect };
export async function script(page, path) {
  const content = await readFile(new URL(`../../../${path}`, import.meta.url), 'utf8');
  await page.addScriptTag({ content });
}
export async function fixture(page, html, lang = 'en') {
  await page.setContent(`<html lang="${lang}"><head></head><body>${html}</body></html>`);
}
export const nav = `<a class="skip-link" href="#main">Skip</a>
  <nav class="cv-site-nav"><button class="cv-theme-toggle"></button><button class="cv-motion-toggle"></button>
  <span class="cv-nav-lang"><a class="current" href="#en">EN</a><a href="#fr">FR</a></span></nav>
  <main id="main"></main>`;
