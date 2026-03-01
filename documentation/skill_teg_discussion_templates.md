# TEG Discussion Templates Master Guide

**Last Updated:** February 3, 2026  
**Purpose:** Comprehensive guide for preparing and conducting Technical Engineering Group (TEG) discussion sessions  
**Source Document:** `c:\projects\POCs\src\dmedev5\docs\teg discussion template.md`

---

## Table of Contents

1. [Overview](#overview)
2. [TEG Session Types](#teg-session-types)
3. [Scheduling Process](#scheduling-process)
4. [Discussion Categories](#discussion-categories)
5. [Category Templates](#category-templates)
6. [Best Practices](#best-practices)
7. [Common Pitfalls](#common-pitfalls)
8. [Quick Reference](#quick-reference)

---

## Overview

### What is TEG?

The Technical Engineering Group (TEG) provides a structured forum for:
- Design reviews and feedback
- Brainstorming technical solutions
- Knowledge sharing and SME discussions
- ROM (Rough Order of Magnitude) preparation
- Architecture and design validation

### Session Format Types

1. **Time-boxed Brainstorming** (up to 30 minutes)
   - Flush out designs or processes
   - Generate design alternatives
   - Identify gaps in designs
   - Get early feedback

2. **Discussion and Feedback Session** (standard duration)
   - Detailed design reviews
   - ROM presentations
   - Knowledge sharing
   - Architecture presentations

### Key Information

- **Schedule:** Tuesdays or Thursdays, 2:30 - 4:00 PM
- **Contact:** DL_HS_HRSA_EntArchitecture@reisystems.com
- **SharePoint:** HEAT SharePoint (for one-pager uploads)
- **Tracking:** Azure DevOps TEG board

---

## TEG Session Types

### Brainstorming Sessions

**Duration:** 30 minutes (strictly time-boxed)

**Purpose:**
- Flush out design or process
- Get ideas for design alternatives
- Brainstorm solutions
- Identify design gaps

**Key Rules:**
- Session will be cut off at 30 minutes
- Can be rescheduled for next available slot
- Requires preparation upfront
- TEG team moderates to ensure everyone participates

### Discussion Sessions

**Duration:** Standard TEG time slot

**Purpose:**
- Detailed design reviews
- ROM presentations
- Knowledge sharing
- Architecture validation
- Decision analysis

---

## Scheduling Process

### Step-by-Step Guide

1. **Select Discussion Category**
   - Choose from 11 available categories (see below)
   - Determine if brainstorming or discussion format

2. **Prepare One-Pager Document**
   - Use appropriate category template
   - Include all required sections
   - Add reference materials and links

3. **Upload to SharePoint**
   - Upload one-pager to TEG SharePoint
   - Ensure document is accessible to team

4. **Create ADO Work Items**
   - Create backlog item in TEG Azure DevOps board
   - Create associated task
   - Add one-pager link to "One Page Link" field
   - Populate "Tentative Completion Date" field

5. **Automated Notification**
   - System sends automated email on session day
   - Email includes topic details

### Prerequisites

- Access to HEAT SharePoint
- Access to TEG Azure DevOps board
- Completed one-pager document
- Reference materials ready

---

## Discussion Categories

### 1. Brainstorming Session(s)
**Format:** Brainstorming & Q/A  
**Duration:** 30 minutes (time-boxed)  
**Use For:** Design alternatives, gap identification, early-stage ideation

### 2. KT/Questions and Answer Session/SME Discussion
**Format:** SME Inputs & Q/A  
**Use For:** Getting SME knowledge, answering specific questions, knowledge transfer

### 3. Analysis and Design for ROM Preparation
**Format:** Discussion and feedback  
**Use For:** ROM approach review, cost estimation preparation

### 4. Knowledge Sharing
**Format:** Discussion and feedback  
**Use For:** Sharing knowledge, lessons learned, best practices

### 5. Analysis of Alternatives (AoA) / Decision Analysis and Resolution (DAR)
**Format:** Discussion and feedback  
**Use For:** Comparing design alternatives, decision-making support

### 6. Design Approach
**Format:** Discussion and feedback  
**Use For:** High-level design review, approach validation

### 7. Detailed Design Presentation / OIT Presentation Review
**Format:** Discussion and feedback  
**Use For:** Comprehensive design reviews, client presentation preparation

### 8. Initial Kick-Off for New Task Order
**Format:** Discussion and feedback  
**Use For:** New project initiation, scope alignment

### 9. Demo of New Tool or Software
**Format:** Discussion and feedback  
**Use For:** Demonstrating tool functionality, use case validation

### 10. Knowledge Sharing of New Tool or Software
**Format:** Discussion and feedback  
**Use For:** Architecture/technology deep-dive, tool evaluation

### 11. Idea Backlog: Technical Approach or Design Alternatives
**Format:** Discussion and feedback  
**Use For:** Idea validation, technical feasibility assessment

---

## Category Templates

### Category 1: Brainstorming Session(s)

#### Required Sections

**Problem Statement**
- Clearly define the problem to be addressed
- Examples:
  - "Brainstorming multiple design approaches for [project/release]"
  - "Brainstorming Topic XYZ"

**Outcome Expectation**
- What you want to achieve:
  - Flush out one or more design options
  - Clean up design document for client review
  - Get early feedback for future TEG session

**Overview of Topic and Options**
- Current understanding of subject matter
- Any previous brainstorming outcomes/decisions
- Design options being considered

**Reference Materials**
- Links to REI or HRSA documentation
- External documents or websites
- Relevant background materials

**Sections to Complete During Session**
Choose relevant sections:
- Design considerations
- Impacted systems (solutions, subsystems, modules, ETLs, pipelines, reports, data marts, environments)
- Downstream/upstream impacts
- Testing requirements
- Constraints
- Risks
- Problem statement refinement
- Design details and flow diagrams

---

### Category 2: KT/Q&A Session/SME Discussion

#### Required Sections

**Outcome Expectation**
- Getting answers to specific questions
- Knowledge transfer objectives

**Questions/Topics**
- Document all questions clearly
- Organize by topic area
- Prioritize questions

**Recap**
- Document KT details received
- Action items from discussion

**Reference Materials**
- Links to REI or HRSA documentation
- External documents or websites
- Background materials for SME review

#### Special Notes
- Work with TEG Scrum Master for scheduling
- Allows SME to prepare materials in advance
- May require follow-up meetings with SMEs

---

### Category 3: ROM Preparation (Analysis and Design)

**Template File:** TEG ROM Template V1.3.xlsx

#### Required Sections

**ROM Title**
- Clear, descriptive title

**Outcome Expectation**
- Review the ROM approach

**Background & Requirements**
- Exact requirements from client (verbatim)

**Understanding of Requirements** *(Client-facing section)*
- Understanding of scope (high-level)
- List of business/technical uses to be supported

**Assumptions** *(Client-facing section)*
- Assumptions for each requirement
- Known limitations
- Dependencies

**Design Considerations**
- Technical constraints
- Design trade-offs

**Design Details** *(Client-facing section)*
- Bullet points or high-level summary per requirement
- High-level approach to implement
- Flow diagrams (if applicable)
- Multiple options with pros/cons (if applicable)

**Impacted Systems**
- Solutions, subsystems, modules affected
- ETLs, pipelines, reports, data marts
- Environments or systems
- Downstream/upstream impacts
- Testing requirements

**Constraints / Risks**
- Technical constraints
- Project risks

**Adoption Plan** *(if applicable)*
- Rollout strategy
- Change management considerations

**ROMs (Bottom's up Excel Link)** *(Optional)*
- Link to detailed cost breakdown

---

### Category 4: Knowledge Sharing

#### Required Sections

**Problem Statement**
- Context for knowledge sharing

**Outcome Expectation**
- What attendees should learn
- Expected takeaways

**Requirement, Event Description, or Needs**
- Background information
- Why this knowledge is important
- How it applies to current work

---

### Category 5: Analysis of Alternatives (AoA/DAR)

#### Required Sections

**Problem Statement**
- Clear definition of decision to be made

**Outcome Expectation**
- Review alternatives at high level
- Get feedback on recommendation

**Requirement or Application Needs**
- Business/technical requirements driving decision

**Alternatives with Pros/Cons**
- Option 1: [Description]
  - Pros: [List]
  - Cons: [List]
- Option 2: [Description]
  - Pros: [List]
  - Cons: [List]
- [Additional options as needed]

**Recommendation**
- Recommended alternative
- Justification for recommendation

**Implementation Details** *(if required)*
- Details on implementing recommended alternative

---

### Category 6: Design Approach

#### Required Sections

**Problem Statement**
- What problem the design addresses

**Outcome Expectation**
- Provide feedback on the approach

**Requirement or Application Needs**
- Business/technical requirements

**Design Constraints** *(if any)*
- Technical limitations
- Business constraints

**Design Details and Flow Diagram**
- High-level design description
- Flow diagrams
- Component interactions

---

### Category 7: Detailed Design Presentation / OIT Presentation Review

#### Required Sections

**Purpose / Agenda / Background / Problem Statement**
- Context for presentation

**Design Considerations**
- Basis of software architecture

**Software Architecture / Logical Diagrams**
- Multiple slides if multiple options
- Component diagrams
- Integration points

**Error Logging & Auditing**
- Logging strategy
- Audit requirements

**Concurrency**
- Concurrent access handling
- Locking strategies

**Recommendations**
- Design recommendations
- Best practices

**Fault Tolerance**
- Error handling
- Recovery mechanisms

**Rollback Strategy** *(if phasing out existing application)*
- Migration approach
- Rollback procedures

**Tenants Management** *(if multi-tenant)*
- Tenant isolation
- Data segregation

**Authentication & Authorization**
- Users
- Roles and permissions
- Security model

**Modern Platform Services**
- List of services being used
- Cloud services
- Third-party integrations

**Data Architecture**
- Data model
- Data flow
- Data masking requirements
- Columns/fields requiring masking

**Capacity Planning**
- Hardware architecture
- Network topologies
- Farm/Server user for installation
- Server usage/load confirmation with O&M
- Server installation requirements
- Storage estimates
- Scaling requirements (horizontal/vertical)
- Load estimates
- Peak time considerations
- Ports/Security requirements

**DevOps – Automation**
- CI/CD Pipeline
- Automation testing
- New tool/licensing requirements

**Monitoring**
- Monitoring strategy
- Alerting

**Performance**
- Performance requirements
- Optimization strategies

**Assumptions / Constraints**
- Design assumptions
- Technical constraints

---

### Category 8: Initial Kick-Off for New Task Order

#### Required Sections

**Task or Line Item Order Details**
- Contract details
- Task order number

**Overview**
- Project summary
- Key objectives

**Outcome Expectation**
- Information sharing
- Feedback on activities

**High-Level Scope**
- What's included
- What's excluded

**High-Level Activities Involved**
- Major work streams
- Key deliverables

---

### Category 9: Demo of New Tool or Software

#### Required Sections

**Objective**
- Demonstrate working functionality

**Expectation**
- High-level understanding of tool/software

**Overview of Tool or Software**
- What it is
- Why it's relevant

**Demo Details**
- What will be demonstrated
- Demo script/flow

**Use Cases**
- One or more practical use cases
- How it applies to current work

---

### Category 10: Knowledge Sharing of New Tool or Software

#### Required Sections

**Objective**
- Demonstrate architecture/technology details

**Expectation**
- High-level understanding of tool/software

**Overview of Tool or Software**
- What it is
- What problem/need it satisfies

**Topic Details**
- Technical deep-dive

**Software Architecture**
- Architecture overview
- Details about each component

**Capacity Planning**
- Scalability considerations
- Resource requirements

**Authorization**
- Authorization model

**Authentication**
- Authentication mechanisms

**Scalability**
- Horizontal/vertical scaling
- Performance characteristics

**Monitoring**
- Monitoring capabilities
- Observability

**Performance**
- Performance benchmarks
- Optimization strategies

---

### Category 11: Idea Backlog (Technical Approach/Design Alternatives)

#### Required Sections

**Overview of the Idea**
- Idea details
- JIRA link

**Outcome Expectation**
- Review technical feasibility

**Is Business Viability Done?**
- Yes / No
- If yes, share background notes

**Is Any Similar Capability Exist in REI?**
- Yes / No
- If yes, share comparison/differences

**Approach Details**
- Technical approach description

**Alternatives Table** *(if applicable)*
| Alternative | Pros | Cons |
|------------|------|------|
| Option 1   | ...  | ...  |
| Option 2   | ...  | ...  |

**Recommendation**
- Recommended approach
- Justification

---

## Best Practices

### Preparation

1. **Start Early**
   - Begin one-pager preparation at least 1 week before session
   - Allows time for reference material gathering
   - Enables SME coordination if needed

2. **Be Specific**
   - Clear problem statements
   - Specific questions
   - Well-defined outcomes

3. **Include Visuals**
   - Flow diagrams
   - Architecture diagrams
   - Screenshots (if applicable)

4. **Provide Context**
   - Background information
   - Previous decisions
   - Related work

### During Session

1. **Time Management**
   - Stick to time limits (especially 30-min brainstorming)
   - Prioritize most important topics
   - Save detailed discussions for follow-ups

2. **Engagement**
   - Encourage participation from all attendees
   - Ask specific questions to SMEs
   - Take notes on feedback

3. **Focus**
   - Stay on topic
   - Defer tangential discussions
   - Capture parking lot items

### After Session

1. **Documentation**
   - Update one-pager with decisions
   - Document action items
   - Share session notes

2. **Follow-Up**
   - Schedule follow-up sessions if needed
   - Complete action items
   - Update ADO work items

3. **Communication**
   - Share outcomes with stakeholders
   - Update relevant documentation
   - Close ADO tasks

---

## Common Pitfalls

### ❌ Avoid These Mistakes

1. **Insufficient Preparation**
   - Vague problem statements
   - Missing reference materials
   - Unclear outcome expectations
   - Result: Wasted session time

2. **Wrong Session Type**
   - Using brainstorming for detailed design review
   - Using discussion session for early-stage ideation
   - Result: Mismatched expectations

3. **Missing Prerequisites**
   - No one-pager uploaded
   - ADO work item not created
   - SME not notified (for KT sessions)
   - Result: Session cancellation

4. **Poor Time Management**
   - Trying to cover too much in 30 minutes
   - Getting stuck on details in brainstorming
   - Not prioritizing topics
   - Result: Incomplete discussions

5. **Lack of Follow-Through**
   - Not documenting decisions
   - Missing action items
   - Not scheduling follow-ups
   - Result: Lost progress

### ✅ Success Factors

1. **Clear Objectives**
   - Well-defined problem statement
   - Specific outcome expectations
   - Prioritized topics

2. **Proper Format Selection**
   - Brainstorming for early-stage work
   - Discussion for detailed reviews
   - KT/Q&A for knowledge transfer

3. **Complete Documentation**
   - All template sections filled
   - Reference materials included
   - Diagrams and visuals provided

4. **Effective Facilitation**
   - TEG team moderates
   - Everyone participates
   - Time limits respected

5. **Action-Oriented Follow-Up**
   - Decisions documented
   - Action items assigned
   - Progress tracked in ADO

---

## Quick Reference

### Session Type Selection Matrix

| Your Need | Session Type | Duration | Category |
|-----------|-------------|----------|----------|
| Early-stage design ideas | Brainstorming | 30 min | Category 1 |
| Need SME answers | KT/Q&A | Standard | Category 2 |
| ROM preparation | Discussion | Standard | Category 3 |
| Share knowledge | Discussion | Standard | Category 4 |
| Compare alternatives | Discussion | Standard | Category 5 |
| High-level design review | Discussion | Standard | Category 6 |
| Detailed design review | Discussion | Standard | Category 7 |
| New project kickoff | Discussion | Standard | Category 8 |
| Tool demo | Discussion | Standard | Category 9 |
| Tool architecture review | Discussion | Standard | Category 10 |
| Idea validation | Discussion | Standard | Category 11 |

### Essential Checklist

**Before Scheduling:**
- [ ] Category selected
- [ ] One-pager completed using template
- [ ] Reference materials gathered
- [ ] Diagrams/visuals prepared
- [ ] SME identified (if needed)

**Scheduling:**
- [ ] One-pager uploaded to SharePoint
- [ ] ADO backlog item created
- [ ] ADO task created
- [ ] One-pager link added to ADO
- [ ] Tentative completion date set
- [ ] SME notified (if KT/Q&A session)

**During Session:**
- [ ] Problem statement reviewed
- [ ] Outcome expectations stated
- [ ] Key topics covered
- [ ] Feedback captured
- [ ] Decisions documented
- [ ] Action items identified

**After Session:**
- [ ] One-pager updated with decisions
- [ ] Action items assigned
- [ ] ADO work items updated
- [ ] Follow-up sessions scheduled (if needed)
- [ ] Stakeholders notified

### Contact Information

**TEG Team Email:** DL_HS_HRSA_EntArchitecture@reisystems.com

**For Questions About:**
- Scheduling: Contact TEG Scrum Master
- Process: Refer to HEAT SharePoint guide
- Technical: Email TEG team

### Key Resources

- **SharePoint:** HEAT SharePoint (one-pager storage)
- **ADO Board:** TEG Azure DevOps board
- **ROM Template:** TEG ROM Template V1.3.xlsx
- **Process Guide:** HEAT SharePoint guide me document

---

## Appendix: Template Selection Guide

### Quick Decision Tree

```
Start Here
    |
    ├─ Need to brainstorm/ideate? → Category 1 (Brainstorming)
    |
    ├─ Need SME answers? → Category 2 (KT/Q&A)
    |
    ├─ Preparing cost estimate? → Category 3 (ROM Preparation)
    |
    ├─ Sharing knowledge/lessons? → Category 4 (Knowledge Sharing)
    |
    ├─ Comparing options? → Category 5 (AoA/DAR)
    |
    ├─ High-level design review? → Category 6 (Design Approach)
    |
    ├─ Detailed design/architecture? → Category 7 (Detailed Design)
    |
    ├─ Starting new project? → Category 8 (Kick-Off)
    |
    ├─ Demonstrating tool? → Category 9 (Tool Demo)
    |
    ├─ Tool architecture review? → Category 10 (Tool Knowledge)
    |
    └─ Validating new idea? → Category 11 (Idea Backlog)
```

### Time Commitment Estimates

| Activity | Time Required |
|----------|--------------|
| One-pager preparation (simple) | 2-4 hours |
| One-pager preparation (complex) | 1-2 days |
| Reference material gathering | 1-2 hours |
| Diagram creation | 2-4 hours |
| ADO work item setup | 15 minutes |
| Session attendance | 30 min - 1.5 hours |
| Post-session documentation | 1-2 hours |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Feb 3, 2026 | Initial master guide created from TEG discussion template |

---

## Related Master Guides

- ADO_Automation_Master_Guide.md (for ADO work item creation)
- Salesforce_FLS_Automation_Master_Guide.md (for Salesforce automation patterns)

---

**End of Master Guide**
