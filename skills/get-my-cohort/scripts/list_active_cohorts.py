#!/usr/bin/env python3
"""List active 4Geeks cohort enrollments with safe fields only."""

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

URL = "https://breathecode.herokuapp.com/v1/admissions/user/me"
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


def format_date(value):
    if not isinstance(value, str) or not value.strip():
        return ""
    try:
        dt = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(MADRID).strftime("%d/%m/%Y")
    except ValueError:
        return ""


def days_remaining(value):
    if not isinstance(value, str) or not value.strip():
        return "no disponible"
    try:
        dt = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        if dt.tzinfo is None:
            end_date = dt.date()
        else:
            end_date = dt.astimezone(MADRID).date()
        return str((end_date - datetime.now(MADRID).date()).days)
    except ValueError:
        return "no disponible"


def safe_text(value, fallback):
    if not isinstance(value, str) or not value.strip():
        return fallback
    value = " ".join(value.split())
    if "@" in value or "http://" in value.lower() or "https://" in value.lower():
        return fallback
    return value[:180]


def main():
    token = load_token()
    if not token:
        print("ERROR\tCREDENTIAL_MISSING")
        return 0
    request = urllib.request.Request(URL, headers={"Authorization": "Token " + token, "Accept": "application/json"}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            status = response.status
            body = response.read(8 * 1024 * 1024)
    except urllib.error.HTTPError as error:
        status, body = error.code, b""
    except (urllib.error.URLError, TimeoutError, OSError):
        token = None
        print("ERROR\tNETWORK_ERROR")
        return 0
    finally:
        request = None
    token = None
    if status in (401, 403):
        print("ERROR\tTOKEN_REJECTED")
        return 0
    if status != 200:
        print("ERROR\tSERVICE_ERROR")
        return 0
    try:
        data = json.loads(body.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError):
        print("ERROR\tINVALID_RESPONSE")
        return 0
    if not isinstance(data, dict) or not isinstance(data.get("cohorts"), list):
        print("ERROR\tINVALID_RESPONSE")
        return 0
    active_count = 0
    started = []
    main_programs = []
    for enrollment in data["cohorts"]:
        if not isinstance(enrollment, dict) or str(enrollment.get("educational_status", "")).strip().upper() != "ACTIVE":
            continue
        cohort = enrollment.get("cohort")
        if not isinstance(cohort, dict):
            continue
        active_count += 1
        stage_value = cohort.get("stage")
        stage = stage_value.strip().upper() if isinstance(stage_value, str) else ""
        name = safe_text(cohort.get("name"), "Nombre no disponible")
        start = format_date(cohort.get("kickoff_date")) or "no disponible"
        ending = cohort.get("ending_date")
        end = format_date(ending) or ("sin fecha prevista" if cohort.get("never_ends") is True else "no disponible")
        if stage == "STARTED":
            started.append(name)
            main_programs.append((name, start, end, days_remaining(ending)))

    if len(main_programs) > 1:
        print(f"MAIN_PROGRAMS\t{len(main_programs)}")
        for name, start, end, days in main_programs:
            print(f"PROGRAM\t{name}\t{start}\t{end}\t{days}")
    elif main_programs:
        name, start, end, days = main_programs[0]
        print(f"PROGRAM\t{name}\t{start}\t{end}\t{days}")
    else:
        print("PROGRAM\tNO_STARTED_PROGRAM")
    print(f"ACTIVE_MODULES\t{active_count}")
    for name in started:
        print(f"STARTED_MODULE\t{name}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        print("ERROR\tCHECK_ERROR")
        sys.exit(0)
