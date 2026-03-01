# Skills Repository Configuration Guide

## Overview

This repository uses a configurable root path system to support cloning to different locations. All skill paths in documentation use the `${SKILLS_ROOT}` placeholder, which you replace with your actual repository location.

---

## Quick Setup

### 1. Configure Your Root Path

Edit `skills_config.json` in the repository root:

```json
{
  "SKILLS_ROOT": "YOUR_PATH_HERE"
}
```

**Examples by Platform:**

**Windows:**
```json
{
  "SKILLS_ROOT": "C:\\Users\\YourName\\Documents\\06_Skills"
}
```

**Linux:**
```json
{
  "SKILLS_ROOT": "/home/username/06_Skills"
}
```

**macOS:**
```json
{
  "SKILLS_ROOT": "/Users/username/Documents/06_Skills"
}
```

**Google Drive (Windows):**
```json
{
  "SKILLS_ROOT": "G:\\My Drive\\06_Skills"
}
```

### 2. Using Paths in Documentation

All documentation uses the `${SKILLS_ROOT}` placeholder format:

**Documentation shows:**
```
${SKILLS_ROOT}/automation/skill_daily_planning.md
```

**You use (example with C:\Skills):**
```
C:\Skills\automation\skill_daily_planning.md
```

---

## Platform-Specific Instructions

### Windows (PowerShell/Command Prompt)

**Path Format:** Use backslashes with proper escaping in JSON
```json
{
  "SKILLS_ROOT": "C:\\Users\\YourName\\Documents\\06_Skills"
}
```

**Using in Commands:**
```powershell
# Navigate to skills directory
cd "C:\Users\YourName\Documents\06_Skills\_tools"

# Reference a skill file
Get-Content "C:\Users\YourName\Documents\06_Skills\automation\skill_daily_planning.md"
```

**Environment Variable (Optional):**
```powershell
# Set temporary environment variable
$env:SKILLS_ROOT = "C:\Users\YourName\Documents\06_Skills"

# Use in commands
cd "$env:SKILLS_ROOT\_tools"
```

### Linux/macOS (Bash/Zsh)

**Path Format:** Use forward slashes
```json
{
  "SKILLS_ROOT": "/home/username/06_Skills"
}
```

**Using in Commands:**
```bash
# Navigate to skills directory
cd /home/username/06_Skills/_tools

# Reference a skill file
cat /home/username/06_Skills/automation/skill_daily_planning.md
```

**Environment Variable (Optional):**
```bash
# Add to ~/.bashrc or ~/.zshrc
export SKILLS_ROOT="/home/username/06_Skills"

# Use in commands
cd "$SKILLS_ROOT/_tools"
```

### Devin AI (Workspace)

**Path Format:** Typically `/workspace/skills`
```json
{
  "SKILLS_ROOT": "/workspace/skills"
}
```

**Clone and Configure:**
```bash
# Clone to workspace
git clone https://github.com/adourish/skills.git /workspace/skills

# Update config
cd /workspace/skills
nano skills_config.json
# Update SKILLS_ROOT to "/workspace/skills"

# Use in commands
cat /workspace/skills/automation/skill_daily_planning.md
```

---

## AI Assistant Integration

### Windsurf Cascade

**Method 1: Direct Path Substitution**
```
"Load the skill at C:\Skills\automation\skill_daily_planning.md"
```

**Method 2: Ask Cascade to Read Config**
```
"Read skills_config.json and then load the daily_planning skill"
```

**Method 3: Provide Context**
```
"My SKILLS_ROOT is C:\Skills. Load the daily_planning skill."
```

### Claude Code

**Method 1: Use @ Mentions with Full Path**
```
@C:\Skills\automation\skill_daily_planning.md
```

**Method 2: Reference Config First**
```
@skills_config.json
Then: "Load the daily_planning skill"
```

### Devin AI

**Method 1: Use Full Workspace Path**
```bash
cat /workspace/skills/automation/skill_daily_planning.md
```

**Method 2: Set Environment Variable**
```bash
export SKILLS_ROOT="/workspace/skills"
cat $SKILLS_ROOT/automation/skill_daily_planning.md
```

---

## Converting Documentation Paths

### Pattern Replacement

**Find:** `${SKILLS_ROOT}`  
**Replace with:** Your actual path from `skills_config.json`

### Examples

| Documentation Path | Your Config | Actual Path |
|-------------------|-------------|-------------|
| `${SKILLS_ROOT}/automation/skill_daily_planning.md` | `C:\Skills` | `C:\Skills\automation\skill_daily_planning.md` |
| `${SKILLS_ROOT}/_tools/run_process_new.py` | `/home/user/06_Skills` | `/home/user/06_Skills/_tools/run_process_new.py` |
| `${SKILLS_ROOT}/documentation/mermaid-diagrams/` | `G:\My Drive\06_Skills` | `G:\My Drive\06_Skills\documentation\mermaid-diagrams\` |

---

## Troubleshooting

### Issue: "Path not found"

**Check:**
1. Verify `skills_config.json` has correct path
2. Ensure path uses correct slashes for your OS (\ for Windows, / for Linux/Mac)
3. Check for typos in path
4. Verify repository is actually at that location

**Test:**
```powershell
# Windows
Test-Path "C:\Users\YourName\Documents\06_Skills"

# Linux/Mac
ls -la /home/username/06_Skills
```

### Issue: "Invalid JSON in skills_config.json"

**Common mistakes:**
- Forgot to escape backslashes: `C:\Skills` should be `C:\\Skills`
- Missing quotes around path
- Trailing comma in JSON

**Valid format:**
```json
{
  "SKILLS_ROOT": "C:\\Users\\Name\\06_Skills"
}
```

### Issue: "AI can't find skills"

**Solutions:**
1. Provide full path directly to AI
2. Reference `skills_config.json` first, then ask for skill
3. Use absolute paths in commands instead of placeholders

---

## Advanced: Programmatic Access

### Python

```python
import json
import os

# Load config
with open('skills_config.json', 'r') as f:
    config = json.load(f)

SKILLS_ROOT = config['SKILLS_ROOT']

# Build paths
daily_planning = os.path.join(SKILLS_ROOT, 'automation', 'skill_daily_planning.md')
print(f"Skill path: {daily_planning}")
```

### PowerShell

```powershell
# Load config
$config = Get-Content skills_config.json | ConvertFrom-Json
$SKILLS_ROOT = $config.SKILLS_ROOT

# Build paths
$dailyPlanning = Join-Path $SKILLS_ROOT "automation\skill_daily_planning.md"
Write-Host "Skill path: $dailyPlanning"
```

### Bash

```bash
# Load config (requires jq)
SKILLS_ROOT=$(jq -r '.SKILLS_ROOT' skills_config.json)

# Build paths
daily_planning="$SKILLS_ROOT/automation/skill_daily_planning.md"
echo "Skill path: $daily_planning"
```

---

## Migration from Hardcoded Paths

If you have existing scripts or notes with hardcoded paths:

### Find and Replace

**Old format:**
```
G:\My Drive\06_Skills\automation\skill_daily_planning.md
```

**New format:**
```
${SKILLS_ROOT}/automation/skill_daily_planning.md
```

### Regex Pattern (for bulk updates)

**Find:** `G:\\My Drive\\06_Skills\\`  
**Replace:** `${SKILLS_ROOT}/`

**Or for forward slashes:**  
**Find:** `G:/My Drive/06_Skills/`  
**Replace:** `${SKILLS_ROOT}/`

---

## Best Practices

1. **Always update `skills_config.json` first** when cloning to a new location
2. **Use forward slashes in documentation** - they work on all platforms
3. **Escape backslashes in JSON** - `C:\Skills` becomes `C:\\Skills`
4. **Test your path** before running complex commands
5. **Share your config** with AI assistants at the start of sessions
6. **Keep config.json in .gitignore** if paths are user-specific (optional)

---

## Support

If you encounter issues with path configuration:

1. Check this guide's Troubleshooting section
2. Verify your `skills_config.json` syntax
3. Test paths manually in your terminal/command prompt
4. Ensure repository is fully cloned and accessible
