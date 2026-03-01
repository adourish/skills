#!/usr/bin/env python3
"""Update existing Todoist task with Kings Manor account number"""

import requests
import json

# Load Todoist token from environments.json
env_path = r'G:\My Drive\03_Areas\Keys\Environments\environments.json'
with open(env_path, 'r') as f:
    env_data = json.load(f)
    todoist_token = env_data['environments']['todoist']['credentials']['apiToken']

headers = {'Authorization': f'Bearer {todoist_token}'}

# First, get all tasks to find the Kings Manor HOE task
response = requests.get('https://api.todoist.com/api/v1/tasks', headers=headers)
tasks = response.json()
tasks = tasks.get('results', []) if isinstance(tasks, dict) else tasks

# Find the Kings Manor task
kings_manor_task = None
for task in tasks:
    if 'Kings Manor HOE' in task.get('content', ''):
        kings_manor_task = task
        break

if kings_manor_task:
    print(f"Found task: {kings_manor_task['content']}")
    print(f"Task ID: {kings_manor_task['id']}")
    
    # Update the task with account number
    updated_description = '''Kings Manor HOE Account Setup

Account Number: 958-9548

Contact: Kristen Christensen (kchristensen@scs-management.com, 703-230-8617)
Payment: Use Townsq app for online payment
Note: Outstanding balance for 1st Quarter dues

Action: Set up account and pay outstanding balance using account number 958-9548.'''
    
    update_data = {
        'description': updated_description
    }
    
    update_response = requests.post(
        f'https://api.todoist.com/api/v1/tasks/{kings_manor_task["id"]}',
        headers=headers,
        json=update_data
    )
    
    if update_response.status_code in [200, 204]:
        print(f"\n✅ Task updated successfully!")
        print(f"   Account Number: 958-9548")
        print(f"   Contact: Kristen Christensen")
        print(f"   Payment Method: Townsq app")
    else:
        print(f"\n❌ Failed to update task: {update_response.status_code}")
        print(f"   Response: {update_response.text}")
else:
    print("❌ Kings Manor HOE task not found in Todoist")
    print("   Creating new task with account number...")
    
    # Create new task with account number
    task_data = {
        'content': 'Setup Kings Manor HOE account - Account #958-9548',
        'description': '''Kings Manor HOE Account Setup

Account Number: 958-9548

Contact: Kristen Christensen (kchristensen@scs-management.com, 703-230-8617)
Payment: Use Townsq app for online payment
Note: Outstanding balance for 1st Quarter dues

Action: Set up account and pay outstanding balance using account number 958-9548.''',
        'priority': 3
    }
    
    create_response = requests.post(
        'https://api.todoist.com/api/v1/tasks',
        headers=headers,
        json=task_data
    )
    
    if create_response.status_code in [200, 201]:
        task = create_response.json()
        print(f"\n✅ New task created successfully!")
        print(f"   Title: {task['content']}")
        print(f"   Account Number: 958-9548")
        print(f"   Task ID: {task['id']}")
    else:
        print(f"\n❌ Failed to create task: {create_response.status_code}")
        print(f"   Response: {create_response.text}")
