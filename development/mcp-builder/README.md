# MCP Server Development Guide

Comprehensive guide for building Model Context Protocol (MCP) servers that enable LLMs to interact with external services.

---

## Overview

This skill provides a structured workflow for creating high-quality MCP servers. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks.

---

## What You'll Learn

- **Phase 1:** Deep research and planning
- **Phase 2:** Implementation with best practices
- **Phase 3:** Review and testing
- **Phase 4:** Create evaluations

---

## Quick Reference

| Phase | Focus | Key Activities |
|-------|-------|----------------|
| **1. Research** | Understanding requirements | API research, capability mapping, tool design |
| **2. Implementation** | Building the server | Code structure, error handling, documentation |
| **3. Review** | Quality assurance | Testing, edge cases, error scenarios |
| **4. Evaluation** | Validation | Create test cases, measure success |

---

## Use Cases

### When to Build an MCP Server

- **API Integration:** Connect LLMs to external services (Gmail, Todoist, Calendar)
- **Data Access:** Provide LLMs access to databases or file systems
- **Tool Extension:** Add new capabilities to AI assistants
- **Workflow Automation:** Enable complex multi-step processes

### Examples from Your Workflow

- ✅ **MCP Daily Planning System** - Already using MCP for email/calendar/tasks
- 💡 **Custom Integrations** - Build MCP servers for new services
- 💡 **File Processing** - MCP server for document operations
- 💡 **Media Management** - MCP server for media filing automation

---

## Integration with Skills Folder

**Location:** `G:\My Drive\06_Skills\development\mcp-builder\`

**Related Skills:**
- **Document Processing** (`documentation/document-processing/`) - Could build MCP servers for these
- **Diagram Tools** (`documentation/diagram-tools/`) - MCP server for diagram generation
- **File Organization** (`automation/skill_file_organization.md`) - MCP server for PARA filing

---

## Prerequisites

- Understanding of the service/API you want to integrate
- Python or TypeScript knowledge
- Familiarity with MCP concepts
- Testing environment

---

## Best Practices

1. **Start with Research** - Understand the API thoroughly before coding
2. **Design Tools Carefully** - Each tool should have a clear, single purpose
3. **Handle Errors Gracefully** - Provide helpful error messages
4. **Document Everything** - Clear documentation helps LLMs use your server
5. **Test Thoroughly** - Test edge cases and error scenarios
6. **Create Evaluations** - Measure success with concrete test cases

---

## Resources

**Full Guide:** See `SKILL.md` for complete development workflow

**MCP Documentation:**
- [MCP Specification](https://modelcontextprotocol.io/docs)
- [Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)

**Your MCP Implementation:**
- `C:\Users\sol90\CascadeProjects\mcptools\` - Your MCP Daily Planning System

---

## Changelog

- **2026-03-01:** Added MCP Builder skill from Anthropic repository

---

**Source:** https://github.com/anthropics/skills/tree/main/skills/mcp-builder  
**License:** See LICENSE.txt in skill folder
