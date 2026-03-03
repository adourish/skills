# Skill: README Maintenance

**Category**: system  
**Priority**: MEDIUM  
**Last Updated**: March 3, 2026  
**Prerequisites**:
- Understanding of skills repository structure
- Familiarity with Markdown syntax
- Knowledge of Mermaid diagram syntax

---

## Overview

This skill provides procedures for maintaining the README.md file in the skills repository, ensuring all skills are properly documented in both the Mermaid diagram and text-based lists. Keeping the README synchronized with actual skill files is critical for discoverability and AI assistant integration.

## When to Use This Skill

- After creating new skills
- When reorganizing or renaming skills
- During periodic audits of the repository
- When skill counts don't match actual files
- Before major releases or documentation updates

## Prerequisites

- Access to skills repository
- Understanding of repository structure
- Familiarity with skill categories
- Knowledge of Markdown and Mermaid syntax

## Core Concepts

### README Structure

The README contains two main sections that must stay synchronized:

**1. Mermaid Diagram (Visual)**
- Located around line 291-467
- Shows skills as nodes in a graph
- Includes skill counts in category headers
- Uses ⭐ to mark featured/priority skills
- Section 508 compliant color styling

**2. Text-Based Lists (Searchable)**
- Located around line 1249-1343
- Organized by category with descriptions
- Includes direct links to skill files
- Easier for search and copy-paste

### Skill Categories

**🛠️ Tools** (`_tools/`) - Skill development and creation  
**🤖 Automation** (`automation/`) - Daily workflows and processes  
**🔌 Integrations** (`integrations/`) - API clients and service wrappers  
**💻 Development** (`development/`) - Dev tools and workflows  
**📝 Documentation** (`documentation/`) - Templates and diagram creation  
**⚙️ System** (`system/`) - Core configuration and setup

### Skill Counts

Track total skills and per-category counts:
- Update in diagram header: `Root["📁 06_Skills<br/>XX AI Skills<br/>6 Categories"]`
- Update in category nodes: `Development["💻 DEVELOPMENT<br/>XX Skills<br/>Dev Tools"]`
- Update in opening tagline: `**XX battle-tested skills. 6 categories. 3 AI platforms.**`

---

## Step-by-Step Instructions

### Task 1: Audit Existing Skills

**Objective**: Generate a complete list of all skill files in the repository

**PowerShell Script**:

```powershell
# Navigate to skills repository
cd c:\projects\POCs\src\dmedev5\skills

# Get all skill files by category
$categories = @{
    'Tools' = '_tools'
    'Automation' = 'automation'
    'Integrations' = 'integrations'
    'Development' = 'development'
    'Documentation' = 'documentation'
    'System' = 'system'
}

$allSkills = @()

foreach ($category in $categories.Keys) {
    $path = $categories[$category]
    
    # Find all .md files (excluding README files)
    $skills = Get-ChildItem -Path $path -Filter "*.md" -Recurse | 
        Where-Object { $_.Name -notmatch 'README' } |
        Select-Object @{N='Category';E={$category}}, Name, FullName
    
    $allSkills += $skills
    
    Write-Host "`n$category ($($skills.Count) skills):" -ForegroundColor Cyan
    $skills | ForEach-Object { Write-Host "  - $($_.Name)" }
}

Write-Host "`nTotal Skills: $($allSkills.Count)" -ForegroundColor Green

# Export to CSV for review
$allSkills | Export-Csv -Path "./skill-audit.csv" -NoTypeInformation
Write-Host "`nExported to skill-audit.csv" -ForegroundColor Yellow
```

**Expected Output**:
```
Tools (3 skills):
  - skill_creator.md
  - tool_filing.md
  - quick_filing.md

Automation (10 skills):
  - skill_daily_planning.md
  - skill_email_processing.md
  ...

Total Skills: 64
```

---

### Task 2: Verify Skills in Mermaid Diagram

**Objective**: Ensure all skills appear in the visual diagram

**Steps**:

1. **Open README.md**
   - Navigate to line ~291 (Mermaid diagram section)

2. **Check Category Counts**
   - Compare diagram counts with actual file counts
   - Example: `Development["💻 DEVELOPMENT<br/>19 Skills<br/>Dev Tools"]`

3. **Verify Each Skill Node**
   - Each skill should have a node like: `Development --> D1["skill_name<br/>Description"]`
   - Featured skills marked with ⭐: `Development --> D1["skill_name ⭐<br/>Description"]`

4. **Check Styling**
   - Each node should have a style definition
   - Example: `style D1 fill:#1b5e20,stroke:#ffffff,stroke-width:3px,color:#ffffff`

**Missing Skill Pattern**:

If a skill is missing, add it following this pattern:

```mermaid
Development --> D20["new_skill_name ⭐<br/>Short description"]
```

Then add styling:

```mermaid
style D20 fill:#1b5e20,stroke:#ffffff,stroke-width:3px,color:#ffffff
```

---

### Task 3: Verify Skills in Text Lists

**Objective**: Ensure all skills appear in searchable text sections

**Steps**:

1. **Navigate to Category Sections**
   - Tools: ~line 1249
   - Automation: ~line 1255
   - Integrations: ~line 1268
   - Development: ~line 1278
   - Documentation: ~line 1300
   - System: ~line 1332

2. **Check Each Skill Entry**
   - Format: `- **[skill_name](path/to/skill.md)** - Description`
   - Example: `- **[copado_user_stories](development/skill_copado_user_stories.md)** - Copado User Story creation and management`

3. **Verify Alphabetical/Logical Order**
   - Skills should be in logical order (not necessarily alphabetical)
   - Group related skills together

**Missing Skill Pattern**:

Add following this format:

```markdown
- **[skill_name](category/skill_name.md)** - Brief description of what the skill does
```

---

### Task 4: Update Skill Counts

**Objective**: Update all skill count references in README

**Locations to Update**:

1. **Opening Tagline** (line ~7):
   ```markdown
   **64 battle-tested skills. 6 categories. 3 AI platforms. Zero excuses for bad code.**
   ```

2. **Diagram Root Node** (line ~293):
   ```mermaid
   Root["📁 06_Skills<br/>64 AI Skills<br/>6 Categories"]
   ```

3. **Category Nodes** (lines ~295-300):
   ```mermaid
   Root --> Tools["🛠️ TOOLS<br/>3 Skills<br/>Skill Development"]
   Root --> Automation["🤖 AUTOMATION<br/>10 Skills<br/>Daily Workflows"]
   Root --> Integrations["🔌 INTEGRATIONS<br/>5 Skills<br/>API & Services"]
   Root --> Development["💻 DEVELOPMENT<br/>19 Skills<br/>Dev Tools"]
   Root --> Documentation["📝 DOCUMENTATION<br/>21 Skills<br/>Templates & Diagrams"]
   Root --> System["⚙️ SYSTEM<br/>11 Skills<br/>Core Configuration"]
   ```

**Calculation**:
- Count actual skill files per category
- Sum for total
- Update all three locations

---

### Task 5: Add New Skills to README

**Objective**: Complete workflow for adding new skills to README

**Complete Checklist**:

- [ ] **Create skill file** in appropriate category folder
- [ ] **Add to Mermaid diagram**:
  - [ ] Add node: `Category --> DXX["skill_name ⭐<br/>Description"]`
  - [ ] Add style: `style DXX fill:#color,stroke:#ffffff,stroke-width:3px,color:#ffffff`
  - [ ] Increment category count in node
- [ ] **Add to text list**:
  - [ ] Add entry: `- **[skill_name](path)** - Description`
  - [ ] Place in logical order within category
- [ ] **Update skill counts**:
  - [ ] Update opening tagline total
  - [ ] Update diagram root node total
  - [ ] Update category node count
- [ ] **Commit changes**:
  - [ ] `git add README.md`
  - [ ] `git commit -m "Add [skill_name] to README"`
  - [ ] `git push origin main`

**Example Commit Message**:

```
Add Copado skills to README

- Added 7 Copado skills to Development, Automation, and System categories
- Updated skill counts: 57 -> 64 total skills
- Added skills to both Mermaid diagram and text lists
- Updated opening tagline with Copado DevOps mention
```

---

## Common Patterns

### Pattern 1: Adding Single Skill

```markdown
1. Create skill file: development/skill_new_feature.md
2. Add to Mermaid diagram:
   Development --> D20["new_feature ⭐<br/>Feature description"]
   style D20 fill:#1b5e20,stroke:#ffffff,stroke-width:3px,color:#ffffff
3. Add to text list:
   - **[new_feature](development/skill_new_feature.md)** - Feature description
4. Update counts: Development 19 -> 20, Total 64 -> 65
5. Commit and push
```

---

### Pattern 2: Adding Multiple Related Skills

```markdown
1. Create all skill files in same category
2. Add all nodes to Mermaid diagram sequentially
3. Add all style definitions
4. Add all text list entries (keep grouped together)
5. Update counts once for all additions
6. Single commit with descriptive message
```

---

### Pattern 3: Reorganizing Skills

```markdown
1. Move/rename skill files
2. Update Mermaid diagram node references
3. Update text list paths
4. Update any cross-references in other skills
5. Test all links work
6. Commit with clear reorganization message
```

---

## Troubleshooting

### Issue 1: Skill Count Mismatch

**Symptom**: Diagram shows different count than actual files

**Solution**:

```powershell
# Count actual files
$actualCount = (Get-ChildItem -Path development -Filter "skill_*.md" -Recurse).Count
Write-Host "Actual Development skills: $actualCount"

# Check README
# Search for "DEVELOPMENT<br/>" in README
# Update count to match actual
```

---

### Issue 2: Missing Skill in Diagram

**Symptom**: Skill file exists but not in Mermaid diagram

**Solution**:

1. Find last skill node in category (e.g., `Development --> D19`)
2. Add new node: `Development --> D20["skill_name<br/>Description"]`
3. Add style: `style D20 fill:#1b5e20,stroke:#ffffff,stroke-width:3px,color:#ffffff`
4. Increment category count

---

### Issue 3: Broken Link in Text List

**Symptom**: Link doesn't work when clicked

**Solution**:

1. Verify file path is correct
2. Check file actually exists: `Test-Path development/skill_name.md`
3. Ensure path is relative to README location
4. Fix path in text list entry

---

## Best Practices

### Maintenance Schedule

**After Every New Skill**:
- Add to both diagram and text list immediately
- Update counts
- Commit changes

**Weekly Audit**:
- Run audit script to verify all skills listed
- Check for orphaned files
- Verify all links work

**Monthly Review**:
- Review skill descriptions for accuracy
- Update featured (⭐) skills based on usage
- Reorganize if categories become unbalanced

### Naming Conventions

**Skill Files**:
- Pattern: `skill_{name}.md`
- Use underscores, not hyphens
- Keep names concise but descriptive

**Diagram Nodes**:
- Pattern: `Category --> DXX["skill_name ⭐<br/>Description"]`
- Use sequential numbering (D1, D2, D3...)
- Keep descriptions under 40 characters

**Text List Entries**:
- Pattern: `- **[skill_name](path/skill_name.md)** - Description`
- Description can be longer (60-80 characters)
- Start with verb or noun phrase

### Color Coding (Section 508 Compliant)

**Category Colors** (4.5:1 contrast minimum):
- Tools: `#00695c` (teal)
- Automation: `#e65100` (orange)
- Integrations: `#6a1b9a` (purple)
- Development: `#1b5e20` (dark green) or `#2e7d32` (medium green)
- Documentation: `#880e4f` (dark pink) or `#ad1457` (medium pink)
- System: `#f57f17` (amber) or `#e65100` (orange)

**Featured Skills** (⭐):
- Use `stroke-width:3px` for bold border
- Darker shade of category color

---

## Automation Script

**Complete README Update Script**:

```powershell
# update-readme-skills.ps1
param(
    [string]$SkillName,
    [string]$Category,
    [string]$Description,
    [switch]$Featured
)

$readmePath = "./README.md"
$readme = Get-Content $readmePath -Raw

# 1. Find next node number for category
$categoryPrefix = switch ($Category) {
    'Tools' { 'T' }
    'Automation' { 'A' }
    'Integrations' { 'I' }
    'Development' { 'D' }
    'Documentation' { 'Doc' }
    'System' { 'S' }
}

# Extract existing node numbers
$pattern = "$Category --> $categoryPrefix(\d+)\["
$matches = [regex]::Matches($readme, $pattern)
$maxNum = ($matches | ForEach-Object { [int]$_.Groups[1].Value } | Measure-Object -Maximum).Maximum
$nextNum = $maxNum + 1
$nodeId = "$categoryPrefix$nextNum"

# 2. Build node entry
$star = if ($Featured) { " ⭐" } else { "" }
$nodeEntry = "    $Category --> $nodeId[`"$SkillName$star<br/>$Description`"]"

# 3. Build style entry
$color = switch ($Category) {
    'Development' { '#1b5e20' }
    'Automation' { '#e65100' }
    'System' { '#f57f17' }
    default { '#1b5e20' }
}
$strokeWidth = if ($Featured) { '3px' } else { '2px' }
$styleEntry = "    style $nodeId fill:$color,stroke:#ffffff,stroke-width:$strokeWidth,color:#ffffff"

# 4. Build text list entry
$path = "$($Category.ToLower())/skill_$SkillName.md"
$textEntry = "- **[$SkillName]($path)** - $Description"

Write-Host "Generated entries:" -ForegroundColor Cyan
Write-Host $nodeEntry
Write-Host $styleEntry
Write-Host $textEntry
Write-Host "`nManually add these to README.md" -ForegroundColor Yellow
```

**Usage**:

```powershell
.\update-readme-skills.ps1 -SkillName "copado_deployments" -Category "Development" -Description "Deployment execution" -Featured
```

---

## Related Skills

- `skill_organizing_skills.md` - Guidelines for organizing skills
- `skill_creator.md` - Creating new skills
- `tool_filing.md` - Filing tools correctly

---

## References

- [Mermaid Diagram Syntax](https://mermaid.js.org/intro/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Section 508 Color Palette](documentation/skill_section_508_color_palette.md)

---

## Checklist Template

Use this checklist when adding new skills:

```markdown
## Adding [Skill Name] to README

- [ ] Skill file created: `[category]/skill_[name].md`
- [ ] Added to Mermaid diagram (node)
- [ ] Added to Mermaid diagram (style)
- [ ] Added to text-based list
- [ ] Updated category count in diagram
- [ ] Updated total count in root node
- [ ] Updated total count in tagline
- [ ] Verified all links work
- [ ] Committed changes
- [ ] Pushed to GitHub
- [ ] Verified on GitHub (hard refresh)
```

---

**Skill Owner**: TEG Development Team  
**Last Validated**: March 3, 2026  
**Next Review**: April 1, 2026
