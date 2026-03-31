# Developer Complete Work — Definition of Done

## Quick Reference

**Use when:** Wrapping up a feature, bug fix, or enhancement — all code changes are deployed and working, and you need to complete documentation, tests, and commit/push
**Don't use when:** Mid-sprint work-in-progress; first draft of a feature doc (use `skill_bphc_ado_feature_documentation.md` instead)
**Trigger phrases:** "developer complete", "dev complete", "definition of done", "commit and push", "wrap up feature", "finish feature", "complete work", "done with feature", "mark complete", "ship it", "create a pr"
**Time:** 30–90 min depending on feature size and doc freshness
**Repo:** `https://ehbads.hrsa.gov/ads/EHBs/EHBs/_git/BPHC-GAM2010`

---

## Overview

This skill executes the full Definition of Done (DoD) checklist for BPHC-GAM2010. It ensures all touched feature documents are updated to reflect the designed/deployed state, handoff documents are created, tests are documented, and the work is committed and pushed.

**The DoD has four phases:**

```
Phase 1 — Inventory      Identify all files touched and docs affected
Phase 2 — Feature Docs   Update each affected feature doc to designed state
Phase 3 — Handoff        Create or update handoff document(s)
Phase 4 — Commit & Push  Stage, commit, and push (if on ADO network)
```

---

## Phase 1 — Inventory

Before touching any docs, build the full picture of what changed.

### 1.1 — Identify Touched Files

```bash
# All modified/new files since last commit
git status --short

# Diff summary vs main branch
git diff --stat dev/DME/feature/sf-develop...HEAD
```

Group them into:
- **Apex classes** (`force-app/main/default/classes/`)
- **LWC components** (`force-app/main/default/lwc/`)
- **Objects / metadata** (`force-app/main/default/objects/`, `flows/`, etc.)
- **Tests** (`force-app/main/default/classes/*Test.cls`, `Tests/e2e/`)
- **Docs already modified** (`docs/`)

### 1.2 — Map Files → Feature Docs

For each Apex class or LWC component, identify:
- Which feature doc covers it: `docs/Features/{Domain}/Feature_*.md`
- Whether a sub-feature is large enough to warrant its own doc (see §2.5)
- Whether the handoff doc already exists: `docs/Handoff/Handoff_*_{date}.md`

**Mapping table (fill in before proceeding):**

| File / Component | Feature Doc | New Handoff Needed? |
|-----------------|-------------|---------------------|
| (fill from git status) | | |

### 1.3 — Check Network Connectivity

```bash
# Test ADO connectivity
curl -s --max-time 5 -o /dev/null -w "%{http_code}" https://ehbads.hrsa.gov/ads/EHBs/EHBs/ 2>/dev/null
# 200/301/302 = network up; anything else = offline, skip push
```

---

## Phase 2 — Feature Document Updates

For **each feature doc** affected by this work, add or update every section below. If a feature doc does not exist yet, create it using the template in §2.6 before filling in the sections.

**Feature doc location:** `docs/Features/{Domain}/Feature_{ComponentName}_v1.0.md`

---

### 2.1 — Designed State

Update the technical design section to reflect the **current deployed state** (not the aspirational design).

Required content:
- **Data model** — all custom objects, fields, and relationships (Lookup/Master-Detail) touched
- **Component hierarchy** — which LWC renders inside which (parent → child)
- **Apex entry points** — `@AuraEnabled` methods, trigger handlers, batch/scheduled jobs
- **Event flow** — custom events fired and their payloads (`detail.scheduleKey`, etc.)
- **State management** — `@track` properties, `@wire` adapters, reactive getters used

```markdown
## Technical Design — Designed State

### Component Architecture
```
[Parent LWC]
  └── cmn_ConstructionBatchList
        ├── data: getConstructionBatches()  ← Apex
        ├── expand: getBatchCIs()           ← Apex (lazy)
        └── event: openconstruction { scheduleKey, ciId }
```

### Data Flow
1. `connectedCallback` → `getConstructionBatches()` Apex call
2. Expand click → `getBatchCIs({ scheduleKey })` Apex (lazy, cached)
3. Open click → dispatches `openconstruction` custom event

### Key Fields
| Object | Field | Type | Purpose |
|--------|-------|------|---------|
| `cmn_ContextInstance__c` | `View_Mode__c` | Text | Filter for Construction state |
| `cmn_ContextInstance__c` | `ScheduleKey__c` | Text | Groups bulk batch CIs |
```

---

### 2.2 — Acceptance Criteria

Replace any placeholder ACs with verified, testable statements. Mark each as ✅ Verified, ⬜ Not Tested, or ❌ Failed.

Format:
```markdown
## Acceptance Criteria

| # | Scenario | Given | When | Then | Status |
|---|----------|-------|------|------|--------|
| AC-01 | [Title] | [precondition] | [action] | [expected outcome] | ✅ Verified |
| AC-02 | [Title] | ... | ... | ... | ⬜ Not Tested |
```

**Rules:**
- Every AC must be independently verifiable (Given/When/Then format preferred)
- At minimum one AC per user story / business requirement
- Deployment-blocking ACs must be ✅ before PR merge
- ACs that require config data (registry, bundle items) should note that dependency

---

### 2.3 — Test Coverage

Document both **unit test** and **E2E test** coverage. Do not leave this section blank.

```markdown
## Test Coverage

### Unit Tests (Apex)

| Test Class | Method | Covers | Status |
|------------|--------|--------|--------|
| `cmn_SubmissionConstructionControllerTest` | `getBatchCIs_returnsMatchingCIs` | Happy path — 1 CI returned | ✅ |
| `cmn_SubmissionConstructionControllerTest` | `getBatchCIs_noMatchingCIs_returnsEmpty` | Empty schedule key match | ✅ |
| `cmn_SubmissionConstructionControllerTest` | `getBatchCIs_blankScheduleKey_throws` | Blank input guard | ✅ |

**Run:**
```bash
sf apex run test --class-names cmn_SubmissionConstructionControllerTest --target-org dmedev5 --synchronous
```

### Jest Tests (LWC)

| Test File | Coverage | Status |
|-----------|----------|--------|
| `lwc/__tests__/cmn_ConstructionBatchList.test.js` | [list what's covered] | ✅ / ⬜ |

**Run:**
```bash
npm run test:unit -- --testPathPattern=cmn_ConstructionBatchList
```

### E2E Tests (Playwright)

| Spec File | Project Name | Tests |
|-----------|-------------|-------|
| `Tests/e2e/construction-batch-ci-expansion.spec.js` | `construction-batch-ci-expansion` | T_CBL01–T_CBL07 |

**Run:**
```bash
npx playwright test --project=construction-batch-ci-expansion
```

### Coverage Gaps

| Gap | Severity | Notes |
|-----|----------|-------|
| (any gaps here) | | |
```

---

### 2.4 — Test Scenarios

Write human-readable test scenarios covering happy path, edge cases, and failure modes. These are separate from ACs — they describe the full test matrix a QA engineer would execute.

```markdown
## Test Scenarios

### Happy Path

| ID | Scenario | Steps | Expected |
|----|----------|-------|----------|
| TS-01 | Expand bulk batch loads CI list | 1. Navigate to Setup tab 2. Click expand toggle on a bulk row | CI sub-table appears with one row per CI in the batch |
| TS-02 | Collapse hides CI list | 1. Expand a batch 2. Click collapse toggle | CI sub-table disappears; chevron returns to right |
| TS-03 | Open CI from sub-table | 1. Expand batch 2. Click Open on a CI row | `openconstruction` event fires with `ciId` set |

### Edge Cases

| ID | Scenario | Steps | Expected |
|----|----------|-------|----------|
| TS-04 | Batch with 0 CIs in Construction | Expand a batch whose CIs have View_Mode__c ≠ 'Construction' | Empty sub-table state or error message |
| TS-05 | Batch with >10 CIs | Expand large batch | Pagination controls visible; page shows first 10 CIs |
| TS-06 | Refresh while expanded | Expand batch → click Refresh | All panels collapsed; fresh batch list loaded |

### Failure / Error States

| ID | Scenario | Steps | Expected |
|----|----------|-------|----------|
| TS-07 | Apex error on expand | Network/permission issue during getBatchCIs | Error message shown in panel; no stack trace exposed |
| TS-08 | No construction batches | Org has no CIs with View_Mode__c = 'Construction' | Empty state message shown |
```

---

### 2.5 — Sub-Feature Files

**Create a sub-feature doc when:**
- The sub-feature has its own user story / acceptance criteria
- It affects a different domain from the parent feature
- It will be deployed independently or has its own maintenance lifecycle

**Threshold:** If a change touches >3 Apex classes or >2 LWC components in a domain not covered by the parent feature doc, create `docs/Features/{NewDomain}/Feature_{SubFeatureName}_v1.0.md`.

Use the template in §2.6 for the new file, then add a cross-reference in the parent doc:

```markdown
## Related Features

- [Construction Batch CI Expansion](../SubmissionConstruction/Feature_ConstructionBatchCIExpansion_v1.0.md)
```

---

### 2.6 — Feature Doc Template (new file)

```markdown
# Feature: {Feature Name}

**Version:** 1.0
**Last Updated:** {YYYY-MM-DD}
**Status:** ✅ Deployed
**Products:** GAM; [PWPM | PRS | PRM | COM | LGP as applicable]
**Feature Type:** [UI Enhancement | Backend Service | Integration | Data Model | Bug Fix]
**Target Release:** {Sprint/Date}
**Branch:** `dev/DME/feature/anthony`
**In-Scope (MVP):** Yes
**Part of Original ROM (POOR):** No

---

## 1. Executive Summary

{1–3 sentence summary: what it does, who benefits, why it matters}

---

## 2. Business Context

**Problem:** {What was missing or broken}
**Solution:** {What was built}
**Business Value:** {Impact on users / operations}

---

## 3. User Journey

{Step-by-step narrative of the user's experience through this feature}

1. User navigates to {page}
2. User sees {component} and {action}
3. System responds with {outcome}
...

---

## 4. Wireframes

{ASCII or linked PNG wireframes of the before/after state}

```
Before:
┌─────────────────────────┐
│  [Table header]         │
│  Row 1   Count: 5  Open │
│  Row 2   Count: 3  Open │
└─────────────────────────┘

After:
┌─────────────────────────────────────────┐
│  [Table header]                         │
│  ▶ Row 1  Bulk—5 grantees  In Progress  │
│    ├── CI #1  Health Center  Draft  ⊕   │
│    ├── CI #2  Clinic ABC     Draft  ⊕   │
│    └── [1–5 of 5] ◀ ▶                   │
│  ▶ Row 2  Bulk—3 grantees  In Progress  │
└─────────────────────────────────────────┘
```

---

## 5. Technical Design — Designed State

### Component Architecture
{Component hierarchy diagram}

### Data Flow
{Numbered steps tracing data from trigger to render}

### Key Fields
{Table of objects, fields, types, purposes}

---

## 6. Code Walkthrough

{Linear walkthrough of the code path — see §2.7}

---

## 7. Acceptance Criteria

| # | Scenario | Given | When | Then | Status |
|---|----------|-------|------|------|--------|
| AC-01 | ... | ... | ... | ... | ✅ |

---

## 8. Test Coverage

{Unit + Jest + E2E tables — see §2.3}

---

## 9. Test Scenarios

{Happy path, edge cases, error states — see §2.4}

---

## 10. Known Issues / Gaps

| Item | Severity | Notes |
|------|----------|-------|

---

## 11. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | {date} | Initial implementation |
```

---

### 2.7 — Code Walkthrough

For each major feature, add a **linear code walkthrough** that traces the full execution path from user action to data persistence and back. This is the most valuable long-term reference for onboarding and debugging.

**Format:**
```markdown
## Code Walkthrough — {Feature Name}

### Entry Point: {user action or trigger}

**1. LWC — `{ComponentName}.js` : `{handlerName}(event)`**
```
File: force-app/main/default/lwc/cmn_ConstructionBatchList/cmn_ConstructionBatchList.js
Line: ~87

handleToggleExpand(event) {
  // 1a. Read scheduleKey from data attribute
  const scheduleKey = event.currentTarget.dataset.scheduleKey;
  // 1b. Toggle isExpanded in batchPanels map (immutable replace → reactivity)
  this.batchPanels = { ...this.batchPanels, [scheduleKey]: { isExpanded: true } };
  // 1c. Lazy-load CIs if not already fetched
  if (nowExpanded && !current.allCIs) this._loadCIs(scheduleKey);
}
```

**2. Apex — `{ControllerName}.{methodName}()`**
```
File: force-app/main/default/classes/cmn_SubmissionConstructionController.cls
Line: ~620

getBatchCIs(scheduleKey):
  → SOQL: SELECT Id, Workflow_Status__c, View_Mode__c, Resource_Organization1__r.Name
           FROM cmn_ContextInstance__c
           WHERE ScheduleKey__c = :scheduleKey AND View_Mode__c = 'Construction'
  → Returns: List<BatchCIDTO> (id, orgName, grantNumber, workflowStatus, constructionStatus, viewMode)
```

**3. LWC — Reactive render**
```
_loadCIs resolves → this.batchPanels[scheduleKey].allCIs = result
  → get rows() recomputes → panelHasCIs = pagedCIs.length > 0
  → <template if:true={row.panelHasCIs}> renders CI sub-table
```

**Error path:**
```
getBatchCIs throws → catch sets panel.error
  → <template if:true={row.panelError}> renders alert
  → panel.isLoading = false (spinner clears)
```
```

---

### 2.8 — User Journey Update

Rewrite or extend the User Journey section so it reflects the **current deployed behavior**, not the aspirational spec. Use numbered steps, and note which component handles each step.

```markdown
## User Journey — {Role}

**Precondition:** User is on Reviews & Monitoring page, Setup tab active

1. **Page load** — `cmn_ConstructionBatchList` calls `getConstructionBatches()` Apex; spinner shown
2. **Batch list renders** — one row per bulk ScheduleKey; single-action CIs each get their own row
3. **User sees "Bulk — N grantees"** — row shows bundle, type, count, status, created date, Open button
4. **User clicks expand (▶)** — `handleToggleExpand` fires; CI load begins (lazy); row-level spinner shown
5. **CIs load** — `getBatchCIs` Apex returns; sub-table renders with one row per CI
6. **User reviews CI list** — Grantee Name, Grant Number, Workflow Status, Construction Status, View Mode visible
7. **User opens individual CI** — clicks Open → `openconstruction` event dispatched with `ciId`; parent navigates
8. **User collapses row** — clicks collapse (▼) → sub-table hides; CIs remain cached for re-expand
9. **User opens batch** — clicks batch-level Open → `openconstruction` event with `scheduleKey`
10. **User refreshes** — `handleRefresh` → `_load()` → all panel state cleared; fresh batch list loaded
```

---

### 2.9 — Wireframes Update

Update wireframes to show the **actual rendered state**, including:
- Before state (what existed before this work)
- After state (what exists now)
- Error state
- Empty state
- Edge cases (e.g., batch with 0 CIs matching filter)

ASCII wireframes are preferred for version-control-friendly docs:
```
┌── [Before] Batch list ──────────────────────────────────┐
│  Bundle  │ Type          │ Status    │ Created │ Action  │
│  ──────────────────────────────────────────────────────  │
│          │ Bulk — 3      │ In Progr. │ Mar 31  │  Open   │
│          │ Bulk — 5      │ In Progr. │ Mar 31  │  Open   │
└─────────────────────────────────────────────────────────┘

┌── [After] Batch list — expanded ────────────────────────┐
│  ▼       │ Bulk — 3      │ In Progr. │ Mar 31  │  Open   │
│  ┌── CI sub-table ───────────────────────────────────┐  │
│  │ Grantee Name  │ Grant # │ Wf Status │ Const.│ VM │⊕│ │
│  │ Health Ctr A  │H80GR001 │ Draft     │InProg │Con │⊕│ │
│  │ Clinic B      │H80GR002 │ Draft     │InProg │Con │⊕│ │
│  │ Medical C     │H80GR003 │ Draft     │InProg │Con │⊕│ │
│  │ [1–3 of 3]                                        │  │
│  └───────────────────────────────────────────────────┘  │
│  ▶       │ Bulk — 5      │ In Progr. │ Mar 31  │  Open   │
└─────────────────────────────────────────────────────────┘
```

---

## Phase 3 — Handoff Document

Create a handoff document for each logical unit of work deployed in this session.

**File:** `docs/Handoff/Handoff_{ComponentOrFeature}_{YYYY-MM-DD}.md`

**Required sections (minimum viable handoff):**

```markdown
# Handoff: {Feature / Component Name}

**Date:** {YYYY-MM-DD}
**Branch:** `dev/DME/feature/anthony`
**Status:** Implemented — deployed to dmedev5
**Scope:** {1–2 sentence summary of what was built/fixed}

---

## 1. Summary
{What changed and why}

## 2. What Was Changed
### Change 1 — {Name}
**File:** `force-app/...`
**Problem:** {what was wrong or missing}
**Fix:** {what was added/changed}

## 3. Files Changed
| File | Change |
|------|--------|

## 4. Deployment Notes
Deploy ID(s): {from sf deploy output}

## 5. Acceptance Criteria
| # | Scenario | Expected | Status |
|---|----------|----------|--------|

## 6. E2E Test Cases
| ID | Test | Trigger | Asserts | Status |
|----|------|---------|---------|--------|

## 7. Key Files
| File | Role |
|------|------|

## 8. Risks / Open Items
| Item | Severity | Notes |
|------|----------|-------|
```

**Handoff anti-patterns to avoid:**
- Do NOT repeat what git diff already shows — focus on the "why" and the "non-obvious"
- Do NOT leave Acceptance Criteria as ⬜ without a note explaining what blocks testing
- Do NOT create a handoff doc that duplicates an existing one — append to the existing doc if it covers the same session/branch

---

## Phase 4 — Commit & Push

### 4.1 — Stage the Right Files

```bash
# Review what's changed
git status --short
git diff --stat HEAD

# Stage selectively — never use git add -A without reviewing
# Apex + LWC changes
git add force-app/main/default/classes/{ChangedClass}.cls
git add force-app/main/default/classes/{ChangedClass}.cls-meta.xml
git add force-app/main/default/lwc/{ComponentName}/

# Tests
git add Tests/e2e/{spec-name}.spec.js
git add Tests/screenshots/{prefix}-*.png
git add playwright.config.js

# Docs
git add docs/Handoff/Handoff_{Name}_{Date}.md
git add docs/Features/{Domain}/Feature_{Name}_v1.0.md

# Never stage these:
# .env, *.stackdump, bash.exe.stackdump, node_modules/, .claude/worktrees/
```

### 4.2 — Commit Message Format

```
{type}({scope}): {short description}

{body — what and why, not how}

Co-Authored-By: Dev Team <noreply@hrsa.gov>
```

**Types:** `feat` | `fix` | `refactor` | `test` | `docs` | `chore`

**Scope:** component or domain name (`construction`, `pwpm`, `narrative`, `psp`, etc.)

**Examples:**
```
feat(construction): expandable CI sub-table in Setup batch list
fix(lifecycle): resolve node key lookup and View_Mode__c stamp on CI init
docs(handoff): add PSP Construction handoff with AC and E2E tests
test(construction): add E2E spec for batch CI expansion (T_CBL01–T_CBL07)
```

**Commit:**
```bash
git commit -m "$(cat <<'EOF'
feat(construction): {short description}

- {bullet 1}
- {bullet 2}
- {bullet 3}

Co-Authored-By: Dev Team <noreply@hrsa.gov>
EOF
)"
```

### 4.3 — Check Network Before Push

```bash
# Test ADO network connectivity
node -e "
const { execSync } = require('child_process');
try {
  execSync('curl -s --max-time 5 -o /dev/null -w \"%{http_code}\" https://ehbads.hrsa.gov/ads/EHBs/EHBs/', { shell: 'cmd.exe', encoding: 'utf8' });
  console.log('Network: UP — safe to push');
} catch (e) { console.log('Network: DOWN — skip push, note in pending_push memory'); }
"
```

### 4.4 — Push

```bash
# Push to feature branch (current branch: dev/DME/feature/anthony)
git push origin dev/DME/feature/anthony

# If push fails due to upstream divergence:
git pull --rebase origin dev/DME/feature/anthony
git push origin dev/DME/feature/anthony
```

### 4.5 — If Offline (Network Down)

Update the pending push memory file:

```
C:\Users\adourish\.claude\projects\C--projects-BPHC-GAM2010\memory\project_pending_push.md
```

Add an entry:
```markdown
## Pending Push — {YYYY-MM-DD}

**Branch:** dev/DME/feature/anthony
**Commits:** {N} local commits pending push
**Reason:** ADO network outage / VPN not connected
**Push when:** Network restored to ehbads.hrsa.gov

**Commits to push:**
- {commit hash}: {commit message}
```

### 4.6 — PR Creation (optional, when integration branch is ready)

```bash
# PR: dev/DME/feature/anthony → dev/DME/feature/sf-develop
# (QE creates sf-develop; push there triggers QE pipeline)

# Check current branch tracks remote
git log --oneline origin/dev/DME/feature/sf-develop..HEAD

# Create PR via ADO API (see skill_bphc_ado_feature_documentation.md for full flow)
# PR merge strategy: noFastForward
# bypassPolicy: True for doc-only changes
```

---

## Phase 2 Checklist (Copy & Use)

Copy this checklist into the feature doc or a scratch note and check off items as you go:

```
## DoD Checklist — {Feature} — {Date}

### Documentation
- [ ] Feature doc updated or created
- [ ] Designed state written (data model, component arch, data flow)
- [ ] User journey updated (numbered steps, component callouts)
- [ ] Wireframes updated (before/after/error/empty states)
- [ ] Code walkthrough written (entry point → Apex → render → error path)
- [ ] Sub-feature docs created (if any)
- [ ] Cross-references added between related docs

### Acceptance Criteria
- [ ] All ACs are Given/When/Then format
- [ ] Every AC has a ✅ / ⬜ / ❌ status
- [ ] Deployment-blocking ACs are ✅ or have documented exception

### Tests
- [ ] Unit tests written for new Apex methods (happy path + error guard)
- [ ] Jest tests written or updated for LWC (or gap noted with justification)
- [ ] E2E tests written and passing (or soft-skipped with documented reason)
- [ ] Test scenarios documented (happy, edge, error states)
- [ ] Test coverage gaps documented

### Handoff
- [ ] Handoff doc created or updated
- [ ] All changed files listed with descriptions
- [ ] Deploy IDs recorded
- [ ] Risks / open items documented

### Commit & Push
- [ ] Staged only relevant files (no .env, .stackdump, node_modules)
- [ ] Commit message follows feat/fix/docs/test({scope}): format
- [ ] Tests pass locally (lint-staged hook passes)
- [ ] Pushed to origin (or pending_push memory updated if offline)
```

---

## Common Patterns & Shortcuts

### Finding the Feature Doc for a Component

```bash
# Search feature docs for references to a component name
grep -r "cmn_ConstructionBatchList" docs/Features/ --include="*.md" -l

# Or by domain — construction/submission work
ls docs/Features/SubmissionInitiation/
ls docs/Features/ProgressStatusPanel/
```

### Verifying Deploy IDs

```bash
# List recent deploys with IDs
sf org list metadata-types --target-org dmedev5 2>/dev/null

# Or check the last deploy output from CI
git log --oneline -5
```

### Checking Pending Commits Before Push

```bash
# Commits not yet in sf-develop
git log --oneline origin/dev/DME/feature/sf-develop..HEAD 2>/dev/null || git log --oneline -10
```

---

## Section 508 Reminder

Before marking any feature doc ✅, apply the Section 508 review:
- Heading hierarchy: H1 → H2 → H3 (no skips)
- Alt text: all images/screenshots have descriptive alt text
- Links: descriptive text (not "click here")
- Status indicators: emoji + text label (not emoji-only)
- Mermaid/ASCII diagrams: include a text description below

(See `memory/feedback_section_508.md` for full checklist)

---

## ADO Reminder

After pushing and creating the PR, update any linked ADO work items:
- Move User Story/Tech Story to "Done" or "Closed" state
- Add completion comment with PR link and deploy ID
- Link the handoff doc URL in the ADO work item description

(See `skill_bphc_ado_feature_documentation.md` for ADO API patterns)
