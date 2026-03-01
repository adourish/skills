# Process New - Complete Daily Workflow
# Runs daily planning + automated file processing

param(
    [int]$Days = 7
)

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "              PROCESS NEW - Complete Workflow               " -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

# Step 1: Daily Planning
Write-Host "STEP 1: Daily Planning & Kanban Board" -ForegroundColor Yellow
Write-Host "----------------------------------------------------------------`n" -ForegroundColor Yellow

Set-Location "G:\My Drive\06_Master_Guides\Scripts"

# Run daily planner
Write-Host "Running daily planner..." -ForegroundColor Cyan
python daily_planner.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Daily plan generated`n" -ForegroundColor Green
    
    # Create Kanban board
    Write-Host "Creating Kanban board in Amplenote..." -ForegroundColor Cyan
    node sync_plan_to_amplenote.js
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Kanban board created`n" -ForegroundColor Green
    } else {
        Write-Host "[WARN] Kanban board creation failed`n" -ForegroundColor Yellow
    }
} else {
    Write-Host "[ERROR] Daily planner failed`n" -ForegroundColor Red
}

# Step 2: File Processing
Write-Host "`nSTEP 2: Automated File Processing" -ForegroundColor Yellow
Write-Host "----------------------------------------------------------------`n" -ForegroundColor Yellow

# Check Downloads folder
$downloadsPath = "$env:USERPROFILE\Downloads"
$operateInbox = "G:\My Drive\01_Operate\Inbox"

Write-Host "Checking Downloads folder..." -ForegroundColor Cyan
$recentFiles = Get-ChildItem $downloadsPath | Where-Object {
    $_.LastWriteTime -gt (Get-Date).AddDays(-$Days)
}

if ($recentFiles) {
    Write-Host "Found $($recentFiles.Count) recent file(s)`n" -ForegroundColor Green
    
    foreach ($file in $recentFiles) {
        $ext = $file.Extension.ToLower()
        $name = $file.Name
        $size = [math]::Round($file.Length / 1MB, 2)
        
        Write-Host "FILE: $name ($size MB)" -ForegroundColor White
        
        # Determine destination based on file type
        $destination = $null
        $action = "Move to Operate/Inbox"
        
        # Videos
        if ($ext -in @('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm')) {
            # Check if adult content (based on naming patterns)
            if ($name -match 'hookup|megapack|xxx|porn|adult|nsfw') {
                Write-Host "   -> Adult video - Skipping (manual review needed)" -ForegroundColor Yellow
                continue
            } else {
                $destination = "G:\My Drive\04_Resources\Media\Videos"
                $action = "Move to Resources/Media/Videos"
            }
        }
        # Documents
        elseif ($ext -in @('.pdf', '.doc', '.docx', '.txt', '.md')) {
            $destination = $operateInbox
            $action = "Move to Operate/Inbox"
        }
        # Images
        elseif ($ext -in @('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')) {
            $destination = "G:\My Drive\04_Resources\Media\Photos"
            $action = "Move to Resources/Media/Photos"
        }
        # Archives
        elseif ($ext -in @('.zip', '.rar', '.7z', '.tar', '.gz')) {
            $destination = $operateInbox
            $action = "Move to Operate/Inbox (extract first)"
        }
        # Spreadsheets
        elseif ($ext -in @('.xlsx', '.xls', '.csv')) {
            $destination = $operateInbox
            $action = "Move to Operate/Inbox"
        }
        # Default
        else {
            $destination = $operateInbox
            $action = "Move to Operate/Inbox"
        }
        
        # Execute move
        if ($destination) {
            try {
                # Ensure destination exists
                if (-not (Test-Path $destination)) {
                    New-Item -ItemType Directory -Path $destination -Force | Out-Null
                }
                
                # Move file
                $destPath = Join-Path $destination $file.Name
                
                # Check if file already exists
                if (Test-Path $destPath) {
                    Write-Host "   [WARN] File already exists at destination - skipping" -ForegroundColor Yellow
                } else {
                    Move-Item $file.FullName $destPath -Force
                    Write-Host "   [OK] $action" -ForegroundColor Green
                }
            } catch {
                Write-Host "   [ERROR] Failed to move: $_" -ForegroundColor Red
            }
        }
        
        Write-Host ""
    }
} else {
    Write-Host "[OK] No recent files in Downloads folder`n" -ForegroundColor Green
}

# Summary
Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "                  PROCESS NEW COMPLETE                      " -ForegroundColor Cyan
Write-Host "================================================================`n" -ForegroundColor Cyan

Write-Host "SUMMARY:" -ForegroundColor Yellow
Write-Host "   - Daily plan generated and Kanban board created" -ForegroundColor White
Write-Host "   - Downloads folder processed" -ForegroundColor White
Write-Host "   - Files moved to appropriate locations`n" -ForegroundColor White

Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "   1. Open Amplenote to view your Kanban board" -ForegroundColor White
Write-Host "   2. Review Operate/Inbox for items needing manual filing" -ForegroundColor White
Write-Host "   3. Process any adult content manually if needed`n" -ForegroundColor White
