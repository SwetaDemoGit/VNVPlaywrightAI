# Playwright Test Project

A small, beginner-friendly browser automation project using JavaScript, Node.js, and Playwright Test. It runs tests in Chromium and includes an example test for the Playwright homepage.

## Requirements

- Node.js (LTS recommended)
- npm

## Install

From this directory, install the project dependencies and Chromium:

```bash
npm install
npx playwright install chromium
```

## Run tests

Run all tests in headless mode:

```bash
npm test
```

Run all tests with a visible browser:

```bash
npm run test:headed
```

Open the HTML report after a test run:

```bash
npm run report
```

## Project structure

```text
playwright-test-project/
├── tests/
│   └── example.spec.js
├── .gitignore
├── package.json
├── playwright.config.js
└── README.md
```

The shared `baseURL` is set in `playwright.config.js`, so tests can navigate to paths such as `/` with `page.goto('/')`. The configuration also sets a 30-second test timeout, a 5-second assertion timeout, Chromium, and the HTML reporter.
