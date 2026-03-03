# Azure SQL Database Queries

**Last Updated:** March 2, 2026  
**Purpose:** Query Azure SQL databases for PRS/PRM package data and other enterprise data sources  
**Primary Database:** INT (az-hs-mi-int.71b05803ca2a.database.windows.net)

---

## Table of Contents

1. [Overview](#overview)
2. [Database Connections](#database-connections)
3. [Credentials Management](#credentials-management)
4. [Connection Methods](#connection-methods)
5. [PRS Package Queries](#prs-package-queries)
6. [Common Query Patterns](#common-query-patterns)
7. [Python Integration](#python-integration)
8. [PowerShell Integration](#powershell-integration)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)
11. [Related Skills](#related-skills)

---

## Overview

Azure SQL databases host enterprise data including PRS/PRM package definitions, historical data, and legacy system information. This skill covers querying these databases using various tools and languages.

### Key Databases

**INT Database (Primary):**
- **Server:** `az-hs-mi-int.71b05803ca2a.database.windows.net`
- **Database:** `BHCMIS`
- **Purpose:** PRS package data, historical analysis
- **Access:** Read-only via `qauser` account

### Use Cases

- Extract PRS package metadata for analysis
- Query historical form data
- Generate Excel reports from database data
- Validate data migrations
- Research legacy system structures

---

## Database Connections

### INT Database Connection Details

**Server Information:**
```
Server: az-hs-mi-int.71b05803ca2a.database.windows.net
Database: BHCMIS
Port: 1433 (default)
Authentication: SQL Server Authentication
```

**Credentials:**
```
Username: qauser
Password: qauser
```

**Connection String:**
```
Server=az-hs-mi-int.71b05803ca2a.database.windows.net;Database=BHCMIS;User Id=qauser;Password=qauser;Encrypt=True;TrustServerCertificate=False;
```

### Key Tables

**PRS Package Tables:**

1. **Lu_Package** (118 Progress Reports)
   - Primary table for Progress Report packages
   - Contains package metadata, OMB numbers, years
   - Used for 2008-2025 package analysis

2. **LU_PRS_Package** (45 Supplemental Packages)
   - Supplemental package definitions
   - Additional package types and configurations
   - Total combined: 163 packages

---

## Credentials Management

### CRITICAL: Load from Environments

**User Rule:** All environment credentials MUST be loaded from:
```
G:\My Drive\03_Areas\Keys\Environments\
```

**NEVER** reference credentials from project directories.

**ALWAYS** use:
```powershell
$envs = & 'G:\My Drive\03_Areas\Keys\Environments\Load-Environments.ps1'
```

### Environment Configuration

The `environments.json` file should contain:

```json
{
  "azure_sql": {
    "int": {
      "server": "az-hs-mi-int.71b05803ca2a.database.windows.net",
      "database": "BHCMIS",
      "username": "qauser",
      "password": "qauser",
      "port": 1433,
      "encrypt": true,
      "trust_server_certificate": false
    }
  }
}
```

---

## Connection Methods

### Method 1: SQL Server Management Studio (SSMS)

**Steps:**
1. Open SSMS
2. Server name: `az-hs-mi-int.71b05803ca2a.database.windows.net`
3. Authentication: SQL Server Authentication
4. Login: `qauser`
5. Password: `qauser`
6. Click Connect

**Pros:**
- Visual query builder
- Easy result exploration
- Export to CSV/Excel

**Cons:**
- Manual process
- Not scriptable

### Method 2: Azure Data Studio

**Steps:**
1. Open Azure Data Studio
2. New Connection
3. Server: `az-hs-mi-int.71b05803ca2a.database.windows.net`
4. Authentication type: SQL Login
5. User name: `qauser`
6. Password: `qauser`
7. Database: `BHCMIS`
8. Encrypt: True
9. Trust server certificate: False

**Pros:**
- Modern interface
- Notebook support
- Cross-platform

**Cons:**
- Requires installation

### Method 3: Python (Recommended for Automation)

See [Python Integration](#python-integration) section below.

### Method 4: PowerShell

See [PowerShell Integration](#powershell-integration) section below.

---

## PRS Package Queries

### Query All Progress Report Packages

**Lu_Package Table (118 packages):**

```sql
SELECT 
    PackageId,
    PackageName,
    Description,
    ShortName,
    PackagePath,
    'Lu_Package' AS SourceTable,
    PackageType,
    OMBNumber,
    Year,
    CreatedDate,
    LastUpdateDate
FROM Lu_Package
ORDER BY Year DESC, PackageName;
```

### Query Supplemental Packages

**LU_PRS_Package Table (45 packages):**

```sql
SELECT 
    PackageId,
    PackageName,
    Description,
    ShortName,
    PackagePath,
    'LU_PRS_Package' AS SourceTable,
    PackageType,
    OMBNumber,
    Year,
    CreatedDate,
    LastUpdateDate
FROM LU_PRS_Package
ORDER BY Year DESC, PackageName;
```

### Query All Packages Combined

**Union of both tables (163 total):**

```sql
SELECT 
    PackageId,
    PackageName,
    Description,
    ShortName,
    PackagePath,
    'Lu_Package' AS SourceTable,
    PackageType,
    OMBNumber,
    Year,
    CreatedDate,
    LastUpdateDate
FROM Lu_Package

UNION ALL

SELECT 
    PackageId,
    PackageName,
    Description,
    ShortName,
    PackagePath,
    'LU_PRS_Package' AS SourceTable,
    PackageType,
    OMBNumber,
    Year,
    CreatedDate,
    LastUpdateDate
FROM LU_PRS_Package

ORDER BY Year DESC, PackageName;
```

### Query Packages by Year

```sql
SELECT 
    PackageId,
    PackageName,
    PackageType,
    OMBNumber,
    Year
FROM Lu_Package
WHERE Year = 2025
ORDER BY PackageName;
```

### Query Packages by Type

```sql
SELECT 
    PackageType,
    COUNT(*) AS PackageCount
FROM (
    SELECT PackageType FROM Lu_Package
    UNION ALL
    SELECT PackageType FROM LU_PRS_Package
) AS AllPackages
GROUP BY PackageType
ORDER BY PackageCount DESC;
```

### Query Recent Packages

```sql
SELECT TOP 10
    PackageName,
    Year,
    CreatedDate,
    LastUpdateDate
FROM Lu_Package
ORDER BY LastUpdateDate DESC;
```

---

## Common Query Patterns

### Count Records

```sql
-- Count Lu_Package records
SELECT COUNT(*) AS TotalPackages FROM Lu_Package;

-- Count LU_PRS_Package records
SELECT COUNT(*) AS TotalSupplementalPackages FROM LU_PRS_Package;

-- Count all packages
SELECT 
    (SELECT COUNT(*) FROM Lu_Package) + 
    (SELECT COUNT(*) FROM LU_PRS_Package) AS TotalAllPackages;
```

### Filter by Date Range

```sql
SELECT 
    PackageName,
    Year,
    CreatedDate
FROM Lu_Package
WHERE CreatedDate BETWEEN '2020-01-01' AND '2025-12-31'
ORDER BY CreatedDate DESC;
```

### Search by Name Pattern

```sql
SELECT 
    PackageId,
    PackageName,
    Description
FROM Lu_Package
WHERE PackageName LIKE '%Progress%'
   OR Description LIKE '%Progress%'
ORDER BY PackageName;
```

### Group by Year

```sql
SELECT 
    Year,
    COUNT(*) AS PackageCount,
    MIN(CreatedDate) AS FirstCreated,
    MAX(LastUpdateDate) AS LastUpdated
FROM Lu_Package
GROUP BY Year
ORDER BY Year DESC;
```

### Find Packages with Specific OMB Number

```sql
SELECT 
    PackageName,
    OMBNumber,
    Year,
    PackageType
FROM Lu_Package
WHERE OMBNumber = '0915-0285'
ORDER BY Year DESC;
```

---

## Python Integration

### Install Required Package

```bash
pip install pyodbc
```

### Basic Connection

```python
import pyodbc
import json

# Load credentials from environments.json
with open('G:/My Drive/03_Areas/Keys/Environments/environments.json', 'r') as f:
    envs = json.load(f)

# Get INT database config
int_config = envs['azure_sql']['int']

# Build connection string
conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={int_config['server']};"
    f"DATABASE={int_config['database']};"
    f"UID={int_config['username']};"
    f"PWD={int_config['password']};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
)

# Connect
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Execute query
cursor.execute("SELECT TOP 10 * FROM Lu_Package")

# Fetch results
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close connection
cursor.close()
conn.close()
```

### Query to DataFrame

```python
import pyodbc
import pandas as pd
import json

# Load credentials
with open('G:/My Drive/03_Areas/Keys/Environments/environments.json', 'r') as f:
    envs = json.load(f)

int_config = envs['azure_sql']['int']

# Build connection string
conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={int_config['server']};"
    f"DATABASE={int_config['database']};"
    f"UID={int_config['username']};"
    f"PWD={int_config['password']};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
)

# Query to DataFrame
query = """
SELECT 
    PackageId,
    PackageName,
    Description,
    Year,
    PackageType,
    OMBNumber
FROM Lu_Package
ORDER BY Year DESC
"""

df = pd.read_sql(query, conn_str)
print(df.head())

# Export to CSV
df.to_csv('prs_packages.csv', index=False)

# Export to Excel
df.to_excel('prs_packages.xlsx', index=False, sheet_name='Packages')
```

### Complete PRS Package Extraction Script

```python
import pyodbc
import pandas as pd
import json
from datetime import datetime

def extract_prs_packages():
    """
    Extract all PRS packages from INT database
    Used for PRS Excel Master Documentation regeneration
    """
    
    # Load credentials from environments.json
    with open('G:/My Drive/03_Areas/Keys/Environments/environments.json', 'r') as f:
        envs = json.load(f)
    
    int_config = envs['azure_sql']['int']
    
    # Build connection string
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={int_config['server']};"
        f"DATABASE={int_config['database']};"
        f"UID={int_config['username']};"
        f"PWD={int_config['password']};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
    )
    
    # Query all packages from both tables
    query = """
    SELECT 
        PackageId,
        PackageName,
        Description,
        ShortName,
        PackagePath,
        'Lu_Package' AS SourceTable,
        PackageType,
        OMBNumber,
        Year,
        CreatedDate,
        LastUpdateDate
    FROM Lu_Package
    
    UNION ALL
    
    SELECT 
        PackageId,
        PackageName,
        Description,
        ShortName,
        PackagePath,
        'LU_PRS_Package' AS SourceTable,
        PackageType,
        OMBNumber,
        Year,
        CreatedDate,
        LastUpdateDate
    FROM LU_PRS_Package
    
    ORDER BY Year DESC, PackageName
    """
    
    # Execute query
    print("Connecting to INT database...")
    df = pd.read_sql(query, conn_str)
    
    print(f"Extracted {len(df)} packages")
    print(f"  Lu_Package: {len(df[df['SourceTable'] == 'Lu_Package'])} packages")
    print(f"  LU_PRS_Package: {len(df[df['SourceTable'] == 'LU_PRS_Package'])} packages")
    
    # Export to CSV
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_file = f'prs_packages_{timestamp}.csv'
    df.to_csv(csv_file, index=False)
    print(f"Exported to: {csv_file}")
    
    return df

if __name__ == '__main__':
    df = extract_prs_packages()
```

---

## PowerShell Integration

### Basic Connection

```powershell
# Load credentials from environments
$envs = & 'G:\My Drive\03_Areas\Keys\Environments\Load-Environments.ps1'
$intConfig = $envs.azure_sql.int

# Build connection string
$connectionString = "Server=$($intConfig.server);Database=$($intConfig.database);User Id=$($intConfig.username);Password=$($intConfig.password);Encrypt=True;TrustServerCertificate=False;"

# Create connection
$connection = New-Object System.Data.SqlClient.SqlConnection
$connection.ConnectionString = $connectionString

# Open connection
$connection.Open()

# Create command
$command = $connection.CreateCommand()
$command.CommandText = "SELECT TOP 10 * FROM Lu_Package"

# Execute query
$reader = $command.ExecuteReader()

# Read results
while ($reader.Read()) {
    Write-Host "Package: $($reader['PackageName'])"
}

# Close connection
$reader.Close()
$connection.Close()
```

### Query to DataTable

```powershell
# Load credentials
$envs = & 'G:\My Drive\03_Areas\Keys\Environments\Load-Environments.ps1'
$intConfig = $envs.azure_sql.int

# Build connection string
$connectionString = "Server=$($intConfig.server);Database=$($intConfig.database);User Id=$($intConfig.username);Password=$($intConfig.password);Encrypt=True;TrustServerCertificate=False;"

# Create connection
$connection = New-Object System.Data.SqlClient.SqlConnection
$connection.ConnectionString = $connectionString

# Create command
$command = $connection.CreateCommand()
$command.CommandText = @"
SELECT 
    PackageId,
    PackageName,
    Year,
    PackageType,
    OMBNumber
FROM Lu_Package
ORDER BY Year DESC
"@

# Create adapter and dataset
$adapter = New-Object System.Data.SqlClient.SqlDataAdapter $command
$dataset = New-Object System.Data.DataSet
$adapter.Fill($dataset)

# Get results
$table = $dataset.Tables[0]
Write-Host "Total packages: $($table.Rows.Count)"

# Display results
$table | Format-Table -AutoSize

# Export to CSV
$table | Export-Csv -Path "prs_packages.csv" -NoTypeInformation

# Close connection
$connection.Close()
```

---

## Best Practices

### 1. Always Load Credentials from Environments

```python
# ✅ CORRECT: Load from environments.json
with open('G:/My Drive/03_Areas/Keys/Environments/environments.json', 'r') as f:
    envs = json.load(f)
int_config = envs['azure_sql']['int']

# ❌ WRONG: Hardcode credentials
username = "qauser"
password = "qauser"
```

### 2. Use Parameterized Queries

```python
# ✅ CORRECT: Parameterized query
cursor.execute("SELECT * FROM Lu_Package WHERE Year = ?", (2025,))

# ❌ WRONG: String concatenation (SQL injection risk)
cursor.execute(f"SELECT * FROM Lu_Package WHERE Year = {year}")
```

### 3. Close Connections

```python
# ✅ CORRECT: Use context manager
with pyodbc.connect(conn_str) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM Lu_Package")
        rows = cursor.fetchall()

# Or explicitly close
conn = pyodbc.connect(conn_str)
try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Lu_Package")
    rows = cursor.fetchall()
finally:
    cursor.close()
    conn.close()
```

### 4. Handle Errors Gracefully

```python
import pyodbc

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Lu_Package")
    rows = cursor.fetchall()
except pyodbc.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
```

### 5. Use Read-Only Queries

```sql
-- ✅ CORRECT: Read-only SELECT
SELECT * FROM Lu_Package;

-- ❌ WRONG: Modifying data (will fail with qauser)
UPDATE Lu_Package SET Year = 2026 WHERE PackageId = 1;
DELETE FROM Lu_Package WHERE Year < 2020;
```

### 6. Limit Result Sets

```sql
-- ✅ CORRECT: Use TOP or WHERE to limit results
SELECT TOP 100 * FROM Lu_Package;
SELECT * FROM Lu_Package WHERE Year = 2025;

-- ⚠️ CAUTION: Selecting all rows (163 packages is OK, but be careful)
SELECT * FROM Lu_Package;
```

---

## Troubleshooting

### Issue 1: "Login failed for user 'qauser'"

**Problem:** Cannot authenticate to database.

**Solution:**
```
1. Verify credentials in environments.json
2. Check network connectivity to Azure
3. Verify VPN connection if required
4. Confirm server name is correct
5. Try connecting via SSMS to test credentials
```

### Issue 2: "ODBC Driver not found"

**Problem:** Python can't find SQL Server ODBC driver.

**Solution:**
```bash
# Download and install ODBC Driver 17 for SQL Server
# https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

# Or use ODBC Driver 18
conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    # ... rest of connection string
)
```

### Issue 3: "SSL Provider: The certificate chain was issued by an authority that is not trusted"

**Problem:** SSL certificate validation fails.

**Solution:**
```python
# Option 1: Trust server certificate (less secure)
conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=yes;"  # Changed to yes
)

# Option 2: Install Azure SQL certificate
# Follow Azure documentation for certificate installation
```

### Issue 4: "Table does not exist"

**Problem:** Query fails with table not found.

**Solution:**
```sql
-- List all tables in database
SELECT TABLE_SCHEMA, TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_SCHEMA, TABLE_NAME;

-- Verify table name and schema
SELECT * FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_NAME LIKE '%Package%';
```

### Issue 5: Query Timeout

**Problem:** Query takes too long and times out.

**Solution:**
```python
# Increase timeout
conn = pyodbc.connect(conn_str, timeout=60)

# Or in connection string
conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"Connection Timeout=60;"  # 60 seconds
)
```

---

## Quick Reference

### Connection String Template

```
Server=az-hs-mi-int.71b05803ca2a.database.windows.net;Database=BHCMIS;User Id=qauser;Password=qauser;Encrypt=True;TrustServerCertificate=False;
```

### Python Quick Start

```python
import pyodbc
import pandas as pd

conn_str = "Server=az-hs-mi-int.71b05803ca2a.database.windows.net;Database=BHCMIS;User Id=qauser;Password=qauser;Encrypt=True;TrustServerCertificate=False;"

df = pd.read_sql("SELECT * FROM Lu_Package", conn_str)
print(df.head())
```

### PowerShell Quick Start

```powershell
$connectionString = "Server=az-hs-mi-int.71b05803ca2a.database.windows.net;Database=BHCMIS;User Id=qauser;Password=qauser;Encrypt=True;TrustServerCertificate=False;"

$connection = New-Object System.Data.SqlClient.SqlConnection
$connection.ConnectionString = $connectionString
$connection.Open()

$command = $connection.CreateCommand()
$command.CommandText = "SELECT TOP 10 * FROM Lu_Package"
$reader = $command.ExecuteReader()

while ($reader.Read()) {
    Write-Host $reader['PackageName']
}

$reader.Close()
$connection.Close()
```

---

## Related Skills

### Development Skills
- **[skill_salesforce_development](skill_salesforce_development.md)** - Salesforce development patterns
- **[skill_git_version_control](skill_git_version_control.md)** - Version control workflows

### Automation Skills
- **[skill_powershell_automation](../automation/skill_powershell_automation.md)** - PowerShell scripting
- **[skill_file_organization](../automation/skill_file_organization.md)** - PARA method filing

### System Skills
- **[skill_environments_credentials](../system/skill_environments_credentials.md)** - Credential management
- **[skill_user_commands](../system/skill_user_commands.md)** - Quick command reference

---

## Success Metrics

- **Query Performance:** Most queries complete in < 5 seconds
- **Data Accuracy:** 100% match with source tables
- **Automation Success:** Python scripts run without manual intervention
- **Credential Security:** No hardcoded credentials in scripts

---

## Maintenance

- Update this skill when new databases are added
- Document new query patterns as discovered
- Keep connection string templates current
- Review and update troubleshooting section quarterly
- Update package counts as data changes
