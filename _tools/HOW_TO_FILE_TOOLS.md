# How to File New Tools in Skills Folder

Complete guide for organizing tools in the `G:\My Drive\06_Skills\` folder structure.

---

## Quick Decision Tree

```
New Tool → Ask: What is its PRIMARY purpose?

├─ Daily automation/planning → _tools/
├─ Utility scripts → _scripts/
├─ Workflow automation → automation/
├─ API integration → integrations/
├─ Development setup → development/
├─ Documentation generation → documentation/
└─ System configuration → system/
```

---

## Folder Structure

### **_tools/** - Daily Planning & Automation
**Purpose:** Tools that run regularly for daily operations

**Examples:**
- Email analysis and task generation
- Calendar integration
- Todoist automation
- Amplenote note creation
- Daily planning workflows

**When to use:**
- ✅ Runs on schedule (daily, hourly)
- ✅ Part of daily workflow
- ✅ Integrates multiple services
- ✅ Produces actionable outputs

**Current tools:**
- `run_process_new_v2.py` - Main daily planning workflow
- `scheduler.py` - Automated scheduling
- `auth_manager.py` - Credential management
- `gmail_tools.py`, `todoist_tools.py`, `calendar_tools.py` - API integrations

---

### **_scripts/** - Utility Scripts
**Purpose:** One-off or occasional utility scripts

**Examples:**
- Data cleanup scripts
- Migration tools
- Testing utilities
- Debugging helpers

**When to use:**
- ✅ Run manually when needed
- ✅ Not part of regular workflow
- ✅ Utility/helper function
- ✅ Temporary or experimental

**File naming:** `{action}_{target}.py`
- `cleanup_old_tasks.py`
- `migrate_notes.py`
- `test_api_connection.py`

---

### **automation/** - Workflow Automation
**Purpose:** Automated workflows and process orchestration

**Examples:**
- Multi-step workflows
- Process automation
- Batch operations
- Scheduled tasks

**When to use:**
- ✅ Orchestrates multiple tools
- ✅ Complex workflow with steps
- ✅ Scheduled automation
- ✅ Business process automation

**Structure:**
```
automation/
├── workflow_name/
│   ├── README.md
│   ├── workflow.py
│   └── config.yaml
```

---

### **integrations/** - API Integrations
**Purpose:** Standalone API integration libraries

**Examples:**
- API client libraries
- Service wrappers
- Integration modules
- Data connectors

**When to use:**
- ✅ Reusable API client
- ✅ Service integration
- ✅ Can be used by multiple tools
- ✅ Well-defined interface

**Structure:**
```
integrations/
├── service_name/
│   ├── README.md
│   ├── client.py
│   ├── models.py
│   └── tests/
```

---

### **development/** - Development Tools
**Purpose:** Development setup, configs, and tooling

**Examples:**
- IDE configurations
- Linters and formatters
- Build scripts
- Development utilities

**When to use:**
- ✅ Development environment setup
- ✅ Code quality tools
- ✅ Build/deploy scripts
- ✅ Developer utilities

**Examples:**
- `.vscode/` settings
- `pyproject.toml`
- `setup.py`
- `Makefile`

---

### **documentation/** - Documentation Tools
**Purpose:** Tools for creating and managing documentation

**Examples:**
- Diagram generators
- Documentation converters
- Template generators
- Report builders

**When to use:**
- ✅ Creates documentation
- ✅ Converts formats
- ✅ Generates diagrams
- ✅ Documentation workflow

**Current tools:**
- `diagram-tools/mermaid_to_visio.py` - Convert Mermaid to Visio

**Structure:**
```
documentation/
├── diagram-tools/
├── report-generators/
└── template-tools/
```

---

### **system/** - System Configuration
**Purpose:** System setup, configuration, and maintenance

**Examples:**
- System setup scripts
- Configuration management
- Environment setup
- System utilities

**When to use:**
- ✅ System configuration
- ✅ Environment setup
- ✅ System maintenance
- ✅ Infrastructure setup

---

## Filing Process

### Step 1: Identify Purpose

Ask yourself:
1. **What does this tool do?** (primary function)
2. **When do I use it?** (frequency, context)
3. **Who uses it?** (me, team, automated)
4. **What does it integrate with?** (services, APIs)

### Step 2: Choose Folder

Use the decision tree above to select the appropriate folder.

**If unsure between two folders:**
- Choose based on **primary purpose**
- Consider **who/what triggers it**
- Think about **maintenance** (where would you look for it?)

### Step 3: Organize Files

**Single file tool:**
```
folder/
└── tool_name.py
```

**Multi-file tool:**
```
folder/
└── tool_name/
    ├── README.md
    ├── main.py
    ├── config.yaml
    └── tests/
```

**Complex tool:**
```
folder/
└── tool_name/
    ├── README.md
    ├── src/
    │   ├── __init__.py
    │   ├── main.py
    │   └── utils.py
    ├── tests/
    ├── docs/
    └── config/
```

### Step 4: Document

**Minimum documentation:**
- Purpose (one sentence)
- Usage (command to run)
- Prerequisites (dependencies)

**Create README.md:**
```markdown
# Tool Name

Brief description of what it does.

## Usage

\`\`\`bash
python tool_name.py [options]
\`\`\`

## Prerequisites

- Python 3.8+
- Dependencies: `pip install -r requirements.txt`

## Configuration

Environment variables or config files needed.
```

---

## Examples

### Example 1: Email Analysis Tool

**Question:** Where does `analyze_emails.py` go?

**Analysis:**
- **Purpose:** Analyzes emails for daily planning
- **Frequency:** Daily, automated
- **Integration:** Gmail API, OpenRouter
- **Output:** Todoist tasks

**Answer:** `_tools/analyze_emails.py`
- Part of daily workflow
- Runs automatically
- Integrates multiple services

---

### Example 2: Mermaid to Visio Converter

**Question:** Where does `mermaid_to_visio.py` go?

**Analysis:**
- **Purpose:** Converts diagram formats
- **Frequency:** As needed
- **Integration:** None (standalone)
- **Output:** Documentation files

**Answer:** `documentation/diagram-tools/mermaid_to_visio.py`
- Creates documentation
- Not part of daily workflow
- Documentation-focused

---

### Example 3: API Client Library

**Question:** Where does `notion_client.py` go?

**Analysis:**
- **Purpose:** Notion API wrapper
- **Frequency:** Used by other tools
- **Integration:** Notion API
- **Output:** Reusable library

**Answer:** `integrations/notion/client.py`
- Reusable API client
- Can be imported by multiple tools
- Well-defined interface

---

### Example 4: One-time Migration Script

**Question:** Where does `migrate_old_notes.py` go?

**Analysis:**
- **Purpose:** Migrate data once
- **Frequency:** One-time use
- **Integration:** Amplenote
- **Output:** Migrated data

**Answer:** `_scripts/migrate_old_notes.py`
- One-time utility
- Not part of regular workflow
- Temporary/maintenance script

---

## Best Practices

### 1. **One Tool, One Purpose**
Each tool should have a clear, single purpose. If a tool does multiple things, consider splitting it.

### 2. **Reusable Components**
If code is used by multiple tools, extract it to `integrations/` or create a shared library.

### 3. **Configuration Separate from Code**
Use config files (`config.yaml`, `.env`) instead of hardcoding values.

### 4. **Document Dependencies**
Always include `requirements.txt` or document dependencies in README.

### 5. **Version Control**
Keep development in Git repos (like CascadeProjects), copy stable versions to Skills folder.

### 6. **Naming Conventions**

**Files:**
- Use snake_case: `analyze_emails.py`
- Be descriptive: `convert_mermaid_to_visio.py` not `convert.py`
- Include action: `create_`, `update_`, `delete_`, `analyze_`

**Folders:**
- Use kebab-case: `diagram-tools/`
- Be specific: `email-analysis/` not `tools/`

### 7. **README Template**

```markdown
# Tool Name

One-line description.

## Purpose

Why this tool exists and what problem it solves.

## Usage

\`\`\`bash
python tool_name.py --option value
\`\`\`

## Prerequisites

- Python 3.8+
- Node.js (if needed)
- API keys: List what's needed

## Configuration

How to configure (environment variables, config files).

## Examples

Common use cases with examples.

## Troubleshooting

Common issues and solutions.
```

---

## Maintenance

### Moving Tools

If you realize a tool is in the wrong place:

1. **Create new location**
2. **Copy files** (don't move yet)
3. **Update references** in other tools
4. **Test** that everything works
5. **Delete old location**
6. **Update documentation**

### Deprecating Tools

When a tool is no longer needed:

1. **Move to** `05_Archive/tools/`
2. **Document why** it was deprecated
3. **Note replacement** if applicable
4. **Keep for reference** (don't delete immediately)

---

## Quick Reference

| Tool Type | Folder | Example |
|-----------|--------|---------|
| Daily automation | `_tools/` | Email analysis |
| Utility script | `_scripts/` | Data cleanup |
| Workflow | `automation/` | Multi-step process |
| API client | `integrations/` | Service wrapper |
| Dev tool | `development/` | Linter config |
| Doc tool | `documentation/` | Diagram converter |
| System setup | `system/` | Environment setup |

---

## Getting Help

**Still not sure where to file a tool?**

Ask these questions:
1. Is it part of my daily workflow? → `_tools/`
2. Is it a one-time utility? → `_scripts/`
3. Is it reusable by other tools? → `integrations/`
4. Does it create documentation? → `documentation/`
5. Is it for development? → `development/`

**When in doubt:** Start in `_scripts/`, move later if it becomes part of regular workflow.

---

---

## Private/Sensitive Content

Some content should not be documented in public-facing skills:

### Media Files
For organizing media (videos, pictures, audio, magazines), see:
**`G:\My Drive\04_Resources\Media\HOW_TO_FILE_MEDIA.md`**

This guide covers:
- Video organization (movies, TV shows, documentaries, tutorials)
- Picture management (photos, screenshots, wallpapers)
- Audio filing (music, podcasts, audiobooks)
- Magazine and document organization
- Privacy considerations for sensitive media

**Privacy Rule:** When creating skills or documentation that might be shared, reference the media filing guide generically without listing specific folder names.

---

## Changelog

- **2026-03-01:** Created initial guide
- **2026-03-01:** Moved Mermaid converter to `documentation/diagram-tools/`
- **2026-03-01:** Added reference to media filing guide for private content
