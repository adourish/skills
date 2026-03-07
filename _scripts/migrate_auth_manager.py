#!/usr/bin/env python3
"""
Phase 4 migration: replace auth_manager.py across all repos and patch callers.
Run once, then delete.
"""

import re
from pathlib import Path

NEW_AUTH_MANAGER = '''\
#!/usr/bin/env python3
"""
Authentication Manager — wraps CredentialResolver for OAuth token management.
Personal services: Gmail, Todoist, Amplenote.
"""

import json
import logging
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import requests

from credential_resolver import CredentialResolver

logger = logging.getLogger(__name__)

GMAIL_TOKEN_PATH = Path(r\'G:\\My Drive\\03_Areas\\Keys\\Gmail\\token.json\')


class AuthManager:
    """Manages OAuth tokens with automatic refresh via CredentialResolver."""

    def __init__(self):
        self._resolver = CredentialResolver()
        self._gmail_creds = None
        self._todoist_token = None
        self._amplenote_token = None
        logger.info("AuthManager initialized (providers: %s)", self._resolver.providers())

    async def get_gmail_credentials(self) -> Credentials:
        """Get Gmail credentials from token.json, refreshing if expired."""
        if self._gmail_creds and not self._gmail_creds.expired:
            return self._gmail_creds

        if GMAIL_TOKEN_PATH.exists():
            token_data = json.loads(GMAIL_TOKEN_PATH.read_text())
            self._gmail_creds = Credentials(
                token=token_data[\'token\'],
                refresh_token=token_data[\'refresh_token\'],
                token_uri=token_data[\'token_uri\'],
                client_id=token_data[\'client_id\'],
                client_secret=token_data[\'client_secret\'],
                scopes=token_data[\'scopes\']
            )
            if self._gmail_creds.expired and self._gmail_creds.refresh_token:
                logger.info("Refreshing Gmail token")
                self._gmail_creds.refresh(Request())
                token_data[\'token\'] = self._gmail_creds.token
                GMAIL_TOKEN_PATH.write_text(json.dumps(token_data, indent=2))
                logger.info("Gmail token refreshed and saved")

        return self._gmail_creds

    async def get_todoist_token(self) -> str:
        """Get Todoist API token."""
        if not self._todoist_token:
            self._todoist_token = self._resolver.get("todoist", "api.apiToken")
        return self._todoist_token

    async def get_amplenote_token(self) -> str:
        """Get Amplenote access token."""
        if not self._amplenote_token:
            self._amplenote_token = self._resolver.get("amplenote", "oauth.accessToken")
        return self._amplenote_token

    async def refresh_amplenote_token(self) -> str:
        """Refresh Amplenote access token and persist via resolver."""
        client_id     = self._resolver.get("amplenote", "oauth.clientId")
        refresh_token = self._resolver.get("amplenote", "oauth.refreshToken")

        logger.info("Refreshing Amplenote access token...")
        response = requests.post(
            \'https://api.amplenote.com/oauth/token\',
            json={
                \'grant_type\':    \'refresh_token\',
                \'refresh_token\': refresh_token,
                \'client_id\':     client_id
            },
            headers={\'Content-Type\': \'application/json\'}
        )

        if response.status_code == 200:
            token_data = response.json()
            self._amplenote_token = token_data[\'access_token\']
            self._resolver.put("amplenote", "oauth.accessToken", token_data[\'access_token\'])
            if \'refresh_token\' in token_data:
                self._resolver.put("amplenote", "oauth.refreshToken", token_data[\'refresh_token\'])
            logger.info("Amplenote token refreshed (expires in %s s)", token_data.get(\'expires_in\', \'?\'))
            return self._amplenote_token
        else:
            raise Exception(f"Amplenote token refresh failed: {response.status_code} {response.text}")

    async def refresh_all_tokens(self):
        """Refresh all tokens that need refreshing."""
        logger.info("Checking all tokens for refresh")
        try:
            await self.get_gmail_credentials()
            logger.info("Gmail token checked/refreshed")
        except Exception as e:
            logger.error("Error refreshing Gmail token: %s", e)
        logger.info("Token refresh check complete")
'''

# --- locations to write auth_manager.py ---
AUTH_MANAGER_PATHS = [
    Path(r"G:\My Drive\06_Skills\skills\_tools\auth_manager.py"),
    Path(r"G:\My Drive\06_Skills\skills\_automation\auth_manager.py"),
    Path(r"G:\My Drive\06_Skills\pskills\_tools\auth_manager.py"),
    Path(r"G:\My Drive\06_Skills\pskills\_automation\auth_manager.py"),
]

# --- files to bulk-patch (AuthManager call sites) ---
TOOLS_DIRS = [
    Path(r"G:\My Drive\06_Skills\skills\_tools"),
    Path(r"G:\My Drive\06_Skills\skills\_automation"),
    Path(r"G:\My Drive\06_Skills\pskills\_tools"),
    Path(r"G:\My Drive\06_Skills\pskills\_automation"),
]

# Pattern: AuthManager(Path(r'...')) or AuthManager(Path("...")) or AuthManager(ENV_PATH)
AUTHMANAGER_CALL = re.compile(
    r"AuthManager\((?:Path\(['\"].*?['\"]\)|ENV_PATH)\)"
)
ENV_PATH_LINE = re.compile(
    r"^ENV_PATH\s*=\s*Path\(.*environments\.json.*\)\s*\n",
    re.MULTILINE
)

def patch_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    original = text

    # Remove ENV_PATH assignment lines
    text = ENV_PATH_LINE.sub("", text)

    # Replace AuthManager(Path(...)) and AuthManager(ENV_PATH) with AuthManager()
    text = AUTHMANAGER_CALL.sub("AuthManager()", text)

    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False

def patch_todoist_tools(path: Path):
    """Replace the _load_openrouter_key method with resolver lookup."""
    text = path.read_text(encoding='utf-8')

    old = '''\
    def _load_openrouter_key(self) -> Optional[str]:
        """Load OpenRouter API key from environments.json"""
        try:
            env_path = Path.home() / "Google Drive" / "My Drive" / "03_Areas" / "Keys" / "Environments" / "environments.json"
            if not env_path.exists():
                env_path = Path("G:/My Drive/03_Areas/Keys/Environments/environments.json")

            if env_path.exists():
                with open(env_path, 'r') as f:
                    config = json.load(f)
                    return config.get('environments', {}).get('openrouter', {}).get('credentials', {}).get('apiKey')
        except Exception as e:
            logger.warning(f"Could not load OpenRouter key: {e}")
        return None'''

    new = '''\
    def _load_openrouter_key(self) -> Optional[str]:
        """Load OpenRouter API key via CredentialResolver."""
        try:
            from credential_resolver import CredentialResolver
            return CredentialResolver().get("openrouter", "api.apiKey")
        except Exception as e:
            logger.warning(f"Could not load OpenRouter key: {e}")
        return None'''

    # Also remove now-unused imports (json, Path) only if they appear in the load method context
    updated = text.replace(old, new)
    if updated != text:
        path.write_text(updated, encoding='utf-8')
        print(f"  patched todoist_tools: {path}")
    else:
        print(f"  WARN: todoist_tools pattern not matched in {path}")

def main():
    # 1. Write new auth_manager.py to all locations
    print("Writing new auth_manager.py...")
    for p in AUTH_MANAGER_PATHS:
        p.write_text(NEW_AUTH_MANAGER, encoding='utf-8')
        print(f"  wrote {p}")

    # 2. Bulk-patch all AuthManager call sites
    print("\nPatching AuthManager call sites...")
    for tools_dir in TOOLS_DIRS:
        for py_file in tools_dir.glob("*.py"):
            if py_file.name == "auth_manager.py":
                continue  # already rewritten
            if patch_file(py_file):
                print(f"  patched {py_file.name} ({py_file.parent.parent.name}/{py_file.parent.name})")

    # 3. Fix todoist_tools in both repos
    print("\nPatching todoist_tools.py...")
    for tools_dir in TOOLS_DIRS:
        tt = tools_dir / "todoist_tools.py"
        if tt.exists():
            patch_todoist_tools(tt)

    print("\nDone.")

if __name__ == "__main__":
    main()
