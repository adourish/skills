#!/usr/bin/env python3
"""Quick script to create a Todoist task"""

import requests
import json
import os

# Load Todoist token from environments.json
env_path = r'G:\My Drive\03_Areas\Keys\Environments\environments.json'
with open(env_path, 'r') as f:
    env_data = json.load(f)
    todoist_token = env_data['environments']['todoist']['credentials']['apiToken']

# Create task
headers = {'Authorization': f'Bearer {todoist_token}'}
task_data = {
    'content': 'Renew Vehicle Registration - 2018 Volkswagen (WSY4040)',
    'description': '''Vehicle Registration Renewal Details:

Year: 2018
Make: VOLKSWAGEN
VIN: WVWVF7AU8JW299881
Plate Number: WSY4040
Title Number: 1303935838
Garage Jurisdiction: FAIRFAX COUNTY

Action: Renew vehicle registration before expiration date.
Check DMV website or mail for renewal notice.''',
    'priority': 3  # High priority (1-4, where 4 is urgent)
}

response = requests.post(
    'https://api.todoist.com/api/v1/tasks',
    headers=headers,
    json=task_data
)

if response.status_code in [200, 201]:
    task = response.json()
    print(f"✅ Task created successfully!")
    print(f"   Title: {task['content']}")
    due_info = task.get('due')
    if due_info:
        print(f"   Due: {due_info.get('string', 'No due date')}")
    else:
        print(f"   Due: No due date")
    print(f"   Priority: {task['priority']}")
    print(f"   ID: {task['id']}")
else:
    print(f"❌ Failed to create task: {response.status_code}")
    print(f"   Response: {response.text}")
