#!/usr/bin/env python3
"""
Gmail OAuth Setup
Sets up OAuth for Gmail and Google Drive access
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Paths
GMAIL_TOKEN_PATH = r'G:\My Drive\Areas\Keys\Gmail\token.json'
GMAIL_CREDENTIALS_PATH = r'G:\My Drive\Areas\Keys\Gmail\credentials.json'

# Scopes for Gmail, Drive, and Calendar
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]

def setup_gmail_oauth():
    """Set up Gmail and Google Drive OAuth"""
    print("\n" + "="*60)
    print("GMAIL & GOOGLE DRIVE OAUTH SETUP")
    print("="*60)
    print("\nThis will set up access to:")
    print("  - Gmail (personal email)")
    print("  - Google Drive (personal documents)")
    print("\n" + "="*60)
    
    if not os.path.exists(GMAIL_CREDENTIALS_PATH):
        print(f"\n❌ ERROR: credentials.json not found at:")
        print(f"   {GMAIL_CREDENTIALS_PATH}")
        print("\nYou need to:")
        print("1. Go to Google Cloud Console")
        print("2. Create OAuth 2.0 credentials")
        print("3. Download credentials.json")
        print("4. Save it to the path above")
        return False
    
    try:
        print("\n🔐 Starting OAuth flow...")
        print("   Browser will open for authentication")
        print("   Sign in with your personal Google account")
        print("   Grant access to Gmail and Drive\n")
        
        # Create OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file(
            GMAIL_CREDENTIALS_PATH, SCOPES
        )
        
        # Run local server for OAuth callback
        creds = flow.run_local_server(port=0)
        
        # Save credentials
        os.makedirs(os.path.dirname(GMAIL_TOKEN_PATH), exist_ok=True)
        with open(GMAIL_TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
        
        print("\n" + "="*60)
        print("✅ GMAIL & GOOGLE DRIVE OAUTH SUCCESSFUL!")
        print("="*60)
        print(f"Token saved to: {GMAIL_TOKEN_PATH}")
        print("\nYou can now run:")
        print("  python daily_planner.py")
        print("\nTo see Gmail emails and Google Drive documents in your daily plan!")
        return True
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ GMAIL OAUTH FAILED")
        print("="*60)
        print(f"Error: {e}")
        return False

if __name__ == '__main__':
    success = setup_gmail_oauth()
    
    if not success:
        print("\n⚠️  OAuth setup failed.")
        print("Check that credentials.json exists and is valid.")
