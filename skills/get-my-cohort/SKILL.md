---
name: get-my-cohort
description: When Luis asks which cohort or module he is currently enrolled in or when it ends, show only ACTIVE cohort names, start/end dates, and stage.
---

# Get my active cohorts

1. Run `scripts/list_active_cohorts.py` with Python 3. The helper uses `TOKEN_4GEEKS` from the environment or reads only that variable from `~/.openclaw/.env` if absent.
2. Call only `GET /v1/admissions/user/me`. Keep the response in memory; never save or log it, and never display email addresses, IDs, slugs, URLs, financial status, or unrelated profile fields.
3. In the enrollment list, identify the main program as the entry whose cohort `stage` is `STARTED`; report only that program's name, kickoff/start date, ending date, and days remaining. Compute remaining calendar days from today's date in `Europe/Madrid`; say `fecha de fin no disponible` if there is no ending date.
4. Count all enrollments with `educational_status=ACTIVE` as active modules, but list names only for active entries whose cohort `stage` is `STARTED`. Report the active-module count separately from that short name list, and do not expose modules whose stage is `INACTIVE`.
5. If multiple program entries have `stage=STARTED`, report them as multiple rather than guessing which is primary; if there is none, state that no STARTED program was returned. If the API fails, report that the information could not be retrieved without partial results.
6. Verify output contains only the main cohort's name/dates/days remaining, count of ACTIVE module enrollments, and names of the STARTED ACTIVE modules. Never display IDs, emails, slugs, URLs, financial fields, or raw responses.
