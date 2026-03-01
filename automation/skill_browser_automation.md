# Browser Automation - Master Guide

**Last Updated:** January 26, 2026  
**Purpose:** Comprehensive guide for web automation using Playwright and MCP servers  
**Success Rate:** 100% (5/5 ADO stories created successfully)

---

## Table of Contents

1. [Overview](#overview)
2. [Playwright Fundamentals](#playwright-fundamentals)
3. [MCP Server Integration](#mcp-server-integration)
4. [Element Selection Strategies](#element-selection-strategies)
5. [Handling Dynamic Content](#handling-dynamic-content)
6. [Form Filling and Interaction](#form-filling-and-interaction)
7. [Save Patterns](#save-patterns)
8. [Dialog Handling](#dialog-handling)
9. [Error Handling and Retries](#error-handling-and-retries)
10. [Azure DevOps Automation](#azure-devops-automation)
11. [Best Practices](#best-practices)
12. [Troubleshooting](#troubleshooting)

---

## Overview

Browser automation enables programmatic control of web browsers for testing, data extraction, and workflow automation. This guide focuses on Playwright with MCP (Model Context Protocol) server integration.

### Prerequisites

- Playwright MCP server configured
- Browser installed (Chromium, Firefox, or WebKit)
- Understanding of HTML/CSS selectors
- Basic JavaScript knowledge

### Key Concepts

- **Locators:** Selectors to find elements on the page
- **Actions:** Click, type, fill, select, etc.
- **Waits:** Explicit waits for elements or conditions
- **Assertions:** Verify page state
- **MCP Tools:** Pre-built browser automation functions

---

## Playwright Fundamentals

### Browser Lifecycle

```javascript
// Launch browser
const browser = await playwright.chromium.launch({
    headless: false,  // Show browser window
    slowMo: 100       // Slow down by 100ms
});

// Create context (isolated session)
const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    userAgent: 'Custom User Agent'
});

// Create page
const page = await context.newPage();

// Navigate
await page.goto('https://example.com');

// Close
await page.close();
await context.close();
await browser.close();
```

### Basic Navigation

```javascript
// Navigate to URL
await page.goto('https://example.com');

// Navigate with options
await page.goto('https://example.com', {
    waitUntil: 'networkidle',  // Wait for network to be idle
    timeout: 30000              // 30 second timeout
});

// Go back
await page.goBack();

// Go forward
await page.goForward();

// Reload
await page.reload();

// Get current URL
const url = page.url();
```

---

## MCP Server Integration

### Available MCP Tools

The Playwright MCP server provides pre-built tools for common automation tasks:

#### Navigation
- `mcp1_browser_navigate` - Navigate to URL
- `mcp1_browser_navigate_back` - Go back
- `mcp1_browser_close` - Close browser

#### Interaction
- `mcp1_browser_click` - Click element
- `mcp1_browser_type` - Type text
- `mcp1_browser_fill_form` - Fill multiple form fields
- `mcp1_browser_hover` - Hover over element
- `mcp1_browser_drag` - Drag and drop

#### Selection
- `mcp1_browser_select_option` - Select dropdown option

#### Information
- `mcp1_browser_snapshot` - Get page accessibility snapshot
- `mcp1_browser_take_screenshot` - Capture screenshot
- `mcp1_browser_console_messages` - Get console logs
- `mcp1_browser_network_requests` - Get network activity

#### Advanced
- `mcp1_browser_evaluate` - Execute JavaScript
- `mcp1_browser_press_key` - Press keyboard key
- `mcp1_browser_handle_dialog` - Handle alerts/confirms
- `mcp1_browser_file_upload` - Upload files

### Using MCP Tools

```javascript
// Navigate to page
mcp1_browser_navigate({
    url: "https://dev.azure.com/organization/project"
});

// Take snapshot to see page structure
mcp1_browser_snapshot();

// Click element
mcp1_browser_click({
    element: "New Work Item button",
    ref: "button[aria-label='New Work Item']"
});

// Fill form
mcp1_browser_fill_form({
    fields: [
        {
            name: "Title",
            type: "textbox",
            ref: "input[aria-label='Title']",
            value: "My User Story"
        },
        {
            name: "Description",
            type: "textbox",
            ref: "textarea[aria-label='Description']",
            value: "Story description"
        }
    ]
});

// Press keyboard shortcut
mcp1_browser_press_key({
    key: "Control+s"
});
```

---

## Element Selection Strategies

### Selector Priority

**Best to Worst:**

1. **Data attributes** - `[data-testid="submit-btn"]`
2. **ARIA labels** - `[aria-label="Submit"]`
3. **ID** - `#submit-button`
4. **Name** - `[name="submit"]`
5. **Class** - `.submit-btn` (avoid if possible)
6. **Text content** - `text=Submit`
7. **XPath** - `//button[text()="Submit"]` (last resort)

### Selector Examples

```javascript
// By data attribute (BEST)
await page.click('[data-testid="submit-button"]');

// By ARIA label (GOOD)
await page.click('[aria-label="Submit form"]');

// By ID (GOOD)
await page.click('#submit-btn');

// By role and name (GOOD)
await page.click('button[name="submit"]');

// By text content (OK)
await page.click('text=Submit');

// By class (AVOID - fragile)
await page.click('.btn.btn-primary.submit');

// By XPath (LAST RESORT)
await page.click('//button[@class="submit-btn"]');
```

### Combining Selectors

```javascript
// Multiple conditions
await page.click('button[aria-label="Submit"][type="submit"]');

// Descendant selector
await page.click('.form-container button[type="submit"]');

// Direct child
await page.click('.form > button');

// Nth element
await page.click('button:nth-child(2)');

// Contains text
await page.click('button:has-text("Submit")');
```

### Dynamic Selectors

```javascript
// Using variables
const buttonLabel = "Submit";
await page.click(`button[aria-label="${buttonLabel}"]`);

// Finding by partial text
await page.click(`button:has-text("${partialText}")`);

// Finding by data attribute value
const itemId = "12345";
await page.click(`[data-item-id="${itemId}"]`);
```

---

## Handling Dynamic Content

### Wait Strategies

```javascript
// Wait for element to be visible
await page.waitForSelector('button[aria-label="Submit"]', {
    state: 'visible',
    timeout: 5000
});

// Wait for element to be hidden
await page.waitForSelector('.loading-spinner', {
    state: 'hidden'
});

// Wait for element to be attached to DOM
await page.waitForSelector('.dynamic-content', {
    state: 'attached'
});

// Wait for network to be idle
await page.waitForLoadState('networkidle');

// Wait for specific timeout
await page.waitForTimeout(2000);  // 2 seconds

// Wait for function to return true
await page.waitForFunction(() => {
    return document.querySelector('.data-loaded') !== null;
});
```

### Polling for Elements

```javascript
// Wait for element with retry
async function waitForElement(page, selector, timeout = 10000) {
    const startTime = Date.now();
    
    while (Date.now() - startTime < timeout) {
        const element = await page.$(selector);
        if (element) {
            return element;
        }
        await page.waitForTimeout(500);  // Check every 500ms
    }
    
    throw new Error(`Element ${selector} not found after ${timeout}ms`);
}

// Usage
const button = await waitForElement(page, 'button[aria-label="Submit"]');
await button.click();
```

### Handling AJAX/Fetch Requests

```javascript
// Wait for specific network request
await page.waitForResponse(response => 
    response.url().includes('/api/data') && response.status() === 200
);

// Wait for all network requests to complete
await page.waitForLoadState('networkidle');

// Intercept and modify requests
await page.route('**/api/data', route => {
    route.fulfill({
        status: 200,
        body: JSON.stringify({ data: 'mocked' })
    });
});
```

---

## Form Filling and Interaction

### Text Input

```javascript
// Type text (simulates keystrokes)
await page.type('input[name="username"]', 'john.doe');

// Fill text (faster, sets value directly)
await page.fill('input[name="username"]', 'john.doe');

// Clear and fill
await page.fill('input[name="username"]', '');
await page.fill('input[name="username"]', 'new.value');

// Type with delay between keystrokes
await page.type('input[name="search"]', 'query', { delay: 100 });
```

### Dropdowns and Select Elements

```javascript
// Select by value
await page.selectOption('select[name="country"]', 'US');

// Select by label
await page.selectOption('select[name="country"]', { label: 'United States' });

// Select by index
await page.selectOption('select[name="country"]', { index: 2 });

// Select multiple options
await page.selectOption('select[name="tags"]', ['tag1', 'tag2', 'tag3']);
```

### Custom Dropdowns (Non-Select)

```javascript
// Click to open dropdown
await page.click('[data-testid="dropdown-trigger"]');

// Wait for dropdown to appear
await page.waitForSelector('.dropdown-menu', { state: 'visible' });

// Click option
await page.click('.dropdown-menu li:has-text("Option 1")');

// Or use keyboard navigation
await page.click('[data-testid="dropdown-trigger"]');
await page.keyboard.press('ArrowDown');
await page.keyboard.press('ArrowDown');
await page.keyboard.press('Enter');
```

### Checkboxes and Radio Buttons

```javascript
// Check checkbox
await page.check('input[type="checkbox"][name="agree"]');

// Uncheck checkbox
await page.uncheck('input[type="checkbox"][name="agree"]');

// Select radio button
await page.check('input[type="radio"][value="option1"]');

// Verify checked state
const isChecked = await page.isChecked('input[type="checkbox"][name="agree"]');
```

### File Uploads

```javascript
// Upload single file
await page.setInputFiles('input[type="file"]', 'path/to/file.pdf');

// Upload multiple files
await page.setInputFiles('input[type="file"]', [
    'path/to/file1.pdf',
    'path/to/file2.pdf'
]);

// Clear file input
await page.setInputFiles('input[type="file"]', []);

// Using MCP tool
mcp1_browser_file_upload({
    paths: ['C:\\Users\\user\\Documents\\file.pdf']
});
```

---

## Save Patterns

### CRITICAL: Control+S vs Button Click

**ALWAYS use `Control+s` keyboard shortcut for saving in Azure DevOps and similar applications.**

```javascript
// ✅ CORRECT - Use keyboard shortcut
await page.keyboard.press('Control+s');

// Wait for save to complete
await page.waitForTimeout(2000);

// Verify save (asterisk removed from title)
const title = await page.title();
const isSaved = !title.includes('*');

// ❌ WRONG - Don't click Save button
// await page.click('button[aria-label="Save"]');
// Reason: Button can be blocked by tooltips or other overlays
```

### Save Verification

```javascript
// Method 1: Check title for asterisk
async function verifySaved(page) {
    const title = await page.title();
    return !title.includes('*');
}

// Method 2: Wait for save indicator
await page.waitForSelector('.save-indicator:has-text("Saved")', {
    state: 'visible',
    timeout: 5000
});

// Method 3: Check for disabled save button
await page.waitForSelector('button[aria-label="Save"][disabled]');
```

### Complete Save Pattern

```javascript
async function saveAndVerify(page) {
    console.log('Saving...');
    
    // Press Control+s
    await page.keyboard.press('Control+s');
    
    // Wait for save operation
    await page.waitForTimeout(2000);
    
    // Verify save completed
    const title = await page.title();
    const isSaved = !title.includes('*');
    
    if (!isSaved) {
        throw new Error('Save verification failed - asterisk still in title');
    }
    
    console.log('✓ Save verified');
    return true;
}
```

---

## Dialog Handling

### Alert, Confirm, Prompt

```javascript
// Listen for dialog
page.on('dialog', async dialog => {
    console.log(`Dialog type: ${dialog.type()}`);
    console.log(`Dialog message: ${dialog.message()}`);
    
    // Accept dialog
    await dialog.accept();
    
    // Or dismiss dialog
    // await dialog.dismiss();
    
    // For prompt, provide input
    // await dialog.accept('input text');
});

// Trigger action that shows dialog
await page.click('button[aria-label="Delete"]');
```

### beforeunload Dialog

**CRITICAL for Azure DevOps:** When navigating away from unsaved work, handle the beforeunload dialog.

```javascript
// Method 1: Accept dialog (leave page)
page.on('dialog', async dialog => {
    if (dialog.type() === 'beforeunload') {
        await dialog.accept();  // Leave page
    }
});

// Method 2: Dismiss dialog (stay on page)
page.on('dialog', async dialog => {
    if (dialog.type() === 'beforeunload') {
        await dialog.dismiss();  // Stay on page
    }
});

// Using MCP tool
mcp1_browser_handle_dialog({
    accept: true  // true to leave, false to stay
});
```

### Custom Modals

```javascript
// Wait for modal to appear
await page.waitForSelector('.modal', { state: 'visible' });

// Click button in modal
await page.click('.modal button[aria-label="Confirm"]');

// Wait for modal to disappear
await page.waitForSelector('.modal', { state: 'hidden' });
```

---

## Error Handling and Retries

### Try-Catch Pattern

```javascript
try {
    await page.click('button[aria-label="Submit"]');
    console.log('✓ Click successful');
} catch (error) {
    console.error('✗ Click failed:', error.message);
    
    // Take screenshot for debugging
    await page.screenshot({ path: 'error.png' });
    
    // Get page HTML for inspection
    const html = await page.content();
    console.log('Page HTML:', html);
    
    throw error;
}
```

### Retry Logic

```javascript
async function clickWithRetry(page, selector, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            await page.click(selector, { timeout: 5000 });
            console.log(`✓ Click successful on attempt ${i + 1}`);
            return true;
        } catch (error) {
            console.log(`✗ Attempt ${i + 1} failed: ${error.message}`);
            
            if (i === maxRetries - 1) {
                throw new Error(`Failed after ${maxRetries} attempts`);
            }
            
            // Wait before retry
            await page.waitForTimeout(1000);
        }
    }
}

// Usage
await clickWithRetry(page, 'button[aria-label="Submit"]');
```

### Graceful Degradation

```javascript
// Try primary selector, fall back to alternatives
async function clickFlexible(page, selectors) {
    for (const selector of selectors) {
        try {
            await page.click(selector, { timeout: 2000 });
            console.log(`✓ Clicked using selector: ${selector}`);
            return true;
        } catch (error) {
            console.log(`✗ Selector failed: ${selector}`);
        }
    }
    
    throw new Error('All selectors failed');
}

// Usage
await clickFlexible(page, [
    'button[data-testid="submit"]',
    'button[aria-label="Submit"]',
    'button:has-text("Submit")'
]);
```

---

## Azure DevOps Automation

### Critical ADO Workflow

**MUST follow this exact sequence for editing work items:**

1. Navigate to work item URL
2. Wait for page load (networkidle + 1000ms)
3. Click field to edit
4. Type/fill new value
5. **SAVE with Control+s** (NOT Save button)
6. Wait for save to complete (1500-2000ms)
7. Verify save (check asterisk removed from title)
8. THEN navigate to next item

### Creating User Story

```javascript
// Navigate to ADO
await page.goto('https://dev.azure.com/org/project/_workitems');
await page.waitForLoadState('networkidle');
await page.waitForTimeout(1000);

// Click New Work Item
await page.click('button[aria-label="New Work Item"]');
await page.waitForTimeout(500);

// Select User Story
await page.click('li:has-text("User Story")');
await page.waitForLoadState('networkidle');
await page.waitForTimeout(1000);

// Fill Title
await page.click('input[aria-label="Title"]');
await page.fill('input[aria-label="Title"]', 'My User Story Title');

// Fill Description
await page.click('textarea[aria-label="Description"]');
await page.fill('textarea[aria-label="Description"]', 'Story description here');

// Fill Acceptance Criteria
await page.click('textarea[aria-label="Acceptance Criteria"]');
await page.fill('textarea[aria-label="Acceptance Criteria"]', 'AC1: ...\nAC2: ...');

// SAVE with Control+s
await page.keyboard.press('Control+s');
await page.waitForTimeout(2000);

// Verify save
const title = await page.title();
if (title.includes('*')) {
    throw new Error('Save failed - asterisk still in title');
}

console.log('✓ User Story created and saved');
```

### Adding Parent Link

```javascript
// Click "Add an existing work item" button
await page.click('button[aria-label="Add link"]');
await page.waitForTimeout(500);

// Click "Parent" option
await page.click('li:has-text("Parent")');
await page.waitForTimeout(500);

// Click picker combobox
await page.click('[role="combobox"][aria-label="Work item picker"]');
await page.waitForTimeout(500);

// Type Feature ID
await page.fill('[role="combobox"]', '421006');
await page.waitForTimeout(1500);  // Wait for dropdown

// Press ArrowDown to select first result
await page.keyboard.press('ArrowDown');
await page.keyboard.press('Enter');
await page.waitForTimeout(1000);

// Click OK button in dialog
await page.click('button:has-text("OK")');
await page.waitForTimeout(2000);

// SAVE with Control+s
await page.keyboard.press('Control+s');
await page.waitForTimeout(2000);

// Verify parent link appears
const parentLink = await page.$('a:has-text("#421006")');
if (!parentLink) {
    throw new Error('Parent link not found after save');
}

console.log('✓ Parent link added and verified');
```

### Setting Dropdown Fields

```javascript
// Click dropdown field
await page.click('[aria-label="Vendor Type"]');
await page.waitForTimeout(500);

// Use keyboard navigation (RECOMMENDED)
await page.keyboard.press('ArrowDown');  // Move to first option
await page.keyboard.press('ArrowDown');  // Move to second option
await page.keyboard.press('Enter');      // Select

// Or click option directly
// await page.click('li:has-text("DME")');

await page.waitForTimeout(500);

// SAVE
await page.keyboard.press('Control+s');
await page.waitForTimeout(2000);
```

---

## Best Practices

### 1. Always Wait for Elements

```javascript
// ❌ WRONG - No wait
await page.click('button');

// ✅ CORRECT - Wait for element
await page.waitForSelector('button[aria-label="Submit"]', { state: 'visible' });
await page.click('button[aria-label="Submit"]');
```

### 2. Use Explicit Waits

```javascript
// ❌ WRONG - Arbitrary timeout
await page.waitForTimeout(5000);

// ✅ CORRECT - Wait for specific condition
await page.waitForSelector('.data-loaded', { state: 'visible' });
await page.waitForLoadState('networkidle');
```

### 3. Verify Actions

```javascript
// Click button
await page.click('button[aria-label="Submit"]');

// Verify result
await page.waitForSelector('.success-message', { state: 'visible' });
const message = await page.textContent('.success-message');
console.log('Success:', message);
```

### 4. Take Screenshots on Errors

```javascript
try {
    await page.click('button[aria-label="Submit"]');
} catch (error) {
    await page.screenshot({ 
        path: `error-${Date.now()}.png`,
        fullPage: true 
    });
    throw error;
}
```

### 5. Use Page Snapshots for Debugging

```javascript
// Get accessibility snapshot
const snapshot = await page.accessibility.snapshot();
console.log(JSON.stringify(snapshot, null, 2));

// Or use MCP tool
mcp1_browser_snapshot();
```

### 6. Clean Up Resources

```javascript
try {
    // Automation logic
    await page.goto('https://example.com');
    // ... more actions ...
} finally {
    // Always close browser
    await page.close();
    await context.close();
    await browser.close();
}
```

---

## Troubleshooting

### Issue 1: Element Not Found

**Problem:** `Error: Element not found`

**Solutions:**
```javascript
// 1. Wait for element
await page.waitForSelector(selector, { state: 'visible', timeout: 10000 });

// 2. Check if element exists
const element = await page.$(selector);
if (!element) {
    console.log('Element not found, taking snapshot...');
    await page.screenshot({ path: 'debug.png' });
}

// 3. Try alternative selectors
const selectors = [
    'button[data-testid="submit"]',
    'button[aria-label="Submit"]',
    'button:has-text("Submit")'
];
for (const sel of selectors) {
    const elem = await page.$(sel);
    if (elem) {
        await elem.click();
        break;
    }
}
```

### Issue 2: Element Not Clickable

**Problem:** `Element is not clickable at point (x, y)`

**Solutions:**
```javascript
// 1. Scroll element into view
await page.locator(selector).scrollIntoViewIfNeeded();
await page.click(selector);

// 2. Wait for element to be stable
await page.waitForSelector(selector, { state: 'visible' });
await page.waitForTimeout(500);  // Let animations finish
await page.click(selector);

// 3. Use force click (bypass actionability checks)
await page.click(selector, { force: true });

// 4. Click using JavaScript
await page.evaluate(selector => {
    document.querySelector(selector).click();
}, selector);
```

### Issue 3: Timeout Errors

**Problem:** `Timeout exceeded while waiting for selector`

**Solutions:**
```javascript
// 1. Increase timeout
await page.waitForSelector(selector, { timeout: 30000 });

// 2. Check if page loaded
await page.waitForLoadState('networkidle');

// 3. Verify selector is correct
const snapshot = await page.content();
console.log('Page HTML:', snapshot);

// 4. Use polling
async function waitForElement(selector, maxWait = 30000) {
    const start = Date.now();
    while (Date.now() - start < maxWait) {
        const elem = await page.$(selector);
        if (elem) return elem;
        await page.waitForTimeout(500);
    }
    throw new Error(`Element ${selector} not found after ${maxWait}ms`);
}
```

### Issue 4: Save Not Working

**Problem:** Changes not saved in Azure DevOps

**Solutions:**
```javascript
// 1. ALWAYS use Control+s, not Save button
await page.keyboard.press('Control+s');

// 2. Wait longer for save
await page.waitForTimeout(2000);

// 3. Verify save completed
const title = await page.title();
if (title.includes('*')) {
    console.log('Save not complete, waiting longer...');
    await page.waitForTimeout(2000);
}

// 4. Check for error messages
const errorMsg = await page.$('.error-message');
if (errorMsg) {
    const text = await errorMsg.textContent();
    console.error('Save error:', text);
}
```

### Issue 5: Dialog Not Handled

**Problem:** `beforeunload` dialog blocks navigation

**Solutions:**
```javascript
// Set up dialog handler BEFORE action
page.on('dialog', async dialog => {
    console.log('Dialog detected:', dialog.type());
    await dialog.accept();  // or dialog.dismiss()
});

// Then perform action
await page.goto('https://next-page.com');

// Or use MCP tool
mcp1_browser_handle_dialog({ accept: true });
```

---

## Quick Reference

### Most Common Patterns

```javascript
// Navigate and wait
await page.goto(url);
await page.waitForLoadState('networkidle');
await page.waitForTimeout(1000);

// Click element
await page.waitForSelector(selector, { state: 'visible' });
await page.click(selector);

// Fill form field
await page.click('input[aria-label="Title"]');
await page.fill('input[aria-label="Title"]', 'value');

// Save (ADO pattern)
await page.keyboard.press('Control+s');
await page.waitForTimeout(2000);

// Verify save
const title = await page.title();
const saved = !title.includes('*');

// Handle dialog
page.on('dialog', async dialog => await dialog.accept());

// Take screenshot
await page.screenshot({ path: 'screenshot.png' });

// Get page snapshot
mcp1_browser_snapshot();
```

---

## Related Documentation

- **ADO Automation:** `MASTER_GUIDE_AZURE_DEVOPS_AUTOMATION.md`
- **PowerShell Automation:** `MASTER_GUIDE_POWERSHELL_AUTOMATION.md`
- **Playwright Documentation:** https://playwright.dev/
- **MCP Server Documentation:** https://modelcontextprotocol.io/

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-26 | Initial creation with ADO automation patterns |
