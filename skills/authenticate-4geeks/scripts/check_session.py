#!/usr/bin/env python3
"""Safely check the authenticated 4Geeks student session."""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = "https://breathecode.herokuapp.com"
ENDPOINT = "/v1/admissions/user/me"


def load_token():
    token = os.environ.get("TOKEN_4GEEKS")
    if token:
        return token.strip()

    env_path = Path.home() / ".openclaw" / ".env"
    try:
        # Parse only the requested key; never print or expose file contents.
        with env_path.open("r", encoding="utf-8") as env_file:
            for line in env_file:
                candidate = line.strip()
                if not candidate or candidate.startswith("#") or "=" not in candidate:
                    continue
                key, value = candidate.split("=", 1)
                if key.strip() == "TOKEN_4GEEKS":
                    value = value.strip()
                    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
                        value = value[1:-1]
                    return value
    except (OSError, UnicodeError):
        return None
    return None


def safe_name(data):
    """Return an account display name, never email/IDs or arbitrary payload."""
    if not isinstance(data, dict):
        return None
    # Only allow simple text values in name-like fields.
    for key in ("username", "user_name", "name", "first_name"):
        value = data.get(key)
        if isinstance(value, str) and value.strip() and "@" not in value:
            return " ".join(value.split())[:100]
    profile = data.get("profile")
    if isinstance(profile, dict):
        for key in ("username", "user_name", "name", "first_name"):
            value = profile.get(key)
            if isinstance(value, str) and value.strip() and "@" not in value:
                return " ".join(value.split())[:100]
    return None


def main():
    token = load_token()
    if not token:
        print("CREDENTIAL_MISSING")
        return 2

    request = urllib.request.Request(
        BASE_URL + ENDPOINT,
        headers={"Authorization": "Token " + token, "Accept": "application/json"},
        method="GET",
    )
    # Drop the local reference before processing any response; never log request/headers.
    token = None

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            status = response.status
            body = response.read(1024 * 1024)
    except urllib.error.HTTPError as error:
        status = error.code
        # Do not read or print error bodies; they may contain personal data.
        body = b""
    except (urllib.error.URLError, TimeoutError, OSError):
        print("NETWORK_ERROR")
        return 3
    finally:
        request = None

    if status in (401, 403):
        print("TOKEN_REJECTED")
        return 0
    if status != 200:
        print("SERVICE_ERROR")
        return 0

    try:
        data = json.loads(body.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError):
        print("ACTIVE")
        return 0

    name = safe_name(data)
    if name:
        # Sanitized output: only a bounded display-name field.
        print("ACTIVE\t" + name.replace("\t", " ").replace("\n", " "))
    else:
        print("ACTIVE")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # Fail closed; never emit exceptions that may contain request details.
        print("CHECK_ERROR")
        sys.exit(4)
