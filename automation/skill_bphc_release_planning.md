# BPHC Release Planning Estimates — Build & Sync Workflow

## Quick Reference

**Use when:** Rebuilding the Release Planning Excel, changing release structure/targets, syncing completion percentages from feature CSV, or patching ADO epic effort fields
**Don't use when:** One-off ADO task updates; feature doc creation (use `skill_bphc_ado_feature_documentation.md`)
**Trigger phrases:** "rebuild planning excel", "update release plan", "rerun planning", "update ado effort", "sync completion percentages", "new release structure", "planning estimates"
**Time:** 5–15 min (build only: ~1 min; full sync with ADO patch: ~5–10 min)
**Repo:** `C:\projects\BPHC-GAM2010`

---

## Release Structure (current as of 2026-03-19)

```
R1 — June 2026 (UAT)
  R1a  Foundation + Common          (53 features, 41% done)
  R1b  PWPM                         (14 features, 48% done)
  R1c  Data Migration (DM Series)   (11 features,  0% done)
  R1d  Data Integration             ( 3 features,  0% done)
  R1e  Multi-Vendor / Org           ( 6 features,  5% done)

R2 — August 2026
  R2a  PRM                          (12 features, 28% done)

R3 — October 2026
  R3a  LGP                          (32 features, 31% done)
  R3b  COM Product                  ( 7 features, 14% done)
  R3c  Foundation + Common (LGP/COM)( 1 feature,  12% done)
  R3d  Data Migration: Deferred     ( 3 features,  0% done)

R4 — TBD
  R4a  Configuration + Platform     (28 features, 54% done)
  R4b  Non-MVP + AI + Enhancements  (33 features, 43% done)
```

---

## Key Files

| File | Purpose |
|------|---------|
| `docs/Planning/ReleasePlanningEstimates/build_release_planning_excel.py` | Master builder — generates base Excel from CSV |
| `docs/Planning/ReleasePlanningEstimates/Release_Planning_Estimates_v2.0.csv` | Source of truth for all features, hours, statuses |
| `scripts/inject_completion_release_sheets.py` | Post-processor — injects % Complete, Remaining Hrs, Sprints into Excel |
| `docs/Features/FEATURE_COMPLETION_SUMMARY.csv` | Per-feature completion % (from QA testing output) |
| `docs/Planning/ReleasePlanningEstimates/patch_ado_effort_pct.py` | Patches ADO epic/feature Effort field with AI hour % |
| `G:\My Drive\03_Areas\Keys\Environments\devops-hrsa-ado.json` | ADO credentials (PAT + org URL) |

---

## Step 1 — Rebuild the Excel

```bash
cd "C:\projects\BPHC-GAM2010\docs\Planning\ReleasePlanningEstimates"
python build_release_planning_excel.py
```

**Output:** `Release_Planning_Estimates_v3.X.xlsx` (version set in `OUT_XLSX` at top of script)

**What it generates (33 sheets):**
- `Release Plan` — summary table, capacity fit analysis, product building blocks, scenarios
- `Release Detail` — per-release feature breakdown by product group and category
- `Release Schedule` — flat feature list across all releases with cumulative hours
- `Scenarios` — 3 alternate phasing scenarios with capacity fit
- `Dimensions` — MVP / BPR / POOR breakdowns
- `Original ROM Comparison`, `Hours Summary`, `Epic Progress` — rollup views
- `All Features`, `R1a Features` … `R4b Features` — per-release flat lists
- `PG Common` … `PG Deferred Forms` — per-product-group flat lists
- `Scope Growth Analysis` — feature count/hours trend

---

## Step 2 — Inject Completion Columns

```bash
cd "C:\projects\BPHC-GAM2010"
python scripts/inject_completion_release_sheets.py
```

**What it injects into Release Plan, Release Detail, and Release Schedule:**
- `% Complete` — color-coded (green ≥80%, yellow ≥50%, orange ≥20%, red <20%)
- `Remaining Hrs` — Human hours × (1 − % Complete)
- `Sprints (80h/person)` — Remaining ÷ 80

**Per-release completion source:** `RELEASE_AVG` dict in the inject script (manually maintained).
**Per-feature completion source:** `FEATURE_COMPLETION_SUMMARY.csv` matched via `ADO_HINTS` lookup.

---

## Step 3 — Backup

```bash
cp "docs/Planning/ReleasePlanningEstimates/Release_Planning_Estimates_v3.X.xlsx" \
   "docs/Planning/ReleasePlanningEstimates/archive/Release_Planning_Estimates_v3.X_backup_YYYYMMDD.xlsx"
```

---

## Step 4 (Optional) — Patch ADO Effort Fields

```bash
cd "C:\projects\BPHC-GAM2010\docs\Planning\ReleasePlanningEstimates"
python patch_ado_effort_pct.py
```

**What it does:** Reads `Release_Planning_Estimates_v2.0.csv`, computes each feature's AI hours as a % of grand total AI hours, and PATCHes `Microsoft.VSTS.Scheduling.Effort` on every ADO feature and epic.

**ADO Epic IDs patched:**

| Release | ADO Epic ID |
|---------|------------|
| R1a | #429740 |
| R1b | #429747 (was PWPM in v3.8; update if reassigned) |
| R1c | #430303 |
| R1d | #430304 |
| R1e | #429743 |
| R2a | #429747 (PRM — verify current ID) |
| R3a | #429742 (LGP) |
| R3b | #429744 (COM) |
| R4a | #429745 |
| R4b | #429746 |
| Platform (grand total) | #427499 |

> **Note:** `patch_ado_effort_pct.py` still uses old release codes (R1b=PRM, R1c=PWPM, etc.). Update `EPIC_IDS` and `assign_release()` in that script when IDs or structure change.

---

## Changing the Release Structure

When the release structure changes (e.g., new target dates, products move between releases):

### 1. Update `build_release_planning_excel.py`

| Section | What to change |
|---------|---------------|
| `OUT_XLSX` | Bump version (e.g., `v3.9.xlsx` → `v4.0.xlsx`) |
| `RELEASE_META` | Add/remove/rename releases; update `target`, `desc`, `note` |
| `Feature._release()` | Update product group → release code mappings |
| `Feature.priority` | Update which releases are "Highest" priority |
| `main()` — capacity vars | Update `r1x_feats` variables and fit analysis to match new R1 group |
| `main()` — window logic | Update `window` string for each release prefix |
| `main()` — recommendations | Update recommendation text |
| `main()` — scenarios sheet | Update scenario definitions |
| Date header | Update date string |

### 2. Update `inject_completion_release_sheets.py`

| Section | What to change |
|---------|---------------|
| `IN_FILE` / `OUT_FILE` | Update to new version filename |
| `RELEASE_AVG` | Remap old release codes → new codes, carry over completion % |

### 3. Update `patch_ado_effort_pct.py`

| Section | What to change |
|---------|---------------|
| `EPIC_IDS` | Add new epic IDs for new releases |
| `assign_release()` | Mirror the same routing logic as `Feature._release()` |

---

## Capacity Reference

| Parameter | Value |
|-----------|-------|
| Developers | 12 |
| QC engineers | 6 |
| Hours/week/person | 40h |
| Weekly team capacity | 720h |
| Capacity to June UAT | 5,700h |
| AI model | 0.75× human (25% reduction) |
| QA model | 40% of dev hours |
| Sprint size | 80h/person |
| Team sprint capacity | 1,440h (18 people × 80h) |

**June R1 capacity check (v3.9):**
- R1a + R1b (Foundation + PWPM): 4,271h AI → **fits** (+1,429h slack)
- R1a–R1d (+ Data): 5,373h AI → **fits** (+327h slack)
- All R1 including Multi-Vendor: 5,919h AI → **219h over** (Multi-Vendor is swing item)

---

## Full Run (all steps)

```bash
cd "C:\projects\BPHC-GAM2010\docs\Planning\ReleasePlanningEstimates"
python build_release_planning_excel.py
cd "C:\projects\BPHC-GAM2010"
python scripts/inject_completion_release_sheets.py
cp "docs/Planning/ReleasePlanningEstimates/Release_Planning_Estimates_v3.9.xlsx" \
   "docs/Planning/ReleasePlanningEstimates/archive/Release_Planning_Estimates_v3.9_backup_$(date +%Y%m%d).xlsx"
# optional ADO patch:
# python docs/Planning/ReleasePlanningEstimates/patch_ado_effort_pct.py
```
