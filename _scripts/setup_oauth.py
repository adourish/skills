#!/usr/bin/env python3
"""
OAuth Setup Script for Holistic Daily Planning
Sets up user authentication for Google Drive and Microsoft Graph (Outlook + SharePoint)
"""

import os
import json
import webbrowser
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from msal import PublicClientApplication

# Paths
ENVIRONMENTS_PATH = r'G:\My Drive\03_Areas\Keys\Environments\environments.json'
GMAIL_CREDS_PATH = r'G:\My Drive\03_Areas\Keys\Gmail\credentials.json'
GMAIL_TOKEN_PATH = r'G:\My Drive\03_Areas\Keys\Gmail\token.json'
MS_TOKEN_PATH = r'G:\My Drive\03_Areas\Keys\Microsoft365\token.json'

# Scopes
GOOGLE_SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]

MICROSOFT_SCOPES = [
    'https://graph.microsoft.com/Mail.Read',
    'https://graph.microsoft.com/Calendars.Read',
    'https://graph.microsoft.com/Files.Read.All',
    'https://graph.microsoft.com/Sites.Read.All',
    'https://graph.microsoft.com/User.Read'
]

def setup_google_oauth():
    """Set up Google OAuth with Gmail and Drive scopes"""
    print("\n" + "="*60)
    print("GOOGLE OAUTH SETUP (Gmail + Drive)")
    print("="*60)
    
    if not os.path.exists(GMAIL_CREDS_PATH):
        print(f"❌ Credentials file not found: {GMAIL_CREDS_PATH}")
        print("   Download from Google Cloud Console")
        return False
    
    try:
        # Delete old token to force re-authentication with new scopes
        if os.path.exists(GMAIL_TOKEN_PATH):
            print("🗑️  Removing old token to re-authenticate with Drive scope...")
            os.remove(GMAIL_TOKEN_PATH)
        
        print("🔐 Starting OAuth flow...")
        print("   Browser will open for authentication")
        print("   Grant access to Gmail and Drive\n")
        
        flow = InstalledAppFlow.from_client_secrets_file(
            GMAIL_CREDS_PATH,
            GOOGLE_SCOPES
        )
        
        creds = flow.run_local_server(port=0)
        
        # Save the credentials
        with open(GMAIL_TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
        
        print("✅ Google OAuth successful!")
        print(f"   Token saved to: {GMAIL_TOKEN_PATH}")
        print(f"   Scopes: Gmail + Drive")
        return True
        
    except Exception as e:
        print(f"❌ Google OAuth failed: {e}")
        return False

def setup_microsoft_oauth():
    """Set up Microsoft OAuth with delegated permissions"""
    print("\n" + "="*60)
    print("MICROSOFT 365 OAUTH SETUP (Outlook + SharePoint)")
    print("="*60)
    
    # Load config
    with open(ENVIRONMENTS_PATH, 'r') as f:
        config = json.load(f)
    
    ms_config = config['environments']['microsoft365']['oauth']
    client_id = ms_config['clientId']
    tenant_id = ms_config['tenantId']
    
    try:
        # Create public client application for delegated permissions
        app = PublicClientApplication(
            client_id,
            authority=f"https://login.microsoftonline.com/{tenant_id}"
        )
        
        print("🔐 Starting OAuth flow...")
        print("   Browser will open for authentication")
        print("   Sign in with your work account")
        print("   Grant access to Mail, Calendar, Files, and Sites\n")
        
        # Interactive authentication
        result = app.acquire_token_interactive(
            scopes=MICROSOFT_SCOPES,
            prompt="select_account"
        )
        
        if "access_token" in result:
            # Save token
            os.makedirs(os.path.dirname(MS_TOKEN_PATH), exist_ok=True)
            
            token_data = {
                'access_token': result['access_token'],
                'refresh_token': result.get('refresh_token'),
                'expires_in': result.get('expires_in'),
                'token_type': result.get('token_type'),
                'scope': result.get('scope'),
                'acquired_at': datetime.now().isoformat()
            }
            
            with open(MS_TOKEN_PATH, 'w') as f:
                json.dump(token_data, f, indent=2)
            
            print("✅ Microsoft 365 OAuth successful!")
            print(f"   Token saved to: {MS_TOKEN_PATH}")
            print(f"   Scopes: Mail, Calendar, Files, Sites")
            return True
        else:
            print(f"❌ Microsoft 365 OAuth failed: {result.get('error_description')}")
            return False
            
    except Exception as e:
        print(f"❌ Microsoft 365 OAuth failed: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("HOLISTIC DAILY PLANNING - OAUTH SETUP")
    print("="*60)
    print("\nThis script will set up OAuth authentication for:")
    print("  1. Google (Gmail + Drive)")
    print("  2. Microsoft 365 (Outlook + SharePoint)")
    print("\nYou'll need to:")
    print("  - Sign in to your Google account")
    print("  - Sign in to your Microsoft 365 work account")
    print("  - Grant permissions for each service")
    print("\n" + "="*60)
    
    input("\nPress Enter to continue...")
    
    # Setup Google OAuth
    google_success = setup_google_oauth()
    
    # Setup Microsoft OAuth
    ms_success = setup_microsoft_oauth()
    
    # Summary
    print("\n" + "="*60)
    print("OAUTH SETUP SUMMARY")
    print("="*60)
    print(f"Google (Gmail + Drive):     {'✅ Success' if google_success else '❌ Failed'}")
    print(f"Microsoft 365 (Outlook + SharePoint): {'✅ Success' if ms_success else '❌ Failed'}")
    print("="*60)
    
    if google_success and ms_success:
        print("\n✅ All OAuth setups complete!")
        print("   You can now run 'process new' with full holistic planning")
        print("\n   Run: python daily_planner.py")
    else:
        print("\n⚠️  Some OAuth setups failed")
        print("   Check error messages above and try again")

if __name__ == '__main__':
    main()
