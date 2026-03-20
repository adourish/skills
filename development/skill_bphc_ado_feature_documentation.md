# BPHC ADO Feature Documentation Workflow

## Quick Reference

**Use when:** Creating new ADO Features, User Stories, Tech Stories, or Tasks for the BPHC-GAM2010 project — including feature markdown docs, bidirectional linking, and PR creation
**Don't use when:** Simple one-off ADO task updates (use the ADO web UI); non-BPHC projects
**Trigger phrases:** "create a feature", "add ado feature", "feature doc", "create stories", "create tasks", "bidirectional link", "link ado to doc", "create PR for work items", "new feature for bphc"
**Time:** 15–30 min per feature (doc + ADO items + bidirectional links)
**Repo:** `https://ehbads.hrsa.gov/ads/EHBs/EHBs/_git/BPHC-GAM2010`

---

## ADO Hierarchy

```
ADO Organization: https://ehbads.hrsa.gov/ads/EHBs/EHBs
Project: EHBs

Epic (top level — do not create new epics without approval)
  └── Feature  ← one per capability/product area
        ├── User Story  ← business-facing "As a... I want... So that..."
        │     └── Task  ← concrete work items (DEV/QA/BA, hours)
        └── Tech Story  ← also created as "User Story" type in ADO; engineering-focused
              └── Task
```

---

## Key ADO IDs

### Platform Epics

| Epic | ID | URL |
| --- | --- | --- |
| Salesforce Features (platform) | #427499 | `_workitems/edit/427499` |
| PRM Product Features | #428772 | `_workitems/edit/428772` |
| COM Product Features | #428773 | `_workitems/edit/428773` |
| PWPM Product Features | #428774 | `_workitems/edit/428774` |
| LGP Product Features | #428775 | `_workitems/edit/428775` |

### Sprint Iterations

| Sprint | Path |
| --- | --- |
| Sprint 7 (Config/Setup) | `EHBs\DME BHCMIS Purple\FY25 System Mod Sprint 7` |
| Sprint 8 (Phase 1 / Core) | `EHBs\DME BHCMIS Purple\FY25 System Mod Sprint 8` |
| Sprint 9 (Phase 2 / Testing) | `EHBs\DME BHCMIS Purple\FY25 System Mod Sprint 9` |
| Sprint 10 (Phase 3 / Release) | `EHBs\DME BHCMIS Purple\FY25 System Mod Sprint 10` |

---

## CRITICAL: Always Use the Correct Area Path

> **RULE:** Every ADO work item created for BPHC-GAM2010 MUST use `"System.AreaPath": "EHBs\\BHCMISPRS"`.
> Using the wrong area path (e.g., `"EHBs"` alone) causes items to be owned by the wrong team,
> which prevents backlog reordering and sprint assignment. Always set this field — even on updates/patches.

```
CORRECT:   "EHBs\\BHCMISPRS"
WRONG:     "EHBs"    ← items cannot be reordered; owned by wrong team
```

---

## ADO REST API — Core Pattern

### Authentication & Constants

```python
import json, urllib.request, urllib.parse, base64, ssl, sys, time
sys.stdout.reconfigure(encoding='utf-8')

PAT      = "<PAT from G:/My Drive/03_Areas/Keys/Environments/devops-hrsa-ado.json>"
auth     = base64.b64encode(f":{PAT}".encode()).decode()
HDR_GET  = {"Authorization": f"Basic {auth}", "Content-Type": "application/json"}
HDR_PTCH = {"Authorization": f"Basic {auth}", "Content-Type": "application/json-patch+json"}
BASE_URL = "https://ehbads.hrsa.gov/ads/EHBs/EHBs/_apis/wit"
REPO_URL = "https://ehbads.hrsa.gov/ads/EHBs/EHBs/_git/BPHC-GAM2010"
AREA     = "EHBs\\BHCMISPRS"   # ← ALWAYS use this — never "EHBs" alone
VENDOR   = "DME"
ctx      = ssl._create_unverified_context()
```

> **PAT source:** Read from `G:/My Drive/03_Areas/Keys/Environments/devops-hrsa-ado.json`
> Never hardcode the PAT into committed scripts — use a local-only credentials file.

### create_item() Helper

```python
def create_item(item_type, fields, parent_id=None):
    """Create any ADO work item type. item_type examples: 'Feature', 'User Story', 'Task'"""
    ops = [{"op": "add", "path": f"/fields/{k}", "value": v} for k, v in fields.items()]
    if parent_id:
        ops.append({
            "op": "add", "path": "/relations/-",
            "value": {
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": f"{BASE_URL}/workItems/{parent_id}",
                "attributes": {"comment": ""}
            }
        })
    # IMPORTANT: item_type must be URL-encoded ("User Story" → "User%20Story")
    url = f"{BASE_URL}/workitems/${urllib.parse.quote(item_type)}?api-version=6.0"
    req = urllib.request.Request(url, data=json.dumps(ops).encode(), headers=HDR_PTCH, method="POST")
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        result = json.loads(r.read())
    print(f"  #{result['id']} [{item_type}] {fields.get('System.Title','')[:75]}")
    time.sleep(0.4)   # rate limit
    return result
```

### Required Fields by Work Item Type

#### Feature

```python
{
    "System.Title": "Feature title",
    "System.Description": "<p>HTML description</p>",
    "System.AreaPath": AREA,
    "System.IterationPath": ITER,                               # sprint path
    "Microsoft.VSTS.Common.Priority": 2,
    "Microsoft.VSTS.Scheduling.TargetDate": "2026-06-25T00:00:00Z",
    "HRSA.Vendor.Type": VENDOR,
    "HRSA.Bureau": "BPHC",
    "HRSA.JIRA.Enhancement": "No",                             # REQUIRED — omitting causes 400
}
```

#### User Story / Tech Story (same ADO type = "User Story")

```python
{
    "System.Title": "US: As a ...",                            # or "TS: Implement ..."
    "System.Description": "<p>HTML description</p>",
    "Microsoft.VSTS.Common.AcceptanceCriteria": "<ul><li>AC text</li></ul>",
    "System.AreaPath": AREA,
    "System.IterationPath": ITER,
    "Microsoft.VSTS.Common.Priority": 2,
    "HRSA.Vendor.Type": VENDOR,
    "HRSA.Bureau": "BPHC",
    "HRSA.JIRA.Enhancement": "No",
}
```

#### Task

```python
{
    "System.Title": "T: Task description",
    "System.AreaPath": AREA,
    "System.IterationPath": ITER,
    "Microsoft.VSTS.Scheduling.OriginalEstimate": float(hours),
    "Microsoft.VSTS.Scheduling.RemainingWork": float(hours),
    "HRSA.Vendor.Type": VENDOR,
    "HRSA.JIRA.Enhancement": "No",
}
```

> Note: Tasks do NOT need `HRSA.Bureau` but it won't fail if included.

---

## Feature Markdown Document Format

### File Location

```
docs/Features/{Domain}/Feature_{Name}_v1.0.md
```

Common domains: `Configuration`, `DataMigration`, `Security`, `ProductConfiguration`, `AssignmentandStatus`, `SecureExternalUpload`

### Standard Header Block

```markdown
# Feature Title

**Version:** 1.0
**Last Updated:** YYYY-MM-DD
**Status:** 📋 Planned | 🔄 In Progress | ✅ Deployed | 🔍 Design & Discovery
**Products:** GAM; PRS; LGP; COM; PWPM
**Feature Type:** [Category]
**Target Release:** June 25, 2026
**ADO Feature:** [ADO #NNNNN](https://ehbads.hrsa.gov/ads/EHBs/EHBs/_workitems/edit/NNNNN)
**ADO User Story:** [#NNNNN](https://ehbads.hrsa.gov/ads/EHBs/EHBs/_workitems/edit/NNNNN)
**ADO Tech Story:** [#NNNNN](https://ehbads.hrsa.gov/ads/EHBs/EHBs/_workitems/edit/NNNNN)
**Parent Epic:** [ADO #NNNNN](https://ehbads.hrsa.gov/ads/EHBs/EHBs/_workitems/edit/NNNNN)
**In-Scope (MVP):** Yes | No — [reason]
**Part of Original ROM (POOR):** Yes | No
**Section 508 Compliant:** Yes (design requirement)
```

### Standard Sections

1. Executive Summary / Overview (purpose, business value, stakeholders)
2. Business Design / Configuration Scope (context, system applicability)
3. Feature Catalog / User Stories (table of capabilities OR user story specs)
4. Technical Design / Source→Target Mapping (architecture, objects, fields)
5. Implementation Plan (phased tasks with owner + hour estimates)
6. Implementation Status (table: capability → status → notes)
7. Known Issues (ID, description, severity, status)
8. Related Documents / Dependencies

---

## Bidirectional Linking Pattern

### Direction 1: ADO → Markdown (patch ADO description)

```python
import re

def add_doc_link_to_ado(item_id, doc_path):
    """Add/replace clickable Feature Doc link in ADO work item description."""
    doc_url = f"{REPO_URL}?path=/{doc_path}"
    link_html = (
        f'<p><strong>Feature Doc:</strong> '
        f'<a href="{doc_url}" target="_blank">{doc_path}</a></p>'
    )
    # GET current description
    req = urllib.request.Request(f"{BASE_URL}/workItems/{item_id}?api-version=6.0", headers=HDR_GET)
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        current = json.loads(r.read())["fields"].get("System.Description", "") or ""

    # Replace existing doc link (if re-running), then append
    cleaned = re.sub(r'<p><strong>Feature Doc:</strong>.*?</p>', '', current, flags=re.DOTALL)
    new_desc = cleaned.rstrip() + "\n" + link_html

    ops = [{"op": "replace", "path": "/fields/System.Description", "value": new_desc}]
    req = urllib.request.Request(
        f"{BASE_URL}/workItems/{item_id}?api-version=6.0",
        data=json.dumps(ops).encode(), headers=HDR_PTCH, method="PATCH"
    )
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        json.loads(r.read())
```

### Direction 2: Markdown → ADO (replace TBD placeholders)

```python
def update_markdown_with_ids(filepath, feat_id, us1_id, us2_id, ts1_id):
    """Replace #TBD placeholders in feature markdown with real ADO IDs."""
    ado_base = "https://ehbads.hrsa.gov/ads/EHBs/EHBs/_workitems/edit"
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(
        r'\*\*ADO Feature:\*\* \[ADO #TBD\]\(https://ehbads\.hrsa\.gov/ads/EHBs/EHBs/_workitems/\)',
        f'**ADO Feature:** [ADO #{feat_id}]({ado_base}/{feat_id})',
        content
    )
    content = content.replace(
        "**ADO User Story:** TBD",
        f"**ADO User Stories:** [#{us1_id}]({ado_base}/{us1_id}) · [#{us2_id}]({ado_base}/{us2_id})",
        1
    )
    content = content.replace(
        "**ADO Tech Story:** TBD",
        f"**ADO Tech Story:** [#{ts1_id}]({ado_base}/{ts1_id})",
        1
    )
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
```

---

## Full Workflow — Feature + Doc + Bidirectional Links

```
1. Write feature markdown doc
   → docs/Features/{Domain}/Feature_{Name}_v1.0.md
   → Use #TBD placeholders for ADO IDs

2. Run ADO creation script
   → Creates: Feature → US1 + US2 + TS1 → Tasks
   → Returns IDs; saves to docs/Planning/ado_{name}_ids.json

3. Patch ADO descriptions with doc links (Direction 1)
   → add_doc_link_to_ado(feat_id, doc_path)

4. Update markdown with ADO IDs (Direction 2)
   → update_markdown_with_ids(filepath, feat_id, us1_id, us2_id, ts1_id)

5. Commit + push + PR
   → git checkout -b dev/DME/feature/sf-{feature-name}
   → git add docs/Features/{Domain}/  scripts/  docs/Planning/
   → git commit -m "feat: add {name} feature doc and ADO work items"
   → git push origin dev/DME/feature/sf-{feature-name}
   → Create PR: dev/DME/feature/sf-{feature-name} → dev/DME/feature/sf-develop via ADO REST API
```

---

## PR Creation via ADO REST API

```python
def create_pr(repo_id, source_branch, target_branch, title, description, work_item_ids):
    """Create a PR in ADO and link work items."""
    pr_body = {
        "title": title,
        "description": description,
        "sourceRefName": f"refs/heads/{source_branch}",
        "targetRefName": f"refs/heads/{target_branch}",
        "workItemRefs": [
            {"id": str(wid), "url": f"{BASE_URL}/workItems/{wid}"}
            for wid in work_item_ids
        ],
        "isDraft": False,
    }
    url = f"https://ehbads.hrsa.gov/ads/EHBs/EHBs/_apis/git/repositories/{repo_id}/pullrequests?api-version=6.0"
    req = urllib.request.Request(url, data=json.dumps(pr_body).encode(), headers=HDR_GET, method="POST")
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        pr = json.loads(r.read())
    return pr["pullRequestId"]

# Complete (merge) a PR
def complete_pr(repo_id, pr_id, last_commit_id):
    body = {
        "status": "completed",
        "lastMergeSourceCommit": {"commitId": last_commit_id},
        "completionOptions": {
            "mergeStrategy": "noFastForward",
            "deleteSourceBranch": False,
            "bypassPolicy": True,
            "bypassReason": "Doc-only changes — no Salesforce metadata",
            "transitionWorkItems": True,
        }
    }
    url = f"https://ehbads.hrsa.gov/ads/EHBs/EHBs/_apis/git/repositories/{repo_id}/pullrequests/{pr_id}?api-version=6.0"
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=HDR_PTCH, method="PATCH")
    with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
        return json.loads(r.read())

# BPHC repo ID (constant)
REPO_ID = "9b62fff5-6c9a-4fab-82d9-8d1ed0a1d8e3"
```

> **Merge strategies:** Use `"noFastForward"` for doc PRs; use `"squash"` for feature code PRs.
> `bypassPolicy: True` is appropriate for doc-only changes with no Salesforce metadata.

---

## Existing Reference Scripts

| Script | Creates |
| --- | --- |
| `scripts/create_product_config_testing_features_ado.py` | 3 features per product (Config/Testing/Release) × 4 products |
| `scripts/create_bundle_scheduling_features_ado.py` | BCE/DSE/MCY Configuration Hub enhancement features |
| `scripts/create_dm11_feature_ado.py` | DM11 Assignment Management (deferred wave pattern) |
| `scripts/create_dm10_feature_ado.py` | DM10 Programs/Activity Codes (migration wave pattern) |
| `scripts/create_scanning_feature_ado.py` | Scanning security shared feature pattern |

**Use `create_product_config_testing_features_ado.py` as the primary template** — it demonstrates the full pattern: resume support, story→task ID mapping, all required fields, and batch bidirectional linking.

---

## Known ADO Field Gotchas

| Issue | Cause | Fix |
| --- | --- | --- |
| HTTP 400 on User Story | Space in type name not URL-encoded | `urllib.parse.quote("User Story")` |
| HTTP 400 "field not recognized" | Wrong field name (e.g., `Custom.VendorType`) | Correct name: `HRSA.Vendor.Type` |
| HTTP 400 "required field missing" | `HRSA.JIRA.Enhancement` omitted | Add `"HRSA.JIRA.Enhancement": "No"` to all items |
| Double `?` in URL | Manual URL construction error | Use `sep = "&" if "?" in path else "?"` |
| Unicode encoding error on Windows | `sys.stdout` default encoding | Add `sys.stdout.reconfigure(encoding='utf-8')` |
| Feature not showing under Epic | `Hierarchy-Reverse` relation wrong URL | Use `{BASE_URL}/workItems/{parent_id}` (no trailing slash) |
| Items can't be reordered / "owned by another team" | `System.AreaPath` set to `"EHBs"` instead of `"EHBs\\BHCMISPRS"` | Always use `AREA = "EHBs\\BHCMISPRS"` for all BPHC-GAM2010 items |

---

## Doc Naming Conventions

| Type | Pattern | Example |
| --- | --- | --- |
| Feature doc | `Feature_{Name}_v1.0.md` | `Feature_BundleConfigurationEnhancements_v1.0.md` |
| Product config | `Feature_{PRODUCT}_{Type}_v1.0.md` | `Feature_PRM_PlatformConfiguration_v1.0.md` |
| Data migration | `Feature_DataMigration{N}_{Topic}_v1.0.md` | `Feature_DataMigration10_ProgramsActivityCodesCans_v1.0.md` |
| User story | `UserStory_{Name}_v1.0.md` | `UserStory_ReviewerListPages_v1.0.md` |
| Tech story | `TechStory_{Name}_v1.0.md` | `TechStory_ReviewerListPages_v1.0.md` |
| ADO IDs output | `ado_{slug}_ids.json` | `ado_product_config_testing_ids.json` |
| Reference CSV | `{feature_slug}_reference.csv` | `dm10_programs_reference.csv` |

---

## Salesforce Object Prefixes (for doc accuracy)

| Prefix | Domain | Example |
| --- | --- | --- |
| `bphc_` | BPHC grant management | `bphc_Award__c` |
| `cfgHub_` | Configuration Hub | `cfgHub_BundleDefinition__c` |
| `cmn_` | Common/shared | `cmn_Program__c`, `cmn_ActivityCode__c`, `cmn_Tenant__c` |
| `ai_` | AI project components | `ai_Prompt__c` |

**Key shared objects used in feature docs:**
- Programs: `cmn_Program__c` (fields: `Abbreviation__c`, `Program_Code__c`, `Program_Group_Code__c`, `Program_Status__c`, `CFDA_Number__c`, `Service_Type_Code__c`)
- Activity Codes: `cmn_ActivityCode__c` (external ID: `Activity_Code__c`; `Source__c` picklist includes "HRSA EHBs")
- Program-Activity Junction: `cmn_ProgramActivityCode__c`
- Tenant: `cmn_Tenant__c`
- Bundles: `cfgHub_BundleDefinition__c`, `cfgHub_BundleItem__c`
- Cohorts: `cfgHub_Cohort__c`, `cfgHub_CohortMember__c`
- Schedules: `cfgHub_ScheduleDefinition__c`, `cfgHub_FundingCycle__c`
- Audit log (new): `cfgHub_BundleAuditLog__c`

---

## Program Reference (from DEV5 Tenant Configuration)

| Program | Abbrev | Code | Group | CFDA | Activity Codes |
| --- | --- | --- | --- | --- | --- |
| American Rescue Plan Capital | ARP-C | ARP-CAPITAL | EMERGENCY-FUNDING | — | ARP-CAPITAL |
| Capital Development | CAP | C8A | CAPITAL-INFRASTRUCTURE | — | C12,C13,C14,C80,C81,C8A,C8C,C8D,C8E |
| Health Center Controlled Network | HCCN | U86 | TECHNICAL-ASSISTANCE | — | H2Q,H80,H8A,H8C,H8D,H8F,H8G,HQC,U86 |
| Health Center Program | HCP | H80 | HEALTH-CENTER-PROGRAM | 93.224 | H19,H1B,H20,H27,H66,H80,H85,H8G,H8I,H8L,H8M,P04,PCHP,SB1 |
| National Training & TA Partners | NTTAP | U30 | TECHNICAL-ASSISTANCE | — | U30,U3F |
| Native Hawaiian Health Care | NHHC | H1C | NATIONAL-GRANTS | — | H1C |
| New Access Point | NAP | NAP | HEALTH-CENTER-PROGRAM | 93.224 | NAP |
| Primary Care Association | PCA | PCA | NATIONAL-GRANTS | — | PCA |
| Service Area Competition | SAC | SAC | HEALTH-CENTER-PROGRAM | 93.224 | SAC |
| State and Regional PCAs | PCA | U58 | TECHNICAL-ASSISTANCE | — | U58,U5B,U5F |

Machine-readable: `docs/Features/DataMigration/dm10_programs_reference.csv`

---

## Related Skills

- [skill_bphc_gitflow.md](skill_bphc_gitflow.md) — Branch naming, PR creation, GitFlow workflow
- [skill_bphc_context_lifecycle_pattern.md](skill_bphc_context_lifecycle_pattern.md) — Context Instance, lifecycle architecture
- [skill_bphc_external_id_architecture.md](skill_bphc_external_id_architecture.md) — External IDs for data migration

---

**Last Updated:** 2026-03-12
**Category:** BPHC Projects
**Repo:** BPHC-GAM2010
