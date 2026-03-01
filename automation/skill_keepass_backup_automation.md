# SKILL: KeePass Backup Automation

**Actionable workflow for automating KeePass database backups with multi-location redundancy and integrity verification.**

**Last Updated:** March 1, 2026  
**Version:** 1.0.0  
**Category:** Automation

---

## What This Skill Does

Provides automated backup workflows for KeePass password databases:
- Scheduled daily and weekly backups
- Multi-location redundancy (Google Drive + local)
- Automatic backup rotation (keeps last 10 per location)
- Integrity verification with SHA256 hashing
- Manual backup with force and verify options

## When to Use This Skill

- **User says:** "Setup KeePass backups"
- **User says:** "Automate password database backups"
- **User says:** "Verify KeePass backup integrity"
- **User creates:** New KeePass database requiring backup protection
- **Trigger:** Initial KeePass setup or backup system configuration

## What You'll Need

- KeePass database file (`.kdbx`)
- PowerShell (Windows) or Bash (Linux/Mac)
- Write access to backup locations
- Windows Task Scheduler (for automated scheduling)

---

## Workflow: Setup Automated Backups

### Step 1: Verify Prerequisites

**Check KeePass database exists:**

```powershell
# Verify database file
Test-Path "${PARA_ROOT}/03_Areas/Keys/keys pass.kdbx"

# Check file size (should be > 0 bytes)
Get-Item "${PARA_ROOT}/03_Areas/Keys/keys pass.kdbx" | Select-Object Length
```

**Create backup directories:**

```powershell
# Create backup locations
New-Item -ItemType Directory -Force -Path "${PARA_ROOT}/05_Archive/Credentials_Backup/KeePass"
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\Documents\Backups\KeePass"
```

### Step 2: Install Backup Script

**Copy backup script to Keys folder:**

The backup script (`backup_keepass.ps1`) should be located in `${PARA_ROOT}/03_Areas/Keys/`

**Key features:**
- Multi-location backup (Google Drive + local Documents)
- Automatic rotation (keeps last 10 backups)
- SHA256 hash verification
- Timestamped backup files
- Logging to `backup_log.txt`

### Step 3: Setup Scheduled Tasks

**Run the setup script:**

```powershell
cd "${PARA_ROOT}/03_Areas/Keys"
.\setup_backup_schedule.ps1
```

**This creates two scheduled tasks:**

1. **Daily Backup** - Runs at 2:00 AM every day
   - Task Name: `KeePass_Daily_Backup`
   - Frequency: Daily
   - Action: `.\backup_keepass.ps1`

2. **Weekly Verified Backup** - Runs at 3:00 AM every Sunday
   - Task Name: `KeePass_Weekly_Backup`
   - Frequency: Weekly (Sunday)
   - Action: `.\backup_keepass.ps1 -Verify`

### Step 4: Test Backup Manually

**Run initial backup:**

```powershell
cd "${PARA_ROOT}/03_Areas/Keys"

# Basic backup
.\backup_keepass.ps1

# Force backup even if current
.\backup_keepass.ps1 -Force

# Backup with integrity verification
.\backup_keepass.ps1 -Verify
```

**Expected output:**
```
[2026-03-01 14:30:00] Starting KeePass backup...
[2026-03-01 14:30:01] Backing up to: G:\My Drive\05_Archive\Credentials_Backup\KeePass
[2026-03-01 14:30:02] Backup created: keys_pass_20260301_143000.kdbx
[2026-03-01 14:30:03] Backing up to: C:\Users\sol90\Documents\Backups\KeePass
[2026-03-01 14:30:04] Backup created: keys_pass_20260301_143000.kdbx
[2026-03-01 14:30:05] Backup completed successfully
```

### Step 5: Verify Scheduled Tasks

**Check task status:**

```powershell
# View daily backup task
Get-ScheduledTask -TaskName "KeePass_Daily_Backup"

# View weekly backup task
Get-ScheduledTask -TaskName "KeePass_Weekly_Backup"

# Check task history
Get-ScheduledTask -TaskName "KeePass_Daily_Backup" | Get-ScheduledTaskInfo

# View last run time and result
Get-ScheduledTaskInfo -TaskName "KeePass_Daily_Backup" | Select-Object LastRunTime, LastTaskResult
```

---

## Backup Script Details

### Configuration Variables

```powershell
# Source database
$KEEPASS_DB = "${PARA_ROOT}/03_Areas/Keys/keys pass.kdbx"

# Backup locations (multiple for redundancy)
$BACKUP_LOCATIONS = @(
    "${PARA_ROOT}/05_Archive/Credentials_Backup/KeePass",
    "$env:USERPROFILE\Documents\Backups\KeePass"
)

# Retention policy
$MAX_BACKUPS_PER_LOCATION = 10

# Logging
$LOG_FILE = "${PARA_ROOT}/03_Areas/Keys/backup_log.txt"
```

### Backup File Naming

**Format:** `keys_pass_YYYYMMDD_HHMMSS.kdbx`

**Examples:**
- `keys_pass_20260301_020000.kdbx` - Daily backup at 2:00 AM
- `keys_pass_20260302_143015.kdbx` - Manual backup at 2:30:15 PM

### Backup Process

1. **Check if backup needed** (unless `-Force` used)
   - Compare source file hash with latest backup hash
   - Skip if identical (no changes since last backup)

2. **Create timestamped backup**
   - Copy database to each backup location
   - Use timestamp in filename for versioning

3. **Verify integrity** (if `-Verify` flag used)
   - Calculate SHA256 hash of source
   - Calculate SHA256 hash of backup
   - Compare hashes to ensure perfect copy

4. **Rotate old backups**
   - Keep only last 10 backups per location
   - Delete oldest backups automatically

5. **Log results**
   - Append to `backup_log.txt`
   - Include timestamp, location, success/failure

---

## Workflow: Restore from Backup

### Step 1: List Available Backups

```powershell
# List backups in Google Drive
Get-ChildItem "${PARA_ROOT}/05_Archive/Credentials_Backup/KeePass" -Filter "keys_pass_*.kdbx" |
    Sort-Object LastWriteTime -Descending |
    Select-Object Name, LastWriteTime, @{Name='Size(KB)';Expression={[math]::Round($_.Length/1KB,2)}}

# List backups in local Documents
Get-ChildItem "$env:USERPROFILE\Documents\Backups\KeePass" -Filter "keys_pass_*.kdbx" |
    Sort-Object LastWriteTime -Descending |
    Select-Object Name, LastWriteTime
```

### Step 2: Verify Backup Integrity

```powershell
# Calculate hash of backup file
$backupHash = Get-FileHash "${PARA_ROOT}/05_Archive/Credentials_Backup/KeePass/keys_pass_20260301_020000.kdbx" -Algorithm SHA256

# Display hash
$backupHash.Hash
```

### Step 3: Restore Database

**⚠️ WARNING: This will overwrite your current database!**

```powershell
# Backup current database first (just in case)
Copy-Item "${PARA_ROOT}/03_Areas/Keys/keys pass.kdbx" `
    -Destination "${PARA_ROOT}/03_Areas/Keys/keys pass_BEFORE_RESTORE.kdbx"

# Restore from backup
Copy-Item "${PARA_ROOT}/05_Archive/Credentials_Backup/KeePass/keys_pass_20260301_020000.kdbx" `
    -Destination "${PARA_ROOT}/03_Areas/Keys/keys pass.kdbx" -Force

# Verify restoration
Get-FileHash "${PARA_ROOT}/03_Areas/Keys/keys pass.kdbx" -Algorithm SHA256
```

### Step 4: Test Restored Database

```powershell
# Try to open database in KeePass GUI
Start-Process "C:\Program Files\KeePass Password Safe 2\KeePass.exe" `
    -ArgumentList "${PARA_ROOT}/03_Areas/Keys/keys pass.kdbx"

# Or test with Python
cd "${PARA_ROOT}/03_Areas/Keys"
python keepass_loader.py list
```

---

## Backup Locations

### Primary Backup: Google Drive Archive

**Path:** `${PARA_ROOT}/05_Archive/Credentials_Backup/KeePass/`

**Advantages:**
- ✅ Cloud storage (accessible anywhere)
- ✅ Google Drive sync and versioning
- ✅ Protected by Google account security
- ✅ Survives local hardware failure

**Disadvantages:**
- ⚠️ Requires internet for access
- ⚠️ Syncs to cloud (encryption important)

### Secondary Backup: Local Documents

**Path:** `$env:USERPROFILE\Documents\Backups\KeePass\`

**Advantages:**
- ✅ Fast local access (no internet needed)
- ✅ Not dependent on cloud service
- ✅ Immediate availability

**Disadvantages:**
- ⚠️ Lost if computer fails
- ⚠️ Not accessible remotely

### Recommended: Both Locations

Using both locations provides:
- **Redundancy** - Multiple failure points required for data loss
- **Availability** - Access backups locally or remotely
- **Performance** - Fast local restore when needed
- **Disaster Recovery** - Cloud backup survives hardware failure

---

## Maintenance Tasks

### Daily (Automated)

**Task:** Daily backup at 2:00 AM
- Runs automatically via scheduled task
- Backs up to both locations
- Rotates old backups
- Logs results

**No action required** - just verify it's running

### Weekly (Automated)

**Task:** Weekly verified backup at 3:00 AM Sunday
- Runs automatically via scheduled task
- Includes integrity verification
- Ensures backup quality
- Logs detailed results

**No action required** - check logs if concerned

### Monthly (Manual)

**Task:** Verify backup system health

```powershell
# Check scheduled tasks are enabled
Get-ScheduledTask -TaskName "KeePass_*" | Select-Object TaskName, State

# Review backup log for errors
Get-Content "${PARA_ROOT}/03_Areas/Keys/backup_log.txt" -Tail 50

# Verify backup counts
(Get-ChildItem "${PARA_ROOT}/05_Archive/Credentials_Backup/KeePass" -Filter "keys_pass_*.kdbx").Count
(Get-ChildItem "$env:USERPROFILE\Documents\Backups\KeePass" -Filter "keys_pass_*.kdbx").Count

# Test manual backup
cd "${PARA_ROOT}/03_Areas/Keys"
.\backup_keepass.ps1 -Verify
```

### Quarterly (Manual)

**Task:** Test backup restoration

```powershell
# Restore to test location (don't overwrite current)
Copy-Item "${PARA_ROOT}/05_Archive/Credentials_Backup/KeePass/keys_pass_*.kdbx" `
    -Destination "${PARA_ROOT}/03_Areas/Keys/test_restore.kdbx"

# Verify can open with KeePass
# (Enter master password to confirm)
```

---

## Troubleshooting

### Backup Not Running

**Problem:** Scheduled task not executing

**Solution:**
```powershell
# Check task status
Get-ScheduledTask -TaskName "KeePass_Daily_Backup"

# View task history
Get-ScheduledTask -TaskName "KeePass_Daily_Backup" | Get-ScheduledTaskInfo

# Enable task if disabled
Enable-ScheduledTask -TaskName "KeePass_Daily_Backup"

# Run task manually to test
Start-ScheduledTask -TaskName "KeePass_Daily_Backup"
```

### Backup Fails with "Access Denied"

**Problem:** Insufficient permissions for backup location

**Solution:**
```powershell
# Check write permissions
Test-Path "${PARA_ROOT}/05_Archive/Credentials_Backup/KeePass" -PathType Container

# Create directory if missing
New-Item -ItemType Directory -Force -Path "${PARA_ROOT}/05_Archive/Credentials_Backup/KeePass"

# Run backup as administrator
Start-Process powershell -Verb RunAs -ArgumentList "-File backup_keepass.ps1"
```

### Hash Verification Fails

**Problem:** Backup file hash doesn't match source

**Solution:**
```powershell
# Delete corrupted backup
Remove-Item "${PARA_ROOT}/05_Archive/Credentials_Backup/KeePass/keys_pass_CORRUPTED.kdbx"

# Force new backup
.\backup_keepass.ps1 -Force -Verify

# Check log for errors
Get-Content "${PARA_ROOT}/03_Areas/Keys/backup_log.txt" -Tail 20
```

### Too Many Backups

**Problem:** More than 10 backups in location (rotation not working)

**Solution:**
```powershell
# Manual cleanup - keep last 10
Get-ChildItem "${PARA_ROOT}/05_Archive/Credentials_Backup/KeePass" -Filter "keys_pass_*.kdbx" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -Skip 10 |
    Remove-Item -Force

# Verify rotation in script
# Check $MAX_BACKUPS_PER_LOCATION variable
```

### Database File Locked

**Problem:** Cannot backup because KeePass has file open

**Solution:**
```powershell
# Close KeePass application
Stop-Process -Name "KeePass" -Force -ErrorAction SilentlyContinue

# Wait a moment
Start-Sleep -Seconds 2

# Run backup
.\backup_keepass.ps1
```

---

## Security Considerations

### Backup Encryption

**KeePass database is encrypted at rest:**
- ✅ Backups are encrypted (same as source)
- ✅ Master password required to open
- ✅ Safe to store in cloud
- ✅ Safe to store on local disk

**No additional encryption needed** - KeePass handles it

### Backup Locations Security

**Google Drive:**
- Protected by Google account 2FA
- Encrypted in transit (HTTPS)
- Encrypted at rest (Google's encryption)
- Access controlled by Google account

**Local Documents:**
- Protected by Windows user account
- BitLocker encryption (if enabled)
- Physical security of computer
- No cloud exposure

### Master Password Protection

**Critical:** Backups are only as secure as your master password

- ✅ Use strong, unique master password
- ✅ Never write down master password
- ✅ Use password manager for master password (ironic but effective)
- ✅ Consider using key file in addition to password

### Backup Log Security

**Log file contains:**
- ✅ Timestamps of backups
- ✅ File paths
- ✅ Success/failure status
- ❌ NO passwords
- ❌ NO database contents

**Safe to keep** - no sensitive data in logs

---

## Integration with Other Skills

### Works With: skill_keepass_integration.md

**Backup automation complements KeePass integration:**
- Integration provides access to credentials
- Backup provides data protection
- Together: Complete KeePass workflow

**Example workflow:**
1. Use `skill_keepass_integration.md` to access credentials
2. Use `skill_keepass_backup_automation.md` to protect database
3. Backups run automatically in background

### Works With: skill_environments_credentials.md

**Backup protects credential storage:**
- Environments skill documents credential management
- Backup skill protects KeePass database
- Both ensure credential availability

### Works With: skill_daily_planning.md

**Backup runs during off-hours:**
- Daily planning runs during work hours
- Backups run at 2:00 AM (no conflict)
- Both automated, no manual intervention

---

## AI Agent Instructions

**When user requests KeePass backup setup:**

1. **Verify prerequisites** - Check database exists
2. **Create backup directories** - Ensure locations exist
3. **Setup scheduled tasks** - Run setup script
4. **Test backup** - Run manual backup with `-Verify`
5. **Confirm success** - Check task status and logs

**Output format:**
```
✅ KeePass backup automation configured
📁 Backup locations: 2 (Google Drive + Local)
⏰ Schedule: Daily 2:00 AM, Weekly Sunday 3:00 AM
🔄 Retention: Last 10 backups per location
🔐 Security: Encrypted database, SHA256 verification
📊 Status: Run `Get-ScheduledTask -TaskName "KeePass_*"` to verify
```

---

## Related Skills

- **skill_keepass_integration.md** - Access KeePass credentials programmatically
- **skill_environments_credentials.md** - Overall credential management strategy
- **skill_powershell_automation.md** - PowerShell automation techniques
- **skill_file_organization.md** - PARA method file organization

---

## Changelog

- **2026-03-01:** Created KeePass backup automation skill
- **2026-03-01:** Extracted from `KEEPASS_QUICK_START.md` in Google Drive
- **2026-03-01:** Added AI agent instructions and troubleshooting
- **2026-03-01:** Integrated with existing KeePass and credential skills

---

**Location:** `${SKILLS_ROOT}/automation/skill_keepass_backup_automation.md`  
**Category:** Automation  
**Complexity:** Intermediate  
**Requires:** PowerShell, KeePass database, Windows Task Scheduler  
**Backup Locations:** 2 (redundant)  
**Automation:** Fully automated daily/weekly backups
