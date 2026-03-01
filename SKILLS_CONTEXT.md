# Skills Context for AI (Windsurf/Cascade)

**Version:** 1.0.0  
**Last Updated:** March 1, 2026  
**Total Skills:** 36  
**Purpose:** Single source of truth for AI agents to quickly understand and use available skills

---

## Quick Start for AI

**Most Important Skills:**
1. **[user_commands](system/skill_user_commands.md)** - START HERE for all commands
2. **[daily_planning](automation/skill_daily_planning.md)** - Daily workflow automation
3. **[routing_rules](system/skill_routing_rules.md)** - Where things go
4. **[section_508_compliance](system/skill_section_508_compliance.md)** - Accessibility standards

**Most Common User Requests:**
- "Help me plan my day" → Use `daily_planning` skill
- "File my downloads" → Use `file_organization` skill  
- "Process my emails" → Use `email_processing` skill
- "Create a diagram" → Use `mermaid_diagrams` or `visio_via_mermaid` skills
- "Show me all commands" → Use `user_commands` skill

---

## Skills by Frequency

### Daily Use (5 skills)
- **daily_planning** - `python run_process_new.py` (30 seconds)
- **file_organization** - Ask AI to help file downloads (10-30 min)
- **user_commands** - Quick command reference (instant)
- **routing_rules** - Where things go (instant)
- **git_version_control** - Version control (ongoing)

### Weekly Use (1 skill)
- **email_processing** - Process emails manually (5-10 min)

### Setup Required First (3 skills)
- **environments_credentials** - Configure API keys (5-10 min)
- **routing_rules** - Understand system organization (5 min)
- **mcp_server_setup** - Set up Windsurf integration (15 min)

### As-Needed (27 skills)
All other skills - reference when specific functionality needed

---

## Skills by Category

### 🤖 Automation (7 skills)
**Purpose:** Automate daily workflows and processes

| Skill | Command | Use When |
|-------|---------|----------|
| daily_planning | `python run_process_new.py` | Every morning |
| email_processing | `python email_processor.py` | Weekly email cleanup |
| file_organization | Ask AI | Downloads need filing |
| browser_automation | Use Playwright MCP | Web scraping needed |
| powershell_automation | See skill | Windows automation |
| torrent_downloads | See skill | Torrent management |
| archive_parts_recovery | See skill | File recovery |

### 🔌 Integrations (5 skills)
**Purpose:** Connect to external APIs and services

| Skill | Command | Use When |
|-------|---------|----------|
| amplenote_api | `node refresh_amplenote_token.js` | Token expired |
| amplenote_relay_systems | See skill | Advanced automation |
| gmail_automation | `python setup_gmail_oauth.py` | Gmail setup |
| todoist_api | `python query_todoist.py` | Task management |
| keepass_integration | See skill | Password access |

### 💻 Development (5 skills)
**Purpose:** Software development tools and workflows

| Skill | Command | Use When |
|-------|---------|----------|
| salesforce_development | `sfdx force:org:open -u dmedev5` | Salesforce work |
| salesforce_fls_automation | See skill | FLS configuration |
| salesforce_developer_activity_report | See skill | Activity tracking |
| git_version_control | `git status` | Version control |
| azure_devops_automation | See skill | ADO work items |

### 📝 Documentation (10 skills)
**Purpose:** Create and manage documentation and diagrams

| Skill | Command | Use When |
|-------|---------|----------|
| mermaid_diagrams | Create .mmd file | Diagram creation |
| visio_via_mermaid | `python mermaid-to-visio.py` | Mermaid → Visio |
| mermaid_from_visio | Manual or script | Visio → Mermaid |
| mermaid_section_508 | Use approved colors | Accessible Mermaid |
| visio_section_508 | Follow guidelines | Accessible Visio |
| visio_grant_lifecycle_diagram | Use template | Grant diagrams |
| teg_discussion_templates | Use template | TEG documents |
| feature_documentation | Follow standards | Feature docs |
| qif_dndd_fillable_forms_visio_spec | See spec | QIF forms |
| teg_discussion_template_alt | Use alt template | Alt TEG docs |

### ⚙️ System (9 skills)
**Purpose:** Core system configuration and workflows

| Skill | Command | Use When |
|-------|---------|----------|
| user_commands | Reference skill | Need any command |
| section_508_compliance | Follow guidelines | Accessibility |
| routing_rules | Reference skill | Where things go |
| environments_credentials | Check environments.json | API setup |
| cascade_workflow | Follow patterns | AI collaboration |
| agent_handoff | Follow protocols | Agent transitions |
| mcp_server_setup | `python server.py` | MCP integration |
| process_new | `python run_process_new.py` | Complete workflow |
| organizing_skills | Follow guidelines | Skill creation |

---

## Common Workflows

### Morning Routine
1. Run `daily_planning` → Generates Kanban board
2. Check Todoist tasks on DakBoard
3. File any downloads using `file_organization`
4. Reference `routing_rules` for where things go

### Weekly Email Processing
1. Run `email_processing` → Extracts tasks from emails
2. Tasks auto-created in Todoist
3. Notes auto-created in Amplenote
4. Review and organize

### Creating Accessible Diagrams
1. Use `mermaid_diagrams` → Create diagram
2. Apply `mermaid_section_508` → Use compliant colors
3. Convert with `visio_via_mermaid` → Generate Visio
4. Validate with `section_508_compliance` → Check accessibility

### Development Workflow
1. Use `git_version_control` → Branch and commit
2. Use `salesforce_development` → Code changes
3. Use `azure_devops_automation` → Track work items
4. Reference `environments_credentials` → API access

---

## Key Commands Reference

**Daily Planning:**
```powershell
cd "${SKILLS_ROOT}/_tools"
python run_process_new.py
```

**Refresh Amplenote Token:**
```powershell
cd "${SKILLS_ROOT}/_scripts"
node refresh_amplenote_token.js
```

**Query Todoist:**
```powershell
cd "${SKILLS_ROOT}/_tools"
python query_todoist.py
```

**Git Operations:**
```powershell
git status
git add .
git commit -m "message"
git push
```

**Salesforce:**
```powershell
sfdx force:org:open -u dmedev5
sfdx force:source:pull
sfdx force:source:push
```

---

## Dependencies Map

**Setup First:**
- environments_credentials → Required by most API integrations
- routing_rules → Required for file organization
- mcp_server_setup → Required for Windsurf integration

**Common Dependency Chains:**
1. environments_credentials → gmail_automation → email_processing → daily_planning
2. environments_credentials → todoist_api → daily_planning
3. environments_credentials → amplenote_api → daily_planning
4. mermaid_diagrams → visio_via_mermaid → visio_section_508
5. section_508_compliance → mermaid_section_508 + visio_section_508

---

## Skill Selection Guide

**User says:** "Help me plan my day"  
**Use:** daily_planning  
**Command:** `python run_process_new.py`

**User says:** "File my downloads"  
**Use:** file_organization  
**Action:** Check Downloads, suggest PARA locations

**User says:** "Process my emails"  
**Use:** email_processing  
**Command:** `python email_processor.py`

**User says:** "Create a diagram"  
**Use:** mermaid_diagrams or visio_via_mermaid  
**Action:** Ask for diagram type, create Mermaid syntax

**User says:** "Make it accessible" or "Section 508"  
**Use:** section_508_compliance, mermaid_section_508, or visio_section_508  
**Action:** Apply accessible colors and guidelines

**User says:** "Show me commands"  
**Use:** user_commands  
**Action:** Display command reference

**User says:** "Where does this go?"  
**Use:** routing_rules  
**Action:** Explain PARA method and routing

**User says:** "Set up API" or "Configure credentials"  
**Use:** environments_credentials  
**Action:** Guide through API setup

**User says:** "Salesforce" or "SFDC"  
**Use:** salesforce_development  
**Command:** `sfdx force:org:open -u dmedev5`

**User says:** "Git" or "commit" or "push"  
**Use:** git_version_control  
**Command:** `git status` (then guide through workflow)

---

## Section 508 Compliance

**All diagrams must:**
- Use approved color palette (see mermaid_section_508 or visio_section_508)
- Have 4.5:1 contrast minimum
- Include text labels (no color-only meaning)
- Use icons to supplement colors

**Approved Colors:**
- Dark: Navy Blue (#0d47a1), Forest Green (#1b5e20), Burgundy (#880e4f)
- Light: Light Blue (#e1f5fe), Light Green (#e8f5e9), Light Pink (#fce4ec)

---

## File Locations

**Skills:** `${SKILLS_ROOT}/`  
**Tools:** `${SKILLS_ROOT}/_tools/`  
**Scripts:** `${SKILLS_ROOT}/_scripts/`  
**Credentials:** `${PARA_ROOT}/03_Areas/Keys/Environments/environments.json`  
**KeePass:** `${PARA_ROOT}/03_Areas/Keys/keys pass.kdbx`

---

## PARA Method (Routing Rules)

**Projects:** `${PARA_ROOT}/01_Operate/Projects/` - Active work with deadlines  
**Areas:** `${PARA_ROOT}/03_Areas/` - Ongoing responsibilities  
**Resources:** `${PARA_ROOT}/04_Resources/` - Reference material  
**Archive:** `${PARA_ROOT}/05_Archive/` - Completed/inactive items

**Tasks:** Todoist (permanent storage)  
**Notes:** Amplenote (reference + daily view)  
**Events:** Google Calendar  
**Files:** PARA method

---

## AI Integration Notes

**For Windsurf/Cascade:**
- Always check `user_commands` first for quick command reference
- Use `skills_manifest.json` for programmatic skill lookup
- Reference this file (`SKILLS_CONTEXT.md`) for comprehensive overview
- Follow `cascade_workflow` for best AI collaboration patterns
- Use `agent_handoff` protocols when transitioning between AI agents

**Skill Discovery:**
1. Check user_commands for command reference
2. Check skills_manifest.json for structured data
3. Check SKILLS_CONTEXT.md for comprehensive guide
4. Check individual skill files for detailed documentation

**Best Practices:**
- Always provide copy-paste commands
- Reference skill files by name
- Explain what command does before running
- Ask for confirmation on destructive operations
- Use Section 508 compliant colors for all diagrams

---

**Quick Links:**
- [Skills Manifest JSON](skills_manifest.json) - Machine-readable skill index
- [Skills README](README.md) - Human-readable overview with diagrams
- [User Commands](system/skill_user_commands.md) - Command quick reference
- [Routing Rules](system/skill_routing_rules.md) - Where things go

---

**Last Updated:** March 1, 2026  
**Location:** `${SKILLS_ROOT}/SKILLS_CONTEXT.md`  
**For:** Windsurf, Cascade, and other AI agents
