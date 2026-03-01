# Skill Creator

Meta-skill for creating new skills in a structured, consistent way.

---

## Overview

This skill helps you create high-quality skills by providing a structured approach to skill development. It's a "skill for creating skills" - meta but practical.

---

## What is a Skill?

A skill is a reusable guide that helps AI assistants perform specific tasks consistently and effectively.

**Good Skills Have:**
- Clear purpose and scope
- Structured workflow
- Examples and use cases
- Best practices
- Quality checks

---

## When to Create a New Skill

### ✅ Create a Skill When:
- You perform a task repeatedly
- The task has a clear process
- Others could benefit from the approach
- You want consistent results
- The task is complex enough to need guidance

### ❌ Don't Create a Skill When:
- It's a one-time task
- The process is too simple (1-2 steps)
- It's too specific to one situation
- Existing skills already cover it

---

## Skill Creation Process

### 1. Define Purpose
- What problem does this skill solve?
- Who will use it?
- What's the expected outcome?

### 2. Outline Structure
- What are the main steps?
- What decisions need to be made?
- What are common pitfalls?

### 3. Add Examples
- Real-world use cases
- Before/after scenarios
- Edge cases

### 4. Document Best Practices
- What works well?
- What to avoid?
- Tips for success

### 5. Create Quality Checks
- How do you know it worked?
- What are success criteria?
- How to verify results?

---

## Skill Template

```markdown
# Skill Name

Brief description of what this skill does.

---

## Overview

Detailed explanation of the skill's purpose and value.

---

## When to Use

- ✅ Use case 1
- ✅ Use case 2
- ❌ When not to use

---

## Process

### Step 1: [Action]
Description and guidance

### Step 2: [Action]
Description and guidance

---

## Examples

### Example 1: [Scenario]
Concrete example with details

---

## Best Practices

1. Practice 1
2. Practice 2

---

## Quality Checks

- [ ] Check 1
- [ ] Check 2

---

## Resources

Links to related skills, docs, tools
```

---

## Examples from Your Skills Folder

### ✅ Well-Structured Skills You've Created:

**HOW_TO_FILE_TOOLS.md**
- Clear decision tree
- Folder-by-folder breakdown
- Multiple examples
- Best practices included

**HOW_TO_FILE_MEDIA.md**
- Comprehensive filing rules
- Privacy considerations
- Automation examples
- Clear structure

**Document Processing Skills**
- Quick reference tables
- Common use cases
- Dependencies listed
- Integration points

---

## Integration with Skills Folder

**Location:** `G:\My Drive\06_Skills\_tools\skill-creator\`

**Use This Skill To Create:**
- New automation workflows
- Integration guides
- Process documentation
- Tool usage guides

**Related Skills:**
- **Doc Co-Authoring** (`documentation/doc-coauthoring/`) - Collaborative writing process
- **HOW_TO_FILE_TOOLS** (`_tools/HOW_TO_FILE_TOOLS.md`) - Where to file new skills

---

## Skill Filing Decision

**Question:** Where should a new skill go?

**Use the decision tree:**
```
New Skill → What's its purpose?

├─ Daily automation → _tools/
├─ Utility function → _scripts/
├─ Workflow process → automation/
├─ API integration → integrations/
├─ Development guide → development/
├─ Documentation creation → documentation/
└─ System setup → system/
```

See `HOW_TO_FILE_TOOLS.md` for complete filing guide.

---

## Best Practices for Skill Creation

1. **Start with Real Needs** - Create skills for actual problems you face
2. **Keep It Focused** - One skill, one clear purpose
3. **Use Examples** - Show, don't just tell
4. **Test It** - Try using the skill yourself
5. **Iterate** - Improve based on usage
6. **Link Related Skills** - Build a connected knowledge base

---

## Quality Checklist

Before finalizing a skill, check:

- [ ] Clear purpose statement
- [ ] Structured process/workflow
- [ ] At least 2 concrete examples
- [ ] Best practices section
- [ ] Integration with existing skills
- [ ] Proper location in Skills folder
- [ ] README.md created
- [ ] Changelog started

---

## Resources

**Full Guide:** See `SKILL.md` for complete skill creation workflow

**Your Existing Skills:**
- Browse `G:\My Drive\06_Skills\` for examples
- Review successful skills for patterns
- Note what makes them effective

---

## Changelog

- **2026-03-01:** Added Skill Creator skill from Anthropic repository

---

**Source:** https://github.com/anthropics/skills/tree/main/skills/skill-creator  
**License:** See LICENSE.txt in skill folder
