import { test, expect, chromium } from '@playwright/test';
const prefix = process.env.E2E_PREFIX || '';
for (const channel of ['chrome', 'msedge'] as const) test(`native WebMCP ${channel}`, async () => {
  const browser = await chromium.launch({ channel, args: ['--enable-features=WebMCP', '--enable-blink-features=WebMCP'] });
  const page = await browser.newPage({ baseURL: process.env.E2E_URL || 'http://127.0.0.1:8934' });
  try {
    for (const route of ['index-en.html', 'index-fr.html', 'blog/posts/ipc-toolkit-contact-library/', 'blog/fr/projects/notes/artemis-switch/']) {
      await page.goto(`${prefix}/${route}`);
      await expect(page.locator('html')).toHaveAttribute('data-webmcp', 'ready');
      const report = await page.evaluate(async () => {
        const api = (document as any).modelContext;
        const tools = await api.getTools();
        const call = async (name: string, input: object) => {
          const tool = tools.find((item: any) => item.name === name);
          let response;
          try { response = await api.executeTool(tool, input); }
          catch (error) { if (!(error as Error).message.startsWith('Failed to parse input')) throw error; response = await api.executeTool(tool, JSON.stringify(input)); }
          return typeof response === 'string' ? JSON.parse(response) : response;
        };
        const outlineResult = await call('website_get_outline', {});
        const outline = JSON.parse(outlineResult.content[0].text);
        const section = outline.sections.find((item: any) => item.level === 2) || outline.sections[0];
        const read = await call('website_read_section', { section_id: section.id });
        const search = await call('website_search_page', { query: section.title });
        const invalid = await call('website_read_section', { section_id: 'not-a-section' });
        const badInput = await call('website_search_page', { query: '', surprise: true });
        const shown = await call('website_show_section', { section_id: section.id });
        return { names: tools.map((item: any) => item.name), outline, read: JSON.parse(read.content[0].text), search: JSON.parse(search.content[0].text), invalid, badInput, shown, focused: document.activeElement?.id, sectionId: section.id };
      });
      expect(report.names).toEqual(expect.arrayContaining(['website_get_outline', 'website_read_section', 'website_search_page', 'website_show_section']));
      expect(report.outline.sections.length).toBeGreaterThan(0);
      expect(report.read.id).toBe(report.sectionId);
      expect(report.search.total).toBeGreaterThan(0);
      expect(report.invalid.isError).toBe(true);
      expect(report.badInput.isError).toBe(true);
      expect(report.focused).toBe(report.sectionId);
    }
  } finally { await browser.close(); }
});
test('unsupported browsers retain normal page behavior', async ({ page }) => {
  await page.addInitScript(() => Object.defineProperty(document, 'modelContext', { value: undefined }));
  await page.goto(`${prefix}/index-en.html`);
  await expect(page.locator('html')).toHaveAttribute('data-webmcp', 'unsupported');
  await expect(page.locator('#photo-header')).toBeVisible();
});
