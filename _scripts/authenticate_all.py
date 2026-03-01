#!/usr/bin/env python3
"""
Authenticate All Services
Interactive script to set up all OAuth tokens for holistic daily planning
"""

import os
import sys
from pathlib import Path

def check_token_status():
    """Check which tokens are missing or expired"""
    gmail_token = Path(r'G:\My Drive\03_Areas\Keys\Gmail\token.json')
    ms_token = Path(r'G:\My Drive\03_Areas\Keys\Microsoft365\token.json')
    
    status = {
        'gmail': gmail_token.exists(),
        'microsoft': ms_token.exists()
    }
    
    return status

def main():
    print("\n" + "="*60)
    print("AUTHENTICATION SETUP FOR HOLISTIC DAILY PLANNING")
    print("="*60)
    
    status = check_token_status()
    
    print("\nCurrent Authentication Status:")
    print(f"  {'✅' if status['gmail'] else '❌'} Gmail/Google Drive")
    print(f"  {'✅' if status['microsoft'] else '❌'} Microsoft 365 (Outlook/SharePoint)")
    
    missing = [k for k, v in status.items() if not v]
    
    if not missing:
        print("\n✅ All tokens are present!")
        print("\nNote: Tokens may still be expired. Run 'process new' to verify.")
        return
    
    print(f"\n⚠️  Missing: {', '.join(missing)}")
    print("\nWhat would you like to do?")
    print("  1. Set up Gmail/Google Drive OAuth")
    print("  2. Set up Microsoft 365 OAuth")
    print("  3. Set up both")
    print("  4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1" or choice == "3":
        print("\n" + "="*60)
        print("GMAIL/GOOGLE DRIVE SETUP")
        print("="*60)
        print("\nTo set up Gmail and Google Drive:")
        print("1. Delete existing token if present:")
        print("   del \"G:\\My Drive\\03_Areas\\Keys\\Gmail\\token.json\"")
        print("\n2. Run the daily planner - it will trigger OAuth flow:")
        print("   python daily_planner.py")
        print("\n3. A browser will open for you to sign in with your Google account")
        print("4. Grant permissions for Gmail and Drive access")
        
    if choice == "2" or choice == "3":
        print("\n" + "="*60)
        print("MICROSOFT 365 SETUP")
        print("="*60)
        print("\nTo set up Microsoft 365 (Outlook/SharePoint):")
        print("1. Run the OAuth setup script:")
        print("   python setup_microsoft_oauth.py")
        print("\n2. A browser will open for you to sign in with your work account")
        print("3. Grant permissions for Mail, Calendar, Files, and Sites")
        print("\n⚠️  Note: Your organization may require admin approval")
        print("   If blocked, contact your IT administrator")
        
        if choice == "2":
            run_now = input("\nRun Microsoft OAuth setup now? (y/n): ").strip().lower()
            if run_now == 'y':
                os.system('python setup_microsoft_oauth.py')
    
    if choice == "4":
        print("\nExiting...")
        return
    
    print("\n" + "="*60)
    print("After authentication, run 'process new' to generate your daily plan!")
    print("="*60)

if __name__ == '__main__':
    main()
