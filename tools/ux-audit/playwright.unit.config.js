import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './unit',
  timeout: 15_000,
  fullyParallel: true,
  workers: 2,
  forbidOnly: !!process.env.CI,
  retries: 0,
  reporter: 'list',
  outputDir: 'unit-results',
  use: { browserName: 'chromium', trace: 'retain-on-failure' },
});
