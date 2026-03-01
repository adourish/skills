# Azure DevOps Story Creation - Master Automation Guide

## Overview

**Purpose**: Complete guide for automating Azure DevOps User Story creation using Playwright browser automation via MCP (Model Context Protocol).

**Last Updated**: January 27, 2026

**Success Rate**: 100% (7/7 work items created successfully)
- 5 User Stories (Classic PRM)
- 1 Feature (ESV Platform)
- 1 User Story (Salesforce Capabilities)

**Critical Update (Jan 27, 2026)**: Vendor Type MUST be set immediately after Title/Description/Acceptance Criteria and BEFORE attempting to save or add parent links. The page will show "Field 'Vendor Type' cannot be empty" error and prevent saving until this is set.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Critical Process Overview](#critical-process-overview)
3. [Field-by-Field Automation](#field-by-field-automation)
4. [Parent Link Automation](#parent-link-automation)
5. [Feature Creation via Dialog](#feature-creation-via-dialog)
6. [Assignment Automation](#assignment-automation)
7. [Common Issues and Solutions](#common-issues-and-solutions)
8. [Verification Steps](#verification-steps)
9. [Complete Example](#complete-example)
10. [Rollback and Recovery](#rollback-and-recovery)

---

## Prerequisites

### Required Access
- Azure DevOps authenticated session in browser
- Correct ADO organization URL: `https://ehbads.hrsa.gov/ads/EHBs/EHBs/`
- Permissions to create User Stories in target project

### Required Information
- Epic ID (e.g., #414151, #415047)
- Parent Feature IDs (e.g., #421006, #421007, #421010)
- Story/Feature details: Title, Description, Acceptance Criteria (Stories only)
- Vendor Type: DME (required field for both Stories and Features)
- Target Date: Required for Features (e.g., 3/31/2026)
- Area Path: EHBs\BHCMISPRS
- Iteration: EHBs\DME BHCMIS Purple

### Tools
- Playwright MCP server (mcp-playwright)
- Browser automation capabilities via Cascade

---

## Critical Process Overview

### The Golden Rule
**ALWAYS save with `Control+s` keyboard shortcut, NEVER click the Save button.**

The Save button can be blocked by tooltips and cause automation failures.

### Story Creation Sequence

```
1. Navigate to new story URL
2. Wait for page load (2 seconds minimum)
3. Fill Title field
4. Fill Description field
5. Fill Acceptance Criteria field
6. Set Vendor Type = DME (CRITICAL: Must be done before step 7)
7. Add Parent Link to Feature
8. Save with Control+s
9. Wait for save completion (3 seconds)
10. Verify story was created (check for story ID)
```

**CRITICAL**: Step 6 (Vendor Type) MUST be completed before attempting to add parent links or save. The page will display "Field 'Vendor Type' cannot be empty" error and block all save operations until this required field is set.

### Timing Guidelines

| Action | Wait Time | Reason |
|--------|-----------|--------|
| After navigation | 2000ms | Page load and form initialization |
| After field fill | 500ms | UI update and validation |
| After Vendor Type | 500ms | Dropdown selection processing |
| After parent link dialog open | 1500ms | Dialog initialization |
| After typing Feature ID | 2500ms | Dropdown population |
| After keyboard selection | 1500ms | Selection processing |
| After OK button | 2000ms | Dialog close and link creation |
| After Control+s save | 3000ms | Save processing and redirect |

---

## Feature Creation via Dialog

### Overview
Features are best created using the "Add link" > "New item" dialog from the parent Epic page. This approach automatically establishes the parent-child relationship and provides a streamlined workflow.

### Critical Requirements for Features
1. **Target Date** - REQUIRED field (will show error if empty)
2. **Vendor Type** - REQUIRED field (must be set to "DME")
3. **Description** - Recommended for context
4. **Work Item Type** - Must change from default "User Story" to "Feature"

### Step-by-Step Process

```javascript
// 1. Navigate to parent Epic
await page.goto('https://ehbads.hrsa.gov/ads/EHBs/EHBs/_workitems/edit/415047');
await page.waitForTimeout(2000);

// 2. Click Add link in Related Work section
await page.locator('button:has-text("Add link")').first().click();
await page.waitForTimeout(500);

// 3. Click New item
await page.getByRole('menuitem', { name: 'New item' }).click();
await page.waitForTimeout(1500);

// 4. Change work item type to Feature
await page.locator('#work-item-types_txt').click();
await page.waitForTimeout(300);
await page.locator('#work-item-types_txt').fill('Feature');
await page.waitForTimeout(500);
await page.keyboard.press('Enter');
await page.waitForTimeout(500);

// 5. Fill Title
await page.getByRole('textbox', { name: 'Title', exact: true }).click();
await page.getByRole('textbox', { name: 'Title', exact: true }).fill('ESV Platform Approach - Analysis of Alternatives');
await page.waitForTimeout(500);

// 6. Set Target Date (REQUIRED)
await page.getByRole('dialog').getByLabel('Target Date').click();
await page.getByRole('dialog').getByLabel('Target Date').fill('3/31/2026');
await page.waitForTimeout(500);

// 7. Set Vendor Type to DME (REQUIRED)
const vendorTypeCombobox = await page.getByRole('dialog').getByRole('combobox', { name: 'Vendor Type' });
await vendorTypeCombobox.click();
await page.waitForTimeout(300);
await vendorTypeCombobox.fill('DME');
await page.waitForTimeout(300);
await page.keyboard.press('Enter');
await page.waitForTimeout(500);

// 8. Fill Description (in dialog)
await page.getByRole('dialog').getByLabel('Description').click();
await page.getByRole('dialog').getByLabel('Description').fill('Your description here');
await page.waitForTimeout(500);

// 9. Click OK to create
await page.getByRole('button', { name: 'OK' }).click();
await page.waitForTimeout(2000);

// 10. Save with Control+s
await page.keyboard.press('Control+s');
await page.waitForTimeout(3000);
```

### Key Differences from User Story Creation
- **Dialog-based**: Feature created in dialog, not separate page
- **Target Date**: Required field (Stories don't have this)
- **No Acceptance Criteria**: Features don't have this field
- **Parent Link**: Automatically created by using "New item" from parent
- **Scoped Locators**: Use `getByRole('dialog')` to target fields in dialog

### Common Dialog Issues

**Issue**: "Field 'Target Date' cannot be empty" alert
- **Solution**: Always set Target Date before clicking OK

**Issue**: "Field 'Vendor Type' cannot be empty" alert  
- **Solution**: Set Vendor Type to DME before clicking OK

**Issue**: Dialog closes unexpectedly (Escape key)
- **Solution**: Feature may still be created but unsaved. Navigate to it and complete setup.

**Issue**: Can't click fields in dialog
- **Solution**: Use scoped locators: `page.getByRole('dialog').getByLabel('FieldName')`

---

## Assignment Automation

### Overview
Assigning work items to users can be automated quickly using the Assigned To field dropdown.

### Fast Assignment Process

```javascript
// 1. Click Assigned To button
await page.getByRole('button', { name: 'Selected identity' }).click();
await page.waitForTimeout(300);

// 2. Click the desired user (first option is often current user)
await page.getByRole('option', { name: ' Dourish, Anthony (HRSA) C' }).click();
await page.waitForTimeout(500);

// 3. Save
await page.keyboard.press('Control+s');
await page.waitForTimeout(2000);
```

### Assignment Best Practices
- **Current User**: Often pre-selected or first in dropdown
- **Search**: Type name in dropdown to filter users
- **Batch Assignment**: Assign multiple items by navigating between them
- **Verify**: Check "Assigned To" field shows correct name before saving

### Assignment Timing
- After clicking Assigned To: 300ms
- After selecting user: 500ms  
- After save: 2000ms

---

## Field-by-Field Automation

### 1. Title Field

**Locator**: `input[aria-label="Title Field"]`

**Method**:
```javascript
const titleField = await page.locator('input[aria-label="Title Field"]').first();
await titleField.click();
await titleField.fill('Your Story Title Here');
await page.waitForTimeout(500);
```

**Best Practices**:
- Always use `.first()` to get the primary title field
- Click before filling to ensure focus
- Keep titles concise but descriptive
- Use proper capitalization

### 2. Description Field

**Locator**: `div[aria-label="Description"]`

**Method**:
```javascript
const descriptionField = await page.locator('div[aria-label="Description"]').first();
await descriptionField.click();
await descriptionField.fill('Your description text here.');
await page.waitForTimeout(500);
```

**Best Practices**:
- This is a rich text div, not an input
- Include context about what the story implements
- Reference Classic PRM features if applicable
- Keep it 1-2 sentences for clarity

### 3. Acceptance Criteria Field

**Locator**: `div[aria-label="Acceptance Criteria"]`

**Method**:
```javascript
const acceptanceCriteriaField = await page.locator('div[aria-label="Acceptance Criteria"]').first();
await acceptanceCriteriaField.click();
const criteria = `- Criterion 1
- Criterion 2
- Criterion 3`;
await acceptanceCriteriaField.fill(criteria);
await page.waitForTimeout(500);
```

**Best Practices**:
- Use bullet points with `-` prefix
- Each criterion should be testable
- Include technical details (component names, methods)
- List 5-8 specific criteria

### 4. Vendor Type Field (REQUIRED)

**Locator**: `combobox[name="Vendor Type"]` or via role

**Method**:
```javascript
const vendorTypeCombobox = await page.getByRole('combobox', { name: 'Vendor Type' });
await vendorTypeCombobox.click();
await page.waitForTimeout(300);
await vendorTypeCombobox.fill('DME');
await page.waitForTimeout(300);
await page.keyboard.press('Enter');
await page.waitForTimeout(500);
```

**Critical Notes**:
- This field MUST be set or save will fail
- Always set to "DME" for this project
- Use keyboard Enter to confirm selection
- Verify field shows "DME" after setting

---

## Parent Link Automation

### Overview
Adding parent links is the most complex part of the automation due to ADO's dynamic dialog system.

### Step-by-Step Process

#### Step 1: Open Parent Link Dialog

**Locator**: `button:has-text("Add an existing work item")`

**Method**:
```javascript
const addWorkItemButton = await page.locator('button:has-text("Add an existing work item")').first();
await addWorkItemButton.click();
await page.waitForTimeout(1500);
```

**What Happens**:
- Dialog opens with "Add link" title
- Link type defaults to "Parent"
- Combobox appears for entering work item ID

#### Step 2: Enter Feature ID

**Locator**: `input[role="combobox"]` (use `.last()` to get the picker)

**Method**:
```javascript
const pickerInput = await page.locator('input[role="combobox"]').last();
await pickerInput.click();
await pickerInput.fill('421006');
await page.waitForTimeout(2500);
```

**What Happens**:
- Typing triggers search
- Dropdown populates with matching features
- Wait 2500ms for dropdown to fully load

#### Step 3: Select Feature from Dropdown

**Method 1: Keyboard Navigation (RECOMMENDED)**
```javascript
await page.keyboard.press('ArrowDown');
await page.waitForTimeout(300);
await page.keyboard.press('Enter');
await page.waitForTimeout(1500);
```

**Method 2: Click Feature Button**
```javascript
const featureButton = await page.locator('button').filter({ hasText: '421006' }).filter({ hasText: 'Configuration - Bundle Configuration' }).first();
await featureButton.click();
await page.waitForTimeout(1500);
```

**Best Practice**: Use keyboard navigation - it's more reliable and faster.

#### Step 4: Click OK Button

**Locator**: `button:has-text("OK")`

**Method**:
```javascript
const okButton = await page.locator('button:has-text("OK")').first();
await okButton.click();
await page.waitForTimeout(2000);
```

**What Happens**:
- Dialog closes
- Parent link is added to Related Work section
- Story is NOT saved yet - must use Control+s

### Parent Feature Reference

| Feature ID | Feature Name | Use For |
|------------|--------------|---------|
| #421006 | Configuration - Bundle Configuration | Bundle, package, export, dashboard stories |
| #421007 | Configuration - Package Management | Task closure, package lifecycle stories |
| #421010 | Configuration - Notifications | Email, notification, alert stories |

---

## Common Issues and Solutions

### Issue 1: "Field 'Vendor Type' cannot be empty"

**Symptom**: Alert appears when trying to save

**Solution**:
```javascript
// Set Vendor Type BEFORE adding parent link
const vendorTypeCombobox = await page.getByRole('combobox', { name: 'Vendor Type' });
await vendorTypeCombobox.click();
await vendorTypeCombobox.fill('DME');
await page.keyboard.press('Enter');
await page.waitForTimeout(500);
```

### Issue 2: OK Button Disabled in Parent Link Dialog

**Symptom**: OK button remains disabled after selecting feature

**Cause**: Feature not properly selected from dropdown

**Solution**:
- Ensure you wait 2500ms after typing Feature ID
- Use keyboard navigation (ArrowDown + Enter) instead of clicking
- Verify feature appears in the dialog before clicking OK

### Issue 3: "beforeunload" Dialog Appears

**Symptom**: Dialog asking "Leave site?" when navigating

**Cause**: Navigating away without saving changes

**Solution**:
```javascript
// Always save before navigating
await page.keyboard.press('Control+s');
await page.waitForTimeout(3000);

// If dialog appears, accept it
await page.getByRole('button', { name: 'Leave' }).click();
```

### Issue 4: Timeout Waiting for Element

**Symptom**: `TimeoutError: locator.click: Timeout 5000ms exceeded`

**Cause**: Element not visible or page not fully loaded

**Solution**:
- Increase wait time after navigation
- Use snapshot to verify page state
- Check if dialog or overlay is blocking element
- Use ref-based clicking from snapshot

### Issue 5: Parent Link Not Appearing

**Symptom**: Story saves but no parent link in Related Work

**Cause**: Didn't save after adding link

**Solution**:
```javascript
// ALWAYS save after adding parent link
const okButton = await page.locator('button:has-text("OK")').first();
await okButton.click();
await page.waitForTimeout(2000);

// CRITICAL: Save with Control+s
await page.keyboard.press('Control+s');
await page.waitForTimeout(3000);
```

---

## Verification Steps

### After Each Story Creation

1. **Check Story ID**: Verify URL changed to `/edit/[StoryID]`
2. **Check Title**: No asterisk (*) in title = saved successfully
3. **Check Vendor Type**: Should show "DME" in Classification section
4. **Check Parent Link**: Links tab should show "(1)" indicating one link
5. **Check Related Work**: Parent feature should appear in Related Work section

### Verification Code

```javascript
// Get current URL to extract story ID
const currentUrl = await page.url();
const storyIdMatch = currentUrl.match(/\/edit\/(\d+)/);
if (storyIdMatch) {
    const storyId = storyIdMatch[1];
    console.log(`Story created: #${storyId}`);
}

// Take snapshot to verify fields
await page.waitForTimeout(2000);
const snapshot = await page.locator('main').textContent();
console.log('Verification:', snapshot.includes('DME') ? 'Vendor Type OK' : 'Vendor Type MISSING');
```

---

## Complete Example

### Full Story Creation Script

```javascript
async (page) => {
    // Navigate to new story page
    await page.goto('https://ehbads.hrsa.gov/ads/EHBs/EHBs/_workitems/create/User%20Story');
    await page.waitForTimeout(2000);
    
    // Fill Title
    const titleField = await page.locator('input[aria-label="Title Field"]').first();
    await titleField.click();
    await titleField.fill('Add Package Metadata Fields to Bundle Configuration');
    await page.waitForTimeout(500);
    
    // Fill Description
    const descriptionField = await page.locator('div[aria-label="Description"]').first();
    await descriptionField.click();
    await descriptionField.fill('Enhance Bundle Definition to include Classic PRM package metadata fields for compatibility and reporting.');
    await page.waitForTimeout(500);
    
    // Fill Acceptance Criteria
    const acceptanceCriteriaField = await page.locator('div[aria-label="Acceptance Criteria"]').first();
    await acceptanceCriteriaField.click();
    const criteria = `- Add fields to cfgHub_BundleDefinition__c: OMB_Number__c, Package_Type__c, Reporting_Year__c
- Update cfgHub_BundleConfigurationForm LWC to display these fields
- Add validation for OMB Number format
- Update bundle creation service to handle new fields
- Test with sample data`;
    await acceptanceCriteriaField.fill(criteria);
    await page.waitForTimeout(500);
    
    // Set Vendor Type
    const vendorTypeCombobox = await page.getByRole('combobox', { name: 'Vendor Type' });
    await vendorTypeCombobox.click();
    await page.waitForTimeout(300);
    await vendorTypeCombobox.fill('DME');
    await page.waitForTimeout(300);
    await page.keyboard.press('Enter');
    await page.waitForTimeout(500);
    
    // Add Parent Link
    const addWorkItemButton = await page.locator('button:has-text("Add an existing work item")').first();
    await addWorkItemButton.click();
    await page.waitForTimeout(1500);
    
    const pickerInput = await page.locator('input[role="combobox"]').last();
    await pickerInput.click();
    await pickerInput.fill('421006');
    await page.waitForTimeout(2500);
    
    await page.keyboard.press('ArrowDown');
    await page.waitForTimeout(300);
    await page.keyboard.press('Enter');
    await page.waitForTimeout(1500);
    
    const okButton = await page.locator('button:has-text("OK")').first();
    await okButton.click();
    await page.waitForTimeout(2000);
    
    // Save
    await page.keyboard.press('Control+s');
    await page.waitForTimeout(3000);
    
    // Verify
    const currentUrl = await page.url();
    const storyIdMatch = currentUrl.match(/\/edit\/(\d+)/);
    return storyIdMatch ? `Story created: #${storyIdMatch[1]}` : 'Story creation failed';
}
```

---

## Rollback and Recovery

### If Story Creation Fails

1. **Check Browser State**: Use `browser_snapshot` to see current page
2. **Close Dialogs**: Click Cancel or Close on any open dialogs
3. **Navigate Fresh**: Go back to create story URL
4. **Start Over**: Begin from step 1 with fresh page load

### If Wrong Parent Link Added

1. **Navigate to Story**: Go to story edit URL
2. **Remove Link**: Click "Remove link" button in Related Work
3. **Add Correct Link**: Follow parent link process with correct Feature ID
4. **Save**: Use Control+s to save changes

### If Vendor Type Not Set

1. **Edit Story**: Navigate to story edit page
2. **Set Vendor Type**: Follow Vendor Type process
3. **Save**: Use Control+s
4. **Verify**: Check Classification section shows "DME"

---

## Success Metrics

### January 23, 2026 Sessions

#### Morning Session: User Stories
**Stories Created**: 5/5 (100% success rate)

1. **#421206** - Automated Task Closure After Deadlines
2. **#421207** - Add Package Metadata Fields to Bundle Configuration
3. **#421208** - Pre-built Data Export Report Templates
4. **#421210** - Admin Dashboard for Package Status Monitoring
5. **#421211** - Email Notification Templates with Scheduled Delivery

**Average Time per Story**: ~2-3 minutes including verification

**Common Issues Encountered**:
- Parent link dialog timing (solved with 2500ms wait)
- Vendor Type field validation (solved by setting before parent link)
- OK button disabled (solved with keyboard navigation)

#### Evening Session: Feature and User Story
**Work Items Created**: 2/2 (100% success rate)

1. **#421237** - Review and Document Existing Salesforce Platform Capabilities in Use (User Story)
   - Parent: Feature #414153
   - Comprehensive 9-category Salesforce capability review
   - Assigned to user successfully

2. **#421239** - ESV Platform Approach - Analysis of Alternatives (Feature)
   - Parent: Epic #415047
   - Target Date: 3/31/2026
   - Created via dialog from Epic page
   - Assigned to user successfully

**Key Learnings**:
- Dialog-based Feature creation is faster than navigation method
- Target Date is required for Features (not for Stories)
- Vendor Type required for both Stories and Features
- Assignment automation is fast: click dropdown, select user, save
- Scoped locators (`getByRole('dialog')`) prevent field targeting issues
- Features auto-link to parent when created via "New item" dialog

---

## Related Documents

- **Analysis**: `c:\projects\POCs\src\dmedev5\docs\Classic_PRM_Modernization_Analysis.md`
- **Story Details**: `c:\projects\POCs\src\dmedev5\docs\ADO_Stories_To_Create.md`
- **Creation Guide**: `c:\projects\POCs\src\dmedev5\docs\ADO_Story_Creation_Guide.md`
- **Memory**: Search for "ADO Story Creation - Classic PRM Modernization"

---

## Notes

- This guide is based on actual successful automation on January 23, 2026
- All timing values are tested and proven to work
- Keyboard navigation is more reliable than clicking for dropdowns
- Always verify each story before proceeding to the next
- Keep this guide updated with any new learnings or process changes
