# Salesforce Field Level Security (FLS) Automation Master Guide

**Last Updated:** January 29, 2026  
**Purpose:** Automate Field Level Security configuration for custom objects using Playwright browser automation  
**Success Rate:** TBD (Initial version)

---

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Critical Process Overview](#critical-process-overview)
4. [Step-by-Step Instructions](#step-by-step-instructions)
5. [Common Issues and Solutions](#common-issues-and-solutions)
6. [Verification Steps](#verification-steps)
7. [Complete Examples](#complete-examples)
8. [Rollback and Recovery](#rollback-and-recovery)
9. [Related Documents](#related-documents)

---

## 1. Overview

### Purpose
Automate the tedious process of setting Field Level Security for custom objects across multiple profiles. Manual FLS configuration can take hours for objects with many fields and multiple profiles.

### What This Automates
- Navigate to Object Manager → Custom Object → Fields & Relationships
- For each field, set FLS permissions (Visible/Read-Only) for multiple profiles
- Bulk update all fields for a given object
- Support for multiple profiles (System Administrator, Custom Profiles, etc.)

### Time Savings
- **Manual Process:** 5-10 minutes per field × 30 fields = 2.5-5 hours per object
- **Automated Process:** 2-3 minutes per object (regardless of field count)
- **ROI:** 95%+ time savings for objects with 20+ fields

---

## 2. Prerequisites

### Access Requirements
- Salesforce org access with "Customize Application" permission
- System Administrator profile or equivalent
- Object Manager access
- Playwright MCP server running

### Information Needed
1. **Org URL:** e.g., `https://dmedev5-dev-ed.develop.my.salesforce.com`
2. **Object API Name:** e.g., `bphc_GeneralInformation__c`
3. **Profile Names:** List of profiles to update (e.g., "System Administrator", "BPHC User")
4. **FLS Settings:** For each profile:
   - Visible: true/false
   - Read-Only: true/false

### Tools Required
- Playwright browser automation (via MCP)
- Active Salesforce session

---

## 3. Critical Process Overview

### Golden Rules
1. **Always save after each field** - Don't batch multiple fields without saving
2. **Wait for page loads** - Salesforce Setup pages can be slow
3. **Verify profile selection** - Ensure correct profile is selected before setting permissions
4. **Handle dynamic content** - Field lists may load asynchronously
5. **One object at a time** - Don't try to automate multiple objects in parallel

### Process Sequence
```
1. Navigate to Object Manager
2. Search for and select custom object
3. Click "Fields & Relationships"
4. For each field:
   a. Click field name to open detail page
   b. Click "Set Field-Level Security" button
   c. For each profile:
      - Check/uncheck "Visible" checkbox
      - Check/uncheck "Read Only" checkbox
   d. Click "Save"
   e. Wait for confirmation
   f. Return to field list
5. Verify all fields updated
```

---

## 4. Step-by-Step Instructions

### Step 1: Navigate to Object Manager
```javascript
// Navigate to Setup → Object Manager
await page.goto('https://[ORG_URL]/lightning/setup/ObjectManager/home');
await page.waitForLoadState('networkidle');
await page.waitForTimeout(2000);
```

### Step 2: Search for Custom Object
```javascript
// Search for object (e.g., "bphc_GeneralInformation__c")
const searchBox = page.getByPlaceholder('Quick Find');
await searchBox.click();
await searchBox.fill('bphc_GeneralInformation__c');
await page.waitForTimeout(1500);

// Click on the object from search results
await page.getByRole('link', { name: 'bphc_GeneralInformation__c' }).click();
await page.waitForLoadState('networkidle');
await page.waitForTimeout(2000);
```

### Step 3: Navigate to Fields & Relationships
```javascript
// Click "Fields & Relationships" tab
await page.getByRole('link', { name: 'Fields & Relationships' }).click();
await page.waitForLoadState('networkidle');
await page.waitForTimeout(2000);
```

### Step 4: Get List of Custom Fields
```javascript
// Get all custom field rows (exclude standard fields)
const fieldRows = await page.locator('tr').filter({ hasText: '__c' }).all();
console.log(`Found ${fieldRows.length} custom fields`);
```

### Step 5: Process Each Field
```javascript
for (const fieldRow of fieldRows) {
    // Get field name
    const fieldName = await fieldRow.locator('th a').textContent();
    console.log(`Processing field: ${fieldName}`);
    
    // Click field name to open detail page
    await fieldRow.locator('th a').click();
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    
    // Click "Set Field-Level Security" button
    await page.getByRole('button', { name: 'Set Field-Level Security' }).click();
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);
    
    // Set permissions for each profile
    await setProfilePermissions(page, 'System Administrator', { visible: true, readOnly: false });
    await setProfilePermissions(page, 'BPHC User', { visible: true, readOnly: false });
    
    // Save
    await page.keyboard.press('Control+s');
    await page.waitForTimeout(2000);
    
    // Navigate back to field list
    await page.goBack();
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(1500);
}
```

### Step 6: Set Profile Permissions Helper Function
```javascript
async function setProfilePermissions(page, profileName, permissions) {
    // Find the profile row
    const profileRow = page.locator('tr').filter({ hasText: profileName });
    
    // Set "Visible" checkbox
    const visibleCheckbox = profileRow.locator('input[type="checkbox"]').first();
    const isVisibleChecked = await visibleCheckbox.isChecked();
    if (permissions.visible && !isVisibleChecked) {
        await visibleCheckbox.check();
    } else if (!permissions.visible && isVisibleChecked) {
        await visibleCheckbox.uncheck();
    }
    
    // Set "Read Only" checkbox (only if visible)
    if (permissions.visible) {
        const readOnlyCheckbox = profileRow.locator('input[type="checkbox"]').nth(1);
        const isReadOnlyChecked = await readOnlyCheckbox.isChecked();
        if (permissions.readOnly && !isReadOnlyChecked) {
            await readOnlyCheckbox.check();
        } else if (!permissions.readOnly && isReadOnlyChecked) {
            await readOnlyCheckbox.uncheck();
        }
    }
}
```

---

## 5. Common Issues and Solutions

### Issue 1: Page Not Loading
**Symptom:** Blank page or "Setting things up" message  
**Solution:** Wait longer (5-10 seconds) and refresh if needed
```javascript
await page.waitForTimeout(5000);
await page.reload();
```

### Issue 2: Field Not Found
**Symptom:** Cannot locate field in list  
**Solution:** Ensure you're filtering for custom fields (`__c`) and check object has fields
```javascript
const fieldCount = await page.locator('tr').filter({ hasText: '__c' }).count();
if (fieldCount === 0) {
    console.log('No custom fields found - check object');
}
```

### Issue 3: Profile Not Found
**Symptom:** Profile row not visible in FLS page  
**Solution:** Scroll to find profile or verify profile name is exact match
```javascript
const profileRow = page.locator('tr').filter({ hasText: new RegExp(`^${profileName}$`) });
await profileRow.scrollIntoViewIfNeeded();
```

### Issue 4: Save Not Working
**Symptom:** Changes not persisting  
**Solution:** Use explicit Save button instead of keyboard shortcut
```javascript
await page.getByRole('button', { name: 'Save' }).click();
await page.waitForTimeout(2000);
```

### Issue 5: Navigation Timing Issues
**Symptom:** Clicks happening before page fully loads  
**Solution:** Increase wait times and use multiple wait strategies
```javascript
await page.waitForLoadState('networkidle');
await page.waitForSelector('tr:has-text("__c")');
await page.waitForTimeout(2000);
```

---

## 6. Verification Steps

### Verify FLS Was Set Correctly
1. Navigate back to object → Fields & Relationships
2. Click on a random field
3. Click "View Field-Level Security"
4. Verify profiles show correct Visible/Read-Only settings

### Automated Verification
```javascript
// After processing all fields, verify one field
await page.goto(`https://[ORG_URL]/lightning/setup/ObjectManager/[OBJECT]/FieldsAndRelationships/[FIELD_ID]/view`);
await page.getByRole('button', { name: 'View Field-Level Security' }).click();
await page.waitForLoadState('networkidle');

// Check System Administrator has correct permissions
const adminRow = page.locator('tr').filter({ hasText: 'System Administrator' });
const isVisible = await adminRow.locator('td').nth(1).textContent(); // Should be "Visible"
console.log(`System Administrator visibility: ${isVisible}`);
```

---

## 7. Complete Examples

### Example 1: Set All Fields to Visible for System Administrator
```javascript
async function setAllFieldsVisible(objectApiName, profileName) {
    // Navigate to object
    await page.goto(`https://dmedev5-dev-ed.develop.my.salesforce.com/lightning/setup/ObjectManager/home`);
    await page.waitForLoadState('networkidle');
    
    // Search and select object
    await page.getByPlaceholder('Quick Find').fill(objectApiName);
    await page.waitForTimeout(1500);
    await page.getByRole('link', { name: objectApiName }).click();
    await page.waitForLoadState('networkidle');
    
    // Go to Fields & Relationships
    await page.getByRole('link', { name: 'Fields & Relationships' }).click();
    await page.waitForLoadState('networkidle');
    
    // Get all custom fields
    const fields = await page.locator('tr').filter({ hasText: '__c' }).all();
    
    for (let i = 0; i < fields.length; i++) {
        // Re-query fields to avoid stale references
        const currentField = page.locator('tr').filter({ hasText: '__c' }).nth(i);
        const fieldName = await currentField.locator('th a').textContent();
        
        console.log(`[${i+1}/${fields.length}] Processing: ${fieldName}`);
        
        // Click field
        await currentField.locator('th a').click();
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(2000);
        
        // Set FLS
        await page.getByRole('button', { name: 'Set Field-Level Security' }).click();
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(2000);
        
        // Find profile and set visible
        const profileRow = page.locator('tr').filter({ hasText: profileName });
        const visibleCheckbox = profileRow.locator('input[type="checkbox"]').first();
        if (!await visibleCheckbox.isChecked()) {
            await visibleCheckbox.check();
        }
        
        // Save
        await page.keyboard.press('Control+s');
        await page.waitForTimeout(2000);
        
        // Go back to field list
        await page.goBack();
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(1500);
    }
    
    console.log(`✅ Completed FLS for ${fields.length} fields`);
}

// Usage
await setAllFieldsVisible('bphc_GeneralInformation__c', 'System Administrator');
```

### Example 2: Set Multiple Profiles with Different Permissions
```javascript
const flsConfig = {
    'System Administrator': { visible: true, readOnly: false },
    'BPHC User': { visible: true, readOnly: false },
    'BPHC Read Only': { visible: true, readOnly: true },
    'Standard User': { visible: false, readOnly: false }
};

async function setMultiProfileFLS(objectApiName, flsConfig) {
    // ... navigation code same as Example 1 ...
    
    const fields = await page.locator('tr').filter({ hasText: '__c' }).all();
    
    for (let i = 0; i < fields.length; i++) {
        const currentField = page.locator('tr').filter({ hasText: '__c' }).nth(i);
        const fieldName = await currentField.locator('th a').textContent();
        
        console.log(`Processing: ${fieldName}`);
        
        await currentField.locator('th a').click();
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(2000);
        
        await page.getByRole('button', { name: 'Set Field-Level Security' }).click();
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(2000);
        
        // Set permissions for each profile
        for (const [profileName, permissions] of Object.entries(flsConfig)) {
            await setProfilePermissions(page, profileName, permissions);
        }
        
        await page.keyboard.press('Control+s');
        await page.waitForTimeout(2000);
        
        await page.goBack();
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(1500);
    }
}

// Usage
await setMultiProfileFLS('bphc_GeneralInformation__c', flsConfig);
```

---

## 8. Rollback and Recovery

### If Automation Fails Mid-Process
1. **Identify last successful field:** Check console logs for last completed field
2. **Manual verification:** Verify FLS for fields processed so far
3. **Resume from failure point:** Modify script to skip already-processed fields
4. **Alternative:** Use Salesforce metadata API to bulk update remaining fields

### Rollback FLS Changes
```javascript
// Set all fields back to not visible for a profile
async function rollbackFLS(objectApiName, profileName) {
    // Same navigation as before
    const fields = await page.locator('tr').filter({ hasText: '__c' }).all();
    
    for (let i = 0; i < fields.length; i++) {
        // ... navigation to field FLS page ...
        
        const profileRow = page.locator('tr').filter({ hasText: profileName });
        const visibleCheckbox = profileRow.locator('input[type="checkbox"]').first();
        if (await visibleCheckbox.isChecked()) {
            await visibleCheckbox.uncheck();
        }
        
        await page.keyboard.press('Control+s');
        await page.waitForTimeout(2000);
        await page.goBack();
        await page.waitForLoadState('networkidle');
    }
}
```

---

## 9. Related Documents

- **BPHC Canonical Design:** `c:\projects\POCs\src\dmedev5\docs\BPHC_CANONICAL_DESIGN.md`
- **ADO Automation Master Guide:** `G:\My Drive\06_Master_Guides\ADO_Automation_Master_Guide.md`
- **Salesforce Object Manager:** https://help.salesforce.com/s/articleView?id=sf.dev_objectmgr.htm
- **Field-Level Security:** https://help.salesforce.com/s/articleView?id=sf.admin_fls.htm

---

## Success Metrics

- **Fields Processed:** Track number of fields successfully updated
- **Time Per Field:** Average ~5-10 seconds per field
- **Error Rate:** Target <5% (retry failed fields)
- **Total Time:** Complete object with 30 fields in ~3-5 minutes

---

## Next Steps

1. Test automation on a single field first
2. Run on small object (5-10 fields) to validate
3. Apply to all BPHC canonical objects (8 objects × ~30 fields = 240 fields)
4. Document any edge cases or issues encountered
5. Update this guide with lessons learned
