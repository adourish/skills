# PowerShell Automation - Master Guide

**Last Updated:** January 26, 2026  
**Purpose:** Comprehensive guide for PowerShell scripting, automation patterns, and best practices  
**Success Rate:** Proven patterns from production automation

---

## Table of Contents

1. [Overview](#overview)
2. [PowerShell Fundamentals](#powershell-fundamentals)
3. [Script Parameters and Input](#script-parameters-and-input)
4. [File Operations](#file-operations)
5. [Error Handling](#error-handling)
6. [Logging and Debugging](#logging-and-debugging)
7. [Credential Management](#credential-management)
8. [Salesforce CLI Integration](#salesforce-cli-integration)
9. [Common Patterns](#common-patterns)
10. [Best Practices](#best-practices)
11. [Troubleshooting](#troubleshooting)

---

## Overview

PowerShell is the primary scripting language for Windows automation, file processing, and Salesforce CLI integration.

### Prerequisites

- PowerShell 5.1+ (Windows) or PowerShell Core 7+ (cross-platform)
- Execution policy set to allow scripts
- Salesforce CLI installed (for SF automation)

### Check PowerShell Version

```powershell
$PSVersionTable.PSVersion
```

### Set Execution Policy

```powershell
# For current user (recommended)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Check current policy
Get-ExecutionPolicy -List
```

---

## PowerShell Fundamentals

### Variables and Data Types

```powershell
# String
$name = "John Doe"
$path = "C:\Projects\POCs"

# Integer
$count = 42

# Boolean
$isActive = $true

# Array
$items = @("item1", "item2", "item3")
$numbers = 1..10  # Range

# Hashtable (dictionary)
$config = @{
    Org = "dmedev5"
    Type = "lwc"
    Action = "push"
}

# Access hashtable values
$config.Org
$config["Type"]

# Null check
if ($null -eq $variable) {
    Write-Host "Variable is null"
}
```

### String Operations

```powershell
# String interpolation
$message = "Hello, $name!"
$path = "C:\Projects\$projectName\src"

# String concatenation
$fullPath = $basePath + "\" + $fileName

# Multi-line strings (here-string)
$query = @"
SELECT Id, Name, Email
FROM Contact
WHERE AccountId = '$accountId'
"@

# String methods
$text.ToUpper()
$text.ToLower()
$text.Trim()
$text.Replace("old", "new")
$text.Split(",")
$text.StartsWith("prefix")
$text.EndsWith(".txt")
$text.Contains("substring")

# String comparison (case-insensitive by default)
if ($text -eq "value") { }
if ($text -like "*pattern*") { }  # Wildcard
if ($text -match "regex") { }     # Regex
```

### Conditionals

```powershell
# If statement
if ($count -gt 10) {
    Write-Host "Count is greater than 10"
} elseif ($count -eq 10) {
    Write-Host "Count is exactly 10"
} else {
    Write-Host "Count is less than 10"
}

# Switch statement
switch ($action) {
    "push" { Deploy-Code }
    "pull" { Retrieve-Code }
    "test" { Run-Tests }
    default { Write-Host "Unknown action" }
}

# Comparison operators
-eq   # Equal
-ne   # Not equal
-gt   # Greater than
-ge   # Greater than or equal
-lt   # Less than
-le   # Less than or equal
-like # Wildcard match
-match # Regex match
-and  # Logical AND
-or   # Logical OR
-not  # Logical NOT
```

### Loops

```powershell
# ForEach loop
foreach ($item in $items) {
    Write-Host "Processing: $item"
}

# For loop
for ($i = 0; $i -lt $items.Count; $i++) {
    Write-Host "Item $i: $($items[$i])"
}

# While loop
$i = 0
while ($i -lt 10) {
    Write-Host $i
    $i++
}

# Do-While loop
do {
    $input = Read-Host "Enter value (or 'quit')"
} while ($input -ne "quit")

# Break and Continue
foreach ($item in $items) {
    if ($item -eq "skip") { continue }
    if ($item -eq "stop") { break }
    Write-Host $item
}
```

---

## Script Parameters and Input

### Parameter Declaration

```powershell
# Basic parameters
param(
    [string]$Name,
    [int]$Count,
    [switch]$Force
)

# Parameters with validation
param(
    [Parameter(Mandatory=$true)]
    [ValidateNotNullOrEmpty()]
    [string]$Org,
    
    [Parameter(Mandatory=$true)]
    [ValidateSet("lwc", "apex", "object", "trigger")]
    [string]$Type,
    
    [Parameter(Mandatory=$false)]
    [ValidatePattern("^[a-zA-Z_]+$")]
    [string]$Pattern = "*",
    
    [Parameter(Mandatory=$false)]
    [ValidateSet("push", "pull")]
    [string]$Action = "push"
)
```

### Real-World Example: sfsync.ps1 Pattern

```powershell
param(
    [Parameter(Mandatory=$true, HelpMessage="Component type (lwc, apex, object)")]
    [ValidateSet("lwc", "apex", "object", "trigger", "flow")]
    [string]$type,
    
    [Parameter(Mandatory=$true, HelpMessage="Pattern to match files")]
    [string]$pattern,
    
    [Parameter(Mandatory=$true, HelpMessage="Action to perform")]
    [ValidateSet("push", "pull")]
    [string]$action,
    
    [Parameter(Mandatory=$true, HelpMessage="Target org alias")]
    [string]$org,
    
    [Parameter(Mandatory=$false)]
    [switch]$verbose
)

# Usage:
# .\sfsync.ps1 -type lwc -pattern "cmn_Workflow*" -action push -org dmedev5
```

### Reading User Input

```powershell
# Simple input
$name = Read-Host "Enter your name"

# Secure input (password)
$password = Read-Host "Enter password" -AsSecureString

# Convert secure string to plain text (if needed)
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
$plainPassword = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
```

---

## File Operations

### Path Operations

```powershell
# Join paths (handles separators correctly)
$fullPath = Join-Path -Path "C:\Projects" -ChildPath "POCs\src"

# Get file/directory info
$item = Get-Item "C:\Projects\file.txt"
$item.Name
$item.FullName
$item.Extension
$item.LastWriteTime
$item.Length  # Size in bytes

# Test if path exists
if (Test-Path "C:\Projects\file.txt") {
    Write-Host "File exists"
}

# Get parent directory
$parentDir = Split-Path -Path $fullPath -Parent

# Get file name
$fileName = Split-Path -Path $fullPath -Leaf

# Get file name without extension
$baseName = [System.IO.Path]::GetFileNameWithoutExtension($fileName)

# Get extension
$extension = [System.IO.Path]::GetExtension($fileName)
```

### Reading Files

```powershell
# Read entire file as string
$content = Get-Content -Path "file.txt" -Raw

# Read file line by line
$lines = Get-Content -Path "file.txt"
foreach ($line in $lines) {
    Write-Host $line
}

# Read CSV
$data = Import-Csv -Path "data.csv"
foreach ($row in $data) {
    Write-Host "$($row.Name): $($row.Value)"
}

# Read JSON
$json = Get-Content -Path "config.json" -Raw | ConvertFrom-Json
$json.property

# Read XML
[xml]$xml = Get-Content -Path "config.xml"
$xml.root.element
```

### Writing Files

```powershell
# Write string to file (overwrites)
"Hello World" | Out-File -FilePath "output.txt"

# Append to file
"New line" | Out-File -FilePath "output.txt" -Append

# Write array to file (one line per item)
$lines = @("Line 1", "Line 2", "Line 3")
$lines | Out-File -FilePath "output.txt"

# Set content (overwrites)
Set-Content -Path "file.txt" -Value "New content"

# Add content (appends)
Add-Content -Path "file.txt" -Value "Appended line"

# Write CSV
$data | Export-Csv -Path "output.csv" -NoTypeInformation

# Write JSON
$object | ConvertTo-Json -Depth 10 | Out-File "output.json"
```

### File and Directory Operations

```powershell
# Create directory
New-Item -Path "C:\Projects\NewFolder" -ItemType Directory -Force

# Create file
New-Item -Path "C:\Projects\file.txt" -ItemType File -Force

# Copy file
Copy-Item -Path "source.txt" -Destination "dest.txt"

# Copy directory recursively
Copy-Item -Path "C:\Source" -Destination "C:\Dest" -Recurse

# Move file
Move-Item -Path "source.txt" -Destination "C:\NewLocation\source.txt"

# Rename file
Rename-Item -Path "old.txt" -NewName "new.txt"

# Delete file
Remove-Item -Path "file.txt"

# Delete directory recursively
Remove-Item -Path "C:\Folder" -Recurse -Force

# Get files in directory
$files = Get-ChildItem -Path "C:\Projects" -Filter "*.txt"

# Get files recursively
$files = Get-ChildItem -Path "C:\Projects" -Filter "*.cls" -Recurse

# Get only files (exclude directories)
$files = Get-ChildItem -Path "C:\Projects" -File

# Get only directories
$dirs = Get-ChildItem -Path "C:\Projects" -Directory
```

### Pattern Matching and Filtering

```powershell
# Filter files by pattern
$files = Get-ChildItem -Path "force-app\main\default\classes" -Filter "cmn_Workflow*.cls"

# Multiple patterns
$patterns = @("cmn_Workflow*", "cmn_Approval*")
$files = Get-ChildItem -Path "force-app\main\default\classes" | 
    Where-Object { 
        $name = $_.Name
        $patterns | Where-Object { $name -like $_ }
    }

# Filter by properties
$largeFiles = Get-ChildItem -Path "C:\Projects" -Recurse | 
    Where-Object { $_.Length -gt 1MB }

# Filter by date
$recentFiles = Get-ChildItem -Path "C:\Projects" | 
    Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) }
```

---

## Error Handling

### Try-Catch-Finally

```powershell
try {
    # Code that might fail
    $content = Get-Content -Path "file.txt" -ErrorAction Stop
    
    # Process content
    $result = Process-Data -Data $content
    
} catch [System.IO.FileNotFoundException] {
    Write-Error "File not found: $($_.Exception.Message)"
    
} catch [System.UnauthorizedAccessException] {
    Write-Error "Access denied: $($_.Exception.Message)"
    
} catch {
    # Catch all other errors
    Write-Error "Unexpected error: $($_.Exception.Message)"
    Write-Error "Stack trace: $($_.ScriptStackTrace)"
    
} finally {
    # Always executes (cleanup)
    Write-Host "Cleanup completed"
}
```

### Error Action Preference

```powershell
# Stop on error (throw exception)
$ErrorActionPreference = "Stop"

# Continue on error (default)
$ErrorActionPreference = "Continue"

# Silently continue (suppress errors)
$ErrorActionPreference = "SilentlyContinue"

# Per-command error action
Get-Content -Path "file.txt" -ErrorAction Stop
Get-Content -Path "file.txt" -ErrorAction SilentlyContinue
```

### Validation and Guards

```powershell
function Deploy-Code {
    param(
        [string]$Path,
        [string]$Org
    )
    
    # Validate parameters
    if ([string]::IsNullOrWhiteSpace($Path)) {
        throw "Path parameter is required"
    }
    
    if (-not (Test-Path $Path)) {
        throw "Path does not exist: $Path"
    }
    
    # Validate org is authenticated
    $orgs = sf org list --json | ConvertFrom-Json
    $orgExists = $orgs.result | Where-Object { $_.alias -eq $Org }
    if (-not $orgExists) {
        throw "Org '$Org' is not authenticated"
    }
    
    # Proceed with deployment
    Write-Host "Deploying $Path to $Org..."
}
```

---

## Logging and Debugging

### Write-Host vs Write-Output

```powershell
# Write-Host: Display to console (not captured by pipeline)
Write-Host "Processing file..." -ForegroundColor Green

# Write-Output: Send to pipeline (can be captured)
Write-Output "Result data"

# Write-Error: Error message
Write-Error "Something went wrong"

# Write-Warning: Warning message
Write-Warning "This is deprecated"

# Write-Verbose: Verbose output (only shown with -Verbose)
Write-Verbose "Detailed processing info"

# Write-Debug: Debug output (only shown with -Debug)
Write-Debug "Debug information"
```

### Logging Pattern

```powershell
function Write-Log {
    param(
        [string]$Message,
        [ValidateSet("INFO", "WARN", "ERROR", "DEBUG")]
        [string]$Level = "INFO",
        [string]$LogFile = "script.log"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    # Write to console with color
    $color = switch ($Level) {
        "INFO"  { "White" }
        "WARN"  { "Yellow" }
        "ERROR" { "Red" }
        "DEBUG" { "Gray" }
    }
    Write-Host $logMessage -ForegroundColor $color
    
    # Write to log file
    Add-Content -Path $LogFile -Value $logMessage
}

# Usage
Write-Log "Starting deployment" -Level INFO
Write-Log "File not found" -Level WARN
Write-Log "Deployment failed" -Level ERROR
```

### Debugging Techniques

```powershell
# Set breakpoint (in ISE or VS Code)
Set-PSBreakpoint -Script "script.ps1" -Line 42

# Debug mode
Set-PSDebug -Trace 1  # Trace script execution
Set-PSDebug -Trace 2  # Trace with variable assignments
Set-PSDebug -Off      # Turn off tracing

# Measure execution time
$stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
# ... code to measure ...
$stopwatch.Stop()
Write-Host "Execution time: $($stopwatch.Elapsed.TotalSeconds) seconds"

# Verbose output
function Process-Data {
    [CmdletBinding()]
    param([string]$Data)
    
    Write-Verbose "Processing data: $Data"
    # ... processing ...
}

# Call with -Verbose to see verbose output
Process-Data -Data "test" -Verbose
```

---

## Credential Management

### Loading Environment Credentials

```powershell
# CRITICAL: Always load from centralized location
$envs = & 'G:\My Drive\03_Areas\Keys\Environments\Load-Environments.ps1'

# Access credentials
$apiKey = $envs.SALESFORCE_API_KEY
$username = $envs.SALESFORCE_USERNAME
$password = $envs.SALESFORCE_PASSWORD

# Never hardcode credentials
# ❌ WRONG
$apiKey = "hardcoded-key-12345"

# ✅ CORRECT
$apiKey = $envs.API_KEY
```

### Secure String Handling

```powershell
# Create secure string
$securePassword = ConvertTo-SecureString "P@ssw0rd" -AsPlainText -Force

# Create PSCredential
$credential = New-Object System.Management.Automation.PSCredential(
    "username",
    $securePassword
)

# Use credential
Invoke-Command -ComputerName "server" -Credential $credential -ScriptBlock {
    # Commands run with credential
}
```

### API Key Management

```powershell
# Load API keys from environment
$envs = & 'G:\My Drive\03_Areas\Keys\Environments\Load-Environments.ps1'

# Use in API calls
$headers = @{
    "Authorization" = "Bearer $($envs.API_TOKEN)"
    "Content-Type" = "application/json"
}

$response = Invoke-RestMethod -Uri "https://api.example.com/data" -Headers $headers
```

---

## Salesforce CLI Integration

### Running SF Commands

```powershell
# Deploy code
sf project deploy start --source-dir "force-app\main\default\classes\MyClass.cls" --target-org dmedev5

# Capture output
$output = sf org display --target-org dmedev5 --json | ConvertFrom-Json
$orgId = $output.result.id

# Run with error handling
try {
    $result = sf project deploy start --source-dir $sourcePath --target-org $org --json | ConvertFrom-Json
    
    if ($result.status -eq 0) {
        Write-Log "Deployment successful" -Level INFO
    } else {
        Write-Log "Deployment failed: $($result.message)" -Level ERROR
    }
} catch {
    Write-Log "SF CLI error: $($_.Exception.Message)" -Level ERROR
}
```

### sfsync.ps1 Pattern

```powershell
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("lwc", "apex", "object", "trigger", "flow")]
    [string]$type,
    
    [Parameter(Mandatory=$true)]
    [string]$pattern,
    
    [Parameter(Mandatory=$true)]
    [ValidateSet("push", "pull")]
    [string]$action,
    
    [Parameter(Mandatory=$true)]
    [string]$org
)

# Map type to directory
$typeMap = @{
    "lwc" = "force-app\main\default\lwc"
    "apex" = "force-app\main\default\classes"
    "object" = "force-app\main\default\objects"
    "trigger" = "force-app\main\default\triggers"
    "flow" = "force-app\main\default\flows"
}

$baseDir = $typeMap[$type]

# Find matching files
$files = Get-ChildItem -Path $baseDir -Filter "$pattern*" -Recurse

if ($files.Count -eq 0) {
    Write-Warning "No files found matching pattern: $pattern"
    exit 1
}

Write-Host "Found $($files.Count) matching files" -ForegroundColor Green

# Deploy or retrieve
if ($action -eq "push") {
    foreach ($file in $files) {
        Write-Host "Deploying: $($file.FullName)" -ForegroundColor Cyan
        sf project deploy start --source-dir $file.FullName --target-org $org
    }
} else {
    # Pull logic
    Write-Host "Retrieving files..." -ForegroundColor Cyan
    sf project retrieve start --source-dir $baseDir --target-org $org
}
```

---

## Common Patterns

### Batch File Processing

```powershell
# Process all files in directory
$files = Get-ChildItem -Path "C:\Input" -Filter "*.txt"

foreach ($file in $files) {
    try {
        Write-Host "Processing: $($file.Name)"
        
        # Read and process
        $content = Get-Content -Path $file.FullName
        $processed = $content.ToUpper()
        
        # Write to output
        $outputPath = Join-Path "C:\Output" $file.Name
        Set-Content -Path $outputPath -Value $processed
        
        Write-Host "✓ Completed: $($file.Name)" -ForegroundColor Green
        
    } catch {
        Write-Error "✗ Failed: $($file.Name) - $($_.Exception.Message)"
    }
}
```

### Parallel Processing

```powershell
# Process files in parallel (PowerShell 7+)
$files = Get-ChildItem -Path "C:\Input" -Filter "*.txt"

$files | ForEach-Object -Parallel {
    $file = $_
    Write-Host "Processing: $($file.Name)"
    
    # Process file
    $content = Get-Content -Path $file.FullName
    $processed = $content.ToUpper()
    
    # Write output
    $outputPath = Join-Path "C:\Output" $file.Name
    Set-Content -Path $outputPath -Value $processed
    
} -ThrottleLimit 5  # Max 5 parallel jobs
```

### REST API Calls

```powershell
# GET request
$response = Invoke-RestMethod -Uri "https://api.example.com/data" -Method Get

# POST request with JSON body
$body = @{
    name = "John Doe"
    email = "john@example.com"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://api.example.com/users" -Method Post -Body $body -ContentType "application/json"

# With authentication
$headers = @{
    "Authorization" = "Bearer $token"
}

$response = Invoke-RestMethod -Uri "https://api.example.com/data" -Headers $headers

# Error handling
try {
    $response = Invoke-RestMethod -Uri $url -ErrorAction Stop
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    Write-Error "API call failed with status $statusCode"
}
```

### Progress Reporting

```powershell
$files = Get-ChildItem -Path "C:\Input" -Filter "*.txt"
$total = $files.Count
$current = 0

foreach ($file in $files) {
    $current++
    $percentComplete = ($current / $total) * 100
    
    Write-Progress -Activity "Processing Files" `
                   -Status "File $current of $total" `
                   -PercentComplete $percentComplete `
                   -CurrentOperation $file.Name
    
    # Process file
    Start-Sleep -Milliseconds 500  # Simulate work
}

Write-Progress -Activity "Processing Files" -Completed
```

---

## Best Practices

### 1. Use Approved Verbs

```powershell
# ✅ CORRECT - Use approved verbs
function Get-UserData { }
function Set-Configuration { }
function New-Report { }
function Remove-TempFiles { }

# ❌ WRONG - Don't use custom verbs
function Fetch-UserData { }
function Change-Configuration { }

# Get approved verbs
Get-Verb
```

### 2. Parameter Validation

```powershell
function Deploy-Code {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]$Path,
        
        [Parameter(Mandatory=$true)]
        [ValidateSet("dev", "test", "prod")]
        [string]$Environment,
        
        [Parameter(Mandatory=$false)]
        [ValidateRange(1, 100)]
        [int]$Timeout = 30
    )
    
    # Function logic
}
```

### 3. Use CmdletBinding

```powershell
function Process-Data {
    [CmdletBinding(SupportsShouldProcess=$true)]
    param(
        [string]$Data
    )
    
    # Enables -Verbose, -Debug, -WhatIf, -Confirm
    Write-Verbose "Processing: $Data"
    
    if ($PSCmdlet.ShouldProcess($Data, "Process")) {
        # Actual processing
    }
}
```

### 4. Return Objects, Not Strings

```powershell
# ❌ WRONG
function Get-FileInfo {
    param([string]$Path)
    return "File: $Path, Size: $size"
}

# ✅ CORRECT
function Get-FileInfo {
    param([string]$Path)
    
    $file = Get-Item $Path
    
    return [PSCustomObject]@{
        Name = $file.Name
        Path = $file.FullName
        Size = $file.Length
        Modified = $file.LastWriteTime
    }
}

# Can now use in pipeline
Get-FileInfo "file.txt" | Select-Object Name, Size
```

### 5. Use Splatting for Readability

```powershell
# ❌ Hard to read
Invoke-RestMethod -Uri "https://api.example.com" -Method Post -Headers @{"Authorization"="Bearer $token"} -Body $body -ContentType "application/json"

# ✅ Better with splatting
$params = @{
    Uri = "https://api.example.com"
    Method = "Post"
    Headers = @{"Authorization" = "Bearer $token"}
    Body = $body
    ContentType = "application/json"
}
Invoke-RestMethod @params
```

### 6. Comment Your Code

```powershell
<#
.SYNOPSIS
    Deploys Salesforce components to target org
    
.DESCRIPTION
    Deploys Lightning Web Components, Apex classes, or other metadata
    to a Salesforce org using the Salesforce CLI
    
.PARAMETER Type
    Component type (lwc, apex, object, trigger)
    
.PARAMETER Pattern
    File pattern to match (supports wildcards)
    
.PARAMETER Org
    Target org alias
    
.EXAMPLE
    .\Deploy-Components.ps1 -Type lwc -Pattern "cmn_Workflow*" -Org dmedev5
    
.NOTES
    Requires Salesforce CLI to be installed and authenticated
#>
```

---

## Troubleshooting

### Issue 1: Execution Policy Error

**Problem:** "cannot be loaded because running scripts is disabled"

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 2: Path Not Found

**Problem:** Script can't find files or directories

**Solution:**
```powershell
# Use absolute paths or resolve relative paths
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$filePath = Join-Path $scriptDir "data\file.txt"

# Or use $PSScriptRoot (PowerShell 3.0+)
$filePath = Join-Path $PSScriptRoot "data\file.txt"
```

### Issue 3: JSON Parsing Errors

**Problem:** ConvertFrom-Json fails

**Solution:**
```powershell
try {
    $json = Get-Content -Path "file.json" -Raw | ConvertFrom-Json
} catch {
    Write-Error "Invalid JSON: $($_.Exception.Message)"
    # Check file encoding (should be UTF-8)
}
```

### Issue 4: Command Not Found

**Problem:** "The term 'sf' is not recognized"

**Solution:**
```powershell
# Check if SF CLI is installed
Get-Command sf

# If not found, add to PATH or use full path
$sfPath = "C:\Program Files\Salesforce CLI\bin\sf.exe"
& $sfPath org list
```

### Issue 5: Permission Denied

**Problem:** Access denied when writing files

**Solution:**
```powershell
# Check if file is read-only
$file = Get-Item "file.txt"
if ($file.IsReadOnly) {
    $file.IsReadOnly = $false
}

# Run as administrator if needed
# Right-click PowerShell → Run as Administrator
```

---

## Quick Reference

### Most Common Commands

```powershell
# File operations
Get-ChildItem -Path "C:\Projects" -Filter "*.txt" -Recurse
Copy-Item -Path "source.txt" -Destination "dest.txt"
Move-Item -Path "file.txt" -Destination "C:\NewLocation"
Remove-Item -Path "file.txt" -Force

# String operations
$text.ToUpper()
$text.Replace("old", "new")
$text -match "pattern"

# Error handling
try { } catch { Write-Error $_.Exception.Message }

# Logging
Write-Host "Message" -ForegroundColor Green
Write-Error "Error message"
Write-Verbose "Verbose message"

# Salesforce CLI
sf project deploy start --source-dir "path" --target-org org
sf apex run --file "script.apex" --target-org org
sf org list

# Load credentials
$envs = & 'G:\My Drive\03_Areas\Keys\Environments\Load-Environments.ps1'
```

---

## Related Documentation

- **Salesforce Development:** `Salesforce_Development_Master_Guide.md`
- **Azure DevOps Automation:** `MASTER_GUIDE_AZURE_DEVOPS_AUTOMATION.md`
- **Credentials Management:** `MASTER_GUIDE_ENVIRONMENTS_AND_CREDENTIALS.md`
- **PowerShell Documentation:** https://docs.microsoft.com/powershell/

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-26 | Initial creation with comprehensive PowerShell patterns |
