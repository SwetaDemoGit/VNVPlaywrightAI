const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  timeout: 30_000,
  expect: {
    timeout: 5_000,
  },
  reporter: [['html', { open: 'never' }]],
  use: {
    baseURL: 'https://playwright.dev',
    headless: false,
    launchOptions: {
      slowMo: 3000,
    },
    ...devices['Desktop Chrome'],
  },
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        browserName: 'chromium',
      },
    },
  ],
});
