# Salesforce Deployment Patterns

## Overview
Deployment strategies, cache invalidation patterns, and best practices for deploying Salesforce metadata including Apex classes, LWC components, and custom objects.

## Critical Deployment Principles

### 1. Cache Invalidation Pattern

**CRITICAL:** Salesforce caches compiled bytecode. Deploying only the modified class does NOT invalidate the cache. You must deploy ALL classes in the call chain.

```powershell
# ❌ WRONG - Only deploys modified class
.\sfsync.ps1 -type apex -pattern "MyService" -action push -org myorg

# ✅ CORRECT - Deploys entire call chain
.\sfsync.ps1 -type apex -pattern "My*" -action push -org myorg
```

### 2. The Call Chain Rule

When you modify a class, deploy:
1. The modified class
2. All classes that CALL the modified class (upstream)
3. All classes that the modified class calls (downstream)

**Example:**
```
MyApi (REST endpoint)
  └─> calls MyService
      └─> calls MyServiceExtensions
```

If you modify `MyServiceExtensions`, deploy ALL THREE classes.

### 3. LWC Component Deployment

When deploying LWC components, always deploy parent components that reference them.

```powershell
# ❌ WRONG - Only child component
.\sfsync.ps1 -type lwc -pattern "myChildComponent" -action push -org myorg

# ✅ CORRECT - Child and all parents
.\sfsync.ps1 -type lwc -pattern "my*Component" -action push -org myorg
```

## Deployment Tools

### Tool 1: sfsync.ps1 (Generic Script)

```powershell
# Deploy Apex classes
.\sfsync.ps1 -type apex -pattern "MyClass*" -action push -org myorg

# Deploy LWC components
.\sfsync.ps1 -type lwc -pattern "myComponent" -action push -org myorg

# Deploy custom objects
.\sfsync.ps1 -type object -pattern "MyObject__c" -action push -org myorg

# Deploy all metadata
.\sfsync.ps1 -type all -action push -org myorg

# Pull from org
.\sfsync.ps1 -type apex -pattern "MyClass" -action pull -org myorg
```

### Tool 2: Salesforce CLI (sfdx)

```powershell
# Deploy source
sfdx force:source:deploy -p "force-app/main/default/classes/MyClass.cls" -u myorg

# Deploy with test execution
sfdx force:source:deploy -p "force-app/main/default" -u myorg -l RunLocalTests

# Validate deployment (check only)
sfdx force:source:deploy -p "force-app/main/default" -u myorg --checkonly

# Deploy specific metadata
sfdx force:source:deploy -m "ApexClass:MyClass,LightningComponentBundle:myComponent" -u myorg

# Quick deploy (after validation)
sfdx force:source:deploy --validateddeployrequestid 0Af... -u myorg
```

### Tool 3: Salesforce CLI (sf - new)

```powershell
# Deploy source
sf project deploy start -d "force-app/main/default/classes" -o myorg

# Deploy with tests
sf project deploy start -d "force-app/main/default" -o myorg -l RunLocalTests

# Validate only
sf project deploy start -d "force-app/main/default" -o myorg --dry-run

# Deploy metadata
sf project deploy start -m "ApexClass:MyClass" -o myorg
```

## Deployment Patterns

### Pattern 1: Apex Class Deployment

```powershell
# Single class
.\sfsync.ps1 -type apex -pattern "MyService" -action push -org myorg

# Class family (recommended)
.\sfsync.ps1 -type apex -pattern "MyService*" -action push -org myorg

# Multiple related classes
.\sfsync.ps1 -type apex -pattern "My*" -action push -org myorg

# All Apex
.\sfsync.ps1 -type apex -action push -org myorg
```

### Pattern 2: LWC Component Deployment

```powershell
# Single component (with parents)
.\sfsync.ps1 -type lwc -pattern "myComponent*" -action push -org myorg

# Component family
.\sfsync.ps1 -type lwc -pattern "my*" -action push -org myorg

# All LWC
.\sfsync.ps1 -type lwc -action push -org myorg
```

### Pattern 3: Custom Object Deployment

```powershell
# Single object with all fields
.\sfsync.ps1 -type object -pattern "MyObject__c" -action push -org myorg

# Single field
sfdx force:source:deploy -p "force-app/main/default/objects/MyObject__c/fields/MyField__c.field-meta.xml" -u myorg

# Object family
.\sfsync.ps1 -type object -pattern "My*__c" -action push -org myorg
```

### Pattern 4: Full Deployment

```powershell
# Deploy everything
.\sfsync.ps1 -type all -action push -org myorg

# Deploy with validation
sfdx force:source:deploy -p "force-app/main/default" -u myorg --checkonly

# Deploy after validation passes
sfdx force:source:deploy -p "force-app/main/default" -u myorg -l RunLocalTests
```

## Deployment Strategies

### Strategy 1: Incremental Deployment

Deploy small changes frequently to reduce risk.

```powershell
# 1. Deploy modified class and dependencies
.\sfsync.ps1 -type apex -pattern "MyService*" -action push -org myorg

# 2. Verify deployment
sfdx force:data:soql:query -q "SELECT Id, Name FROM MyObject__c LIMIT 1" -u myorg

# 3. Test functionality
# Manual testing or automated tests

# 4. Deploy next change
```

### Strategy 2: Validation Before Deployment

Always validate before deploying to production.

```powershell
# 1. Validate deployment
sfdx force:source:deploy -p "force-app/main/default" -u prod --checkonly -l RunLocalTests

# 2. Review validation results
# Check for errors, test failures, code coverage

# 3. Quick deploy using validation ID
sfdx force:source:deploy --validateddeployrequestid 0Af... -u prod
```

### Strategy 3: Test Execution Levels

```powershell
# No tests (sandbox only)
sfdx force:source:deploy -p "force-app/main/default" -u sandbox -l NoTestRun

# Run specified tests
sfdx force:source:deploy -p "force-app/main/default" -u sandbox -l RunSpecifiedTests -r "MyClassTest,MyServiceTest"

# Run local tests (classes in package)
sfdx force:source:deploy -p "force-app/main/default" -u prod -l RunLocalTests

# Run all tests (production only)
sfdx force:source:deploy -p "force-app/main/default" -u prod -l RunAllTestsInOrg
```

## Common Deployment Scenarios

### Scenario 1: Modified Apex Service Class

```powershell
# Modified: MyService.cls
# Calls: MyServiceHelper.cls
# Called by: MyController.cls, MyApi.cls

# Deploy all related classes
.\sfsync.ps1 -type apex -pattern "MyService*,MyController,MyApi" -action push -org myorg

# Or use wildcard
.\sfsync.ps1 -type apex -pattern "My*" -action push -org myorg
```

### Scenario 2: Modified LWC Component

```powershell
# Modified: myChildComponent
# Used by: myParentComponent, myContainerComponent

# Deploy child and all parents
.\sfsync.ps1 -type lwc -pattern "my*Component" -action push -org myorg
```

### Scenario 3: New Custom Field

```powershell
# Created: MyObject__c.NewField__c

# Deploy field
sfdx force:source:deploy -p "force-app/main/default/objects/MyObject__c/fields/NewField__c.field-meta.xml" -u myorg

# Update page layouts if needed
sfdx force:source:deploy -p "force-app/main/default/layouts" -u myorg

# Update profiles/permission sets for FLS
sfdx force:source:deploy -p "force-app/main/default/profiles" -u myorg
```

### Scenario 4: Trigger Modification

```powershell
# Modified: MyObjectTrigger.trigger
# Uses: MyObjectTriggerHandler.cls

# Deploy trigger and handler
.\sfsync.ps1 -type apex -pattern "MyObject*" -action push -org myorg

# Or deploy individually
sfdx force:source:deploy -m "ApexTrigger:MyObjectTrigger,ApexClass:MyObjectTriggerHandler" -u myorg
```

## Deployment Troubleshooting

### Issue 1: "Changes not appearing after deployment"

**Cause:** Cache not invalidated

**Solution:** Deploy calling classes

```powershell
# Deploy entire call chain
.\sfsync.ps1 -type apex -pattern "MyService*,MyApi*,MyController*" -action push -org myorg
```

### Issue 2: "Test failures during deployment"

**Cause:** Tests dependent on specific data or state

**Solution:** Fix tests or use @TestSetup

```apex
@TestSetup
static void setupTestData() {
    // Create test data that persists across test methods
}
```

### Issue 3: "Code coverage below 75%"

**Cause:** Missing test coverage

**Solution:** Add test classes

```powershell
# Check coverage
sfdx force:apex:test:run -u myorg -c -r human

# Deploy tests first
.\sfsync.ps1 -type apex -pattern "*Test" -action push -org myorg

# Then deploy classes
.\sfsync.ps1 -type apex -pattern "MyService*" -action push -org myorg
```

### Issue 4: "Dependent class is invalid"

**Cause:** Dependency not deployed

**Solution:** Deploy dependencies first

```powershell
# Deploy in order
.\sfsync.ps1 -type apex -pattern "MyBaseClass" -action push -org myorg
.\sfsync.ps1 -type apex -pattern "MyDerivedClass" -action push -org myorg

# Or deploy all together
.\sfsync.ps1 -type apex -pattern "My*" -action push -org myorg
```

## Deployment Best Practices

### 1. Always Deploy Related Components

```powershell
# ✅ GOOD - Deploy family
.\sfsync.ps1 -type apex -pattern "Project*" -action push -org myorg

# ❌ BAD - Deploy single class
.\sfsync.ps1 -type apex -pattern "ProjectService" -action push -org myorg
```

### 2. Use Wildcards for Related Classes

```powershell
# Deploy all classes starting with "cmn_ContextLifecycle"
.\sfsync.ps1 -type apex -pattern "cmn_ContextLifecycle*" -action push -org myorg

# This deploys:
# - cmn_ContextLifecycleService
# - cmn_ContextLifecycleServiceExtensions
# - cmn_ContextLifecycleApi
# - cmn_ContextLifecycleController
```

### 3. Validate Before Production Deployment

```powershell
# 1. Deploy to sandbox
.\sfsync.ps1 -type all -action push -org sandbox

# 2. Test in sandbox
# Manual or automated testing

# 3. Validate in production
sfdx force:source:deploy -p "force-app/main/default" -u prod --checkonly -l RunLocalTests

# 4. Quick deploy
sfdx force:source:deploy --validateddeployrequestid 0Af... -u prod
```

### 4. Deploy Tests First

```powershell
# 1. Deploy test classes
.\sfsync.ps1 -type apex -pattern "*Test" -action push -org myorg

# 2. Deploy implementation classes
.\sfsync.ps1 -type apex -pattern "MyService*" -action push -org myorg
```

### 5. Use Deployment Validation

```powershell
# Check deployment without committing
sfdx force:source:deploy -p "force-app/main/default" -u myorg --checkonly

# Review results before actual deployment
```

## Deployment Checklist

### Pre-Deployment
- ✅ Code reviewed and approved
- ✅ All tests passing locally
- ✅ Code coverage > 75%
- ✅ No hardcoded IDs or credentials
- ✅ Dependencies identified
- ✅ Deployment order planned

### During Deployment
- ✅ Deploy to sandbox first
- ✅ Run all tests
- ✅ Verify functionality
- ✅ Check debug logs for errors
- ✅ Validate in production (checkonly)
- ✅ Deploy to production

### Post-Deployment
- ✅ Verify deployment success
- ✅ Run smoke tests
- ✅ Check for errors in debug logs
- ✅ Verify cache invalidation (changes visible)
- ✅ Update documentation
- ✅ Notify stakeholders

## Deployment Commands Quick Reference

```powershell
# Apex
.\sfsync.ps1 -type apex -pattern "MyClass*" -action push -org myorg

# LWC
.\sfsync.ps1 -type lwc -pattern "myComponent" -action push -org myorg

# Objects
.\sfsync.ps1 -type object -pattern "MyObject__c" -action push -org myorg

# All metadata
.\sfsync.ps1 -type all -action push -org myorg

# Validate only
sfdx force:source:deploy -p "force-app/main/default" -u myorg --checkonly

# With tests
sfdx force:source:deploy -p "force-app/main/default" -u myorg -l RunLocalTests

# Quick deploy
sfdx force:source:deploy --validateddeployrequestid 0Af... -u myorg

# Pull from org
.\sfsync.ps1 -type apex -pattern "MyClass" -action pull -org myorg
```

## Environment-Specific Patterns

### Development (Sandbox)
```powershell
# Fast deployment, no tests
.\sfsync.ps1 -type all -action push -org dev
```

### QA/UAT (Sandbox)
```powershell
# Deploy with local tests
sfdx force:source:deploy -p "force-app/main/default" -u qa -l RunLocalTests
```

### Production
```powershell
# 1. Validate
sfdx force:source:deploy -p "force-app/main/default" -u prod --checkonly -l RunLocalTests

# 2. Quick deploy
sfdx force:source:deploy --validateddeployrequestid 0Af... -u prod
```

## Related Skills
- `skill_salesforce_development.md` - General Salesforce patterns
- `skill_apex_testing.md` - Test class patterns
- `skill_lwc_development.md` - LWC component patterns
- `skill_git_version_control.md` - Version control for deployments
