# Salesforce Cache Invalidation Strategy

**Last Updated:** March 2, 2026  
**Purpose:** Critical patterns for invalidating Salesforce compiled Apex cache to ensure code changes take effect  
**Success Rate:** Proven patterns from production development

---

## Table of Contents

1. [Overview](#overview)
2. [The Problem](#the-problem)
3. [Critical Pattern](#critical-pattern)
4. [Deployment Strategies](#deployment-strategies)
5. [Common Scenarios](#common-scenarios)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)
8. [Related Skills](#related-skills)

---

## Overview

Salesforce caches compiled Apex bytecode for performance. When you deploy a modified class, Salesforce does NOT automatically invalidate the compiled cache for classes that call it. This causes deployed changes to not take effect until the entire call chain is redeployed.

### Key Concept

**This is NOT a caching issue - it's a Salesforce compilation/dependency issue that requires deploying the full call chain.**

### When This Matters

- Modifying service classes called by APIs
- Updating extension classes used by base services
- Changing utility classes referenced by multiple components
- Deploying LWC components with parent-child relationships

---

## The Problem

### What Happens

```
You modify: cmn_ContextLifecycleServiceExtensions
You deploy: cmn_ContextLifecycleServiceExtensions only
Result: Changes don't appear in org
Reason: Compiled cache not invalidated for calling classes
```

### The Call Chain

```
cmn_ContextLifecycleApi (REST endpoint)
  └─> calls cmn_ContextLifecycleService
      └─> calls cmn_ContextLifecycleServiceExtensions (MODIFIED)
```

When you modify `cmn_ContextLifecycleServiceExtensions`, the compiled bytecode for `cmn_ContextLifecycleService` and `cmn_ContextLifecycleApi` still references the OLD version until they are redeployed.

---

## Critical Pattern

### The Rule

**When modifying a class, ALWAYS deploy:**

1. **The modified class** (what you changed)
2. **All classes that CALL it** (up the chain)
3. **All classes that it calls** (down the chain)

### Example: cmn_ContextLifecycleServiceExtensions

**Modified Class:**
- `cmn_ContextLifecycleServiceExtensions`

**Must Deploy:**
1. `cmn_ContextLifecycleServiceExtensions` (the modified class)
2. `cmn_ContextLifecycleService` (calls the Extensions class)
3. `cmn_ContextLifecycleApi` (REST API that calls the Service)
4. Any other classes that reference `cmn_ContextLifecycleServiceExtensions`

### Deployment Command

```powershell
# Deploy entire family using wildcard pattern
.\sfsync.ps1 -type apex -pattern "cmn_ContextLifecycle*" -action push -org dmedev5
```

**Why this works:** Deploys ALL classes in the call chain, forcing Salesforce to recompile the entire dependency tree.

---

## Deployment Strategies

### Strategy 1: Deploy Entire Family (Recommended)

Use wildcard patterns to deploy all related classes:

```powershell
# Deploy all ContextLifecycle classes
.\sfsync.ps1 -type apex -pattern "cmn_ContextLifecycle*" -action push -org dmedev5

# Deploy all Workflow classes
.\sfsync.ps1 -type apex -pattern "cmn_Workflow*" -action push -org dmedev5

# Deploy all Bundle classes
.\sfsync.ps1 -type apex -pattern "cfgHub_Bundle*" -action push -org dmedev5
```

**Pros:**
- Guarantees cache invalidation
- Simple and reliable
- No need to track dependencies manually

**Cons:**
- Deploys more classes than strictly necessary
- Slightly longer deployment time

### Strategy 2: Deploy Explicit Call Chain

Manually specify each class in the call chain:

```powershell
# Deploy modified class and all callers
sf project deploy start --source-dir "force-app\main\default\classes\cmn_ContextLifecycleServiceExtensions.cls" --target-org dmedev5
sf project deploy start --source-dir "force-app\main\default\classes\cmn_ContextLifecycleService.cls" --target-org dmedev5
sf project deploy start --source-dir "force-app\main\default\classes\cmn_ContextLifecycleApi.cls" --target-org dmedev5
```

**Pros:**
- Precise control over what gets deployed
- Minimal deployment footprint

**Cons:**
- Requires manual dependency tracking
- Error-prone if you miss a class
- More commands to execute

### Strategy 3: Deploy Multiple Families

When changes affect multiple families, deploy all of them:

```powershell
# Deploy common, BPHC, and config hub classes
.\sfsync.ps1 -type apex -pattern "cmn_*,bphc_*,cfgHub_*" -action push -org dmedev5
```

**Use when:**
- Modifying base classes used across domains
- Changing shared utilities or helpers
- Updating framework components

---

## Common Scenarios

### Scenario 1: Modified Service Extension

**What you changed:**
- `cmn_ContextLifecycleServiceExtensions.cls`

**What to deploy:**

```powershell
# Deploy entire ContextLifecycle family
.\sfsync.ps1 -type apex -pattern "cmn_ContextLifecycle*" -action push -org dmedev5
```

**Classes deployed:**
- `cmn_ContextLifecycleServiceExtensions` (modified)
- `cmn_ContextLifecycleService` (calls Extensions)
- `cmn_ContextLifecycleApi` (calls Service)
- `cmn_ContextLifecycleORA` (OmniStudio remote action)
- Any other `cmn_ContextLifecycle*` classes

### Scenario 2: Modified Base Service

**What you changed:**
- `cmn_BaseDataService.cls`

**What to deploy:**

```powershell
# Deploy base service
.\sfsync.ps1 -type apex -pattern "cmn_BaseDataService" -action push -org dmedev5

# Deploy all services that extend it
.\sfsync.ps1 -type apex -pattern "bphc_*Service" -action push -org dmedev5
.\sfsync.ps1 -type apex -pattern "cmn_*Service" -action push -org dmedev5
```

**Why:** All service classes that extend `cmn_BaseDataService` must be redeployed to pick up the changes.

### Scenario 3: Modified Utility Class

**What you changed:**
- `StringFormatHelper.cls`

**What to deploy:**

```powershell
# Find all classes that reference StringFormatHelper
# Then deploy them all

# Option 1: Deploy everything (safest)
.\sfsync.ps1 -type apex -pattern "*" -action push -org dmedev5

# Option 2: Deploy known families that use it
.\sfsync.ps1 -type apex -pattern "cmn_*,bphc_*,cfgHub_*" -action push -org dmedev5
```

### Scenario 4: Modified API Endpoint

**What you changed:**
- `cmn_ContextLifecycleApi.cls`

**What to deploy:**

```powershell
# Deploy API and the service it calls
.\sfsync.ps1 -type apex -pattern "cmn_ContextLifecycle*" -action push -org dmedev5
```

**Why:** Even though the API is at the top of the call chain, deploy the entire family to ensure consistency.

### Scenario 5: Modified DTO/Model Class

**What you changed:**
- `cmn_ValidationResultModel.cls`

**What to deploy:**

```powershell
# Deploy model and all classes that use it
.\sfsync.ps1 -type apex -pattern "cmn_*" -action push -org dmedev5
```

**Why:** DTOs are used across many classes. Deploy the entire domain to ensure all references are updated.

---

## Best Practices

### 1. Always Use Wildcard Patterns

```powershell
# ✅ CORRECT: Deploy entire family
.\sfsync.ps1 -type apex -pattern "cmn_ContextLifecycle*" -action push -org dmedev5

# ❌ WRONG: Deploy only modified class
.\sfsync.ps1 -type apex -pattern "cmn_ContextLifecycleServiceExtensions" -action push -org dmedev5
```

### 2. Deploy Before Testing

After any Apex modification:

```powershell
# 1. Deploy entire family
.\sfsync.ps1 -type apex -pattern "cmn_Workflow*" -action push -org dmedev5

# 2. Wait for deployment to complete

# 3. Test in org
sf org open --target-org dmedev5

# 4. Check debug logs
sf apex tail log --target-org dmedev5
```

### 3. Document Dependencies

In your class comments, document the call chain:

```apex
/**
 * Context Lifecycle Service Extensions
 * 
 * DEPLOYMENT NOTE: When modifying this class, ALWAYS deploy:
 * - cmn_ContextLifecycleServiceExtensions (this class)
 * - cmn_ContextLifecycleService (calls this class)
 * - cmn_ContextLifecycleApi (calls Service)
 * 
 * Use: .\sfsync.ps1 -type apex -pattern "cmn_ContextLifecycle*" -action push -org dmedev5
 */
public class cmn_ContextLifecycleServiceExtensions {
    // Implementation
}
```

### 4. Use Version Control

Track what you deployed:

```bash
# Before deployment
git add .
git commit -m "Modified cmn_ContextLifecycleServiceExtensions"

# Deploy
.\sfsync.ps1 -type apex -pattern "cmn_ContextLifecycle*" -action push -org dmedev5

# After successful deployment
git tag -a "deploy-contextlifecycle-$(Get-Date -Format 'yyyyMMdd-HHmm')" -m "Deployed ContextLifecycle family to dmedev5"
git push --tags
```

### 5. Test in Sandbox First

```powershell
# Deploy to sandbox
.\sfsync.ps1 -type apex -pattern "cmn_ContextLifecycle*" -action push -org sandbox

# Test thoroughly

# Then deploy to production
.\sfsync.ps1 -type apex -pattern "cmn_ContextLifecycle*" -action push -org production
```

### 6. Verify Deployment Success

```powershell
# Check deployment status
sf project deploy report --target-org dmedev5

# Verify in org
sf org open --target-org dmedev5

# Run tests
sf apex run test --class-names "cmn_ContextLifecycleService_Test" --result-format human --target-org dmedev5
```

---

## Troubleshooting

### Issue 1: Changes Still Don't Appear

**Problem:** Deployed entire family but changes still not visible.

**Solution:**

```powershell
# 1. Deploy again with explicit wait
sf project deploy start --source-dir "force-app\main\default\classes" --wait 10 --target-org dmedev5

# 2. Clear Salesforce cache
# Setup → Session Settings → Clear Cache

# 3. Hard refresh browser
# Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

# 4. Check debug logs for errors
sf apex tail log --target-org dmedev5
```

### Issue 2: Deployment Fails with Dependency Error

**Problem:** "This class is referenced by..." error.

**Solution:**

```powershell
# Deploy dependencies first, then the modified class
# Example: If modifying a service that uses a base class

# 1. Deploy base classes
.\sfsync.ps1 -type apex -pattern "cmn_Base*" -action push -org dmedev5

# 2. Deploy service classes
.\sfsync.ps1 -type apex -pattern "cmn_*Service" -action push -org dmedev5

# 3. Deploy API classes
.\sfsync.ps1 -type apex -pattern "cmn_*Api" -action push -org dmedev5
```

### Issue 3: Can't Identify All Callers

**Problem:** Don't know which classes call the modified class.

**Solution:**

```powershell
# Search codebase for references
Get-ChildItem -Path "force-app\main\default\classes" -Filter "*.cls" -Recurse | 
    Select-String -Pattern "cmn_ContextLifecycleServiceExtensions" |
    Select-Object -ExpandProperty Path -Unique

# Or use VS Code search
# Ctrl+Shift+F → Search for class name
```

### Issue 4: Too Many Classes to Deploy

**Problem:** Wildcard pattern matches too many classes.

**Solution:**

```powershell
# Use more specific patterns
# Instead of: cmn_*
# Use: cmn_ContextLifecycle*

# Or deploy in stages
.\sfsync.ps1 -type apex -pattern "cmn_ContextLifecycleService*" -action push -org dmedev5
.\sfsync.ps1 -type apex -pattern "cmn_ContextLifecycleApi*" -action push -org dmedev5
```

### Issue 5: LWC Changes Not Appearing

**Problem:** Lightning Web Component changes don't show after deployment.

**Solution:**

```powershell
# 1. Deploy child component
.\sfsync.ps1 -type lwc -pattern "cfgHub_BundleConfigurationFlow" -action push -org dmedev5

# 2. Deploy parent component (CRITICAL for cache-busting)
.\sfsync.ps1 -type lwc -pattern "cfgHub_BundleConfiguration" -action push -org dmedev5

# 3. Or deploy entire family
.\sfsync.ps1 -type lwc -pattern "cfgHub_Bundle*" -action push -org dmedev5

# 4. Hard refresh browser
# Ctrl+Shift+R
```

---

## Deployment Checklist

Use this checklist for every Apex deployment:

- [ ] Identify the modified class
- [ ] Identify all classes that call it (up the chain)
- [ ] Identify all classes it calls (down the chain)
- [ ] Determine the wildcard pattern (e.g., `cmn_ContextLifecycle*`)
- [ ] Deploy entire family using sfsync.ps1
- [ ] Wait for deployment to complete
- [ ] Verify deployment success
- [ ] Test in org
- [ ] Check debug logs for errors
- [ ] Commit deployment to version control

---

## Common Class Families

### Context Lifecycle Family

```powershell
.\sfsync.ps1 -type apex -pattern "cmn_ContextLifecycle*" -action push -org dmedev5
```

**Classes:**
- `cmn_ContextLifecycleService`
- `cmn_ContextLifecycleServiceExtensions`
- `cmn_ContextLifecycleApi`
- `cmn_ContextLifecycleORA`
- `cmn_ContextLifecycleDTO`
- `cmn_ContextLifecycleUrlHelper`

### Workflow Family

```powershell
.\sfsync.ps1 -type apex -pattern "cmn_Workflow*" -action push -org dmedev5
```

**Classes:**
- `cmn_WorkflowNode`
- `cmn_WorkflowTransitionMethods`
- `cmn_WorkflowService`
- `cmn_WorkflowApi`

### Bundle Configuration Family

```powershell
.\sfsync.ps1 -type apex -pattern "cfgHub_Bundle*" -action push -org dmedev5
```

**Classes:**
- `cfgHub_BundleDefinitionService`
- `cfgHub_BundleDefinitionApi`
- `cfgHub_BundleConfigurationController`

### BPHC Service Family

```powershell
.\sfsync.ps1 -type apex -pattern "bphc_*Service" -action push -org dmedev5
```

**Classes:**
- `bphc_ProjectService`
- `bphc_ActivityService`
- `bphc_GoalService`
- All other BPHC service classes

---

## Quick Reference

### Most Common Patterns

```powershell
# Context Lifecycle
.\sfsync.ps1 -type apex -pattern "cmn_ContextLifecycle*" -action push -org dmedev5

# Workflow
.\sfsync.ps1 -type apex -pattern "cmn_Workflow*" -action push -org dmedev5

# Bundle Configuration
.\sfsync.ps1 -type apex -pattern "cfgHub_Bundle*" -action push -org dmedev5

# All Common Classes
.\sfsync.ps1 -type apex -pattern "cmn_*" -action push -org dmedev5

# All BPHC Classes
.\sfsync.ps1 -type apex -pattern "bphc_*" -action push -org dmedev5

# Multiple Domains
.\sfsync.ps1 -type apex -pattern "cmn_*,bphc_*,cfgHub_*" -action push -org dmedev5
```

### Decision Tree

```
Modified a class?
  ├─> Is it part of a family? (e.g., cmn_ContextLifecycle*)
  │     └─> YES: Deploy entire family with wildcard
  │
  └─> Is it a standalone class?
        ├─> Does it have callers?
        │     └─> YES: Deploy class + all callers
        │
        └─> Is it a base/utility class?
              └─> YES: Deploy entire domain (cmn_*, bphc_*, etc.)
```

---

## Related Skills

### Development Skills
- **[skill_sfsync_deployment](skill_sfsync_deployment.md)** - sfsync.ps1 script usage
- **[skill_salesforce_development](skill_salesforce_development.md)** - Complete Salesforce development guide
- **[skill_salesforce_deployment](skill_salesforce_deployment.md)** - Deployment strategies
- **[skill_apex_testing](skill_apex_testing.md)** - Apex test patterns
- **[skill_lwc_development](skill_lwc_development.md)** - LWC cache-busting

### System Skills
- **[skill_git_version_control](skill_git_version_control.md)** - Git workflows
- **[skill_user_commands](../system/skill_user_commands.md)** - Quick command reference

---

## Success Metrics

- **Cache Hit Rate:** 100% of deployments should invalidate cache correctly
- **Deployment Success:** No "changes not appearing" issues after deployment
- **Time Saved:** Avoid 30-60 minutes of debugging cache issues
- **Consistency:** Standardized deployment process across team

---

## Maintenance

- Update this skill when discovering new cache invalidation patterns
- Document new class families as they are created
- Keep troubleshooting section current with real issues
- Review and update deployment checklist quarterly
