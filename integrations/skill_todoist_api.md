# Todoist API Integration - Master Guide

## Overview

**Purpose**: Comprehensive guide for integrating with the Todoist API for task management, automation, and productivity tracking.

**Last Updated**: February 22, 2026

**API Version**: v1 (Unified API - replaces REST v2 and Sync v9)

**Success Rate**: Production-ready

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication](#authentication)
3. [API Endpoints](#api-endpoints)
4. [Tasks (Items)](#tasks-items)
5. [Projects](#projects)
6. [Sections](#sections)
7. [Comments (Notes)](#comments-notes)
8. [Labels](#labels)
9. [Filters](#filters)
10. [Due Dates and Deadlines](#due-dates-and-deadlines)
11. [Sync API](#sync-api)
12. [Webhooks](#webhooks)
13. [Python Integration](#python-integration)
14. [PowerShell Integration](#powershell-integration)
15. [Common Use Cases](#common-use-cases)
16. [Best Practices](#best-practices)
17. [Troubleshooting](#troubleshooting)
18. [Rate Limits](#rate-limits)

---

## Quick Start

### Prerequisites

- Todoist account (Free or Premium)
- API token from Todoist Settings → Integrations
- Python 3.7+ or PowerShell 5.1+

### API Token Location

Your API token: `bf17651eea9c2ce8ac6aa702172b5eef38bca8bf`

**App Name**: robdog  
**Client ID**: `916fc82138be4eb8a72077fcb05854fc`  
**Client Secret**: `0935136159bf40d89df8acc004e290ce`

**Stored in**: `G:\My Drive\03_Areas\Keys\Environments\environments.json`

**Load in PowerShell**:
```powershell
$envs = & 'G:\My Drive\03_Areas\Keys\Environments\Load-Environments.ps1'
$todoistToken = $envs.todoist.credentials.apiToken
```

**Load in Python**:
```python
import json

with open(r'G:\My Drive\03_Areas\Keys\Environments\environments.json') as f:
    config = json.load(f)
    todoist_token = config['environments']['todoist']['credentials']['apiToken']
```

---

## Authentication

### API Token Authentication

All API requests require the `Authorization` header with your Bearer token:

```bash
curl "https://api.todoist.com/api/v1/tasks" \
  -H "Authorization: Bearer bf17651eea9c2ce8ac6aa702172b5eef38bca8bf"
```

### Security Best Practices

- **NEVER** commit API tokens to source control
- Store tokens in secure locations (encrypted storage)
- Use environment variables or secure config files
- Regenerate tokens if compromised
- Use OAuth for third-party integrations

### OAuth (For Third-Party Apps)

If building an app for others:

1. Register app at: https://developer.todoist.com/appconsole.html
2. Get `client_id` and `client_secret`
3. Implement OAuth flow (see Authorization section in API docs)

---

## API Endpoints

### Base URL

```
https://api.todoist.com
```

### Important: API v1 Changes

**Todoist API v1 is the unified API** that replaced:
- ❌ REST API v2 (deprecated, returns 410)
- ❌ Sync API v9 (deprecated, returns 410)

**Key changes:**
- All endpoints use `/api/v1/` path
- Paginated responses use `results` key
- IDs are opaque strings (v2_id format)
- Lowercase endpoints only (case-sensitive)

### Core Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/api/v1/tasks` | Task management (CRUD operations) |
| `/api/v1/projects` | Project management |
| `/api/v1/sections` | Section management within projects |
| `/api/v1/comments` | Comments on tasks and projects |
| `/api/v1/labels` | Personal labels |
| `/api/v1/filters` | Custom filters |

---

## Tasks (Items)

### Get All Active Tasks

```bash
curl "https://api.todoist.com/api/v1/tasks" \
  -H "Authorization: Bearer $TOKEN"
```

**Python**:
```python
import requests

headers = {"Authorization": f"Bearer {todoist_token}"}
response = requests.get("https://api.todoist.com/api/v1/tasks", headers=headers)

# API v1 returns paginated results
data = response.json()
tasks = data.get('results', []) if isinstance(data, dict) else data
```

**PowerShell**:
```powershell
$headers = @{
    "Authorization" = "Bearer $todoistToken"
}
$tasks = Invoke-RestMethod -Uri "https://api.todoist.com/api/v1/tasks" -Headers $headers
```

### Create a Task

```bash
curl "https://api.todoist.com/api/v1/tasks" \
  -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Buy groceries",
    "due_string": "tomorrow at 12:00",
    "priority": 4,
    "labels": ["shopping"]
  }'
```

**Python**:
```python
task_data = {
    "content": "Buy groceries",
    "due_string": "tomorrow at 12:00",
    "priority": 4,
    "labels": ["shopping"]
}

response = requests.post(
    "https://api.todoist.com/api/v1/tasks",
    headers=headers,
    json=task_data
)
new_task = response.json()
```

### Update a Task

```bash
curl "https://api.todoist.com/api/v1/tasks/{task_id}" \
  -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Buy groceries and milk"}'
```

### Complete a Task

```bash
curl "https://api.todoist.com/api/v1/tasks/{task_id}/close" \
  -X POST \
  -H "Authorization: Bearer $TOKEN"
```

### Delete a Task

```bash
curl "https://api.todoist.com/api/v1/tasks/{task_id}" \
  -X DELETE \
  -H "Authorization: Bearer $TOKEN"
```

### Task Object Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | String | Unique task ID |
| `content` | String | Task content/title |
| `description` | String | Task description (markdown supported) |
| `project_id` | String | Project ID |
| `section_id` | String | Section ID (optional) |
| `parent_id` | String | Parent task ID for subtasks |
| `order` | Integer | Position in project |
| `priority` | Integer | Priority (1-4, 4=urgent) |
| `due` | Object | Due date object |
| `deadline` | Object | Deadline object |
| `labels` | Array | Label names |
| `assignee_id` | String | Assigned user ID |
| `url` | String | Task URL |
| `created_at` | String | Creation timestamp |
| `completed_at` | String | Completion timestamp |

### Priority Levels

- `1` - Normal (default)
- `2` - Medium
- `3` - High
- `4` - Urgent (p1 in UI)

---

## Projects

### Get All Projects

```bash
curl "https://api.todoist.com/api/v1/projects" \
  -H "Authorization: Bearer $TOKEN"
```

### Create a Project

```python
project_data = {
    "name": "Work Projects",
    "color": "blue",
    "is_favorite": True
}

response = requests.post(
    "https://api.todoist.com/api/v1/projects",
    headers=headers,
    json=project_data
)
```

### Project Colors

Available colors: `berry_red`, `red`, `orange`, `yellow`, `olive_green`, `lime_green`, `green`, `mint_green`, `teal`, `sky_blue`, `light_blue`, `blue`, `grape`, `violet`, `lavender`, `magenta`, `salmon`, `charcoal`, `grey`, `taupe`

### Get Project Tasks

```python
project_id = "2203306141"
tasks = requests.get(
    f"https://api.todoist.com/api/v1/tasks?project_id={project_id}",
    headers=headers
).json()
```

---

## Sections

Sections organize tasks within projects.

### Get Project Sections

```python
project_id = "2203306141"
sections = requests.get(
    f"https://api.todoist.com/api/v1/sections?project_id={project_id}",
    headers=headers
).json()
```

### Create a Section

```python
section_data = {
    "name": "In Progress",
    "project_id": "2203306141"
}

response = requests.post(
    "https://api.todoist.com/api/v1/sections",
    headers=headers,
    json=section_data
)
```

---

## Comments (Notes)

### Get Task Comments

```python
task_id = "6XR4GqQQCW6Gv9h4"
comments = requests.get(
    f"https://api.todoist.com/api/v1/comments?task_id={task_id}",
    headers=headers
).json()
```

### Add a Comment

```python
comment_data = {
    "task_id": "6XR4GqQQCW6Gv9h4",
    "content": "This is a comment with **markdown** support"
}

response = requests.post(
    "https://api.todoist.com/api/v1/comments",
    headers=headers,
    json=comment_data
)
```

### Add File Attachment

```python
comment_data = {
    "task_id": "6XR4GqQQCW6Gv9h4",
    "content": "See attached file",
    "attachment": {
        "file_name": "report.pdf",
        "file_type": "application/pdf",
        "file_url": "https://example.com/report.pdf"
    }
}
```

---

## Labels

### Get All Labels

```python
labels = requests.get(
    "https://api.todoist.com/api/v1/labels",
    headers=headers
).json()
```

### Create a Label

```python
label_data = {
    "name": "urgent",
    "color": "red"
}

response = requests.post(
    "https://api.todoist.com/api/v1/labels",
    headers=headers,
    json=label_data
)
```

### Filter Tasks by Label

```python
tasks = requests.get(
    "https://api.todoist.com/api/v1/tasks?label=urgent",
    headers=headers
).json()
```

---

## Filters

Filters are saved searches with custom queries.

### Get All Filters

```python
filters = requests.get(
    "https://api.todoist.com/api/v1/filters",
    headers=headers
).json()
```

### Create a Filter

```python
filter_data = {
    "name": "High Priority Today",
    "query": "today & p1"
}

response = requests.post(
    "https://api.todoist.com/api/v1/filters",
    headers=headers,
    json=filter_data
)
```

### Common Filter Queries

- `today` - Tasks due today
- `tomorrow` - Tasks due tomorrow
- `overdue` - Overdue tasks
- `p1` - Priority 1 (urgent) tasks
- `@label_name` - Tasks with specific label
- `#project_name` - Tasks in specific project
- `assigned to: me` - Tasks assigned to you
- `no date` - Tasks without due date

---

## Due Dates and Deadlines

### Due Date Object

```json
{
  "date": "2026-02-22",
  "timezone": null,
  "string": "tomorrow",
  "lang": "en",
  "is_recurring": false
}
```

### Date Formats

**Full-day**: `YYYY-MM-DD`
```json
{"due": {"date": "2026-02-22"}}
```

**With time (floating)**: `YYYY-MM-DDTHH:MM:SS`
```json
{"due": {"date": "2026-02-22T14:00:00"}}
```

**With timezone**: `YYYY-MM-DDTHH:MM:SSZ`
```json
{"due": {"date": "2026-02-22T14:00:00Z", "timezone": "America/New_York"}}
```

### Natural Language Dates

```python
task_data = {
    "content": "Meeting",
    "due_string": "tomorrow at 2pm"
}
```

Supported formats:
- `today`, `tomorrow`, `next week`
- `Feb 22`, `February 22, 2026`
- `every day`, `every Monday`, `every 2 weeks`
- `tomorrow at 2pm`, `next Friday at 9am`

### Recurring Tasks

```python
task_data = {
    "content": "Weekly review",
    "due_string": "every Monday at 9am"
}
```

### Deadlines

Deadlines are separate from due dates (when to start vs when to finish):

```python
task_data = {
    "content": "Project report",
    "due_string": "Feb 20",  # When to start
    "deadline": {"date": "2026-02-25"}  # When it must be done
}
```

---

## Sync API

The Sync API is optimized for batch operations and incremental sync.

### Full Sync (Initial)

```python
import requests

sync_data = {
    "sync_token": "*",
    "resource_types": '["all"]'
}

response = requests.post(
    "https://api.todoist.com/api/v1/sync",
    headers=headers,
    data=sync_data
)

result = response.json()
sync_token = result['sync_token']  # Save for incremental sync
tasks = result['items']
projects = result['projects']
```

### Incremental Sync

```python
sync_data = {
    "sync_token": sync_token,  # From previous sync
    "resource_types": '["all"]'
}

response = requests.post(
    "https://api.todoist.com/api/v1/sync",
    headers=headers,
    data=sync_data
)
```

### Batch Commands

```python
import json
import uuid

commands = [
    {
        "type": "project_add",
        "temp_id": str(uuid.uuid4()),
        "uuid": str(uuid.uuid4()),
        "args": {
            "name": "New Project",
            "color": "blue"
        }
    },
    {
        "type": "item_add",
        "temp_id": str(uuid.uuid4()),
        "uuid": str(uuid.uuid4()),
        "args": {
            "content": "First task",
            "project_id": "temp_project_id"
        }
    }
]

sync_data = {
    "commands": json.dumps(commands)
}

response = requests.post(
    "https://api.todoist.com/api/v1/sync",
    headers=headers,
    data=sync_data
)
```

### Available Commands

- `item_add`, `item_update`, `item_delete`, `item_complete`, `item_uncomplete`
- `project_add`, `project_update`, `project_delete`, `project_archive`
- `section_add`, `section_update`, `section_delete`
- `note_add`, `note_update`, `note_delete`
- `label_add`, `label_update`, `label_delete`
- `filter_add`, `filter_update`, `filter_delete`

---

## Webhooks

Webhooks send real-time notifications when events occur.

### Setup

1. Go to https://developer.todoist.com/appconsole.html
2. Register your app
3. Configure webhook URL (must be HTTPS)
4. Select events to subscribe to

### Webhook Events

- `item:added`, `item:updated`, `item:deleted`, `item:completed`, `item:uncompleted`
- `project:added`, `project:updated`, `project:deleted`, `project:archived`
- `note:added`, `note:updated`, `note:deleted`
- `section:added`, `section:updated`, `section:deleted`
- `label:added`, `label:updated`, `label:deleted`
- `reminder:fired`

### Webhook Payload

```json
{
  "event_name": "item:added",
  "user_id": "2671355",
  "event_data": {
    "id": "6XR4GqQQCW6Gv9h4",
    "content": "Buy Milk",
    "project_id": "6XR4H993xv8H5qCR",
    "priority": 1,
    "due": null
  },
  "initiator": {
    "email": "user@example.com",
    "full_name": "User Name",
    "id": "2671355"
  },
  "triggered_at": "2026-02-21T10:39:38.000000Z",
  "version": "10"
}
```

### Verify Webhook Signature

```python
import hmac
import hashlib
import base64

def verify_webhook(request_body, signature, client_secret):
    expected = base64.b64encode(
        hmac.new(
            client_secret.encode(),
            request_body.encode(),
            hashlib.sha256
        ).digest()
    ).decode()
    
    return hmac.compare_digest(expected, signature)

# In your webhook handler
signature = request.headers.get('X-Todoist-Hmac-SHA256')
is_valid = verify_webhook(request.body, signature, client_secret)
```

---

## Python Integration

### Install SDK

```bash
pip install todoist-api-python
```

### Using the SDK

```python
from todoist_api_python.api import TodoistAPI

api = TodoistAPI("bf17651eea9c2ce8ac6aa702172b5eef38bca8bf")

# Get all tasks
tasks = api.get_tasks()

# Create a task
task = api.add_task(
    content="Buy groceries",
    due_string="tomorrow at 12:00",
    priority=4
)

# Update a task
api.update_task(task_id=task.id, content="Buy groceries and milk")

# Complete a task
api.close_task(task_id=task.id)

# Get all projects
projects = api.get_projects()

# Create a project
project = api.add_project(name="Work", color="blue")
```

### Complete Example Script

```python
#!/usr/bin/env python3
"""
Todoist Task Manager
Manages tasks using the Todoist API
"""

import json
from todoist_api_python.api import TodoistAPI
from datetime import datetime, timedelta

# Load credentials
with open(r'G:\My Drive\03_Areas\Keys\Environments\environments.json') as f:
    config = json.load(f)
    token = config['environments']['todoist']['credentials']['apiToken']

# Initialize API
api = TodoistAPI(token)

def get_today_tasks():
    """Get all tasks due today"""
    tasks = api.get_tasks(filter="today")
    print(f"\n📅 Tasks due today: {len(tasks)}")
    for task in tasks:
        priority_emoji = "🔴" if task.priority == 4 else "🟡" if task.priority == 3 else "⚪"
        print(f"{priority_emoji} {task.content}")
    return tasks

def create_daily_tasks():
    """Create recurring daily tasks"""
    daily_tasks = [
        {"content": "Review emails", "due_string": "every day at 9am", "priority": 3},
        {"content": "Daily standup", "due_string": "every weekday at 10am", "priority": 4},
        {"content": "End of day review", "due_string": "every day at 5pm", "priority": 2}
    ]
    
    for task_data in daily_tasks:
        task = api.add_task(**task_data)
        print(f"✓ Created: {task.content}")

def get_overdue_tasks():
    """Get all overdue tasks"""
    tasks = api.get_tasks(filter="overdue")
    print(f"\n⚠️ Overdue tasks: {len(tasks)}")
    for task in tasks:
        print(f"  - {task.content} (due: {task.due.date if task.due else 'N/A'})")
    return tasks

def get_project_stats():
    """Get statistics for all projects"""
    projects = api.get_projects()
    print(f"\n📊 Project Statistics:")
    
    for project in projects:
        tasks = api.get_tasks(project_id=project.id)
        print(f"  {project.name}: {len(tasks)} tasks")

if __name__ == "__main__":
    print("="*60)
    print("TODOIST TASK MANAGER")
    print("="*60)
    
    get_today_tasks()
    get_overdue_tasks()
    get_project_stats()
```

---

## PowerShell Integration

### Basic REST API Calls

```powershell
# Load credentials
$envs = & 'G:\My Drive\03_Areas\Keys\Environments\Load-Environments.ps1'
$token = $envs.todoist.credentials.apiToken

# Set headers
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

# Get all tasks
$tasks = Invoke-RestMethod -Uri "https://api.todoist.com/api/v1/tasks" -Headers $headers

# Display tasks
$tasks | ForEach-Object {
    Write-Host "[$($_.priority)] $($_.content)"
}

# Create a task
$taskData = @{
    content = "PowerShell automation task"
    due_string = "tomorrow"
    priority = 3
} | ConvertTo-Json

$newTask = Invoke-RestMethod `
    -Uri "https://api.todoist.com/api/v1/tasks" `
    -Method Post `
    -Headers $headers `
    -Body $taskData

Write-Host "Created task: $($newTask.content) (ID: $($newTask.id))"

# Complete a task
Invoke-RestMethod `
    -Uri "https://api.todoist.com/api/v1/tasks/$($newTask.id)/close" `
    -Method Post `
    -Headers $headers
```

### Complete PowerShell Module

```powershell
# Todoist-Manager.ps1
# PowerShell module for Todoist API integration

function Get-TodoistToken {
    $envs = & 'G:\My Drive\03_Areas\Keys\Environments\Load-Environments.ps1'
    return $envs.todoist.credentials.apiToken
}

function Get-TodoistHeaders {
    $token = Get-TodoistToken
    return @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }
}

function Get-TodoistTasks {
    param(
        [string]$Filter,
        [string]$ProjectId
    )
    
    $headers = Get-TodoistHeaders
    $uri = "https://api.todoist.com/api/v1/tasks"
    
    if ($Filter) {
        $uri += "?filter=$Filter"
    } elseif ($ProjectId) {
        $uri += "?project_id=$ProjectId"
    }
    
    return Invoke-RestMethod -Uri $uri -Headers $headers
}

function Add-TodoistTask {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Content,
        
        [string]$DueString,
        [int]$Priority = 1,
        [string]$ProjectId,
        [string[]]$Labels
    )
    
    $headers = Get-TodoistHeaders
    
    $taskData = @{
        content = $Content
    }
    
    if ($DueString) { $taskData.due_string = $DueString }
    if ($Priority) { $taskData.priority = $Priority }
    if ($ProjectId) { $taskData.project_id = $ProjectId }
    if ($Labels) { $taskData.labels = $Labels }
    
    $body = $taskData | ConvertTo-Json
    
    return Invoke-RestMethod `
        -Uri "https://api.todoist.com/api/v1/tasks" `
        -Method Post `
        -Headers $headers `
        -Body $body
}

function Complete-TodoistTask {
    param(
        [Parameter(Mandatory=$true)]
        [string]$TaskId
    )
    
    $headers = Get-TodoistHeaders
    
    Invoke-RestMethod `
        -Uri "https://api.todoist.com/api/v1/tasks/$TaskId/close" `
        -Method Post `
        -Headers $headers
}

function Get-TodoistProjects {
    $headers = Get-TodoistHeaders
    return Invoke-RestMethod -Uri "https://api.todoist.com/api/v1/projects" -Headers $headers
}

# Export functions
Export-ModuleMember -Function Get-TodoistTasks, Add-TodoistTask, Complete-TodoistTask, Get-TodoistProjects
```

**Usage**:
```powershell
# Import module
Import-Module .\Todoist-Manager.ps1

# Get today's tasks
$todayTasks = Get-TodoistTasks -Filter "today"

# Create a task
$task = Add-TodoistTask -Content "Review code" -DueString "tomorrow at 2pm" -Priority 3

# Complete a task
Complete-TodoistTask -TaskId $task.id
```

---

## Common Use Cases

### 1. Daily Task Review

```python
from todoist_api_python.api import TodoistAPI

api = TodoistAPI(token)

# Get today's tasks
today_tasks = api.get_tasks(filter="today")

# Get overdue tasks
overdue_tasks = api.get_tasks(filter="overdue")

# Print summary
print(f"Today: {len(today_tasks)} tasks")
print(f"Overdue: {len(overdue_tasks)} tasks")

for task in today_tasks:
    print(f"  - {task.content}")
```

### 2. Email to Task Automation

```python
import imaplib
import email
from todoist_api_python.api import TodoistAPI

def emails_to_tasks():
    # Connect to email
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('user@gmail.com', 'password')
    mail.select('inbox')
    
    # Search for flagged emails
    _, messages = mail.search(None, 'FLAGGED')
    
    api = TodoistAPI(token)
    
    for msg_id in messages[0].split():
        _, msg_data = mail.fetch(msg_id, '(RFC822)')
        email_body = msg_data[0][1]
        message = email.message_from_bytes(email_body)
        
        # Create task from email
        api.add_task(
            content=message['subject'],
            description=f"From: {message['from']}\n\n{message.get_payload()}",
            labels=["email"]
        )
        
        # Unflag email
        mail.store(msg_id, '-FLAGS', '\\Flagged')
```

### 3. Calendar Sync

```python
from todoist_api_python.api import TodoistAPI
from datetime import datetime, timedelta

api = TodoistAPI(token)

# Get tasks with due dates in next 7 days
tasks = api.get_tasks()

calendar_events = []
for task in tasks:
    if task.due and task.due.date:
        event = {
            'summary': task.content,
            'start': task.due.date,
            'description': task.description or ''
        }
        calendar_events.append(event)

# Export to calendar (Google Calendar, Outlook, etc.)
```

### 4. Project Template

```python
def create_project_from_template(project_name, template_tasks):
    """Create a new project with predefined tasks"""
    api = TodoistAPI(token)
    
    # Create project
    project = api.add_project(name=project_name, color="blue")
    
    # Add tasks from template
    for task_template in template_tasks:
        api.add_task(
            content=task_template['content'],
            project_id=project.id,
            due_string=task_template.get('due_string'),
            priority=task_template.get('priority', 1)
        )
    
    return project

# Usage
template = [
    {"content": "Project kickoff", "due_string": "today", "priority": 4},
    {"content": "Requirements gathering", "due_string": "in 2 days", "priority": 3},
    {"content": "Design phase", "due_string": "in 1 week", "priority": 2},
    {"content": "Implementation", "due_string": "in 2 weeks", "priority": 2}
]

project = create_project_from_template("New Client Project", template)
```

### 5. Productivity Stats

```python
import requests
from datetime import datetime

headers = {"Authorization": f"Bearer {token}"}

# Get productivity stats
stats = requests.get(
    "https://api.todoist.com/api/v1/tasks/completed/stats",
    headers=headers
).json()

print(f"Total completed: {stats['completed_count']}")
print(f"Karma: {stats['karma']}")
print(f"Daily goal: {stats['goals']['daily_goal']}")
print(f"Weekly goal: {stats['goals']['weekly_goal']}")

# Get completed tasks by date
completed = requests.get(
    "https://api.todoist.com/api/v1/tasks/completed/by_completion_date",
    headers=headers
).json()
```

### 6. Bulk Task Import

```python
import csv
from todoist_api_python.api import TodoistAPI

api = TodoistAPI(token)

# Read tasks from CSV
with open('tasks.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        api.add_task(
            content=row['task'],
            due_string=row['due_date'],
            priority=int(row['priority']),
            project_id=row['project_id']
        )
        print(f"Created: {row['task']}")
```

---

## Best Practices

### 1. Error Handling

```python
from todoist_api_python.api import TodoistAPI
from todoist_api_python.api_async import TodoistAPIAsync
import requests

api = TodoistAPI(token)

try:
    task = api.add_task(content="New task")
except Exception as e:
    print(f"Error creating task: {e}")
    # Log error, retry, or handle gracefully
```

### 2. Rate Limiting

- Respect rate limits: 450 requests per 15 minutes
- Use Sync API for batch operations
- Implement exponential backoff for retries

```python
import time
from requests.exceptions import HTTPError

def api_call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except HTTPError as e:
            if e.response.status_code == 429:
                wait_time = 2 ** attempt
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("Max retries exceeded")
```

### 3. Incremental Sync

Always use incremental sync after initial full sync:

```python
# First sync
sync_token = "*"

# Subsequent syncs
sync_data = {
    "sync_token": sync_token,
    "resource_types": '["items"]'  # Only sync tasks
}
```

### 4. Use Temp IDs for Batch Operations

```python
import uuid

commands = [
    {
        "type": "project_add",
        "temp_id": str(uuid.uuid4()),
        "uuid": str(uuid.uuid4()),
        "args": {"name": "Project"}
    }
]
```

### 5. Secure Token Storage

```python
import os
from pathlib import Path

# Use environment variables
token = os.getenv('TODOIST_API_TOKEN')

# Or secure config file
config_path = Path.home() / '.todoist' / 'config.json'
```

### 6. Pagination

```python
# For endpoints that support pagination
cursor = None
all_tasks = []

while True:
    params = {"limit": 100}
    if cursor:
        params["cursor"] = cursor
    
    response = requests.get(
        "https://api.todoist.com/api/v1/tasks",
        headers=headers,
        params=params
    ).json()
    
    all_tasks.extend(response.get('results', []))
    
    cursor = response.get('next_cursor')
    if not cursor:
        break
```

---

## Troubleshooting

### Common Errors

#### 401 Unauthorized

**Cause**: Invalid or missing API token

**Solution**:
```python
# Verify token
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("https://api.todoist.com/api/v1/user", headers=headers)
if response.status_code == 401:
    print("Invalid token. Check your API token in Todoist settings.")
```

#### 404 Not Found

**Cause**: Invalid task/project ID or endpoint

**Solution**:
- Verify IDs are current (opaque string v2_id format)
- Check endpoint URL spelling (lowercase only)
- Ensure resource exists and you have access

#### 410 Gone (Deprecated Endpoint)

**Cause**: Using deprecated REST v2 or Sync v9 endpoints

**Solution**:
```python
# ❌ WRONG (deprecated)
response = requests.get("https://api.todoist.com/rest/v2/tasks")
response = requests.post("https://api.todoist.com/sync/v9/sync")

# ✅ CORRECT (API v1)
response = requests.get("https://api.todoist.com/api/v1/tasks")
```

#### 429 Too Many Requests

**Cause**: Rate limit exceeded

**Solution**:
```python
if response.status_code == 429:
    retry_after = int(response.headers.get('Retry-After', 60))
    print(f"Rate limited. Retry after {retry_after}s")
    time.sleep(retry_after)
```

#### 400 Bad Request

**Cause**: Invalid request data

**Solution**:
```python
response = requests.post(url, headers=headers, json=data)
if response.status_code == 400:
    error = response.json()
    print(f"Error: {error.get('error')}")
    print(f"Details: {error.get('error_extra')}")
```

### Debugging Tips

1. **Enable verbose logging**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **Inspect API responses**:
```python
response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"Body: {response.text}")
```

3. **Validate JSON**:
```python
import json
try:
    data = json.loads(response.text)
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}")
```

---

## Rate Limits

### Limits

- **REST API**: 450 requests per 15 minutes per user
- **Sync API Full Sync**: 100 requests per 15 minutes per user
- **Sync API Partial Sync**: 1000 requests per 15 minutes per user

### Best Practices

1. **Use Sync API for batch operations** (up to 100 commands per request)
2. **Cache data locally** to reduce API calls
3. **Use incremental sync** instead of full sync
4. **Implement exponential backoff** for retries

### Monitoring Rate Limits

```python
response = requests.get(url, headers=headers)

# Check rate limit headers
remaining = response.headers.get('X-RateLimit-Remaining')
reset_time = response.headers.get('X-RateLimit-Reset')

print(f"Requests remaining: {remaining}")
print(f"Reset at: {reset_time}")
```

---

## Quick Reference

### Essential Endpoints

```bash
# Tasks
GET    /api/v1/tasks
POST   /api/v1/tasks
POST   /api/v1/tasks/{id}
DELETE /api/v1/tasks/{id}
POST   /api/v1/tasks/{id}/close

# Projects
GET    /api/v1/projects
POST   /api/v1/projects
POST   /api/v1/projects/{id}
DELETE /api/v1/projects/{id}

# Comments
GET    /api/v1/comments?task_id={id}
POST   /api/v1/comments

# Labels
GET    /api/v1/labels
POST   /api/v1/labels

# Sync
POST   /api/v1/sync
```

### Common Filters

- `today` - Due today
- `tomorrow` - Due tomorrow
- `overdue` - Overdue tasks
- `p1` - Priority 1 (urgent)
- `@label` - By label
- `#project` - By project
- `assigned to: me` - Assigned to you
- `no date` - No due date

### Priority Mapping

| UI | API | Description |
|----|-----|-------------|
| p1 | 4 | Urgent (red) |
| p2 | 3 | High (orange) |
| p3 | 2 | Medium (yellow) |
| p4 | 1 | Normal (white) |

---

## Related Guides

- [MASTER_GUIDE_GMAIL_AUTOMATION.md](MASTER_GUIDE_GMAIL_AUTOMATION.md) - Email integration
- [MASTER_GUIDE_POWERSHELL_AUTOMATION.md](MASTER_GUIDE_POWERSHELL_AUTOMATION.md) - PowerShell scripting
- [MASTER_GUIDE_ENVIRONMENTS_AND_CREDENTIALS.md](MASTER_GUIDE_ENVIRONMENTS_AND_CREDENTIALS.md) - Credential management

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-21 | Initial creation with API v1 documentation |

---

## Resources

- **Official API Docs**: https://developer.todoist.com/rest/v2
- **Python SDK**: https://github.com/Doist/todoist-api-python
- **TypeScript SDK**: https://github.com/Doist/todoist-api-typescript
- **App Console**: https://developer.todoist.com/appconsole.html
- **Community**: https://todoist.com/help

---

**Security Notice**: This guide contains references to API tokens stored in secure locations. Never commit tokens to source control or share them publicly.
