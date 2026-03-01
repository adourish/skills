import asyncio
from amplenote_tools import AmplenoteTools
from auth_manager import AuthManager
from pathlib import Path

async def query_amplenote():
    auth = AuthManager(Path(r'G:\My Drive\03_Areas\Keys\Environments\environments.json'))
    amp = AmplenoteTools(auth)
    
    # Search for daily plan note
    notes = await amp.get_notes(tag='daily-plan')
    
    print("\n=== AMPLENOTE DAILY PLAN NOTES ===\n")
    print(f"Found {len(notes)} notes with 'daily-plan' tag\n")
    
    # Find the static daily plan
    daily_plan_note = None
    for note in notes:
        if note.get('name') == '📋 Daily Plan':
            daily_plan_note = note
            break
    
    if daily_plan_note:
        uuid = daily_plan_note['uuid']
        print(f"Daily Plan Note: {daily_plan_note.get('name')}")
        print(f"UUID: {uuid}")
        print(f"URL: https://www.amplenote.com/notes/{uuid}\n")
        
        # Get content
        content = await amp.get_note_content(uuid)
        print("=== NOTE CONTENT ===\n")
        print(content if content else "(Note appears empty)")
    else:
        print("No '📋 Daily Plan' note found")

asyncio.run(query_amplenote())
