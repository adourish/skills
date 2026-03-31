# E2E Testing — Salesforce + Playwright

## Quick Reference

**Use when:** Testing UI features against the live Salesforce org; verifying acceptance criteria in the browser; "test in the UI", "do e2e", "test in the browser", "test the UI"
**Don't use when:** Unit tests (use Apex test runner or Jest); pure API validation (use Postman/curl)
**Trigger phrases:** "e2e test", "test in the ui", "test the ui", "do e2e", "test in the browser", "ui test", "run playwright", "smoke test", "acceptance test in browser"
**Time:** 5–30 min depending on spec complexity
**Repo:** `https://ehbads.hrsa.gov/ads/EHBs/EHBs/_git/BPHC-GAM2010`

---

## Overview

E2E tests for BPHC-GAM2010 use **Playwright** (CLI + spec files) against the **dmedev5** Salesforce org. Authentication is handled via the Salesforce CLI frontdoor URL pattern — no credentials are embedded in tests.

```
Pattern:
  sf org open --url-only → authenticated frontdoor URL
      ↓
  npx playwright test → spec files in Tests/e2e/
      ↓
  Screenshots in Tests/screenshots/
```

---

## Phase 1 — Setup

### 1.1 — Get Authenticated Frontdoor URL

```bash
# Returns a one-time authenticated URL (no browser pop-up)
SF_URL=$(sf org open --target-org dmedev5 --url-only 2>&1 | grep "^https")
echo $SF_URL
```

Append `retURL` to land on a specific page:

```bash
# Reviews & Monitoring page
FULL_URL="${SF_URL}&retURL=%2Flightning%2Fn%2FReviews_and_Monitoring"

# A specific record
FULL_URL="${SF_URL}&retURL=%2Flightning%2Fr%2FAccount%2F{recordId}%2Fview"
```

### 1.2 — Playwright Config

Spec files live in `Tests/e2e/`. Each feature gets its own spec file and a named project in `playwright.config.js`.

```javascript
// playwright.config.js — add a new project per feature
{
  name: "my-feature-name",
  testMatch: "**/my-feature-name.spec.js",
  use: { ...devices["Desktop Chrome"] }
}
```

### 1.3 — Run Tests

```bash
# Run a specific project
npx playwright test --project=my-feature-name

# Run with UI reporter
npx playwright test --project=my-feature-name --reporter=list

# Run headed (visible browser) — useful for debugging
npx playwright test --project=my-feature-name --headed

# Run a single test by title
npx playwright test --project=my-feature-name -g "T_CBL03"

# Take a screenshot of the current page state
npx playwright screenshot --browser chromium "$FULL_URL" Tests/screenshots/debug.png
```

---

## Phase 2 — Writing Specs

### 2.1 — Spec File Structure

```javascript
// Tests/e2e/my-feature.spec.js
const { test, expect } = require("@playwright/test");

// ── Helpers ────────────────────────────────────────────────────────────────

const SF_URL = process.env.SF_FRONTDOOR_URL; // set in shell before running

function targetUrl(retUrl) {
  return `${SF_URL}&retURL=${encodeURIComponent(retUrl)}`;
}

// ── Tests ──────────────────────────────────────────────────────────────────

test.describe("Feature Name", () => {

  test("T_F01 — happy path description", async ({ page }) => {
    await page.goto(targetUrl("/lightning/n/My_Page"));
    await page.waitForLoadState("networkidle");

    // Use getByTitle / getByRole / getByLabel — these pierce LWC shadow roots
    const btn = page.getByTitle("My Button Title").first();
    await btn.waitFor({ state: "visible" });

    // IMPORTANT: use dispatchEvent for LWC buttons, not click()
    await btn.dispatchEvent("click");

    // Verify result
    await page.getByTitle("Expected State").waitFor({ state: "visible" });
  });

});
```

### 2.2 — Environment Variable Pattern

Pass the frontdoor URL via environment variable so it's never hardcoded:

```bash
# In shell before running tests:
export SF_FRONTDOOR_URL=$(sf org open --target-org dmedev5 --url-only 2>&1 | grep "^https")
npx playwright test --project=my-feature
```

```javascript
// In spec file:
const SF_URL = process.env.SF_FRONTDOOR_URL;
if (!SF_URL) throw new Error("SF_FRONTDOOR_URL not set — run: export SF_FRONTDOOR_URL=$(sf org open --url-only ...)");
```

---

## Phase 3 — LWC Shadow DOM Rules

**Salesforce LWC uses closed shadow roots.** This affects how Playwright interacts with components.

### Finding Elements (works fine)

`getByTitle()`, `getByRole()`, `getByLabel()`, `locator('[data-*]')` — all pierce closed shadow roots for element discovery via accessibility APIs.

```javascript
// These work for locating elements
const btn = page.getByTitle("Expand grantee list").first();
const input = page.getByLabel("Grant Number");
const row = page.locator('[data-schedule-key="SUB-123"]');
```

### Clicking Elements (CRITICAL)

`locator.click()` dispatches via mouse coordinates — **does NOT reach LWC handlers in closed shadow roots**.

`locator.dispatchEvent("click")` fires directly on the DOM node — **works**.

```javascript
// WRONG — click doesn't reach handler in closed shadow root
await btn.click();
await btn.click({ force: true });

// CORRECT — dispatchEvent reaches the LWC onclick handler
await btn.dispatchEvent("click");
```

### Typing / Filling

```javascript
// Standard fill works for LWC inputs
await page.getByLabel("Grant Number").fill("H80CS12345");

// Or via dispatchEvent if fill doesn't trigger LWC change handler
await input.dispatchEvent("input");
```

### Post-Interaction Assertions

After clicking, the element you located may stale (e.g., title changed). Assert on the **resulting state**, not the original element:

```javascript
// WRONG — expandBtn's title changes after expand, so this locator now points to a different element
await expect(expandBtn).toHaveAttribute("aria-expanded", "true");

// CORRECT — assert on the new state
await page.getByTitle("Collapse grantee list").first().waitFor({ state: "visible" });
```

---

## Phase 4 — Test ID Convention

Use consistent IDs across spec, feature doc, handoff doc, and ADO work items:

```
T_{PREFIX}{NN} — {description}

Prefix conventions:
  CBL = Construction Batch List
  MI  = Modification Initiation (PWPM)
  PSP = Progress Status Panel
  SC  = Submission Creation
  WZ  = Wizard
  NR  = Narrative
```

Example:
```javascript
test("T_CBL01 — batch list renders with at least one row", async ({ page }) => { ... });
test("T_CBL02 — bulk batch row has expand toggle", async ({ page }) => { ... });
```

---

## Phase 5 — Screenshots

Take screenshots at key moments for visual verification and handoff docs:

```javascript
// Named screenshots go in Tests/screenshots/
await page.screenshot({
  path: `Tests/screenshots/my-feature-T_F01-00-initial.png`,
  fullPage: false
});

// After an action
await btn.dispatchEvent("click");
await page.waitForLoadState("networkidle");
await page.screenshot({
  path: `Tests/screenshots/my-feature-T_F01-01-after-click.png`
});
```

Naming convention: `{feature-prefix}-{test-id}-{NN}-{description}.png`

---

## Phase 6 — Soft Skips

When a test depends on data that may not exist in the org, use a conditional skip:

```javascript
test("T_CBL06 — pagination shows for batch with >10 CIs", async ({ page }) => {
  await page.goto(targetUrl("/lightning/n/Reviews_and_Monitoring"));
  await page.waitForLoadState("networkidle");

  const largeBatch = page.locator(".batch-row-large");
  const count = await largeBatch.count();

  if (count === 0) {
    test.skip(true, "No large batch available in org — create a bulk batch with >10 CIs to validate");
    return;
  }

  // ... rest of test
});
```

---

## Phase 7 — Spec → Feature Doc Integration

After writing and running specs, update the feature doc's **Test Coverage** and **Test Scenarios** sections (see `skill_dev_complete.md` §2.3 and §2.4):

```markdown
### E2E Tests (Playwright)

| Spec File | Project Name | Tests |
|-----------|-------------|-------|
| `Tests/e2e/my-feature.spec.js` | `my-feature` | T_F01–T_F07 |

**Run:**
```bash
export SF_FRONTDOOR_URL=$(sf org open --target-org dmedev5 --url-only 2>&1 | grep "^https")
npx playwright test --project=my-feature
```
```

---

## Common Commands Cheatsheet

```bash
# Authenticated URL
export SF_FRONTDOOR_URL=$(sf org open --target-org dmedev5 --url-only 2>&1 | grep "^https")

# Run specific project
npx playwright test --project=my-feature --reporter=list

# Run headed for debugging
npx playwright test --project=my-feature --headed --timeout=60000

# Run single test
npx playwright test --project=my-feature -g "T_F01"

# Screenshot a page
npx playwright screenshot --browser chromium "$SF_FRONTDOOR_URL&retURL=%2Flightning%2Fn%2FMy_Page" Tests/screenshots/debug.png

# Show test results
npx playwright show-report
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|---|---|---|
| `btn.click()` on LWC buttons | Coordinates don't reach closed shadow handler | `btn.dispatchEvent("click")` |
| `btn.click({ force: true })` | Same problem | `btn.dispatchEvent("click")` |
| Hardcoded Salesforce URLs | Sessions expire, org URLs change | `sf org open --url-only` pattern |
| `page.locator('.slds-button').click()` | CSS class-based, brittle | `page.getByTitle()` or `getByRole()` |
| Assert `aria-expanded` after expand | Locator stales when title changes | Assert on resulting state instead |
| `page.waitForTimeout(2000)` | Flaky timing | `waitFor({ state: 'visible' })` or `networkidle` |
