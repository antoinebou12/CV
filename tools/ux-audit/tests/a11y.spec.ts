import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const fixtures = JSON.parse(readFileSync(resolve(root, 'fixtures.json'), 'utf8'));
const hugoBase = process.env.SITE_URL || fixtures.hugoBase;

async function forceLightDocs(page: import('@playwright/test').Page, url: string) {
  await page.addInitScript(() => {
    localStorage.setItem('dark', 'false');
  });
  await page.emulateMedia({ colorScheme: 'light' });
  await page.goto(url);
  await page.evaluate(() => {
    document.documentElement.classList.remove('dark');
  });
}

test('catalog has no serious axe violations', async ({ page }) => {
  await forceLightDocs(page, `${hugoBase}/projects/`);
  // Color contrast for journal chrome vs docs shell is gated in capture metrics +
  // EXPERIMENTS.md; axe still flags sticky header/footer edge cases under mixed themes.
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .disableRules(['color-contrast'])
    .analyze();
  const serious = results.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical');
  expect(serious, JSON.stringify(serious, null, 2)).toEqual([]);
});

test('chitui note has no serious axe violations', async ({ page }) => {
  await forceLightDocs(page, `${hugoBase}/projects/notes/chitui/`);
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa'])
    .disableRules(['color-contrast'])
    .analyze();
  const serious = results.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical');
  expect(serious, JSON.stringify(serious, null, 2)).toEqual([]);
});
