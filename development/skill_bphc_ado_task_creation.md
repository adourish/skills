# BPHC ADO Task Creation via REST API

## Quick Reference

**Use when:** Creating ADO Tasks (or User Stories/Features) for the BPHC-GAM2010 project using the REST API — batch task creation, sprint assignment, time tracking, parent linking
**Don't use when:** One-off ADO web UI edits; non-BPHC projects
**Trigger phrases:** "create ado tasks", "add tasks to sprint", "create work items", "ado task for", "track hours in ado"
**Time:** ~1 min per task (API-based, no browser automation)
**Repo:** `https://ehbads.hrsa.gov/ads/EHBs/EHBs/_git/BPHC-GAM2010`

---

## ADO Constants

```
Organization URL:  https://ehbads.hrsa.gov/ads/EHBs
Project:           EHBs
API Version:       6.0
Area Path:         EHBs\BHCMISPRS        ← ALWAYS use this
Team:              DME BHCMIS Purple
Team ID:           4b88302c-3871-41fb-92ce-4889f00a06ea
```

### Credentials

**Source:** `G:\My Drive\03_Areas\Keys\Environments\devops-hrsa-ado.json`

Read the PAT from that file at runtime. **Never hardcode PATs into committed files.**

### Required Fields (all work item types)

| Field | Value |
|-------|-------|
| `HRSA.Vendor.Type` | `DME` |
| `HRSA.Bureau` | `BPHC` |
| `HRSA.JIRA.Enhancement` | `No` |
| `Microsoft.VSTS.Scheduling.TargetDate` | `2025-09-30T00:00:00Z` |
| `System.AreaPath` | `EHBs\\BHCMISPRS` |

### Sprint Iterations

| Sprint | Path | Dates |
|--------|------|-------|
| Sprint 7 | `EHBs\DME BHCMIS Purple\FY25 System Mod Sprint 7` | 2026-03-11 → 2026-03-24 |
| Sprint 8 | `EHBs\DME BHCMIS Purple\FY25 System Mod Sprint 8` | 2026-03-25 → 2026-04-07 |
| Sprint 9 | `EHBs\DME BHCMIS Purple\FY25 System Mod Sprint 9` | 2026-04-08 → 2026-04-21 |
| Sprint 10 | `EHBs\DME BHCMIS Purple\FY25 System Mod Sprint 10` | 2026-04-22 → 2026-05-05 |

To get the **current sprint** dynamically:

```bash
curl -s -u ":$PAT" \
  "$BASE/EHBs/4b88302c-3871-41fb-92ce-4889f00a06ea/_apis/work/teamsettings/iterations?\$timeframe=current&api-version=6.0"
```

### Key People

| Name | Identity | uniqueName |
|------|----------|------------|
| Dourish, Anthony | `7a741f5c-35f1-4563-abb8-c19c5c38d5ea` | `HRSA\ADourish` |

### Platform Epics (for parent linking)

| Epic | ID |
|------|----|
| Salesforce Features (platform) | #427499 |
| PRM Product Features | #428772 |
| COM Product Features | #428773 |
| PWPM Product Features | #428774 |
| LGP Product Features | #428775 |

---

## API Patterns

### Method: PATCH (not POST)

ADO Server uses `PATCH` for work item creation (different from ADO Services which uses `POST`).

```
PATCH {base}/EHBs/_apis/wit/workitems/$Task?api-version=6.0
Content-Type: application/json-patch+json
```

### State Transition

Tasks cannot be created directly in `Active` state. Create as `New` (default), then update:

```
Step 1: PATCH  .../$Task?api-version=6.0           → creates in "New" state
Step 2: PATCH  .../workitems/{id}?api-version=6.0  → set state to "Active"
```

Valid states: `New` → `Active` → `Closed` | `Removed`

---

## Python Helper Script

Use this pattern for batch task creation. Handles all the ADO quirks (PATCH method, state transition, parent linking, SSL context).

```python
import json, urllib.request, urllib.parse, base64, ssl, sys, time
sys.stdout.reconfigure(encoding='utf-8')

# ── Credentials (read from file — never hardcode) ──────────────────────────
creds = json.load(open(r"G:\My Drive\03_Areas\Keys\Environments\devops-hrsa-ado.json"))
PAT = creds["credentials"]["pat"]

auth     = base64.b64encode(f":{PAT}".encode()).decode()
HDR      = {"Authorization": f"Basic {auth}", "Content-Type": "application/json-patch+json"}
HDR_GET  = {"Authorization": f"Basic {auth}", "Content-Type": "application/json"}
BASE     = "https://ehbads.hrsa.gov/ads/EHBs/EHBs/_apis/wit"
AREA     = "EHBs\\BHCMISPRS"
ctx      = ssl._create_unverified_context()


def create_task(title, description, assigned_to, iteration_path,
                remaining_hours, completed_hours, original_estimate,
                parent_id=None, activate=True):
    """Create an ADO Task with time tracking and optional parent link.

    Args:
        title: Task title
        description: HTML or plain text description
        assigned_to: Display name (e.g. "Dourish, Anthony (HRSA) C")
        iteration_path: Sprint path (e.g. "EHBs\\DME BHCMIS Purple\\FY25 System Mod Sprint 8")
        remaining_hours: Hours remaining
        completed_hours: Hours already worked
        original_estimate: Total estimated hours
        parent_id: Optional parent work item ID (User Story or Feature)
        activate: If True, transitions task from New → Active

    Returns:
        dict with 'id', 'url', 'title'
    """
    ops = [
        {"op": "add", "path": "/fields/System.Title", "value": title},
        {"op": "add", "path": "/fields/System.AssignedTo", "value": assigned_to},
        {"op": "add", "path": "/fields/System.IterationPath", "value": iteration_path},
        {"op": "add", "path": "/fields/System.AreaPath", "value": AREA},
        {"op": "add", "path": "/fields/System.Description", "value": description},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.RemainingWork", "value": remaining_hours},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.CompletedWork", "value": completed_hours},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.OriginalEstimate", "value": original_estimate},
        {"op": "add", "path": "/fields/Microsoft.VSTS.Scheduling.TargetDate", "value": "2025-09-30T00:00:00Z"},
        {"op": "add", "path": "/fields/HRSA.Vendor.Type", "value": "DME"},
        {"op": "add", "path": "/fields/HRSA.Bureau", "value": "BPHC"},
        {"op": "add", "path": "/fields/HRSA.JIRA.Enhancement", "value": "No"},
    ]

    # Add parent link if provided
    if parent_id:
        ops.append({
            "op": "add", "path": "/relations/-",
            "value": {
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": f"{BASE}/workItems/{parent_id}",
                "attributes": {"comment": ""}
            }
        })

    # Step 1: Create (lands in "New" state)
    url = f"{BASE}/workitems/$Task?api-version=6.0"
    req = urllib.request.Request(url, data=json.dumps(ops).encode(), headers=HDR, method="PATCH")
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        result = json.loads(r.read())

    wid = result["id"]
    time.sleep(0.3)

    # Step 2: Activate
    if activate:
        activate_ops = [{"op": "add", "path": "/fields/System.State", "value": "Active"}]
        activate_url = f"{BASE}/workitems/{wid}?api-version=6.0"
        req2 = urllib.request.Request(activate_url, data=json.dumps(activate_ops).encode(), headers=HDR, method="PATCH")
        with urllib.request.urlopen(req2, context=ctx, timeout=30) as r2:
            json.loads(r2.read())
        time.sleep(0.3)

    print(f"  #{wid} - {title}")
    return {"id": wid, "url": f"{BASE}/workItems/{wid}", "title": title}


def get_current_sprint():
    """Return the current sprint iteration path."""
    url = (f"https://ehbads.hrsa.gov/ads/EHBs/EHBs/"
           f"4b88302c-3871-41fb-92ce-4889f00a06ea/"
           f"_apis/work/teamsettings/iterations?$timeframe=current&api-version=6.0")
    req = urllib.request.Request(url, headers=HDR_GET)
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        data = json.loads(r.read())
    itr = data["value"][0]
    return itr["path"]


def update_task(task_id, fields_dict):
    """Update fields on an existing work item.

    Args:
        task_id: Work item ID
        fields_dict: Dict of field paths to values, e.g.:
            {"System.State": "Closed", "Microsoft.VSTS.Scheduling.RemainingWork": 0}
    """
    ops = [{"op": "add", "path": f"/fields/{k}", "value": v} for k, v in fields_dict.items()]
    url = f"{BASE}/workitems/{task_id}?api-version=6.0"
    req = urllib.request.Request(url, data=json.dumps(ops).encode(), headers=HDR, method="PATCH")
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        result = json.loads(r.read())
    print(f"  #{task_id} updated")
    return result


def close_task(task_id, completed_hours=None):
    """Close a task and optionally update completed hours."""
    fields = {"System.State": "Closed", "Microsoft.VSTS.Scheduling.RemainingWork": 0}
    if completed_hours is not None:
        fields["Microsoft.VSTS.Scheduling.CompletedWork"] = completed_hours
    return update_task(task_id, fields)
```

---

## Usage Examples

### Example 1: Create a batch of sprint tasks

```python
sprint = get_current_sprint()
assignee = "Dourish, Anthony (HRSA) C"

tasks = [
    ("Documents Integration - Review Compare, Upload",
     "F008 docs review/compare, upload modal, versioning", 2, 3, 5),
    ("Contributions Integration - Request, Provide, Withdraw",
     "Contribution service workflows, badge counts", 1.5, 2.5, 4),
    ("Communication Integration - Chatter Feed",
     "Chatter feed, Communication tab, CommunicationAPI", 1, 1.5, 2.5),
    ("External Comms Integration - Messaging, Unread Counts",
     "Ext comms LWC, message modal, unread badges", 1.5, 2, 3.5),
]

print(f"Creating tasks in {sprint}...")
for title, desc, remaining, completed, estimate in tasks:
    create_task(title, desc, assignee, sprint, remaining, completed, estimate)
```

### Example 2: Create task with parent link

```python
create_task(
    title="Implement cmn_DocumentCompareService",
    description="Apex service for document version comparison",
    assigned_to="Dourish, Anthony (HRSA) C",
    iteration_path=get_current_sprint(),
    remaining_hours=4,
    completed_hours=0,
    original_estimate=4,
    parent_id=427499  # Platform epic
)
```

### Example 3: Close completed tasks

```python
close_task(431482, completed_hours=5)
close_task(431483, completed_hours=4)
```

### Example 4: Update remaining hours

```python
update_task(431484, {
    "Microsoft.VSTS.Scheduling.RemainingWork": 0.5,
    "Microsoft.VSTS.Scheduling.CompletedWork": 2
})
```

---

## curl Examples (for quick one-offs)

### Get current sprint

```bash
PAT=$(python -c "import json; print(json.load(open(r'G:\\My Drive\\03_Areas\\Keys\\Environments\\devops-hrsa-ado.json'))['credentials']['pat'])")

curl -s -u ":$PAT" \
  "https://ehbads.hrsa.gov/ads/EHBs/EHBs/4b88302c-3871-41fb-92ce-4889f00a06ea/_apis/work/teamsettings/iterations?\$timeframe=current&api-version=6.0" \
  | python -c "import sys,json; d=json.loads(sys.stdin.read()); print(d['value'][0]['path'])"
```

### Create a single task (write JSON to temp file to avoid shell escaping)

```bash
cat > /tmp/ado-task.json << 'EOF'
[
  {"op":"add","path":"/fields/System.Title","value":"My task title"},
  {"op":"add","path":"/fields/System.AssignedTo","value":"Dourish, Anthony (HRSA) C"},
  {"op":"add","path":"/fields/System.IterationPath","value":"EHBs\\DME BHCMIS Purple\\FY25 System Mod Sprint 8"},
  {"op":"add","path":"/fields/System.AreaPath","value":"EHBs\\BHCMISPRS"},
  {"op":"add","path":"/fields/Microsoft.VSTS.Scheduling.RemainingWork","value":4},
  {"op":"add","path":"/fields/Microsoft.VSTS.Scheduling.OriginalEstimate","value":4},
  {"op":"add","path":"/fields/Microsoft.VSTS.Scheduling.TargetDate","value":"2025-09-30T00:00:00Z"},
  {"op":"add","path":"/fields/HRSA.Vendor.Type","value":"DME"},
  {"op":"add","path":"/fields/HRSA.Bureau","value":"BPHC"},
  {"op":"add","path":"/fields/HRSA.JIRA.Enhancement","value":"No"}
]
EOF

curl -s -X PATCH -u ":$PAT" \
  "https://ehbads.hrsa.gov/ads/EHBs/EHBs/_apis/wit/workitems/\$Task?api-version=6.0" \
  -H "Content-Type: application/json-patch+json" \
  -d @/tmp/ado-task.json
```

### Activate a task (transition New → Active)

```bash
curl -s -X PATCH -u ":$PAT" \
  "https://ehbads.hrsa.gov/ads/EHBs/EHBs/_apis/wit/workitems/431482?api-version=6.0" \
  -H "Content-Type: application/json-patch+json" \
  -d '[{"op":"add","path":"/fields/System.State","value":"Active"}]'
```

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `You must pass a valid patch document` | Using `POST` instead of `PATCH`, or shell mangling the JSON payload | Use `PATCH` method; write JSON to temp file or use Python |
| `State 'Active' is not valid` | Can't create directly in Active state | Create as New, then update to Active in second call |
| `Field 'Vendor Type' cannot be empty` | Missing `HRSA.Vendor.Type` | Always include `"HRSA.Vendor.Type": "DME"` |
| `Variable does not exist` on deploy | Org missing a field referenced in code | Include the field metadata in the deployment |
| Items not visible in sprint board | Wrong Area Path | Must use `EHBs\\BHCMISPRS`, not `EHBs` |
| 404 on API call | URL has double `EHBs/EHBs` where only one is needed | Org = `EHBs`, Project = `EHBs` → URL is `https://ehbads.hrsa.gov/ads/EHBs/EHBs/_apis/...` |

---

## Work Item Type Field Reference

### Task Fields

| Field | Path | Type | Required |
|-------|------|------|----------|
| Title | `System.Title` | string | Yes |
| Assigned To | `System.AssignedTo` | string (display name) | No |
| State | `System.State` | New/Active/Closed/Removed | Auto |
| Area Path | `System.AreaPath` | string | Yes |
| Iteration Path | `System.IterationPath` | string | Yes |
| Description | `System.Description` | HTML string | No |
| Original Estimate | `Microsoft.VSTS.Scheduling.OriginalEstimate` | float (hours) | No |
| Remaining Work | `Microsoft.VSTS.Scheduling.RemainingWork` | float (hours) | No |
| Completed Work | `Microsoft.VSTS.Scheduling.CompletedWork` | float (hours) | No |
| Target Date | `Microsoft.VSTS.Scheduling.TargetDate` | datetime | Yes* |
| Vendor Type | `HRSA.Vendor.Type` | DME | Yes |
| Bureau | `HRSA.Bureau` | BPHC | Yes* |
| JIRA Enhancement | `HRSA.JIRA.Enhancement` | No | Yes |
| Priority | `Microsoft.VSTS.Common.Priority` | 1-4 | No (defaults to 2) |

*Required by org policy — omitting may cause 400 errors.

### Parent Linking

```json
{
  "op": "add",
  "path": "/relations/-",
  "value": {
    "rel": "System.LinkTypes.Hierarchy-Reverse",
    "url": "https://ehbads.hrsa.gov/ads/EHBs/EHBs/_apis/wit/workItems/{parentId}",
    "attributes": {"comment": ""}
  }
}
```
