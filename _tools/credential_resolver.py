#!/usr/bin/env python3
"""
CredentialResolver — cascade credential lookup across pskills, aitools, skills, Keys/.

Search order and paths are defined in ~/.credentials/config.json.
Providers are skipped gracefully if their path does not exist on the current machine.

Usage:
    from credential_resolver import CredentialResolver

    resolver = CredentialResolver()
    token  = resolver.get("todoist", "api.apiToken")
    creds  = resolver.get("dmedev5")
    resolver.put("amplenote", "oauth.accessToken", new_token)
"""

import base64
import json
import logging
import os
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = Path.home() / ".credentials" / "config.json"


class CredentialNotFoundError(Exception):
    pass


class CredentialResolver:
    def __init__(self, config_path: Path = None):
        config_path = Path(config_path) if config_path else DEFAULT_CONFIG
        if not config_path.exists():
            raise FileNotFoundError(f"Resolver config not found: {config_path}")

        with open(config_path) as f:
            self._config = json.load(f)

        key_path = Path(self._config["decryption_key_path"])
        if not key_path.exists():
            raise FileNotFoundError(f"DevKey not found: {key_path}")
        self._key = base64.b64decode(key_path.read_text().strip())

        self._aliases: dict[str, str] = self._config.get("aliases", {})
        self._providers: list[dict] = [
            p for p in self._config["search_paths"]
            if Path(p["keys_path"]).exists()
        ]

        skipped = [
            p["name"] for p in self._config["search_paths"]
            if not Path(p["keys_path"]).exists()
        ]
        if skipped:
            logger.debug("Skipped unavailable providers: %s", skipped)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, name: str, field: str = None) -> Any:
        """
        Get a credential by name (alias or canonical).
        Optionally specify a dot-separated field path, e.g. "api.apiToken".
        Returns the full decrypted credentials dict if field is None.
        """
        canonical = self._aliases.get(name, name)
        key_file = self._find(canonical)
        if key_file is None:
            raise CredentialNotFoundError(
                f"No key file found for '{name}' (canonical: '{canonical}') "
                f"across providers: {self.providers()}"
            )

        data = json.loads(key_file.read_text())
        creds = self._decrypt_all(data.get("encryptedCredentials", {}))

        if field is None:
            return creds

        return self._dig(creds, field)

    def put(self, name: str, field: str, value: str):
        """
        Write an updated value back to the key file that owns this credential.
        Re-encrypts the field in place.
        """
        canonical = self._aliases.get(name, name)
        key_file = self._find(canonical)
        if key_file is None:
            raise CredentialNotFoundError(f"Cannot write back: '{name}' not found")

        data = json.loads(key_file.read_text())
        self._set_encrypted(data["encryptedCredentials"], field, value)
        key_file.write_text(json.dumps(data, indent=4))
        logger.info("Updated %s.%s in %s", name, field, key_file.name)

    def providers(self) -> list[str]:
        """Returns the names of providers available on this machine."""
        return [p["name"] for p in self._providers]

    def find(self, name: str) -> str | None:
        """Returns which provider owns the credential, or None."""
        canonical = self._aliases.get(name, name)
        for provider in self._providers:
            key_file = Path(provider["keys_path"]) / f"{canonical.lower()}-keys.json"
            if key_file.exists():
                return provider["name"]
        return None

    def missing(self) -> list[str]:
        """Returns aliases that have no key file in any provider."""
        return [
            alias for alias, canonical in self._aliases.items()
            if self.find(alias) is None
        ]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _find(self, canonical: str) -> Path | None:
        for provider in self._providers:
            key_file = Path(provider["keys_path"]) / f"{canonical.lower()}-keys.json"
            if key_file.exists():
                logger.debug("Resolved '%s' via provider '%s'", canonical, provider["name"])
                return key_file
        return None

    def _decrypt_all(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: self._decrypt_all(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._decrypt_all(i) for i in obj]
        if isinstance(obj, str) and obj.startswith("ENC:"):
            return self._decrypt(obj)
        return obj

    def _decrypt(self, enc_value: str) -> str:
        data = base64.b64decode(enc_value.removeprefix("ENC:"))
        iv, ct = data[:16], data[16:]
        cipher = Cipher(algorithms.AES(self._key), modes.CBC(iv))
        dec = cipher.decryptor()
        padded = dec.update(ct) + dec.finalize()
        pad_len = padded[-1]
        return padded[:-pad_len].decode("utf-8")

    def _encrypt(self, plaintext: str) -> str:
        padder = padding.PKCS7(128).padder()
        padded = padder.update(plaintext.encode()) + padder.finalize()
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self._key), modes.CBC(iv))
        enc = cipher.encryptor()
        ct = enc.update(padded) + enc.finalize()
        return "ENC:" + base64.b64encode(iv + ct).decode()

    def _dig(self, obj: dict, field: str) -> Any:
        parts = field.split(".")
        for part in parts:
            if not isinstance(obj, dict) or part not in obj:
                raise KeyError(f"Field path '{field}' not found in credentials")
            obj = obj[part]
        return obj

    def _set_encrypted(self, obj: dict, field: str, value: str):
        parts = field.split(".")
        for part in parts[:-1]:
            obj = obj[part]
        obj[parts[-1]] = self._encrypt(value)
