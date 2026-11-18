#!/usr/bin/env python3
"""Resolve a project by title and emit only its review state and safe feedback fields."""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = "https://breathecode.herokuapp.com"
TASKS_URL = BASE + "/v1/assignment/user/me/task"
PAGE_SIZE = 1000
MAX_PAGES = 100
MADRID = ZoneInfo("Europe/Madrid")


def load_token():
    token = os.environ.get("TOKEN_4GEEKS")
    if token:
        return token.strip()
    try:
        with (Path.home() / ".openclaw" / ".env").open("r", encoding="utf-8") as f:
            for line in f:
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


def request_json(token, url):
    req = urllib.request.Request(url, headers={"Authorization": "Token " + token, "Accept": "application/json"}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            status = response.status
            body = response.read(8 * 1024 * 1024)
    except urllib.error.HTTPError as e:
        status, body = e.code, b""
    except (urllib.error.URLError, TimeoutError, OSError):
        return None, "NETWORK_ERROR"
    finally:
        req = None
    if status in (401, 403):
        return None, "TOKEN_REJECTED"
    if status != 200:
        return None, "SERVICE_ERROR"
    try:
        return json.loads(body.decode("utf-8")), None
    except (UnicodeError, json.JSONDecodeError):
        return None, "INVALID_RESPONSE"


def unwrap(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("results", "tasks", "data"):
            if isinstance(data.get(key), list):
                return data[key]
    return None


def normalize(s):
    return " ".join(s.casefold().split()) if isinstance(s, str) else ""


def title_of(item):
    for key in ("title", "name"):
        val = item.get(key)
        if isinstance(val, str) and val.strip():
            return " ".join(val.split())
    asset = item.get("asset")
    if isinstance(asset, dict):
        for key in ("title", "name"):
            val = asset.get(key)
            if isinstance(val, str) and val.strip():
                return " ".join(val.split())
    return "Proyecto sin título"


def enum_value(obj, *keys):
    for key in keys:
        val = obj.get(key) if isinstance(obj, dict) else None
        if isinstance(val, str) and val.strip():
            return val.strip().upper()
        if isinstance(val, dict):
            for nested in ("status", "slug", "name"):
                x = val.get(nested)
                if isinstance(x, str) and x.strip():
                    return x.strip().upper()
    return ""


def fetch_tasks(token):
    results = []
    offset = 0
    for _ in range(MAX_PAGES):
        query = urllib.parse.urlencode({"task_type": "PROJECT", "limit": PAGE_SIZE, "offset": offset})
        data, error = request_json(token, TASKS_URL + "?" + query)
        if error:
            return None, error
        items = unwrap(data)
        if items is None:
            return None, "INVALID_RESPONSE"
        results.extend(x for x in items if isinstance(x, dict))
        if len(items) < PAGE_SIZE:
            return results, None
        offset += len(items)
    return None, "PAGINATION_LIMIT_REACHED"


def fmt_date(value):
    if not isinstance(value, str) or not value.strip():
        return ""
    try:
        dt = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(MADRID).strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return ""


def safe_text(value):
    if not isinstance(value, str):
        return ""
    value = " ".join(value.split())
    if not value or "@" in value or "http://" in value.lower() or "https://" in value.lower():
        return ""
    return value[:2000]


def status_label(detail):
    task_status = enum_value(detail, "task_status", "status")
    revision_status = enum_value(detail, "revision_status")
    status = revision_status or task_status
    if status == "APPROVED":
        return "aprobado"
    if status == "REJECTED":
        return "rechazado"
    if status in ("PENDING", "DONE", ""):
        return "pendiente de revisión" if status in ("PENDING", "DONE") else "desconocido"
    return "desconocido"


def find_optional_feedback(detail):
    feedback = ""
    grade = ""
    feedback_keys = {"feedback", "comment", "comments", "review_comment", "review_feedback", "teacher_feedback"}
    grade_keys = {"grade", "score", "rating", "points"}
    def walk(obj, depth=0):
        nonlocal feedback, grade
        if depth > 5 or feedback and grade:
            return
        if isinstance(obj, dict):
            for key, value in obj.items():
                k = str(key).casefold()
                if k in feedback_keys and isinstance(value, str) and value.strip() and not feedback:
                    feedback = safe_text(value)
                elif k in grade_keys and isinstance(value, (str, int, float)) and not isinstance(value, bool) and not grade:
                    grade = safe_text(str(value))
                if isinstance(value, (dict, list)):
                    walk(value, depth + 1)
        elif isinstance(obj, list):
            for value in obj[:20]:
                walk(value, depth + 1)
    walk(detail)
    return feedback, grade


def main():
    if len(sys.argv) < 2 or not " ".join(sys.argv[1:]).strip():
        print("ERROR\tPROJECT_NAME_REQUIRED")
        return 0
    query = " ".join(sys.argv[1:]).strip()
    token = load_token()
    if not token:
        print("ERROR\tCREDENTIAL_MISSING")
        return 0
    tasks, error = fetch_tasks(token)
    if error:
        token = None
        print("ERROR\t" + error)
        return 0
    needle = normalize(query)
    matches = [item for item in tasks if needle in normalize(title_of(item))]
    if not matches:
        token = None
        print("NOT_FOUND")
        return 0
    if len(matches) > 1:
        print("AMBIGUOUS")
        for item in matches:
            print("MATCH\t" + title_of(item)[:240])
        token = None
        return 0
    item = matches[0]
    task_id = item.get("id") or item.get("task_id")
    title = title_of(item)
    if task_id is None:
        token = None
        print("ERROR\tTASK_ID_MISSING")
        return 0
    url = BASE + "/v1/assignment/task/" + urllib.parse.quote(str(task_id), safe="")
    detail, error = request_json(token, url)
    token = None
    task_id = None
    if error:
        print("ERROR\t" + error)
        return 0
    if not isinstance(detail, dict):
        print("ERROR\tINVALID_RESPONSE")
        return 0
    print("TITLE\t" + title[:240])
    print("RESULT\t" + status_label(detail))
    delivered = fmt_date(detail.get("delivered_at"))
    reviewed = fmt_date(detail.get("reviewed_at"))
    print("DELIVERED\t" + (delivered or "no disponible"))
    print("REVIEWED\t" + (reviewed or "no disponible"))
    feedback, grade = find_optional_feedback(detail)
    print("FEEDBACK\t" + (feedback or "La API no proporciona feedback para este proyecto."))
    print("GRADE\t" + (grade or "La API no proporciona nota para este proyecto."))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        print("ERROR\tCHECK_ERROR")
        sys.exit(0)
