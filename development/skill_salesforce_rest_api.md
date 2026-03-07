# Salesforce REST API Development

## Overview
Patterns for authenticating with Salesforce APIs, obtaining bearer tokens, and making REST API calls to Salesforce orgs. Covers OAuth 2.0 flows, token management, and common API patterns.

## OAuth 2.0 Authentication

### 1. Username-Password Flow (Development/Testing)

**Use Case:** Server-to-server integration, automated scripts, testing

```http
POST https://[instance].salesforce.com/services/oauth2/token
Content-Type: application/x-www-form-urlencoded

grant_type=password
&client_id=[CONNECTED_APP_CLIENT_ID]
&client_secret=[CONNECTED_APP_CLIENT_SECRET]
&username=[USERNAME]
&password=[PASSWORD][SECURITY_TOKEN]
```

**Example:**
```http
POST https://instance--sandbox.sandbox.my.salesforce.com/services/oauth2/token
Content-Type: application/x-www-form-urlencoded

grant_type=password
&client_id=[YOUR_CONNECTED_APP_CLIENT_ID]
&client_secret=[YOUR_CONNECTED_APP_CLIENT_SECRET]
&username=user@example.com.sandbox
&password=MyPassword123MySecurityToken
```

**Response:**
```json
{
    "access_token": "00D...token...",
    "instance_url": "https://instance.salesforce.com",
    "id": "https://login.salesforce.com/id/orgId/userId",
    "token_type": "Bearer",
    "issued_at": "1234567890",
    "signature": "base64signature"
}
```

**PowerShell Example:**
```powershell
$body = @{
    grant_type = "password"
    client_id = $env:SF_CLIENT_ID
    client_secret = $env:SF_CLIENT_SECRET
    username = $env:SF_USERNAME
    password = "$($env:SF_PASSWORD)$($env:SF_SECURITY_TOKEN)"
}

$response = Invoke-RestMethod -Uri "https://login.salesforce.com/services/oauth2/token" -Method Post -Body $body
$accessToken = $response.access_token
$instanceUrl = $response.instance_url
```

**Python Example:**
```python
import requests
import os

auth_url = "https://login.salesforce.com/services/oauth2/token"
auth_data = {
    "grant_type": "password",
    "client_id": os.getenv("SF_CLIENT_ID"),
    "client_secret": os.getenv("SF_CLIENT_SECRET"),
    "username": os.getenv("SF_USERNAME"),
    "password": f"{os.getenv('SF_PASSWORD')}{os.getenv('SF_SECURITY_TOKEN')}"
}

response = requests.post(auth_url, data=auth_data)
auth_response = response.json()
access_token = auth_response["access_token"]
instance_url = auth_response["instance_url"]
```

### 2. Web Server Flow (Production)

**Use Case:** Web applications, user authentication

**Step 1: Redirect to Authorization URL**
```http
GET https://login.salesforce.com/services/oauth2/authorize
  ?response_type=code
  &client_id=[CLIENT_ID]
  &redirect_uri=[REDIRECT_URI]
  &scope=api refresh_token
```

**Step 2: Exchange Code for Token**
```http
POST https://login.salesforce.com/services/oauth2/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&client_id=[CLIENT_ID]
&client_secret=[CLIENT_SECRET]
&redirect_uri=[REDIRECT_URI]
&code=[AUTHORIZATION_CODE]
```

### 3. Refresh Token Flow

**Use Case:** Renew expired access tokens

```http
POST https://login.salesforce.com/services/oauth2/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token
&client_id=[CLIENT_ID]
&client_secret=[CLIENT_SECRET]
&refresh_token=[REFRESH_TOKEN]
```

**PowerShell Example:**
```powershell
$body = @{
    grant_type = "refresh_token"
    client_id = $env:SF_CLIENT_ID
    client_secret = $env:SF_CLIENT_SECRET
    refresh_token = $env:SF_REFRESH_TOKEN
}

$response = Invoke-RestMethod -Uri "https://login.salesforce.com/services/oauth2/token" -Method Post -Body $body
$accessToken = $response.access_token
```

## Using Bearer Tokens

### 1. Authorization Header

**All Salesforce REST API calls require the Bearer token in the Authorization header:**

```http
GET https://[instance_url]/services/data/v60.0/sobjects/Account/[ACCOUNT_ID]
Authorization: Bearer [ACCESS_TOKEN]
```

**PowerShell Example:**
```powershell
$headers = @{
    "Authorization" = "Bearer $accessToken"
    "Content-Type" = "application/json"
}

$response = Invoke-RestMethod -Uri "$instanceUrl/services/data/v60.0/sobjects/Account/$accountId" -Headers $headers
```

**Python Example:**
```python
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

response = requests.get(f"{instance_url}/services/data/v60.0/sobjects/Account/{account_id}", headers=headers)
data = response.json()
```

**JavaScript Example:**
```javascript
const headers = {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json'
};

const response = await fetch(`${instanceUrl}/services/data/v60.0/sobjects/Account/${accountId}`, {
    headers: headers
});
const data = await response.json();
```

## Common API Endpoints

### 1. Query (SOQL)

```http
GET https://[instance_url]/services/data/v60.0/query?q=SELECT+Id,Name+FROM+Account+LIMIT+10
Authorization: Bearer [ACCESS_TOKEN]
```

**PowerShell:**
```powershell
$query = "SELECT Id, Name, Industry FROM Account WHERE Industry = 'Healthcare' LIMIT 10"
$encodedQuery = [System.Web.HttpUtility]::UrlEncode($query)
$uri = "$instanceUrl/services/data/v60.0/query?q=$encodedQuery"

$response = Invoke-RestMethod -Uri $uri -Headers $headers
$records = $response.records
```

### 2. Create Record (POST)

```http
POST https://[instance_url]/services/data/v60.0/sobjects/Account
Authorization: Bearer [ACCESS_TOKEN]
Content-Type: application/json

{
    "Name": "New Account",
    "Industry": "Healthcare",
    "BillingCity": "Washington"
}
```

**PowerShell:**
```powershell
$accountData = @{
    Name = "New Account"
    Industry = "Healthcare"
    BillingCity = "Washington"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "$instanceUrl/services/data/v60.0/sobjects/Account" -Method Post -Headers $headers -Body $accountData
$newAccountId = $response.id
```

### 3. Update Record (PATCH)

```http
PATCH https://[instance_url]/services/data/v60.0/sobjects/Account/[ACCOUNT_ID]
Authorization: Bearer [ACCESS_TOKEN]
Content-Type: application/json

{
    "Industry": "Technology",
    "Phone": "555-1234"
}
```

**PowerShell:**
```powershell
$updateData = @{
    Industry = "Technology"
    Phone = "555-1234"
} | ConvertTo-Json

Invoke-RestMethod -Uri "$instanceUrl/services/data/v60.0/sobjects/Account/$accountId" -Method Patch -Headers $headers -Body $updateData
```

### 4. Delete Record (DELETE)

```http
DELETE https://[instance_url]/services/data/v60.0/sobjects/Account/[ACCOUNT_ID]
Authorization: Bearer [ACCESS_TOKEN]
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "$instanceUrl/services/data/v60.0/sobjects/Account/$accountId" -Method Delete -Headers $headers
```

### 5. Custom Apex REST Endpoint

```http
GET https://[instance_url]/services/apexrest/MyCustomEndpoint/[PARAM]
Authorization: Bearer [ACCESS_TOKEN]
```

**Apex REST Class:**
```apex
@RestResource(urlMapping='/MyCustomEndpoint/*')
global with sharing class MyCustomEndpoint {
    
    @HttpGet
    global static MyResponse doGet() {
        RestRequest req = RestContext.request;
        RestResponse res = RestContext.response;
        
        String param = req.requestURI.substring(req.requestURI.lastIndexOf('/') + 1);
        
        // Process request
        MyResponse response = new MyResponse();
        response.status = 'success';
        response.data = getData(param);
        
        return response;
    }
    
    @HttpPost
    global static MyResponse doPost(MyRequest requestData) {
        // Process POST request
        MyResponse response = new MyResponse();
        response.status = 'success';
        return response;
    }
}
```

**Calling Custom Endpoint:**
```powershell
$response = Invoke-RestMethod -Uri "$instanceUrl/services/apexrest/MyCustomEndpoint/12345" -Headers $headers
```

## Token Management Best Practices

### 1. Store Credentials Securely

```powershell
# ✅ GOOD - Load from secure location
$envs = & 'G:\My Drive\03_Areas\Keys\Environments\Load-Environments.ps1'
$clientId = $envs.SF_CLIENT_ID
$clientSecret = $envs.SF_CLIENT_SECRET

# ❌ BAD - Hardcoded credentials
$clientId = "3MVG9Ifyu2h_RmVm..."
$clientSecret = "47CB52A34365E36C..."
```

### 2. Token Expiration Handling

```powershell
function Get-SalesforceToken {
    param([string]$username, [string]$password, [string]$securityToken)
    
    $body = @{
        grant_type = "password"
        client_id = $env:SF_CLIENT_ID
        client_secret = $env:SF_CLIENT_SECRET
        username = $username
        password = "$password$securityToken"
    }
    
    try {
        $response = Invoke-RestMethod -Uri "https://login.salesforce.com/services/oauth2/token" -Method Post -Body $body
        return @{
            AccessToken = $response.access_token
            InstanceUrl = $response.instance_url
            IssuedAt = [DateTimeOffset]::FromUnixTimeMilliseconds($response.issued_at).DateTime
        }
    } catch {
        Write-Error "Failed to obtain token: $_"
        return $null
    }
}

function Invoke-SalesforceApi {
    param(
        [string]$endpoint,
        [hashtable]$token,
        [string]$method = "GET",
        [object]$body = $null
    )
    
    # Check if token is expired (tokens typically last 2 hours)
    $tokenAge = (Get-Date) - $token.IssuedAt
    if ($tokenAge.TotalHours -gt 1.5) {
        Write-Warning "Token is old, consider refreshing"
    }
    
    $headers = @{
        "Authorization" = "Bearer $($token.AccessToken)"
        "Content-Type" = "application/json"
    }
    
    $uri = "$($token.InstanceUrl)$endpoint"
    
    $params = @{
        Uri = $uri
        Headers = $headers
        Method = $method
    }
    
    if ($body) {
        $params.Body = ($body | ConvertTo-Json -Depth 10)
    }
    
    Invoke-RestMethod @params
}
```

### 3. Environment-Specific URLs

```powershell
# Production
$authUrl = "https://login.salesforce.com/services/oauth2/token"

# Sandbox
$authUrl = "https://test.salesforce.com/services/oauth2/token"

# Custom Domain
$authUrl = "https://mydomain.my.salesforce.com/services/oauth2/token"
```

## Complete Example: CRUD Operations

```powershell
# 1. Authenticate
$envs = & 'G:\My Drive\03_Areas\Keys\Environments\Load-Environments.ps1'

$authBody = @{
    grant_type = "password"
    client_id = $envs.SF_CLIENT_ID
    client_secret = $envs.SF_CLIENT_SECRET
    username = $envs.SF_USERNAME
    password = "$($envs.SF_PASSWORD)$($envs.SF_SECURITY_TOKEN)"
}

$authResponse = Invoke-RestMethod -Uri "https://test.salesforce.com/services/oauth2/token" -Method Post -Body $authBody
$accessToken = $authResponse.access_token
$instanceUrl = $authResponse.instance_url

$headers = @{
    "Authorization" = "Bearer $accessToken"
    "Content-Type" = "application/json"
}

# 2. Create Account
$newAccount = @{
    Name = "Test Account"
    Industry = "Healthcare"
    BillingCity = "Washington"
} | ConvertTo-Json

$createResponse = Invoke-RestMethod -Uri "$instanceUrl/services/data/v60.0/sobjects/Account" -Method Post -Headers $headers -Body $newAccount
$accountId = $createResponse.id
Write-Host "Created Account: $accountId"

# 3. Read Account
$account = Invoke-RestMethod -Uri "$instanceUrl/services/data/v60.0/sobjects/Account/$accountId" -Headers $headers
Write-Host "Account Name: $($account.Name)"

# 4. Update Account
$updateData = @{
    Phone = "555-1234"
    Website = "https://example.com"
} | ConvertTo-Json

Invoke-RestMethod -Uri "$instanceUrl/services/data/v60.0/sobjects/Account/$accountId" -Method Patch -Headers $headers -Body $updateData
Write-Host "Updated Account"

# 5. Query Accounts
$query = "SELECT Id, Name, Industry FROM Account WHERE Name LIKE 'Test%' LIMIT 10"
$encodedQuery = [System.Web.HttpUtility]::UrlEncode($query)
$queryResponse = Invoke-RestMethod -Uri "$instanceUrl/services/data/v60.0/query?q=$encodedQuery" -Headers $headers

foreach ($record in $queryResponse.records) {
    Write-Host "$($record.Id): $($record.Name) - $($record.Industry)"
}

# 6. Delete Account
Invoke-RestMethod -Uri "$instanceUrl/services/data/v60.0/sobjects/Account/$accountId" -Method Delete -Headers $headers
Write-Host "Deleted Account"
```

## Error Handling

### 1. Common Error Responses

```json
// 401 Unauthorized - Invalid/Expired Token
{
    "error": "invalid_grant",
    "error_description": "authentication failure"
}

// 400 Bad Request - Invalid Data
[
    {
        "message": "Required fields are missing: [Name]",
        "errorCode": "REQUIRED_FIELD_MISSING",
        "fields": ["Name"]
    }
]

// 404 Not Found - Record Doesn't Exist
[
    {
        "message": "The requested resource does not exist",
        "errorCode": "NOT_FOUND"
    }
]
```

### 2. Error Handling Pattern

```powershell
function Invoke-SalesforceApiSafe {
    param(
        [string]$uri,
        [hashtable]$headers,
        [string]$method = "GET",
        [object]$body = $null
    )
    
    try {
        $params = @{
            Uri = $uri
            Headers = $headers
            Method = $method
        }
        
        if ($body) {
            $params.Body = ($body | ConvertTo-Json -Depth 10)
        }
        
        $response = Invoke-RestMethod @params
        return @{
            Success = $true
            Data = $response
            Error = $null
        }
        
    } catch {
        $errorDetails = $_.ErrorDetails.Message | ConvertFrom-Json
        
        return @{
            Success = $false
            Data = $null
            Error = @{
                StatusCode = $_.Exception.Response.StatusCode.value__
                Message = $errorDetails[0].message
                ErrorCode = $errorDetails[0].errorCode
            }
        }
    }
}

# Usage
$result = Invoke-SalesforceApiSafe -uri "$instanceUrl/services/data/v60.0/sobjects/Account/$accountId" -headers $headers

if ($result.Success) {
    Write-Host "Account: $($result.Data.Name)"
} else {
    Write-Error "Error $($result.Error.StatusCode): $($result.Error.Message)"
}
```

## API Versioning

```powershell
# Always specify API version
$apiVersion = "v60.0"  # Winter '25

# Query endpoint
$queryUrl = "$instanceUrl/services/data/$apiVersion/query"

# SObject endpoint
$sobjectUrl = "$instanceUrl/services/data/$apiVersion/sobjects/Account"

# Custom Apex REST (no version in URL)
$customUrl = "$instanceUrl/services/apexrest/MyEndpoint"
```

## Connected App Setup

### 1. Create Connected App in Salesforce

1. Setup → App Manager → New Connected App
2. Basic Information:
   - Connected App Name: `My Integration App`
   - API Name: `My_Integration_App`
   - Contact Email: `admin@example.com`
3. API (Enable OAuth Settings):
   - ✅ Enable OAuth Settings
   - Callback URL: `https://localhost:8080/callback` (or your URL)
   - Selected OAuth Scopes:
     - Full access (full)
     - Perform requests on your behalf at any time (refresh_token, offline_access)
     - Access and manage your data (api)
4. Save and note:
   - Consumer Key (Client ID)
   - Consumer Secret (Client Secret)

### 2. Security Considerations

- ✅ Use IP restrictions for production
- ✅ Enable refresh token policy
- ✅ Set session timeout policies
- ✅ Use least privilege OAuth scopes
- ✅ Rotate client secrets regularly

## Quick Reference

### Authentication Endpoints
```
Production: https://login.salesforce.com/services/oauth2/token
Sandbox: https://test.salesforce.com/services/oauth2/token
Custom Domain: https://[domain].my.salesforce.com/services/oauth2/token
```

### Common API Endpoints
```
Query: /services/data/v60.0/query?q=[SOQL]
SObject: /services/data/v60.0/sobjects/[OBJECT]/[ID]
Apex REST: /services/apexrest/[ENDPOINT]
Composite: /services/data/v60.0/composite
Bulk API: /services/data/v60.0/jobs/ingest
```

### Required Headers
```
Authorization: Bearer [ACCESS_TOKEN]
Content-Type: application/json
Accept: application/json
```

### Token Lifespan
- Access Token: ~2 hours (configurable)
- Refresh Token: Until revoked or expired by policy

## Related Skills
- `skill_salesforce_development.md` - Apex REST endpoint development
- `skill_soql_sosl.md` - Query patterns for API calls
- `skill_powershell_automation.md` - PowerShell scripting patterns
