import { test, expect, type Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { writeFile } from 'node:fs/promises';
const prefix = process.env.E2E_PREFIX || '';
// E2E_PROJECTS=uml-mcp,chitui limits the run; otherwise every note linked from the directory is checked.
const only = (process.env.E2E_PROJECTS || '').split(',').filter(Boolean);
const screenshots = process.env.E2E_PROJECT_SHOTS !== '0';

async function slugs(page: Page) {
  await page.goto(`${prefix}/blog/projects/`);
  const found = await page.locator('a[href*="/projects/notes/"]').evaluateAll(links =>
    [...new Set(links.map(a => new URL((a as HTMLAnchorElement).href).pathname.match(/projects\/notes\/([\w.-]+)\//)?.[1]).filter(Boolean))]);
  return (only.length ? found.filter(slug => only.includes(slug as string)) : found) as string[];
}

/** Spacing and layout problems a reviewer would see: content touching a box edge, overflow, cramped stacks. */
async function spacing(page: Page) {
  return page.evaluate(() => {
    const boxes = [...document.querySelectorAll<HTMLElement>(
      '.repo-shell-main section, .repo-shell-main details, .repo-shell-main article, .repo-shell-main aside, .repo-shell-main .fig, .repo-shell-main .tablewrap, .repo-shell-main pre')];
    const issues: { kind: string; where: string; detail: string }[] = [];
    const name = (el: Element) => `${el.tagName.toLowerCase()}${el.id ? '#' + el.id : ''}.${[...el.classList].slice(0, 2).join('.')}`;
    for (const box of boxes) {
      if (!box.getClientRects().length) continue;
      const style = getComputedStyle(box);
      // A box only looks framed if it has a border or a background that differs from what is behind it.
      const behind = (el: Element | null): string => {
        for (; el; el = el.parentElement) {
          const bg = getComputedStyle(el).backgroundColor;
          if (bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent') return bg;
        }
        return 'none';
      };
      const ownBg = style.backgroundColor;
      const filled = ownBg !== 'rgba(0, 0, 0, 0)' && ownBg !== 'transparent' && ownBg !== behind(box.parentElement);
      const framed = parseFloat(style.borderLeftWidth) > 0 || filled;
      if (!framed) continue;
      const rect = box.getBoundingClientRect();
      const border = parseFloat(style.borderLeftWidth);
      // Visible text nodes directly inside this framed box (not inside a nested framed box).
      const walker = document.createTreeWalker(box, NodeFilter.SHOW_TEXT);
      let tightest = Infinity;
      let sample = '';
      while (walker.nextNode()) {
        const node = walker.currentNode as Text;
        if (!node.nodeValue?.trim()) continue;
        const parent = node.parentElement!;
        const owner = parent.closest('section, details, article, aside, .fig, .tablewrap, pre');
        if (owner !== box) continue;
        if (parent.closest('.sr-only')) continue;
        // Wide tables and code scroll sideways on purpose; their hidden part is reachable.
        let scroller: Element | null = parent;
        let scrolls = false;
        for (; scroller && scroller !== box.parentElement; scroller = scroller.parentElement) {
          const s2 = getComputedStyle(scroller);
          if (['auto', 'scroll'].includes(s2.overflowX) && scroller.scrollWidth > scroller.clientWidth + 1) { scrolls = true; break; }
        }
        if (scrolls) continue;
        const range = document.createRange();
        range.selectNodeContents(node);
        const r = range.getBoundingClientRect();
        if (!r.width) continue;
        const inset = Math.min(r.left - rect.left - border, rect.right - border - r.right);
        if (inset < tightest) { tightest = inset; sample = node.nodeValue.trim().slice(0, 40); }
      }
      if (tightest < 6) issues.push({ kind: 'text-touches-edge', where: name(box), detail: `${Math.round(tightest)}px: "${sample}"` });
      if (box.scrollWidth > box.clientWidth + 2 && !['auto', 'scroll'].includes(style.overflowX)) {
        issues.push({ kind: 'clipped-overflow', where: name(box), detail: `${box.scrollWidth}>${box.clientWidth}` });
      }
    }
    // Consecutive siblings with no vertical gap at all.
    for (const main of document.querySelectorAll('.repo-shell-main, .repo-dossier')) {
      const kids = [...main.children].filter(el => el.getClientRects().length && getComputedStyle(el).position !== 'absolute');
      for (let i = 1; i < kids.length; i++) {
        const gap = kids[i].getBoundingClientRect().top - kids[i - 1].getBoundingClientRect().bottom;
        if (gap < 4 && kids[i].getBoundingClientRect().height > 24) issues.push({ kind: 'no-vertical-gap', where: name(kids[i]), detail: `${Math.round(gap)}px after ${name(kids[i - 1])}` });
      }
    }
    // Copy buttons must stay inside the code block they copy.
    for (const button of document.querySelectorAll('.repo-copy')) {
      const pre = button.closest('pre');
      if (!pre || !button.getClientRects().length) continue;
      const b = button.getBoundingClientRect(), r = pre.getBoundingClientRect();
      if (b.top < r.top - 2 || b.bottom > r.bottom + 2) issues.push({ kind: 'detached-copy-button', where: name(pre.parentElement!), detail: `${Math.round(b.top - r.top)}px from its block` });
    }
    return {
      overflow: document.documentElement.scrollWidth > innerWidth + 2,
      issues,
      plainLinkRows: [...document.querySelectorAll('.repo-snapshot, .repo-reference-list, .repo-file-list')].filter(e => e.getClientRects().length).length,
    };
  });
}

for (const width of [390, 1280]) for (const theme of ['light', 'dark'] as const) {
  test(`project notes ${width} ${theme}`, async ({ page }, info) => {
    test.setTimeout(1_800_000);
    await page.setViewportSize({ width, height: 900 });
    await page.emulateMedia({ colorScheme: theme, reducedMotion: 'reduce' });
    const errors: string[] = [];
    page.on('pageerror', error => errors.push(`${page.url()}: ${error.message}`));
    const all = await slugs(page);
    expect(all.length).toBeGreaterThan(0);
    const summary: Record<string, unknown> = {};
    for (const slug of all) {
      await page.goto(`${prefix}/blog/projects/notes/${slug}/`);
      // Open every disclosure so collapsed panels are measured too.
      await page.evaluate(() => document.querySelectorAll('details').forEach(d => { (d as HTMLDetailsElement).open = true; }));
      await page.waitForTimeout(400);
      const layout = await spacing(page);
      const contrast = (await new AxeBuilder({ page }).include('.repo-shell-main').withRules(['color-contrast']).analyze()).violations
        .flatMap(v => v.nodes.map(n => `${n.target.join(' ')} :: ${n.any[0]?.message?.slice(0, 110)}`));
      summary[slug] = { ...layout, contrast };
      if (screenshots) await page.screenshot({ path: info.outputPath(`${slug}.png`), fullPage: true });
      expect.soft(layout.overflow, `${slug}: horizontal overflow`).toBe(false);
      expect.soft(layout.issues.filter(i => i.kind !== 'no-vertical-gap'), `${slug}: spacing`).toEqual([]);
      expect.soft(contrast, `${slug}: contrast`).toEqual([]);
    }
    const report = JSON.stringify(summary, null, 2);
    await writeFile(info.outputPath('project-audit.json'), report);
    await info.attach('project-audit.json', { body: report, contentType: 'application/json' });
    expect(errors).toEqual([]);
  });
}
