# MASTER GUIDE: KeePass Integration

**Accessing and Searching KeePass Database from Scripts**

**Last Updated:** February 22, 2026  
**Version:** 1.0.0

---

## Table of Contents

1. [Overview](#overview)
2. [KeePass Database Location](#keepass-database-location)
3. [Python Integration](#python-integration)
4. [PowerShell Integration](#powershell-integration)
5. [Search Examples](#search-examples)
6. [Security Best Practices](#security-best-practices)
7. [Common Use Cases](#common-use-cases)
8. [Troubleshooting](#troubleshooting)

---

## Overview

This guide shows how to programmatically access your KeePass database to retrieve credentials for automation scripts.

### What You Can Do

- ✅ Search for credentials by title, username, or URL
- ✅ Retrieve passwords securely
- ✅ Prompt for master password at runtime
- ✅ Integrate with automation scripts
- ✅ Avoid hardcoding credentials

### What You Should NOT Do

- ❌ Store master password in scripts
- ❌ Log or print passwords
- ❌ Leave database unlocked
- ❌ Share master password

---

## KeePass Database Location

**Primary Database:** `G:\My Drive\03_Areas\Keys\keys pass.kdbx`

**Backup Databases:** `G:\My Drive\03_Areas\Keys\Backup\`

---

## Python Integration

### Installation

```powershell
pip install pykeepass
```

### Basic Usage - Prompt for Password

```python
#!/usr/bin/env python3
"""
KeePass credential retrieval with password prompt
"""

from pykeepass import PyKeePass
import getpass
import os

# KeePass database path
KEEPASS_DB = r'G:\My Drive\03_Areas\Keys\keys pass.kdbx'

def open_keepass():
    """Open KeePass database with password prompt"""
    if not os.path.exists(KEEPASS_DB):
        raise FileNotFoundError(f"KeePass database not found at {KEEPASS_DB}")
    
    # Prompt for master password (hidden input)
    master_password = getpass.getpass("Enter KeePass master password: ")
    
    try:
        kp = PyKeePass(KEEPASS_DB, password=master_password)
        print("✅ KeePass database unlocked")
        return kp
    except Exception as e:
        print(f"❌ Failed to unlock database: {e}")
        return None

def search_by_title(kp, title):
    """Search for entry by title"""
    entry = kp.find_entries(title=title, first=True)
    if entry:
        return {
            'title': entry.title,
            'username': entry.username,
            'password': entry.password,
            'url': entry.url,
            'notes': entry.notes
        }
    return None

def search_by_username(kp, username):
    """Search for entry by username"""
    entry = kp.find_entries(username=username, first=True)
    if entry:
        return {
            'title': entry.title,
            'username': entry.username,
            'password': entry.password,
            'url': entry.url
        }
    return None

def search_by_url(kp, url):
    """Search for entry by URL"""
    entry = kp.find_entries(url=url, first=True)
    if entry:
        return {
            'title': entry.title,
            'username': entry.username,
            'password': entry.password,
            'url': entry.url
        }
    return None

def list_all_entries(kp):
    """List all entry titles (for reference)"""
    entries = kp.find_entries()
    return [entry.title for entry in entries]

# Example usage
if __name__ == '__main__':
    # Open database with password prompt
    kp = open_keepass()
    
    if kp:
        # Search for a credential
        cred = search_by_title(kp, "Gmail")
        
        if cred:
            print(f"\nFound credential:")
            print(f"  Title: {cred['title']}")
            print(f"  Username: {cred['username']}")
            print(f"  Password: {'*' * len(cred['password'])}")  # Don't print actual password
            print(f"  URL: {cred['url']}")
        else:
            print("Credential not found")
        
        # List all available entries
        print("\nAvailable entries:")
        for title in list_all_entries(kp):
            print(f"  - {title}")
```

### Advanced Usage - Credential Helper Script

```python
#!/usr/bin/env python3
"""
KeePass Credential Helper
Usage: python keepass_helper.py <search_term>
"""

import sys
from pykeepass import PyKeePass
import getpass

KEEPASS_DB = r'G:\My Drive\03_Areas\Keys\keys pass.kdbx'

class KeePassHelper:
    def __init__(self):
        self.kp = None
    
    def unlock(self):
        """Unlock database with password prompt"""
        password = getpass.getpass("KeePass master password: ")
        try:
            self.kp = PyKeePass(KEEPASS_DB, password=password)
            return True
        except:
            print("❌ Invalid password or database error")
            return False
    
    def search(self, search_term):
        """Search for credential by title, username, or URL"""
        if not self.kp:
            return None
        
        # Try searching by title first
        entry = self.kp.find_entries(title=search_term, first=True)
        
        # If not found, try username
        if not entry:
            entry = self.kp.find_entries(username=search_term, first=True)
        
        # If still not found, try URL
        if not entry:
            entry = self.kp.find_entries(url=f"*{search_term}*", first=True)
        
        if entry:
            return {
                'title': entry.title,
                'username': entry.username,
                'password': entry.password,
                'url': entry.url,
                'notes': entry.notes
            }
        return None
    
    def get_password(self, search_term):
        """Get just the password for a credential"""
        cred = self.search(search_term)
        return cred['password'] if cred else None
    
    def get_username(self, search_term):
        """Get just the username for a credential"""
        cred = self.search(search_term)
        return cred['username'] if cred else None

def main():
    if len(sys.argv) < 2:
        print("Usage: python keepass_helper.py <search_term>")
        sys.exit(1)
    
    search_term = sys.argv[1]
    
    helper = KeePassHelper()
    if helper.unlock():
        cred = helper.search(search_term)
        
        if cred:
            print(f"\n✅ Found: {cred['title']}")
            print(f"Username: {cred['username']}")
            print(f"Password: {cred['password']}")
            if cred['url']:
                print(f"URL: {cred['url']}")
            if cred['notes']:
                print(f"Notes: {cred['notes']}")
        else:
            print(f"❌ No credential found for '{search_term}'")

if __name__ == '__main__':
    main()
```

**Usage:**
```powershell
# Search for Gmail credentials
python keepass_helper.py Gmail

# Search for Todoist
python keepass_helper.py Todoist

# Search by username
python keepass_helper.py sol9001@gmail.com
```

---

## PowerShell Integration

### Using KeePass CLI (KeePassXC)

**Install KeePassXC:**
- Download from: https://keepassxc.org/download/
- Includes CLI tool: `keepassxc-cli`

### PowerShell Script

```powershell
# KeePass credential retrieval using KeePassXC CLI
param(
    [Parameter(Mandatory=$true)]
    [string]$SearchTerm
)

$KeePassDB = "G:\My Drive\03_Areas\Keys\keys pass.kdbx"
$KeePassCLI = "C:\Program Files\KeePassXC\keepassxc-cli.exe"

# Check if KeePassXC CLI is installed
if (-not (Test-Path $KeePassCLI)) {
    Write-Error "KeePassXC CLI not found. Install from https://keepassxc.org/"
    exit 1
}

# Check if database exists
if (-not (Test-Path $KeePassDB)) {
    Write-Error "KeePass database not found at $KeePassDB"
    exit 1
}

# Prompt for master password (secure)
$SecurePassword = Read-Host "Enter KeePass master password" -AsSecureString
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecurePassword)
$Password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# Search for entry
Write-Host "Searching for '$SearchTerm'..." -ForegroundColor Cyan

# Use KeePassXC CLI to search
$result = & $KeePassCLI search $KeePassDB $SearchTerm --password $Password 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Found credential:" -ForegroundColor Green
    Write-Host $result
} else {
    Write-Host "`n❌ Credential not found or error occurred" -ForegroundColor Red
}

# Clear password from memory
$Password = $null
[System.GC]::Collect()
```

**Usage:**
```powershell
.\Get-KeePassCredential.ps1 -SearchTerm "Gmail"
```

### Alternative: Using KeePass PowerShell Module

```powershell
# Install KeePass PowerShell module
Install-Module -Name PoShKeePass -Scope CurrentUser

# Import module
Import-Module PoShKeePass

# Open database with password prompt
$KeePassDB = "G:\My Drive\03_Areas\Keys\keys pass.kdbx"
$MasterPassword = Read-Host "KeePass master password" -AsSecureString

# Get database connection
$KeePassConnection = New-KeePassConnection -Database $KeePassDB -MasterPassword $MasterPassword

# Search for entry
$Entry = Get-KeePassEntry -KeePassConnection $KeePassConnection -Title "Gmail"

if ($Entry) {
    Write-Host "✅ Found: $($Entry.Title)"
    Write-Host "Username: $($Entry.UserName)"
    Write-Host "Password: $($Entry.Password)"
    Write-Host "URL: $($Entry.URL)"
} else {
    Write-Host "❌ Entry not found"
}

# Close connection
Remove-KeePassConnection -KeePassConnection $KeePassConnection
```

---

## Search Examples

### Example 1: Get Gmail Credentials

```python
from keepass_helper import KeePassHelper

helper = KeePassHelper()
if helper.unlock():
    username = helper.get_username("Gmail")
    password = helper.get_password("Gmail")
    
    # Use credentials
    print(f"Gmail: {username}")
```

### Example 2: Get Todoist API Token

```python
helper = KeePassHelper()
if helper.unlock():
    todoist_cred = helper.search("Todoist")
    api_token = todoist_cred['password']  # API token stored as password
    
    # Use in API call
    import requests
    headers = {'Authorization': f'Bearer {api_token}'}
```

### Example 3: Get Salesforce Credentials

```python
helper = KeePassHelper()
if helper.unlock():
    sf_cred = helper.search("Salesforce")
    
    username = sf_cred['username']
    password = sf_cred['password']
    security_token = sf_cred['notes']  # Security token in notes
```

### Example 4: List All Available Credentials

```python
from pykeepass import PyKeePass
import getpass

password = getpass.getpass("KeePass password: ")
kp = PyKeePass(KEEPASS_DB, password=password)

print("Available credentials:")
for entry in kp.find_entries():
    print(f"  - {entry.title} ({entry.username})")
```

---

## Security Best Practices

### DO:
- ✅ Always prompt for master password at runtime
- ✅ Use `getpass` for hidden password input
- ✅ Clear passwords from memory after use
- ✅ Use secure string types in PowerShell
- ✅ Close database connection when done
- ✅ Store API tokens in password field or notes

### DON'T:
- ❌ Hardcode master password in scripts
- ❌ Store master password in environment variables
- ❌ Print passwords to console (use `*` masking)
- ❌ Log passwords to files
- ❌ Leave database unlocked indefinitely
- ❌ Share master password via email/chat

### Password Prompt Best Practices

```python
# Good - Hidden input
import getpass
password = getpass.getpass("Master password: ")

# Bad - Visible input
password = input("Master password: ")  # DON'T DO THIS

# Good - Clear from memory after use
password = None
import gc
gc.collect()
```

---

## Common Use Cases

### Use Case 1: Email Automation

```python
from keepass_helper import KeePassHelper
import smtplib

helper = KeePassHelper()
if helper.unlock():
    gmail_cred = helper.search("Gmail")
    
    # Use credentials for SMTP
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(gmail_cred['username'], gmail_cred['password'])
    # Send email...
    server.quit()
```

### Use Case 2: API Integration

```python
helper = KeePassHelper()
if helper.unlock():
    api_cred = helper.search("MyAPI")
    api_key = api_cred['password']
    
    # Use in requests
    import requests
    response = requests.get(
        'https://api.example.com/data',
        headers={'Authorization': f'Bearer {api_key}'}
    )
```

### Use Case 3: Database Connection

```python
helper = KeePassHelper()
if helper.unlock():
    db_cred = helper.search("PostgreSQL")
    
    import psycopg2
    conn = psycopg2.connect(
        host=db_cred['url'],
        database=db_cred['notes'],  # DB name in notes
        user=db_cred['username'],
        password=db_cred['password']
    )
```

### Use Case 4: Integration with Existing Scripts

```python
# In your automation script
from keepass_helper import KeePassHelper

def get_credential(service_name):
    """Get credential from KeePass"""
    helper = KeePassHelper()
    if helper.unlock():
        return helper.search(service_name)
    return None

# Use in script
todoist_cred = get_credential("Todoist")
if todoist_cred:
    TODOIST_TOKEN = todoist_cred['password']
    # Continue with automation...
```

---

## Troubleshooting

### Error: "Database not found"

**Cause:** KeePass database path is incorrect

**Solution:**
```python
import os
KEEPASS_DB = r'G:\My Drive\03_Areas\Keys\keys pass.kdbx'
if not os.path.exists(KEEPASS_DB):
    print(f"Database not found at: {KEEPASS_DB}")
    print("Check the path and try again")
```

### Error: "Invalid password"

**Cause:** Incorrect master password

**Solution:**
- Verify master password is correct
- Check for caps lock
- Try opening in KeePass GUI to verify

### Error: "Module 'pykeepass' not found"

**Cause:** Python library not installed

**Solution:**
```powershell
pip install pykeepass
```

### Error: "Permission denied"

**Cause:** Database file is locked or in use

**Solution:**
- Close KeePass GUI application
- Check if another script has database open
- Verify file permissions

### Entry Not Found

**Cause:** Search term doesn't match entry title

**Solution:**
```python
# List all entries to find exact title
kp = open_keepass()
for entry in kp.find_entries():
    print(entry.title)
```

---

## Integration with Master Guides

### Update environments.json Fallback

```python
# Check KeePass first, then environments.json
from keepass_helper import KeePassHelper
import json

def get_credential(service_name):
    """Get credential from KeePass or environments.json"""
    
    # Try KeePass first
    helper = KeePassHelper()
    if helper.unlock():
        cred = helper.search(service_name)
        if cred:
            return cred
    
    # Fallback to environments.json
    env_file = r'G:\My Drive\03_Areas\Keys\Environments\environments.json'
    with open(env_file, 'r') as f:
        env_config = json.load(f)
    
    # Search in environments
    if service_name.lower() in env_config.get('environments', {}):
        return env_config['environments'][service_name.lower()]
    
    return None
```

---

## Quick Reference

### Python Commands

```python
# Open database
from pykeepass import PyKeePass
import getpass
kp = PyKeePass(KEEPASS_DB, password=getpass.getpass())

# Search by title
entry = kp.find_entries(title="Gmail", first=True)

# Search by username
entry = kp.find_entries(username="user@example.com", first=True)

# Get password
password = entry.password

# List all entries
entries = kp.find_entries()
```

### PowerShell Commands

```powershell
# Using PoShKeePass module
Import-Module PoShKeePass
$conn = New-KeePassConnection -Database $db -MasterPassword $pass
$entry = Get-KeePassEntry -KeePassConnection $conn -Title "Gmail"
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-22 | Initial release with Python and PowerShell integration examples |

---

**End of Master Guide**

For credential management best practices, see [MASTER_GUIDE_Environments_and_Credentials.md](MASTER_GUIDE_Environments_and_Credentials.md)
