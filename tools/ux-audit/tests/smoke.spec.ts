import { test, expect } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const fixtures = JSON.parse(readFileSync(resolve(root, 'fixtures.json'), 'utf8'));
const hugoBase = process.env.SITE_URL || fixtures.hugoBase;

async function noHorizontalOverflow(page: import('@playwright/test').Page) {
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  );
  expect(overflow, 'page must not horizontally overflow').toBe(false);
}

test.describe('project note hard gates', () => {
  for (const slug of ['chitui', 'tch099', 'mediaboxdockercompose', 'ipc-toolkit']) {
    test(`${slug}: installation before architecture`, async ({ page }) => {
      await page.goto(`${hugoBase}/projects/notes/${slug}/`);
      const order = await page.evaluate(() => {
        const marker = (id: string) => {
          const el = document.getElementById(id);
          return el ? el.getBoundingClientRect().top + window.scrollY : -1;
        };
        return {
          install: marker('installation'),
          arch: marker('architecture'),
          title: document.getElementById('single-post-title')?.textContent || '',
        };
      });
      expect(order.title.length).toBeGreaterThan(3);
      expect(order.install).toBeGreaterThan(0);
      expect(order.arch).toBeGreaterThan(order.install);
      await noHorizontalOverflow(page);
    });
  }

  test('catalog search filters without a search service', async ({ page }) => {
    await page.goto(`${hugoBase}/projects/`);
    const search = page.locator('[data-repo-search]');
    await expect(search).toBeVisible();
    await search.fill('zzzz-no-such-project-xyz');
    await expect(page.locator('[data-repo-empty]')).toBeVisible();
    await page.locator('[data-repo-reset]').click();
    await expect(page.locator('[data-repo-empty]')).toBeHidden();
    const count = Number(await page.locator('[data-repo-count]').textContent());
    expect(count).toBeGreaterThan(10);
  });

  test('tch099 exposes deployment topology', async ({ page }) => {
    await page.goto(`${hugoBase}/projects/notes/tch099/`);
    await expect(page.locator('#deployment')).toBeVisible();
    await expect(page.locator('.repo-topology')).toBeVisible();
  });

  test('ipc-toolkit exposes algorithm section', async ({ page }) => {
    await page.goto(`${hugoBase}/projects/notes/ipc-toolkit/`);
    await expect(page.locator('#algorithm')).toBeVisible();
  });
});
