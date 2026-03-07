# Agent Handoff Guide - Process New Workflow

**Last Updated:** February 22, 2026  
**Status:** ✅ Fully Functional - MCP Server Unified

## Quick Reference
**Use when:** Switching AI agents mid-session, resuming a "process new" workflow in a new session, agent needs handoff context
**Don't use when:** Staying within the same AI session — just continue the conversation
**Trigger phrases:** "hand off", "continue in new session", "agent handoff", "resume process new", "switching to Claude"
**Time:** Instant — follow the Quick Start below
**Command:** Check MCP server is running, then follow handoff protocol

---

## Quick Start for Any Agent

When user says **"process new"** or **"daily planner"**:

```powershell
cd "G:\My Drive\06_Master_Guides\MCP_Server"
python run_process_new.py
```

**That's it.** Everything is automatic. No prompts, no configuration needed.

---

## What Was Completed in This Session

### ✅ Full Feature Migration
Migrated all functionality from standalone `daily_planner.py` to modular MCP server:
- Gmail scanning with smart filtering (promotional emails removed)
- Todoist task management with DakBoard integration
- Google Calendar events (Alex Hartnett auto-filtered)
- Google Drive document tracking (last 7 days)
- File system scanning (Inbox, Downloads folders)
- Reference email detection (account numbers, confirmations)
- Amplenote note creation using INSERT_NODES API
- Comprehensive statistics tracking

### ✅ Scripts Unified
- **Old script:** `Scripts/daily_planner.py.deprecated` (archived)
- **New wrapper:** `Scripts/daily_planner.py` (calls MCP server)
- **MCP server:** `MCP_Server/run_process_new.py` (single source of truth)
- Both paths execute same code - no duplication

### ✅ Email Filtering Enhanced
Automatically filters out:
- Promotional emails (Audible, Best Buy, Salesforce)
- Marketing newsletters
- Shipping notifications
- Political emails
- Automated system emails

Only shows actionable items from real people with real deadlines.

### ✅ Test Files Cleaned
Removed all test scripts from MCP_Server:
- `test_*.py` files (6 files removed)
- `verify_amplenote_content.py` removed
- Old output files cleaned (kept most recent only)

### ✅ Documentation Created
- `MCP_SERVER_SETUP.md` - Comprehensive setup guide for agents
- `AGENT_HANDOFF.md` - This file (quick reference)

---

## Architecture Overview

### MCP Server Structure
```
MCP_Server/
├── run_process_new.py          # Main orchestration script
├── auth_manager.py              # Authentication for all services
├── gmail_tools.py               # Gmail with smart filtering
├── todoist_tools.py             # Task management + DakBoard
├── calendar_tools.py            # Google Calendar integration
├── amplenote_tools.py           # Amplenote INSERT_NODES API
├── drive_tools.py               # Google Drive document scanning
├── filesystem_tools.py          # Local file system scanning
├── server.py                    # MCP server for Windsurf
├── requirements.txt             # Python dependencies
└── trigger_process_new.bat      # Windows batch launcher
```

### Key Features

**Smart Email Filtering:**
- Skips promotional/marketing emails automatically
- Detects reference emails (account numbers, confirmations)
- Only shows actionable items

**DakBoard Integration:**
- Kill-and-fill approach (deletes old tasks, creates new)
- 5 individual DO NOW tasks (high priority, red)
- 1 DO SOON summary task (medium priority, yellow)
- All details in task title (visible on DakBoard)

**Amplenote Integration:**
- Uses INSERT_NODES actions API (not REST create/update)
- Creates rich notes with checkboxes
- Includes email previews, documents, statistics
- Sections: DO NOW, DO SOON, MONITOR, REFERENCE EMAILS, DOCUMENTS, STATISTICS

**File System Scanning:**
- Inbox folder: `G:\My Drive\01_Operate\Inbox`
- Downloads folder: Recent files (last 7 days)
- Creates tasks for file organization

**Google Drive Tracking:**
- Recent documents (last 7 days)
- Shows what user is actively working on

---

## Output Locations

**JSON File:**
```
G:\My Drive\06_Master_Guides\MCP_Server\process_new_output_YYYYMMDD_HHMMSS.json
```

**Todoist Tasks:**
- Check user's Todoist app
- Tasks auto-created with 🎯 TODAY: and ⏰ SOON: prefixes

**Amplenote Note:**
- URL printed in terminal output
- Format: `https://www.amplenote.com/notes/{uuid}`

---

## Common Issues & Solutions

### "Gmail token expired"
- Just run again - OAuth flow triggers automatically
- User signs in once, token saved

### "Promotional emails appearing"
- Check `gmail_tools.py` skip_senders and skip_keywords
- Add sender domain to skip list

### "Amplenote note empty"
- Fixed - uses INSERT_NODES API now
- Tokens refresh automatically on expiration
- If manual refresh needed, script will prompt with instructions

### "Todoist tasks not created"
- Check API token in environments.json
- Path: `environments.todoist.credentials.apiToken`

### "No workspace open" error
- Don't use grep_search on G: drive without workspace
- Use read_file, find_by_name, or list_dir instead

---

## Configuration Files

**Credentials:**
```
G:\My Drive\03_Areas\Keys\Environments\environments.json
```

Contains tokens for:
- Gmail (OAuth)
- Google Calendar (OAuth)
- Google Drive (OAuth)
- Todoist (API token)
- Amplenote (OAuth access token)

**All authentication is automatic** - tokens refresh as needed.

---

## Master Guides Reference

**Key guides for process new:**
- `09_MASTER_GUIDE_PROCESS_NEW.md` - Process new workflow
- `05_MASTER_GUIDE_Daily_Planning.md` - Daily planning system
- `20_MASTER_GUIDE_Amplenote_API_Integration.md` - Amplenote API
- `21_MASTER_GUIDE_GMAIL_AUTOMATION.md` - Gmail integration
- `22_MASTER_GUIDE_TODOIST_API_INTEGRATION.md` - Todoist integration

**Note:** Guides reference `Scripts/daily_planner.py` which now calls MCP server.

---

## For Future Development

### Adding New Data Sources
1. Create new tool module in `MCP_Server/` (e.g., `slack_tools.py`)
2. Add to `run_process_new.py` imports and initialization
3. Call in data gathering section
4. Add items to categorization logic
5. Update Amplenote output if needed

### Modifying Filters
Edit `gmail_tools.py`:
- `skip_senders` - Add email domains to skip
- `skip_keywords` - Add subject/body keywords to skip
- `reference_patterns` - Add patterns for reference email detection

### Changing Categorization
Edit `run_process_new.py` categorization logic (lines ~93-131):
- Adjust DO NOW criteria (currently: today's date or file organization)
- Adjust DO SOON criteria (currently: future dates)
- Adjust MONITOR criteria (currently: no due date)

---

## Testing

**Quick test:**
```powershell
cd "G:\My Drive\06_Master_Guides\MCP_Server"
python run_process_new.py
```

**Expected output:**
- File scanning results
- Email count (urgent + reference)
- Task count
- Calendar event count
- Document count
- Categorized items (DO NOW, DO SOON, MONITOR)
- Todoist tasks created
- Amplenote note URL

**Typical run time:** 30-60 seconds

---

## Important Notes

1. **Single Source of Truth:** MCP Server is authoritative
2. **No Duplication:** Scripts/daily_planner.py is wrapper only
3. **Fully Autonomous:** No user prompts or configuration needed
4. **Smart Filtering:** Only actionable items, no promotional fluff
5. **DakBoard Compatible:** Individual tasks with full details in titles
6. **Amplenote Rich Content:** Uses INSERT_NODES for proper formatting

---

## Summary for Next Agent

**System is production-ready:**
- ✅ All features working
- ✅ Scripts unified (no duplication)
- ✅ Email filtering enhanced (no promotional emails)
- ✅ Test files cleaned up
- ✅ Documentation complete
- ✅ Amplenote integration working (INSERT_NODES API)
- ✅ Todoist DakBoard integration working (kill-and-fill)
- ✅ Google Drive and file system scanning working

**To run process new:**
```powershell
python "G:\My Drive\06_Master_Guides\MCP_Server\run_process_new.py"
```

**No setup needed. Just run it.**
