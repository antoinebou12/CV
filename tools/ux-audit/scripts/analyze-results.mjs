// Summarise Playwright audit output into a Markdown report.
// node scripts/analyze-results.mjs <e2e-results dir> [report.md]
// Reads every content-audit.json and project-audit.json below the directory. Findings are
// grouped by kind and by page type: one kind on every page of a type points at a template,
// a kind on a single page points at that page's content.
import { readdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

const [dir, out] = process.argv.slice(2);
if (!dir) { console.error('usage: node scripts/analyze-results.mjs <e2e-results dir> [report.md]'); process.exit(2); }

async function* walk(folder) {
  for (const entry of await readdir(folder, { withFileTypes: true })) {
    const full = path.join(folder, entry.name);
    if (entry.isDirectory()) yield* walk(full);
    else if (/^(content|project)-audit\.json$/.test(entry.name)) yield full;
  }
}

const pageType = p => {
  const m = p.replace(/^\/(?:CV\/)?blog\/(?:fr\/)?/, '').match(/^([\w-]+)\/(?:notes\/)?/);
  if (!m) return p.includes('/blog/') ? 'blog home' : 'cv';
  return p.includes('/projects/notes/') ? 'project notes' : m[1];
};

const rows = []; // { source, page, type, kind, text }
let siteRows = [];
let files = 0;
for await (const file of walk(dir)) {
  files++;
  const data = JSON.parse(await readFile(file, 'utf8'));
  const source = path.basename(path.dirname(file));
  if (data.pages) {
    for (const [page, p] of Object.entries(data.pages)) for (const f of p.findings) rows.push({ source, page, type: pageType(page), kind: f.kind, text: f.text });
    siteRows = siteRows.concat((data.site || []).map(f => ({ source, ...f })));
  } else {
    for (const [slug, p] of Object.entries(data)) {
      for (const f of p.issues || []) if (f.kind !== 'no-vertical-gap') rows.push({ source, page: slug, type: 'project notes', kind: f.kind, text: `${f.where} ${f.detail}` });
      for (const c of p.contrast || []) rows.push({ source, page: slug, type: 'project notes', kind: 'contrast', text: c });
      if (p.overflow) rows.push({ source, page: slug, type: 'project notes', kind: 'overflow', text: 'horizontal overflow' });
    }
  }
}

// A run that crashed before writing its audit file must not read as a clean run.
if (!files) { console.error(`No content-audit.json or project-audit.json below ${dir}: the run did not finish.`); process.exit(1); }

const by = (list, key) => list.reduce((map, row) => map.set(key(row), [...(map.get(key(row)) || []), row]), new Map());
const lines = ['# Audit analysis', '', `Source: \`${dir}\` · ${rows.length} page findings · ${siteRows.length} site findings`, ''];
lines.push('## By kind', '', '| Kind | Findings | Pages | Page types | Example |', '| --- | ---: | ---: | --- | --- |');
for (const [kind, list] of [...by(rows, r => r.kind)].sort((a, b) => b[1].length - a[1].length)) {
  const pages = new Set(list.map(r => r.page));
  const types = [...by(list, r => r.type)].map(([t, l]) => `${t} (${new Set(l.map(r => r.page)).size})`).join(', ');
  lines.push(`| ${kind} | ${list.length} | ${pages.size} | ${types} | ${list[0].text.replace(/\|/g, '\\|').slice(0, 90)} |`);
}
lines.push('', '## Likely template issues', '', 'The same text found on many pages comes from a shared template or partial, not from one article.', '');
const repeatedText = [...by(rows, r => `${r.kind}::${r.text.replace(/^\d+x /, '')}`)].filter(([, l]) => new Set(l.map(r => r.page)).size >= 3);
if (!repeatedText.length) lines.push('- None.');
for (const [key, list] of repeatedText.sort((a, b) => b[1].length - a[1].length).slice(0, 20)) {
  const [kind, text] = key.split('::');
  lines.push(`- **${kind}** on ${new Set(list.map(r => r.page)).size} pages: ${text.slice(0, 140)}`);
}
lines.push('', '## Site-level repetition', '');
if (!siteRows.length) lines.push('- None.');
for (const f of siteRows) lines.push(`- ${f.kind}: ${f.text}`);
lines.push('', '## Pages with the most findings', '');
for (const [page, list] of [...by(rows, r => r.page)].sort((a, b) => b[1].length - a[1].length).slice(0, 15)) {
  lines.push(`- \`${page}\`: ${list.length} (${[...new Set(list.map(r => r.kind))].join(', ')})`);
}
const report = lines.join('\n') + '\n';
if (out) await writeFile(out, report);
console.log(report);
