# MCP Server Setup Guide for AI Agents

**For AI agents helping with "process new" workflow**

## Quick Reference
**Use when:** Setting up the MCP server for the first time, MCP connection lost, adding new MCP tools, AI agent needs direct tool access to Gmail/Todoist/Amplenote
**Don't use when:** MCP is already running — just use it
**Trigger phrases:** "set up MCP", "MCP server", "connect MCP", "MCP not working", "start the server"
**Time:** Initial setup ~15 minutes; restart ~30 seconds
**Command:** `python server.py` (in `_tools/`)

## Quick Start

The user has a fully functional MCP server that handles all daily planning workflows. You have two options:

### Option 1: Use MCP Server Directly (Recommended)

```powershell
cd "G:\My Drive\06_Master_Guides\MCP_Server"
python run_process_new.py
```

### Option 2: Use Wrapper Script (Backward Compatible)

```powershell
cd "G:\My Drive\06_Master_Guides\Scripts"
python daily_planner.py
```

Both methods call the same underlying implementation.

---

## What It Does

**Scans:**
- 📧 Gmail (last 30 days) - Filters out promotional/marketing emails
- 📋 Todoist (all active tasks)
- 📅 Google Calendar (next 7 days)
- 📄 Google Drive (recent documents, last 7 days)
- 📂 File system (Inbox folder, Downloads folder)

**Detects:**
- Reference emails (account numbers, confirmations, credentials)
- Urgent vs. promotional emails
- Files needing organization

**Creates:**
1. **JSON output** - Complete plan data
2. **Todoist tasks** - 5 individual DO NOW tasks + 1 DO SOON summary (DakBoard compatible)
3. **Amplenote note** - Comprehensive daily plan with:
   - 🎯 DO NOW (checkboxes)
   - ⏰ DO SOON (checkboxes)
   - 📋 MONITOR (checkboxes)
   - 📌 REFERENCE EMAILS
   - 📄 RECENT DOCUMENTS
   - 📊 STATISTICS

---

## MCP Server Architecture

**Location:** `G:\My Drive\06_Master_Guides\MCP_Server\`

**Modules:**
- `auth_manager.py` - Handles authentication for all services
- `gmail_tools.py` - Gmail scanning with smart filtering
- `todoist_tools.py` - Task management and DakBoard integration
- `calendar_tools.py` - Google Calendar integration
- `amplenote_tools.py` - Amplenote note creation using INSERT_NODES API
- `drive_tools.py` - Google Drive document scanning
- `filesystem_tools.py` - Local file system scanning
- `run_process_new.py` - Main orchestration script

**Server:** `server.py` - MCP server for Windsurf integration

---

## For Other AI Agents

When a user asks you to "run process new" or "daily planner":

1. **Navigate to MCP Server:**
   ```powershell
   cd "G:\My Drive\06_Master_Guides\MCP_Server"
   ```

2. **Run the script:**
   ```powershell
   python run_process_new.py
   ```

3. **Wait for completion** (30-60 seconds)

4. **Output locations:**
   - JSON: `process_new_output_YYYYMMDD_HHMMSS.json`
   - Todoist: Check user's Todoist app (tasks auto-created)
   - Amplenote: URL printed in output

---

## Key Features

### Smart Email Filtering

**Automatically skips:**
- Promotional emails (Audible, Best Buy, etc.)
- Marketing newsletters
- Shipping notifications
- Political emails
- Automated system emails

**Includes:**
- Real deadlines and action items
- Important communications from real people
- Reference information (account numbers, confirmations)

### DakBoard Integration

**Kill and Fill approach:**
- Deletes ALL old daily plan tasks
- Creates 5 individual DO NOW tasks (high priority, red)
- Creates 1 DO SOON summary task (medium priority, yellow)
- All details in task title (visible on DakBoard)

### Amplenote Integration

Uses INSERT_NODES actions API to create rich notes with:
- Checkboxes for all tasks
- Email previews with sender and body snippet
- Document tracking
- Comprehensive statistics

---

## Troubleshooting

### "Gmail token expired"
- Just run again - OAuth flow will trigger automatically
- User signs in once, token saved for future use

### "Todoist API error"
- Check token in `G:\My Drive\03_Areas\Keys\Environments\environments.json`
- Token path: `environments.todoist.credentials.apiToken`

### "Amplenote note empty"
- This has been fixed - uses INSERT_NODES API now
- If issue persists, check token in environments.json

### "Too many promotional emails"
- Filtering has been enhanced
- Should only show actionable items
- If promo emails appear, add sender to skip_senders in gmail_tools.py

---

## Important Notes

1. **Single Source of Truth:** MCP Server is the authoritative implementation
2. **Old Script Deprecated:** `Scripts/daily_planner.py.deprecated` is outdated
3. **No Confusion:** Both paths (Scripts and MCP_Server) use same code
4. **Always Updated:** Latest filtering and features in MCP Server

---

## Configuration

**Credentials:** `G:\My Drive\03_Areas\Keys\Environments\environments.json`

**Services configured:**
- Gmail (OAuth)
- Google Calendar (OAuth)
- Google Drive (OAuth)
- Todoist (API token)
- Amplenote (OAuth access token)

**All authentication is automatic** - tokens refresh as needed.

---

## Summary for AI Agents

**When user says "process new":**
1. Run: `python "G:\My Drive\06_Master_Guides\MCP_Server\run_process_new.py"`
2. Wait for completion
3. Report results from terminal output
4. Share Amplenote URL if provided

**No prompts, no questions, fully autonomous.**
