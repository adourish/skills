# Amplenote Relay Systems - Master Guide

**Last Updated:** February 21, 2026  
**Version:** 1.0  
**Author:** Cascade AI Assistant

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [System Comparison](#system-comparison)
3. [MCP Server Relay](#mcp-server-relay)
4. [Chrome Extension Hybrid](#chrome-extension-hybrid)
5. [Direct Plugin v2.0](#direct-plugin-v20)
6. [Decision Guide](#decision-guide)
7. [Setup Instructions](#setup-instructions)
8. [Usage Examples](#usage-examples)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)
11. [API Reference](#api-reference)
12. [Advanced Workflows](#advanced-workflows)

---

## Overview

You have **three powerful relay systems** for Amplenote automation, each designed for different use cases:

### 1. MCP Server Relay
Queue-based system using Model Context Protocol for script automation and Cascade integration.

### 2. Chrome Extension Hybrid
Real-time browser extension with visual UI for web content capture and automation.

### 3. Direct Plugin v2.0
Standalone Amplenote plugin for manual note operations without external dependencies.

**All files located at:** `C:\Users\sol90\CascadeProjects\`

---

## System Comparison

### Quick Reference Table

| Feature | MCP Server | Chrome Extension | Direct Plugin |
|---------|-----------|------------------|---------------|
| **Real-time Processing** | ❌ Manual | ✅ Automatic | ✅ Immediate |
| **Web Content Capture** | ❌ No | ✅ Yes | ❌ No |
| **External Scripts** | ✅ Easy | ⚠️ Via Extension API | ❌ No |
| **Visual Queue UI** | ❌ No | ✅ Popup | ❌ No |
| **Context Menu** | ❌ No | ✅ Right-click | ❌ No |
| **Cascade Integration** | ✅ Native | ❌ No | ❌ No |
| **Browser Required** | ❌ No | ✅ Chrome | ✅ Any |
| **Setup Complexity** | ⚠️ Medium | ✅ Easy | ✅ Very Easy |
| **Scheduled Tasks** | ✅ Yes | ⚠️ Via Scripts | ❌ No |
| **Batch Operations** | ✅ Yes | ✅ Yes | ⚠️ Manual |
| **Cross-platform** | ✅ Yes | ❌ Chrome Only | ✅ Yes |

### Architecture Diagrams

**MCP Server:**
```
Scripts/Apps → MCP Server (JSON Queue) → Manual Processing → Amplenote
     ↓              ↓                           ↓
  Python/JS    Local Storage              Plugin Functions
```

**Chrome Extension:**
```
Web Content → Chrome Extension → Amplenote Plugin → Real-time Processing
     ↓              ↓                    ↓
  Capture      Local Storage      JavaScript Bridge
```

**Direct Plugin:**
```
User Input → Amplenote Plugin → Immediate Execution → Notes
     ↓              ↓                      ↓
  Manual      Plugin Functions      Amplenote API
```

---

## MCP Server Relay

### Location
`C:\Users\sol90\CascadeProjects\amplenote-relay-mcp\`

### What It Does
- Manages a JSON-based queue of note operations
- Integrates with Cascade/Windsurf via MCP protocol
- Enables Python, Node.js, PowerShell script automation
- Supports scheduled and batch operations

### Key Files
- `index.js` - MCP server implementation
- `package.json` - Dependencies
- `amplenote-queue.json` - Queue storage (auto-created)
- `README.md` - Full documentation
- `QUICKSTART.md` - 5-minute setup
- `USAGE_EXAMPLES.md` - 10+ practical examples

### Setup (5 minutes)

**Step 1: Configure Windsurf MCP Settings**

1. Open: `%APPDATA%\Windsurf\mcp_settings.json`
2. Add this configuration:

```json
{
  "mcpServers": {
    "amplenote-relay": {
      "command": "node",
      "args": ["C:\\Users\\sol90\\CascadeProjects\\amplenote-relay-mcp\\index.js"]
    }
  }
}
```

3. Save and restart Windsurf

**Step 2: Verify Installation**

In Cascade, test the MCP tools:
```
Use the get_all_operations tool
```

Expected response:
```json
{
  "success": true,
  "total": 0,
  "pending": 0,
  "completed": 0,
  "failed": 0,
  "items": []
}
```

### MCP Tools Available

1. **add_note_operation** - Queue create/update/append/delete operations
2. **get_pending_operations** - View pending items
3. **get_all_operations** - View all items with statistics
4. **mark_operation_complete** - Mark items as processed
5. **mark_operation_failed** - Mark items as failed
6. **clear_completed_operations** - Clean up the queue

### Operation Format

```json
{
  "operation": "create|update|append|delete",
  "noteName": "string",      // Required for create
  "noteUUID": "string",      // Required for update/append/delete
  "content": "string",       // Required for create/update/append
  "tags": ["array"]          // Optional for create
}
```

### Usage Examples

**From Cascade:**
```
Add a note operation:
- operation: create
- noteName: Daily Journal 2026-02-21
- content: # Today's Notes\n\n## Morning
- tags: ["journal", "daily"]
```

**From Python Script:**
```python
import subprocess
import json

def add_note_operation(operation, **kwargs):
    args = {'operation': operation, **kwargs}
    # Call MCP server via subprocess
    # See USAGE_EXAMPLES.md for full implementation
```

**From Node.js:**
```javascript
// See amplenote-relay-mcp/USAGE_EXAMPLES.md
// for complete implementation examples
```

### Best Use Cases
- ✅ Scheduled automation (daily journals, reports)
- ✅ Python/Node.js script integration
- ✅ Cascade/Windsurf workflows
- ✅ Batch note creation from data sources
- ✅ Server-side processing
- ✅ Headless operation

---

## Chrome Extension Hybrid

### Location
`C:\Users\sol90\CascadeProjects\amplenote-chrome-relay\`

### What It Does
- Captures web content via context menus
- Provides visual queue management UI
- Real-time bidirectional communication with Amplenote
- Browser-based automation and scripting

### Key Files
- `manifest.json` - Extension configuration
- `background.js` - Queue management service worker
- `content.js` - Bridge between extension and page
- `injected.js` - JavaScript API for Amplenote
- `popup.html` - Visual queue interface
- `popup.js` - Popup logic
- `README.md` - Complete documentation

### Setup (3 minutes)

**Step 1: Install Chrome Extension**

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select folder: `C:\Users\sol90\CascadeProjects\amplenote-chrome-relay`
5. Extension icon appears in toolbar

**Step 2: Create Extension Icons (Optional for Testing)**

Create three PNG files in `icons/` folder:
- `icon16.png` (16x16 pixels)
- `icon48.png` (48x48 pixels)
- `icon128.png` (128x128 pixels)

Use any icon generator or simple colored squares. Extension works without icons but shows default icon.

**Step 3: Install Amplenote Plugin**

1. In Amplenote, create new note: "Content Access Plugin - Chrome Hybrid"
2. Create table at top:
   - Row 1: `name` | `Content Access Plugin - Chrome Hybrid`
   - Row 2: `description` | `Real-time relay with Chrome extension`
   - Row 3: `icon` | `code`
3. Below table, create code block: ` ```javascript `
4. Copy code from: `C:\Users\sol90\CascadeProjects\amplenote-access-plugin\lib\plugin-chrome-hybrid.js`
   - Copy lines 1-257 (the object inside, excluding `const plugin = ` and `module.exports`)
5. Close code block: ` ``` `
6. Go to Settings → Plugins → Add a plugin → Select your note

**Step 4: Verify Connection**

1. Open Amplenote in Chrome
2. Open browser console (F12)
3. Should see: "Amplenote Relay content script loaded"
4. Type: `window.AmplnoteRelay.ready` - should return `true`

### Features

**Context Menu Integration:**
- Right-click selected text → "Save to Amplenote"
- Right-click link → "Save to Amplenote"
- Right-click page → "Save to Amplenote"
- Auto-tags with "web-clip" and includes source URL

**Popup Interface:**
- View queue statistics (total, pending, completed)
- Add operations via form
- View operation history
- One-click queue management

**JavaScript API:**
Available on Amplenote pages:
```javascript
window.AmplnoteRelay.addOperation(operation)
window.AmplnoteRelay.getPending()
window.AmplnoteRelay.getAll()
window.AmplnoteRelay.markComplete(itemId)
window.AmplnoteRelay.markFailed(itemId, error)
window.AmplnoteRelay.clearCompleted()
```

### Usage Examples

**Save Web Selection:**
1. Select text on any webpage
2. Right-click → "Save to Amplenote"
3. Content queued with source metadata
4. In Amplenote: Note menu → "Process Queue from Chrome"

**From Browser Console:**
```javascript
// On Amplenote page
await window.AmplnoteRelay.addOperation({
  operation: 'create',
  noteName: 'Research Note',
  content: 'Interesting finding...',
  tags: ['research', 'web']
});
```

**Bookmarklet:**
```javascript
javascript:(function(){
  window.AmplnoteRelay.addOperation({
    operation: 'create',
    noteName: document.title,
    content: '[' + document.title + '](' + location.href + ')',
    tags: ['bookmark']
  });
  alert('Saved to Amplenote!');
})();
```

### Amplenote Plugin Functions

- **Process Queue from Chrome** - Process all pending operations
- **Process Next Queue Item** - Process one operation at a time
- **View Queue Status** - See queue statistics in note
- Plus all standard plugin functions (Create, Update, Append, etc.)

### Best Use Cases
- ✅ Web content capture and clipping
- ✅ Research note collection
- ✅ Reading list management
- ✅ Browser-based automation
- ✅ Real-time processing
- ✅ Visual queue management
- ✅ Interactive workflows

---

## Direct Plugin v2.0

### Location
`C:\Users\sol90\CascadeProjects\amplenote-access-plugin\`

### What It Does
- Standalone Amplenote plugin for note operations
- No external dependencies or setup
- Direct, immediate execution
- Full read and write capabilities

### Key Files
- `lib/plugin.js` - Core plugin code (v2.0)
- `README.md` - Feature documentation
- `PLUGIN_V2_FOR_AMPLENOTE.md` - Installation guide

### Setup (2 minutes)

**Step 1: Create Plugin Note**

1. In Amplenote, create new note: "Content Access Plugin"
2. Create table at top:
   - Row 1: `name` | `Content Access Plugin`
   - Row 2: `description` | `Read and write access to Amplenote notes`
   - Row 3: `icon` | `code`

**Step 2: Add Plugin Code**

1. Below table, create code block: ` ```javascript `
2. Copy code from: `C:\Users\sol90\CascadeProjects\amplenote-access-plugin\lib\plugin.js`
   - Copy lines 1-257 (the object inside, excluding `const plugin = ` and `module.exports`)
3. Close code block: ` ``` `

**Step 3: Install Plugin**

1. Go to Settings → Plugins
2. Click "Add a plugin"
3. Select your plugin note
4. Enable the plugin

### Features

**Write Operations:**
- Create New Note - Interactive note creation with tags
- Update Current Note - Replace content of open note
- Append to Current Note - Add content to end
- Update Note by UUID - Update any note by UUID
- Delete Note by UUID - Delete with confirmation

**Read Operations:**
- Export Note Content - Export as JSON
- List All Notes - Show all notes with UUIDs
- Search Notes - Search with query and preview
- Get Note by Tag - Retrieve notes by tag
- Export All Notes Data - Complete export

**Text Operations:**
- Insert Current Note Info - Quick metadata insertion
- Analyze Note Structure - Count headers, links, tasks

### Usage

1. Open any note in Amplenote
2. Click three-dot menu (⋮) at top right
3. Click "More options"
4. Select desired plugin function

### Best Use Cases
- ✅ Quick manual operations
- ✅ Direct note management
- ✅ No setup required
- ✅ Simple workflows
- ✅ Learning Amplenote API
- ✅ Backup and export

---

## Decision Guide

### Which System Should I Use?

**Use MCP Server if you:**
- Need scheduled automation (daily journals, reports)
- Use Python, Node.js, or PowerShell scripts
- Want Cascade/Windsurf integration
- Need headless operation
- Prefer command-line workflows
- Have server-side processing needs

**Use Chrome Extension if you:**
- Capture web content frequently
- Need real-time processing
- Want visual queue management
- Work primarily in browser
- Like context menu shortcuts
- Need web-based automation

**Use Direct Plugin if you:**
- Want simplest setup
- Need manual operations only
- Don't want external dependencies
- Prefer direct control
- Are learning Amplenote API
- Need quick note management

**Use Multiple Systems if you:**
- Want maximum flexibility
- Have different contexts (web vs scripts)
- Need redundancy
- Want to test different approaches

### Decision Tree

```
START
  ↓
Do you need to capture web content?
  ├─ YES → Chrome Extension
  └─ NO → Continue
      ↓
Do you need scheduled/automated operations?
  ├─ YES → MCP Server
  └─ NO → Continue
      ↓
Do you need external script integration?
  ├─ YES → MCP Server
  └─ NO → Continue
      ↓
Do you want visual queue management?
  ├─ YES → Chrome Extension
  └─ NO → Continue
      ↓
Do you want the simplest setup?
  ├─ YES → Direct Plugin
  └─ NO → MCP Server or Chrome Extension
```

---

## Setup Instructions

### Prerequisites

**All Systems:**
- Amplenote account
- Modern web browser

**MCP Server:**
- Node.js 18+ installed
- Windsurf IDE

**Chrome Extension:**
- Google Chrome browser
- Developer mode enabled

**Direct Plugin:**
- None (works standalone)

### Installation Checklist

**MCP Server:**
- [ ] Node.js installed and in PATH
- [ ] MCP settings configured in Windsurf
- [ ] Windsurf restarted
- [ ] MCP tools visible in Cascade
- [ ] Test operation successful

**Chrome Extension:**
- [ ] Extension loaded in Chrome
- [ ] Icons created (optional)
- [ ] Amplenote plugin installed
- [ ] Connection verified in console
- [ ] Context menu working

**Direct Plugin:**
- [ ] Plugin note created
- [ ] Code pasted correctly
- [ ] Plugin installed in settings
- [ ] Plugin enabled
- [ ] Functions visible in note menu

---

## Usage Examples

### Daily Journal Automation

**MCP Server Approach:**
```javascript
// Scheduled script (runs daily)
const today = new Date().toISOString().split('T')[0];

await mcp.add_note_operation({
  operation: "create",
  noteName: `Daily Journal - ${today}`,
  content: `# ${today}\n\n## Morning\n\n## Afternoon\n\n## Evening\n\n## Notes\n`,
  tags: ["journal", "daily", today]
});
```

**Chrome Extension Approach:**
```javascript
// Bookmarklet or scheduled extension script
const today = new Date().toISOString().split('T')[0];

window.AmplnoteRelay.addOperation({
  operation: "create",
  noteName: `Daily Journal - ${today}`,
  content: `# ${today}\n\n## Morning\n\n## Afternoon\n\n## Evening\n`,
  tags: ["journal", "daily"]
});
```

**Direct Plugin Approach:**
1. Open Amplenote
2. Note menu → "Create New Note"
3. Enter name: "Daily Journal - [date]"
4. Enter content manually
5. Add tags: "journal, daily"

### Web Content Capture

**Chrome Extension (Best):**
1. Select text on webpage
2. Right-click → "Save to Amplenote"
3. Content queued with source URL
4. Process queue in Amplenote

**MCP Server (Alternative):**
```python
# Python script to capture from clipboard
import pyperclip

content = pyperclip.paste()
add_note_operation(
    'create',
    noteName='Web Clip',
    content=content,
    tags=['web-clip']
)
```

### Meeting Notes Creation

**MCP Server (Scheduled):**
```javascript
// From calendar integration
async function createMeetingNote(meeting) {
  const content = `# ${meeting.title}
  
**Date:** ${meeting.date}
**Attendees:** ${meeting.attendees.join(', ')}

## Agenda

## Discussion

## Action Items
- [ ] 

## Next Steps
`;

  await mcp.add_note_operation({
    operation: 'create',
    noteName: `Meeting: ${meeting.title}`,
    content: content,
    tags: ['meetings', 'work']
  });
}
```

**Chrome Extension (Manual):**
1. Click extension icon
2. "+ Add Operation"
3. Select "Create Note"
4. Fill in meeting details
5. Process in Amplenote

### Batch Note Creation

**MCP Server (Best):**
```javascript
const bookmarks = [
  { title: "Article 1", url: "https://example.com/1" },
  { title: "Article 2", url: "https://example.com/2" }
];

for (const bookmark of bookmarks) {
  await mcp.add_note_operation({
    operation: 'create',
    noteName: bookmark.title,
    content: `[Link](${bookmark.url})`,
    tags: ['reading']
  });
}
```

### Research Workflow

**Chrome Extension (Best):**
1. Browse research sources
2. Select interesting passages
3. Right-click → "Save to Amplenote"
4. All snippets queued with sources
5. Batch process in Amplenote
6. Review and organize

**Combined Approach:**
1. Use Chrome extension for web capture
2. Use MCP server for scheduled summaries
3. Use direct plugin for manual organization

---

## Best Practices

### Queue Management

**MCP Server:**
- Clear completed operations regularly
- Monitor queue size
- Use meaningful operation names
- Add timestamps to content
- Tag operations by source

**Chrome Extension:**
- Check popup regularly
- Process queue daily
- Clear completed items
- Use consistent tagging
- Review failed operations

### Error Handling

**Always:**
- Validate UUIDs before update/append/delete
- Check operation format
- Handle failed operations
- Log errors for debugging
- Test with small batches first

**MCP Server:**
```javascript
try {
  const result = await mcp.add_note_operation(operation);
  if (!result.success) {
    console.error('Failed:', result.error);
  }
} catch (error) {
  console.error('Error:', error.message);
}
```

**Chrome Extension:**
```javascript
try {
  await window.AmplnoteRelay.addOperation(operation);
} catch (error) {
  console.error('Failed to queue:', error);
}
```

### Content Formatting

**Use Markdown:**
```markdown
# Heading 1
## Heading 2

**Bold text**
*Italic text*

- Bullet list
- Item 2

1. Numbered list
2. Item 2

[Link text](https://url.com)

- [ ] Task item
- [x] Completed task
```

**Include Metadata:**
```javascript
const content = `# ${title}

**Source:** ${sourceUrl}
**Date:** ${new Date().toISOString()}
**Tags:** ${tags.join(', ')}

---

${actualContent}
`;
```

### Tagging Strategy

**Consistent Tags:**
- Use lowercase
- Hyphenate multi-word tags
- Create tag hierarchy
- Document tag meanings
- Review tags periodically

**Example Tag System:**
```
Source: web-clip, email, manual
Type: article, note, task, meeting
Status: inbox, processed, archived
Project: project-a, project-b
Date: 2026-02, 2026-q1
```

### Security

**Protect UUIDs:**
- Don't share note UUIDs publicly
- Store UUIDs securely
- Use environment variables for scripts
- Rotate if compromised

**Validate Input:**
- Sanitize user input
- Validate operation format
- Check content length
- Prevent injection attacks

---

## Troubleshooting

### MCP Server Issues

**MCP tools not showing in Cascade:**
- ✓ Check Node.js is installed: `node --version`
- ✓ Verify MCP settings path is correct
- ✓ Restart Windsurf completely
- ✓ Check for typos in settings JSON
- ✓ View Windsurf logs for errors

**Queue file not found:**
- ✓ File is auto-created on first use
- ✓ Check path: `C:\Users\sol90\CascadeProjects\amplenote-relay-mcp\amplenote-queue.json`
- ✓ Verify folder permissions
- ✓ Try running MCP server manually

**Operations not being added:**
- ✓ Check operation format matches schema
- ✓ Use `get_all_operations` to verify
- ✓ Check for error messages in response
- ✓ Validate JSON syntax

### Chrome Extension Issues

**Extension not loading:**
- ✓ Check Chrome version (requires Manifest V3)
- ✓ Verify folder path is correct
- ✓ Check for errors in `chrome://extensions/`
- ✓ Reload extension
- ✓ Check console for errors

**API not available:**
- ✓ Refresh Amplenote page
- ✓ Check console for "Amplenote Relay" messages
- ✓ Verify extension is enabled
- ✓ Check content script loaded
- ✓ Try: `window.AmplnoteRelay.ready`

**Queue not processing:**
- ✓ Check Amplenote plugin is installed
- ✓ Verify extension is running
- ✓ Check browser console for errors
- ✓ Try processing one item at a time
- ✓ Check operation format

**Context menu not appearing:**
- ✓ Reload extension
- ✓ Check extension permissions
- ✓ Verify on supported page
- ✓ Check background script errors

### Direct Plugin Issues

**Plugin not appearing in menu:**
- ✓ Check plugin is enabled in settings
- ✓ Verify code format is correct
- ✓ Check for JavaScript syntax errors
- ✓ Ensure table is properly formatted
- ✓ Reload Amplenote page

**Functions failing:**
- ✓ Check note is open (for current note functions)
- ✓ Verify UUID is correct (for UUID functions)
- ✓ Check Amplenote console for errors
- ✓ Try with simple test note first

**Code block issues:**
- ✓ Ensure code block starts with ` ```javascript `
- ✓ Ensure code block ends with ` ``` `
- ✓ No extra text after closing backticks
- ✓ Copy object only (not `const plugin =` or `module.exports`)

### General Issues

**Operations failing:**
- ✓ Check operation format
- ✓ Verify UUIDs are correct
- ✓ Check content is valid
- ✓ Test with simple operation first
- ✓ Check Amplenote API limits

**Duplicate notes created:**
- ✓ Check for duplicate queue items
- ✓ Implement deduplication logic
- ✓ Use unique identifiers in names
- ✓ Clear completed operations

**Performance issues:**
- ✓ Process operations in batches
- ✓ Clear completed items regularly
- ✓ Limit queue size
- ✓ Optimize content size

---

## API Reference

### Operation Format (All Systems)

```typescript
interface Operation {
  operation: 'create' | 'update' | 'append' | 'delete';
  noteName?: string;      // Required for create
  noteUUID?: string;      // Required for update/append/delete
  content?: string;       // Required for create/update/append
  tags?: string[];        // Optional for create
  source?: {              // Optional metadata
    url?: string;
    title?: string;
    timestamp?: string;
  };
}
```

### MCP Server Tools

**add_note_operation**
```javascript
await mcp.add_note_operation({
  operation: 'create',
  noteName: 'Note Title',
  content: 'Content here',
  tags: ['tag1', 'tag2']
});
```

**get_pending_operations**
```javascript
const pending = await mcp.get_pending_operations();
// Returns: { success: true, count: N, items: [...] }
```

**get_all_operations**
```javascript
const all = await mcp.get_all_operations();
// Returns: { success: true, total: N, pending: N, completed: N, failed: N, items: [...] }
```

**mark_operation_complete**
```javascript
await mcp.mark_operation_complete({ itemId: 'id-here' });
```

**mark_operation_failed**
```javascript
await mcp.mark_operation_failed({ itemId: 'id-here', error: 'Error message' });
```

**clear_completed_operations**
```javascript
const result = await mcp.clear_completed_operations();
// Returns: { success: true, count: N }
```

### Chrome Extension API

**addOperation**
```javascript
await window.AmplnoteRelay.addOperation({
  operation: 'create',
  noteName: 'Note Title',
  content: 'Content here',
  tags: ['tag1']
});
```

**getPending**
```javascript
const pending = await window.AmplnoteRelay.getPending();
```

**getAll**
```javascript
const all = await window.AmplnoteRelay.getAll();
```

**markComplete**
```javascript
await window.AmplnoteRelay.markComplete(itemId);
```

**markFailed**
```javascript
await window.AmplnoteRelay.markFailed(itemId, 'Error message');
```

**clearCompleted**
```javascript
await window.AmplnoteRelay.clearCompleted();
```

### Amplenote Plugin API (Used Internally)

**Create Note:**
```javascript
const newNote = await app.createNote(noteName, tags);
// Returns: { uuid: 'note-uuid' }
```

**Insert Content:**
```javascript
await app.insertNoteContent({ uuid: noteUUID }, content);
```

**Replace Content:**
```javascript
await app.replaceNoteContent({ uuid: noteUUID }, newContent);
```

**Get Content:**
```javascript
const content = await app.getNoteContent({ uuid: noteUUID });
```

**Delete Note:**
```javascript
await app.deleteNote(noteUUID);
```

**Filter Notes:**
```javascript
const notes = await app.filterNotes({ query: 'search term' });
const taggedNotes = await app.filterNotes({ tag: 'tagname' });
```

---

## Advanced Workflows

### Multi-System Integration

**Research Pipeline:**
1. **Chrome Extension** - Capture web snippets throughout day
2. **MCP Server** - Nightly script consolidates into research note
3. **Direct Plugin** - Manual review and organization

**Task Management:**
1. **Chrome Extension** - Capture tasks from emails/web
2. **MCP Server** - Sync with external task manager
3. **Direct Plugin** - Manual task updates

**Content Creation:**
1. **Chrome Extension** - Collect sources and references
2. **MCP Server** - Generate outline from template
3. **Direct Plugin** - Write and edit content

### Automation Examples

**Daily Digest (MCP Server):**
```javascript
// Run daily at 6 AM
async function createDailyDigest() {
  const today = new Date().toISOString().split('T')[0];
  
  // Get yesterday's notes
  const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];
  
  const content = `# Daily Digest - ${today}

## Yesterday's Activity
[Auto-generated summary]

## Today's Focus
- [ ] Priority 1
- [ ] Priority 2

## Notes
`;

  await mcp.add_note_operation({
    operation: 'create',
    noteName: `Digest - ${today}`,
    content: content,
    tags: ['digest', 'daily', today]
  });
}
```

**Reading List Sync (Chrome Extension):**
```javascript
// Browser extension background script
chrome.bookmarks.onCreated.addListener((id, bookmark) => {
  if (bookmark.url && bookmark.url.includes('article')) {
    window.AmplnoteRelay.addOperation({
      operation: 'create',
      noteName: 'Reading: ' + bookmark.title,
      content: `[${bookmark.title}](${bookmark.url})`,
      tags: ['reading', 'to-read']
    });
  }
});
```

**Meeting Notes Template (MCP Server):**
```javascript
async function createMeetingNote(title, attendees, date) {
  const template = `# ${title}

**Date:** ${date}
**Attendees:** ${attendees.join(', ')}

## Pre-Meeting
- [ ] Review agenda
- [ ] Prepare materials

## Agenda
1. 

## Discussion Notes

## Decisions Made

## Action Items
- [ ] 

## Follow-up
`;

  await mcp.add_note_operation({
    operation: 'create',
    noteName: `Meeting: ${title} - ${date}`,
    content: template,
    tags: ['meetings', 'work', date]
  });
}
```

---

## Quick Reference

### File Locations

```
C:\Users\sol90\CascadeProjects\
├── amplenote-relay-mcp/          # MCP Server
│   ├── index.js
│   ├── amplenote-queue.json
│   └── README.md
│
├── amplenote-chrome-relay/       # Chrome Extension
│   ├── manifest.json
│   ├── background.js
│   ├── popup.html
│   └── README.md
│
└── amplenote-access-plugin/      # Amplenote Plugins
    └── lib/
        ├── plugin.js              # v2.0 Direct
        ├── plugin-with-relay.js   # MCP integration
        └── plugin-chrome-hybrid.js # Chrome integration
```

### Configuration Files

**Windsurf MCP Settings:**
`%APPDATA%\Windsurf\mcp_settings.json`

**Chrome Extensions:**
`chrome://extensions/`

**Amplenote Plugins:**
Settings → Plugins in Amplenote

### Support Resources

**Documentation:**
- MCP Server: `amplenote-relay-mcp/README.md`
- Chrome Extension: `amplenote-chrome-relay/README.md`
- Direct Plugin: `amplenote-access-plugin/README.md`
- This Guide: `G:\My Drive\06_Master_Guides\Amplenote_Relay_Systems_Master_Guide.md`

**Example Code:**
- MCP: `amplenote-relay-mcp/USAGE_EXAMPLES.md`
- Chrome: `amplenote-chrome-relay/README.md` (examples section)
- Comparison: `C:\Users\sol90\CascadeProjects\RELAY_COMPARISON.md`

---

## Appendix

### Version History

**v1.0 (February 21, 2026)**
- Initial master guide creation
- All three systems documented
- Complete setup instructions
- Usage examples and best practices

### Future Enhancements

**Planned Features:**
- [ ] Mobile companion apps
- [ ] Webhook support
- [ ] Operation templates
- [ ] Priority queues
- [ ] Scheduled operations UI
- [ ] Export/import configurations

### Contributing

To improve this guide:
1. Test workflows and document findings
2. Add new usage examples
3. Update troubleshooting section
4. Share automation scripts
5. Report issues and solutions

### License

All code and documentation: MIT License

---

**Last Updated:** February 21, 2026  
**Next Review:** As needed when systems are updated

---

*This master guide is your complete reference for all Amplenote relay systems. Bookmark this file for quick access to setup instructions, usage examples, and troubleshooting tips.*
