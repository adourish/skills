# Devin AI Integration with Skills Repository

Complete guide for using the Skills repository with Devin, the autonomous AI software engineer.

---

## Overview

Devin is an autonomous AI software engineer that can plan, execute, and complete complex software engineering tasks. This skill covers how to effectively use the Skills repository with Devin for enhanced productivity and standardized workflows.

**Devin Capabilities:**
- Autonomous task execution
- Full development environment access
- Command-line interface
- File system operations
- Web browsing and research
- Long-running task management

---

## When to Use

- Complex multi-step development tasks
- Full-stack application development
- Automated testing and debugging
- Repository setup and configuration
- CI/CD pipeline implementation
- Documentation generation
- Code refactoring projects

---

## Prerequisites

- Devin account and access
- Skills repository cloned locally or accessible
- Understanding of your project requirements
- Clear task specifications

---

## Setup for Devin

### Step 1: Provide Repository Access

**Method 1: Direct Repository Access**

```
"Clone the skills repository:
git clone https://github.com/adourish/skills.git /workspace/skills"
```

**Method 2: Provide as Context**

```
"I have a skills repository at https://github.com/adourish/skills
Please review the README.md and SKILLS_CONTEXT.md to understand available skills"
```

---

### Step 2: Configure Devin's Workspace

```
"Set up the workspace:
1. Clone skills repo to /workspace/skills
2. Review the repository structure
3. Identify relevant skills for this task
4. Follow the skill guidelines for implementation"
```

---

## Using Skills with Devin

### Method 1: Reference Specific Skills

**Task-Based Approach:**

```
"I need to implement a daily planning workflow.
Please review the daily_planning skill at:
/workspace/skills/automation/skill_daily_planning.md

Then implement the workflow following these specifications:
- Use Python for automation
- Integrate with Todoist API
- Generate Kanban board
- Follow the skill's best practices"
```

**What Devin Does:**
1. Reads the skill documentation
2. Understands requirements and dependencies
3. Plans implementation steps
4. Executes code development
5. Tests and validates
6. Provides completion summary

---

### Method 2: Multi-Skill Workflows

**Complex Task Approach:**

```
"I need to set up a complete development workflow.
Review these skills from /workspace/skills/:
- development/skill_git_version_control.md
- development/skill_gitflow_workflow.md
- development/skill_github_pull_requests.md
- system/skill_environments_credentials.md

Then:
1. Initialize git repository with GitFlow
2. Set up environment configuration
3. Create initial project structure
4. Implement PR workflow
5. Document the setup process"
```

---

### Method 3: Skill-Based Development

**Following Skill Templates:**

```
"Build an MCP server for [service name].
Use the mcp_builder skill as a guide:
/workspace/skills/development/mcp-builder/README.md

Follow the 4-phase process:
1. Research and planning
2. Implementation
3. Review and test
4. Create evaluations

Ensure all dependencies are documented."
```

---

### Method 4: Documentation Tasks

**Using Documentation Skills:**

```
"Create comprehensive documentation for [project].
Follow the doc_coauthoring skill:
/workspace/skills/documentation/doc-coauthoring/README.md

Use the 3-stage process:
1. Context Gathering - Ask clarifying questions
2. Refinement & Structure - Create draft
3. Reader Testing - Validate clarity

Also reference internal_comms skill for changelog format."
```

---

## Devin Workflow Patterns

### Pattern 1: Autonomous Implementation

```
Task: "Implement daily planning automation"

Devin Workflow:
1. Review: /workspace/skills/automation/skill_daily_planning.md
2. Analyze: Dependencies (Todoist, Amplenote, Gmail APIs)
3. Plan: Implementation steps with milestones
4. Setup: Environment and credentials
5. Develop: Python automation script
6. Test: Validate with test data
7. Document: Usage instructions and examples
8. Deploy: Provide deployment instructions
```

---

### Pattern 2: Repository Setup

```
Task: "Set up new project following best practices"

Devin Workflow:
1. Review: skill_git_version_control.md, skill_gitflow_workflow.md
2. Initialize: Git repository with GitFlow branches
3. Configure: .gitignore, README, LICENSE
4. Setup: Development environment
5. Create: Initial project structure
6. Document: Setup instructions
7. Commit: Initial commit with proper message
8. Verify: All setup steps completed
```

---

### Pattern 3: Skill Creation

```
Task: "Create a new skill for [functionality]"

Devin Workflow:
1. Review: /workspace/skills/_tools/skill-creator/README.md
2. Review: /workspace/skills/_tools/HOW_TO_FILE_TOOLS.md
3. Determine: Appropriate category and folder
4. Create: Skill markdown following template
5. Include: All required sections (Overview, Prerequisites, Examples, etc.)
6. Add: Section 508 compliant diagrams if needed
7. Update: README.md with new skill reference
8. Test: Validate all links and examples
9. Commit: Changes with descriptive message
```

---

### Pattern 4: Code Review & Refactoring

```
Task: "Review and refactor codebase following skills guidelines"

Devin Workflow:
1. Review: Relevant development skills
2. Analyze: Current codebase structure
3. Identify: Areas for improvement
4. Plan: Refactoring strategy
5. Implement: Changes incrementally
6. Test: Ensure no regressions
7. Document: Changes and rationale
8. Create: Pull request with detailed description
```

---

## Best Practices for Devin

### 1. Provide Clear Context

```
✅ Good:
"Review the skills repository structure at /workspace/skills/
Focus on automation skills for daily workflow implementation.
Follow the daily_planning skill guidelines."

❌ Bad:
"Do something with the skills repo"
```

### 2. Reference Specific Skills

```
✅ Good:
"Use /workspace/skills/development/skill_github_pull_requests.md
as a guide for implementing the PR workflow"

❌ Bad:
"Look at some GitHub skill"
```

### 3. Break Down Complex Tasks

```
✅ Good:
"Phase 1: Review mcp_builder skill and plan architecture
Phase 2: Implement core MCP server functionality
Phase 3: Add tests and documentation
Phase 4: Create deployment guide"

❌ Bad:
"Build an MCP server"
```

### 4. Specify Quality Standards

```
✅ Good:
"Follow Section 508 compliance guidelines from:
/workspace/skills/system/skill_section_508_compliance.md
Ensure all diagrams have 4.5:1 contrast ratio"

❌ Bad:
"Make it accessible"
```

### 5. Request Validation

```
✅ Good:
"After implementation:
1. Run all tests
2. Validate against skill requirements
3. Check for security issues
4. Verify documentation completeness
5. Provide summary of changes"

❌ Bad:
"Just finish it"
```

---

## Common Devin Tasks with Skills

### Task 1: Setup Development Environment

```
"Set up a complete development environment for [project].

Reference these skills:
- /workspace/skills/system/skill_environments_credentials.md
- /workspace/skills/development/skill_git_version_control.md
- /workspace/skills/system/skill_mcp_server_setup.md

Steps:
1. Create environments.json with API credentials template
2. Initialize git repository
3. Set up MCP server configuration
4. Create project structure following PARA method
5. Document setup process
6. Provide verification checklist"
```

---

### Task 2: Implement Automation Workflow

```
"Implement email processing automation.

Review and follow:
/workspace/skills/automation/skill_email_processing.md

Requirements:
- Python implementation
- Gmail API integration
- Extract tasks and events
- Generate summary report
- Error handling and logging
- Unit tests
- Usage documentation

Ensure code follows skill's best practices."
```

---

### Task 3: Create Documentation

```
"Create comprehensive project documentation.

Use these skills as guides:
- /workspace/skills/documentation/doc-coauthoring/README.md
- /workspace/skills/documentation/internal-comms/README.md
- /workspace/skills/documentation/skill_feature_documentation.md

Include:
- Project overview
- Setup instructions
- API documentation
- Usage examples
- Troubleshooting guide
- Changelog
- Contributing guidelines"
```

---

### Task 4: Build MCP Server

```
"Build an MCP server for [service].

Follow the complete guide:
/workspace/skills/development/mcp-builder/README.md
/workspace/skills/development/mcp-builder/SKILL.md

Implement all 4 phases:
1. Research: API documentation, authentication, rate limits
2. Implementation: Server code, tools, resources
3. Review: Testing, error handling, documentation
4. Evaluations: Create test suite and examples

Deliverables:
- Working MCP server
- Configuration file
- README with setup instructions
- Example usage
- Test suite"
```

---

## Devin-Specific Features

### Autonomous Planning

Devin can autonomously plan multi-step tasks:

```
"Review all automation skills in /workspace/skills/automation/
Then create a comprehensive automation suite that:
1. Processes emails daily
2. Organizes files using PARA method
3. Generates daily planning board
4. Integrates with Todoist and Amplenote

Plan the architecture, implement all components, test thoroughly,
and provide complete documentation."
```

### Long-Running Tasks

Devin can handle extended tasks:

```
"This is a multi-day project to refactor the entire codebase.

Day 1: Review all development skills and create refactoring plan
Day 2-3: Implement refactoring following GitFlow workflow
Day 4: Testing and validation
Day 5: Documentation and PR creation

Work autonomously and provide daily progress updates."
```

### Research and Learning

Devin can research and learn:

```
"Research best practices for [technology].
Compare with guidelines in relevant skills from /workspace/skills/
Create a comprehensive implementation guide that combines
industry best practices with our skill standards."
```

---

## Integration with Other Tools

### With GitHub

```
"Set up GitHub integration following:
/workspace/skills/development/skill_github_pull_requests.md

1. Fork repository
2. Create feature branch
3. Implement changes
4. Create pull request with detailed description
5. Respond to code review feedback"
```

### With CI/CD

```
"Set up CI/CD pipeline.
Reference automation skills for workflow patterns.
Implement:
- Automated testing
- Code quality checks
- Deployment automation
- Monitoring and alerts"
```

### With Documentation Tools

```
"Generate documentation using:
/workspace/skills/documentation/document-processing/

Create:
- Word documents with python-docx
- PowerPoint presentations
- PDF reports
- Excel spreadsheets with data"
```

---

## Troubleshooting

### Issue: Devin Can't Access Skills Repository

**Solution:**
```
"Clone the repository first:
git clone https://github.com/adourish/skills.git /workspace/skills

Then verify access:
ls -la /workspace/skills/
cat /workspace/skills/README.md"
```

### Issue: Unclear Task Requirements

**Solution:**
```
"Before starting, please:
1. Review the relevant skill documentation
2. Ask clarifying questions about requirements
3. Propose an implementation plan
4. Wait for approval before proceeding"
```

### Issue: Devin Deviates from Skill Guidelines

**Solution:**
```
"Stop. Review the skill guidelines again:
/workspace/skills/[category]/[skill].md

Ensure your implementation follows:
- Prerequisites listed in the skill
- Step-by-step process
- Best practices section
- Quality standards

Revise your approach to align with the skill."
```

---

## Quick Reference

### Loading Skills in Devin

```bash
# Clone repository
git clone https://github.com/adourish/skills.git /workspace/skills

# Reference specific skill
cat /workspace/skills/automation/skill_daily_planning.md

# List all skills in category
ls -la /workspace/skills/automation/

# Search for specific skill
find /workspace/skills -name "*github*"
```

### Common Commands

```bash
# Review skill structure
tree /workspace/skills -L 2

# Read skill content
cat /workspace/skills/[category]/[skill].md

# Search skills for keyword
grep -r "keyword" /workspace/skills/

# Update skills repository
cd /workspace/skills && git pull origin main
```

### Task Templates

**Simple Task:**
```
"Review [skill] and implement [feature] following the guidelines"
```

**Complex Task:**
```
"Multi-phase project:
1. Review skills: [list]
2. Plan: [requirements]
3. Implement: [specifications]
4. Test: [criteria]
5. Document: [deliverables]"
```

**Autonomous Task:**
```
"Complete project autonomously:
- Review all relevant skills
- Plan implementation
- Execute with best practices
- Test thoroughly
- Document completely
- Provide summary"
```

---

## Related Skills

- **[skill_creator](_tools/skill-creator/README.md)** - Creating new skills
- **[git_version_control](development/skill_git_version_control.md)** - Git workflows
- **[github_pull_requests](development/skill_github_pull_requests.md)** - PR workflow
- **[mcp_builder](development/mcp-builder/README.md)** - Building MCP servers
- **[doc_coauthoring](documentation/doc-coauthoring/README.md)** - Documentation creation

---

## Changelog

- **2026-03-01:** Created Devin integration skill

---

**Location:** `G:\My Drive\06_Skills\system\skill_devin_integration.md`  
**Category:** System  
**Difficulty:** Intermediate  
**Time:** Varies by task complexity
