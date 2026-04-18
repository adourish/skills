---
name: unifi
description: Interact with UniFi APIs — cloud Site Manager (api.ui.com) and local Network Application (192.168.0.1)
argument-hint: "[cloud|local] [action] e.g. 'list devices'"
---

# UniFi API Skill

Two distinct UniFi APIs are available:

| API | Base URL | Auth Header | MCP Prefix |
|-----|----------|-------------|------------|
| Site Manager (cloud) | `https://api.ui.com/v1` | `X-API-KEY` | `unifi_` |
| Network Application (local) | `https://<host>/proxy/network/integration/v1` | `X-API-KEY` | `unifi_network_` |

## Credentials

Loaded from environment variables (set from `environments.json` on Google Drive):

| Var | Service |
|-----|---------|
| `UNIFI_API_KEY` | Cloud Site Manager |
| `UNIFI_NETWORK_API_KEY` | Local Network App |
| `UNIFI_NETWORK_HOST` | Local host (default: `192.168.0.1`) |

**Google Drive path:** `G:\My Drive\03_Areas\Keys\Environments\environments.json`

```json
"unifi": { "credentials": { "apiKey": "CAq5..." } },
"unifi_network": { "credentials": { "apiKey": "teiP...", "host": "192.168.0.1" } }
```

### Load credentials (PowerShell)

```powershell
$env_path = "G:\My Drive\03_Areas\Keys\Environments\environments.json"
$envs = Get-Content $env_path | ConvertFrom-Json
$env:UNIFI_API_KEY          = $envs.unifi.credentials.apiKey
$env:UNIFI_NETWORK_API_KEY  = $envs.unifi_network.credentials.apiKey
$env:UNIFI_NETWORK_HOST     = $envs.unifi_network.credentials.host
```

### Load credentials (bash/zsh)

```bash
ENV_PATH="$HOME/Library/CloudStorage/GoogleDrive-personal/My Drive/03_Areas/Keys/Environments/environments.json"
export UNIFI_API_KEY=$(jq -r '.unifi.credentials.apiKey' "$ENV_PATH")
export UNIFI_NETWORK_API_KEY=$(jq -r '.unifi_network.credentials.apiKey' "$ENV_PATH")
export UNIFI_NETWORK_HOST=$(jq -r '.unifi_network.credentials.host' "$ENV_PATH")
```

---

## MCP Tools (via `amplenote` MCP server)

### Cloud Site Manager (`unifi_*`)

| Tool | Description |
|------|-------------|
| `unifi_list_hosts` | List all UniFi consoles/hosts |
| `unifi_get_host` | Get details for a specific host |
| `unifi_list_sites` | List sites across all hosts |
| `unifi_list_devices` | List devices at a site |

### Local Network Application (`unifi_network_*`)

| Tool | Description |
|------|-------------|
| `unifi_network_list_sites` | List sites on local controller |
| `unifi_network_list_devices` | List network devices (APs, switches, routers) |
| `unifi_network_list_clients` | List connected clients |
| `unifi_network_get_device` | Get details for a specific device by MAC |

---

## Direct API (curl fallback)

### Cloud — list sites
```bash
curl -s -X GET 'https://api.ui.com/v1/sites' \
  -H "X-API-KEY: $UNIFI_API_KEY" \
  -H 'Accept: application/json'
```

### Cloud — list devices at a site
```bash
SITE_ID="your-site-id"
curl -s -X GET "https://api.ui.com/v1/sites/$SITE_ID/devices" \
  -H "X-API-KEY: $UNIFI_API_KEY" \
  -H 'Accept: application/json'
```

### Local — list sites (ignores self-signed cert with -k)
```bash
curl -k -s -X GET "https://$UNIFI_NETWORK_HOST/proxy/network/integration/v1/sites" \
  -H "X-API-KEY: $UNIFI_NETWORK_API_KEY" \
  -H 'Accept: application/json'
```

### Local — list devices
```bash
SITE_ID="default"
curl -k -s -X GET "https://$UNIFI_NETWORK_HOST/proxy/network/integration/v1/sites/$SITE_ID/devices" \
  -H "X-API-KEY: $UNIFI_NETWORK_API_KEY" \
  -H 'Accept: application/json'
```

### Local — list clients
```bash
curl -k -s -X GET "https://$UNIFI_NETWORK_HOST/proxy/network/integration/v1/sites/$SITE_ID/clients" \
  -H "X-API-KEY: $UNIFI_NETWORK_API_KEY" \
  -H 'Accept: application/json'
```

---

## Rate Limits

- **Cloud API**: ~100 req/min per API key
- **Local API**: No documented limit; avoid polling more than once per second
- Both APIs return standard HTTP 429 when rate-limited

## Notes

- The local Network Application uses a **self-signed TLS certificate** — always use `-k` with curl or `rejectUnauthorized: false` in Node.js
- The local host defaults to `192.168.0.1` but can be overridden via `UNIFI_NETWORK_HOST`
- Cloud API key is scoped per UniFi account; it sees all sites and hosts linked to that account
- Device MAC addresses are the canonical identifier for `unifi_network_get_device`
