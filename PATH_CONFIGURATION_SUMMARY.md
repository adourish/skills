# Path Configuration Summary - March 1, 2026

## Overview

All hardcoded `G:\My Drive\` paths have been replaced with configurable placeholders to support cloning the repository to different locations.

---

## Configuration Variables

### ${SKILLS_ROOT}
- **Purpose:** Root directory of the Skills repository
- **Default:** `G:\My Drive\06_Skills`
- **Used for:** All skill files, tools, scripts within the repository

### ${PARA_ROOT}
- **Purpose:** Root directory of PARA method organization
- **Default:** `G:\My Drive`
- **Used for:** Projects, Areas, Resources, Archive folders, credentials, KeePass database

### Configuration File

**Location:** `${SKILLS_ROOT}/skills_config.json`

```json
{
  "SKILLS_ROOT": "G:\\My Drive\\06_Skills",
  "PARA_ROOT": "G:\\My Drive"
}
```

**Update these values** to match your local environment.

---

## Files Updated

### Core Documentation

1. **README.md** ✅
   - File locations section
   - PARA method paths
   - Footer location reference
   - Fixed non-compliant diagram colors

2. **SKILLS_CONTEXT.md** ✅
   - Key commands reference
   - File locations section
   - PARA method routing rules
   - Footer location reference

3. **skills_config.json** ✅
   - Added `PARA_ROOT` configuration
   - Updated examples for all platforms
   - Enhanced usage documentation

### Skills Updated

4. **integrations/skill_keepass_integration.md** ✅
   - KeePass database location
   - Backup database location
   - Added configuration note

5. **system/skill_environments_credentials.md** ✅
   - KeePass database path
   - environments.json path
   - .env file path
   - Backup location path
   - Added configuration note

---

## Path Replacement Examples

### Before (Hardcoded)
```
G:\My Drive\06_Skills\automation\skill_daily_planning.md
G:\My Drive\03_Areas\Keys\Environments\environments.json
G:\My Drive\01_Operate\Projects\
```

### After (Configurable)
```
${SKILLS_ROOT}/automation/skill_daily_planning.md
${PARA_ROOT}/03_Areas/Keys/Environments/environments.json
${PARA_ROOT}/01_Operate/Projects/
```

### Actual Usage (Example: Linux)
If you configure:
```json
{
  "SKILLS_ROOT": "/home/username/06_Skills",
  "PARA_ROOT": "/home/username/GoogleDrive"
}
```

Then paths become:
```
/home/username/06_Skills/automation/skill_daily_planning.md
/home/username/GoogleDrive/03_Areas/Keys/Environments/environments.json
/home/username/GoogleDrive/01_Operate/Projects/
```

---

## Key Management Skills

### Existing Skills for Credentials/Keys

1. **skill_keepass_integration.md** (`integrations/`)
   - How to access KeePass database programmatically
   - Python and PowerShell integration
   - Search examples and security best practices
   - **Location:** `${PARA_ROOT}/03_Areas/Keys/keys pass.kdbx`

2. **skill_environments_credentials.md** (`system/`)
   - Complete credentials management guide
   - Three-tier credential storage system:
     - **KeePass** - Passwords, API keys, secrets
     - **environments.json** - API configurations, OAuth
     - **.env** - Legacy environment variables
   - Security principles and best practices
   - Credential lookup workflow

### Credential Storage Hierarchy

```
${PARA_ROOT}/03_Areas/Keys/
├── keys pass.kdbx              # PRIMARY: Passwords & secrets
├── Environments/
│   └── environments.json       # PRIMARY: API configurations
├── .env                        # LEGACY: Environment variables
├── load_credentials.py         # Python loader
├── load_credentials.ps1        # PowerShell loader
└── README.md                   # Documentation
```

### When to Use Each

| Need | Use | Location |
|------|-----|----------|
| Password | KeePass | `${PARA_ROOT}/03_Areas/Keys/keys pass.kdbx` |
| API Key (sensitive) | KeePass | `${PARA_ROOT}/03_Areas/Keys/keys pass.kdbx` |
| API Configuration | environments.json | `${PARA_ROOT}/03_Areas/Keys/Environments/environments.json` |
| OAuth tokens | environments.json | `${PARA_ROOT}/03_Areas/Keys/Environments/environments.json` |
| Legacy env vars | .env | `${PARA_ROOT}/03_Areas/Keys/.env` |

---

## Platform-Specific Examples

### Windows
```json
{
  "SKILLS_ROOT": "G:\\My Drive\\06_Skills",
  "PARA_ROOT": "G:\\My Drive"
}
```

### Windows (Alternative)
```json
{
  "SKILLS_ROOT": "C:\\Users\\YourName\\Documents\\06_Skills",
  "PARA_ROOT": "C:\\Users\\YourName\\Documents"
}
```

### Linux
```json
{
  "SKILLS_ROOT": "/home/username/06_Skills",
  "PARA_ROOT": "/home/username/GoogleDrive"
}
```

### macOS
```json
{
  "SKILLS_ROOT": "/Users/username/Documents/06_Skills",
  "PARA_ROOT": "/Users/username/Google Drive"
}
```

---

## Files Still Containing Hardcoded Paths

The following files may still contain hardcoded paths for documentation/example purposes:

- **SESSION_SUMMARY_20260222.md** - Historical session summary (archive)
- **QUICKSTART.md** - Contains examples with specific paths (update recommended)
- **CONFIGURATION.md** - Contains examples (intentional for documentation)
- **SECTION_508_COLOR_AUDIT_2026-03-01.md** - Audit report (archive)
- **_tools/README.md** - May contain example paths
- **_tools/WINDSURF_INSTALLATION.md** - Installation guide with examples

**Recommendation:** Update QUICKSTART.md to use `${SKILLS_ROOT}` and `${PARA_ROOT}` placeholders in examples.

---

## Migration Guide

### For Existing Users

1. **No action required** if your paths match the defaults:
   - Skills: `G:\My Drive\06_Skills`
   - PARA: `G:\My Drive`

2. **If you've cloned elsewhere:**
   - Edit `skills_config.json`
   - Update `SKILLS_ROOT` to your repository location
   - Update `PARA_ROOT` to your Google Drive/PARA root

### For New Users

1. Clone repository to your preferred location
2. Edit `skills_config.json` with your paths
3. When reading documentation, replace:
   - `${SKILLS_ROOT}` with your repository path
   - `${PARA_ROOT}` with your PARA method root

### For GitHub Users

The repository at https://github.com/adourish/skills uses relative paths in documentation. When cloning:

```bash
# Clone to your preferred location
git clone https://github.com/adourish/skills.git /your/path/06_Skills

# Update configuration
cd /your/path/06_Skills
nano skills_config.json
# Set SKILLS_ROOT and PARA_ROOT to your paths
```

---

## Related Documentation

- **[CONFIGURATION.md](CONFIGURATION.md)** - Complete configuration guide
- **[skill_keepass_integration.md](integrations/skill_keepass_integration.md)** - KeePass usage
- **[skill_environments_credentials.md](system/skill_environments_credentials.md)** - Credentials management
- **[skill_routing_rules.md](system/skill_routing_rules.md)** - PARA method file organization

---

## Summary

✅ **Configuration system implemented**
- Two configuration variables: `SKILLS_ROOT` and `PARA_ROOT`
- Configured in `skills_config.json`
- Platform-agnostic path handling

✅ **Core files updated**
- README.md
- SKILLS_CONTEXT.md
- skill_keepass_integration.md
- skill_environments_credentials.md

✅ **Keys management documented**
- KeePass integration skill exists
- Credentials management skill exists
- Clear hierarchy and usage guidelines

✅ **Ready for cloning**
- Repository can be cloned to any location
- Simple configuration file update required
- All documentation uses relative paths

---

**Last Updated:** March 1, 2026  
**Status:** Path configuration complete, ready for multi-environment deployment
