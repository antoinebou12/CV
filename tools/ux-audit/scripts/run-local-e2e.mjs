import { spawn } from 'node:child_process';
process.env.E2E_PORT ||= '8891';
process.env.E2E_URL = `http://127.0.0.1:${process.env.E2E_PORT}`;
delete process.env.E2E_PREFIX;
const server = spawn(process.execPath, ['scripts/serve-e2e.mjs'], { stdio: ['ignore', 'pipe', 'inherit'], env: process.env });
let started = false;
server.stdout.on('data', data => {
  process.stdout.write(data);
  if (!started && data.toString().includes('E2E site:')) {
    started = true;
    const tests = spawn(process.execPath, ['node_modules/@playwright/test/cli.js', 'test', '--config', 'playwright.e2e.config.ts', ...process.argv.slice(2)], { stdio: 'inherit', env: process.env });
    tests.on('exit', code => { server.kill(); process.exitCode = code || 0; });
  }
});
server.on('exit', code => { if (!started) process.exitCode = code || 1; });
