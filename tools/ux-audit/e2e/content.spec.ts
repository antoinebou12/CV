import { test, expect, type Page } from '@playwright/test';
import { writeFile } from 'node:fs/promises';
const prefix = (process.env.E2E_PREFIX || '').replace(/\/$/, '');
const limit = process.env.E2E_LIMIT ? Number(process.env.E2E_LIMIT) : Infinity;

type Finding = { kind: string; text: string };

async function sitemapUrls(page: Page, baseURL: string) {
  const urls = new Set<string>();
  const seen = new Set<string>();
  const visit = async (url: string) => {
    if (seen.has(url)) return;
    seen.add(url);
    const xml = await (await page.request.get(url)).text();
    for (const [, loc] of xml.matchAll(/<loc>(.*?)<\/loc>/g)) {
      const target = new URL(new URL(loc.replaceAll('&amp;', '&')).pathname, baseURL).href;
      if (/<sitemapindex/.test(xml)) await visit(target);
      else urls.add(target);
    }
  };
  await visit(new URL(`${prefix}/blog/sitemap.xml`, baseURL).href);
  return [...urls].sort();
}

/** Formatting and repetition problems in the main content of one page. */
async function audit(page: Page) {
  return page.evaluate(() => {
    const findings: { kind: string; text: string }[] = [];
    const root = document.querySelector('main') || document.body;
    const visible = (el: Element) => el.getClientRects().length > 0 && !el.closest('nav, footer, header, script, style, pre, code, .sr-only, [aria-hidden="true"], svg, .post-diagram, .repo-mermaid-source');
    const clean = (s: string) => s.replace(/\s+/g, ' ').trim();
    const fr = document.documentElement.lang.startsWith('fr');

    // Repeated paragraphs and list items (same visible text twice on one page).
    const blocks = [...root.querySelectorAll('p, li, dd, blockquote, figcaption, td')].filter(visible)
      .filter(el => !el.querySelector('p, li, ul, ol, table'))
      .map(el => clean((el as HTMLElement).innerText)).filter(t => t.length >= 60);
    const blockCount = new Map<string, number>();
    blocks.forEach(t => blockCount.set(t, (blockCount.get(t) || 0) + 1));
    for (const [t, n] of blockCount) if (n > 1) findings.push({ kind: 'repeated-block', text: `${n}x ${t.slice(0, 120)}` });

    // Repeated sentences across different blocks (catches copy-pasted intros and closers).
    const sentenceCount = new Map<string, number>();
    for (const t of new Set(blocks)) for (const s of t.split(/(?<=[.!?])\s+/)) {
      const k = s.trim();
      if (k.length >= 50) sentenceCount.set(k, (sentenceCount.get(k) || 0) + 1);
    }
    for (const [s, n] of sentenceCount) if (n > 1) findings.push({ kind: 'repeated-sentence', text: `${n}x ${s.slice(0, 120)}` });

    // Duplicate headings at the same level.
    const heads = [...root.querySelectorAll('h1, h2, h3, h4')].filter(visible).map(h => `${h.tagName} ${clean((h as HTMLElement).innerText).replace(/\s+\d+$/, '')}`);
    const headCount = new Map<string, number>();
    heads.forEach(h => headCount.set(h, (headCount.get(h) || 0) + 1));
    for (const [h, n] of headCount) if (n > 1) findings.push({ kind: 'duplicate-heading', text: `${n}x ${h}` });
    for (const h of root.querySelectorAll('h1, h2, h3, h4')) {
      if (visible(h) && !clean((h as HTMLElement).innerText) && !h.querySelector('img, svg')) findings.push({ kind: 'empty-heading', text: h.outerHTML.slice(0, 100) });
    }

    // Text-level formatting, checked inside each block so adjacent elements never merge into false matches.
    const textBlocks = [...root.querySelectorAll('p, li, dd, dt, td, th, figcaption, blockquote, summary, h1, h2, h3, h4, .repo-evidence-label')]
      .filter(visible).filter(el => !el.querySelector('p, li, ul, ol, table, h1, h2, h3, h4'))
      // Inline code (image tags, commands, identifiers) is not prose: "alpine:edge alpine:latest" or "ruff check ." are fine.
      .map(el => { const copy = el.cloneNode(true) as HTMLElement; copy.querySelectorAll('code, kbd, samp').forEach(n => n.replaceWith('Ⓒ')); return clean(copy.textContent || ''); })
      .filter(Boolean);
    const checks: [string, RegExp][] = [
      ['markdown-residue', /\*\*[^*\s][^*]{0,60}\*\*|(?:^|\s)#{2,6}\s\S|\]\((?:https?:|\/)[^)]*\)/g],
      ['template-residue', /\{\{[<%]?|ZgotmplZ|\bundefined\b|\bNaN\b|\[object Object\]/g],
      ['escaped-entity', /&(?:amp|lt|gt|quot|#\d+);/g],
      ['doubled-word', /\b([A-Za-zÀ-ÿ]{3,})\s+\1\b/gi],
      ['placeholder', /\b(?:TODO|TBD|FIXME|lorem ipsum)\b/gi],
    ];
    if (!fr) checks.push(['space-before-punctuation', /\w\s+[,.;:!?](?=\s|$)/g]);
    for (const text of new Set(textBlocks)) for (const [kind, re] of checks) {
      for (const m of [...text.matchAll(re)].slice(0, 2)) findings.push({ kind, text: text.slice(Math.max(0, m.index! - 30), m.index! + m[0].length + 30) });
    }

    // English interface words on French pages (buttons, summaries, labels).
    if (fr) {
      // Only words that are unambiguously English: "Source", "Service" and "Client" are French too.
      const english = /^(Show|Hide|Read more|Previous|Next|Search|Copy|Copied|Updated|Download|Back|Expand|Collapse|View source|Steps as text|Layered view|Not detected|Nothing found)\b/;
      for (const el of root.querySelectorAll('button, summary, .repo-evidence-label, .repo-badge, h2, h3, h4')) {
        // README excerpts are quoted in their original language on purpose.
        if (el.closest('.repo-guide-chapter, .repo-source-excerpt, .repo-source-markdown')) continue;
        const t = clean((el as HTMLElement).innerText);
        if (visible(el) && english.test(t)) findings.push({ kind: 'english-on-french-page', text: t.slice(0, 80) });
      }
    }
    return {
      title: document.title,
      description: document.querySelector('meta[name="description"]')?.getAttribute('content') || '',
      h1: clean((document.querySelector('h1') as HTMLElement | null)?.innerText || ''),
      findings,
    };
  });
}

test('content formatting and repetition on every sitemap page', async ({ page, baseURL }, info) => {
  test.setTimeout(3_600_000);
  const urls = (await sitemapUrls(page, baseURL!)).slice(0, limit);
  expect(urls.length).toBeGreaterThan(0);
  const pages: Record<string, { title: string; description: string; h1: string; findings: Finding[] }> = {};
  for (const url of urls) {
    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30_000 });
      await page.evaluate(() => document.querySelectorAll('details').forEach(d => { (d as HTMLDetailsElement).open = true; }));
      pages[new URL(url).pathname] = await audit(page);
    } catch (error) {
      pages[new URL(url).pathname] = { title: '', description: '', h1: '', findings: [{ kind: 'load-error', text: String(error).slice(0, 160) }] };
    }
  }
  // Site-level repetition: the same title or description on several pages.
  const site: Finding[] = [];
  for (const field of ['title', 'description'] as const) {
    const groups = new Map<string, string[]>();
    for (const [path, p] of Object.entries(pages)) {
      if (!p[field]) continue;
      const key = `${/\/fr\//.test(path) ? 'fr' : 'en'}::${p[field]}`;
      groups.set(key, [...(groups.get(key) || []), path]);
    }
    for (const [value, paths] of groups) if (paths.length > 1 && !paths.every(p => /\/(?:page|tags|categories)\//.test(p))) {
      site.push({ kind: `duplicate-${field}`, text: `${paths.length}x "${value.split('::')[1].slice(0, 80)}": ${paths.slice(0, 4).join(', ')}` });
    }
  }
  const report = { pages, site };
  await writeFile(info.outputPath('content-audit.json'), JSON.stringify(report, null, 2));
  await info.attach('content-audit.json', { body: JSON.stringify(report, null, 2), contentType: 'application/json' });
  const blocking = new Set(['markdown-residue', 'template-residue', 'escaped-entity', 'doubled-word', 'placeholder', 'empty-heading', 'repeated-block', 'load-error']);
  for (const [path, p] of Object.entries(pages)) {
    expect.soft(p.findings.filter(f => blocking.has(f.kind)), path).toEqual([]);
  }
  expect.soft(site.filter(f => f.kind === 'duplicate-title'), 'duplicate titles').toEqual([]);
});
