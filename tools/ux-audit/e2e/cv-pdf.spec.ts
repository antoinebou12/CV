import { test, expect } from '@playwright/test';
import { readFileSync, existsSync, writeFileSync } from 'node:fs';
import { resolve, dirname, extname } from 'node:path';
import { fileURLToPath } from 'node:url';

// LaTeX CV PDFs (cv-en/resume.pdf, cv-fr/resume.pdf): structure, text, links and a rendered
// visual check. pdf.js runs inside Chromium so the same renderer is used locally and in CI.
// Set E2E_PDF_LINKS=1 to also HEAD-check every external link (needs network).
const root = resolve(dirname(fileURLToPath(import.meta.url)), '../../..');
const PDFS = [
  { lang: 'en', file: 'cv-en/resume.pdf', mustContain: ['Antoine Boucher', 'Software Engineer', 'Experience', 'Education', 'Competences'] },
  { lang: 'fr', file: 'cv-fr/resume.pdf', mustContain: ['Antoine Boucher', 'Ingénieur logiciel', 'Expérience', 'Formation', 'Compétences'] },
];
const pdfjsDir = resolve(root, 'tools/ux-audit/node_modules/pdfjs-dist');
const MAX_PAGES = 2;
const MARGIN_PT = 18; // ink closer than this to the page edge means content escaped the margins

const types: Record<string, string> = { '.mjs': 'text/javascript', '.js': 'text/javascript', '.pdf': 'application/pdf', '.html': 'text/html', '.wasm': 'application/wasm' };

test.describe('LaTeX CV PDFs', () => {
  for (const pdf of PDFS) {
    test(`${pdf.lang}: pages, text, links and margins`, async ({ page, request }, info) => {
      const path = resolve(root, pdf.file);
      test.skip(!existsSync(path), `${pdf.file} is not built`);
      // Serve pdf.js and the PDF from a private origin so modules and the worker load normally.
      await page.route('http://pdf.local/**', (route) => {
        const url = new URL(route.request().url());
        const file = url.pathname === '/resume.pdf' ? path : url.pathname === '/' ? null : resolve(pdfjsDir, '.' + url.pathname);
        if (!file) return route.fulfill({ status: 200, contentType: 'text/html', body: '<!doctype html><title>pdf</title><body></body>' });
        if (!existsSync(file)) return route.fulfill({ status: 404, body: 'missing ' + url.pathname });
        return route.fulfill({ status: 200, contentType: types[extname(file)] || 'application/octet-stream', body: readFileSync(file) });
      });
      await page.goto('http://pdf.local/');
      const result = await page.evaluate(async ({ maxPages, margin }) => {
        const pdfjs = await import('/build/pdf.mjs');
        pdfjs.GlobalWorkerOptions.workerSrc = '/build/pdf.worker.mjs';
        const doc = await pdfjs.getDocument({ url: '/resume.pdf' }).promise;
        const pages: { index: number; width: number; height: number; text: string; links: string[]; ink: { left: number; top: number; right: number; bottom: number } | null; image: string }[] = [];
        for (let n = 1; n <= doc.numPages; n++) {
          const pg = await doc.getPage(n);
          const scale = 2;
          const viewport = pg.getViewport({ scale });
          const canvas = document.createElement('canvas');
          canvas.width = viewport.width; canvas.height = viewport.height;
          const context = canvas.getContext('2d', { willReadFrequently: true })!;
          await pg.render({ canvasContext: context, viewport }).promise;
          const text = (await pg.getTextContent()).items.map((i: any) => i.str).join(' ');
          const links = (await pg.getAnnotations()).filter((a: any) => a.subtype === 'Link' && a.url).map((a: any) => a.url as string);
          // Ink bounding box in PDF points: any non-white pixel.
          const { data } = context.getImageData(0, 0, canvas.width, canvas.height);
          let left = canvas.width, top = canvas.height, right = -1, bottom = -1;
          for (let y = 0; y < canvas.height; y += 1) {
            for (let x = 0; x < canvas.width; x += 1) {
              const o = (y * canvas.width + x) * 4;
              if (data[o] < 235 || data[o + 1] < 235 || data[o + 2] < 235) {
                if (x < left) left = x; if (x > right) right = x; if (y < top) top = y; if (y > bottom) bottom = y;
              }
            }
          }
          const ink = right < 0 ? null : { left: left / scale, top: top / scale, right: (canvas.width - right) / scale, bottom: (canvas.height - bottom) / scale };
          pages.push({ index: n, width: viewport.width / scale, height: viewport.height / scale, text, links, ink, image: canvas.toDataURL('image/png') });
        }
        return { numPages: doc.numPages, pages, maxPages, margin };
      }, { maxPages: MAX_PAGES, margin: MARGIN_PT });

      expect(result.numPages, 'page count').toBeLessThanOrEqual(MAX_PAGES);
      const fullText = result.pages.map(p => p.text).join(' ');
      for (const needle of pdf.mustContain) expect(fullText, `text contains ${needle}`).toContain(needle);
      expect(fullText).not.toMatch(/Page \d+ of \d+/);
      expect(fullText).not.toMatch(/\?\?|\\[a-z]+\{/); // unresolved references or raw LaTeX

      const links = [...new Set(result.pages.flatMap(p => p.links))];
      expect(links.length, 'has hyperlinks').toBeGreaterThan(3);
      for (const url of links) {
        expect(url, 'https, mailto or tel link').toMatch(/^(https:\/\/|mailto:|tel:\+?\d+$)/);
        expect(url, 'no whitespace or LaTeX residue in link').not.toMatch(/[\s{}\\]/);
      }
      if (process.env.E2E_PDF_LINKS === '1') {
        const broken: string[] = [];
        for (const url of links.filter(u => u.startsWith('http'))) {
          try {
            const response = await request.fetch(url, { method: 'HEAD', maxRedirects: 5, timeout: 15000 });
            if (response.status() >= 400 && response.status() !== 405 && response.status() !== 403) broken.push(`${response.status()} ${url}`);
          } catch (error) { broken.push(`${String(error).slice(0, 60)} ${url}`); }
        }
        expect(broken, 'reachable links').toEqual([]);
      }

      for (const pg of result.pages) {
        expect(pg.ink, `page ${pg.index} has content`).not.toBeNull();
        const ink = pg.ink!;
        expect(ink.left, `page ${pg.index} left margin`).toBeGreaterThanOrEqual(MARGIN_PT);
        expect(ink.right, `page ${pg.index} right margin`).toBeGreaterThanOrEqual(MARGIN_PT);
        expect(ink.top, `page ${pg.index} top margin`).toBeGreaterThanOrEqual(MARGIN_PT);
        expect(ink.bottom, `page ${pg.index} bottom margin`).toBeGreaterThanOrEqual(MARGIN_PT);
        const png = Buffer.from(pg.image.split(',')[1], 'base64');
        await info.attach(`${pdf.lang}-page-${pg.index}.png`, { body: png, contentType: 'image/png' });
        writeFileSync(info.outputPath(`${pdf.lang}-page-${pg.index}.png`), png);
      }
      await info.attach(`${pdf.lang}-links.json`, { body: JSON.stringify(links, null, 2), contentType: 'application/json' });
    });
  }
});
