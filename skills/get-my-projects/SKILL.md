---
name: get-my-projects
description: When Luis asks what his projects are or their statuses, fetch only his assigned PROJECT tasks from the 4Geeks student API and list title and category.
---

# Get my projects

1. Run `scripts/list_projects.py` with Python 3. It uses the same token-loading rules as `skills/authenticate-4geeks/scripts/check_session.py` and calls only `GET /v1/assignment/user/me/task` with `task_type=PROJECT`.
2. Follow pagination using a high page size and increasing `offset` until a page contains fewer than the requested limit. Keep responses in memory only; never write API data to disk, log raw responses, or print IDs, URLs, emails, or other personal fields.
3. Map each result as follows: `task_status=PENDING` → `pendiente`; `task_status=DONE` with no approved/rejected revision → `entregado`; approved task/revision → `calificado`; rejected task/revision → `calificado (rechazado)`. If conflicting, missing, or unknown status values prevent a safe mapping, place it in `estado desconocido` and do not guess.
4. Use only a sanitized project title and the mapped category from the helper output. Group projects under `Pendiente (N)`, `Entregado (N)`, and `Calificado (N)` headings; annotate rejected projects with `(rechazado)`. Report unknown states separately if any. If the API request fails, explain briefly and do not present partial results as complete.
5. Verify that the output contains only titles, statuses, and counts. If a title is missing, use `Proyecto sin título`; never substitute an ID or URL.
