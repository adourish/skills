# Skill: Copado CLI Automation Scripts

**Category**: automation  
**Priority**: MEDIUM  
**Last Updated**: March 3, 2026  
**Prerequisites**:
- `skill_copado_cli_installation.md`
- `skill_copado_cli_metadata_operations.md`
- PowerShell or Bash scripting knowledge
- Understanding of automation patterns

---

## Overview

This skill provides reusable automation scripts for common Copado CLI operations including bulk User Story creation, automated deployments, metadata backups, and environment synchronization.

## When to Use This Skill

- Automating repetitive Copado tasks
- Bulk operations on User Stories
- Scheduled metadata backups
- Environment synchronization
- Deployment automation
- Monitoring and reporting

## Prerequisites

- Copado CLI installed and configured
- PowerShell 7+ (Windows) or Bash (Mac/Linux)
- Authenticated to required orgs
- Script execution permissions

## Core Concepts

### Script Categories

**Deployment Scripts**:
- Automated deployment to environments
- Validation and quick deploy
- Rollback automation

**Backup Scripts**:
- Scheduled metadata backups
- Incremental backups
- Backup rotation

**Monitoring Scripts**:
- Deployment status monitoring
- Test result aggregation
- Coverage reporting

**Bulk Operations**:
- Bulk User Story creation
- Batch deployments
- Mass metadata retrieval

---

## Step-by-Step Instructions

### Task 1: Automated Deployment Script

**Objective**: Deploy approved PRs to Copado automatically

**PowerShell Script**: `scripts/Deploy-ToCopado.ps1`

```powershell
<#
.SYNOPSIS
    Deploy approved PRs to Copado User Stories
.DESCRIPTION
    Retrieves approved PRs from intermediate repo, deploys to Dev Sandbox,
    creates Copado User Stories, and commits metadata
.PARAMETER Branch
    Source branch to deploy (default: dev)
.PARAMETER TargetOrg
    Target Salesforce org (default: dmedev5)
.PARAMETER CreateUserStory
    Create Copado User Story after deployment
.EXAMPLE
    .\Deploy-ToCopado.ps1 -Branch "feature/US-1234" -CreateUserStory
#>

param(
    [string]$Branch = "dev",
    [string]$TargetOrg = "dmedev5",
    [string]$Project = "BPHC Modernization",
    [switch]$CreateUserStory,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

# Extract User Story ID from branch name
$userStoryId = $Branch -replace "feature/", "" -replace "-.*", ""
Write-Host "Processing branch: $Branch (User Story: $userStoryId)" -ForegroundColor Cyan

# Step 1: Deploy to Dev Sandbox via SFDX
Write-Host "`n[1/4] Deploying to Dev Sandbox..." -ForegroundColor Yellow

if ($DryRun) {
    Write-Host "DRY RUN: Would deploy force-app to $TargetOrg" -ForegroundColor Gray
} else {
    sfdx force:source:deploy -p force-app -u $TargetOrg --verbose
    if ($LASTEXITCODE -ne 0) {
        throw "Deployment to Dev Sandbox failed"
    }
    Write-Host "✓ Deployed to $TargetOrg" -ForegroundColor Green
}

# Step 2: Run Apex Tests
Write-Host "`n[2/4] Running Apex Tests..." -ForegroundColor Yellow

if ($DryRun) {
    Write-Host "DRY RUN: Would run Apex tests in $TargetOrg" -ForegroundColor Gray
} else {
    $testResults = sfdx force:apex:test:run -u $TargetOrg -r human -w 10 | Out-String
    Write-Host $testResults
    
    if ($testResults -match "Failing: (\d+)") {
        $failures = [int]$matches[1]
        if ($failures -gt 0) {
            throw "$failures test(s) failed"
        }
    }
    Write-Host "✓ All tests passed" -ForegroundColor Green
}

# Step 3: Create Copado User Story (if requested)
if ($CreateUserStory) {
    Write-Host "`n[3/4] Creating Copado User Story..." -ForegroundColor Yellow
    
    if ($DryRun) {
        Write-Host "DRY RUN: Would create User Story for $userStoryId" -ForegroundColor Gray
    } else {
        $storyTitle = "$userStoryId: Deployed from intermediate repo"
        
        $storyId = copado user-story create `
            --title $storyTitle `
            --org $TargetOrg `
            --project $Project `
            --json | ConvertFrom-Json | Select-Object -ExpandProperty id
        
        Write-Host "✓ Created User Story: $storyId" -ForegroundColor Green
        
        # Step 4: Commit metadata to Copado
        Write-Host "`n[4/4] Committing metadata to Copado..." -ForegroundColor Yellow
        
        copado user-story commit `
            --id $storyId `
            --message "Deployed from branch: $Branch"
        
        Write-Host "✓ Metadata committed to Copado" -ForegroundColor Green
        Write-Host "`nCopado User Story ID: $storyId" -ForegroundColor Cyan
    }
} else {
    Write-Host "`n[3/4] Skipping User Story creation (use -CreateUserStory to enable)" -ForegroundColor Gray
}

Write-Host "`n✓ Deployment complete!" -ForegroundColor Green
```

**Usage**:

```powershell
# Deploy and create User Story
.\Deploy-ToCopado.ps1 -Branch "feature/US-1234-project-validation" -CreateUserStory

# Dry run
.\Deploy-ToCopado.ps1 -Branch "dev" -DryRun

# Deploy without User Story
.\Deploy-ToCopado.ps1 -Branch "dev"
```

---

### Task 2: Metadata Backup Script

**Objective**: Automated daily metadata backups

**PowerShell Script**: `scripts/Backup-Metadata.ps1`

```powershell
<#
.SYNOPSIS
    Backup Salesforce metadata from specified org
.DESCRIPTION
    Retrieves all metadata, compresses, and stores with timestamp
.PARAMETER Org
    Source org to backup (default: production)
.PARAMETER BackupDir
    Backup directory (default: ./backups)
.PARAMETER Compress
    Compress backup to ZIP file
.PARAMETER Retention
    Number of days to retain backups (default: 30)
.EXAMPLE
    .\Backup-Metadata.ps1 -Org production -Compress -Retention 90
#>

param(
    [string]$Org = "production",
    [string]$BackupDir = "./backups",
    [switch]$Compress,
    [int]$Retention = 30
)

$ErrorActionPreference = "Stop"

# Create backup directory
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupPath = Join-Path $BackupDir "$Org-$timestamp"
New-Item -ItemType Directory -Path $backupPath -Force | Out-Null

Write-Host "Backing up metadata from $Org to $backupPath" -ForegroundColor Cyan

# Retrieve all metadata
Write-Host "`n[1/3] Retrieving metadata..." -ForegroundColor Yellow

copado metadata retrieve `
    --org $Org `
    --output $backupPath `
    --all `
    --timeout 1800

if ($LASTEXITCODE -ne 0) {
    throw "Metadata retrieval failed"
}

Write-Host "✓ Metadata retrieved" -ForegroundColor Green

# Compress backup
if ($Compress) {
    Write-Host "`n[2/3] Compressing backup..." -ForegroundColor Yellow
    
    $zipPath = "$backupPath.zip"
    Compress-Archive -Path $backupPath -DestinationPath $zipPath -Force
    
    # Remove uncompressed directory
    Remove-Item -Path $backupPath -Recurse -Force
    
    Write-Host "✓ Backup compressed: $zipPath" -ForegroundColor Green
    $finalPath = $zipPath
} else {
    $finalPath = $backupPath
}

# Clean up old backups
Write-Host "`n[3/3] Cleaning up old backups (retention: $Retention days)..." -ForegroundColor Yellow

$cutoffDate = (Get-Date).AddDays(-$Retention)
$oldBackups = Get-ChildItem -Path $BackupDir -Filter "$Org-*" | 
    Where-Object { $_.LastWriteTime -lt $cutoffDate }

foreach ($backup in $oldBackups) {
    Write-Host "Removing old backup: $($backup.Name)" -ForegroundColor Gray
    Remove-Item -Path $backup.FullName -Recurse -Force
}

Write-Host "✓ Cleanup complete" -ForegroundColor Green

# Summary
$backupSize = if ($Compress) {
    (Get-Item $zipPath).Length / 1MB
} else {
    (Get-ChildItem -Path $backupPath -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
}

Write-Host "`n✓ Backup complete!" -ForegroundColor Green
Write-Host "Location: $finalPath" -ForegroundColor Cyan
Write-Host "Size: $([math]::Round($backupSize, 2)) MB" -ForegroundColor Cyan
```

**Schedule with Task Scheduler (Windows)**:

```powershell
# Create scheduled task for daily backup
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" `
    -Argument "-File C:\scripts\Backup-Metadata.ps1 -Org production -Compress"

$trigger = New-ScheduledTaskTrigger -Daily -At 2:00AM

Register-ScheduledTask -TaskName "Copado Metadata Backup" `
    -Action $action `
    -Trigger $trigger `
    -Description "Daily backup of Salesforce metadata"
```

**Schedule with Cron (Linux/Mac)**:

```bash
# Add to crontab
0 2 * * * /usr/local/bin/pwsh /scripts/Backup-Metadata.ps1 -Org production -Compress
```

---

### Task 3: Bulk User Story Creation

**Objective**: Create multiple User Stories from CSV

**PowerShell Script**: `scripts/Create-BulkUserStories.ps1`

```powershell
<#
.SYNOPSIS
    Create multiple Copado User Stories from CSV file
.DESCRIPTION
    Reads CSV with User Story details and creates them in Copado
.PARAMETER CsvPath
    Path to CSV file with User Story data
.PARAMETER Org
    Target Salesforce org
.PARAMETER Project
    Copado project name
.EXAMPLE
    .\Create-BulkUserStories.ps1 -CsvPath ./user-stories.csv -Project "BPHC Modernization"
#>

param(
    [Parameter(Mandatory)]
    [string]$CsvPath,
    [string]$Org = "dmedev5",
    [string]$Project = "BPHC Modernization"
)

$ErrorActionPreference = "Stop"

# Read CSV
$userStories = Import-Csv -Path $CsvPath

Write-Host "Creating $($userStories.Count) User Stories in $Project" -ForegroundColor Cyan

$created = @()
$failed = @()

foreach ($story in $userStories) {
    try {
        Write-Host "`nCreating: $($story.Title)" -ForegroundColor Yellow
        
        $storyId = copado user-story create `
            --title $story.Title `
            --description $story.Description `
            --org $Org `
            --project $Project `
            --json | ConvertFrom-Json | Select-Object -ExpandProperty id
        
        Write-Host "✓ Created: $storyId" -ForegroundColor Green
        
        $created += [PSCustomObject]@{
            Title = $story.Title
            StoryId = $storyId
            Status = "Created"
        }
    }
    catch {
        Write-Host "✗ Failed: $($_.Exception.Message)" -ForegroundColor Red
        
        $failed += [PSCustomObject]@{
            Title = $story.Title
            Error = $_.Exception.Message
        }
    }
}

# Summary
Write-Host "`n=== Summary ===" -ForegroundColor Cyan
Write-Host "Created: $($created.Count)" -ForegroundColor Green
Write-Host "Failed: $($failed.Count)" -ForegroundColor Red

# Export results
$created | Export-Csv -Path "./user-stories-created.csv" -NoTypeInformation
if ($failed.Count -gt 0) {
    $failed | Export-Csv -Path "./user-stories-failed.csv" -NoTypeInformation
}

Write-Host "`nResults exported to ./user-stories-created.csv" -ForegroundColor Cyan
```

**CSV Format** (`user-stories.csv`):

```csv
Title,Description
US-1234: Project Validation,"Implement project validation logic including required fields and budget ranges"
US-1235: Activity Validation,"Add activity validation for dates and types"
US-1236: Review Workflow,"Create review workflow with approval process"
```

**Usage**:

```powershell
.\Create-BulkUserStories.ps1 -CsvPath ./user-stories.csv -Project "BPHC Modernization"
```

---

### Task 4: Environment Sync Script

**Objective**: Synchronize metadata between environments

**Bash Script**: `scripts/sync-environments.sh`

```bash
#!/bin/bash
# Sync metadata from source to target environment

set -e

SOURCE_ORG=${1:-dmedev5}
TARGET_ORG=${2:-qa}
METADATA_TYPES=${3:-"ApexClass,LightningComponentBundle,CustomObject"}

TEMP_DIR="./sync-temp"

echo "Syncing metadata from $SOURCE_ORG to $TARGET_ORG"
echo "Metadata types: $METADATA_TYPES"

# Step 1: Retrieve from source
echo -e "\n[1/4] Retrieving metadata from $SOURCE_ORG..."
mkdir -p $TEMP_DIR

copado metadata retrieve \
  --org $SOURCE_ORG \
  --type $METADATA_TYPES \
  --output $TEMP_DIR

echo "✓ Retrieved metadata"

# Step 2: Compare with target
echo -e "\n[2/4] Comparing with $TARGET_ORG..."

copado metadata diff \
  --source $SOURCE_ORG \
  --target $TARGET_ORG \
  --type $METADATA_TYPES \
  --output ./diff-report.txt

echo "✓ Diff report generated: ./diff-report.txt"

# Step 3: Validate deployment
echo -e "\n[3/4] Validating deployment to $TARGET_ORG..."

copado metadata deploy \
  --org $TARGET_ORG \
  --source $TEMP_DIR \
  --validate-only \
  --test-level RunLocalTests

echo "✓ Validation passed"

# Step 4: Deploy
echo -e "\n[4/4] Deploying to $TARGET_ORG..."

read -p "Proceed with deployment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  copado metadata deploy \
    --org $TARGET_ORG \
    --source $TEMP_DIR \
    --test-level RunLocalTests
  
  echo "✓ Deployment complete"
else
  echo "Deployment cancelled"
fi

# Cleanup
rm -rf $TEMP_DIR

echo -e "\n✓ Sync complete!"
```

**Usage**:

```bash
# Sync all metadata types
./sync-environments.sh dmedev5 qa

# Sync specific types
./sync-environments.sh dmedev5 qa "ApexClass,ApexTrigger"
```

---

### Task 5: Deployment Monitoring Script

**Objective**: Monitor deployment status and send notifications

**PowerShell Script**: `scripts/Monitor-Deployment.ps1`

```powershell
<#
.SYNOPSIS
    Monitor Copado deployment status
.DESCRIPTION
    Polls deployment status and sends notifications on completion
.PARAMETER DeploymentId
    Copado deployment ID to monitor
.PARAMETER Org
    Target org
.PARAMETER NotifyEmail
    Email address for notifications
.EXAMPLE
    .\Monitor-Deployment.ps1 -DeploymentId "0Af5w00000abcde" -Org qa
#>

param(
    [Parameter(Mandatory)]
    [string]$DeploymentId,
    [string]$Org = "qa",
    [string]$NotifyEmail,
    [int]$PollInterval = 30
)

$ErrorActionPreference = "Stop"

Write-Host "Monitoring deployment: $DeploymentId" -ForegroundColor Cyan

$startTime = Get-Date
$status = "In Progress"

while ($status -eq "In Progress" -or $status -eq "Queued") {
    # Get deployment status
    $result = copado deployment status --id $DeploymentId --json | ConvertFrom-Json
    $status = $result.status
    $progress = $result.progress
    
    # Display progress
    $elapsed = [math]::Round(((Get-Date) - $startTime).TotalMinutes, 1)
    Write-Host "`r[$elapsed min] Status: $status | Progress: $progress%" -NoNewline
    
    if ($status -eq "In Progress" -or $status -eq "Queued") {
        Start-Sleep -Seconds $PollInterval
    }
}

Write-Host "`n"

# Final status
if ($status -eq "Completed") {
    Write-Host "✓ Deployment completed successfully!" -ForegroundColor Green
    
    # Get deployment details
    $details = copado deployment details --id $DeploymentId --json | ConvertFrom-Json
    
    Write-Host "`nDeployment Summary:" -ForegroundColor Cyan
    Write-Host "Components Deployed: $($details.componentsDeployed)" -ForegroundColor White
    Write-Host "Tests Passed: $($details.testsPassed)" -ForegroundColor White
    Write-Host "Code Coverage: $($details.codeCoverage)%" -ForegroundColor White
    Write-Host "Duration: $([math]::Round($details.duration / 60, 1)) minutes" -ForegroundColor White
    
    $exitCode = 0
}
else {
    Write-Host "✗ Deployment failed with status: $status" -ForegroundColor Red
    
    # Get error details
    $errors = copado deployment errors --id $DeploymentId --json | ConvertFrom-Json
    
    Write-Host "`nErrors:" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "  - $($error.message)" -ForegroundColor Red
    }
    
    $exitCode = 1
}

# Send notification
if ($NotifyEmail) {
    $subject = if ($status -eq "Completed") {
        "✓ Deployment Successful: $DeploymentId"
    } else {
        "✗ Deployment Failed: $DeploymentId"
    }
    
    $body = "Deployment $DeploymentId to $Org completed with status: $status"
    
    # Send email (configure SMTP settings)
    # Send-MailMessage -To $NotifyEmail -Subject $subject -Body $body -SmtpServer "smtp.example.com"
    
    Write-Host "`nNotification sent to $NotifyEmail" -ForegroundColor Cyan
}

exit $exitCode
```

**Usage**:

```powershell
# Monitor deployment
.\Monitor-Deployment.ps1 -DeploymentId "0Af5w00000abcde" -Org qa

# Monitor with email notification
.\Monitor-Deployment.ps1 -DeploymentId "0Af5w00000abcde" -Org qa -NotifyEmail "team@example.com"
```

---

## Common Patterns

### Pattern 1: Daily Deployment Automation

```powershell
# Schedule daily deployment at 10 AM
# 1. Backup current state
.\Backup-Metadata.ps1 -Org dmedev5 -Compress

# 2. Deploy approved PRs
.\Deploy-ToCopado.ps1 -Branch "dev" -CreateUserStory

# 3. Monitor deployment
.\Monitor-Deployment.ps1 -DeploymentId $deploymentId -NotifyEmail "team@example.com"
```

---

### Pattern 2: Environment Refresh

```bash
# Complete environment refresh
# 1. Backup target environment
./backup-metadata.sh uat

# 2. Sync from source
./sync-environments.sh production uat

# 3. Verify sync
./verify-sync.sh production uat
```

---

## Best Practices

### Script Development

- Use parameter validation
- Add help documentation
- Include error handling
- Log all operations
- Support dry-run mode

### Security

- Never hardcode credentials
- Use environment variables
- Encrypt sensitive data
- Audit script execution
- Restrict script permissions

### Reliability

- Add retry logic
- Validate inputs
- Check prerequisites
- Handle timeouts
- Clean up temp files

### Maintenance

- Version control scripts
- Document dependencies
- Test before deployment
- Monitor script performance
- Update regularly

---

## Related Skills

- `skill_copado_cli_installation.md` - CLI setup
- `skill_copado_cli_metadata_operations.md` - Metadata commands
- `skill_copado_cli_cicd_integration.md` - CI/CD integration
- `skill_copado_user_stories.md` - User Story management

---

## References

- [PowerShell Documentation](https://docs.microsoft.com/en-us/powershell/)
- [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/)
- [Copado CLI Documentation](https://docs.copado.com/articles/#!copado-ci-cd-publication/copado-cli)

---

**Skill Owner**: TEG Development Team  
**Last Validated**: March 3, 2026  
**Next Review**: April 1, 2026
