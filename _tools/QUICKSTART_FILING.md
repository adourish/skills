# Quick Start: Filing New Tools

Fast reference for organizing tools in the Skills folder.

## Quick Decision

**Ask: What's the primary purpose?**

| Purpose | Folder | Example |
|---------|--------|---------|
| Daily automation | `_tools/` | Email → Tasks workflow |
| One-time utility | `_scripts/` | Data cleanup |
| Documentation | `documentation/` | Diagram converter |
| API wrapper | `integrations/` | Notion client |
| Dev setup | `development/` | Linter config |
| Workflow | `automation/` | Multi-step process |
| System config | `system/` | Environment setup |

## Common Patterns

### Daily Planning Tools → `_tools/`
- Runs regularly (scheduled)
- Part of daily workflow
- Integrates multiple services
- Examples: `run_process_new_v2.py`, `scheduler.py`

### Documentation Tools → `documentation/`
- Creates/converts docs
- Generates diagrams
- Format conversion
- Examples: `mermaid_to_visio.py`

### Utility Scripts → `_scripts/`
- Run manually when needed
- One-time or occasional use
- Testing/debugging helpers
- Examples: `cleanup_old_tasks.py`

### API Integrations → `integrations/`
- Reusable API client
- Service wrapper
- Used by multiple tools
- Examples: `notion_client.py`

## Filing Steps

1. **Identify purpose** - What does it do?
2. **Choose folder** - Use table above
3. **Add README** - Document usage
4. **Test** - Verify it works

## When Unsure

**Default:** Start in `_scripts/`, move to `_tools/` if it becomes part of regular workflow.

See `HOW_TO_FILE_TOOLS.md` for complete guide.
