# Skills Repository Quick Start Guide

Complete guide for using the Skills repository in Windsurf Cascade and Claude Code.

---

## Overview

This repository contains 50+ AI agent skills for automation, development, documentation, and system configuration. This guide shows you how to effectively use these skills in Windsurf Cascade and Claude Code.

**Repository:** https://github.com/adourish/skills

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [For Windsurf Cascade Users](#for-windsurf-cascade-users)
3. [For Claude Code Users](#for-claude-code-users)
4. [Common Workflows](#common-workflows)
5. [Skill Categories](#skill-categories)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Prerequisites

- **Local Access:** Clone or download the repository to your machine
- **GitHub Access:** https://github.com/adourish/skills
- **Location:** Recommended path: `G:\My Drive\06_Skills\` (or your preferred location)

### Repository Structure

```
06_Skills/
├── _tools/              # Skill development tools
├── automation/          # Daily workflows (7 skills)
├── integrations/        # API integrations (5 skills)
├── development/         # Dev tools (8 skills)
├── documentation/       # Templates & diagrams (19 skills)
├── system/              # Core configuration (9 skills)
├── README.md            # Main documentation
├── SKILLS_CONTEXT.md    # AI-optimized reference
└── skills_manifest.json # Machine-readable index
```

### Key Files to Know

1. **README.md** - Complete skill catalog with diagrams
2. **SKILLS_CONTEXT.md** - Single source of truth for AI agents
3. **skills_manifest.json** - Programmatic skill access
4. **user_commands** - Quick command reference

---

## For Windsurf Cascade Users

### Method 1: Reference Specific Skills

**Natural Language Approach:**

```
"Check the daily_planning skill at G:\My Drive\06_Skills\automation\skill_daily_planning.md"

"Load the GitHub pull requests skill from the development folder"

"Show me the GitFlow workflow skill"
```

**What Cascade Does:**
1. Reads the skill markdown file
2. Understands the workflow
3. Provides step-by-step guidance
4. Executes commands with your approval

---

### Method 2: Load Multiple Skills

**Batch Loading:**

```
"Load the following skills:
- file_organization
- routing_rules
- skill_creator"
```

**Use Case:** When you need multiple related skills for a complex task

---

### Method 3: Load by Category

**Category-Based Loading:**

```
"Load all documentation skills from G:\My Drive\06_Skills\documentation\"

"Show me all development skills"

"What automation skills are available?"
```

**Categories:**
- Tools (2 skills)
- Automation (7 skills)
- Integrations (5 skills)
- Development (8 skills)
- Documentation (19 skills)
- System (9 skills)

---

### Method 4: Use Skills Context

**For Overview:**

```
"Reference SKILLS_CONTEXT.md for complete skill overview"

"What skills are available in this repository?"

"Show me the skill dependency chains"
```

---

### Windsurf Workflow Examples

#### Example 1: Daily Planning

```
You: "Plan my day"

Cascade:
1. Reads: automation/skill_daily_planning.md
2. Checks: environments.json configured?
3. Navigates: cd "C:\Users\sol90\CascadeProjects\mcptools"
4. Executes: python run_process_new_v2.py
5. Monitors: Completion (~30 seconds)
6. Verifies: Todoist tasks created
7. Reports: "Created 5 tasks from 12 emails and 3 calendar events"
```

#### Example 2: Create New Skill

```
You: "Create a skill for API rate limiting"

Cascade:
1. Loads: _tools/skill-creator/README.md
2. Loads: _tools/HOW_TO_FILE_TOOLS.md
3. Asks: Purpose, category, prerequisites
4. Creates: Skill markdown with proper structure
5. Determines: development/ folder (API-related)
6. Updates: README.md with new skill
7. Commits: Changes to git (if requested)
```

#### Example 3: Document Processing

```
You: "Create a Word document with a table of my tasks"

Cascade:
1. Loads: documentation/document-processing/skill_docx.md
2. Checks: Dependencies (docx-js installed?)
3. Fetches: Tasks from Todoist
4. Generates: Code using docx-js
5. Creates: Document with formatted table
6. Saves: tasks_summary.docx
```

---

## For Claude Code Users

### Method 1: Direct File Reference

**Using @ Mentions:**

```
@G:\My Drive\06_Skills\automation\skill_daily_planning.md

@skill_github_pull_requests.md

@README.md
```

**What Claude Does:**
- Loads file content into context
- Understands skill structure
- Provides guidance based on skill
- Suggests commands and workflows

---

### Method 2: Folder Reference

**Load Entire Categories:**

```
@G:\My Drive\06_Skills\documentation\

@development/

@automation/
```

**Use Case:** When exploring a category or need multiple related skills

---

### Method 3: Multiple Skills

**Batch @ References:**

```
@skill_file_organization.md
@skill_routing_rules.md
@HOW_TO_FILE_TOOLS.md
```

**Use Case:** Complex tasks requiring multiple skill sets

---

### Method 4: Context File

**For Overview:**

```
@SKILLS_CONTEXT.md

@skills_manifest.json
```

---

### Claude Workflow Examples

#### Example 1: Quick Command Lookup

```
You: "What's the command to plan my day?"

Claude:
1. Loads: @user_commands
2. Finds: daily_planning section
3. Provides: python run_process_new_v2.py
4. Explains: Scans Gmail, Calendar, Todoist
5. Shows: Expected output (tasks, notes, JSON)
```

#### Example 2: Build MCP Server

```
You: "Build an MCP server for Notion integration"

Claude:
1. Loads: @mcp-builder/README.md
2. Loads: @mcp-builder/SKILL.md
3. Phase 1: Research Notion API
4. Phase 2: Implement server code
5. Phase 3: Review and test
6. Phase 4: Create evaluations
7. Provides: Complete working MCP server
```

#### Example 3: Create Accessible Diagram

```
You: "Create a Section 508 compliant flowchart"

Claude:
1. Loads: @mermaid_section_508.md
2. Uses: Approved color palette
3. Ensures: 4.5:1 contrast ratio
4. Adds: Icons + text labels
5. Generates: Mermaid diagram code
6. Validates: Accessibility compliance
```

---

## Common Workflows

### Workflow 1: Setup New Project

**Skills Needed:**
1. `environments_credentials` - Configure API keys
2. `git_version_control` - Initialize repository
3. `routing_rules` - Set up PARA structure
4. `mcp_server_setup` - Configure Windsurf integration

**Steps:**
```
1. Load @environments_credentials.md
2. Create environments.json with API keys
3. Load @git_version_control.md
4. Initialize git repository
5. Load @routing_rules.md
6. Create PARA folder structure
7. Load @mcp_server_setup.md
8. Configure MCP for Windsurf
```

---

### Workflow 2: Daily Planning Routine

**Skills Needed:**
1. `daily_planning` - Main workflow
2. `email_processing` - Email analysis
3. `todoist_api` - Task management
4. `amplenote_api` - Note creation

**Steps:**
```
1. Run: python run_process_new_v2.py
2. Review: Todoist tasks created
3. Check: Amplenote daily note
4. Verify: Calendar events processed
5. Adjust: Priorities as needed
```

---

### Workflow 3: Contributing to Skills Repo

**Skills Needed:**
1. `skill_creator` - Create new skill
2. `github_pull_requests` - Submit changes
3. `gitflow_workflow` - Branching strategy

**Steps:**
```
1. Load @skill-creator/README.md
2. Create new skill markdown
3. Load @skill_github_pull_requests.md
4. Fork repository
5. Create feature branch
6. Commit changes
7. Create pull request
8. Respond to code review
```

---

### Workflow 4: Document Creation

**Skills Needed:**
1. `doc_coauthoring` - Collaborative writing
2. `document_processing` - DOCX/PPTX/PDF/XLSX
3. `internal_comms` - Announcements/changelogs

**Steps:**
```
1. Load @doc-coauthoring/README.md
2. Stage 1: Context Gathering
3. Stage 2: Refinement & Structure
4. Stage 3: Reader Testing
5. Load @document-processing/skill_docx.md
6. Generate Word document
7. Load @internal-comms/README.md
8. Create changelog entry
```

---

## Skill Categories

### 🛠️ Tools (2 skills)
- **skill_creator** - Create new skills
- **HOW_TO_FILE_TOOLS** - Organize tools

### 🤖 Automation (7 skills)
- **daily_planning** ⭐ - Kanban board generation
- **email_processing** - Email automation
- **file_organization** - PARA method
- browser_automation, powershell_automation, torrent_downloads, archive_parts_recovery

### 🔌 Integrations (5 skills)
- amplenote_api, todoist_api, gmail_automation
- amplenote_relay_systems, keepass_integration

### 💻 Development (8 skills)
- **mcp_builder** ⭐ - Build MCP servers
- **github_pull_requests** ⭐ - PR workflow
- **gitflow_workflow** ⭐ - GitFlow branching
- git_version_control, salesforce_development, salesforce_fls_automation, salesforce_developer_activity_report, azure_devops_automation

### 📝 Documentation (19 skills)
- **doc_coauthoring** ⭐ - Collaborative writing
- **document_processing** ⭐ - DOCX/PPTX/PDF/XLSX
- **internal_comms** - Announcements
- mermaid_diagrams, visio_via_mermaid, diagram_tools, and more

### ⚙️ System (9 skills)
- **user_commands** ⭐ - Quick reference
- environments_credentials, routing_rules, section_508_compliance, cascade_workflow, process_new, agent_handoff, mcp_server_setup, organizing_skills

---

## Best Practices

### 1. Start with README.md

```
@README.md
```

- Get overview of all skills
- Understand categories
- See skill relationships
- Find what you need

### 2. Use SKILLS_CONTEXT.md for AI

```
@SKILLS_CONTEXT.md
```

- AI-optimized format
- Complete metadata
- Dependency chains
- Quick lookup

### 3. Load Related Skills Together

```
@skill_daily_planning.md
@skill_email_processing.md
@skill_todoist_api.md
```

- Better context
- Understand dependencies
- Complete workflows

### 4. Check Prerequisites First

Before using a skill:
1. Check "Prerequisites" section
2. Verify dependencies installed
3. Configure required credentials
4. Test with simple example

### 5. Follow Skill Structure

All skills have:
- **Overview** - What it does
- **When to Use** - Use cases
- **Prerequisites** - Requirements
- **Step-by-Step Guide** - Instructions
- **Examples** - Real scenarios
- **Best Practices** - Tips
- **Troubleshooting** - Common issues
- **Related Skills** - Connections

---

## Troubleshooting

### Issue: "Skill not found"

**Solution:**
```
# Verify path
ls "G:\My Drive\06_Skills\automation\skill_daily_planning.md"

# Use full path
@G:\My Drive\06_Skills\automation\skill_daily_planning.md

# Or navigate to folder first
cd "G:\My Drive\06_Skills"
@automation/skill_daily_planning.md
```

### Issue: "Command doesn't work"

**Solution:**
1. Check prerequisites in skill
2. Verify environment configured
3. Test with simple example
4. Check error messages
5. Review troubleshooting section in skill

### Issue: "Too many skills loaded"

**Solution:**
- Start new conversation
- Load only essential skills
- Use SKILLS_CONTEXT.md for overview
- Reference specific skills as needed

### Issue: "Skill outdated"

**Solution:**
```
# Pull latest from GitHub
cd "G:\My Drive\06_Skills"
git pull origin main

# Or download latest release
# https://github.com/adourish/skills/releases
```

---

## Quick Reference

### Most Used Skills

**Daily:**
- daily_planning - `python run_process_new_v2.py`
- file_organization - PARA method
- user_commands - Command reference

**Weekly:**
- email_processing - Email automation

**As Needed:**
- skill_creator - Create new skills
- github_pull_requests - Contribute changes
- document_processing - Create docs

### Common Commands

```bash
# Daily planning
python run_process_new_v2.py

# File organization
# Ask AI to help with PARA method

# Git workflow
git checkout -b feature/my-feature
git commit -m "Add feature"
git push origin feature/my-feature

# Create pull request
gh pr create --title "Add feature"
```

### Skill Loading Shortcuts

**Windsurf:**
```
"Load daily planning skill"
"Show me all automation skills"
"Reference SKILLS_CONTEXT.md"
```

**Claude:**
```
@skill_daily_planning.md
@automation/
@SKILLS_CONTEXT.md
```

---

## Additional Resources

### Documentation
- **README.md** - Complete skill catalog
- **SKILLS_CONTEXT.md** - AI-optimized reference
- **SKILLS_DIAGRAM.md** - Visual relationships
- **skills_manifest.json** - Programmatic access

### External Links
- **GitHub Repository:** https://github.com/adourish/skills
- **Anthropic Skills:** https://github.com/anthropics/skills (source for some skills)
- **MCP Documentation:** https://modelcontextprotocol.io/

### Support
- Check skill's "Troubleshooting" section
- Review "Related Skills" for alternatives
- Search skills_manifest.json for keywords
- Create issue on GitHub for bugs

---

## Changelog

- **2026-03-01:** Created Quick Start Guide
- **2026-03-01:** Added Windsurf and Claude Code examples
- **2026-03-01:** Included common workflows and troubleshooting

---

**Location:** `G:\My Drive\06_Skills\QUICKSTART.md`  
**Repository:** https://github.com/adourish/skills  
**Total Skills:** 50 across 6 categories
