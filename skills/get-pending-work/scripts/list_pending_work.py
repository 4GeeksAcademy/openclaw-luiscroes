#!/usr/bin/env python3
"""Fetch pending and rejected 4Geeks tasks; output sanitized lines only."""

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
TYPE_ORDER = ("PROJECT", "EXERCISE", "LESSON", "QUIZ")
TYPE_LABELS = {
    "PROJECT": "proyecto",
    "EXERCISE": "ejercicio",
    "LESSON": "lección",
    "QUIZ": "quiz",
}


def load_token():
    token = os.environ.get("TOKEN_4GEEKS")
    if token:
        return token.strip()
    try:
        with (Path.home() / ".openclaw" / ".env").open("r", encoding="utf-8") as env_file:
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
            if isinstance(data.get(key), list):
                return data[key]
    return None


def fetch_page(token, task_status, offset):
    query = urllib.parse.urlencode({"task_status": task_status, "limit": PAGE_SIZE, "offset": offset})
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
        status, body = error.code, b""
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


def fetch_all(token, status):
    all_items = []
    offset = 0
    for _ in range(MAX_PAGES):
        items, error = fetch_page(token, status, offset)
        if error:
            return None, error
        all_items.extend(item for item in items if isinstance(item, dict))
        if len(items) < PAGE_SIZE:
            return all_items, None
        offset += len(items)
    return None, "PAGINATION_LIMIT_REACHED"


def get_text(obj, keys):
    if not isinstance(obj, dict):
        return ""
    for key in keys:
        value = obj.get(key)
        if isinstance(value, str) and value.strip():
            return " ".join(value.split())
    return ""


def safe_title(item):
    title = get_text(item, ("title", "name"))
    if not title and isinstance(item.get("asset"), dict):
        title = get_text(item["asset"], ("title", "name"))
    if not title or "@" in title or "http://" in title.lower() or "https://" in title.lower():
        return "Tarea sin título"
    return title[:240].replace("\t", " ").replace("\n", " ")


def get_value(item, *keys):
    for key in keys:
        value = item.get(key)
        if isinstance(value, str):
            return value.strip().upper()
        if isinstance(value, dict):
            nested = get_text(value, ("status", "slug", "name"))
            if nested:
                return nested.upper()
    return ""


def task_type(item):
    value = get_value(item, "task_type", "type")
    if not value and isinstance(item.get("task"), dict):
        value = get_value(item["task"], "task_type", "type")
    return value if value else "OTHER"


def main():
    token = load_token()
    if not token:
        print("ERROR\tCREDENTIAL_MISSING")
        return 0

    pending, error = fetch_all(token, "PENDING")
    if error:
        print("ERROR\t" + error)
        return 0
    done, error = fetch_all(token, "DONE")
    token = None
    if error:
        print("ERROR\t" + error)
        return 0

    groups = {}
    for item in pending:
        groups.setdefault(task_type(item), []).append((safe_title(item), "pendiente"))

    for item in done:
        revision_status = get_value(item, "revision_status")
        task_status = get_value(item, "task_status", "status")
        if revision_status != "REJECTED" and task_status != "REJECTED":
            continue
        groups.setdefault(task_type(item), []).append((safe_title(item), "rechazado; requiere corrección"))

    ordered_types = [kind for kind in TYPE_ORDER if kind in groups]
    ordered_types += sorted(kind for kind in groups if kind not in TYPE_ORDER)
    total = sum(len(groups[kind]) for kind in ordered_types)
    print(f"TOTAL\t{total}")
    for kind in ordered_types:
        label = TYPE_LABELS.get(kind, "otro")
        print(f"TIPO\t{label}\t{len(groups[kind])}")
        for title, status in groups[kind]:
            print(f"ITEM\t{title}\t{status}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        print("ERROR\tCHECK_ERROR")
        sys.exit(0)
