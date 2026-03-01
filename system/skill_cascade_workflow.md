# CASCADE Workflow: How I Find Context and Continue Work

**Visual Guide to My Decision-Making Process**

**Last Updated:** February 22, 2026

---

## 🎯 Starting Point: Every Request Begins Here

```
┌─────────────────────────────────────────────────────────────┐
│                    USER MAKES REQUEST                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│         STEP 1: Check Root README.md First                   │
│         Location: G:\My Drive\README.md (00_README.md)       │
│                                                              │
│  What I Look For:                                            │
│  • "Process New" workflow                                    │
│  • Routing rules (Todoist/Amplenote/Calendar)                │
│  • Credential sources (KeePass, environments.json)           │
│  • Daily/Weekly/As-Needed process categories                 │
│  • Quick reference by use case                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│         STEP 2: Check Master Guides Index                    │
│         Location: 06_Master_Guides\01_MASTER_GUIDE_README.md │
│                                                              │
│  What I Look For:                                            │
│  • All 13 master guides listed by category                   │
│  • Keywords for each guide                                   │
│  • Difficulty levels                                         │
│  • "Use When" descriptions                                   │
│  • Related guides cross-references                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│         STEP 3: Identify Relevant Master Guide(s)            │
│                                                              │
│  Based on request keywords, I select:                        │
│  • Daily Planning → 05_MASTER_GUIDE_Daily_Planning.md        │
│  • Email Processing → 06_MASTER_GUIDE_Email_Processing.md    │
│  • Credentials → 04_MASTER_GUIDE_Environments_and_Credentials│
│  • KeePass → 08_MASTER_GUIDE_KeePass_Integration.md          │
│  • File Organization → 07_MASTER_GUIDE_FILE_ORGANIZATION.md  │
│  • Salesforce → 14_MASTER_GUIDE_Salesforce_Development.md    │
│  • Git → 10_MASTER_GUIDE_GIT_VERSION_CONTROL.md              │
│  • etc.                                                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│         STEP 4: Check Specific Master Guide                  │
│                                                              │
│  I read the relevant guide for:                              │
│  • Exact commands to run                                     │
│  • File locations                                            │
│  • Credential sources                                        │
│  • Workflow steps                                            │
│  • Troubleshooting tips                                      │
│  • Related guides to check                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│         STEP 5: Check Supporting Documents                   │
│                                                              │
│  If needed, I also check:                                    │
│  • ROUTING_RULES.md (where things go)                        │
│  • COMPLETE_FILING_GUIDE.md (file organization)              │
│  • environments.json (API credentials)                       │
│  • KeePass database (passwords)                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│         STEP 6: Execute Based on Documentation               │
│                                                              │
│  I follow the documented workflow exactly                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Decision Tree: Request Type → Master Guide

```
USER REQUEST
    │
    ├─ "process new" / "check emails" / "daily planning"
    │   └─→ Root README.md → "Process New" section
    │       └─→ MASTER_GUIDE_Daily_Planning.md
    │
    ├─ "file this" / "organize downloads" / "where does X go"
    │   └─→ MASTER_GUIDE_FILE_ORGANIZATION.md
    │       └─→ COMPLETE_FILING_GUIDE.md
    │
    ├─ "get credential" / "find password" / "API key"
    │   └─→ MASTER_GUIDE_Environments_and_Credentials.md
    │       ├─→ Check KeePass (keys pass.kdbx)
    │       ├─→ Check environments.json
    │       └─→ Check .env file
    │
    ├─ "search keepass" / "get password from keepass"
    │   └─→ MASTER_GUIDE_KeePass_Integration.md
    │
    ├─ "deploy salesforce" / "apex" / "lwc"
    │   └─→ Salesforce_Development_Master_Guide.md
    │       └─→ MASTER_GUIDE_POWERSHELL_AUTOMATION.md (for sfsync)
    │
    ├─ "git" / "branch" / "commit" / "merge"
    │   └─→ MASTER_GUIDE_GIT_VERSION_CONTROL.md
    │
    ├─ "create ADO work item" / "user story"
    │   └─→ MASTER_GUIDE_AZURE_DEVOPS_AUTOMATION.md
    │       └─→ MASTER_GUIDE_BROWSER_AUTOMATION.md
    │
    ├─ "automate browser" / "playwright"
    │   └─→ MASTER_GUIDE_BROWSER_AUTOMATION.md
    │
    ├─ "amplenote" / "create note" / "sync to amplenote"
    │   └─→ MASTER_GUIDE_Amplenote_API_Integration.md
    │       └─→ Check ROUTING_RULES.md (tasks vs notes)
    │
    ├─ "todoist" / "tasks" / "where do tasks go"
    │   └─→ ROUTING_RULES.md
    │       └─→ MASTER_GUIDE_Daily_Planning.md
    │
    └─ "email processing" / "extract tasks from email"
        └─→ MASTER_GUIDE_Email_Processing.md
            └─→ ROUTING_RULES.md (routing to Todoist/Calendar/Amplenote)
```

---

## 🎯 Decision Trees

### Email Processing Decision Tree

**When "Process New" is requested, follow this decision flow:**

```
📧 NEW EMAIL RECEIVED
    │
    ├─→ Is sender in spam/newsletter patterns?
    │   ├─→ YES → Skip (filter out)
    │   └─→ NO → Continue
    │
    ├─→ Contains actionable patterns?
    │   │   (action verbs + deadlines + requests)
    │   │
    │   ├─→ YES → ACTIONABLE EMAIL
    │   │   │
    │   │   ├─→ Extract deadline from content
    │   │   ├─→ Determine priority (urgent/normal)
    │   │   ├─→ Create Todoist task
    │   │   │   ├─→ Title: Extracted action
    │   │   │   ├─→ Due date: Parsed deadline
    │   │   │   ├─→ Priority: P1/P2/P3
    │   │   │   ├─→ Labels: #email, #work/#personal
    │   │   │   └─→ Description: Email link + context
    │   │   │
    │   │   └─→ Add to Kanban board (Today/Tomorrow/Week/Backlog)
    │   │
    │   └─→ NO → Is it important reference info?
    │       │
    │       ├─→ YES → REFERENCE EMAIL
    │       │   │
    │       │   ├─→ Contains confirmation numbers?
    │       │   ├─→ Contains credentials/access info?
    │       │   ├─→ Important announcement/policy?
    │       │   │
    │       │   └─→ Create Amplenote note
    │       │       ├─→ Title: Subject + sender
    │       │       ├─→ Tags: #email, #reference
    │       │       └─→ Content: Full email body
    │       │
    │       └─→ NO → Skip (not actionable, not important)
    │
    └─→ Check for missed items
        ├─→ From important sender?
        ├─→ Has deadline but no Todoist task?
        └─→ Flag as potentially missed
```

**Holistic Data Collection (Personal + Work):**
```
"PROCESS NEW" COMMAND
    │
    ├─→ 📧 EMAIL SOURCES
    │   │
    │   ├─→ Gmail (last 2 weeks)
    │   │   ├─→ API: Gmail API v1
    │   │   ├─→ Filter spam/shipping notifications
    │   │   ├─→ Identify actionable items
    │   │   └─→ Extract reference items
    │   │
    │   └─→ Outlook (last 2 weeks)
    │       ├─→ API: Microsoft Graph v1.0
    │       ├─→ Endpoint: /me/messages
    │       ├─→ Auth: OAuth delegated permissions
    │       ├─→ Filter spam/newsletters
    │       ├─→ Identify actionable items
    │       └─→ Extract reference items
    │
    ├─→ 📋 TASK SOURCES
    │   │
    │   └─→ Todoist (all active tasks)
    │       ├─→ API: Todoist API v1
    │       ├─→ Endpoint: /api/v1/tasks
    │       ├─→ Filter completed tasks
    │       └─→ Prioritize by due date
    │
    ├─→ 📄 DOCUMENT SOURCES
    │   │
    │   ├─→ Google Drive (last 7 days)
    │   │   ├─→ API: Google Drive API v3
    │   │   ├─→ Endpoint: /drive/v3/files
    │   │   ├─→ Auth: OAuth with Drive scope
    │   │   └─→ Track: Docs, Sheets, Slides
    │   │
    │   └─→ SharePoint/OneDrive (last 7 days)
    │       ├─→ API: Microsoft Graph v1.0
    │       ├─→ Endpoint: /me/drive/recent
    │       ├─→ Auth: OAuth delegated permissions
    │       └─→ Track: Word, Excel, PowerPoint, PDFs
    │
    ├─→ Deduplicate across all sources
    │
    ├─→ Auto-create Todoist tasks (actionable emails)
    ├─→ Auto-create Amplenote notes (reference emails)
    ├─→ Flag potentially missed items
    │
    └─→ Generate Holistic Kanban board in Amplenote
        ├─→ 🔥 Today (urgent + due today)
        ├─→ 📅 Tomorrow (due tomorrow)
        ├─→ 📆 This Week (due within 7 days)
        ├─→ 📦 Backlog (no deadline)
        ├─→ 📄 Documents in Progress (Google Drive + SharePoint)
        └─→ 📧 Email Summary (Gmail + Outlook counts)
```

---

## 📊 Visual: My Reading Order

```
┌─────────────────────────────────────────────────────────────┐
│                    USER REQUEST                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Root README.md │ ◄─── ALWAYS START HERE
                    └─────────────────┘
                              │
                ┌─────────────┼─────────────┐
                │                           │
                ▼                           ▼
    ┌──────────────────────┐    ┌──────────────────────┐
    │ Master Guides Index  │    │  ROUTING_RULES.md    │
    │ (README.md)          │    │  (if about routing)  │
    └──────────────────────┘    └──────────────────────┘
                │
                ▼
    ┌──────────────────────┐
    │ Specific Master      │
    │ Guide for topic      │
    └──────────────────────┘
                │
                ▼
    ┌──────────────────────┐
    │ Supporting Docs:     │
    │ • environments.json  │
    │ • KeePass database   │
    │ • Filing guides      │
    │ • Scripts folder     │
    └──────────────────────┘
```

---

## 🎯 Example: "Process New" Request (Holistic Daily Planning)

**User says:** "process new"

```
Step 1: Read Root README.md
    ↓
Found: "Process New" section
    ↓
Shows workflow:
    1. Daily Planning (python daily_planner.py)
    2. Process Downloads (file organization)
    ↓
Step 2: Read MASTER_GUIDE_Daily_Planning.md
    ↓
Found: Holistic daily planning workflow
    ↓
Step 3: Collect Data from ALL Sources (Work + Personal)
    ↓
    📧 PERSONAL EMAIL
    ├─→ Gmail API (last 2 weeks)
    │   ├─→ Filter spam/shipping
    │   └─→ Extract actionable items
    ↓
    📧 WORK EMAIL
    ├─→ Outlook via Microsoft Graph (last 2 weeks)
    │   ├─→ Endpoint: /me/messages
    │   ├─→ Filter spam/newsletters
    │   └─→ Extract actionable items
    ↓
    📋 TASKS
    ├─→ Todoist API v1 (all active tasks)
    │   └─→ Endpoint: /api/v1/tasks
    ↓
    📄 PERSONAL DOCUMENTS
    ├─→ Google Drive API (last 7 days)
    │   └─→ Recently modified files
    ↓
    📄 WORK DOCUMENTS
    ├─→ SharePoint via Microsoft Graph (last 7 days)
    │   ├─→ Endpoint: /me/drive/recent
    │   └─→ Recently accessed files
    ↓
Step 4: Smart Processing
    • Deduplicate across all sources
    • Extract deadlines from emails
    • Categorize by timeframe (Today/Tomorrow/Week/Backlog)
    • Track document activity
    ↓
Step 5: Create ONE Unified Amplenote Daily Plan
    ↓
    📝 Daily Plan - Sunday, February 22, 2026
    ├─→ 🔥 Today (personal + work tasks)
    ├─→ 📅 Tomorrow
    ├─→ 📆 This Week
    ├─→ 📦 Backlog
    ├─→ 📄 Documents in Progress
    │   ├─→ Google Drive files
    │   └─→ SharePoint files
    └─→ 📧 Email Summary
        ├─→ Gmail: X actionable items
        └─→ Outlook: Y actionable items
    ↓
Step 6: Execute Commands
    • python daily_planner.py (collects all data)
    • node sync_plan_to_amplenote.js (creates unified board)
    ↓
Result: ONE Kanban board with complete personal + work context
```

**Key Point:** All sources (Gmail, Outlook, Todoist, Google Drive, SharePoint) are scanned and combined into a **single holistic daily plan** in Amplenote. No separate work/personal boards - everything in one view.

---

## 🎯 Example: "Get Gmail Credentials" Request

**User says:** "I need Gmail credentials"

```
Step 1: Read Root README.md
    ↓
Found: Credentials Management section
    ↓
Shows lookup order:
    1. Check KeePass first
    2. Check environments.json
    3. Check .env file
    ↓
Step 2: Read MASTER_GUIDE_Environments_and_Credentials.md
    ↓
Found: Credential lookup workflow
    • KeePass location: G:\My Drive\03_Areas\Keys\keys pass.kdbx
    • environments.json location
    ↓
Step 3: Check environments.json
    ↓
Found: Gmail credentials in environments.json
    • OAuth client ID
    • OAuth client secret
    • Token location
    ↓
Step 4: Return credentials
    • Don't say "I don't have credentials"
    • Reference the actual location
```

---

## 🎯 Example: "Where Do Tasks Go?" Request

**User says:** "where should tasks go?"

```
Step 1: Read Root README.md
    ↓
Found: Routing Rules section
    ↓
Shows: Tasks → Todoist (permanent storage)
    ↓
Step 2: Read ROUTING_RULES.md
    ↓
Found: Complete routing guide
    • Tasks → Todoist
    • Notes → Amplenote
    • Events → Google Calendar
    ↓
Step 3: Read MASTER_GUIDE_Daily_Planning.md
    ↓
Found: "CRITICAL: Todoist vs Amplenote" section
    • Todoist = permanent task storage
    • Amplenote = temporary daily view + reference notes
    ↓
Step 4: Answer with confidence
    • Tasks go to Todoist
    • Amplenote is for daily Kanban view only
```

---

## 📁 Key Files I Always Check

### Tier 1: Always Read First
1. **`G:\My Drive\README.md`** - Root starting point
2. **`G:\My Drive\06_Master_Guides\README.md`** - Master guides index

### Tier 2: Read Based on Request Type
3. **`ROUTING_RULES.md`** - Where things go (Todoist/Amplenote/Calendar)
4. **`MASTER_GUIDE_Daily_Planning.md`** - Daily workflow
5. **`MASTER_GUIDE_Environments_and_Credentials.md`** - Credential lookup
6. **`MASTER_GUIDE_KeePass_Integration.md`** - KeePass access

### Tier 3: Supporting Files
7. **`environments.json`** - API credentials
8. **`keys pass.kdbx`** - KeePass database (via script)
9. **`COMPLETE_FILING_GUIDE.md`** - File organization rules

---

## 🔄 How I Continue Previous Work

### Scenario: User Returns After Break

```
User: "continue where we left off"
    ↓
Step 1: Check Root README.md
    • See what processes exist
    • See recent additions
 ## 📖 Reading Order for Common Tasks

### "Process new" or "I need to process my emails"

**Goal:** Intelligently scan Gmail + Outlook for actionable items, auto-create tasks/notes, generate Kanban board

**Reading Order:**
1. **Start**: Root README.md - "Process New" quick start section
2. **Workflow**: [05_MASTER_GUIDE_Daily_Planning.md](05_MASTER_GUIDE_Daily_Planning.md) - Email intelligence system
3. **Routing**: [02_MASTER_GUIDE_ROUTING_RULES.md](02_MASTER_GUIDE_ROUTING_RULES.md) - Email → Task/Note routing logic
4. **Credentials**: [MASTER_GUIDE_Environments_and_Credentials.md](MASTER_GUIDE_Environments_and_Credentials.md) - Gmail + Outlook OAuth

**What CASCADE Should Do:**
1. Run `email_intelligence.py` to scan Gmail + Outlook (or current `daily_planner.py` until new script exists)
2. Auto-create Todoist tasks for actionable emails
3. Auto-create Amplenote notes for reference emails
4. Flag potentially missed items
5. Generate Kanban board with `sync_plan_to_amplenote.js`
6. Report summary: tasks created, notes created, missed items

**Key Principles:**
- **Filter aggressively**: Skip spam, newsletters, automated alerts
- **Detect deadlines**: Parse natural language ("by Friday", "end of week")
- **Auto-create tasks**: Don't just list emails, create actionable Todoist tasks
- **Flag missing items**: Identify emails user may have overlooked
- **Dual sources**: Process both Gmail (personal) and Outlook (work)

### "I need to process my emails" (Legacy - same as above)

    ↓
Step 2: Check Master Guides Index
    • See recent additions: "KeePass Integration (Feb 2026)"
    • See total guides: 13
    ↓
Step 3: Review recent guides
    • MASTER_GUIDE_Daily_Planning.md
    • MASTER_GUIDE_Email_Processing.md
    • MASTER_GUIDE_KeePass_Integration.md
    ↓
Step 4: Understand current state
    • Daily planning system exists
    • Email processing routes to Todoist
    • KeePass integration documented
    • Routing rules clarified
    ↓
Step 5: Ask user what they want to do next
    • Or suggest next logical step
```

---

## ✅ Checklist: Before Answering Any Request

- [ ] Read Root README.md first
- [ ] Check Master Guides Index
- [ ] Identify relevant master guide(s)
- [ ] Read specific master guide
- [ ] Check credential sources (KeePass, environments.json)
- [ ] Check routing rules if about tasks/notes/events
- [ ] Verify file locations exist
- [ ] Follow documented workflow exactly
- [ ] Never say "I don't have X" without checking all sources first

---

## 🎓 Key Principles

### 1. Documentation is Truth
- If it's in a master guide, that's the correct way
- Don't invent new workflows
- Follow documented processes

### 2. Check Before Creating
- Check KeePass before saying "no credential"
- Check environments.json before creating new config
- Check existing guides before creating new ones

### 3. Root README is Starting Point
- Always start with Root README.md
- It shows the big picture
- It links to everything else

### 4. Master Guides are Detailed Instructions
- Root README = overview
- Master Guides = detailed how-to
- Supporting docs = specific data

### 5. Routing Rules Matter
- Tasks → Todoist
- Notes → Amplenote
- Events → Calendar
- Always check ROUTING_RULES.md

---

## 📊 Summary Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    MY WORKFLOW                               │
└─────────────────────────────────────────────────────────────┘

USER REQUEST
    ↓
Root README.md ──────────→ Big picture, workflows, routing
    ↓
Master Guides Index ─────→ Find relevant guide
    ↓
Specific Master Guide ───→ Detailed instructions
    ↓
Supporting Documents ────→ Credentials, data, rules
    ↓
EXECUTE DOCUMENTED WORKFLOW
    ↓
NEVER INVENT, ALWAYS FOLLOW DOCUMENTATION
```

---

## 🎯 The Golden Rule

**"If it's documented, follow it. If it's not documented, document it first."**

---

**End of Workflow Guide**

This is how I always find context and continue work. The documentation is my source of truth.
