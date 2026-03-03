# Skill: Copado CLI CI/CD Integration

**Category**: automation  
**Priority**: MEDIUM  
**Last Updated**: March 3, 2026  
**Prerequisites**:
- `skill_copado_cli_installation.md`
- `skill_copado_cli_metadata_operations.md`
- Understanding of CI/CD concepts
- Access to CI/CD platform (GitHub Actions, Azure DevOps, GitLab)

---

## Overview

Integrating Copado CLI with CI/CD pipelines enables automated validation, testing, and deployment of Salesforce metadata. This skill covers GitHub Actions, Azure DevOps, and GitLab CI/CD integration patterns.

## When to Use This Skill

- Automating deployment validation on Pull Requests
- Running Apex tests automatically
- Deploying to QA/UAT on merge
- Implementing continuous integration
- Automating metadata backups
- Enforcing quality gates

## Prerequisites

- Copado CLI installed in CI environment
- CI/CD platform access (GitHub, Azure DevOps, GitLab)
- Copado service account with API access
- JWT authentication configured
- Repository with Salesforce metadata

## Core Concepts

### CI/CD Pipeline Stages

**Build Stage**:
- Install dependencies
- Authenticate to Copado
- Validate syntax

**Test Stage**:
- Run Apex tests
- Check code coverage
- Validate metadata

**Deploy Stage**:
- Deploy to target environment
- Run smoke tests
- Notify stakeholders

### Authentication Methods for CI/CD

**JWT (Recommended)**:
- Non-interactive authentication
- Service account
- Secure token storage

**Environment Variables**:
```
COPADO_CLIENT_ID
COPADO_JWT_KEY
COPADO_USERNAME
COPADO_INSTANCE_URL
```

### Quality Gates

- Apex test pass rate: 100%
- Code coverage: ≥75%
- No deployment errors
- No security vulnerabilities
- Metadata validation passes

---

## Step-by-Step Instructions

### Task 1: GitHub Actions Integration

**Objective**: Automate Copado operations with GitHub Actions

**Create Workflow File**:

`.github/workflows/copado-validate.yml`:

```yaml
name: Copado Validation

on:
  pull_request:
    branches: [main, dev]
    paths:
      - 'force-app/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install Copado CLI
        run: npm install -g @copado/cli
      
      - name: Authenticate to Copado
        env:
          COPADO_CLIENT_ID: ${{ secrets.COPADO_CLIENT_ID }}
          COPADO_JWT_KEY: ${{ secrets.COPADO_JWT_KEY }}
          COPADO_USERNAME: ${{ secrets.COPADO_USERNAME }}
        run: |
          echo "$COPADO_JWT_KEY" > server.key
          copado auth jwt \
            --client-id $COPADO_CLIENT_ID \
            --jwt-key-file ./server.key \
            --username $COPADO_USERNAME \
            --instance-url https://test.salesforce.com
      
      - name: Validate Deployment
        run: |
          copado metadata deploy \
            --org qa \
            --source ./force-app \
            --validate-only \
            --test-level RunLocalTests
      
      - name: Run Apex Tests
        run: |
          copado apex test run \
            --org qa \
            --test-level RunLocalTests \
            --output-dir ./test-results
      
      - name: Check Code Coverage
        run: |
          COVERAGE=$(copado apex test coverage --org qa --json | jq '.coverage')
          if [ $COVERAGE -lt 75 ]; then
            echo "Code coverage $COVERAGE% is below 75%"
            exit 1
          fi
      
      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: ./test-results
```

**Configure Secrets**:

1. Navigate to GitHub repo → Settings → Secrets
2. Add secrets:
   - `COPADO_CLIENT_ID`
   - `COPADO_JWT_KEY`
   - `COPADO_USERNAME`

**Deploy on Merge**:

`.github/workflows/copado-deploy.yml`:

```yaml
name: Deploy to QA

on:
  push:
    branches: [dev]
    paths:
      - 'force-app/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install Copado CLI
        run: npm install -g @copado/cli
      
      - name: Authenticate to Copado
        env:
          COPADO_CLIENT_ID: ${{ secrets.COPADO_CLIENT_ID }}
          COPADO_JWT_KEY: ${{ secrets.COPADO_JWT_KEY }}
          COPADO_USERNAME: ${{ secrets.COPADO_USERNAME }}
        run: |
          echo "$COPADO_JWT_KEY" > server.key
          copado auth jwt \
            --client-id $COPADO_CLIENT_ID \
            --jwt-key-file ./server.key \
            --username $COPADO_USERNAME \
            --instance-url https://test.salesforce.com
      
      - name: Deploy to QA
        run: |
          copado metadata deploy \
            --org qa \
            --source ./force-app \
            --test-level RunLocalTests
      
      - name: Notify Team
        if: success()
        run: |
          echo "Deployment to QA successful"
          # Add Slack/Teams notification here
```

---

### Task 2: Azure DevOps Integration

**Objective**: Integrate Copado CLI with Azure Pipelines

**Create Pipeline File**:

`azure-pipelines.yml`:

```yaml
trigger:
  branches:
    include:
      - main
      - dev
  paths:
    include:
      - force-app/**

pool:
  vmImage: 'ubuntu-latest'

variables:
  - group: copado-credentials

stages:
  - stage: Validate
    displayName: 'Validate Metadata'
    jobs:
      - job: ValidateJob
        displayName: 'Validate Deployment'
        steps:
          - task: NodeTool@0
            inputs:
              versionSpec: '18.x'
            displayName: 'Install Node.js'
          
          - script: npm install -g @copado/cli
            displayName: 'Install Copado CLI'
          
          - script: |
              echo "$(COPADO_JWT_KEY)" > server.key
              copado auth jwt \
                --client-id $(COPADO_CLIENT_ID) \
                --jwt-key-file ./server.key \
                --username $(COPADO_USERNAME) \
                --instance-url https://test.salesforce.com
            displayName: 'Authenticate to Copado'
          
          - script: |
              copado metadata deploy \
                --org qa \
                --source ./force-app \
                --validate-only \
                --test-level RunLocalTests
            displayName: 'Validate Deployment'
          
          - script: |
              copado apex test run \
                --org qa \
                --test-level RunLocalTests \
                --output-dir $(Build.ArtifactStagingDirectory)/test-results
            displayName: 'Run Apex Tests'
          
          - task: PublishTestResults@2
            inputs:
              testResultsFormat: 'JUnit'
              testResultsFiles: '$(Build.ArtifactStagingDirectory)/test-results/*.xml'
            displayName: 'Publish Test Results'

  - stage: Deploy
    displayName: 'Deploy to QA'
    dependsOn: Validate
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/dev'))
    jobs:
      - deployment: DeployJob
        displayName: 'Deploy to QA'
        environment: 'QA'
        strategy:
          runOnce:
            deploy:
              steps:
                - checkout: self
                
                - task: NodeTool@0
                  inputs:
                    versionSpec: '18.x'
                
                - script: npm install -g @copado/cli
                  displayName: 'Install Copado CLI'
                
                - script: |
                    echo "$(COPADO_JWT_KEY)" > server.key
                    copado auth jwt \
                      --client-id $(COPADO_CLIENT_ID) \
                      --jwt-key-file ./server.key \
                      --username $(COPADO_USERNAME) \
                      --instance-url https://test.salesforce.com
                  displayName: 'Authenticate to Copado'
                
                - script: |
                    copado metadata deploy \
                      --org qa \
                      --source ./force-app \
                      --test-level RunLocalTests
                  displayName: 'Deploy to QA'
```

**Configure Variable Group**:

1. Navigate to Azure DevOps → Pipelines → Library
2. Create variable group: `copado-credentials`
3. Add variables:
   - `COPADO_CLIENT_ID`
   - `COPADO_JWT_KEY` (mark as secret)
   - `COPADO_USERNAME`

---

### Task 3: GitLab CI/CD Integration

**Objective**: Automate Copado operations with GitLab CI/CD

**Create Pipeline File**:

`.gitlab-ci.yml`:

```yaml
image: node:18

variables:
  COPADO_INSTANCE_URL: "https://test.salesforce.com"

stages:
  - validate
  - test
  - deploy

before_script:
  - npm install -g @copado/cli
  - echo "$COPADO_JWT_KEY" > server.key
  - |
    copado auth jwt \
      --client-id $COPADO_CLIENT_ID \
      --jwt-key-file ./server.key \
      --username $COPADO_USERNAME \
      --instance-url $COPADO_INSTANCE_URL

validate:
  stage: validate
  script:
    - |
      copado metadata deploy \
        --org qa \
        --source ./force-app \
        --validate-only \
        --test-level RunLocalTests
  only:
    - merge_requests
    - dev
    - main

test:
  stage: test
  script:
    - |
      copado apex test run \
        --org qa \
        --test-level RunLocalTests \
        --output-dir ./test-results
    - |
      COVERAGE=$(copado apex test coverage --org qa --json | jq '.coverage')
      if [ $COVERAGE -lt 75 ]; then
        echo "Code coverage $COVERAGE% is below 75%"
        exit 1
      fi
  artifacts:
    reports:
      junit: test-results/*.xml
  only:
    - merge_requests
    - dev
    - main

deploy_qa:
  stage: deploy
  script:
    - |
      copado metadata deploy \
        --org qa \
        --source ./force-app \
        --test-level RunLocalTests
  only:
    - dev
  when: manual

deploy_production:
  stage: deploy
  script:
    - |
      copado metadata deploy \
        --org production \
        --source ./force-app \
        --validate-only \
        --test-level RunLocalTests
    - |
      copado metadata deploy \
        --org production \
        --validation-id $VALIDATION_ID \
        --quick-deploy
  only:
    - main
  when: manual
  environment:
    name: production
```

**Configure CI/CD Variables**:

1. Navigate to GitLab → Settings → CI/CD → Variables
2. Add variables:
   - `COPADO_CLIENT_ID`
   - `COPADO_JWT_KEY` (mark as protected and masked)
   - `COPADO_USERNAME`

---

### Task 4: Automated Testing Pipeline

**Objective**: Run comprehensive tests automatically

**Test Execution Script**:

`scripts/run-tests.sh`:

```bash
#!/bin/bash
set -e

ORG=${1:-qa}
OUTPUT_DIR=${2:-./test-results}

echo "Running Apex tests in $ORG..."

# Run all tests
copado apex test run \
  --org $ORG \
  --test-level RunLocalTests \
  --output-dir $OUTPUT_DIR \
  --format junit

# Check code coverage
COVERAGE=$(copado apex test coverage --org $ORG --json | jq '.coverage')
echo "Code coverage: $COVERAGE%"

if [ $COVERAGE -lt 75 ]; then
  echo "ERROR: Code coverage $COVERAGE% is below 75%"
  exit 1
fi

# Check for test failures
FAILURES=$(copado apex test results --org $ORG --json | jq '.failures')
if [ $FAILURES -gt 0 ]; then
  echo "ERROR: $FAILURES test(s) failed"
  exit 1
fi

echo "All tests passed with $COVERAGE% coverage"
```

**Integration in CI**:

```yaml
# GitHub Actions
- name: Run Tests
  run: ./scripts/run-tests.sh qa ./test-results

# Azure DevOps
- script: ./scripts/run-tests.sh qa $(Build.ArtifactStagingDirectory)/test-results
  displayName: 'Run Apex Tests'

# GitLab CI
script:
  - ./scripts/run-tests.sh qa ./test-results
```

---

### Task 5: Automated Deployment Pipeline

**Objective**: Deploy automatically on successful validation

**Deployment Script**:

`scripts/deploy.sh`:

```bash
#!/bin/bash
set -e

ORG=$1
SOURCE=${2:-./force-app}
TEST_LEVEL=${3:-RunLocalTests}

echo "Deploying to $ORG..."

# Validate first
echo "Validating deployment..."
VALIDATION_ID=$(copado metadata deploy \
  --org $ORG \
  --source $SOURCE \
  --validate-only \
  --test-level $TEST_LEVEL \
  --json | jq -r '.id')

echo "Validation ID: $VALIDATION_ID"

# Wait for validation
copado deployment status --id $VALIDATION_ID --wait

# Check validation result
STATUS=$(copado deployment status --id $VALIDATION_ID --json | jq -r '.status')

if [ "$STATUS" != "Completed" ]; then
  echo "ERROR: Validation failed with status: $STATUS"
  exit 1
fi

# Quick deploy using validation
echo "Deploying using validation $VALIDATION_ID..."
copado metadata deploy \
  --org $ORG \
  --validation-id $VALIDATION_ID \
  --quick-deploy

echo "Deployment successful"
```

**Usage in Pipeline**:

```yaml
# Deploy to QA
- name: Deploy to QA
  run: ./scripts/deploy.sh qa ./force-app RunLocalTests

# Deploy to Production
- name: Deploy to Production
  run: ./scripts/deploy.sh production ./force-app RunLocalTests
```

---

## Common Patterns

### Pattern 1: PR Validation

```yaml
on:
  pull_request:
    branches: [main, dev]

jobs:
  validate:
    steps:
      - Checkout code
      - Install Copado CLI
      - Authenticate
      - Validate deployment
      - Run tests
      - Check coverage
      - Comment on PR with results
```

---

### Pattern 2: Continuous Deployment

```yaml
on:
  push:
    branches: [dev]

jobs:
  deploy:
    steps:
      - Checkout code
      - Install Copado CLI
      - Authenticate
      - Deploy to QA
      - Run smoke tests
      - Notify team
```

---

### Pattern 3: Scheduled Backup

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  backup:
    steps:
      - Install Copado CLI
      - Authenticate
      - Retrieve all metadata
      - Compress backup
      - Upload to storage
```

---

## Troubleshooting

### Issue 1: Authentication Fails in CI

**Symptom**: JWT authentication fails in pipeline

**Solution**:

```yaml
# Ensure JWT key is properly formatted
- name: Setup JWT Key
  run: |
    echo "${{ secrets.COPADO_JWT_KEY }}" | base64 -d > server.key
    chmod 600 server.key

# Use correct instance URL
- name: Authenticate
  run: |
    copado auth jwt \
      --client-id ${{ secrets.COPADO_CLIENT_ID }} \
      --jwt-key-file ./server.key \
      --username ${{ secrets.COPADO_USERNAME }} \
      --instance-url https://test.salesforce.com
```

---

### Issue 2: Timeout in CI Pipeline

**Symptom**: Pipeline times out during deployment

**Solution**:

```yaml
# Increase timeout
- name: Deploy with Extended Timeout
  timeout-minutes: 30
  run: |
    copado metadata deploy \
      --org qa \
      --source ./force-app \
      --timeout 1800
```

---

## Best Practices

### Security

- Store credentials in CI secrets
- Use JWT for non-interactive auth
- Rotate credentials regularly
- Use separate service accounts
- Enable IP restrictions

### Performance

- Cache npm dependencies
- Use quick deploy when possible
- Deploy in parallel when safe
- Limit metadata scope
- Use incremental deployments

### Reliability

- Always validate before deploy
- Run tests on every PR
- Monitor pipeline failures
- Set up alerts
- Keep logs for audit

### Maintenance

- Update CLI regularly
- Test pipeline changes in dev
- Document pipeline configuration
- Version control all scripts
- Review pipeline metrics

---

## Related Skills

- `skill_copado_cli_installation.md` - CLI setup
- `skill_copado_cli_metadata_operations.md` - Metadata commands
- `skill_copado_cli_automation_scripts.md` - Automation scripts
- `skill_copado_deployments.md` - Deployment strategies

---

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Azure Pipelines Documentation](https://docs.microsoft.com/en-us/azure/devops/pipelines/)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [Copado CLI Documentation](https://docs.copado.com/articles/#!copado-ci-cd-publication/copado-cli)

---

**Skill Owner**: TEG Development Team  
**Last Validated**: March 3, 2026  
**Next Review**: April 1, 2026
