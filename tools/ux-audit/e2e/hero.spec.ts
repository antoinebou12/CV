import { test, expect, type Page } from '@playwright/test';
import { writeFile } from 'node:fs/promises';
const prefix = (process.env.E2E_PREFIX || '').replace(/\/$/, '');
// The CV hero pages and the blog home are the site's front doors.
const pages = ['/index-en.html', '/index-fr.html', '/blog/', '/blog/fr/'];

/** Load timing, transfer weight and render-blocking resources for one page load. */
async function performance(page: Page) {
  return page.evaluate(async () => {
    const lcp = await new Promise<number>(resolve => {
      let last = 0;
      new PerformanceObserver(list => { for (const e of list.getEntries()) last = e.startTime; }).observe({ type: 'largest-contentful-paint', buffered: true });
      setTimeout(() => resolve(last), 1500);
    });
    let cls = 0;
    new PerformanceObserver(list => { for (const e of list.getEntries() as any[]) if (!e.hadRecentInput) cls += e.value; }).observe({ type: 'layout-shift', buffered: true });
    await new Promise(r => setTimeout(r, 300));
    const nav = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
    const resources = performance.getEntriesByType('resource') as PerformanceResourceTiming[];
    const origin = location.origin;
    const bytes = (r: PerformanceResourceTiming) => r.transferSize || r.encodedBodySize || 0;
    const blocking = [...document.querySelectorAll('head link[rel="stylesheet"]:not([media="print"]), head script[src]:not([defer]):not([async]):not([type="module"])')]
      .map(e => (e as HTMLLinkElement).href || (e as HTMLScriptElement).src);
    return {
      ttfb: Math.round(nav.responseStart), domContentLoaded: Math.round(nav.domContentLoadedEventEnd), load: Math.round(nav.loadEventEnd),
      lcp: Math.round(lcp), cls: Math.round(cls * 1000) / 1000,
      requests: resources.length, kb: Math.round(resources.reduce((s, r) => s + bytes(r), nav.transferSize || 0) / 1024),
      thirdParty: [...new Set(resources.filter(r => !r.name.startsWith(origin)).map(r => new URL(r.name).host))],
      heaviest: resources.sort((a, b) => bytes(b) - bytes(a)).slice(0, 6).map(r => `${Math.round(bytes(r) / 1024)}KB ${r.name.replace(origin, '').slice(0, 90)}`),
      slowest: resources.sort((a, b) => b.duration - a.duration).slice(0, 4).map(r => `${Math.round(r.duration)}ms ${r.name.replace(origin, '').slice(0, 90)}`),
      renderBlocking: blocking.map(u => u.replace(origin, '')),
    };
  });
}

/** Images: broken or missing logos, oversized files, missing dimensions. Forces lazy images to load. */
async function images(page: Page) {
  return page.evaluate(async () => {
    const all = [...document.images];
    const below = all.filter(i => i.getBoundingClientRect().top > innerHeight * 1.5);
    const eagerBelowFold = below.filter(i => i.loading !== 'lazy' && !i.closest('[hidden], details:not([open])')).map(i => i.getAttribute('src') || '').slice(0, 8);
    for (const img of all) img.loading = 'eager';
    await Promise.all(all.map(img => img.decode().catch(() => undefined)));
    const shown = all.filter(i => i.getClientRects().length && !i.closest('[hidden]'));
    return {
      total: all.length,
      broken: all.filter(i => (i.getAttribute('src') || i.currentSrc) && !i.naturalWidth && !i.closest('[hidden]')).map(i => i.getAttribute('src')),
      emptySrc: all.filter(i => !i.getAttribute('src') && !i.getAttribute('data-src') && !i.srcset).length,
      remote: [...new Set(all.map(i => i.currentSrc || i.src).filter(s => s && !s.startsWith(location.origin) && !s.startsWith('data:')).map(s => new URL(s).host))],
      oversized: shown.filter(i => i.naturalWidth > 0 && i.getBoundingClientRect().width > 0 && i.naturalWidth > 2.5 * i.getBoundingClientRect().width * devicePixelRatio && i.naturalWidth > 400)
        .map(i => `${i.naturalWidth}px shown at ${Math.round(i.getBoundingClientRect().width)}px: ${i.getAttribute('src')?.slice(0, 80)}`).slice(0, 10),
      noDimensions: all.filter(i => !i.getAttribute('width') && !i.getAttribute('height') && !i.style.aspectRatio && !i.closest('.post-diagram')).map(i => i.getAttribute('src')?.slice(0, 70)).slice(0, 10),
      eagerBelowFold,
      missingAlt: all.filter(i => !i.hasAttribute('alt')).map(i => i.getAttribute('src')?.slice(0, 70)).slice(0, 10),
    };
  });
}

/** Document structure and spacing: heading order, landmarks, edge contact on phones, awkward gaps. */
async function structure(page: Page) {
  return page.evaluate(() => {
    const visible = (e: Element) => e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden';
    const heads = [...document.querySelectorAll('h1, h2, h3, h4, h5, h6')].filter(visible);
    const skips: string[] = [];
    for (let i = 1; i < heads.length; i++) {
      const a = +heads[i - 1].tagName[1], b = +heads[i].tagName[1];
      if (b - a > 1) skips.push(`${heads[i - 1].tagName}→${heads[i].tagName} "${(heads[i] as HTMLElement).innerText.trim().slice(0, 40)}"`);
    }
    const main = document.querySelector('main');
    const sections = [...(main?.querySelectorAll(':scope > section, :scope > * > section, :scope > div > section') || [])].filter(visible);
    const unlabelled = sections.filter(s => !s.querySelector('h1, h2, h3') && !s.getAttribute('aria-label') && !s.getAttribute('aria-labelledby')).map(s => `${s.className || s.id}`.slice(0, 60));
    // Text that touches the viewport edge (phones) and big empty gaps between consecutive sections.
    const edge = [...document.querySelectorAll('main p, main li, main h1, main h2, main h3, main a.btn, main button')].filter(visible)
      .filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && (r.left < 8 || innerWidth - r.right < 8); })
      .map(e => `${e.tagName}.${(e as HTMLElement).className.toString().split(' ')[0]} "${(e as HTMLElement).innerText.trim().slice(0, 30)}"`).slice(0, 8);
    const gaps: string[] = [];
    for (let i = 1; i < sections.length; i++) {
      const gap = sections[i].getBoundingClientRect().top - sections[i - 1].getBoundingClientRect().bottom;
      if (gap > 160 || gap < -2) gaps.push(`${Math.round(gap)}px before ${sections[i].id || sections[i].className.toString().split(' ')[0]}`);
    }
    // Left edges of section headings should line up; a stray offset reads as broken structure.
    const lefts = sections.map(s => s.querySelector('h2')).filter(Boolean).map(h => Math.round((h as Element).getBoundingClientRect().left));
    const common = lefts.sort((a, b) => lefts.filter(v => v === b).length - lefts.filter(v => v === a).length)[0];
    const misaligned = sections.map(s => s.querySelector('h2')).filter(h => h && Math.abs(Math.round(h.getBoundingClientRect().left) - common) > 4)
      .map(h => `"${(h as HTMLElement).innerText.trim().slice(0, 30)}" at ${Math.round(h!.getBoundingClientRect().left)}px vs ${common}px`);
    return {
      h1: document.querySelectorAll('h1').length,
      skips, unlabelled, edge, gaps, misaligned,
      landmarks: { main: !!main, nav: !!document.querySelector('nav'), footer: !!document.querySelector('footer'), skipLink: !!document.querySelector('a[href="#main"], a[href="#content"], .skip-link') },
      overflow: document.documentElement.scrollWidth > innerWidth + 2,
      height: document.documentElement.scrollHeight,
    };
  });
}

for (const width of [390, 1440]) for (const theme of ['light', 'dark'] as const) {
  test(`hero and blog home ${width} ${theme}`, async ({ page }, info) => {
    test.setTimeout(300_000);
    await page.setViewportSize({ width, height: 900 });
    await page.emulateMedia({ colorScheme: theme, reducedMotion: 'reduce' });
    const failed: string[] = [];
    page.on('requestfailed', r => failed.push(`${r.failure()?.errorText} ${r.url().slice(0, 100)}`));
    page.on('response', r => { if (r.status() >= 400) failed.push(`${r.status()} ${r.url().slice(0, 100)}`); });
    const errors: string[] = [];
    page.on('pageerror', e => errors.push(e.message));
    const report: Record<string, unknown> = {};
    for (const path of pages) {
      failed.length = 0;
      await page.goto(prefix + path, { waitUntil: 'load' });
      const perf = await performance(page);
      const shot = info.outputPath(`${path.replace(/\W+/g, '-')}.png`);
      await page.screenshot({ path: shot, fullPage: true });
      const img = await images(page);
      const layout = await structure(page);
      report[path] = { perf, images: img, structure: layout, failedRequests: [...failed] };
      expect.soft(img.broken, `${path}: broken images`).toEqual([]);
      expect.soft(failed.filter(f => !/mapmyvisitors|novatorem|clustrmaps|youtube|google/.test(f)), `${path}: failed requests`).toEqual([]);
      expect.soft(layout.overflow, `${path}: overflow`).toBe(false);
      expect.soft(layout.h1, `${path}: one h1`).toBe(1);
      expect.soft(layout.skips, `${path}: heading levels`).toEqual([]);
      expect.soft(layout.edge, `${path}: text touching the viewport edge`).toEqual([]);
      expect.soft(perf.cls, `${path}: layout shift`).toBeLessThan(0.1);
    }
    await writeFile(info.outputPath('hero-audit.json'), JSON.stringify(report, null, 2));
    await info.attach('hero-audit.json', { body: JSON.stringify(report, null, 2), contentType: 'application/json' });
    expect(errors).toEqual([]);
  });
}
