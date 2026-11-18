---
name: get-pending-work
description: When Luis asks what work is left to submit or complete, fetch his pending tasks and rejected submissions from the 4Geeks student API, grouped by task type.
---

# Get pending work

1. Run `scripts/list_pending_work.py` with Python 3. It uses `TOKEN_4GEEKS` from the process environment or, if absent, reads only that variable from `~/.openclaw/.env`. It must call only `GET /v1/assignment/user/me/task` with `task_status=PENDING` and `task_status=DONE`, using pagination for both.
2. Keep all API responses in memory. Never save or log response bodies, and never output emails, IDs, private URLs, or fields other than sanitized title, task type, status, and totals.
3. Include all `PENDING` tasks and only the `DONE` tasks whose `revision_status` is `REJECTED`. Label rejected items `rechazado; requiere corrección`. Do not show completed or approved items.
4. Group by task type in this order: projects (`PROJECT`), exercises (`EXERCISE`), lessons (`LESSON`), quizzes (`QUIZ`), then other/unknown types. Show the total number of listed pending items first, including rejected items.
5. Use only titles from the helper output, replacing missing titles with `Tarea sin título`. If fetching either filter fails or pagination is incomplete, report an error and do not present partial output as complete. Verify the response contains only totals, group labels, sanitized titles, and statuses.
