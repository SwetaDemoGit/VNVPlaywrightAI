const { test, expect } = require('@playwright/test');

const appUrl = 'https://demo.playwright.dev/todomvc/#/';

test.beforeEach(async ({ page }) => {
  await page.goto(appUrl);
});

async function addTodo(page, title) {
  const newTodoInput = page.getByRole('textbox', {
    name: 'What needs to be done?',
  });
  await newTodoInput.fill(title);
  await newTodoInput.press('Enter');
}

function todoItems(page) {
  return page.getByTestId('todo-item');
}

test('TODO-002: adds multiple tasks as separate list items', async ({ page }) => {
  await addTodo(page, 'Buy groceries');
  await addTodo(page, 'Read a book');

  await expect(todoItems(page)).toHaveCount(2);
  await expect(page.getByTestId('todo-count')).toHaveText('2 items left');
});

test('TODO-003: does not add an empty task', async ({ page }) => {
  await page
    .getByRole('textbox', { name: 'What needs to be done?' })
    .press('Enter');

  await expect(todoItems(page)).toHaveCount(0);
});

test('TODO-004: does not add a whitespace-only task', async ({ page }) => {
  const newTodoInput = page.getByRole('textbox', {
    name: 'What needs to be done?',
  });
  await newTodoInput.fill('   ');
  await newTodoInput.press('Enter');

  await expect(todoItems(page)).toHaveCount(0);
});

test('TODO-005: allows duplicate task titles as separate tasks', async ({ page }) => {
  await addTodo(page, 'Repeat task');
  await addTodo(page, 'Repeat task');

  await expect(todoItems(page)).toHaveCount(2);
  await expect(page.getByTestId('todo-title')).toHaveText([
    'Repeat task',
    'Repeat task',
  ]);
});

test('TODO-006: displays punctuation and non-ASCII task text literally', async ({
  page,
}) => {
  const taskTitle = 'Review <tags> & “quotes” — café';
  await addTodo(page, taskTitle);

  await expect(page.getByTestId('todo-title')).toHaveText(taskTitle);
  await expect(page.getByRole('listitem').filter({ hasText: taskTitle })).toHaveCount(
    1,
  );
});

test('TODO-007: completing one task updates its state and active count', async ({
  page,
}) => {
  await addTodo(page, 'Task A');
  await addTodo(page, 'Task B');

  const taskA = todoItems(page).filter({ hasText: 'Task A' });
  const taskB = todoItems(page).filter({ hasText: 'Task B' });
  await taskA.getByRole('checkbox', { name: 'Toggle Todo' }).check();

  await expect(taskA.getByRole('checkbox', { name: 'Toggle Todo' })).toBeChecked();
  await expect(taskB.getByRole('checkbox', { name: 'Toggle Todo' })).not.toBeChecked();
  await expect(page.getByTestId('todo-count')).toHaveText('1 item left');
});

test('TODO-008: reactivates a completed task', async ({ page }) => {
  await addTodo(page, 'Task A');
  const task = todoItems(page).filter({ hasText: 'Task A' });
  const toggle = task.getByRole('checkbox', { name: 'Toggle Todo' });

  await toggle.check();
  await toggle.uncheck();

  await expect(toggle).not.toBeChecked();
  await expect(page.getByTestId('todo-count')).toHaveText('1 item left');
});

test('TODO-009: toggles all tasks between completed and active', async ({
  page,
}) => {
  await addTodo(page, 'Task A');
  await addTodo(page, 'Task B');
  const toggleAll = page.getByLabel('Mark all as complete');

  await toggleAll.check();
  await expect(
    todoItems(page).getByRole('checkbox', { name: 'Toggle Todo' }),
  ).toHaveCount(2);
  await expect(
    todoItems(page).getByRole('checkbox', { name: 'Toggle Todo' }).nth(0),
  ).toBeChecked();
  await expect(
    todoItems(page).getByRole('checkbox', { name: 'Toggle Todo' }).nth(1),
  ).toBeChecked();

  await toggleAll.uncheck();
  await expect(
    todoItems(page).getByRole('checkbox', { name: 'Toggle Todo' }).nth(0),
  ).not.toBeChecked();
  await expect(
    todoItems(page).getByRole('checkbox', { name: 'Toggle Todo' }).nth(1),
  ).not.toBeChecked();
});

test('TODO-010: Active filter shows only active tasks', async ({ page }) => {
  await addTodo(page, 'Task A');
  await addTodo(page, 'Task B');
  await todoItems(page)
    .filter({ hasText: 'Task B' })
    .getByRole('checkbox', { name: 'Toggle Todo' })
    .check();

  await page.getByRole('link', { name: 'Active' }).click();

  await expect(todoItems(page)).toHaveCount(1);
  await expect(page.getByTestId('todo-title')).toHaveText('Task A');
});

test('TODO-011: Completed filter shows only completed tasks', async ({
  page,
}) => {
  await addTodo(page, 'Task A');
  await addTodo(page, 'Task B');
  await todoItems(page)
    .filter({ hasText: 'Task B' })
    .getByRole('checkbox', { name: 'Toggle Todo' })
    .check();

  await page.getByRole('link', { name: 'Completed' }).click();

  await expect(todoItems(page)).toHaveCount(1);
  await expect(page.getByTestId('todo-title')).toHaveText('Task B');
});

test('TODO-012: All filter shows active and completed tasks', async ({
  page,
}) => {
  await addTodo(page, 'Task A');
  await addTodo(page, 'Task B');
  await todoItems(page)
    .filter({ hasText: 'Task B' })
    .getByRole('checkbox', { name: 'Toggle Todo' })
    .check();
  await page.getByRole('link', { name: 'Completed' }).click();
  await page.getByRole('link', { name: 'All' }).click();

  await expect(todoItems(page)).toHaveCount(2);
  await expect(page.getByTestId('todo-title')).toHaveText(['Task A', 'Task B']);
});

test('TODO-013: saves an edited task title', async ({ page }) => {
  await addTodo(page, 'Original title');
  await page.getByTestId('todo-title').dblclick();

  const editInput = page.getByRole('textbox', { name: 'Edit' });
  await editInput.fill('Updated title');
  await editInput.press('Enter');

  await expect(page.getByTestId('todo-title')).toHaveText('Updated title');
});

test('TODO-014: cancels an edit with Escape', async ({ page }) => {
  await addTodo(page, 'Original title');
  await page.getByTestId('todo-title').dblclick();

  const editInput = page.getByRole('textbox', { name: 'Edit' });
  await editInput.fill('Temporary title');
  await editInput.press('Escape');

  await expect(page.getByTestId('todo-title')).toHaveText('Original title');
});

test('TODO-015: deletes one task and retains other tasks', async ({ page }) => {
  await addTodo(page, 'Task A');
  await addTodo(page, 'Task B');
  const taskA = todoItems(page).filter({ hasText: 'Task A' });
  await taskA.hover();
  await taskA.getByRole('button', { name: 'Delete' }).click();

  await expect(page.getByTestId('todo-title')).toHaveText('Task B');
  await expect(todoItems(page)).toHaveCount(1);
});

test('TODO-016: clears completed tasks and retains active tasks', async ({
  page,
}) => {
  await addTodo(page, 'Task A');
  await addTodo(page, 'Task B');
  await todoItems(page)
    .filter({ hasText: 'Task A' })
    .getByRole('checkbox', { name: 'Toggle Todo' })
    .check();
  await page.getByRole('button', { name: 'Clear completed' }).click();

  await expect(page.getByTestId('todo-title')).toHaveText('Task B');
  await expect(todoItems(page)).toHaveCount(1);
});

test('TODO-017: retains tasks after reloading the page', async ({ page }) => {
  await addTodo(page, 'Task A');
  await addTodo(page, 'Task B');
  await page.reload();

  await expect(page.getByTestId('todo-title')).toHaveText(['Task A', 'Task B']);
});

test('TODO-018: updates the remaining count for zero, one, and multiple active tasks', async ({
  page,
}) => {
  await expect(page.getByTestId('todo-count')).toHaveCount(0);

  await addTodo(page, 'Task A');
  await expect(page.getByTestId('todo-count')).toHaveText('1 item left');

  await addTodo(page, 'Task B');
  await expect(page.getByTestId('todo-count')).toHaveText('2 items left');

  await todoItems(page)
    .filter({ hasText: 'Task A' })
    .getByRole('checkbox', { name: 'Toggle Todo' })
    .check();
  await expect(page.getByTestId('todo-count')).toHaveText('1 item left');
});
