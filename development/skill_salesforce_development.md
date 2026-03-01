# Salesforce Development Master Guide

**Last Updated:** January 26, 2026  
**Purpose:** Comprehensive guide for Salesforce development including SOQL queries, code deployment, cache management, and best practices  
**Success Rate:** Proven patterns from production development

---

## Table of Contents

1. [Overview](#overview)
2. [Environment Setup](#environment-setup)
3. [SOQL Query Patterns](#soql-query-patterns)
4. [Code Synchronization](#code-synchronization)
5. [Cache-Busting Strategies](#cache-busting-strategies)
6. [Apex Development](#apex-development)
7. [Lightning Web Components (LWC)](#lightning-web-components-lwc)
8. [Debugging and Troubleshooting](#debugging-and-troubleshooting)
9. [Best Practices](#best-practices)
10. [Common Issues and Solutions](#common-issues-and-solutions)

---

## Overview

This guide covers essential Salesforce development workflows including:
- Querying data with SOQL
- Deploying code to orgs
- Managing component caching
- Development best practices

### Prerequisites

- Salesforce CLI installed (`sf` command)
- PowerShell 5.1+ (for Windows scripts)
- Git for version control
- VS Code with Salesforce extensions (recommended)

---

## Environment Setup

### Salesforce CLI Authentication

```powershell
# Authenticate to an org with alias
sf org login web --alias dmedev5 --instance-url https://login.salesforce.com

# Set default org
sf config set target-org dmedev5

# List authenticated orgs
sf org list

# Display current org info
sf org display --target-org dmedev5
```

### Project Structure

```
project-root/
├── force-app/
│   └── main/
│       └── default/
│           ├── classes/          # Apex classes
│           ├── lwc/              # Lightning Web Components
│           ├── objects/          # Custom objects
│           ├── triggers/         # Apex triggers
│           └── aura/             # Aura components (legacy)
├── scripts/
│   └── apex/                     # Anonymous Apex scripts
├── sfdx-project.json             # Project configuration
└── sfsync.ps1                    # Custom sync script
```

---

## SOQL Query Patterns

### Basic Query Syntax

```apex
// Simple query
List<Account> accounts = [SELECT Id, Name FROM Account LIMIT 10];

// Query with WHERE clause
List<Contact> contacts = [
    SELECT Id, FirstName, LastName, Email
    FROM Contact
    WHERE AccountId = :accountId
];

// Query with relationship
List<Opportunity> opps = [
    SELECT Id, Name, Account.Name, Account.Industry
    FROM Opportunity
    WHERE StageName = 'Closed Won'
];
```

### Querying Custom Objects

```apex
// Query custom object
List<cmn_ContextInstance__c> contexts = [
    SELECT Id, Context_Instance_Id__c, Current_Node_Key__c,
           Bundle_Definition__c, Bundle_Definition__r.Name
    FROM cmn_ContextInstance__c
    WHERE Item_Status__c = 'Active'
    ORDER BY CreatedDate DESC
    LIMIT 100
];

// Query with related records
List<cfgHub_BundleDefinition__c> bundles = [
    SELECT Id, Name, 
           Workflow_Definition__c,
           Workflow_Definition__r.Process_Map_JSON__c,
           (SELECT Id, Node_Key__c FROM cmn_Context_Instances__r)
    FROM cfgHub_BundleDefinition__c
    WHERE Active__c = true
];
```

### Query Limitations and Best Practices

**CRITICAL LIMITATIONS:**
- Long Text Area fields cannot be used in WHERE clauses
- Maximum 50,000 records per query
- Maximum 100 SOQL queries per transaction
- Maximum 10,000 records returned per query (use LIMIT)

```apex
// ❌ WRONG - Cannot filter on long text field
List<cfgHub_BundleDefinition__c> bundles = [
    SELECT Id, Name, Workflow_Definition__r.Process_Map_JSON__c
    FROM cfgHub_BundleDefinition__c
    WHERE Workflow_Definition__r.Process_Map_JSON__c != null  // ERROR!
];

// ✅ CORRECT - Query all, filter in code
List<cfgHub_BundleDefinition__c> bundles = [
    SELECT Id, Name, Workflow_Definition__c, 
           Workflow_Definition__r.Process_Map_JSON__c
    FROM cfgHub_BundleDefinition__c
    WHERE Workflow_Definition__c != null
    LIMIT 10
];

// Filter in Apex
cfgHub_BundleDefinition__c bundle = null;
for (cfgHub_BundleDefinition__c b : bundles) {
    if (String.isNotBlank(b.Workflow_Definition__r?.Process_Map_JSON__c)) {
        bundle = b;
        break;
    }
}
```

### Dynamic SOQL

```apex
// Build query dynamically
String objectName = 'Account';
String fieldName = 'Name';
String whereClause = 'Industry = \'Technology\'';

String query = 'SELECT Id, ' + fieldName + ' FROM ' + objectName;
if (String.isNotBlank(whereClause)) {
    query += ' WHERE ' + whereClause;
}
query += ' LIMIT 100';

List<SObject> records = Database.query(query);
```

### Query Performance Tips

```apex
// ✅ Use selective filters (indexed fields)
List<Contact> contacts = [
    SELECT Id, Name 
    FROM Contact 
    WHERE Email = 'test@example.com'  // Email is indexed
];

// ✅ Limit fields to only what you need
List<Account> accounts = [
    SELECT Id, Name  // Only query needed fields
    FROM Account
];

// ✅ Use LIMIT to prevent governor limit issues
List<Opportunity> opps = [
    SELECT Id, Name 
    FROM Opportunity 
    WHERE StageName = 'Prospecting'
    LIMIT 200  // Always use LIMIT
];

// ✅ Bulkify queries (query once, not in loop)
Set<Id> accountIds = new Set<Id>();
for (Contact c : contacts) {
    accountIds.add(c.AccountId);
}
Map<Id, Account> accountMap = new Map<Id, Account>([
    SELECT Id, Name, Industry 
    FROM Account 
    WHERE Id IN :accountIds
]);
```

---

## Code Synchronization

### Using sfsync.ps1 (Custom Script)

The `sfsync.ps1` script provides streamlined deployment with pattern matching.

**Basic Syntax:**
```powershell
.\sfsync.ps1 -type <type> -pattern <pattern> -action <action> -org <org>
```

**Parameters:**
- `-type`: Component type (lwc, apex, object, trigger, flow, etc.)
- `-pattern`: Glob pattern to match files
- `-action`: push (deploy) or pull (retrieve)
- `-org`: Target org alias

#### Deploy Apex Classes

```powershell
# Deploy single class
.\sfsync.ps1 -type apex -pattern "cmn_WorkflowNode" -action push -org dmedev5

# Deploy multiple classes with pattern
.\sfsync.ps1 -type apex -pattern "cmn_Workflow*" -action push -org dmedev5

# Deploy all classes in a package
.\sfsync.ps1 -type apex -pattern "cmn_*" -action push -org dmedev5
```

#### Deploy Lightning Web Components

```powershell
# Deploy single LWC
.\sfsync.ps1 -type lwc -pattern "cmn_WorkflowDiagram" -action push -org dmedev5

# Deploy multiple LWCs with pattern
.\sfsync.ps1 -type lwc -pattern "cmn_Workflow*" -action push -org dmedev5

# Deploy all bundle-related components
.\sfsync.ps1 -type lwc -pattern "cfgHub_Bundle*" -action push -org dmedev5
```

#### Deploy Other Metadata

```powershell
# Deploy custom object
.\sfsync.ps1 -type object -pattern "cmn_ContextInstance__c" -action push -org dmedev5

# Deploy trigger
.\sfsync.ps1 -type trigger -pattern "cmn_ContextInstanceTrigger" -action push -org dmedev5

# Deploy flow
.\sfsync.ps1 -type flow -pattern "Approval_Outcome_Handler" -action push -org dmedev5
```

### Using Salesforce CLI Directly

```powershell
# Deploy specific source files
sf project deploy start --source-dir "force-app\main\default\classes\cmn_WorkflowNode.cls" --target-org dmedev5

# Deploy entire directory
sf project deploy start --source-dir "force-app\main\default\lwc\cmn_WorkflowDiagram" --target-org dmedev5

# Deploy with tests
sf project deploy start --source-dir "force-app\main\default\classes" --test-level RunLocalTests --target-org dmedev5

# Quick deploy (no tests)
sf project deploy start --source-dir "force-app\main\default\classes" --target-org dmedev5

# Deploy and wait for completion
sf project deploy start --source-dir "force-app\main\default\lwc" --wait 10 --target-org dmedev5
```

### Retrieve Code from Org

```powershell
# Retrieve specific metadata
sf project retrieve start --metadata ApexClass:cmn_WorkflowNode --target-org dmedev5

# Retrieve all Apex classes
sf project retrieve start --metadata ApexClass --target-org dmedev5

# Retrieve LWC
sf project retrieve start --metadata LightningComponentBundle:cmn_WorkflowDiagram --target-org dmedev5

# Retrieve using manifest
sf project retrieve start --manifest manifest/package.xml --target-org dmedev5
```

---

## Cache-Busting Strategies

### Lightning Web Component Caching

**CRITICAL ISSUE:** Salesforce aggressively caches LWC components. Changes may not appear immediately.

#### Strategy 1: Deploy Parent Components

When you change a child component, **always deploy the parent component** to break the cache.

```powershell
# Example: Changed cfgHub_BundleConfigurationFlow
# Deploy BOTH child and parent

# Deploy child
.\sfsync.ps1 -type lwc -pattern "cfgHub_BundleConfigurationFlow" -action push -org dmedev5

# Deploy parent (CRITICAL!)
.\sfsync.ps1 -type lwc -pattern "cfgHub_BundleConfiguration" -action push -org dmedev5

# Or deploy all related components
.\sfsync.ps1 -type lwc -pattern "cfgHub_Bundle*" -action push -org dmedev5
```

#### Strategy 2: Hard Refresh in Browser

After deployment:
1. Open the page in Salesforce
2. Press `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)
3. Or open DevTools → Network tab → Check "Disable cache" → Refresh

#### Strategy 3: Clear Salesforce Cache

```
Setup → Session Settings → Clear Cache
```

Or use URL parameter:
```
https://your-org.lightning.force.com/lightning/page?cache=clear
```

#### Strategy 4: Version Bump

Update the component's API version in the meta file:

```xml
<!-- cmn_WorkflowDiagram.js-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<LightningComponentBundle xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>65.0</apiVersion>  <!-- Increment this -->
    <isExposed>true</isExposed>
</LightningComponentBundle>
```

### Apex Class Caching

Apex classes are generally not cached as aggressively, but follow these practices:

```powershell
# Deploy dependent classes together
.\sfsync.ps1 -type apex -pattern "cmn_Workflow*" -action push -org dmedev5

# If class A calls class B, deploy both:
sf project deploy start --source-dir "force-app\main\default\classes\cmn_WorkflowNode.cls,force-app\main\default\classes\cmn_WorkflowTransitionMethods.cls" --target-org dmedev5
```

### Static Resource Caching

Static resources are heavily cached. Always increment the version:

```xml
<!-- Before -->
<StaticResource>
    <cacheControl>Public</cacheControl>
    <contentType>application/javascript</contentType>
</StaticResource>

<!-- Reference with version -->
<script src="{!$Resource.MyScript}?v=2"></script>
```

---

## Apex Development

### Running Anonymous Apex

```powershell
# Run Apex script file
sf apex run --file "scripts\apex\Test-WorkflowNodeTransitions.apex" --target-org dmedev5

# Run inline Apex
sf apex run --target-org dmedev5
# Then paste code and press Ctrl+D
```

### Debug Logs

```powershell
# Tail logs in real-time
sf apex tail log --target-org dmedev5

# Get specific log
sf apex get log --log-id <logId> --target-org dmedev5

# List recent logs
sf apex list log --target-org dmedev5
```

### Running Tests

```powershell
# Run specific test class
sf apex run test --class-names "cmn_WorkflowNode_Test" --result-format human --code-coverage --target-org dmedev5

# Run all tests
sf apex run test --test-level RunLocalTests --result-format human --code-coverage --target-org dmedev5

# Run tests synchronously
sf apex run test --class-names "MyTest" --synchronous --target-org dmedev5
```

### Apex Best Practices

```apex
// ✅ Bulkify - Handle collections, not single records
public static void updateAccounts(List<Account> accounts) {
    List<Account> toUpdate = new List<Account>();
    for (Account acc : accounts) {
        if (acc.AnnualRevenue > 1000000) {
            acc.Rating = 'Hot';
            toUpdate.add(acc);
        }
    }
    update toUpdate;
}

// ✅ Use maps for efficient lookups
Map<Id, Account> accountMap = new Map<Id, Account>([
    SELECT Id, Name FROM Account WHERE Id IN :accountIds
]);

// ✅ Check for null and empty
if (String.isNotBlank(myString)) {
    // Safe to use
}

if (myList != null && !myList.isEmpty()) {
    // Safe to iterate
}

// ✅ Use try-catch for error handling
try {
    insert records;
} catch (DmlException e) {
    System.debug('Error: ' + e.getMessage());
    // Handle error appropriately
}

// ✅ Use Database methods for partial success
Database.SaveResult[] results = Database.insert(records, false);
for (Database.SaveResult sr : results) {
    if (!sr.isSuccess()) {
        for (Database.Error err : sr.getErrors()) {
            System.debug('Error: ' + err.getMessage());
        }
    }
}
```

---

## Lightning Web Components (LWC)

### Component Structure

```javascript
// myComponent.js
import { LightningElement, api, track, wire } from 'lwc';
import getRecords from '@salesforce/apex/MyController.getRecords';

export default class MyComponent extends LightningElement {
    // Public property (can be set from parent)
    @api recordId;
    
    // Tracked property (reactive)
    @track data = [];
    
    // Private property
    _internalValue;
    
    // Lifecycle hooks
    connectedCallback() {
        // Component inserted into DOM
        this.loadData();
    }
    
    renderedCallback() {
        // Component finished rendering
    }
    
    disconnectedCallback() {
        // Component removed from DOM
    }
    
    // Wire service
    @wire(getRecords, { recordId: '$recordId' })
    wiredRecords({ error, data }) {
        if (data) {
            this.data = data;
        } else if (error) {
            console.error('Error:', error);
        }
    }
    
    // Imperative Apex call
    async loadData() {
        try {
            const result = await getRecords({ recordId: this.recordId });
            this.data = result;
        } catch (error) {
            console.error('Error:', error);
        }
    }
    
    // Event handler
    handleClick(event) {
        // Dispatch custom event to parent
        this.dispatchEvent(new CustomEvent('itemselected', {
            detail: { itemId: event.target.dataset.id }
        }));
    }
}
```

### LWC Deployment Checklist

```powershell
# 1. Deploy the changed component
.\sfsync.ps1 -type lwc -pattern "myComponent" -action push -org dmedev5

# 2. Deploy parent components (CRITICAL for cache-busting)
.\sfsync.ps1 -type lwc -pattern "parentComponent" -action push -org dmedev5

# 3. If component uses Apex controller, deploy that too
.\sfsync.ps1 -type apex -pattern "MyController" -action push -org dmedev5

# 4. Hard refresh browser (Ctrl+Shift+R)

# 5. Check browser console for errors
```

### Common LWC Patterns

```javascript
// Getter/Setter pattern
_value;
@api
get value() {
    return this._value;
}
set value(val) {
    this._value = val;
    this.processValue();
}

// Conditional rendering in template
<template if:true={hasData}>
    <div>Data: {data}</div>
</template>
<template if:false={hasData}>
    <div>No data available</div>
</template>

// Iteration
<template for:each={items} for:item="item">
    <div key={item.id}>{item.name}</div>
</template>

// Event handling
<lightning-button label="Click Me" onclick={handleClick}></lightning-button>

// Two-way data binding
<lightning-input value={inputValue} onchange={handleChange}></lightning-input>
```

---

## Debugging and Troubleshooting

### Enable Debug Logs

```
Setup → Debug Logs → New → Select User → Set levels:
- Apex Code: FINEST
- Visualforce: FINER
- System: DEBUG
```

### Common Debug Patterns

```apex
// Basic debug
System.debug('Value: ' + myVariable);

// Debug with log level
System.debug(LoggingLevel.ERROR, 'Critical error: ' + errorMsg);

// Debug complex objects
System.debug('Account: ' + JSON.serializePretty(account));

// Debug with context
System.debug('=== METHOD START: myMethod ===');
System.debug('Input param: ' + param);
// ... method logic ...
System.debug('=== METHOD END: myMethod ===');
```

### Browser DevTools for LWC

```javascript
// Console logging
console.log('Value:', this.data);
console.error('Error:', error);
console.table(this.items); // Display array as table

// Debugger breakpoint
debugger; // Pauses execution

// Check component state
// In browser console:
$0 // Selected element
$0.__lwcElement__ // Access LWC component instance
```

### Query Execution Time

```apex
// Measure query performance
Long startTime = System.currentTimeMillis();
List<Account> accounts = [SELECT Id, Name FROM Account LIMIT 1000];
Long endTime = System.currentTimeMillis();
System.debug('Query took: ' + (endTime - startTime) + 'ms');
```

---

## Best Practices

### 1. Always Use Version Control

```bash
# Commit before making changes
git add .
git commit -m "Before updating workflow architecture"

# Create feature branch
git checkout -b feature/workflow-enhancements

# Commit after successful deployment
git add .
git commit -m "Updated workflow diagram with new node types"
```

### 2. Test in Sandbox First

```powershell
# Deploy to sandbox
.\sfsync.ps1 -type apex -pattern "cmn_Workflow*" -action push -org sandbox

# Test thoroughly

# Then deploy to production
.\sfsync.ps1 -type apex -pattern "cmn_Workflow*" -action push -org production
```

### 3. Use Descriptive Names

```apex
// ❌ Bad
List<Account> a = [SELECT Id FROM Account];

// ✅ Good
List<Account> activeAccounts = [
    SELECT Id, Name, Industry 
    FROM Account 
    WHERE IsActive__c = true
];
```

### 4. Document Your Code

```apex
/**
 * Advances workflow to next node based on transition parameters
 * 
 * @param contextInstanceId The context instance ID
 * @param transitionParams Map of transition parameters
 * @param metadata Optional metadata for enhanced tracking
 * @return WorkflowTransitionResultDTO with transition results
 */
public static WorkflowTransitionResultDTO advanceWorkflow(
    String contextInstanceId,
    Map<String, Object> transitionParams,
    Map<String, Object> metadata
) {
    // Implementation
}
```

### 5. Handle Errors Gracefully

```apex
public static void processRecords(List<Account> accounts) {
    List<Account> toUpdate = new List<Account>();
    
    try {
        for (Account acc : accounts) {
            // Process logic
            toUpdate.add(acc);
        }
        
        if (!toUpdate.isEmpty()) {
            Database.SaveResult[] results = Database.update(toUpdate, false);
            
            for (Integer i = 0; i < results.size(); i++) {
                if (!results[i].isSuccess()) {
                    System.debug(LoggingLevel.ERROR, 
                        'Failed to update account ' + toUpdate[i].Id + ': ' + 
                        results[i].getErrors()[0].getMessage());
                }
            }
        }
    } catch (Exception e) {
        System.debug(LoggingLevel.ERROR, 'Unexpected error: ' + e.getMessage());
        System.debug(LoggingLevel.ERROR, 'Stack trace: ' + e.getStackTraceString());
        throw e; // Re-throw if caller needs to handle
    }
}
```

---

## Common Issues and Solutions

### Issue 1: "Field does not exist" Error

**Problem:** Query fails with field not found error.

**Solution:**
```apex
// Check field API name in Setup → Object Manager
// Use correct API name with __c suffix for custom fields

// ❌ Wrong
SELECT Status FROM cmn_ContextInstance__c

// ✅ Correct
SELECT Item_Status__c FROM cmn_ContextInstance__c
```

### Issue 2: "Field is not writeable" Error

**Problem:** Cannot set value on auto-number or formula field.

**Solution:**
```apex
// Don't try to set auto-number fields
// ❌ Wrong
ctx.Context_Instance_Id__c = 'TEST-123';

// ✅ Correct - Let Salesforce generate it
insert ctx;
ctx = [SELECT Id, Context_Instance_Id__c FROM cmn_ContextInstance__c WHERE Id = :ctx.Id];
```

### Issue 3: LWC Changes Not Appearing

**Problem:** Deployed LWC but changes don't show in UI.

**Solution:**
```powershell
# 1. Deploy parent components
.\sfsync.ps1 -type lwc -pattern "parentComponent*" -action push -org dmedev5

# 2. Hard refresh browser (Ctrl+Shift+R)

# 3. Clear Salesforce cache
# Setup → Session Settings → Clear Cache

# 4. Check browser console for errors
```

### Issue 4: "Too many SOQL queries" Error

**Problem:** Hit 100 SOQL query limit.

**Solution:**
```apex
// ❌ Wrong - Query in loop
for (Contact c : contacts) {
    Account acc = [SELECT Id, Name FROM Account WHERE Id = :c.AccountId];
}

// ✅ Correct - Query once, use map
Set<Id> accountIds = new Set<Id>();
for (Contact c : contacts) {
    accountIds.add(c.AccountId);
}
Map<Id, Account> accountMap = new Map<Id, Account>([
    SELECT Id, Name FROM Account WHERE Id IN :accountIds
]);
for (Contact c : contacts) {
    Account acc = accountMap.get(c.AccountId);
}
```

### Issue 5: "Cannot filter on long text field"

**Problem:** WHERE clause on Long Text Area field fails.

**Solution:**
```apex
// ❌ Wrong
List<Bundle__c> bundles = [
    SELECT Id, LongTextField__c 
    FROM Bundle__c 
    WHERE LongTextField__c != null
];

// ✅ Correct - Query all, filter in code
List<Bundle__c> bundles = [
    SELECT Id, LongTextField__c 
    FROM Bundle__c 
    LIMIT 100
];
Bundle__c result = null;
for (Bundle__c b : bundles) {
    if (String.isNotBlank(b.LongTextField__c)) {
        result = b;
        break;
    }
}
```

### Issue 6: Deployment Fails with "Unknown user permission"

**Problem:** Deploying profile or permission set fails.

**Solution:**
```powershell
# Deploy without profiles/permission sets
sf project deploy start --source-dir "force-app\main\default\classes" --target-org dmedev5

# Or remove problematic permissions from XML before deploying
```

### Issue 7: "Apex CPU time limit exceeded"

**Problem:** Code runs too long (10 seconds limit).

**Solution:**
```apex
// ✅ Optimize queries
// ✅ Reduce loop iterations
// ✅ Use @future or Queueable for long-running operations

@future
public static void processLargeDataSet(Set<Id> recordIds) {
    // Long-running logic here
}
```

---

## Quick Reference Commands

### Most Common Commands

```powershell
# Deploy Apex class
.\sfsync.ps1 -type apex -pattern "ClassName" -action push -org dmedev5

# Deploy LWC (with parent for cache-busting)
.\sfsync.ps1 -type lwc -pattern "componentName" -action push -org dmedev5
.\sfsync.ps1 -type lwc -pattern "parentComponent" -action push -org dmedev5

# Run Apex script
sf apex run --file "scripts\apex\MyScript.apex" --target-org dmedev5

# Tail debug logs
sf apex tail log --target-org dmedev5

# Run tests
sf apex run test --class-names "TestClass" --result-format human --target-org dmedev5

# Query data
sf data query --query "SELECT Id, Name FROM Account LIMIT 10" --target-org dmedev5
```

---

## Environment Credentials

**CRITICAL:** All environment credentials MUST be loaded from:
```
G:\My Drive\03_Areas\Keys\Environments\
```

**NEVER** reference credentials from project directories.

**ALWAYS** use:
```powershell
$envs = & 'G:\My Drive\03_Areas\Keys\Environments\Load-Environments.ps1'
```

---

## Related Documentation

- **ADO Automation Master Guide:** `G:\My Drive\06_Master_Guides\ADO_Automation_Master_Guide.md`
- **Salesforce CLI Documentation:** https://developer.salesforce.com/docs/atlas.en-us.sfdx_cli_reference.meta/sfdx_cli_reference/
- **LWC Developer Guide:** https://developer.salesforce.com/docs/component-library/documentation/en/lwc
- **Apex Developer Guide:** https://developer.salesforce.com/docs/atlas.en-us.apexcode.meta/apexcode/

---

## Success Metrics

- **Deployment Success Rate:** Track successful vs failed deployments
- **Cache-Busting Effectiveness:** Verify changes appear after deployment
- **Query Performance:** Monitor query execution times
- **Test Coverage:** Maintain >75% code coverage (>90% recommended)

---

## Maintenance

- Update this guide when discovering new patterns or solutions
- Document any new issues and their resolutions
- Keep command examples current with latest Salesforce CLI versions
- Review and update best practices quarterly
