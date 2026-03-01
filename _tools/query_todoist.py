import asyncio
from todoist_tools import TodoistTools
from auth_manager import AuthManager
from pathlib import Path

async def query_todoist():
    auth = AuthManager(Path(r'G:\My Drive\03_Areas\Keys\Environments\environments.json'))
    todoist = TodoistTools(auth)
    
    # Get all tasks
    tasks = await todoist.get_tasks()
    
    print("\n=== TODOIST TASKS ===\n")
    
    # Filter for daily plan tasks
    daily_plan_tasks = [t for t in tasks if t.get('content', '').startswith('🎯')]
    
    if daily_plan_tasks:
        print(f"Found {len(daily_plan_tasks)} daily plan tasks:\n")
        for i, task in enumerate(daily_plan_tasks, 1):
            print(f"{i}. {task.get('content', 'No title')}")
            if task.get('description'):
                print(f"   Description: {task['description'][:200]}...")
            print()
    else:
        print("No daily plan tasks found")
    
    # Show all tasks
    print(f"\n=== ALL TASKS ({len(tasks)} total) ===\n")
    for task in tasks[:10]:
        print(f"- {task.get('content', 'No title')}")

asyncio.run(query_todoist())
