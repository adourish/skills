#!/usr/bin/env python3
"""
Email Processor - Extract tasks, events, and notes from Gmail
Usage: python email_processor.py [--days 7] [--auth] [--dry-run]
"""

import os
import re
import json
import argparse
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Paths
ENVIRONMENTS_PATH = r'G:\My Drive\03_Areas\Keys\Environments\environments.json'
TOKEN_PATH = r'G:\My Drive\03_Areas\Keys\Gmail\token.json'

class EmailProcessor:
    def __init__(self):
        self.service = None
        self.authenticate()
        
        # Unimportant senders to skip
        self.skip_senders = [
            'tiktok.com',
            'noreply',
            'no-reply',
            'donotreply',
            'marketing@',
            'promo@',
            'newsletter@',
            'notifications@',
            'redditmail.com',
            'email.monarch.com',
            'rescueme.org',
            'govdelivery.com',
            'membershipto',  # PTA newsletters
            'bankofamerica.com',  # Balance alerts
            'ealerts.',
            'USPSInformeddelivery',
            'schwab.com',
            'creditkarma.com',
            'omadahealth.com'
        ]
    
    def authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(ENVIRONMENTS_PATH):
                    print(f"❌ Error: environments.json not found at {ENVIRONMENTS_PATH}")
                    print("Please ensure Gmail credentials are configured in environments.json")
                    return False
                
                # Load Gmail OAuth credentials from environments.json
                with open(ENVIRONMENTS_PATH, 'r') as f:
                    env_config = json.load(f)
                
                gmail_oauth = env_config['environments']['gmail']['oauth']
                
                # Create credentials dict in format expected by OAuth flow
                client_config = {
                    "installed": {
                        "client_id": gmail_oauth['clientId'],
                        "client_secret": gmail_oauth['clientSecret'],
                        "project_id": gmail_oauth['projectId'],
                        "auth_uri": gmail_oauth['authUri'],
                        "token_uri": gmail_oauth['tokenUri'],
                        "redirect_uris": gmail_oauth['redirectUris']
                    }
                }
                
                flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save token
            os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
            with open(TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=creds)
        print("✅ Authenticated with Gmail API")
        return True
    
    def get_emails_from_week(self, days=7):
        """Get emails from the past week"""
        after_date = (datetime.now() - timedelta(days=days)).strftime('%Y/%m/%d')
        query = f'after:{after_date} -category:promotions -category:social'
        
        try:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=100
            ).execute()
            
            messages = results.get('messages', [])
            print(f"📧 Found {len(messages)} emails from the past {days} days")
            
            return messages
        except Exception as e:
            print(f"❌ Error fetching emails: {e}")
            return []
    
    def is_important(self, sender):
        """Check if email is from an important sender"""
        sender_lower = sender.lower()
        
        # Skip if sender matches any unimportant pattern
        for skip_pattern in self.skip_senders:
            if skip_pattern in sender_lower:
                return False
        
        return True
    
    def get_email_details(self, msg_id):
        """Get full email details"""
        try:
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
                    if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                        break
            elif 'body' in message['payload'] and 'data' in message['payload']['body']:
                body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8', errors='ignore')
            
            return {
                'id': msg_id,
                'subject': subject,
                'from': sender,
                'date': date,
                'body': body[:1000]  # Limit body length
            }
        except Exception as e:
            print(f"❌ Error getting email details: {e}")
            return None
    
    def extract_tasks(self, email):
        """Extract tasks from email"""
        tasks = []
        
        # Task indicators
        action_verbs = ['review', 'complete', 'submit', 'send', 'update', 'prepare',
                       'schedule', 'confirm', 'respond', 'follow up', 'check',
                       'approve', 'sign', 'fill out', 'register', 'book']
        
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
                    'tags': ['email-task', 'inbox']
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
        today = datetime.now()
        
        patterns = {
            'today': today,
            'tomorrow': today + timedelta(days=1),
            'this friday': self._next_weekday(4),
            'next week': today + timedelta(days=7),
            'end of week': self._next_weekday(4),
            'eod': today,
            'asap': today,
        }
        
        for pattern, date in patterns.items():
            if pattern in text:
                return date.strftime('%Y-%m-%d')
        
        # Look for specific dates (MM/DD or MM/DD/YYYY)
        date_match = re.search(r'(\d{1,2})/(\d{1,2})(?:/(\d{2,4}))?', text)
        if date_match:
            month, day = int(date_match.group(1)), int(date_match.group(2))
            year = int(date_match.group(3)) if date_match.group(3) else today.year
            if year < 100:
                year += 2000
            try:
                return f"{year}-{month:02d}-{day:02d}"
            except:
                pass
        
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
        if any(word in text for word in ['urgent', 'asap', 'critical', 'important', 'priority']):
            return 'high'
        if any(word in text for word in ['fyi', 'when you can', 'no rush', 'low priority']):
            return 'low'
        return 'normal'
    
    def extract_events(self, email):
        """Extract calendar events from email"""
        events = []
        
        text = (email['subject'] + ' ' + email['body']).lower()
        
        # Meeting indicators
        meeting_words = ['meeting', 'call', 'conference', 'appointment', 'interview',
                        'presentation', 'demo', 'session', 'webinar']
        
        if any(word in text for word in meeting_words):
            event_date = self._extract_due_date(text)
            event_time = self._extract_event_time(email['body'])
            
            if event_date or event_time:
                event = {
                    'title': email['subject'],
                    'date': event_date,
                    'time': event_time,
                    'location': self._extract_location(email['body']),
                    'source': f"Email from {email['from']}"
                }
                events.append(event)
        
        return events
    
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
            elif period and period.upper() == 'AM' and hour == 12:
                hour = 0
            
            return f"{hour:02d}:{minute:02d}"
        
        return None
    
    def _extract_location(self, text):
        """Extract location from text"""
        # Look for common location patterns
        location_match = re.search(r'(?:location|room|at|in):\s*([^\n]+)', text, re.IGNORECASE)
        if location_match:
            return location_match.group(1).strip()[:100]
        
        return None
    
    def should_save_as_note(self, email):
        """Determine if email should be saved as note"""
        note_indicators = [
            'confirmation', 'receipt', 'invoice', 'password', 'code',
            'booking', 'reservation', 'ticket', 'important', 'reference',
            'account', 'verification', 'reset'
        ]
        
        text = (email['subject'] + ' ' + email['body']).lower()
        return any(indicator in text for indicator in note_indicators)
    
    def process_emails(self, days=7, dry_run=False):
        """Main processing function"""
        print(f"\n{'='*60}")
        print(f"Processing emails from the past {days} days")
        if dry_run:
            print("DRY RUN MODE - No items will be created")
        print(f"{'='*60}\n")
        
        messages = self.get_emails_from_week(days)
        
        if not messages:
            print("No emails to process")
            return None
        
        all_tasks = []
        all_events = []
        notes_to_create = []
        
        # Process emails
        processed_count = 0
        skipped_count = 0
        
        for i, msg in enumerate(messages[:50], 1):  # Process first 50
            email = self.get_email_details(msg['id'])
            
            if not email:
                continue
            
            # Skip unimportant emails
            if not self.is_important(email['from']):
                skipped_count += 1
                continue
            
            processed_count += 1
            print(f"\n📧 Email {processed_count}: {email['subject'][:60]}...")
            print(f"   From: {email['from'][:50]}")
            
            # Extract tasks
            tasks = self.extract_tasks(email)
            if tasks:
                print(f"   ✅ Found {len(tasks)} task(s)")
                for task in tasks:
                    print(f"      - {task['title'][:50]}... (Due: {task['due_date'] or 'Not specified'})")
                all_tasks.extend(tasks)
            
            # Extract events
            events = self.extract_events(email)
            if events:
                print(f"   📅 Found {len(events)} event(s)")
                for event in events:
                    print(f"      - {event['title'][:50]}... ({event['date']} {event['time'] or ''})")
                all_events.extend(events)
            
            # Check if should save as note
            if self.should_save_as_note(email):
                print(f"   📝 Marked for note creation")
                notes_to_create.append(email)
        
        # Generate summary
        print(f"\n{'='*60}")
        print(f"PROCESSING SUMMARY")
        print(f"{'='*60}")
        print(f"📧 Total emails scanned: {min(50, len(messages))}")
        print(f"⏭️  Skipped (unimportant): {skipped_count}")
        print(f"✅ Important emails processed: {processed_count}")
        print(f"📋 Tasks extracted: {len(all_tasks)}")
        print(f"📅 Events identified: {len(all_events)}")
        print(f"📝 Notes to create: {len(notes_to_create)}")
        
        # Save results
        results = {
            'processed_date': datetime.now().isoformat(),
            'days_processed': days,
            'tasks': all_tasks,
            'events': all_events,
            'notes': [{'subject': e['subject'], 'from': e['from'], 'date': e['date']} for e in notes_to_create]
        }
        
        output_file = f"email_processing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_path = os.path.join(os.path.dirname(__file__), output_file)
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Results saved to: {output_path}")
        
        return results

def main():
    parser = argparse.ArgumentParser(description='Process Gmail emails for tasks, events, and notes')
    parser.add_argument('--days', type=int, default=7, help='Number of days to process (default: 7)')
    parser.add_argument('--auth', action='store_true', help='Authenticate only, do not process')
    parser.add_argument('--dry-run', action='store_true', help='Analyze emails but do not create items')
    
    args = parser.parse_args()
    
    processor = EmailProcessor()
    
    if not processor.service:
        print("❌ Authentication failed. Please check your credentials.")
        return
    
    if args.auth:
        print("✅ Authentication successful!")
        return
    
    results = processor.process_emails(days=args.days, dry_run=args.dry_run)
    
    if results:
        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("="*60)
        print("1. Review the extracted tasks and events in the JSON file")
        print("2. Run sync script to create items in Amplenote:")
        print("   node sync_email_to_amplenote.js")
        print("3. Archive processed emails in Gmail")
        print("="*60)

if __name__ == '__main__':
    main()
