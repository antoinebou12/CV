import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const fixtures = JSON.parse(readFileSync(resolve(root, 'fixtures.json'), 'utf8'));
const hugoBase = process.env.SITE_URL || fixtures.hugoBase;
const cvBase = process.env.CV_URL || fixtures.cvBase;

async function check(url) {
  try {
    const res = await fetch(url, { redirect: 'follow' });
    return { url, ok: res.ok, status: res.status };
  } catch (error) {
    return { url, ok: false, status: 0, error: String(error.message || error) };
  }
}

const targets = [
  `${cvBase}/index-en.html`,
  `${hugoBase}/projects/`,
  `${hugoBase}/projects/notes/chitui/`,
  `${hugoBase}/projects/notes/tch099/`,
  `${hugoBase}/projects/notes/mediaboxdockercompose/`,
  `${hugoBase}/projects/notes/ipc-toolkit/`,
];

const results = [];
for (const url of targets) results.push(await check(url));
for (const row of results) {
  console.log(`${row.ok ? 'OK' : 'FAIL'} ${row.status} ${row.url}${row.error ? ` (${row.error})` : ''}`);
}
if (results.some((row) => !row.ok)) {
  console.error('\nPreflight failed. Start a static CV server and Hugo (or set SITE_URL / CV_URL).');
  process.exit(1);
}
console.log('\nPreflight passed.');
