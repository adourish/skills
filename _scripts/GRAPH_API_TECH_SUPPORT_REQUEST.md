# Microsoft Graph API Access Request - Tech Support

**Date:** February 22, 2026  
**Requestor:** Anthony Dourish (adourish@reisystems.com)  
**Purpose:** Enable automated daily planning workflow with work email and SharePoint integration

---

## SUMMARY

I need delegated user permissions configured for an Azure AD application to access Microsoft Graph API for automated email processing and document management. The application will run locally on my machine and access only my own work email, calendar, and files.

---

## REQUIRED PERMISSIONS

The following **delegated permissions** (not application permissions) are needed:

| Permission | Scope | Purpose |
|------------|-------|---------|
| `Mail.Read` | https://graph.microsoft.com/Mail.Read | Read work emails from Outlook |
| `Calendars.Read` | https://graph.microsoft.com/Calendars.Read | Read calendar events |
| `Files.Read.All` | https://graph.microsoft.com/Files.Read.All | Read OneDrive files |
| `Sites.Read.All` | https://graph.microsoft.com/Sites.Read.All | Read SharePoint documents |
| `User.Read` | https://graph.microsoft.com/User.Read | Read user profile |

**Note:** These are READ-ONLY permissions. No write/modify/delete access is requested.

---

## EXISTING AZURE APP REGISTRATION

An Azure AD application has already been created with the following details:

- **Application Name:** Email Calendar Automation
- **Client ID:** `1e1de7bf-6be5-4795-ad73-bf753ccb5ba5`
- **Tenant ID:** `31996441-7546-4120-826b-df0c3e239671` (REI Systems Inc)
- **Client Secret ID:** `bc6f3fe6-3f07-4857-b619-8e25983c1574`
- **Client Secret Expires:** August 21, 2026
- **Redirect URI:** `http://localhost:8080/callback`

---

## WHAT NEEDS TO BE CONFIGURED

### 1. API Permissions (in Azure Portal)
Navigate to: **Azure Portal → App Registrations → Email Calendar Automation → API Permissions**

Add the following **Microsoft Graph Delegated Permissions**:
- ✅ Mail.Read
- ✅ Calendars.Read  
- ✅ Files.Read.All
- ✅ Sites.Read.All
- ✅ User.Read

**Then click "Grant admin consent for REI Systems Inc"**

### 2. Authentication Settings
Navigate to: **Azure Portal → App Registrations → Email Calendar Automation → Authentication**

Verify:
- ✅ Platform: Public client/native (mobile & desktop)
- ✅ Redirect URI: `http://localhost:8080/callback`
- ✅ Allow public client flows: **Yes**

---

## AUTHENTICATION FLOW

The application uses **OAuth 2.0 Authorization Code Flow with PKCE** for delegated permissions:

1. User runs: `python setup_microsoft_oauth.py`
2. Browser opens to Microsoft login page
3. User signs in with work credentials (adourish@reisystems.com)
4. User grants consent for the requested permissions
5. Access token is saved locally at: `G:\My Drive\03_Areas\Keys\Microsoft365\token.json`
6. Token is used to make Graph API calls on behalf of the signed-in user

**Security:** Token is stored locally on my machine only. No credentials are shared or stored in code.

---

## CURRENT ERROR

When attempting to authenticate, the OAuth flow fails because the required API permissions have not been granted admin consent in Azure AD.

**Error Message:**
```
⚠️  Microsoft 365 token not found
   Run: python setup_oauth.py
```

**Root Cause:** The Azure app registration exists but lacks the necessary Graph API permissions or admin consent.

---

## WHAT I NEED FROM TECH SUPPORT

Please configure the Azure AD application "Email Calendar Automation" with:

1. ✅ Add the 5 delegated permissions listed above (Mail.Read, Calendars.Read, Files.Read.All, Sites.Read.All, User.Read)
2. ✅ Grant admin consent for these permissions
3. ✅ Verify authentication settings allow public client flows
4. ✅ Confirm redirect URI `http://localhost:8080/callback` is configured

**Estimated Time:** 5-10 minutes

---

## USE CASE

This automation will:
- Scan my Outlook inbox for urgent/actionable emails
- Identify recent SharePoint documents I've accessed
- Combine with personal Gmail and Google Drive items
- Generate a unified daily task list in Amplenote

**Benefits:**
- Reduces manual email triage time
- Ensures work items aren't missed
- Provides holistic view of personal + work tasks

---

## TECHNICAL DETAILS

**Python Library:** `msal` (Microsoft Authentication Library)  
**Authentication Type:** Delegated (user context)  
**Token Storage:** Local file system (encrypted Google Drive folder)  
**API Endpoint:** https://graph.microsoft.com/v1.0/  
**Tenant:** REI Systems Inc (reisystems.com)

---

## CONTACT

**Name:** Anthony Dourish  
**Email:** adourish@reisystems.com  
**Team:** DME BHCMIS Purple  

**Questions?** Feel free to reach out if you need any additional information or clarification.

---

## APPENDIX: VERIFICATION STEPS

After configuration, I will verify by running:

```bash
cd "G:\My Drive\06_Master_Guides\Scripts"
python setup_microsoft_oauth.py
```

**Expected Result:**
- Browser opens to Microsoft login
- I sign in with adourish@reisystems.com
- Consent screen shows the 5 permissions
- I click "Accept"
- Token is saved successfully
- Script shows: "✅ MICROSOFT 365 OAUTH SUCCESSFUL!"

**Test API Call:**
```bash
python daily_planner.py
```

**Expected Output:**
```
✅ Microsoft 365 authenticated (delegated)
📧 Checking Outlook (last 2 weeks)...
   Found X urgent items from Outlook
```

---

**Thank you for your assistance!**
