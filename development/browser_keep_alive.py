#!/usr/bin/env python3
"""
Browser Keep Alive Skill

Opens a browser using Playwright MCP and keeps it open for manual user interaction.
Useful for scenarios where login verification or manual steps are required.

Usage:
    When you need to open a browser for testing but require manual login/verification:
    1. Use mcp1_browser_navigate to open the target URL
    2. DO NOT call mcp1_browser_close
    3. Leave browser open for user to complete manual steps
    4. User will report back with findings

Common Use Cases:
    - Salesforce login with email verification
    - Testing web applications that require authentication
    - Manual QA testing of deployed components
    - Debugging UI issues that require user interaction

Pattern:
    ✅ CORRECT:
    1. mcp1_browser_navigate(url)
    2. Tell user: "Browser is open at [URL]. Please complete login and report back."
    3. Wait for user feedback
    4. Fix issues based on user report
    
    ❌ INCORRECT:
    1. mcp1_browser_navigate(url)
    2. mcp1_browser_close()  # Don't do this!
    3. User can't interact with closed browser

Key Rules:
    - NEVER call mcp1_browser_close after opening for user interaction
    - Always inform user the browser is open and waiting
    - Let user complete manual steps (login, verification, etc.)
    - Wait for user to report errors or findings
    - Only close browser when user explicitly requests it

Example Workflow:
    User: "Test the Reviews and Monitoring page"
    AI: 
        1. mcp1_browser_navigate("https://org.salesforce.com/page")
        2. "Browser is open. Please log in and complete verification."
        3. "Let me know what errors you see."
    User: "I see error X in console"
    AI: Fixes error X and deploys
    
Related Skills:
    - salesforce_deployment.py (for deploying fixes)
    - break_cache.py (for cache invalidation after deployment)
    - console_debugging.py (for analyzing browser errors)

Author: Cascade AI
Date: 2026-03-03
Version: 1.0
"""

# This is a pattern/skill file, not executable code
# It documents the correct approach for browser automation with manual interaction

def open_browser_for_manual_testing(url: str) -> dict:
    """
    Opens browser and keeps it alive for manual user interaction.
    
    Args:
        url: The URL to navigate to
        
    Returns:
        dict with status and instructions for user
        
    Example:
        result = open_browser_for_manual_testing(
            "https://hrsa-dcpaas--dmedev5.sandbox.lightning.force.com/lightning/n/Reviews_and_Monitoring"
        )
    """
    return {
        "status": "browser_open",
        "action": "mcp1_browser_navigate",
        "url": url,
        "next_steps": [
            "Browser is now open at the target URL",
            "User should complete any required login/verification",
            "User should test the functionality",
            "User should report any errors or issues",
            "AI will fix reported issues and redeploy"
        ],
        "do_not": [
            "Do NOT call mcp1_browser_close",
            "Do NOT try to automate login if verification is required",
            "Do NOT assume success without user confirmation"
        ]
    }


# Skill Metadata
SKILL_METADATA = {
    "name": "Browser Keep Alive",
    "category": "development",
    "tags": ["browser", "testing", "manual", "playwright", "debugging"],
    "difficulty": "beginner",
    "prerequisites": ["mcp-playwright server configured"],
    "related_skills": [
        "salesforce_deployment",
        "break_cache",
        "console_debugging"
    ]
}
