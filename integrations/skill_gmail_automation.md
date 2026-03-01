# Gmail Organizer - Setup Guide

## ✅ Secure OAuth 2.0 Implementation

This script uses proper OAuth 2.0 flow - your credentials stay secure!

---

## 📋 Prerequisites

1. **Google Cloud Project** with Gmail API enabled
2. **OAuth 2.0 Credentials** (Desktop app type)
3. **Python 3.7+** installed

---

## 🔧 Setup Steps

### Step 1: Create OAuth Credentials (IMPORTANT - Do This First!)

1. Go to https://console.cloud.google.com/apis/credentials
2. Select your project (or create a new one)
3. Click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
4. Choose **"Desktop app"** as application type
5. Name it (e.g., "Gmail Organizer")
6. Click **"CREATE"**
7. Click **"DOWNLOAD JSON"** button
8. Save the file as `credentials.json` in `G:\My Drive\`

⚠️ **NEVER share credentials.json or token.json with anyone!**

---

### Step 2: Enable Gmail API

1. Go to https://console.cloud.google.com/apis/library
2. Search for "Gmail API"
3. Click **"ENABLE"**

---

### Step 3: Install Python Dependencies

Open PowerShell and run:

```powershell
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

### Step 4: Run the Organizer (Dry Run)

```powershell
cd "G:\My Drive"
python gmail_organizer.py
```

**What happens:**
- Browser opens for you to authorize access
- You log in to your Google account
- You grant permissions (read/modify emails, manage labels)
- Token is saved to `token.json` (secure, local only)
- Script analyzes your inbox
- Shows what it WOULD do (no actual changes)

---

### Step 5: Apply Changes (When Ready)

```powershell
python gmail_organizer.py --execute
```

This will:
- ✅ Create organization labels (Work, Personal, Finance, etc.)
- ✅ Apply labels to existing emails based on rules
- ✅ Show filter suggestions

---

## 📁 Files Created

- **credentials.json** - OAuth client credentials (keep secure!)
- **token.json** - Your access token (keep secure!)
- **gmail_organizer.py** - The organization script

---

## 🏷️ Labels Created

The script creates these labels:

- **Work** - Work-related emails
- **Personal** - Personal emails
- **Finance** - Bills, invoices, bank statements
- **Shopping** - Orders, receipts, shipping
- **Social** - Social media notifications
- **Newsletters** - Newsletters and subscriptions
- **Promotions** - Marketing emails
- **Important** - Flagged as important
- **ToRead** - Emails to read later
- **Archive/2024** - Archive for 2024
- **Archive/2023** - Archive for 2023

---

## 🎯 Organization Rules

The script applies these rules:

### Newsletters
- Detects: "newsletter" in sender, "unsubscribe" links
- Action: Label as "Newsletters"

### Shopping
- Detects: "order", "receipt", "shipped", "delivery" in subject
- Action: Label as "Shopping"

### Social Media
- Detects: facebook.com, twitter.com, linkedin.com, instagram.com
- Action: Label as "Social"

### Finance
- Detects: "invoice", "payment", "bank", "statement" in subject
- Action: Label as "Finance"

---

## 🔒 Security Features

✅ **OAuth 2.0 Flow** - Industry standard authentication  
✅ **Local Token Storage** - Tokens stored only on your machine  
✅ **No Hardcoded Credentials** - Credentials never in code  
✅ **Minimal Permissions** - Only requests necessary scopes  
✅ **Token Refresh** - Automatically refreshes expired tokens  

---

## 🛠️ Customization

Edit `gmail_organizer.py` to customize:

### Add More Labels
```python
labels_to_create = [
    "Work",
    "Personal",
    "YourCustomLabel",  # Add here
    # ...
]
```

### Add More Rules
```python
# In organize_existing_emails function
if 'your_keyword' in subject:
    labels_to_add.append(label_ids['YourLabel'])
```

### Change Analysis Depth
```python
# Analyze more/fewer emails
analyze_inbox(service, max_messages=500)  # Default: 100
```

---

## ⚠️ Important Notes

1. **Backup First** - Consider exporting emails before organizing
2. **Test with Dry Run** - Always run without --execute first
3. **Start Small** - Process 100 emails first, then increase
4. **Keep Tokens Safe** - Never commit token.json to git
5. **Revoke Old Credentials** - Delete the compromised ones from earlier

---

## 🔄 Token Management

### If Token Expires
The script automatically refreshes tokens. No action needed.

### If You Want to Re-authenticate
Delete `token.json` and run the script again.

### If You Want to Revoke Access
1. Go to https://myaccount.google.com/permissions
2. Find "Gmail Organizer" (or your app name)
3. Click "Remove Access"
4. Delete `token.json` locally

---

## 📊 What the Script Does

### Analysis Phase
- Scans recent emails (default: 100)
- Identifies top senders by domain
- Finds common subject keywords
- Suggests organization strategies

### Organization Phase
- Creates label structure
- Applies labels based on rules
- Processes existing emails
- Suggests filters for future emails

### Dry Run vs Execute
- **Dry Run** (default): Shows what would happen, no changes
- **Execute** (--execute flag): Actually applies changes

---

## 🚀 Quick Start Checklist

- [ ] Create OAuth credentials at Google Cloud Console
- [ ] Download credentials.json to G:\My Drive\
- [ ] Enable Gmail API
- [ ] Install Python dependencies
- [ ] Run dry run: `python gmail_organizer.py`
- [ ] Review output
- [ ] Run execute: `python gmail_organizer.py --execute`
- [ ] Verify results in Gmail

---

## 💡 Tips

1. **Start Conservative** - Use dry run multiple times
2. **Customize Rules** - Adjust based on your email patterns
3. **Create Filters** - Set up Gmail filters for ongoing organization
4. **Regular Cleanup** - Run periodically to maintain organization
5. **Archive Old Emails** - Use Archive/YYYY labels for old emails

---

## 🆘 Troubleshooting

### "credentials.json not found"
- Make sure you downloaded it from Google Cloud Console
- Place it in the same folder as gmail_organizer.py

### "Access denied" error
- Make sure Gmail API is enabled
- Check OAuth consent screen is configured
- Verify scopes are correct

### "Token expired" error
- Delete token.json and re-authenticate
- Script should auto-refresh, but manual re-auth works too

### Browser doesn't open
- Check firewall settings
- Try running as administrator
- Manually copy the URL from terminal

---

## 📞 Next Steps

After setup:
1. Run dry run to see analysis
2. Review suggested labels and rules
3. Customize rules for your needs
4. Run with --execute when ready
5. Create Gmail filters for ongoing organization

---

**Remember: Your credentials and tokens are secure and local. Never share them!**
