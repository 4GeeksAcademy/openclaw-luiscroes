#!/usr/bin/env python3
"""Summarize own 4Geeks task progress; print aggregate counts only."""

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
TASK_TYPES = ("PROJECT", "EXERCISE", "LESSON", "QUIZ")
TYPE_LABELS = {
    "PROJECT": "proyectos",
    "EXERCISE": "ejercicios",
    "LESSON": "lecciones",
    "QUIZ": "quizzes",
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


def fetch_page(token, offset):
    query = urllib.parse.urlencode({"limit": PAGE_SIZE, "offset": offset})
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


def get_status(item, key):
    value = item.get(key) if isinstance(item, dict) else None
    if isinstance(value, str):
        return value.strip().upper()
    if isinstance(value, dict):
        for nested_key in ("status", "slug", "name"):
            nested = value.get(nested_key)
            if isinstance(nested, str) and nested.strip():
                return nested.strip().upper()
    return ""


def get_type(item):
    value = get_status(item, "task_type") or get_status(item, "type")
    if not value and isinstance(item.get("task"), dict):
        value = get_status(item["task"], "task_type") or get_status(item["task"], "type")
    return value or "OTHER"


def main():
    token = load_token()
    if not token:
        print("ERROR\tCREDENTIAL_MISSING")
        return 0

    totals = {kind: 0 for kind in TASK_TYPES}
    completed = {kind: 0 for kind in TASK_TYPES}
    all_total = 0
    all_completed = 0
    approved_projects = 0
    offset = 0

    for _ in range(MAX_PAGES):
        items, error = fetch_page(token, offset)
        if error:
            token = None
            print("ERROR\t" + error)
            return 0
        for item in items:
            if not isinstance(item, dict):
                continue
            all_total += 1
            kind = get_type(item)
            task_status = get_status(item, "task_status") or get_status(item, "status")
            revision_status = get_status(item, "revision_status")
            is_rejected = task_status == "REJECTED" or revision_status == "REJECTED"
            is_completed = not is_rejected and task_status in ("DONE", "APPROVED")
            if kind in totals:
                totals[kind] += 1
                if is_completed:
                    completed[kind] += 1
            if is_completed:
                all_completed += 1
            if kind == "PROJECT" and not is_rejected and (task_status == "APPROVED" or revision_status == "APPROVED"):
                approved_projects += 1
        if len(items) < PAGE_SIZE:
            token = None
            percent = (all_completed * 100.0 / all_total) if all_total else 0.0
            print(f"TOTAL\t{all_completed}\t{all_total}")
            print(f"PERCENT\t{percent:.1f}")
            for kind in TASK_TYPES:
                print(f"TYPE\t{TYPE_LABELS[kind]}\t{completed[kind]}\t{totals[kind]}")
            print(f"APPROVED_PROJECTS\t{approved_projects}")
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
        sys.exit(0)
