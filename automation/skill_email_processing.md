# MASTER GUIDE: Email Processing & Task Extraction

**Complete Guide to Processing Emails for Tasks, Calendar Events, and Notes**

**Last Updated:** February 21, 2026  
**Version:** 1.0.0

## Quick Reference
**Use when:** Weekly email cleanup, extracting tasks/action items from email backlog, catching up after time off
**Don't use when:** You want full daily planning — use `skill_daily_planning` which includes email processing
**Trigger phrases:** "process my emails", "extract tasks from email", "weekly email cleanup", "what emails need action"
**Time:** 5-10 minutes
**Command:** `python email_processor.py` (in `_scripts/`) or use MCP `gmail_search` + `gmail_get_email` tools

---

## Table of Contents

1. [Overview](#overview)
2. [Gmail API Setup](#gmail-api-setup)
3. [Email Processing Workflow](#email-processing-workflow)
4. [Automated Task Extraction](#automated-task-extraction)
5. [Calendar Event Creation](#calendar-event-creation)
6. [Note Creation from Emails](#note-creation-from-emails)
7. [Integration with Amplenote](#integration-with-amplenote)
8. [Complete Automation Script](#complete-automation-script)
9. [Manual Processing Checklist](#manual-processing-checklist)
10. [Troubleshooting](#troubleshooting)

---

## Overview

This guide provides a complete workflow for processing emails to extract actionable items:
- ✅ **Tasks** → **Todoist** - Action items that need to be completed
- ✅ **Calendar Events** → **Google Calendar** - Meetings, deadlines, appointments
- ✅ **Notes** → **Amplenote** - Important information to save for reference

### Benefits
- Never miss important action items from emails
- Automatically filter out unimportant emails (newsletters, promotions, alerts)
- Tasks sync to Todoist for unified task management
- Events sync to Google Calendar for scheduling
- Important information archived in Amplenote
- Reduce inbox clutter by focusing only on what matters

### Processing Frequency
- **Daily**: Quick scan for urgent items
- **Weekly**: Comprehensive review of all emails
- **Monthly**: Archive and cleanup

### Importance Filtering

The system automatically filters out unimportant emails from:
- **Marketing & Promotions**: TikTok, newsletters, promotional emails
- **Automated Alerts**: Bank balance alerts, USPS tracking, credit monitoring
- **Social Media**: Reddit, Facebook, Twitter notifications
- **Low-Value Notifications**: PTA newsletters, rescue alerts, health app updates
- **Generic No-Reply**: Automated system emails with no actionable content

**Only important emails are processed** - those from real people, important services, or containing actionable items.

---

## Gmail API Setup

### Prerequisites

1. **Google Cloud Project** with Gmail API enabled
2. **OAuth 2.0 Credentials** (Desktop app type)
3. **Python 3.7+** installed

### Step 1: Create OAuth Credentials

1. Go to https://console.cloud.google.com/apis/credentials
2. Select your project (or create a new one)
3. Click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
4. Choose **"Desktop app"** as application type
5. Name it (e.g., "Email Processor")
6. Click **"CREATE"**
7. Click **"DOWNLOAD JSON"** button
8. Save the file as `credentials.json` in `G:\My Drive\03_Areas\Keys\Gmail\`

### Step 2: Enable Gmail API

1. Go to https://console.cloud.google.com/apis/library
2. Search for "Gmail API"
3. Click **"ENABLE"**

### Step 3: Install Python Dependencies

```powershell
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 4: First-Time Authentication

```powershell
cd "G:\My Drive\06_Master_Guides\Scripts"
python email_processor.py --auth
```

This will:
- Open browser for authorization
- Save token to `G:\My Drive\03_Areas\Keys\Gmail\token.json`
- Grant read-only access to Gmail

---

## Email Processing Workflow

### Weekly Email Review Process

```
1. Fetch Emails (Past 7 Days)
   ↓
2. Filter Out Unimportant Emails
   (Skip: TikTok, newsletters, alerts, promotions)
   ↓
3. Analyze Important Emails Only
   ↓
4. Extract Actionable Items
   ├─→ Tasks → Todoist (action required)
   ├─→ Calendar Events → Google Calendar (time-specific)
   └─→ Notes → Amplenote (reference information)
   ↓
5. Sync to Services
   ├─→ Create Todoist tasks with due dates
   ├─→ Add events to Google Calendar
   └─→ Archive important emails in Amplenote
   ↓
6. Generate Summary Report
```

### Email Analysis Criteria

**Identify as Task if:**
- Contains action verbs: "review", "complete", "submit", "send", "update"
- Has deadline language: "by Friday", "due date", "deadline"
- Contains questions requiring response
- Flagged/starred by you

**Identify as Calendar Event if:**
- Contains date/time information
- Meeting invitations
- Appointment confirmations
- Deadline reminders
- Event announcements

**Identify as Note if:**
- Reference information (passwords, codes, links)
- Important announcements
- Documentation or instructions
- Receipts or confirmations
- Information to save for later

---

## Automated Task Extraction

### Task Detection Patterns

```python
TASK_INDICATORS = {
    'action_verbs': [
        'review', 'complete', 'submit', 'send', 'update', 'prepare',
        'schedule', 'confirm', 'respond', 'follow up', 'check',
        'approve', 'sign', 'fill out', 'register', 'book'
    ],
    'deadline_phrases': [
        'by', 'due', 'deadline', 'before', 'no later than',
        'asap', 'urgent', 'priority', 'today', 'tomorrow',
        'this week', 'end of day', 'eod'
    ],
    'question_indicators': [
        '?', 'can you', 'could you', 'would you', 'please',
        'need you to', 'requesting', 'asking'
    ]
}
```

### Task Extraction Example

**Email Subject:** "Please review Q1 budget by Friday"

**Extracted Task:**
- **Title:** Review Q1 budget
- **Due Date:** This Friday
- **Priority:** Normal
- **Source:** Email from [sender]
- **Tags:** work, budget, review

### Task Priority Assignment

```python
def assign_priority(email):
    priority = 'normal'
    
    # High priority indicators
    if any(word in email.lower() for word in ['urgent', 'asap', 'critical', 'important']):
        priority = 'high'
    
    # Low priority indicators
    if any(word in email.lower() for word in ['fyi', 'when you can', 'no rush']):
        priority = 'low'
    
    # Deadline-based priority
    if has_deadline_within_days(email, 2):
        priority = 'high'
    
    return priority
```

---

## Calendar Event Creation

### Event Detection Patterns

```python
EVENT_INDICATORS = {
    'meeting_words': [
        'meeting', 'call', 'conference', 'appointment', 'interview',
        'presentation', 'demo', 'session', 'webinar', 'training'
    ],
    'time_patterns': [
        r'\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)',  # 2:30 PM
        r'\d{1,2}\s*(?:AM|PM|am|pm)',        # 2 PM
        r'at\s+\d{1,2}',                      # at 2
    ],
    'date_patterns': [
        r'(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)',
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}',
        r'\d{1,2}/\d{1,2}/\d{2,4}',
        r'tomorrow', r'today', r'next week'
    ]
}
```

### Event Extraction Example

**Email Body:**
```
Hi,

Let's schedule a meeting to discuss the project timeline.
How about Tuesday, February 25th at 2:30 PM?

Location: Conference Room B
Duration: 1 hour

Thanks!
```

**Extracted Event:**
- **Title:** Meeting - Project Timeline Discussion
- **Date:** Tuesday, February 25, 2026
- **Time:** 2:30 PM
- **Duration:** 1 hour
- **Location:** Conference Room B
- **Attendees:** [sender email]
- **Source:** Email from [sender]

### Calendar Integration Options

**Option 1: Create Amplenote Task with Date**
```javascript
await addTask(
  inboxNoteUuid,
  'Meeting: Project Timeline Discussion',
  new Date('2026-02-25T14:30:00'),
  false  // not important
);
```

**Option 2: Create Google Calendar Event**
```python
event = {
    'summary': 'Meeting: Project Timeline Discussion',
    'location': 'Conference Room B',
    'start': {
        'dateTime': '2026-02-25T14:30:00',
        'timeZone': 'America/New_York',
    },
    'end': {
        'dateTime': '2026-02-25T15:30:00',
        'timeZone': 'America/New_York',
    },
}
```

---

## Note Creation from Emails

### Note-Worthy Email Types

1. **Reference Information**
   - Account numbers, passwords, access codes
   - Important links or resources
   - Instructions or procedures
   - Contact information

2. **Receipts & Confirmations**
   - Purchase receipts
   - Booking confirmations
   - Registration confirmations
   - Subscription details

3. **Important Announcements**
   - Policy changes
   - System updates
   - Company announcements
   - Service notifications

4. **Documentation**
   - How-to guides
   - Technical documentation
   - Meeting notes sent via email
   - Project updates

### Note Creation Template

```javascript
async function createNoteFromEmail(email) {
  const noteName = `Email: ${email.subject}`;
  const tags = ['email-archive', extractCategory(email)];
  
  const note = await createNote(noteName, tags);
  
  // Add metadata
  await addContent(note.uuid, `**From:** ${email.from}`);
  await addContent(note.uuid, `**Date:** ${email.date}`);
  await addContent(note.uuid, `**Subject:** ${email.subject}`);
  
  // Add email body
  await addHeading(note.uuid, 'Email Content', 2);
  await addContent(note.uuid, email.body);
  
  // Add attachments info
  if (email.attachments.length > 0) {
    await addHeading(note.uuid, 'Attachments', 2);
    for (const attachment of email.attachments) {
      await addBulletList(note.uuid, [
        `${attachment.name} (${attachment.size})`
      ]);
    }
  }
  
  return note;
}
```

### Note Categories

```python
def categorize_email(email):
    categories = []
    
    # Finance
    if any(word in email.lower() for word in ['invoice', 'payment', 'receipt', 'bank']):
        categories.append('finance')
    
    # Travel
    if any(word in email.lower() for word in ['flight', 'hotel', 'booking', 'reservation']):
        categories.append('travel')
    
    # Work
    if email.from_domain in ['company.com', 'work-domain.com']:
        categories.append('work')
    
    # Personal
    if any(word in email.lower() for word in ['family', 'personal', 'home']):
        categories.append('personal')
    
    return categories or ['general']
```

---

## Integration with Amplenote

### Amplenote Note Structure for Email Processing

**Create a Weekly Email Processing Note:**

```
# Email Processing - Week of Feb 17-23, 2026

## 📋 Tasks Extracted (5)
- [ ] Review Q1 budget (Due: Friday) #work #budget
- [ ] Submit expense report (Due: Monday) #finance #urgent
- [ ] Schedule team meeting (Due: This week) #work #meeting
- [ ] Respond to client inquiry (Due: Tomorrow) #work #client
- [ ] Update project timeline (Due: Next week) #work #project

## 📅 Calendar Events (3)
- Meeting: Project Timeline - Tue Feb 25, 2:30 PM
- Dentist Appointment - Wed Feb 26, 10:00 AM
- Team Standup - Fri Feb 28, 9:00 AM

## 📝 Notes Created (2)
- [[Flight Confirmation - NYC Trip]]
- [[Password Reset - Company Portal]]

## 📊 Summary
- Total emails processed: 47
- Tasks created: 5
- Events identified: 3
- Notes saved: 2
- Emails archived: 35
- Emails deleted: 7
```

### Automated Amplenote Integration

```javascript
// Create weekly processing note
async function createWeeklyEmailNote(weekStart, weekEnd) {
  const noteName = `Email Processing - Week of ${weekStart} to ${weekEnd}`;
  const note = await createNote(noteName, ['email-processing', 'weekly-review']);
  
  await addHeading(note.uuid, noteName, 1);
  
  // Add sections
  await addHeading(note.uuid, '📋 Tasks Extracted', 2);
  await addHeading(note.uuid, '📅 Calendar Events', 2);
  await addHeading(note.uuid, '📝 Notes Created', 2);
  await addHeading(note.uuid, '📊 Summary', 2);
  
  return note;
}

// Add task to note
async function addTaskToProcessingNote(noteUuid, task) {
  const taskText = `${task.title} (Due: ${task.dueDate}) ${task.tags.map(t => '#' + t).join(' ')}`;
  await addTask(noteUuid, taskText, task.dueDate, task.priority === 'high');
}
```

---

## Complete Automation Script

### email_processor.py

```python
#!/usr/bin/env python3
"""
Email Processor - Extract tasks, events, and notes from Gmail
"""

import os
import re
import json
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Paths
CREDENTIALS_PATH = r'G:\My Drive\03_Areas\Keys\Gmail\credentials.json'
TOKEN_PATH = r'G:\My Drive\03_Areas\Keys\Gmail\token.json'

class EmailProcessor:
    def __init__(self):
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=creds)
        print("✅ Authenticated with Gmail API")
    
    def get_emails_from_week(self, days=7):
        """Get emails from the past week"""
        after_date = (datetime.now() - timedelta(days=days)).strftime('%Y/%m/%d')
        query = f'after:{after_date}'
        
        results = self.service.users().messages().list(
            userId='me',
            q=query,
            maxResults=100
        ).execute()
        
        messages = results.get('messages', [])
        print(f"📧 Found {len(messages)} emails from the past {days} days")
        
        return messages
    
    def get_email_details(self, msg_id):
        """Get full email details"""
        message = self.service.users().messages().get(
            userId='me',
            id=msg_id,
            format='full'
        ).execute()
        
        headers = message['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
        
        # Get body
        body = ''
        if 'parts' in message['payload']:
            for part in message['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
        elif 'body' in message['payload']:
            body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')
        
        return {
            'id': msg_id,
            'subject': subject,
            'from': sender,
            'date': date,
            'body': body
        }
    
    def extract_tasks(self, email):
        """Extract tasks from email"""
        tasks = []
        
        # Task indicators
        action_verbs = ['review', 'complete', 'submit', 'send', 'update', 'prepare',
                       'schedule', 'confirm', 'respond', 'follow up', 'check']
        
        text = (email['subject'] + ' ' + email['body']).lower()
        
        # Check for action verbs
        for verb in action_verbs:
            if verb in text:
                # Extract potential task
                task = {
                    'title': self._extract_task_title(email, verb),
                    'due_date': self._extract_due_date(text),
                    'priority': self._extract_priority(text),
                    'source': f"Email from {email['from']}",
                    'tags': ['email-task']
                }
                tasks.append(task)
                break  # One task per email for now
        
        return tasks
    
    def _extract_task_title(self, email, action_verb):
        """Extract task title from email"""
        subject = email['subject']
        
        # Remove common prefixes
        subject = re.sub(r'^(RE:|FW:|FWD:)\s*', '', subject, flags=re.IGNORECASE)
        
        # If subject is short and clear, use it
        if len(subject) < 100:
            return subject
        
        # Otherwise, create title from action verb
        return f"{action_verb.title()} - {subject[:50]}..."
    
    def _extract_due_date(self, text):
        """Extract due date from text"""
        # Look for common date patterns
        patterns = {
            'today': datetime.now(),
            'tomorrow': datetime.now() + timedelta(days=1),
            'this friday': self._next_weekday(4),  # Friday = 4
            'next week': datetime.now() + timedelta(days=7),
        }
        
        for pattern, date in patterns.items():
            if pattern in text:
                return date.strftime('%Y-%m-%d')
        
        # Look for specific dates (MM/DD or MM/DD/YYYY)
        date_match = re.search(r'(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?', text)
        if date_match:
            month, day = int(date_match.group(1)), int(date_match.group(2))
            year = int(date_match.group(3)) if date_match.group(3) else datetime.now().year
            if year < 100:
                year += 2000
            return f"{year}-{month:02d}-{day:02d}"
        
        return None
    
    def _next_weekday(self, weekday):
        """Get next occurrence of weekday (0=Monday, 6=Sunday)"""
        today = datetime.now()
        days_ahead = weekday - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return today + timedelta(days=days_ahead)
    
    def _extract_priority(self, text):
        """Extract priority from text"""
        if any(word in text for word in ['urgent', 'asap', 'critical', 'important']):
            return 'high'
        if any(word in text for word in ['fyi', 'when you can', 'no rush']):
            return 'low'
        return 'normal'
    
    def extract_events(self, email):
        """Extract calendar events from email"""
        events = []
        
        text = (email['subject'] + ' ' + email['body']).lower()
        
        # Meeting indicators
        meeting_words = ['meeting', 'call', 'conference', 'appointment', 'interview']
        
        if any(word in text for word in meeting_words):
            event = {
                'title': email['subject'],
                'date': self._extract_event_date(email['body']),
                'time': self._extract_event_time(email['body']),
                'location': self._extract_location(email['body']),
                'source': f"Email from {email['from']}"
            }
            
            if event['date']:
                events.append(event)
        
        return events
    
    def _extract_event_date(self, text):
        """Extract event date from text"""
        # Similar to _extract_due_date but more specific
        return self._extract_due_date(text)
    
    def _extract_event_time(self, text):
        """Extract event time from text"""
        # Look for time patterns (2:30 PM, 14:30, etc.)
        time_match = re.search(r'(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)?', text)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2))
            period = time_match.group(3)
            
            if period and period.upper() == 'PM' and hour < 12:
                hour += 12
            
            return f"{hour:02d}:{minute:02d}"
        
        return None
    
    def _extract_location(self, text):
        """Extract location from text"""
        # Look for common location patterns
        location_match = re.search(r'(?:location|room|at):\s*([^\n]+)', text, re.IGNORECASE)
        if location_match:
            return location_match.group(1).strip()
        
        return None
    
    def should_save_as_note(self, email):
        """Determine if email should be saved as note"""
        note_indicators = [
            'confirmation', 'receipt', 'invoice', 'password', 'code',
            'booking', 'reservation', 'ticket', 'important', 'reference'
        ]
        
        text = (email['subject'] + ' ' + email['body']).lower()
        return any(indicator in text for indicator in note_indicators)
    
    def process_emails(self, days=7):
        """Main processing function"""
        print(f"\n{'='*60}")
        print(f"Processing emails from the past {days} days")
        print(f"{'='*60}\n")
        
        messages = self.get_emails_from_week(days)
        
        all_tasks = []
        all_events = []
        notes_to_create = []
        
        for i, msg in enumerate(messages[:20], 1):  # Process first 20 for demo
            email = self.get_email_details(msg['id'])
            
            print(f"\n📧 Email {i}: {email['subject'][:60]}...")
            print(f"   From: {email['from']}")
            
            # Extract tasks
            tasks = self.extract_tasks(email)
            if tasks:
                print(f"   ✅ Found {len(tasks)} task(s)")
                all_tasks.extend(tasks)
            
            # Extract events
            events = self.extract_events(email)
            if events:
                print(f"   📅 Found {len(events)} event(s)")
                all_events.extend(events)
            
            # Check if should save as note
            if self.should_save_as_note(email):
                print(f"   📝 Marked for note creation")
                notes_to_create.append(email)
        
        # Generate summary
        print(f"\n{'='*60}")
        print(f"PROCESSING SUMMARY")
        print(f"{'='*60}")
        print(f"📧 Emails processed: {min(20, len(messages))}")
        print(f"✅ Tasks extracted: {len(all_tasks)}")
        print(f"📅 Events identified: {len(all_events)}")
        print(f"📝 Notes to create: {len(notes_to_create)}")
        
        # Save results
        results = {
            'processed_date': datetime.now().isoformat(),
            'tasks': all_tasks,
            'events': all_events,
            'notes': [{'subject': e['subject'], 'from': e['from']} for e in notes_to_create]
        }
        
        output_file = f"email_processing_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_file}")
        
        return results

def main():
    processor = EmailProcessor()
    results = processor.process_emails(days=7)
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. Review the extracted tasks and events")
    print("2. Run the Amplenote sync script to create items")
    print("3. Archive processed emails in Gmail")
    print("="*60)

if __name__ == '__main__':
    main()
```

---

## Manual Processing Checklist

### Daily Email Review (5-10 minutes)

- [ ] Open Gmail inbox
- [ ] Scan for urgent emails (flagged, from important senders)
- [ ] Extract immediate action items
- [ ] Create tasks in Amplenote for urgent items
- [ ] Respond to time-sensitive emails
- [ ] Archive or delete processed emails

### Weekly Email Review (30-60 minutes)

- [ ] Run email processing script
- [ ] Review extracted tasks
  - [ ] Verify task titles are clear
  - [ ] Confirm due dates are correct
  - [ ] Assign priorities
  - [ ] Add relevant tags
- [ ] Review extracted events
  - [ ] Add to calendar
  - [ ] Set reminders
  - [ ] Invite attendees if needed
- [ ] Review notes to create
  - [ ] Create Amplenote notes for important emails
  - [ ] Add relevant tags and links
  - [ ] Attach or link to original email
- [ ] Archive processed emails
- [ ] Unsubscribe from unwanted newsletters
- [ ] Update email filters

### Monthly Email Cleanup (1-2 hours)

- [ ] Review old emails (30+ days)
- [ ] Archive completed items
- [ ] Delete unnecessary emails
- [ ] Update email organization rules
- [ ] Review and update email filters
- [ ] Clean up labels/folders
- [ ] Export important emails to notes
- [ ] Update contact information

---

## Troubleshooting

### Gmail API Issues

**Error: "credentials.json not found"**
- Ensure you downloaded OAuth credentials from Google Cloud Console
- Place file in `G:\My Drive\03_Areas\Keys\Gmail\credentials.json`

**Error: "Access denied"**
- Verify Gmail API is enabled in Google Cloud Console
- Check OAuth consent screen is configured
- Ensure correct scopes are requested

**Error: "Token expired"**
- Delete `token.json` and re-authenticate
- Script should auto-refresh, but manual re-auth works

### Task Extraction Issues

**Tasks not being detected**
- Check email contains action verbs
- Verify email has clear subject line
- Manually review email for actionable items

**Incorrect due dates**
- Date parsing may fail for ambiguous dates
- Manually set due dates in Amplenote
- Update date extraction patterns in script

**Too many false positives**
- Adjust task detection thresholds
- Add exclusion patterns for common false positives
- Review and refine action verb list

### Amplenote Integration Issues

**Tasks not creating in Amplenote**
- Verify Amplenote token is valid
- Check API rate limits
- Review error logs in script output

**Duplicate tasks being created**
- Implement deduplication logic
- Check for existing tasks before creating
- Use email ID as unique identifier

---

## Best Practices

### Email Management

1. **Process emails at set times** - Don't check constantly
2. **Use the 2-minute rule** - If it takes < 2 minutes, do it now
3. **Archive aggressively** - Keep inbox clean
4. **Unsubscribe liberally** - Reduce incoming volume
5. **Use filters** - Automate organization

### Task Creation

1. **Be specific** - Clear, actionable task titles
2. **Set realistic due dates** - Don't overcommit
3. **Add context** - Include relevant details
4. **Use tags** - Organize by project, category, priority
5. **Review regularly** - Update and complete tasks

### Note Taking

1. **Capture key information** - Don't save everything
2. **Use consistent tags** - Easy to find later
3. **Link related notes** - Build knowledge base
4. **Add metadata** - Source, date, category
5. **Review periodically** - Keep notes relevant

---

## Integration Examples

### Example 1: Work Email Processing

**Email:**
```
Subject: Q1 Budget Review - Due Friday
From: manager@company.com

Hi,

Please review the attached Q1 budget spreadsheet and provide
your feedback by end of day Friday. We need to finalize this
before the board meeting next week.

Thanks!
```

**Extracted Items:**
- **Task:** Review Q1 budget spreadsheet
  - Due: This Friday (EOD)
  - Priority: High
  - Tags: work, budget, review, urgent
  - Source: Email from manager@company.com

### Example 2: Meeting Invitation

**Email:**
```
Subject: Project Kickoff Meeting
From: project-lead@company.com

Team,

Let's schedule our project kickoff meeting for next Tuesday,
February 25th at 2:30 PM in Conference Room B.

Agenda:
- Project overview
- Timeline review
- Role assignments

See you there!
```

**Extracted Items:**
- **Event:** Project Kickoff Meeting
  - Date: Tuesday, February 25, 2026
  - Time: 2:30 PM
  - Location: Conference Room B
  - Duration: 1 hour (estimated)
  - Source: Email from project-lead@company.com

### Example 3: Important Information

**Email:**
```
Subject: Password Reset Confirmation
From: noreply@company-portal.com

Your password has been successfully reset.

New temporary password: TempPass123!
Please change this on your next login.

Account: john.doe@company.com
Reset date: 2026-02-21 14:30 UTC
```

**Extracted Items:**
- **Note:** Password Reset - Company Portal
  - Category: reference, security
  - Content: Temporary password and reset details
  - Tags: password, company-portal, security
  - Source: Email from company-portal.com

---

## Quick Reference Commands

### Run Email Processor

```powershell
# Process last 7 days (filters out unimportant emails)
python email_processor.py

# Process last 30 days
python email_processor.py --days 30

# Authenticate only
python email_processor.py --auth

# Dry run (analyze only, no sync)
python email_processor.py --dry-run
```

### Sync to Services

```powershell
# Sync tasks to Todoist, events to Calendar, notes to Amplenote
node sync_email_to_services.js
```

**What it does:**
- ✅ Creates tasks in Todoist with due dates and priorities
- 📅 Lists calendar events (manual entry to Google Calendar for now)
- 📝 Creates notes in Amplenote for important emails

**One-Command Workflow:**
```powershell
cd "G:\My Drive\06_Master_Guides\Scripts"
python email_processor.py --days 7 && node sync_email_to_services.js
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-21 | Initial release with Gmail API integration, task/event/note extraction, Amplenote integration |
| 1.1.0 | 2026-02-22 | Added importance filtering, Todoist integration for tasks, Google Calendar for events, Amplenote for notes only |

---

**End of Master Guide**

For questions or issues, refer to the Gmail API documentation or Amplenote API guide.
