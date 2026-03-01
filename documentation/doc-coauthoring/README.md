# Doc Co-Authoring Workflow

Structured workflow for collaborative document creation with AI assistance.

---

## Overview

This skill provides a 3-stage process for creating high-quality documents:
1. **Context Gathering** - Collect information and requirements
2. **Refinement & Structure** - Organize and draft content
3. **Reader Testing** - Validate clarity and completeness

---

## When to Use This Workflow

- Creating comprehensive guides (like your Skills documentation)
- Writing technical documentation
- Developing process workflows
- Building knowledge base articles
- Creating README files

---

## The 3-Stage Process

### Stage 1: Context Gathering

**Goal:** Understand what needs to be documented

**Activities:**
- Ask initial questions about purpose and audience
- Collect information dumps from user
- Identify key topics and scope
- Clarify requirements

**Example:** Creating `HOW_TO_FILE_TOOLS.md`
- What tools need filing?
- What's the folder structure?
- Who will use this guide?

---

### Stage 2: Refinement & Structure

**Goal:** Create well-organized, clear content

**Steps:**
1. **Clarifying Questions** - Fill knowledge gaps
2. **Brainstorming** - Generate ideas and approaches
3. **Curation** - Select best ideas
4. **Gap Check** - Identify missing information
5. **Drafting** - Write initial content
6. **Iterative Refinement** - Improve based on feedback

**Quality Checks:**
- Clear structure with headings
- Logical flow
- Examples and use cases
- Consistent formatting

---

### Stage 3: Reader Testing

**Goal:** Ensure document is clear and complete

**Testing Approaches:**

**Option A: Predict Reader Questions**
- Anticipate what readers will ask
- Add clarifications proactively

**Option B: Sub-Agent Testing**
- Use AI to simulate reader
- Identify confusing sections
- Test with different personas

**Exit Condition:**
- Reader can complete tasks using only the document
- No critical questions remain unanswered

---

## Use Cases in Your Workflow

### ✅ Already Used For:
- `HOW_TO_FILE_TOOLS.md` - Tool filing guide
- `HOW_TO_FILE_MEDIA.md` - Media organization guide
- `README.md` files for various skills
- MCP Daily Planning System documentation

### 💡 Future Use Cases:
- Automation workflow documentation
- Integration guides for new services
- Process documentation for file organization
- Training materials for new tools

---

## Integration with Skills Folder

**Location:** `G:\My Drive\06_Skills\documentation\doc-coauthoring\`

**Complements:**
- **Document Processing** (`documentation/document-processing/`) - Create docs in DOCX/PDF
- **Internal Comms** (`documentation/internal-comms/`) - Professional communication
- **Skill Creator** (`_tools/skill-creator/`) - Create new skill documentation

---

## Best Practices

1. **Start with Questions** - Don't assume you know everything
2. **Iterate Frequently** - Get feedback early and often
3. **Test with Real Users** - Or simulate them with AI
4. **Use Examples** - Concrete examples clarify abstract concepts
5. **Check Completeness** - Can someone use this without asking questions?

---

## Example Workflow

```
User: "I need to document our file organization system"

Stage 1 - Context Gathering:
→ What files need organizing?
→ Who will use this system?
→ What's the current structure?
→ What problems does it solve?

Stage 2 - Refinement:
→ Create folder structure diagram
→ Write decision tree
→ Add examples for each folder
→ Include best practices

Stage 3 - Testing:
→ Can a new user file a tool correctly?
→ Are edge cases covered?
→ Is the decision tree clear?
→ Add missing clarifications

Result: HOW_TO_FILE_TOOLS.md ✅
```

---

## Resources

**Full Guide:** See `SKILL.md` for complete workflow details

**Related Documentation:**
- Your existing guides in `06_Skills/`
- MCP Daily Planning System docs
- README files across projects

---

## Changelog

- **2026-03-01:** Added Doc Co-Authoring skill from Anthropic repository

---

**Source:** https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring  
**License:** See LICENSE.txt in skill folder
