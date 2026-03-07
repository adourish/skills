# Skill: Copado Deployments

**Category**: development  
**Priority**: HIGH  
**Last Updated**: March 3, 2026  
**Prerequisites**:
- `skill_copado_user_stories.md`
- Copado license or Release Manager access
- Understanding of Salesforce environments

---

## Overview

Copado Deployments manage the promotion of metadata through the deployment pipeline (Dev → QA → UAT → Production). This skill covers deployment validation, execution, monitoring, rollback procedures, and handling deployment failures.

## When to Use This Skill

- Promoting User Stories from one environment to another
- Validating deployments before production
- Monitoring deployment progress and status
- Handling deployment failures and errors
- Rolling back failed deployments
- Scheduling production deployments

## Prerequisites

- Completed User Story with committed metadata
- Target environment configured in Copado
- Appropriate permissions for target environment
- Change control approval (for production)

## Core Concepts

### Deployment Types

**Validation Deployment (Dry Run)**
- Tests deployment without making changes
- Runs all Apex tests
- Checks for errors and conflicts
- Required before production deployment
- No metadata changes applied

**Full Deployment**
- Applies metadata changes to target environment
- Runs tests based on test level
- Updates target environment
- Cannot be undone (requires rollback)

### Deployment Pipeline

```
Dev Sandbox (Development)
    ↓
QA (Quality Assurance Testing)
    ↓
UAT (User Acceptance Testing)
    ↓
Production (Live Environment)
```

### Test Levels

- **NoTestRun**: No tests (sandbox only)
- **RunSpecifiedTests**: Run specific test classes
- **RunLocalTests**: Run all tests in org (except managed packages)
- **RunAllTestsInOrg**: Run all tests including managed packages

### Deployment Status

- **Queued**: Waiting to start
- **In Progress**: Currently deploying
- **Completed**: Successfully deployed
- **Failed**: Deployment failed with errors
- **Cancelled**: Manually cancelled

---

## Step-by-Step Instructions

### Task 1: Validate Deployment (Dry Run)

**Objective**: Test deployment without making changes to target environment

**Steps**:

1. **Open User Story**
   - Navigate to User Stories tab
   - Click on completed User Story (e.g., US-1234)

2. **Click Promote**
   - Scroll to "Promotion" section
   - Click "Promote" button
   - Select target environment (e.g., "QA")

3. **Select Validation Mode**
   - Check "Validate Only" checkbox
   - Select test level: "RunLocalTests"
   - Review deployment components

4. **Start Validation**
   - Click "Validate Deployment" button
   - Wait for validation to queue

5. **Monitor Validation**
   - Click "View Deployment" link
   - Monitor progress bar
   - Review real-time logs

**Expected Output**:
```
Validation Status: In Progress
Components: 5
Tests Running: 12
Estimated Time: 3-5 minutes
```

6. **Review Results**
   - Wait for completion
   - Check validation status: "Completed" or "Failed"
   - Review test results
   - Check code coverage (must be ≥75%)

**Success Criteria**:
- Validation Status: Completed
- All tests passed
- Code coverage ≥75%
- No deployment errors

---

### Task 2: Execute Full Deployment

**Objective**: Deploy metadata to target environment

**Steps**:

1. **Verify Validation Passed**
   - Ensure validation completed successfully
   - Review validation results
   - Confirm no errors or warnings

2. **Open User Story**
   - Navigate to User Stories tab
   - Click on User Story (US-1234)

3. **Click Promote**
   - Click "Promote" button
   - Select target environment (e.g., "QA")

4. **Configure Deployment**
   - **Uncheck** "Validate Only" (for full deployment)
   - Select test level:
     - QA/UAT: "RunLocalTests"
     - Production: "RunLocalTests" (REQUIRED)
   - Review deployment components

5. **Execute Deployment**
   - Click "Deploy" button
   - Confirm deployment in popup
   - Wait for deployment to queue

6. **Monitor Deployment**
   - Click "View Deployment" link
   - Monitor progress bar (0% → 100%)
   - Review real-time logs
   - Watch for errors

**Expected Output**:
```
Deployment Status: In Progress
Components Deployed: 2/5
Tests Passed: 8/12
Current Step: Running Apex Tests
Estimated Time Remaining: 2 minutes
```

7. **Verify Deployment Success**
   - Wait for status: "Completed"
   - Review deployment summary
   - Check all components deployed
   - Verify all tests passed

**Success Criteria**:
- Deployment Status: Completed
- All components deployed successfully
- All tests passed
- No errors in logs

---

### Task 3: Monitor Deployment Progress

**Objective**: Track deployment status and identify issues early

**Real-Time Monitoring**:

1. **Access Deployment Record**
   - From User Story: Click "View Deployment"
   - From Deployments tab: Click deployment name

2. **Monitor Progress Bar**
   - 0-25%: Preparing deployment
   - 25-50%: Deploying components
   - 50-75%: Running tests
   - 75-100%: Finalizing deployment

3. **Review Deployment Logs**
   - Scroll to "Deployment Log" section
   - Watch for real-time updates
   - Look for errors or warnings

**Log Indicators**:
```
✓ Component deployed: ApexClass/bphc_ProjectService
✓ Component deployed: LightningComponentBundle/bphc_ProjectsModal
⚠ Warning: Test coverage below 75% for ApexClass/bphc_ProjectService
✗ Error: Test failure in bphc_ProjectServiceTest.testValidation
```

4. **Check Test Results**
   - Expand "Test Results" section
   - Review passed/failed tests
   - Check code coverage percentage
   - Identify failing test methods

5. **Monitor Time Remaining**
   - Check "Estimated Time Remaining"
   - Typical times:
     - QA: 3-5 minutes
     - UAT: 5-7 minutes
     - Production: 7-10 minutes

---

### Task 4: Handle Deployment Failures

**Objective**: Diagnose and resolve deployment errors

**Common Failure Scenarios**:

#### Scenario 1: Test Failure

**Symptom**:
```
Deployment Status: Failed
Error: Test failure in bphc_ProjectServiceTest.testValidation
Message: System.AssertException: Assertion Failed: Expected 1, Actual 0
```

**Solution**:
1. Review failing test in deployment logs
2. Identify root cause (code bug vs. test bug)
3. Fix issue in Dev Sandbox
4. Recommit metadata to User Story
5. Re-validate deployment
6. Re-deploy

**Commands**:
```bash
# Pull latest code
git pull origin dev

# Fix test in local environment
# Edit: force-app/main/default/classes/bphc_ProjectServiceTest.cls

# Deploy fix to Dev Sandbox
sfdx force:source:deploy -p force-app/main/default/classes/bphc_ProjectServiceTest.cls -u dmedev5

# Run tests locally
sfdx force:apex:test:run -n bphc_ProjectServiceTest -u dmedev5 -r human

# Recommit to Copado User Story
# Via Copado UI: User Story → Commit Changes → Select Test Class → Commit
```

#### Scenario 2: Missing Dependency

**Symptom**:
```
Deployment Status: Failed
Error: In field: field - no CustomField named Project__c found
Component: LightningComponentBundle/bphc_ProjectsModal
```

**Solution**:
1. Identify missing dependency (Project__c field)
2. Add dependency to User Story
3. Recommit metadata including dependency
4. Re-validate and re-deploy

**Steps**:
1. Open User Story in Copado
2. Click "Commit Changes"
3. Expand "CustomField" metadata type
4. Select missing field: `bphc_Project_Items__c.Project__c`
5. Commit with message: "Added missing dependency: Project__c field"
6. Re-validate deployment

#### Scenario 3: Code Coverage Below 75%

**Symptom**:
```
Deployment Status: Failed
Error: Average test coverage across all Apex Classes is 72%, at least 75% test coverage is required
```

**Solution**:
1. Identify classes with low coverage
2. Add test methods to increase coverage
3. Deploy updated tests to Dev Sandbox
4. Recommit to User Story
5. Re-validate

**Coverage Report**:
```
bphc_ProjectService: 68% (needs 7% more)
bphc_ActivityService: 82% (OK)
bphc_ReviewService: 71% (needs 4% more)
```

**Fix**:
```apex
// Add test methods to bphc_ProjectServiceTest
@isTest
static void testAdditionalScenarios() {
    // Test edge cases to increase coverage
    bphc_ProjectService service = new bphc_ProjectService();
    
    // Test scenario 1
    service.validateBudget(null);
    
    // Test scenario 2
    service.validateDates(Date.today(), Date.today().addDays(-1));
    
    // Test scenario 3
    service.handleException(new DmlException());
}
```

#### Scenario 4: Deployment Timeout

**Symptom**:
```
Deployment Status: Failed
Error: Deployment timed out after 300 seconds
```

**Solution**:
1. Check deployment size (too many components)
2. Split into smaller deployments
3. Increase timeout in Copado settings (admin only)
4. Retry deployment

**Split Strategy**:
```
Original User Story (US-1234): 50 components
  ↓ Split into:
US-1234-Part1: Apex Classes (20 components)
US-1234-Part2: LWC Components (15 components)
US-1234-Part3: Objects & Fields (15 components)
```

---

### Task 5: Schedule Production Deployment

**Objective**: Plan and execute production deployment during maintenance window

**Planning Steps**:

1. **Select Deployment Window**
   - Preferred: Tuesday-Thursday 6:00-8:00 PM EST
   - Avoid: Friday, Monday, holidays
   - Duration: 1-2 hours

2. **Create Change Control Ticket**
   - Title: "Copado Deployment: US-1234 Project Validation"
   - Description: Components, test results, rollback plan
   - Approvers: Tech Lead, Product Owner, Ops Manager
   - Submit 48 hours in advance

3. **Notify Stakeholders**
   - Email: team@example.com
   - Subject: "Production Deployment: [Date] [Time]"
   - Include: User Stories, expected downtime, rollback plan

4. **Pre-Deployment Checklist**
   - [ ] Validation passed in UAT
   - [ ] All tests passed (75%+ coverage)
   - [ ] Change control approved
   - [ ] Stakeholders notified
   - [ ] Rollback plan documented
   - [ ] Deployment window scheduled
   - [ ] Team members on standby

**Execution Steps**:

1. **5:45 PM - Pre-Deployment**
   - Log into Copado
   - Open User Story
   - Review validation results one more time

2. **6:00 PM - Start Deployment**
   - Click "Promote to Production"
   - Select "RunLocalTests"
   - Click "Deploy"
   - Monitor deployment progress

3. **6:05-6:15 PM - Monitor**
   - Watch deployment logs
   - Check for errors
   - Monitor test execution

4. **6:15 PM - Verify Success**
   - Confirm deployment completed
   - Review deployment summary
   - Check all components deployed

5. **6:20 PM - Smoke Tests**
   - Test critical functionality
   - Verify new features work
   - Check for regressions

6. **6:30 PM - Notify Completion**
   - Email stakeholders: "Deployment completed successfully"
   - Update change control ticket: "Closed - Success"
   - Document any issues encountered

**Rollback Trigger**:
If deployment fails or critical issues found:
1. Execute rollback immediately (see Task 6)
2. Notify stakeholders
3. Document failure reason
4. Schedule fix and re-deployment

---

### Task 6: Rollback Failed Deployment

**Objective**: Revert production to previous state after failed deployment

**When to Rollback**:
- Deployment failed with critical errors
- Production functionality broken
- Data corruption detected
- Critical bug discovered post-deployment

**Rollback Methods**:

#### Method 1: Copado Quick Rollback

**Use When**: Deployment just completed, no subsequent changes

**Steps**:
1. Navigate to Deployments tab
2. Find failed deployment
3. Click "Rollback" button
4. Confirm rollback
5. Monitor rollback progress
6. Verify production restored

**Timeline**: 5-10 minutes

#### Method 2: Manual Rollback via User Story

**Use When**: Need to rollback specific components

**Steps**:
1. Create new User Story: "ROLLBACK-US-1234"
2. Retrieve previous version from Git
3. Commit previous version to User Story
4. Validate deployment
5. Deploy to production
6. Verify rollback success

**Timeline**: 15-30 minutes

#### Method 3: Emergency Sandbox Refresh

**Use When**: Complete environment corruption

**Steps**:
1. Contact Salesforce support
2. Request sandbox refresh from production backup
3. Wait for refresh (1-2 hours)
4. Verify data integrity
5. Resume normal operations

**Timeline**: 2-4 hours

**Post-Rollback Actions**:
1. Document rollback reason
2. Update change control ticket
3. Notify stakeholders
4. Schedule post-mortem meeting
5. Fix root cause in Dev Sandbox
6. Re-test thoroughly
7. Schedule re-deployment

---

## Common Patterns

### Pattern 1: Standard Deployment Flow

```
1. Validate in QA (dry run)
2. Deploy to QA (full deployment)
3. QA testing (2-3 days)
4. Validate in UAT (dry run)
5. Deploy to UAT (full deployment)
6. UAT testing (3-5 days)
7. Validate in Production (dry run)
8. Deploy to Production (scheduled window)
9. Smoke tests
10. Monitor for 24 hours
```

### Pattern 2: Hotfix Deployment

```
1. Create HOTFIX User Story
2. Validate in QA (same day)
3. Deploy to QA (same day)
4. Quick QA test (2 hours)
5. Validate in Production (dry run)
6. Emergency change control approval
7. Deploy to Production (off-hours)
8. Verify fix immediately
9. Monitor closely for 48 hours
```

### Pattern 3: Bundle Deployment

```
1. Create deployment bundle (5-10 User Stories)
2. Validate bundle in QA
3. Deploy bundle to QA
4. QA regression testing (3-5 days)
5. Validate bundle in UAT
6. Deploy bundle to UAT
7. UAT regression testing (5-7 days)
8. Validate bundle in Production
9. Deploy bundle to Production (scheduled)
10. Full regression testing
```

---

## Troubleshooting

### Issue 1: Deployment Stuck "In Progress"

**Symptom**: Deployment running for >30 minutes

**Cause**: Salesforce processing delay, large deployment, test execution slow

**Solution**:
1. Wait 10 more minutes (Salesforce can be slow)
2. Check Salesforce system status: https://status.salesforce.com
3. If >45 minutes, contact Copado support
4. Do NOT cancel unless instructed

### Issue 2: Cannot Promote User Story

**Symptom**: "Promote" button disabled or greyed out

**Cause**: User Story not completed, missing permissions, environment not configured

**Solution**:
1. Check User Story status = "Completed"
2. Verify you have deployment permissions
3. Check target environment configured in Copado
4. Refresh page and try again

### Issue 3: Validation Passes but Deployment Fails

**Symptom**: Validation succeeds, but full deployment fails with same components

**Cause**: Environment changed between validation and deployment, timing issue

**Solution**:
1. Re-run validation immediately before deployment
2. Check for recent changes in target environment
3. Retrieve latest metadata from target
4. Merge any conflicts
5. Re-validate and re-deploy

---

## Best Practices

### Deployment Timing

**QA Deployments**:
- Anytime during business hours
- Daily deployments acceptable
- No approval required

**UAT Deployments**:
- Tuesday-Thursday mornings
- Weekly deployments recommended
- Product Owner approval required

**Production Deployments**:
- Tuesday-Thursday 6:00-8:00 PM EST
- Bi-weekly or monthly
- Full change control approval required
- Never on Fridays or before holidays

### Validation Strategy

**Always Validate Before Production**:
```
1. Validate in UAT (dry run)
2. Review validation results
3. Fix any issues
4. Re-validate until clean
5. Then deploy to production
```

**Never Skip Validation**:
- Saves time in long run
- Catches errors before production
- Required for compliance

### Test Execution

**QA/UAT**: RunLocalTests (faster, sufficient)
**Production**: RunLocalTests (REQUIRED, ensures quality)

**Never Use**: NoTestRun in production

### Deployment Size

**Optimal**: 5-15 components per deployment
**Maximum**: 50 components per deployment
**Large Deployments**: Split into multiple User Stories

### Monitoring

**During Deployment**:
- Watch logs continuously
- Check test results in real-time
- Be ready to rollback

**Post-Deployment**:
- Monitor for 1 hour immediately
- Check error logs daily for 1 week
- User feedback monitoring

---

## Related Skills

- `skill_copado_user_stories.md` - Creating and managing User Stories
- `skill_copado_rollback_procedures.md` - Detailed rollback strategies
- `skill_copado_promotion_paths.md` - Pipeline configuration
- `skill_copado_testing_strategies.md` - Test execution and coverage
- `skill_copado_troubleshooting.md` - Advanced troubleshooting

---

## References

- [Copado Deployments Documentation](https://docs.copado.com/articles/#!copado-ci-cd-publication/deployments)
- [Salesforce Deployment Best Practices](https://developer.salesforce.com/docs/atlas.en-us.daas.meta/daas/daas_deployment_best_practices.htm)
- [Copado Rollback Procedures](https://docs.copado.com/articles/#!copado-ci-cd-publication/rollback)
- TEG Copado Usage Recommendation (Internal)

---

**Skill Owner**: TEG Development Team  
**Last Validated**: March 3, 2026  
**Next Review**: April 1, 2026
