# Skill: Copado Promotion Paths

**Category**: development  
**Priority**: MEDIUM  
**Last Updated**: March 3, 2026  
**Prerequisites**:
- `skill_copado_user_stories.md`
- `skill_copado_deployments.md`
- Copado admin access (for configuration)

---

## Overview

Copado Promotion Paths define the deployment pipeline and quality gates for moving metadata through environments. This skill covers configuring promotion paths, managing approval processes, and understanding environment-branch mapping.

## When to Use This Skill

- Setting up new deployment pipelines
- Configuring quality gates and approvals
- Understanding environment flow
- Troubleshooting promotion issues
- Modifying deployment paths

## Prerequisites

- Copado admin or configuration access
- Understanding of Salesforce environments
- Knowledge of Git branching strategies
- Familiarity with deployment workflows

## Core Concepts

### Promotion Path Structure

A promotion path defines the sequence of environments and rules for deployments:

```
Source Environment → Quality Gates → Target Environment
```

**Example**:
```
Dev Sandbox → [Code Review Required] → QA
QA → [Testing Complete] → UAT
UAT → [Change Control Approved] → Production
```

### Environment Types

**Development Environments**:
- Dev Sandbox (individual or shared)
- Integration Sandbox
- Developer Orgs

**Testing Environments**:
- QA (Quality Assurance)
- UAT (User Acceptance Testing)
- Pre-Production

**Production Environments**:
- Production
- Production Mirror (read-only)

### Quality Gates

Quality gates are checkpoints that must pass before promotion:

- **Automated Tests**: Apex tests must pass
- **Code Coverage**: Minimum 75% required
- **Manual Approval**: Human review required
- **Validation**: Dry-run deployment must succeed
- **Change Control**: Ticket approval required

### Environment-Branch Mapping

Each environment maps to a Git branch:

```
Dev Sandbox → dev branch
QA → qa branch
UAT → uat branch
Production → main branch
```

---

## Step-by-Step Instructions

### Task 1: View Existing Promotion Paths

**Objective**: Understand current deployment pipeline configuration

**Steps**:

1. **Navigate to Copado Setup**
   - Click App Launcher → Copado
   - Click Setup tab
   - Select "Promotion Paths"

2. **View Promotion Path List**
   - See all configured paths
   - Note: "BPHC Salesforce Pipeline"
   - Check status: Active/Inactive

3. **Open Promotion Path**
   - Click "BPHC Salesforce Pipeline"
   - Review configuration

4. **Review Path Details**
   - **Source Environment**: Dev Sandbox
   - **Destination Environment**: QA
   - **Branch Mapping**: dev → qa
   - **Quality Gates**: Automated tests, code coverage
   - **Approval Required**: Yes/No

**Expected Configuration**:
```yaml
Promotion Path: BPHC Salesforce Pipeline

Step 1: Dev → QA
  Source: Dev Sandbox (dev branch)
  Target: QA (qa branch)
  Quality Gates:
    - Run Apex Tests: Yes
    - Minimum Coverage: 75%
    - Manual Approval: No
  Auto-Promote: No

Step 2: QA → UAT
  Source: QA (qa branch)
  Target: UAT (uat branch)
  Quality Gates:
    - Run Apex Tests: Yes
    - Minimum Coverage: 75%
    - Manual Approval: Yes (QA Lead)
  Auto-Promote: No

Step 3: UAT → Production
  Source: UAT (uat branch)
  Target: Production (main branch)
  Quality Gates:
    - Run Apex Tests: Yes (RunLocalTests)
    - Minimum Coverage: 75%
    - Validation Required: Yes
    - Manual Approval: Yes (Tech Lead, Product Owner)
    - Change Control: Required
  Auto-Promote: No
```

---

### Task 2: Configure New Promotion Path

**Objective**: Create deployment pipeline for new project

**Steps**:

1. **Create Promotion Path**
   - Navigate to Copado Setup → Promotion Paths
   - Click "New Promotion Path"
   - Name: "BPHC Hotfix Pipeline"
   - Description: "Fast-track pipeline for critical fixes"

2. **Configure Source Environment**
   - Source Environment: Dev Sandbox
   - Source Branch: dev
   - Git Repository: BPHC-Salesforce

3. **Configure Target Environment**
   - Target Environment: Production
   - Target Branch: main
   - Git Repository: BPHC-Salesforce

4. **Set Quality Gates**
   - Run Tests: Yes
   - Test Level: RunLocalTests
   - Minimum Coverage: 75%
   - Validation Required: Yes
   - Manual Approval: Yes

5. **Configure Approvers**
   - Add approver: Tech Lead
   - Add approver: Product Owner
   - Approval Type: All must approve

6. **Save Promotion Path**
   - Click "Save"
   - Activate: Check "Active"
   - Test: Create test User Story

---

### Task 3: Configure Quality Gates

**Objective**: Set up automated and manual quality checks

**Quality Gate Types**:

#### Automated Quality Gates

**Apex Test Execution**:
```yaml
Quality Gate: Run Apex Tests
Enabled: Yes
Test Level: RunLocalTests
Minimum Coverage: 75%
Failure Action: Block promotion
```

**Code Coverage Check**:
```yaml
Quality Gate: Code Coverage
Enabled: Yes
Minimum Percentage: 75%
Scope: All Apex Classes
Failure Action: Block promotion
```

**Validation Deployment**:
```yaml
Quality Gate: Validation Required
Enabled: Yes (Production only)
Validation Type: Full validation
Failure Action: Block promotion
```

#### Manual Quality Gates

**Code Review Approval**:
```yaml
Quality Gate: Code Review
Enabled: Yes
Approvers: Tech Lead, Senior Developer
Approval Type: Any one approver
Timeout: 48 hours
```

**QA Testing Approval**:
```yaml
Quality Gate: QA Sign-off
Enabled: Yes
Approvers: QA Lead
Approval Type: Required
Test Results: Must attach
```

**Change Control Approval**:
```yaml
Quality Gate: Change Control
Enabled: Yes (Production only)
Approvers: Tech Lead, Product Owner, Ops Manager
Approval Type: All must approve
Ticket Required: Yes
```

**Configuration Steps**:

1. Open Promotion Path
2. Click "Quality Gates" tab
3. Click "Add Quality Gate"
4. Select gate type (Automated/Manual)
5. Configure settings
6. Add approvers (if manual)
7. Set failure action
8. Save

---

### Task 4: Configure Approval Process

**Objective**: Set up multi-level approval workflow

**Approval Levels**:

**Level 1: Technical Approval**
- Approver: Tech Lead
- Criteria: Code quality, architecture, tests
- Timeline: 24 hours

**Level 2: QA Approval**
- Approver: QA Lead
- Criteria: Testing complete, no critical bugs
- Timeline: 48 hours

**Level 3: Business Approval**
- Approver: Product Owner
- Criteria: Requirements met, user acceptance
- Timeline: 48 hours

**Level 4: Operations Approval** (Production only)
- Approver: Ops Manager
- Criteria: Change control, deployment window
- Timeline: 24 hours

**Configuration**:

1. **Navigate to Approval Settings**
   - Open Promotion Path
   - Click "Approvals" tab

2. **Add Approval Level**
   - Click "Add Approval Level"
   - Name: "Technical Review"
   - Order: 1

3. **Configure Approvers**
   - Add User: Tech Lead
   - Add User: Senior Developer (backup)
   - Approval Type: Any one

4. **Set Approval Criteria**
   - Checklist:
     - [ ] Code follows standards
     - [ ] Tests pass (75%+ coverage)
     - [ ] No security vulnerabilities
     - [ ] Documentation updated

5. **Configure Notifications**
   - Email approvers when ready
   - Reminder after 24 hours
   - Escalate after 48 hours

6. **Repeat for Each Level**
   - Add QA approval (Level 2)
   - Add Business approval (Level 3)
   - Add Operations approval (Level 4)

---

### Task 5: Configure Auto-Promotion

**Objective**: Enable automatic deployments for specific paths

**When to Use Auto-Promotion**:
- Dev → QA (after tests pass)
- QA → UAT (after QA approval)
- Never for Production

**Configuration**:

1. **Open Promotion Path**
   - Navigate to "Dev → QA" path

2. **Enable Auto-Promotion**
   - Check "Auto-Promote" checkbox
   - Set conditions:
     - All tests passed
     - Code coverage ≥75%
     - No manual approval required

3. **Configure Schedule**
   - Promotion Time: Daily at 10:00 AM
   - Days: Monday-Friday
   - Skip on holidays: Yes

4. **Set Notifications**
   - Notify on success: Yes
   - Notify on failure: Yes
   - Recipients: Development team

5. **Test Auto-Promotion**
   - Create test User Story
   - Commit to Dev Sandbox
   - Verify auto-promotion to QA

**Best Practice**: Never auto-promote to Production

---

## Common Patterns

### Pattern 1: Standard 4-Tier Pipeline

```
Dev Sandbox
  ↓ [Auto: Tests pass]
QA
  ↓ [Manual: QA approval]
UAT
  ↓ [Manual: Business + Ops approval]
Production
```

**Use Case**: Standard feature development

---

### Pattern 2: Hotfix Pipeline

```
Dev Sandbox
  ↓ [Fast-track: Tests pass]
Production
  ↓ [Post-deployment]
Backport to QA/UAT
```

**Use Case**: Critical production fixes

---

### Pattern 3: Release Train Pipeline

```
Dev Sandbox
  ↓ [Daily auto-promotion]
Integration
  ↓ [Weekly bundle]
QA
  ↓ [Sprint end]
UAT
  ↓ [Release approval]
Production
```

**Use Case**: Large teams, coordinated releases

---

## Troubleshooting

### Issue 1: Promotion Blocked by Quality Gate

**Symptom**: Cannot promote User Story, quality gate failing

**Cause**: Tests failing, coverage low, approval missing

**Solution**:

1. **Check Quality Gate Status**
   - Open User Story
   - View "Quality Gates" section
   - Identify failing gate

2. **Fix Test Failures**
   ```bash
   # Run tests locally
   sfdx force:apex:test:run -u dmedev5 -r human
   
   # Fix failing tests
   # Redeploy to Dev Sandbox
   sfdx force:source:deploy -p force-app -u dmedev5
   
   # Recommit to User Story
   ```

3. **Request Approval**
   - If manual approval required
   - Notify approver via email/Slack
   - Provide approval checklist

---

### Issue 2: Environment Branch Mismatch

**Symptom**: Deployment fails, wrong branch selected

**Cause**: Promotion path misconfigured, branch mapping incorrect

**Solution**:

1. **Verify Branch Mapping**
   - Open Promotion Path
   - Check Source Branch = dev
   - Check Target Branch = qa

2. **Update Branch Mapping**
   - Edit Promotion Path
   - Correct branch names
   - Save changes

3. **Retry Promotion**
   - Open User Story
   - Click "Promote" again
   - Verify correct branches used

---

### Issue 3: Approval Timeout

**Symptom**: Promotion stuck waiting for approval >48 hours

**Cause**: Approver unavailable, notification not received

**Solution**:

1. **Check Approval Status**
   - Open User Story
   - View "Approvals" section
   - Identify pending approver

2. **Escalate Approval**
   - Contact approver directly
   - Use backup approver (if configured)
   - Request expedited review

3. **Override (Emergency Only)**
   - Contact Copado admin
   - Provide justification
   - Admin can override approval

---

## Best Practices

### Promotion Path Design

**Keep It Simple**:
- 3-4 environments maximum
- Clear progression: Dev → QA → UAT → Prod
- Avoid complex branching

**Quality Gates**:
- Always require tests for production
- Minimum 75% code coverage
- Manual approval for production
- Validation required for production

**Approvals**:
- Limit approvers (2-3 per level)
- Set reasonable timeouts (24-48 hours)
- Configure backup approvers
- Clear approval criteria

### Environment Strategy

**Development**:
- Shared Dev Sandbox (BPHC model)
- Auto-promote to QA (optional)
- No approval required

**Testing**:
- QA: Automated tests + QA approval
- UAT: Business approval required
- Pre-prod: Optional staging

**Production**:
- Always require validation
- Always require approval
- Always require change control
- Never auto-promote

### Branch Mapping

**Standard Mapping**:
```
dev → Dev Sandbox
qa → QA
uat → UAT
main → Production
```

**Feature Branches**:
```
feature/US-1234 → Dev Sandbox
  ↓ (merge to dev)
dev → QA
```

---

## Related Skills

- `skill_copado_user_stories.md` - Creating User Stories
- `skill_copado_deployments.md` - Executing deployments
- `skill_copado_branching_strategy.md` - Git branching
- `skill_copado_testing_strategies.md` - Test execution

---

## References

- [Copado Promotion Paths Documentation](https://docs.copado.com/articles/#!copado-ci-cd-publication/promotion-paths)
- [Copado Quality Gates](https://docs.copado.com/articles/#!copado-ci-cd-publication/quality-gates)
- [Copado Approvals](https://docs.copado.com/articles/#!copado-ci-cd-publication/approvals)
- TEG Copado Usage Recommendation (Internal)

---

**Skill Owner**: TEG Development Team  
**Last Validated**: March 3, 2026  
**Next Review**: April 1, 2026
