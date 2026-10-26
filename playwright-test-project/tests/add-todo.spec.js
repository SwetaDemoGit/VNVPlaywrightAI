const { test, expect } = require('@playwright/test');

test('TODO-001: adds a single task', async ({ page }) => {
  await page.goto('https://demo.playwright.dev/todomvc/#/');

  const newTaskInput = page.getByRole('textbox', {
    name: 'What needs to be done?',
  });
  await newTaskInput.fill('Learn Playwright with Copilot');
  await newTaskInput.press('Enter');

  await expect(page.getByTestId('todo-title')).toHaveText(
    'Learn Playwright with Copilot',
  );
  await expect(page.getByTestId('todo-count')).toHaveText('1 item left');
});
