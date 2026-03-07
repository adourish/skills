# Skill: Copado CLI Installation

**Category**: system  
**Priority**: HIGH  
**Last Updated**: March 3, 2026  
**Prerequisites**:
- Node.js 14+ installed
- npm or yarn package manager
- Salesforce org access
- Command line familiarity

---

## Overview

The Copado CLI provides command-line access to Copado DevOps platform functionality, enabling automation, CI/CD integration, and metadata operations. This skill covers installation, authentication, configuration, and troubleshooting.

## When to Use This Skill

- Setting up new developer workstation
- Configuring CI/CD pipelines
- Automating Copado operations
- Troubleshooting CLI issues
- Upgrading CLI version

## Prerequisites

- Node.js 14.x or higher
- npm 6.x or higher (or yarn 1.x+)
- Salesforce org with Copado installed
- Copado user account with API access
- Command line terminal access

## Core Concepts

### Installation Methods

**npm (Recommended)**:
- Global installation via npm
- Automatic updates available
- Cross-platform support

**Standalone Binary**:
- Platform-specific executable
- No Node.js required
- Manual updates

**Docker Container**:
- Isolated environment
- CI/CD friendly
- Consistent across systems

### Authentication Methods

**OAuth 2.0 (Recommended)**:
- Browser-based authentication
- Secure token storage
- Automatic refresh

**JWT (Server-to-Server)**:
- Non-interactive authentication
- CI/CD pipelines
- Service accounts

**Session ID**:
- Manual token entry
- Legacy method
- Not recommended

---

## Step-by-Step Instructions

### Task 1: Install Copado CLI via npm

**Objective**: Install Copado CLI globally on your system

**Prerequisites Check**:

```bash
# Verify Node.js version (14+ required)
node --version
# Expected: v14.x.x or higher

# Verify npm version (6+ required)
npm --version
# Expected: 6.x.x or higher
```

**Installation Steps**:

1. **Install Copado CLI Globally**

```bash
# Install latest version
npm install -g @copado/cli

# Or install specific version
npm install -g @copado/cli@2.5.0
```

**Expected Output**:
```
+ @copado/cli@2.5.0
added 127 packages in 45s
```

2. **Verify Installation**

```bash
# Check CLI version
copado --version

# Expected output
@copado/cli/2.5.0 win32-x64 node-v18.12.0
```

3. **View Available Commands**

```bash
# List all commands
copado --help

# View specific command help
copado auth --help
copado metadata --help
copado deployment --help
```

**Expected Output**:
```
Copado CLI - DevOps Platform Command Line Interface

VERSION
  @copado/cli/2.5.0

USAGE
  $ copado [COMMAND]

COMMANDS
  auth         Authenticate with Salesforce/Copado
  metadata     Retrieve and deploy metadata
  deployment   Manage deployments
  user-story   Manage User Stories
  config       Configure CLI settings
```

---

### Task 2: Authenticate with Salesforce/Copado

**Objective**: Connect CLI to your Salesforce org

**Method 1: OAuth 2.0 (Interactive - Recommended)**

```bash
# Authenticate to Salesforce org
copado auth login --instance-url https://login.salesforce.com

# For sandbox
copado auth login --instance-url https://test.salesforce.com
```

**Steps**:
1. Command opens browser window
2. Login to Salesforce
3. Authorize Copado CLI
4. Browser shows "Authentication successful"
5. Return to terminal

**Expected Output**:
```
Opening browser for authentication...
Waiting for authentication...
Successfully authenticated as: user@example.com
Org ID: 00D5w000000abcd
Instance URL: https://reisystems--dmedev5.sandbox.my.salesforce.com
```

**Method 2: JWT (Non-Interactive - CI/CD)**

```bash
# Authenticate using JWT
copado auth jwt \
  --client-id 3MVG9... \
  --jwt-key-file ./server.key \
  --username user@example.com \
  --instance-url https://login.salesforce.com
```

**Prerequisites**:
- Connected App configured in Salesforce
- Server certificate (.key file)
- Client ID from Connected App

**Method 3: Session ID (Manual)**

```bash
# Authenticate with session ID
copado auth session \
  --session-id 00D5w000000abcd!... \
  --instance-url https://reisystems--dmedev5.sandbox.my.salesforce.com
```

**Get Session ID**:
1. Login to Salesforce
2. Open Developer Console
3. Execute: `System.debug(UserInfo.getSessionId());`
4. Copy session ID from debug log

---

### Task 3: Configure CLI Settings

**Objective**: Set default configuration for CLI operations

**Configuration File Location**:
- Windows: `C:\Users\<username>\.copado\config.json`
- Mac/Linux: `~/.copado/config.json`

**Set Default Org**:

```bash
# Set default username
copado config set defaultusername user@example.com

# Verify setting
copado config get defaultusername
```

**Set API Version**:

```bash
# Set Salesforce API version
copado config set apiVersion 59.0

# Verify
copado config get apiVersion
```

**Set Timeout**:

```bash
# Set command timeout (seconds)
copado config set timeout 600

# Verify
copado config set timeout
```

**Set Log Level**:

```bash
# Set logging level (error, warn, info, debug)
copado config set logLevel info

# Verify
copado config get logLevel
```

**View All Settings**:

```bash
# List all configuration
copado config list
```

**Expected Output**:
```json
{
  "defaultusername": "user@example.com",
  "apiVersion": "59.0",
  "timeout": 600,
  "logLevel": "info",
  "instanceUrl": "https://reisystems--dmedev5.sandbox.my.salesforce.com"
}
```

**Manual Configuration**:

Edit `~/.copado/config.json`:

```json
{
  "defaultusername": "adourish@reisystems.com.dmedev5",
  "apiVersion": "59.0",
  "timeout": 600,
  "logLevel": "info",
  "instanceUrl": "https://reisystems--dmedev5.sandbox.my.salesforce.com",
  "defaultProject": "BPHC-Modernization",
  "deploymentOptions": {
    "testLevel": "RunLocalTests",
    "checkOnly": false,
    "ignoreWarnings": false
  }
}
```

---

### Task 4: Manage Multiple Orgs

**Objective**: Configure and switch between multiple Salesforce orgs

**Authenticate Multiple Orgs**:

```bash
# Authenticate to Dev org
copado auth login --instance-url https://test.salesforce.com --alias dmedev5

# Authenticate to QA org
copado auth login --instance-url https://test.salesforce.com --alias qa

# Authenticate to Production
copado auth login --instance-url https://login.salesforce.com --alias prod
```

**List Authenticated Orgs**:

```bash
# View all orgs
copado org list
```

**Expected Output**:
```
ALIAS    USERNAME                              ORG ID              INSTANCE URL
dmedev5  adourish@reisystems.com.dmedev5       00D5w000000abcd     https://reisystems--dmedev5.sandbox.my.salesforce.com
qa       adourish@reisystems.com.qa            00D5w000000efgh     https://reisystems--qa.sandbox.my.salesforce.com
prod     adourish@reisystems.com               00D5w000000ijkl     https://reisystems.my.salesforce.com
(D)      Default org
```

**Switch Default Org**:

```bash
# Set default org by alias
copado config set defaultusername dmedev5

# Or by full username
copado config set defaultusername adourish@reisystems.com.dmedev5
```

**Use Specific Org for Command**:

```bash
# Use --org flag to override default
copado metadata retrieve --org qa --type ApexClass

# Or use full username
copado metadata retrieve --org adourish@reisystems.com.qa --type ApexClass
```

**Remove Org**:

```bash
# Logout from specific org
copado auth logout --org dmedev5

# Logout from all orgs
copado auth logout --all
```

---

### Task 5: Upgrade Copado CLI

**Objective**: Update to latest CLI version

**Check Current Version**:

```bash
# View installed version
copado --version

# Check for updates
npm outdated -g @copado/cli
```

**Upgrade to Latest**:

```bash
# Update to latest version
npm update -g @copado/cli

# Or reinstall
npm uninstall -g @copado/cli
npm install -g @copado/cli
```

**Upgrade to Specific Version**:

```bash
# Install specific version
npm install -g @copado/cli@2.5.0
```

**Verify Upgrade**:

```bash
# Check new version
copado --version

# Test functionality
copado auth list
```

**Rollback if Needed**:

```bash
# Uninstall current version
npm uninstall -g @copado/cli

# Install previous version
npm install -g @copado/cli@2.4.0
```

---

## Common Patterns

### Pattern 1: Fresh Installation

```bash
# 1. Install CLI
npm install -g @copado/cli

# 2. Verify installation
copado --version

# 3. Authenticate
copado auth login --instance-url https://test.salesforce.com --alias dmedev5

# 4. Configure defaults
copado config set defaultusername dmedev5
copado config set apiVersion 59.0
copado config set timeout 600

# 5. Test connection
copado org list
```

---

### Pattern 2: CI/CD Setup (JWT)

```bash
# 1. Install CLI in CI environment
npm install -g @copado/cli

# 2. Authenticate with JWT (non-interactive)
copado auth jwt \
  --client-id $COPADO_CLIENT_ID \
  --jwt-key-file ./server.key \
  --username $COPADO_USERNAME \
  --instance-url https://login.salesforce.com

# 3. Configure for automation
copado config set timeout 900
copado config set logLevel error

# 4. Verify
copado org list
```

---

### Pattern 3: Multi-Org Developer Setup

```bash
# Authenticate to all environments
copado auth login --instance-url https://test.salesforce.com --alias dev
copado auth login --instance-url https://test.salesforce.com --alias qa
copado auth login --instance-url https://test.salesforce.com --alias uat
copado auth login --instance-url https://login.salesforce.com --alias prod

# Set dev as default
copado config set defaultusername dev

# Verify all orgs
copado org list
```

---

## Troubleshooting

### Issue 1: Command Not Found

**Symptom**:
```bash
copado --version
# bash: copado: command not found
```

**Cause**: CLI not installed or not in PATH

**Solution**:

```bash
# Verify npm global bin location
npm config get prefix

# Windows: Should be C:\Users\<username>\AppData\Roaming\npm
# Mac/Linux: Should be /usr/local

# Add to PATH if missing
# Windows: Add to System Environment Variables
# Mac/Linux: Add to ~/.bashrc or ~/.zshrc
export PATH=$PATH:/usr/local/bin

# Reinstall CLI
npm install -g @copado/cli

# Verify
which copado  # Mac/Linux
where copado  # Windows
```

---

### Issue 2: Authentication Failed

**Symptom**:
```
Error: Authentication failed
Invalid username, password, security token; or user locked out
```

**Cause**: Incorrect credentials, IP restrictions, or expired session

**Solution**:

```bash
# 1. Verify instance URL
# Sandbox: https://test.salesforce.com
# Production: https://login.salesforce.com

# 2. Check IP restrictions in Salesforce
# Setup → Security → Network Access

# 3. Reset security token
# Salesforce → Settings → Reset Security Token

# 4. Try authentication again
copado auth login --instance-url https://test.salesforce.com

# 5. If still failing, use session ID method
copado auth session --session-id <session-id> --instance-url <url>
```

---

### Issue 3: Permission Denied Errors

**Symptom**:
```
Error: EACCES: permission denied, mkdir '/usr/local/lib/node_modules/@copado'
```

**Cause**: Insufficient permissions for global npm install

**Solution (Mac/Linux)**:

```bash
# Option 1: Use sudo (not recommended)
sudo npm install -g @copado/cli

# Option 2: Fix npm permissions (recommended)
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Reinstall CLI
npm install -g @copado/cli
```

**Solution (Windows)**:

```powershell
# Run PowerShell as Administrator
npm install -g @copado/cli
```

---

### Issue 4: SSL Certificate Errors

**Symptom**:
```
Error: unable to verify the first certificate
```

**Cause**: Corporate proxy or firewall blocking SSL

**Solution**:

```bash
# Option 1: Configure npm to use corporate proxy
npm config set proxy http://proxy.company.com:8080
npm config set https-proxy http://proxy.company.com:8080

# Option 2: Disable SSL verification (NOT RECOMMENDED for production)
npm config set strict-ssl false

# Option 3: Use corporate CA certificate
npm config set cafile /path/to/corporate-ca.crt
```

---

### Issue 5: Timeout Errors

**Symptom**:
```
Error: Request timeout after 300000ms
```

**Cause**: Slow network, large metadata, or Salesforce processing delay

**Solution**:

```bash
# Increase timeout in config
copado config set timeout 900

# Or use --timeout flag
copado metadata retrieve --org dmedev5 --type ApexClass --timeout 900

# For very large operations
copado config set timeout 1800  # 30 minutes
```

---

## Best Practices

### Installation

- Use npm for easy updates
- Install globally for command-line access
- Keep CLI version up to date
- Document CLI version in project README

### Authentication

- Use OAuth for interactive sessions
- Use JWT for CI/CD pipelines
- Never commit credentials to Git
- Use environment variables for CI/CD
- Rotate tokens regularly

### Configuration

- Set reasonable timeouts (600-900 seconds)
- Use aliases for orgs (dev, qa, prod)
- Configure default org for convenience
- Use appropriate log levels (info for dev, error for CI)

### Security

- Never share session IDs
- Use JWT for automation (not session IDs)
- Restrict Connected App IP ranges
- Use separate service accounts for CI/CD
- Enable MFA on all accounts

### Maintenance

- Update CLI monthly
- Test updates in dev first
- Document breaking changes
- Keep Node.js updated
- Monitor for security advisories

---

## Related Skills

- `skill_copado_cli_metadata_operations.md` - Using CLI for metadata
- `skill_copado_cli_cicd_integration.md` - CI/CD pipeline setup
- `skill_copado_cli_automation_scripts.md` - Automation scripts
- `skill_copado_troubleshooting.md` - Advanced troubleshooting

---

## References

- [Copado CLI Documentation](https://docs.copado.com/articles/#!copado-ci-cd-publication/copado-cli)
- [npm Documentation](https://docs.npmjs.com/)
- [Salesforce Connected Apps](https://help.salesforce.com/s/articleView?id=sf.connected_app_overview.htm)
- [JWT Bearer Flow](https://help.salesforce.com/s/articleView?id=sf.remoteaccess_oauth_jwt_flow.htm)

---

**Skill Owner**: TEG Development Team  
**Last Validated**: March 3, 2026  
**Next Review**: April 1, 2026
