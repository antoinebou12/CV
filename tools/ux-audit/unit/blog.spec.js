import { test, expect, fixture, script } from './helpers.js';

const glossary = `<section data-glossary><div data-glossary-search hidden><input data-glossary-query></div>
  <p data-glossary-status data-count="results" data-empty="No results"></p>
  <details data-glossary-entry id="outer"><summary>Sécurité</summary><p>Authentication and accès</p>
  <details id="inner"><summary>Nested</summary><p id="café">Secret storage</p></details></details>
  <details data-glossary-entry><summary>Cache</summary><p>Memory and performance</p></details></section>`;
const reader = page => script(page, 'hugo/assets/documentation-reader.js');
const media = page => script(page, 'hugo/assets/article-media.js');
const image = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="20" height="20"%3E%3C/svg%3E';

test('glossary search becomes available when JavaScript initializes', async ({ page }) => {
  await fixture(page, glossary);
  await reader(page);
  await expect(page.locator('[data-glossary-search]')).toBeVisible();
});

for (const query of ['securite', 'SÉCURITÉ', '  sécurité  ', 'ACCES', 'authentication']) {
  test(`glossary matches normalized titles and definitions: ${query}`, async ({ page }) => {
    await fixture(page, glossary);
    await reader(page);
    await page.locator('input').fill(query);
    await expect(page.locator('[data-glossary-entry]:visible')).toHaveCount(1);
    await expect(page.locator('[data-glossary-status]')).toHaveText('1 results');
    await expect(page.locator('#outer')).toBeVisible();
  });
}

test('glossary empty state clears when the query is reset', async ({ page }) => {
  await fixture(page, glossary);
  await reader(page);
  await page.locator('input').fill('unknown term');
  await expect(page.locator('[data-glossary-status]')).toHaveText('No results');
  await expect(page.locator('[data-glossary-entry]:visible')).toHaveCount(0);
  await page.locator('input').fill('');
  await expect(page.locator('[data-glossary-entry]:visible')).toHaveCount(2);
  await expect(page.locator('[data-glossary-status]')).toHaveText('2 results');
});

for (const initial of [true, false]) {
  test(`encoded fragment opens every ancestor disclosure (${initial ? 'initial' : 'hashchange'})`, async ({ page }) => {
    await fixture(page, glossary);
    if (initial) await page.evaluate(() => history.replaceState(null, '', '#caf%C3%A9'));
    await reader(page);
    if (!initial) await page.evaluate(() => { location.hash = 'caf%C3%A9'; });
    await expect(page.locator('#outer')).toHaveAttribute('open', '');
    await expect(page.locator('#inner')).toHaveAttribute('open', '');
    await expect(page.locator('[id="café"]')).toBeVisible();
  });
}

for (const hash of ['#%E0%A4%A', '#missing']) {
  test(`reader ignores invalid or missing fragment ${hash}`, async ({ page }) => {
    await fixture(page, glossary);
    await page.evaluate(hash => history.replaceState(null, '', hash), hash);
    await reader(page);
    await expect(page.locator('#outer')).not.toHaveAttribute('open', '');
  });
}

test('reader is safe on a page without documentation controls', async ({ page }) => {
  await fixture(page, '<main>Article</main>');
  await reader(page);
  await expect(page.locator('main')).toHaveText('Article');
});

for (const lang of ['en', 'fr']) {
  test(`article preview labels, caption, original link and focus: ${lang}`, async ({ page }) => {
    await fixture(page, `<article class="journal-article"><div class="single-post-content"><figure><img src='${image}' alt="Architecture"><figcaption>Service layout</figcaption></figure></div></article>`, lang);
    await media(page);
    const opener = page.locator('.article-media-open');
    await expect(opener).toHaveAccessibleName(`${lang === 'fr' ? 'Agrandir l’image' : 'Enlarge image'}: Architecture`);
    await opener.click();
    const dialog = page.getByRole('dialog');
    await expect(dialog).toBeVisible();
    await expect(dialog.locator('p')).toHaveText('Service layout');
    await expect(dialog.locator('img')).toHaveAttribute('alt', 'Architecture');
    await expect(dialog.locator('a')).toHaveAttribute('href', image);
    await expect(dialog.locator('a')).toHaveAttribute('rel', 'noopener noreferrer');
    const close = dialog.getByRole('button', { name: lang === 'fr' ? 'Fermer' : 'Close' });
    await expect(close).toBeFocused();
    await close.click();
    await expect(dialog).toBeHidden();
    await expect(opener).toBeFocused();
  });
}

test('Escape closes an image preview and restores keyboard focus', async ({ page }) => {
  await fixture(page, `<article class="journal-article"><div class="article-single-hero"><img src='${image}' alt="Hero"></div></article>`);
  await media(page);
  await page.locator('.article-media-open').click();
  await page.keyboard.press('Escape');
  await expect(page.locator('dialog')).toBeHidden();
  await expect(page.locator('.article-media-open')).toBeFocused();
});

for (const wrapper of ['a', 'button', 'div data-deck-viewer', 'div class="diagram-interactive"', 'div class="repo-progressive-diagram"']) {
  test(`article media preserves existing interactive images: ${wrapper}`, async ({ page }) => {
    const tag = wrapper.split(' ')[0];
    await fixture(page, `<article class="journal-article"><div class="single-post-content"><${wrapper}><img src='${image}' alt="Interactive"></${tag}></div></article>`);
    await media(page);
    await expect(page.locator('.article-media-open')).toHaveCount(0);
    await expect(page.locator('dialog')).toHaveCount(0);
  });
}

test('preview falls back to alt text and safely displays caption markup as text', async ({ page }) => {
  await fixture(page, `<article class="journal-article"><div class="single-post-content"><img src='${image}' alt="&lt;b&gt;Diagram&lt;/b&gt;"></div></article>`);
  await media(page);
  await page.locator('.article-media-open').click();
  await expect(page.locator('dialog p')).toHaveText('<b>Diagram</b>');
  await expect(page.locator('dialog p b')).toHaveCount(0);
});

test('initializing article media again does not nest image buttons', async ({ page }) => {
  await fixture(page, `<article class="journal-article"><div class="single-post-content"><img src='${image}' alt="Diagram"></div></article>`);
  await media(page);
  await media(page);
  await expect(page.locator('.article-media-open')).toHaveCount(1);
  await expect(page.locator('dialog')).toHaveCount(1);
});
