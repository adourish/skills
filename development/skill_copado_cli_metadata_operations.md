# Skill: Copado CLI Metadata Operations

**Category**: development  
**Priority**: HIGH  
**Last Updated**: March 3, 2026  
**Prerequisites**:
- `skill_copado_cli_installation.md`
- Copado CLI installed and authenticated
- Understanding of Salesforce metadata types

---

## Overview

The Copado CLI provides powerful commands for retrieving, deploying, and managing Salesforce metadata. This skill covers metadata operations including retrieve, deploy, compare, and conflict resolution using the command line.

## When to Use This Skill

- Retrieving metadata from Salesforce orgs
- Deploying metadata to target environments
- Comparing metadata between orgs
- Automating metadata operations
- Troubleshooting deployment issues
- Backing up metadata

## Prerequisites

- Copado CLI installed and configured
- Authenticated to source and target orgs
- Understanding of Salesforce metadata structure
- Familiarity with metadata types (Apex, LWC, Objects, etc.)

## Core Concepts

### Metadata Types

**Code Components**:
- ApexClass
- ApexTrigger
- ApexComponent
- ApexPage
- LightningComponentBundle

**Configuration**:
- CustomObject
- CustomField
- PermissionSet
- Profile
- CustomMetadata

**Automation**:
- Flow
- WorkflowRule
- ProcessBuilder
- ApprovalProcess

**UI Components**:
- Layout
- CustomTab
- CustomApplication
- FlexiPage

### Metadata Operations

**Retrieve**: Download metadata from org to local directory
**Deploy**: Upload metadata from local directory to org
**Compare**: Diff metadata between orgs or versions
**Validate**: Test deployment without applying changes
**Delete**: Remove metadata from org

### Deployment Options

**Test Levels**:
- NoTestRun (sandbox only)
- RunSpecifiedTests
- RunLocalTests
- RunAllTestsInOrg

**Deployment Modes**:
- Full deployment (apply changes)
- Validation only (dry run)
- Quick deploy (reuse validation)

---

## Step-by-Step Instructions

### Task 1: Retrieve Metadata from Org

**Objective**: Download Salesforce metadata to local directory

**Retrieve All Metadata**:

```bash
# Retrieve all metadata from org
copado metadata retrieve \
  --org dmedev5 \
  --output ./metadata \
  --all

# Expected: Downloads all metadata to ./metadata directory
```

**Retrieve Specific Metadata Type**:

```bash
# Retrieve all Apex classes
copado metadata retrieve \
  --org dmedev5 \
  --type ApexClass \
  --output ./metadata

# Retrieve all LWC components
copado metadata retrieve \
  --org dmedev5 \
  --type LightningComponentBundle \
  --output ./metadata
```

**Retrieve Specific Components**:

```bash
# Retrieve specific Apex class
copado metadata retrieve \
  --org dmedev5 \
  --type ApexClass \
  --name "bphc_ProjectService" \
  --output ./metadata

# Retrieve multiple components
copado metadata retrieve \
  --org dmedev5 \
  --type ApexClass \
  --name "bphc_ProjectService,bphc_ActivityService,bphc_ReviewService" \
  --output ./metadata
```

**Retrieve by Package**:

```bash
# Retrieve using package.xml
copado metadata retrieve \
  --org dmedev5 \
  --package ./manifest/package.xml \
  --output ./metadata
```

**Example package.xml**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
    <types>
        <members>bphc_ProjectService</members>
        <members>bphc_ActivityService</members>
        <name>ApexClass</name>
    </types>
    <types>
        <members>bphc_ProjectsModal</members>
        <members>bphc_ActivitiesTable</members>
        <name>LightningComponentBundle</name>
    </types>
    <version>59.0</version>
</Package>
```

**Expected Output**:
```
Retrieving metadata from dmedev5...
Retrieved: ApexClass/bphc_ProjectService.cls
Retrieved: ApexClass/bphc_ProjectService.cls-meta.xml
Retrieved: ApexClass/bphc_ActivityService.cls
Retrieved: ApexClass/bphc_ActivityService.cls-meta.xml
Metadata retrieved successfully to ./metadata
```

---

### Task 2: Deploy Metadata to Org

**Objective**: Upload metadata from local directory to Salesforce org

**Deploy All Metadata**:

```bash
# Deploy all metadata in directory
copado metadata deploy \
  --org qa \
  --source ./metadata

# Expected: Deploys all metadata to QA org
```

**Deploy Specific Type**:

```bash
# Deploy all Apex classes
copado metadata deploy \
  --org qa \
  --source ./metadata \
  --type ApexClass

# Deploy all LWC components
copado metadata deploy \
  --org qa \
  --source ./metadata \
  --type LightningComponentBundle
```

**Deploy Specific Components**:

```bash
# Deploy specific Apex class
copado metadata deploy \
  --org qa \
  --source ./metadata \
  --type ApexClass \
  --name "bphc_ProjectService"

# Deploy multiple components
copado metadata deploy \
  --org qa \
  --source ./metadata \
  --type ApexClass \
  --name "bphc_ProjectService,bphc_ActivityService"
```

**Deploy with Tests**:

```bash
# Deploy with local tests
copado metadata deploy \
  --org qa \
  --source ./metadata \
  --test-level RunLocalTests

# Deploy with specific tests
copado metadata deploy \
  --org qa \
  --source ./metadata \
  --test-level RunSpecifiedTests \
  --tests "bphc_ProjectServiceTest,bphc_ActivityServiceTest"
```

**Validate Deployment (Dry Run)**:

```bash
# Validate without deploying
copado metadata deploy \
  --org production \
  --source ./metadata \
  --validate-only \
  --test-level RunLocalTests

# Expected: Tests deployment without applying changes
```

**Quick Deploy (Reuse Validation)**:

```bash
# After successful validation, quick deploy
copado metadata deploy \
  --org production \
  --validation-id 0Af5w00000abcde \
  --quick-deploy

# Expected: Deploys immediately without re-running tests
```

**Expected Output**:
```
Deploying metadata to qa...
Deploying: ApexClass/bphc_ProjectService.cls
Deploying: ApexClass/bphc_ActivityService.cls
Running tests...
Test: bphc_ProjectServiceTest.testCreate - PASS
Test: bphc_ProjectServiceTest.testUpdate - PASS
Test: bphc_ActivityServiceTest.testValidation - PASS
Code Coverage: 87%
Deployment successful
Deployment ID: 0Af5w00000abcde
```

---

### Task 3: Compare Metadata Between Orgs

**Objective**: Identify differences in metadata between environments

**Compare All Metadata**:

```bash
# Compare all metadata between orgs
copado metadata diff \
  --source dmedev5 \
  --target qa

# Expected: Shows all differences
```

**Compare Specific Type**:

```bash
# Compare Apex classes only
copado metadata diff \
  --source dmedev5 \
  --target qa \
  --type ApexClass

# Compare LWC components
copado metadata diff \
  --source dmedev5 \
  --target qa \
  --type LightningComponentBundle
```

**Compare Specific Components**:

```bash
# Compare specific Apex class
copado metadata diff \
  --source dmedev5 \
  --target qa \
  --type ApexClass \
  --name "bphc_ProjectService"
```

**Output Format**:

```bash
# Output as JSON
copado metadata diff \
  --source dmedev5 \
  --target qa \
  --type ApexClass \
  --format json \
  --output ./diff-report.json

# Output as HTML
copado metadata diff \
  --source dmedev5 \
  --target qa \
  --format html \
  --output ./diff-report.html
```

**Expected Output**:
```
Comparing metadata between dmedev5 and qa...

ADDED (in dmedev5, not in qa):
  ApexClass/bphc_ReviewService.cls

MODIFIED (different between orgs):
  ApexClass/bphc_ProjectService.cls
    - Line 45: Added validation logic
    - Line 67: Updated error message

DELETED (in qa, not in dmedev5):
  ApexClass/bphc_LegacyService.cls

Summary:
  Added: 1
  Modified: 1
  Deleted: 1
  Total Differences: 3
```

---

### Task 4: Selective Metadata Deployment

**Objective**: Deploy only changed components

**Deploy Changed Files Only**:

```bash
# Get list of changed files from Git
git diff --name-only main..dev > changed-files.txt

# Deploy only changed files
copado metadata deploy \
  --org qa \
  --source ./force-app \
  --changed-files changed-files.txt
```

**Deploy by User Story**:

```bash
# Retrieve metadata for specific User Story
copado metadata retrieve \
  --org dmedev5 \
  --user-story US-1234 \
  --output ./metadata

# Deploy User Story metadata
copado metadata deploy \
  --org qa \
  --source ./metadata \
  --user-story US-1234
```

**Deploy Delta (Incremental)**:

```bash
# Deploy only changes since last deployment
copado metadata deploy \
  --org qa \
  --source ./force-app \
  --delta \
  --since "2026-03-01"
```

---

### Task 5: Metadata Backup and Restore

**Objective**: Create backups and restore metadata

**Create Backup**:

```bash
# Backup all metadata
copado metadata retrieve \
  --org production \
  --output ./backups/prod-$(date +%Y%m%d) \
  --all

# Backup specific types
copado metadata retrieve \
  --org production \
  --type "ApexClass,ApexTrigger,LightningComponentBundle" \
  --output ./backups/prod-code-$(date +%Y%m%d)
```

**Automated Backup Script** (PowerShell):

```powershell
# backup-metadata.ps1
param(
    [string]$Org = "production",
    [string]$BackupDir = "./backups"
)

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupPath = "$BackupDir/$Org-$timestamp"

Write-Host "Backing up metadata from $Org to $backupPath"

copado metadata retrieve `
    --org $Org `
    --output $backupPath `
    --all

if ($LASTEXITCODE -eq 0) {
    Write-Host "Backup completed successfully: $backupPath"
    
    # Compress backup
    Compress-Archive -Path $backupPath -DestinationPath "$backupPath.zip"
    Write-Host "Backup compressed: $backupPath.zip"
} else {
    Write-Error "Backup failed"
}
```

**Restore from Backup**:

```bash
# Restore all metadata
copado metadata deploy \
  --org dmedev5 \
  --source ./backups/prod-20260303 \
  --validate-only  # Test first

# If validation passes, deploy
copado metadata deploy \
  --org dmedev5 \
  --source ./backups/prod-20260303
```

---

## Common Patterns

### Pattern 1: Sync Dev to QA

```bash
# 1. Retrieve from Dev
copado metadata retrieve \
  --org dmedev5 \
  --type "ApexClass,LightningComponentBundle" \
  --output ./sync

# 2. Validate in QA
copado metadata deploy \
  --org qa \
  --source ./sync \
  --validate-only \
  --test-level RunLocalTests

# 3. Deploy to QA
copado metadata deploy \
  --org qa \
  --source ./sync \
  --test-level RunLocalTests
```

---

### Pattern 2: Emergency Hotfix

```bash
# 1. Retrieve current production state
copado metadata retrieve \
  --org production \
  --type ApexClass \
  --name "bphc_ProjectService" \
  --output ./hotfix

# 2. Make fix locally
# Edit: ./hotfix/classes/bphc_ProjectService.cls

# 3. Validate fix
copado metadata deploy \
  --org production \
  --source ./hotfix \
  --validate-only \
  --test-level RunLocalTests

# 4. Quick deploy
copado metadata deploy \
  --org production \
  --validation-id <validation-id> \
  --quick-deploy
```

---

### Pattern 3: Metadata Audit

```bash
# Compare all environments
copado metadata diff --source dev --target qa > dev-qa-diff.txt
copado metadata diff --source qa --target uat > qa-uat-diff.txt
copado metadata diff --source uat --target prod > uat-prod-diff.txt

# Generate audit report
cat dev-qa-diff.txt qa-uat-diff.txt uat-prod-diff.txt > audit-report.txt
```

---

## Troubleshooting

### Issue 1: Deployment Fails - Missing Dependency

**Symptom**:
```
Error: In field: field - no CustomField named Project__c found
```

**Cause**: Dependent metadata not included in deployment

**Solution**:

```bash
# 1. Identify dependencies
copado metadata analyze \
  --source ./metadata \
  --type ApexClass \
  --name "bphc_ProjectService"

# 2. Retrieve missing dependencies
copado metadata retrieve \
  --org dmedev5 \
  --type CustomField \
  --name "bphc_Project_Items__c.Project__c" \
  --output ./metadata

# 3. Deploy with dependencies
copado metadata deploy \
  --org qa \
  --source ./metadata \
  --include-dependencies
```

---

### Issue 2: Retrieve Timeout

**Symptom**:
```
Error: Request timeout after 300000ms
```

**Cause**: Large metadata retrieval, slow network

**Solution**:

```bash
# Increase timeout
copado metadata retrieve \
  --org dmedev5 \
  --type ApexClass \
  --output ./metadata \
  --timeout 900

# Or retrieve in batches
copado metadata retrieve --org dmedev5 --type ApexClass --output ./metadata/apex
copado metadata retrieve --org dmedev5 --type LightningComponentBundle --output ./metadata/lwc
copado metadata retrieve --org dmedev5 --type CustomObject --output ./metadata/objects
```

---

### Issue 3: Metadata Conflict

**Symptom**:
```
Error: Metadata conflict detected
Component modified in target org since last deployment
```

**Cause**: Concurrent changes in target org

**Solution**:

```bash
# 1. Retrieve latest from target
copado metadata retrieve \
  --org qa \
  --type ApexClass \
  --name "bphc_ProjectService" \
  --output ./latest

# 2. Compare with local
diff ./metadata/classes/bphc_ProjectService.cls ./latest/classes/bphc_ProjectService.cls

# 3. Merge manually
# Edit: ./metadata/classes/bphc_ProjectService.cls

# 4. Deploy merged version
copado metadata deploy \
  --org qa \
  --source ./metadata \
  --force  # Override conflict
```

---

## Best Practices

### Retrieval

- Always specify output directory
- Use `--type` to limit scope
- Retrieve dependencies together
- Create backups before major changes
- Use package.xml for complex retrievals

### Deployment

- Always validate before production
- Use appropriate test level
- Deploy small batches (5-15 components)
- Monitor deployment logs
- Keep deployment history

### Comparison

- Compare regularly (weekly)
- Document differences
- Investigate unexpected changes
- Use version control for tracking
- Generate audit reports

### Automation

- Script common operations
- Use CI/CD for deployments
- Schedule regular backups
- Log all operations
- Monitor for failures

### Security

- Never deploy without testing
- Use validation for production
- Require code review
- Track all deployments
- Maintain audit trail

---

## Related Skills

- `skill_copado_cli_installation.md` - CLI setup
- `skill_copado_user_stories.md` - User Story management
- `skill_copado_deployments.md` - Deployment execution
- `skill_copado_cli_cicd_integration.md` - CI/CD automation

---

## References

- [Copado CLI Metadata Commands](https://docs.copado.com/articles/#!copado-ci-cd-publication/copado-cli-metadata)
- [Salesforce Metadata API](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/)
- [Salesforce Metadata Types](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_types_list.htm)

---

**Skill Owner**: TEG Development Team  
**Last Validated**: March 3, 2026  
**Next Review**: April 1, 2026
