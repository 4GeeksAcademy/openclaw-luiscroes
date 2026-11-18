#!/usr/bin/env python3
"""List own 4Geeks projects with sanitized status, keeping API data in memory."""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE_URL = "https://breathecode.herokuapp.com/v1/assignment/user/me/task"
PAGE_SIZE = 1000
MAX_PAGES = 100


def load_token():
    token = os.environ.get("TOKEN_4GEEKS")
    if token:
        return token.strip()
    env_path = Path.home() / ".openclaw" / ".env"
    try:
        with env_path.open("r", encoding="utf-8") as env_file:
            for line in env_file:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                if key.strip() == "TOKEN_4GEEKS":
                    value = value.strip()
                    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
                        value = value[1:-1]
                    return value
    except (OSError, UnicodeError):
        return None
    return None


def unwrap_items(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("results", "tasks", "data"):
            value = data.get(key)
            if isinstance(value, list):
                return value
    return None


def fetch_page(token, offset):
    query = urllib.parse.urlencode({"task_type": "PROJECT", "limit": PAGE_SIZE, "offset": offset})
    request = urllib.request.Request(
        BASE_URL + "?" + query,
        headers={"Authorization": "Token " + token, "Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            status = response.status
            body = response.read(8 * 1024 * 1024)
    except urllib.error.HTTPError as error:
        status = error.code
        body = b""
    except (urllib.error.URLError, TimeoutError, OSError):
        return None, "NETWORK_ERROR"
    finally:
        request = None
    if status in (401, 403):
        return None, "TOKEN_REJECTED"
    if status != 200:
        return None, "SERVICE_ERROR"
    try:
        items = unwrap_items(json.loads(body.decode("utf-8")))
    except (UnicodeError, json.JSONDecodeError):
        return None, "INVALID_RESPONSE"
    if items is None:
        return None, "INVALID_RESPONSE"
    return items, None


def text_field(obj, keys):
    if not isinstance(obj, dict):
        return ""
    for key in keys:
        value = obj.get(key)
        if isinstance(value, str) and value.strip():
            return " ".join(value.split())
    return ""


def get_status(item, key):
    value = item.get(key) if isinstance(item, dict) else None
    if isinstance(value, str):
        return value.strip().upper()
    if isinstance(value, dict):
        return text_field(value, ("status", "slug", "name")).upper()
    return ""


def categorize(item):
    task_status = get_status(item, "task_status")
    revision_status = get_status(item, "revision_status")
    if not task_status:
        task_status = get_status(item, "status")
    # A rejected review is a reviewed/calified outcome, annotated explicitly.
    if task_status == "REJECTED" or revision_status == "REJECTED":
        return "calificado (rechazado)"
    if task_status == "APPROVED" or revision_status == "APPROVED":
        return "calificado"
    if task_status == "PENDING":
        return "pendiente"
    if task_status == "DONE":
        return "entregado"
    return "estado desconocido"


def safe_title(item):
    if not isinstance(item, dict):
        return "Proyecto sin título"
    for key in ("title", "name"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            title = " ".join(value.split())
            # Exclude accidentally returned URLs, email addresses, or control characters.
            if "@" not in title and "http://" not in title.lower() and "https://" not in title.lower():
                return title[:240].replace("\t", " ").replace("\n", " ")
    asset = item.get("asset")
    if isinstance(asset, dict):
        value = text_field(asset, ("title", "name"))
        if value and "@" not in value and "http://" not in value.lower() and "https://" not in value.lower():
            return value[:240].replace("\t", " ").replace("\n", " ")
    return "Proyecto sin título"


def main():
    token = load_token()
    if not token:
        print("ERROR\tCREDENTIAL_MISSING")
        return 2
    grouped = {"pendiente": [], "entregado": [], "calificado": [], "estado desconocido": []}
    offset = 0
    seen = 0
    for _ in range(MAX_PAGES):
        items, error = fetch_page(token, offset)
        if error:
            token = None
            print("ERROR\t" + error)
            return 0
        for item in items:
            if not isinstance(item, dict):
                continue
            title = safe_title(item)
            category = categorize(item)
            if category == "calificado (rechazado)":
                grouped["calificado"].append((title, True))
            elif category in grouped:
                grouped[category].append((title, False))
            seen += 1
        if len(items) < PAGE_SIZE:
            token = None
            for category in ("pendiente", "entregado", "calificado", "estado desconocido"):
                for title, rejected in grouped[category]:
                    print(f"{category}\t{title}\t{'rechazado' if rejected else ''}")
            print("TOTALS\t" + "\t".join(f"{key}={len(grouped[key])}" for key in ("pendiente", "entregado", "calificado", "estado desconocido")))
            return 0
        offset += len(items)
    token = None
    print("ERROR\tPAGINATION_LIMIT_REACHED")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        print("ERROR\tCHECK_ERROR")
        sys.exit(4)
