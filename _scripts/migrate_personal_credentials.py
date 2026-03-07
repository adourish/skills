#!/usr/bin/env python3
"""
One-time migration: environments.json personal credentials → encrypted key files.
Output: skills/09_environments/keys/api-personal-*-keys.json
"""

import json
import os
import base64
from datetime import datetime
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

KEY_FILE     = Path(r"C:\Users\sol90\.credentials\DevKey.key")
ENV_FILE     = Path(r"G:\My Drive\03_Areas\Keys\Environments\environments.json")
KEYS_OUT_DIR = Path(r"G:\My Drive\06_Skills\skills\09_environments\keys")

def load_key() -> bytes:
    return base64.b64decode(KEY_FILE.read_text().strip())

def encrypt(plaintext: str, key: bytes) -> str:
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext.encode()) + padder.finalize()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    enc = cipher.encryptor()
    ct = enc.update(padded) + enc.finalize()
    return "ENC:" + base64.b64encode(iv + ct).decode()

def write_key_file(name: str, env_name: str, cred_types: list, encrypted_credentials: dict):
    data = {
        "metadata": {
            "lastUpdated": datetime.now().strftime("%Y-%m-%d"),
            "credentialTypes": cred_types
        },
        "environmentName": env_name,
        "encryptedCredentials": encrypted_credentials
    }
    out = KEYS_OUT_DIR / f"{name}-keys.json"
    out.write_text(json.dumps(data, indent=4))
    print(f"  wrote {out.name}")

def main():
    key = load_key()
    env = json.loads(ENV_FILE.read_text())["environments"]
    KEYS_OUT_DIR.mkdir(parents=True, exist_ok=True)

    # --- todoist ---
    t = env["todoist"]
    write_key_file("api-personal-todoist", "API-PERSONAL-TODOIST", ["api-token", "oauth"], {
        "api": {
            "type": "api-token",
            "purpose": "Todoist API v1 task management",
            "apiToken":         encrypt(t["credentials"]["apiToken"], key),
            "appClientId":      encrypt(t["credentials"]["appClientId"], key),
            "appClientSecret":  encrypt(t["credentials"]["appClientSecret"], key),
        },
        "meta": {
            "apiUrl":     t["apiUrl"],
            "apiVersion": t["apiVersion"],
            "notes":      t.get("notes", "")
        }
    })

    # --- amplenote ---
    a = env["amplenote"]
    write_key_file("api-personal-amplenote", "API-PERSONAL-AMPLENOTE", ["oauth", "access-token"], {
        "oauth": {
            "type":         "oauth",
            "purpose":      "Amplenote OAuth 2.0",
            "clientId":     encrypt(a["oauth"]["clientId"], key),
            "accessToken":  encrypt(a["credentials"]["accessToken"], key),
            "refreshToken": encrypt(a["credentials"]["refreshToken"], key),
            "tokenUrl":     a["oauth"]["tokenUrl"],
            "authUrl":      a["oauth"]["authUrl"],
            "redirectUri":  a["oauth"]["redirectUri"],
        },
        "meta": {
            "apiUrl":     a["apiUrl"],
            "apiVersion": a["apiVersion"],
            "notes":      a.get("notes", "")
        }
    })

    # --- gmail ---
    g = env["gmail"]
    write_key_file("api-personal-gmail", "API-PERSONAL-GMAIL", ["oauth"], {
        "oauth": {
            "type":         "oauth",
            "purpose":      "Gmail API read access",
            "clientId":     encrypt(g["oauth"]["clientId"], key),
            "clientSecret": encrypt(g["oauth"]["clientSecret"], key),
            "projectId":    g["oauth"]["projectId"],
            "authUri":      g["oauth"]["authUri"],
            "tokenUri":     g["oauth"]["tokenUri"],
            "scopes":       g["oauth"]["scopes"],
            "tokenPath":    g["tokenPath"],
        }
    })

    # --- openrouter ---
    o = env["openrouter"]
    write_key_file("api-personal-openrouter", "API-PERSONAL-OPENROUTER", ["api-key"], {
        "api": {
            "type":    "api-key",
            "purpose": "OpenRouter AI model routing",
            "apiKey":  encrypt(o["credentials"]["apiKey"], key),
        },
        "meta": {
            "apiUrl":  o["apiUrl"],
            "notes":   o.get("notes", "")
        }
    })

    print("Done. Verify files in:", KEYS_OUT_DIR)

if __name__ == "__main__":
    main()
