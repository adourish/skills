# Google Drive API - Setup & Usage Guide

## Quick Reference
**Use when:** Listing, reading, uploading, or searching files in Google Drive programmatically
**Don't use when:** You just want to browse files — open drive.google.com instead
**Trigger phrases:** "Google Drive API", "access Drive", "upload to Drive", "list Drive files", "Drive OAuth", "read from Drive"
**Time:** Initial OAuth setup ~10 minutes; subsequent use ~instant
**Command:** `python google_drive_client.py` (in `_scripts/`)

## ✅ Secure OAuth 2.0 Implementation

Uses the same Google OAuth 2.0 flow as Gmail — credentials stay local and secure.

---

## 📋 Prerequisites

1. **Google Cloud Project** with Drive API enabled
2. **OAuth 2.0 Credentials** (Desktop app type) — can reuse existing `credentials.json` if Gmail is already set up
3. **Python 3.7+** installed

---

## 🔧 Setup Steps

### Step 1: Enable Google Drive API

1. Go to https://console.cloud.google.com/apis/library
2. Search for **"Google Drive API"**
3. Click **"ENABLE"**

> If you already have OAuth credentials from Gmail setup, skip to Step 3.

---

### Step 2: Create OAuth Credentials (if not already done)

1. Go to https://console.cloud.google.com/apis/credentials
2. Click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
3. Choose **"Desktop app"** as application type
4. Name it (e.g., "Drive Client")
5. Click **"CREATE"** then **"DOWNLOAD JSON"**
6. Save as `credentials.json` in `G:\My Drive\`

⚠️ **NEVER share credentials.json or token_drive.json with anyone!**

---

### Step 3: Install Python Dependencies

```powershell
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

### Step 4: Create the Drive Client Script

Save `google_drive_client.py` to `G:\My Drive\06_Skills\_scripts\`:

```python
"""
Google Drive API Client
Usage:
  python google_drive_client.py list [--folder FOLDER_ID]
  python google_drive_client.py search QUERY
  python google_drive_client.py upload FILE_PATH [--folder FOLDER_ID]
  python google_drive_client.py download FILE_ID OUTPUT_PATH
"""

import os
import sys
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

# Scopes required — adjust as needed
SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',   # read files
    # 'https://www.googleapis.com/auth/drive.file',     # create/upload files (uncomment if needed)
]

CREDENTIALS_FILE = r'G:\My Drive\credentials.json'
TOKEN_FILE = r'G:\My Drive\token_drive.json'


def authenticate():
    """Authenticate and return Drive service."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)


def list_files(service, folder_id=None, page_size=20):
    """List files in Drive or a specific folder."""
    query = f"'{folder_id}' in parents" if folder_id else None
    results = service.files().list(
        q=query,
        pageSize=page_size,
        fields="files(id, name, mimeType, modifiedTime, size)"
    ).execute()
    files = results.get('files', [])
    if not files:
        print('No files found.')
    for f in files:
        size = f.get('size', 'N/A')
        print(f"[{f['id']}] {f['name']}  ({f['mimeType']})  modified: {f['modifiedTime']}  size: {size}")
    return files


def search_files(service, query_text, page_size=20):
    """Search for files by name or content."""
    query = f"fullText contains '{query_text}' or name contains '{query_text}'"
    results = service.files().list(
        q=query,
        pageSize=page_size,
        fields="files(id, name, mimeType, modifiedTime)"
    ).execute()
    files = results.get('files', [])
    if not files:
        print('No files found.')
    for f in files:
        print(f"[{f['id']}] {f['name']}  ({f['mimeType']})  modified: {f['modifiedTime']}")
    return files


def upload_file(service, file_path, folder_id=None):
    """Upload a file to Drive."""
    file_name = os.path.basename(file_path)
    metadata = {'name': file_name}
    if folder_id:
        metadata['parents'] = [folder_id]
    media = MediaFileUpload(file_path, resumable=True)
    result = service.files().create(body=metadata, media_body=media, fields='id,name').execute()
    print(f"Uploaded: {result['name']} (ID: {result['id']})")
    return result


def download_file(service, file_id, output_path):
    """Download a file from Drive."""
    request = service.files().get_media(fileId=file_id)
    with io.FileIO(output_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%")
    print(f"Saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Google Drive API Client')
    subparsers = parser.add_subparsers(dest='command')

    list_p = subparsers.add_parser('list', help='List files')
    list_p.add_argument('--folder', help='Folder ID to list')

    search_p = subparsers.add_parser('search', help='Search files')
    search_p.add_argument('query', help='Search query')

    upload_p = subparsers.add_parser('upload', help='Upload a file')
    upload_p.add_argument('file', help='Path to file to upload')
    upload_p.add_argument('--folder', help='Destination folder ID')

    download_p = subparsers.add_parser('download', help='Download a file')
    download_p.add_argument('file_id', help='Drive file ID')
    download_p.add_argument('output', help='Local output path')

    args = parser.parse_args()
    service = authenticate()

    if args.command == 'list':
        list_files(service, folder_id=args.folder)
    elif args.command == 'search':
        search_files(service, args.query)
    elif args.command == 'upload':
        upload_file(service, args.file, folder_id=args.folder)
    elif args.command == 'download':
        download_file(service, args.file_id, args.output)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
```

---

## 🚀 Common Commands

### List files in My Drive
```powershell
cd "G:\My Drive\06_Skills\_scripts"
python google_drive_client.py list
```

### List files in a specific folder
```powershell
python google_drive_client.py list --folder FOLDER_ID
```
> Get the folder ID from the URL when you open the folder in Drive: `drive.google.com/drive/folders/FOLDER_ID`

### Search for files
```powershell
python google_drive_client.py search "budget 2025"
```

### Upload a file
```powershell
python google_drive_client.py upload "C:\Reports\report.pdf"
python google_drive_client.py upload "C:\Reports\report.pdf" --folder FOLDER_ID
```

### Download a file
```powershell
python google_drive_client.py download FILE_ID "C:\Downloads\output.pdf"
```

---

## 🔒 Scopes Reference

| Scope | Access Level |
|-------|-------------|
| `drive.readonly` | Read all files (default — safest) |
| `drive.file` | Create/modify only files the app created |
| `drive.metadata.readonly` | Read file metadata only |
| `drive` | Full read/write access to all files |

Edit the `SCOPES` list in the script to match what you need. Re-delete `token_drive.json` and re-authenticate after changing scopes.

---

## 📁 Files Created

| File | Location | Purpose |
|------|----------|---------|
| `credentials.json` | `G:\My Drive\` | OAuth client credentials — keep secret |
| `token_drive.json` | `G:\My Drive\` | Access token — keep secret, auto-refreshes |
| `google_drive_client.py` | `G:\My Drive\06_Skills\_scripts\` | The Drive client script |

---

## 🔄 Token Management

### Token expires automatically
The script refreshes tokens automatically. No action needed.

### Force re-authentication
```powershell
del "G:\My Drive\token_drive.json"
python google_drive_client.py list
```

### Revoke access entirely
1. Go to https://myaccount.google.com/permissions
2. Find your app and click **"Remove Access"**
3. Delete `token_drive.json` locally

---

## 🔗 Integration with Other Skills

- **`skill_gmail_automation`** — Shares the same `credentials.json` and OAuth project
- **`skill_environments_credentials`** — Store Drive folder IDs in `environments.json` for easy reuse
- **`skill_file_organization`** — Use Drive API to sync local PARA structure with Drive
- **`skill_daily_planning`** — Read Drive files as part of daily workflow

---

## 🆘 Troubleshooting

### "credentials.json not found"
- Download from Google Cloud Console → Credentials
- Place in `G:\My Drive\`

### "Access Not Configured" / "Drive API not enabled"
- Go to https://console.cloud.google.com/apis/library
- Search "Google Drive API" and click ENABLE

### "insufficient authentication scopes"
- Delete `token_drive.json` and re-run (new scope requires re-consent)

### "File not found" on download
- Double-check the file ID from the `list` or `search` command output

### Browser doesn't open for auth
- Run PowerShell as administrator
- Or copy the URL printed in terminal and open manually

---

## 🚀 Quick Start Checklist

- [ ] Enable Google Drive API at Google Cloud Console
- [ ] Confirm `credentials.json` is in `G:\My Drive\`
- [ ] Install Python dependencies: `pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client`
- [ ] Save `google_drive_client.py` to `G:\My Drive\06_Skills\_scripts\`
- [ ] Run `python google_drive_client.py list` — browser opens for auth
- [ ] Grant permissions and verify file listing works

---

## 💡 Tips

1. **Reuse credentials** — If Gmail API is already set up, just enable Drive API in the same project
2. **Use readonly scope first** — Only expand permissions when you actually need write access
3. **Store folder IDs** — Save frequently-used folder IDs in `environments.json`
4. **Avoid `drive` full scope** — Prefer `drive.file` or `drive.readonly` for safety
5. **Token files are sensitive** — Add `token_drive.json` and `credentials.json` to `.gitignore`

---

**Remember: Your credentials and tokens are local and secure. Never share or commit them!**
