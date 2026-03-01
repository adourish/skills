#!/usr/bin/env python3
"""
Daily Planner - Wrapper Script
This script calls the tools implementation to avoid code duplication.

The actual implementation is in: G:\\My Drive\\06_Skills\\_tools\\run_process_new.py
"""

import sys
import os
from pathlib import Path

# Add _tools to path
tools_path = Path(__file__).parent.parent / "_tools"
sys.path.insert(0, str(tools_path))

# Import and run the tools implementation
from run_process_new import main
import asyncio

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  Daily Planner - Process New Workflow")
    print("=" * 70)
    print("\n⚠️  NOTE: This is a WRAPPER script that calls the tools.")
    print("    For direct access, use:")
    print("    cd \"G:\\My Drive\\06_Skills\\_tools\"")
    print("    python run_process_new.py")
    print("\n" + "=" * 70 + "\n")
    asyncio.run(main())
