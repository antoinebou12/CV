import assert from 'node:assert/strict';
import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import { join, posix, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';

// Crawls the built blog for local hrefs/srcs that point at nothing. Shared page-bundle
// resources, lowercase project slugs and renamed assets have all broken links before;
// this keeps the published tree self-consistent regardless of baseURL.
const root = fileURLToPath(new URL('../../', import.meta.url));
const site = resolve(root, process.env.CV_NOTES_SITE || '_site/blog');
const home = readFileSync(resolve(site, 'index.html'), 'utf8');
const canonical = home.match(/<link[^>]+rel=["']?canonical["']?[^>]+href=["']?([^"'\s>]+)/i)
  || home.match(/href=["']?([^"'\s>]+)["']?[^>]+rel=["']?canonical/i);
assert.ok(canonical, 'home page declares a canonical URL');
const base = new URL(canonical[1]);
const prefix = base.pathname.replace(/\/$/, '');
const attr = /(?:href|src)=(?:"([^"]*)"|'([^']*)'|([^"'\s>]+))/g;
const skip = /^(?:https?:(?!\/\/)|mailto:|tel:|data:|javascript:|#|\$\{|'|&)/;

function* htmlFiles(dir) {
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) yield* htmlFiles(full);
    else if (name.endsWith('.html')) yield full;
  }
}

function target(pageUrl, raw) {
  let url = raw.trim();
  if (url.startsWith(base.origin)) url = url.slice(base.origin.length) || '/';
  if (!url || skip.test(url) || url.startsWith('//')) return null;
  if (/^https?:\/\//.test(url)) return null;
  const path = url.split('#')[0].split('?')[0];
  if (!path) return null;
  let sitePath;
  if (path.startsWith('/')) {
    if (prefix && !(path === prefix || path.startsWith(prefix + '/'))) return null; // outside the blog tree
    sitePath = prefix ? path.slice(prefix.length) || '/' : path;
  } else {
    const abs = posix.resolve(posix.dirname(pageUrl), decodeURIComponent(path));
    if (prefix && !abs.startsWith(prefix + '/')) return null;
    sitePath = prefix ? abs.slice(prefix.length) : abs;
  }
  return decodeURIComponent(sitePath);
}

test('every local link and asset reference in the built blog resolves to a file', () => {
  const broken = new Map();
  let checked = 0;
  for (const file of htmlFiles(site)) {
    const rel = '/' + posix.relative(site, file).split('\\').join('/');
    const pageUrl = posix.join(prefix || '/', rel);
    const html = readFileSync(file, 'utf8');
    for (const match of html.matchAll(attr)) {
      const raw = match[1] ?? match[2] ?? match[3] ?? '';
      const sitePath = target(pageUrl, raw);
      if (sitePath === null) continue;
      checked += 1;
      let full = resolve(site, '.' + sitePath);
      if (existsSync(full) && statSync(full).isDirectory()) full = join(full, 'index.html');
      if (!existsSync(full)) broken.set(rel, [...(broken.get(rel) || []), raw]);
    }
  }
  assert.ok(checked > 1000, `crawled ${checked} references`);
  const report = [...broken].map(([page, refs]) => `${page}\n    ${[...new Set(refs)].join('\n    ')}`).join('\n');
  assert.equal(broken.size, 0, `pages with broken local references:\n${report}`);
});
