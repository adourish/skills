# Skill: Copado User Stories

**Category**: development  
**Priority**: HIGH  
**Last Updated**: March 3, 2026  
**Prerequisites**: 
- Salesforce org access
- Copado license (or access to Release Manager with license)
- Understanding of Salesforce metadata

---

## Overview

Copado User Stories are the primary mechanism for tracking and deploying Salesforce metadata changes through the Copado DevOps platform. This skill covers creating User Stories, committing metadata, managing status, and promoting changes through the deployment pipeline.

## When to Use This Skill

- After code has been approved in the intermediate Git repository
- When deploying metadata from Dev Sandbox to Copado
- When tracking feature development through the deployment pipeline
- When bundling multiple changes for coordinated deployment
- When promoting changes from QA → UAT → Production

## Prerequisites

- Copado license (single license holder model for BPHC)
- Dev Sandbox with deployed metadata
- Intermediate Git repository with approved Pull Request
- Understanding of dual-repository workflow

## Core Concepts

### User Story Lifecycle

1. **Created** - User Story initialized with title and description
2. **In Progress** - Metadata being committed from Dev Sandbox
3. **Completed** - All metadata committed, ready for promotion
4. **Deployed** - Successfully promoted through pipeline
5. **Cancelled** - User Story abandoned or rolled back

### User Story Components

- **Title**: Brief description (e.g., "US-1234: Project Validation Logic")
- **Description**: Detailed explanation of changes
- **Project**: Copado project for organization (e.g., "BPHC Modernization")
- **Sprint**: Optional sprint assignment
- **Base Branch**: Source environment (e.g., "dev")
- **Metadata Selection**: Components to commit (Apex, LWC, Objects, etc.)

### Relationship to Intermediate Repo

```
Intermediate Repo (feature/US-1234) 
  → PR Approved & Merged
  → Deploy to Dev Sandbox (SFDX)
  → Create Copado User Story (US-1234)
  → Commit Metadata to Copado
  → Promote through Pipeline
```

---

## Step-by-Step Instructions

### Task 1: Create User Story in Copado UI

**Objective**: Initialize a new User Story for tracking metadata deployment

**Steps**:

1. **Navigate to Copado**
   - Login to Salesforce org
   - Click App Launcher → Search "Copado"
   - Click "User Stories" tab

2. **Create New User Story**
   - Click "New" button
   - Fill in required fields:
     - **User Story Title**: `US-1234: Project Validation Logic`
     - **Project**: Select "BPHC Modernization"
     - **Sprint**: (Optional) Select current sprint
     - **Environment**: Select "Dev Sandbox"
     - **Base Branch**: `dev`

3. **Add Description**
   ```
   Implements project validation logic including:
   - Required field validation
   - Budget range validation
   - Date range validation
   - Cross-field validation rules
   
   Source: feature/US-1234-project-validation
   Intermediate Repo PR: #123
   ```

4. **Save User Story**
   - Click "Save"
   - Note the User Story ID (e.g., `US-00001234`)

**Expected Output**:
- User Story created with status "Draft"
- User Story ID assigned
- Ready for metadata commit

---

### Task 2: Commit Metadata from Dev Sandbox

**Objective**: Commit Salesforce metadata from Dev Sandbox to Copado Git repository

**Steps**:

1. **Open User Story**
   - Navigate to User Stories tab
   - Click on your User Story (US-1234)

2. **Click "Commit Changes"**
   - Scroll to "User Story Commit" section
   - Click "Commit Changes" button

3. **Select Metadata Components**
   - **Option A: Select All Changes**
     - Check "Select All" to commit all modified metadata
   
   - **Option B: Select Specific Components**
     - Expand metadata types (ApexClass, LightningComponentBundle, etc.)
     - Check specific components:
       - `ApexClass: bphc_ProjectService`
       - `ApexClass: bphc_ProjectServiceRules`
       - `ApexClass: bphc_ProjectServiceTest`
       - `LightningComponentBundle: bphc_ProjectsModal`

4. **Add Commit Message**
   ```
   US-1234: Project validation logic
   
   - Added required field validation
   - Added budget range validation
   - Added date range validation
   - Added cross-field validation rules
   - Added comprehensive test coverage
   ```

5. **Commit to Copado**
   - Click "Commit" button
   - Wait for commit to complete (30-60 seconds)
   - Verify commit success message

**Expected Output**:
```
Commit successful
User Story Status: In Progress
Committed Components: 5
Branch: feature/US-1234
```

---

### Task 3: Manage User Story Status

**Objective**: Update User Story status as work progresses

**Status Transitions**:

1. **Draft → In Progress**
   - Automatically set when first commit is made
   - Indicates active development

2. **In Progress → Completed**
   - Manually set when all commits are done
   - Click "Mark as Completed" button
   - Indicates ready for promotion

3. **Completed → Deployed**
   - Automatically set after successful production deployment
   - Indicates work is live

**Steps to Mark Complete**:

1. Open User Story
2. Verify all metadata committed
3. Click "Change Status" dropdown
4. Select "Completed"
5. Add completion notes (optional)
6. Click "Save"

---

### Task 4: Bundle Multiple User Stories

**Objective**: Group related User Stories for coordinated deployment

**When to Bundle**:
- Multiple features for same release
- Dependent changes across multiple stories
- Sprint-based deployments

**Steps**:

1. **Create Deployment Bundle**
   - Navigate to "Deployments" tab
   - Click "New Deployment"
   - Name: "Sprint 23 Release"

2. **Add User Stories**
   - Click "Add User Stories"
   - Select stories:
     - US-1234: Project Validation
     - US-1235: Activity Validation
     - US-1236: Review Workflow
   - Click "Add Selected"

3. **Review Bundle**
   - Verify all metadata components listed
   - Check for conflicts
   - Review deployment order

4. **Deploy Bundle**
   - Click "Deploy to QA"
   - Monitor deployment progress
   - Verify deployment success

---

### Task 5: Promote User Story Through Pipeline

**Objective**: Move User Story from Dev → QA → UAT → Production

**Promotion Path**:
```
Dev Sandbox → QA → UAT → Production
```

**Steps for Each Environment**:

1. **Promote to QA**
   - Open User Story
   - Click "Promote" button
   - Select "QA" environment
   - Click "Validate Deployment" (dry run)
   - Review validation results
   - Click "Deploy to QA"
   - Wait for deployment (2-5 minutes)
   - Verify deployment success

2. **Promote to UAT**
   - Wait for QA testing approval
   - Click "Promote" button
   - Select "UAT" environment
   - Click "Validate Deployment"
   - Review validation results
   - Click "Deploy to UAT"
   - Verify deployment success

3. **Promote to Production**
   - Wait for UAT testing approval
   - Obtain change control approval
   - Schedule deployment window
   - Click "Promote" button
   - Select "Production" environment
   - Click "Validate Deployment" (REQUIRED)
   - Review validation results carefully
   - Run all tests: `--test-level RunLocalTests`
   - Click "Deploy to Production"
   - Monitor deployment closely
   - Verify deployment success
   - Perform smoke tests

**Validation Checklist (Production)**:
- [ ] All Apex tests pass (75%+ coverage)
- [ ] No deployment errors
- [ ] No missing dependencies
- [ ] Change control ticket approved
- [ ] Deployment window scheduled
- [ ] Rollback plan documented
- [ ] Stakeholders notified

---

## Common Patterns

### Pattern 1: Single User Story Deployment

**Scenario**: Deploy one feature independently

```
1. Create User Story (US-1234)
2. Commit metadata from Dev Sandbox
3. Mark as Completed
4. Promote to QA
5. QA testing (2-3 days)
6. Promote to UAT
7. UAT testing (3-5 days)
8. Promote to Production
```

**Timeline**: 1-2 weeks

---

### Pattern 2: Sprint-Based Bundle Deployment

**Scenario**: Deploy multiple features together

```
1. Create multiple User Stories (US-1234, US-1235, US-1236)
2. Commit metadata for each story
3. Mark all as Completed
4. Create Deployment Bundle "Sprint 23"
5. Add all User Stories to bundle
6. Deploy bundle to QA
7. QA testing (3-5 days)
8. Deploy bundle to UAT
9. UAT testing (5-7 days)
10. Deploy bundle to Production
```

**Timeline**: 2-3 weeks

---

### Pattern 3: Hotfix Deployment

**Scenario**: Emergency production fix

```
1. Create User Story (HOTFIX-567)
2. Set Priority: Critical
3. Commit metadata from Dev Sandbox
4. Fast-track validation in QA (same day)
5. Fast-track validation in UAT (same day)
6. Emergency change control approval
7. Deploy to Production (off-hours)
8. Verify fix immediately
```

**Timeline**: 1-2 days

---

## Troubleshooting

### Issue 1: Commit Fails - "No Changes Detected"

**Symptom**: Copado reports no metadata changes when attempting commit

**Cause**: 
- Metadata not deployed to Dev Sandbox
- Copado cache not refreshed
- Wrong org selected

**Solution**:
```bash
# Verify deployment to Dev Sandbox
sfdx force:source:deploy -p force-app -u dmedev5 --verbose

# Refresh Copado metadata cache
# In Copado UI: User Story → Actions → Refresh Metadata

# Verify correct org
# Check User Story "Environment" field = "Dev Sandbox"
```

---

### Issue 2: Deployment Validation Fails

**Symptom**: Validation reports errors before deployment

**Cause**:
- Missing dependencies
- Test failures
- Insufficient code coverage
- Metadata conflicts

**Solution**:
```bash
# Review validation errors in Copado UI
# Common fixes:

# 1. Missing dependency
# Add missing component to User Story commit

# 2. Test failure
# Fix failing test in Dev Sandbox
# Recommit metadata

# 3. Low code coverage
# Add more test methods
# Ensure 75%+ coverage

# 4. Metadata conflict
# Retrieve latest from target org
# Merge conflicts manually
# Recommit
```

---

### Issue 3: User Story Stuck "In Progress"

**Symptom**: Cannot promote User Story, status stuck

**Cause**:
- Uncommitted changes in Dev Sandbox
- Incomplete metadata selection
- Copado workflow rule blocking

**Solution**:
1. Open User Story
2. Click "Commit Changes" again
3. Select any missing components
4. Commit again
5. Manually change status to "Completed"
6. If still blocked, contact Copado admin

---

### Issue 4: Single License Bottleneck

**Symptom**: Multiple developers waiting for license holder

**Cause**: Only one person can create User Stories

**Solution** (Release Manager Model):
```
1. Developers notify Release Manager when PR approved
2. Release Manager creates User Story daily (batch)
3. Release Manager commits all approved changes
4. Release Manager promotes through pipeline
5. Schedule: Daily at 10:00 AM
```

**Communication**:
- Slack channel: #copado-deployments
- Daily standup: Report approved PRs
- Deployment log: Track all User Stories

---

## Best Practices

### User Story Naming

**Good**:
- `US-1234: Add project validation logic`
- `US-1235: Fix activity date calculation`
- `HOTFIX-567: Critical budget field error`

**Bad**:
- `Update code` (too vague)
- `Changes` (no context)
- `Fix` (what fix?)

### Commit Messages

**Good**:
```
US-1234: Project validation logic

Added:
- Required field validation (Project_Title__c, Project_Type__c)
- Budget range validation ($1K - $10M)
- Date range validation (Start < End)
- Cross-field validation (Budget + Type)

Modified:
- bphc_ProjectService.cls
- bphc_ProjectServiceRules.cls
- bphc_ProjectServiceTest.cls

Tests:
- 95% code coverage
- All validation scenarios tested
```

**Bad**:
```
Updated files
```

### Metadata Selection

**Always Include**:
- Modified Apex classes
- Related test classes
- Modified LWC components
- Modified custom objects/fields
- Modified permission sets
- Modified flows/processes

**Never Forget**:
- Test classes (required for production)
- Dependencies (parent objects, lookups)
- Permission sets (for field access)

### Deployment Timing

**Best Times**:
- QA: Anytime during business hours
- UAT: Tuesday-Thursday mornings
- Production: Tuesday-Thursday 6:00-8:00 PM (off-hours)

**Avoid**:
- Production: Friday afternoons
- Production: Day before holidays
- Production: During peak business hours
- Production: Without proper testing

---

## Related Skills

- `skill_copado_deployments.md` - Deployment execution and monitoring
- `skill_copado_promotion_paths.md` - Pipeline configuration
- `skill_copado_dual_repo_workflow.md` - Complete workflow integration
- `skill_copado_rollback_procedures.md` - Rollback strategies
- `skill_copado_cli_metadata_operations.md` - CLI-based metadata management

---

## References

- [Copado User Stories Documentation](https://docs.copado.com/articles/#!copado-ci-cd-publication/user-stories)
- [Copado Commit Best Practices](https://docs.copado.com/articles/#!copado-ci-cd-publication/commit-best-practices)
- [Salesforce Metadata API](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/)
- TEG Copado Usage Recommendation (Internal)

---

**Skill Owner**: TEG Development Team  
**Last Validated**: March 3, 2026  
**Next Review**: April 1, 2026
