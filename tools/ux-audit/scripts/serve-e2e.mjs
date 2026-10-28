import { spawnSync } from 'node:child_process';
import { createServer } from 'node:http';
import { readFile, readdir, stat, mkdir, cp } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../../../', import.meta.url));
const stage = path.join(root, 'tmp/e2e-site');
const port = Number(process.env.E2E_PORT || 8765);
await mkdir(stage, { recursive: true });
const build = spawnSync('hugo', ['--minify', '-s', path.join(root, 'hugo'), '-d', path.join(stage, 'blog'), '-b', `http://127.0.0.1:${port}/blog/`], { stdio: 'inherit' });
if (build.status !== 0) process.exit(build.status || 1);
for (const name of ['index.html', 'index-en.html', 'index-fr.html', 'css', 'js', 'assets', 'images', 'papers', 'antoine-portrait.png']) {
  await cp(path.join(root, name), path.join(stage, name), { recursive: true });
}
for (const name of await readdir(root)) {
  if (/\.(png|jpe?g|webp|svg|ico|pdf)$/i.test(name)) await cp(path.join(root, name), path.join(stage, name));
}
const types = { '.html':'text/html', '.css':'text/css', '.js':'text/javascript', '.json':'application/json', '.svg':'image/svg+xml', '.png':'image/png', '.jpg':'image/jpeg', '.webp':'image/webp', '.xml':'application/xml', '.woff2':'font/woff2' };
createServer(async (req, res) => {
  try {
    const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    let file = path.resolve(stage, '.' + pathname);
    if (!file.startsWith(stage + path.sep) && file !== stage) { res.writeHead(403).end(); return; }
    if ((await stat(file)).isDirectory()) file = path.join(file, 'index.html');
    const body = await readFile(file);
    res.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'application/octet-stream' }).end(body);
  } catch { res.writeHead(404).end('Not found'); }
}).listen(port, '127.0.0.1', () => console.log(`E2E site: http://127.0.0.1:${port}`));
