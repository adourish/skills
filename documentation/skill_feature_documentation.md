# Feature Documentation Master Guide

**Purpose:** Comprehensive guide for creating, structuring, and maintaining feature documentation in Salesforce projects

**Last Updated:** February 26, 2026  
**Version:** 1.0  
**Success Rate:** N/A (New Guide)

---

## Table of Contents

1. [Overview](#overview)
2. [When to Create a Feature Document](#when-to-create-a-feature-document)
3. [Document Structure](#document-structure)
4. [Section-by-Section Guide](#section-by-section-guide)
5. [Feature Catalog Standards](#feature-catalog-standards)
6. [Writing Best Practices](#writing-best-practices)
7. [File Organization](#file-organization)
8. [Templates](#templates)
9. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
10. [Examples and References](#examples-and-references)

---

## Overview

### What is a Feature Document?

A feature document is a comprehensive design specification that describes a Salesforce feature from business requirements through technical implementation. It serves as:

- **Single Source of Truth**: All stakeholders reference the same document
- **Communication Tool**: Bridges business and technical teams
- **Implementation Guide**: Developers follow the technical specifications
- **Historical Record**: Documents decisions and rationale

### Document Philosophy

**Business-First Approach:**
- Start with business value and user needs
- Technical details support business requirements
- Non-technical stakeholders can understand the "what" and "why"
- Technical teams get the "how" in later sections

**Living Documents:**
- Update as requirements evolve
- Track version history
- Document decisions and changes
- Archive superseded versions

---

## When to Create a Feature Document

### Create a Feature Document When:

✅ **New Feature Development**
- Building a new capability not in the existing system
- Modernizing legacy functionality with significant changes
- Adding cross-system functionality

✅ **Complex Enhancements**
- Feature affects multiple objects or components
- Requires new data model or architecture
- Involves workflow or business process changes

✅ **Integration Projects**
- Connecting to external systems
- Implementing new APIs
- Data migration from legacy systems

✅ **Data Model Documentation**
- Documenting common data objects across features
- Defining data lineage from source systems
- Creating data dictionaries and field inventories
- Documenting integration patterns and architecture

### Do NOT Create a Feature Document For:

❌ **Simple Bug Fixes**
- Use ADO work items or bug tracking instead

❌ **Configuration Changes**
- Document in configuration guides or admin documentation

❌ **Minor UI Tweaks**
- Use design system documentation or component specs

❌ **One-Off Scripts**
- Document in script headers and README files

---

## Document Structure

### Standard Template Structure

All feature documents follow this structure:

```markdown
# [Feature Name] Feature Design
**[Subtitle/Description]**

**Date:** [Creation Date]
**Version:** [Version Number]
**Status:** [Design Phase | In Development | Implemented | Deprecated]

---

## Table of Contents
1. Executive Summary
2. Business Design
3. User Experience Design
4. Technical Design
5. Implementation Plan
6. Appendix

---

## Executive Summary
### Purpose
### Business Value
### Key Stakeholders

## Business Design
### Feature Overview
### Feature Catalog
### System Applicability

## User Experience Design
### User Personas
### User Journeys
### Wireframes
### Interaction Flows

## Technical Design
### Data Model
### Architecture
### API Specifications
### Security Model

## Implementation Plan
### Phase 1: MVP
### Phase 2: Enhancements
### Success Criteria

## Appendix
### A. Legacy System Architecture
### B. Gap Analysis
### C. Migration Strategy
```

### Alternative Structure: Data/Integration Features

For data model and integration features, use this structure:

```markdown
# [Feature Name] Feature Documentation
**[Subtitle/Description]**

**Feature Name:** [Name]
**Version:** [Version Number]
**Date:** [Creation Date]
**Status:** [Active | Deprecated]

---

## Overview
[Brief description of the feature and its purpose]

---

## Data Lineage Summary

### Source Systems
1. **[System 1]** - [Description]
2. **[System 2]** - [Description]

### Integration Flows
[Mermaid diagram showing data flow]

**Text Description:**
[Accessible text description of the diagram]

---

## Worksheet Definitions

### WS01: [Worksheet Name]
**Filename:** `WS01_[Name].csv`
**Status:** ✅ Complete | ⏳ Pending | ❌ Blocked
**Records:** [Count]
**Purpose:** [Description]

**Columns:**
- [Column list]

**Data Lineage by Object Type:**
[Table showing lineage]

---

## Common Data Lineage Details

### 1. [Data Domain Name]
**Full Lineage:** `[Source] → [Target]`

**Process Flow:**
1. **[System]** - [Description]
2. **[System]** - [Description]

**Objects Affected:**
- `[Object__c]` ([Description])

**Integration Method:** [Method]
**Data Owner:** [Owner]
**Sync Frequency:** [Frequency]

---

## Integration Architecture

### Integration Methods Overview
[Description of integration patterns]

### Integration Patterns Diagram
[Mermaid sequence diagram]

**Text Description:**
[Pattern descriptions]

---

## Data Ownership & Master Data Management

### Master Data Sources
[Table showing master vs operational systems]

---

## Sync Frequencies
[Table showing sync details]

---

## Worksheet File Locations
[File locations and current files list]

---

## Next Steps

### Immediate Actions
[Checklist of actions]

### Future Enhancements
[List of enhancements]

---

## Section 508 Accessibility Compliance
[Compliance checklist and verification]

---

**Document Owner:** [Team]
**Last Updated:** [Date]
**Next Review:** [Date]
**Status:** [Status]
**Section 508 Compliance:** ✅ Verified [Date]
```

### Required vs Optional Sections

**Standard Feature Documents (User-Facing):**

**Always Required:**
- Executive Summary
- Feature Overview
- Feature Catalog
- Data Model (if new objects/fields)
- Implementation Plan

**Include When Applicable:**
- User Personas (for user-facing features)
- Wireframes (for UI features)
- API Specifications (for services/integrations)
- Legacy System Architecture (for modernization)
- Gap Analysis (for legacy replacement)
- Migration Strategy (for data migration)

**Data/Integration Feature Documents:**

**Always Required:**
- Overview
- Data Lineage Summary (with diagram)
- Worksheet Definitions
- Integration Architecture
- Data Ownership & Master Data Management
- Sync Frequencies
- Section 508 Compliance

**Include When Applicable:**
- Common Data Lineage Details (for each data domain)
- Integration Patterns Diagram
- Worksheet File Locations
- Next Steps
- ETL Transformation Rules
- Field-level Data Mapping

---

## Section-by-Section Guide

### 1. Executive Summary

**Purpose:** 2-3 paragraph overview for executives and stakeholders

**What to Include:**
- **Purpose**: What problem does this solve? (1-2 sentences)
- **Business Value**: Bullet list of key benefits
- **Key Stakeholders**: Who uses this? Who's affected?

**Example:**
```markdown
### Purpose

Enable assigned reviewers to request input from additional subject 
matter experts or stakeholders on specific review items without 
changing the primary reviewer assignment.

### Business Value

- **Improved Collaboration**: Real-time coordination via Chatter
- **Better Visibility**: Single queue with contributor filtering
- **Enhanced Workflow**: Streamlined request and response process
- **Audit Trail**: Complete history of requests and responses

### Key Stakeholders

- **Primary Users**: Reviewers (requestors), Contributors (SMEs)
- **Secondary Users**: Program managers, administrators
- **Systems**: LGP, COM, PRM, PWPM
```

### 2. Business Design

#### Feature Overview

**Purpose:** Detailed business description of the feature

**What to Include:**
- High-level description (2-3 paragraphs)
- Key capabilities (bullet list)
- MVP vs Phase 2 scope
- Integration points
- Key design decisions

**Writing Tips:**
- Use business language, not technical jargon
- Focus on user capabilities, not implementation
- Explain the "what" and "why", not the "how"

#### Feature Catalog

**Purpose:** Complete inventory of all feature capabilities

**Format:** Table with columns:
- Feature ID (F001, F002, etc.)
- Feature Name
- Description
- MVP (✅/🔄/❌)
- System Applicability (LGP, COM, PRM, PWPM)

**Legend:**
- ✅ MVP (Phase 1)
- 🔄 Phase 2 Enhancement
- ❌ Not Applicable

**Example:**
```markdown
| # | Feature | Description | MVP | LGP | COM | PRM | PWPM |
|---|---------|-------------|-----|-----|-----|-----|------|
| F001 | Request Contribution | Reviewer can request contribution | ✅ | ✅ | ✅ | ✅ | ✅ |
| F002 | Batch Request | Request from multiple contributors | ✅ | ✅ | ✅ | ✅ | ✅ |
| F003 | Email Notifications | Send email notifications | 🔄 | 🔄 | 🔄 | 🔄 | 🔄 |
```

**Numbering Convention:**
- Start at F001
- Sequential numbering (F001, F002, F003...)
- Reserve numbers for future features (leave gaps if needed)
- Never reuse feature numbers

#### System Applicability

**Purpose:** Describe how the feature applies to each system

**Format:**
```markdown
#### LGP (Local Government Portal)
- **Use Case**: [Primary use case]
- **Key Features**: [Feature IDs]
- **Volume**: [Expected usage]

#### COM (Compliance Monitoring)
- **Use Case**: [Primary use case]
- **Key Features**: [Feature IDs]
- **Volume**: [Expected usage]
```

### 3. User Experience Design

#### User Personas

**Purpose:** Define who will use this feature

**Format:**
```markdown
#### Persona 1: [Name] - [Role]

**Role**: [Job title/description]

**Goals:**
- [Primary goal 1]
- [Primary goal 2]

**Pain Points:**
- [Current problem 1]
- [Current problem 2]

**Key Workflows:**
- [Workflow 1]
- [Workflow 2]
```

**Best Practices:**
- Create 2-4 personas maximum
- Use real names and roles
- Focus on goals and pain points
- Keep descriptions concise (3-5 bullets each)

#### User Journeys

**Purpose:** Show step-by-step user flows

**Format:** Use ASCII art flowcharts

```markdown
┌─────────────────────────────────────────┐
│ START: User on main page                │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 1. User clicks action button            │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│ 2. Modal opens with form                │
└─────────────────────────────────────────┘
```

**Best Practices:**
- Number each step
- Include decision points
- Show alternative paths
- Keep journeys focused (5-15 steps)

#### Wireframes

**Purpose:** Visual representation of UI

**Options:**
1. ASCII art wireframes (for simple layouts)
2. Link to Figma/design files
3. Screenshots with annotations
4. Combination of above

**When to Include:**
- New UI components
- Complex layouts
- Multi-step wizards
- Dashboard designs

### 4. Technical Design

#### Data Model

**Purpose:** Define objects, fields, and relationships

**Format:** Tables for each object

```markdown
#### Object: cmn_ObjectName__c

**Purpose**: [What this object stores]

| Field Name | Type | Description | Required | Default |
|------------|------|-------------|----------|---------|
| Name | Auto Number | OBJ-{0000} | Yes | Auto |
| Field__c | Text(100) | [Description] | Yes | - |
| Status__c | Picklist | [Values] | Yes | Draft |
```

**Include:**
- Object API names
- Field API names and types
- Field descriptions
- Required/optional flags
- Default values
- Picklist values
- Lookup relationships
- Formula fields

**Relationship Diagrams:**
Use ASCII art to show object relationships:

```markdown
Parent__c
    |
    | (Lookup)
    |
    +-- Child__c
            |
            | (Master-Detail)
            |
            +-- GrandChild__c
```

#### Architecture

**Purpose:** Show component structure and interactions

**Include:**
- Component diagrams
- Service layer architecture
- Integration points
- Data flow diagrams

**Use ASCII art for diagrams:**

```markdown
┌─────────────────────────────────────┐
│ PRESENTATION LAYER (LWC)            │
├─────────────────────────────────────┤
│  componentName                      │
└─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ BUSINESS LOGIC LAYER (Apex)         │
├─────────────────────────────────────┤
│  ServiceClass.cls                   │
└─────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│ DATA LAYER (Objects)                │
└─────────────────────────────────────┘
```

#### API Specifications

**Purpose:** Document service methods and REST endpoints

**Format:**

```markdown
#### Apex Service Class: ServiceName

```apex
public with sharing class ServiceName {
    
    /**
     * Method description
     * @param param1 Description
     * @return Return value description
     */
    public static ReturnType methodName(
        Type param1,
        Type param2
    ) {
        // Implementation notes
    }
}
```
```

**Include:**
- Class names
- Method signatures
- Parameter descriptions
- Return types
- Error handling approach

#### Security Model

**Purpose:** Define access controls

**Include:**
- Object-level security (OLS)
- Field-level security (FLS)
- Sharing rules
- Apex sharing code examples

**Format:**

```markdown
#### Object-Level Security

| Object | Profile | Read | Create | Edit | Delete |
|--------|---------|------|--------|------|--------|
| Object__c | Admin | ✅ | ✅ | ✅ | ✅ |
| Object__c | User | ✅ | ✅ | ✅ | ❌ |
```

### 5. Implementation Plan

**Purpose:** Define phases, timeline, and success criteria

**Format:**

```markdown
### Phase 1: MVP (Weeks 1-4)

**Scope**: [High-level scope]

**Week 1: [Focus Area]**
- Task 1
- Task 2

**Week 2: [Focus Area]**
- Task 1
- Task 2

### Success Criteria

**Phase 1 (MVP):**
- [ ] Feature 1 implemented
- [ ] 80%+ test coverage
- [ ] UAT passed
- [ ] Performance < 2 seconds
```

**Best Practices:**
- Break into 1-2 week phases
- Define clear deliverables
- Include testing criteria
- Set measurable success metrics

### 6. Appendix

**Purpose:** Supporting information and reference material

**Common Appendix Sections:**

**A. Legacy System Architecture**
- Database schemas
- Classic workflows
- Integration points

**B. Gap Analysis**
- Features in legacy not in new system
- New features not in legacy
- Migration considerations

**C. Migration Strategy**
- Data migration approach
- Cutover plan
- Rollback procedures

---

## Feature Catalog Standards

### Numbering System

**Format:** F### (F001, F002, F003...)

**Rules:**
1. Start at F001 for each feature document
2. Sequential numbering
3. Never skip numbers in MVP
4. Can reserve numbers for future features
5. Never reuse feature numbers

### Feature Naming

**Good Names:**
- Request Contribution
- Save Draft
- Send Reminder
- Filter by Status

**Bad Names:**
- Do the thing (too vague)
- Click button (implementation detail)
- Feature 1 (not descriptive)

### Feature Descriptions

**Format:** [Actor] [Action] [Object/Result]

**Examples:**
- "Reviewer can request contribution from a user"
- "Contributor enters text response"
- "System sends email notification"

**Length:** 5-10 words maximum

### MVP vs Phase 2 Decisions

**MVP Criteria (✅):**
- Core functionality required for launch
- Blocks other critical features
- High business value, low complexity
- Frequently used by primary users

**Phase 2 Criteria (🔄):**
- Nice-to-have enhancements
- Low usage frequency
- High complexity, moderate value
- Can be added post-launch

**Not Applicable (❌):**
- Feature doesn't apply to this system
- Replaced by different approach
- Out of scope for this project

---

## Writing Best Practices

### Language and Tone

**Do:**
- Use active voice ("User clicks button")
- Write in present tense
- Be specific and concrete
- Use consistent terminology

**Don't:**
- Use passive voice ("Button is clicked")
- Write in future tense ("Will allow users...")
- Be vague or abstract
- Mix terminology

### Formatting

**Markdown Standards:**
- Use `#` for main sections
- Use `##` for subsections
- Use `###` for sub-subsections
- Use `####` for lowest level

**Lists:**
- Use `-` for unordered lists
- Use `1.` for ordered lists
- Use `- [ ]` for checklists

**Code Blocks:**
- Use triple backticks with language: ```apex
- Use single backticks for inline code: `fieldName`

**Tables:**
- Always include header row
- Use `|` for column separators
- Align columns for readability

### Visual Elements

**ASCII Art Guidelines:**
- Use for flowcharts and diagrams
- Keep width under 80 characters
- Use box-drawing characters: ┌─┐│└┘├┤┬┴┼
- Test rendering in markdown preview

**When to Use ASCII vs Images:**
- ASCII: Simple flows, relationships, architecture
- Images: Complex UI mockups, screenshots, detailed diagrams

---

## File Organization

### Folder Structure

```
docs/
├── Features/
│   ├── FeatureName/
│   │   ├── Feature_FeatureName_v1.0.md
│   │   ├── wireframes/ (optional)
│   │   └── diagrams/ (optional)
│   ├── AnotherFeature/
│   │   └── Feature_AnotherFeature_v1.0.md
│   └── Data_Model/
│       ├── Feature_CommonData_v1.0.md
│       └── csv_exports/
```

**Naming Conventions by Location:**
- **Feature Documents:** `Feature_[FeatureName]_v[Version].md`
- **Design Documents:** `[ComponentName]_Design.md` (for technical specs)
- **Analysis Documents:** `[Topic]_Analysis.md`
- **Master Guides:** `[Topic]_Master_Guide.md`

### File Naming Convention

**Standard Format:** `Feature_[FeatureName]_v[Version].md`

**Examples:**
- `Feature_Contribution_v1.0.md`
- `Feature_ReviewsAndMonitoring_v1.0.md`
- `Feature_VersionCopyForward_v2.1.md`
- `Feature_CommonData_v1.0.md`

**Rules:**
- Always start with `Feature_` prefix
- Use PascalCase for multi-word feature names (no spaces)
- Always include version number: `_v[Major].[Minor].md`
- No spaces in filenames
- No special characters except underscore and period
- Version format: `v1.0`, `v1.1`, `v2.0`, etc.

**Legacy Format (Deprecated):** `[FeatureName]_Feature_Design.md`
- Old format still exists in codebase
- New documents should use standard format
- Rename legacy documents during next major update

### Version Control

**Version Numbers:**
- Format: `Major.Minor` (e.g., 1.0, 1.1, 2.0)
- Major: Significant changes, new phases
- Minor: Updates, clarifications, corrections

**Status Values:**
- `Design Phase` - Initial design, not approved
- `Approved` - Design approved, ready for development
- `In Development` - Implementation in progress
- `Implemented` - Feature complete and deployed
- `Deprecated` - No longer in use, superseded

**Change Tracking:**
- Update version and date in header
- Add change log in appendix if major changes
- Commit to git with descriptive message

---

## Templates

### Quick Start Template

```markdown
# [Feature Name] Feature Design
**[One-line description]**

**Date:** [Today's Date]
**Version:** 1.0
**Status:** Design Phase

---

## Table of Contents
[Standard TOC]

---

## Executive Summary

### Purpose
[What problem does this solve?]

### Business Value
- **[Benefit 1]**: [Description]
- **[Benefit 2]**: [Description]

### Key Stakeholders
- **Primary Users**: [Who]
- **Systems**: [Which systems]

## Business Design

### Feature Overview
[2-3 paragraphs describing the feature]

### Feature Catalog

| # | Feature | Description | MVP | LGP | COM | PRM | PWPM |
|---|---------|-------------|-----|-----|-----|-----|------|
| F001 | [Name] | [Description] | ✅ | ✅ | ✅ | ✅ | ✅ |

### System Applicability

#### LGP (Local Government Portal)
- **Use Case**: [Use case]
- **Key Features**: F001-F010
- **Volume**: [Expected usage]

## Technical Design

### Data Model

#### Object: [ObjectName]__c

| Field Name | Type | Description | Required | Default |
|------------|------|-------------|----------|---------|
| Name | Auto Number | [Format] | Yes | Auto |

## Implementation Plan

### Phase 1: MVP (Weeks 1-4)

**Week 1:** [Focus]
- [Task]

### Success Criteria
- [ ] [Criterion]

---

**End of Document**
```

### Feature Catalog Only Template

For features that only need a catalog (like Reviews & Monitoring):

```markdown
# Feature Catalog - [Feature Name]

**Document:** [Feature Name] - Salesforce Implementation
**Date:** [Date]
**Version:** 1.0
**Status:** Design Phase

## Feature Catalog Overview
[Brief description]

## Complete Feature Catalog

| # | Feature | Description | MVP | LGP | COM | PRM | PWPM |
|---|---------|-------------|-----|-----|-----|-----|------|
| F001 | [Name] | [Description] | ✅ | ✅ | ✅ | ✅ | ✅ |

## Legend
✅ MVP (Phase 1)
🔄 Phase 2 Enhancement
❌ Not Applicable

## Feature Categories
[Group features by category]

## Summary
- Total Features: [X]
- MVP Features: [Y]
- Phase 2 Features: [Z]
```

### Data Model Feature Template

For data model and integration documentation:

```markdown
# [Feature Name] Feature Documentation
**[One-line description]**

**Feature Name:** [Name]
**Version:** 1.0
**Date:** [Today's Date]
**Status:** Active

---

## Overview
[Description of common data and integration needs]

---

## Data Lineage Summary

### Source Systems
1. **[System Name]** - [Description]

### Integration Flows
[Mermaid diagram]

---

## Worksheet Definitions

### WS01: [Name]
**Filename:** `WS01_[Name].csv`
**Status:** ✅ Complete
**Records:** [Count]
**Purpose:** [Description]

---

## Common Data Lineage Details

### 1. [Data Domain]
**Full Lineage:** `[Source] → [Target]`

**Process Flow:**
1. **[System]** - [Description]

**Objects Affected:**
- `[Object__c]`

**Integration Method:** [Method]
**Data Owner:** [Owner]
**Sync Frequency:** [Frequency]

---

## Integration Architecture

### Integration Patterns Diagram
[Mermaid sequence diagram showing 4 patterns]

---

## Section 508 Accessibility Compliance
[Compliance checklist]

---

**Document Owner:** [Team]
**Last Updated:** [Date]
**Section 508 Compliance:** ✅ Verified [Date]
```

---

## Common Mistakes to Avoid

### Content Mistakes

❌ **Too Technical Too Soon**
- Don't start with data model
- Lead with business value
- Save technical details for later sections

❌ **Missing Feature IDs**
- Every feature needs an ID (F001, F002...)
- Reference features by ID in other sections

❌ **Inconsistent Terminology**
- Pick one term and stick with it
- Create a glossary if needed
- Don't mix "user" and "reviewer" for same role

❌ **Vague Requirements**
- "System should be fast" → "Page load < 2 seconds"
- "Easy to use" → "3 clicks to complete task"
- "Lots of data" → "Support 10,000+ records"

### Formatting Mistakes

❌ **Broken Links**
- Test all anchor links in TOC
- Use lowercase with hyphens: `#executive-summary`

❌ **Inconsistent Tables**
- Always include header row
- Align columns
- Use consistent column order

❌ **Poor ASCII Art**
- Test rendering in preview
- Keep under 80 characters wide
- Use proper box-drawing characters

### Process Mistakes

❌ **No Version Control**
- Always commit to git
- Update version number when changing
- Track major changes

❌ **Stale Documents**
- Update when requirements change
- Mark deprecated features
- Archive old versions

---

## Examples and References

### Example Documents

**Location:** `c:\projects\POCs\src\dmedev5\docs\Features\`

**Good Examples - User-Facing Features:**
- `Contribution/Feature_Contribution_v1.0.md`
  - Complete business-first structure
  - Comprehensive feature catalog (27 features)
  - Clear user journeys
  - Detailed data model

- `VersionCopyForward/` (multiple documents)
  - Phased implementation approach
  - Clear status tracking
  - Good use of diagrams

**Good Examples - Data/Integration Features:**
- `Data_Model/Feature_CommonData_v1.0.md`
  - Complete data lineage documentation
  - 12 worksheets with field inventory (12,043 fields)
  - Integration architecture with 4 patterns
  - Section 508 compliant diagrams
  - Comprehensive source system mappings

### Reference Materials

**Internal:**
- Feature documents in `docs/Features/`
- Architecture docs in `docs/Architecture/`
- Analysis reports in `docs/Analysis/`

**External:**
- Salesforce Developer Documentation
- UX/UI Design Systems
- Agile User Story formats

---

## Quick Reference Checklist

### Before You Start
- [ ] Confirm feature needs full document (not just ADO story)
- [ ] Identify primary stakeholders
- [ ] Gather business requirements
- [ ] Review similar features for patterns

### During Writing
- [ ] Follow standard template structure
- [ ] Create feature catalog with IDs
- [ ] Write business sections first
- [ ] Add technical details last
- [ ] Include diagrams where helpful
- [ ] Test all markdown formatting

### Before Publishing
- [ ] Spell check and grammar check
- [ ] Test all TOC links
- [ ] Verify table formatting
- [ ] Review with stakeholders
- [ ] Commit to git with clear message
- [ ] Update version and date

### After Implementation
- [ ] Update status to "Implemented"
- [ ] Document any deviations from design
- [ ] Archive superseded versions
- [ ] Link to implementation code/components

---

## Maintenance and Updates

### When to Update

**Always Update For:**
- Requirement changes
- Scope additions/removals
- Technical approach changes
- Implementation deviations

**Consider Updating For:**
- Minor clarifications
- Formatting improvements
- Additional examples
- New references

### Update Process

1. **Make Changes**
   - Edit document
   - Update version number
   - Update date

2. **Track Changes**
   - Add change log entry (for major changes)
   - Commit to git with descriptive message

3. **Notify Stakeholders**
   - Email key stakeholders
   - Update ADO work items
   - Announce in team meetings

### Archiving

**When to Archive:**
- Feature fully implemented and stable
- Feature deprecated/replaced
- Document superseded by new version

**How to Archive:**
- Move to `docs/Archive/Features/`
- Add "ARCHIVED" to filename
- Update status to "Deprecated"
- Add link to replacement document

---

## Success Metrics

### Document Quality Indicators

**Good Feature Document:**
- ✅ Stakeholders can understand business value
- ✅ Developers can implement from technical specs
- ✅ QA can create test cases from requirements
- ✅ All features have unique IDs
- ✅ MVP vs Phase 2 clearly defined
- ✅ Success criteria measurable

**Needs Improvement:**
- ⚠️ Missing sections from template
- ⚠️ Vague or ambiguous requirements
- ⚠️ No feature catalog or IDs
- ⚠️ Technical jargon in business sections
- ⚠️ Broken links or formatting
- ⚠️ No implementation plan

### Usage Metrics

**Track:**
- Number of clarification questions (fewer is better)
- Implementation deviations (fewer is better)
- Stakeholder approval time (faster is better)
- Developer reference frequency (higher is better)

---

**End of Master Guide**

---

## Document History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-02-26 | Initial creation | Cascade AI |
