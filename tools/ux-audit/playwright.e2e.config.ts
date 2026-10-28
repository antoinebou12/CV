import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e', timeout: 90_000, workers: 1, retries: 0,
  outputDir: process.env.E2E_OUTPUT || 'e2e-results',
  reporter: [['list'], ['html', { outputFolder: process.env.E2E_REPORT || 'e2e-report', open: 'never' }]],
  use: { baseURL: process.env.E2E_URL || 'http://127.0.0.1:8765',
    browserName: 'chromium', channel: process.env.E2E_CHANNEL || undefined,
    screenshot: 'only-on-failure', trace: 'retain-on-failure' },
});
