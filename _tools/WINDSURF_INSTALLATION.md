# Installing MCP Tools in Windsurf

This guide explains how to install and use the Daily Planner MCP server in Windsurf IDE.

## What You Get

Once installed, Windsurf will have access to these MCP tools:

- **gmail_search** - Search Gmail for emails
- **gmail_get_email** - Get full email content
- **todoist_get_tasks** - Get Todoist tasks with filtering
- **todoist_create_task** - Create new Todoist tasks
- **todoist_update_task** - Update existing tasks
- **todoist_complete_task** - Mark tasks as complete
- **calendar_get_events** - Get Google Calendar events
- **amplenote_create_note** - Create Amplenote notes
- **amplenote_update_note** - Update existing notes
- **amplenote_search_notes** - Search Amplenote
- **run_process_new** - Run complete daily planning workflow

## Installation Steps

### 1. Locate Windsurf MCP Configuration

The MCP configuration file is located at:
```
C:\Users\sol90\AppData\Roaming\Windsurf\mcp_config.json
```

### 2. Add MCP Server Configuration

Create or update `mcp_config.json` with the following content:

```json
{
  "mcpServers": {
    "daily-planner": {
      "command": "python",
      "args": [
        "G:\\My Drive\\06_Skills\\_tools\\server.py"
      ],
      "env": {
        "PYTHONPATH": "G:\\My Drive\\06_Skills\\_tools"
      },
      "disabled": false
    }
  }
}
```

### 3. Install Required Python Packages

Open PowerShell and run:

```powershell
pip install mcp google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests
```

### 4. Verify Installation

1. **Restart Windsurf** - Close and reopen Windsurf IDE
2. **Check MCP Status** - Look for MCP server indicator in Windsurf
3. **Test a Tool** - Try using one of the MCP tools in Cascade

### 5. Test the Installation

Ask Cascade to run a simple test:

```
Use the todoist_get_tasks tool to show me my tasks
```

Or run the full workflow:

```
Use the run_process_new tool to create my daily plan
```

## Configuration File Locations

### MCP Server
- **Server:** `G:\My Drive\06_Skills\_tools\server.py`
- **Tools:** `G:\My Drive\06_Skills\_tools\`
  - `auth_manager.py` - Authentication
  - `gmail_tools.py` - Gmail integration
  - `todoist_tools.py` - Todoist integration
  - `calendar_tools.py` - Calendar integration
  - `amplenote_tools.py` - Amplenote integration
  - `run_process_new.py` - Main workflow

### Credentials
- **Location:** `G:\My Drive\03_Areas\Keys\Environments\environments.json`
- **Contains:** API keys and tokens for all services

## Available MCP Tools

### Gmail Tools

**gmail_search**
```json
{
  "query": "from:example@gmail.com subject:invoice",
  "max_results": 10
}
```

**gmail_get_email**
```json
{
  "message_id": "18d4c5e8f9a2b3c1"
}
```

### Todoist Tools

**todoist_get_tasks**
```json
{
  "filter": "today | overdue"
}
```

**todoist_create_task**
```json
{
  "content": "Review project proposal",
  "description": "Check the Q1 proposal document",
  "priority": 4,
  "due_string": "today"
}
```

**todoist_update_task**
```json
{
  "task_id": "7654321",
  "content": "Updated task title",
  "priority": 3
}
```

**todoist_complete_task**
```json
{
  "task_id": "7654321"
}
```

### Calendar Tools

**calendar_get_events**
```json
{
  "days_ahead": 7,
  "max_results": 20
}
```

### Amplenote Tools

**amplenote_create_note**
```json
{
  "title": "Meeting Notes",
  "body": "# Discussion Points\n- Item 1\n- Item 2",
  "tags": ["meetings", "work"]
}
```

**amplenote_search_notes**
```json
{
  "query": "project planning",
  "max_results": 10
}
```

### Workflow Tool

**run_process_new**
```json
{}
```

This runs the complete daily planning workflow:
1. Scans Gmail for urgent emails
2. Fetches Todoist tasks
3. Gets Calendar events
4. Creates AI-powered task summaries
5. Generates Todoist tasks for DakBoard
6. Creates/updates Amplenote daily plan

## Troubleshooting

### MCP Server Not Starting

**Check Python installation:**
```powershell
python --version
```

**Verify file paths:**
```powershell
Test-Path "G:\My Drive\06_Skills\_tools\server.py"
```

**Check logs:**
Look for MCP server logs in Windsurf's output panel.

### Authentication Errors

**Refresh tokens:**
```powershell
cd "G:\My Drive\06_Skills\_scripts"
python authenticate_all.py
```

**Verify credentials:**
```powershell
Test-Path "G:\My Drive\03_Areas\Keys\Environments\environments.json"
```

### Import Errors

**Install missing packages:**
```powershell
pip install mcp google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests
```

**Check PYTHONPATH:**
Make sure the `env.PYTHONPATH` in `mcp_config.json` points to the correct directory.

### Tool Not Found

**Restart Windsurf:**
After making changes to `mcp_config.json`, always restart Windsurf.

**Check server.py:**
Verify that `server.py` is registering all tools correctly.

## Usage Examples

### Example 1: Check Today's Tasks

```
@Cascade Use todoist_get_tasks with filter "today" to show me what I need to do today
```

### Example 2: Create a Task from Email

```
@Cascade Search my Gmail for emails from "john@example.com" and create a Todoist task to respond
```

### Example 3: Run Daily Planning

```
@Cascade Run the complete process_new workflow to create my daily plan
```

### Example 4: Check Calendar

```
@Cascade Show me my calendar events for the next 3 days
```

### Example 5: Search Amplenote

```
@Cascade Search my Amplenote for notes about "project planning"
```

## Advanced Configuration

### Multiple MCP Servers

You can add multiple MCP servers to `mcp_config.json`:

```json
{
  "mcpServers": {
    "daily-planner": {
      "command": "python",
      "args": ["G:\\My Drive\\06_Skills\\_tools\\server.py"],
      "env": {"PYTHONPATH": "G:\\My Drive\\06_Skills\\_tools"},
      "disabled": false
    },
    "another-server": {
      "command": "node",
      "args": ["path/to/server.js"],
      "disabled": false
    }
  }
}
```

### Disable MCP Server Temporarily

Set `"disabled": true` in the configuration:

```json
{
  "mcpServers": {
    "daily-planner": {
      "command": "python",
      "args": ["G:\\My Drive\\06_Skills\\_tools\\server.py"],
      "disabled": true
    }
  }
}
```

## Related Skills

- [skill_mcp_server_setup.md](../system/skill_mcp_server_setup.md) - MCP server architecture
- [skill_todoist_api.md](../integrations/skill_todoist_api.md) - Todoist API integration
- [skill_amplenote_api.md](../integrations/skill_amplenote_api.md) - Amplenote API integration
- [skill_gmail_automation.md](../integrations/skill_gmail_automation.md) - Gmail automation
- [skill_daily_planning.md](../automation/skill_daily_planning.md) - Daily planning workflow

---

**Last Updated:** March 1, 2026  
**Location:** `G:\My Drive\06_Skills\_tools\WINDSURF_INSTALLATION.md`
