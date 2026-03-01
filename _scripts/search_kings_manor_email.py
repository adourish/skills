#!/usr/bin/env python3
"""Search Gmail for Kings Manor HOE email and extract account number"""

import os
import json
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Load credentials
creds_path = r'G:\My Drive\03_Areas\Keys\Gmail\token.json'
with open(creds_path, 'r') as f:
    token_data = json.load(f)

creds = Credentials(
    token=token_data['token'],
    refresh_token=token_data['refresh_token'],
    token_uri=token_data['token_uri'],
    client_id=token_data['client_id'],
    client_secret=token_data['client_secret'],
    scopes=token_data['scopes']
)

# Refresh if needed
if creds.expired and creds.refresh_token:
    creds.refresh(Request())

# Build Gmail service
service = build('gmail', 'v1', credentials=creds)

# Search for SCS Associa or Kristen Christensen emails with invoice/account info
query = '(SCS Associa OR Kristen Christensen OR kchristensen@scs-management.com) AND (invoice OR account OR payment OR "account number")'
results = service.users().messages().list(userId='me', q=query, maxResults=20).execute()
messages = results.get('messages', [])

print(f"Found {len(messages)} emails matching 'Kings Manor' or 'HOE'")
print("="*60)

for msg in messages:
    # Get full message
    message = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
    
    # Get headers
    headers = message['payload']['headers']
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
    from_email = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
    date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
    
    # Get body
    body = ''
    if 'parts' in message['payload']:
        for part in message['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                if 'data' in part['body']:
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
    elif 'body' in message['payload'] and 'data' in message['payload']['body']:
        body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')
    
    # Show all emails to find account number
    print(f"\n{'='*60}")
    print(f"From: {from_email}")
    print(f"Subject: {subject}")
    print(f"Date: {date}")
    print(f"\nBody:")
    print(body if body else "[No text body found]")
    print(f"{'='*60}")
