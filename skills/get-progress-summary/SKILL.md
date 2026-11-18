---
name: get-progress-summary
description: When Luis asks how far along he is in the course, summarize completed tasks by type, overall completion percentage, and approved projects.
---

# Get progress summary

1. Run `scripts/summarize_progress.py` with Python 3. It calls only `GET /v1/assignment/user/me/task` without status/type filters, paginating all results using `limit` and `offset`. It loads `TOKEN_4GEEKS` from the environment or only that variable from `~/.openclaw/.env` if missing.
2. Keep API responses in memory only; never save or log them. The helper must output aggregate counts only, not task titles, IDs, URLs, emails, or response data.
3. Count `DONE` and `APPROVED` task statuses as completed; do not count `REJECTED` or `PENDING`. Count projects approved when their `revision_status` is `APPROVED` or their task status is `APPROVED`.
4. Report counts completed/total for projects, exercises, lessons, and quizzes; also report overall completed/total across every returned task, global percentage, and number of approved projects. Types absent from the response should be reported as `0/0` and identified as none returned, not estimated.
5. If fetching fails or pagination cannot be completed, state that the summary is unavailable; do not report partial counts as complete. Verify the helper completed pagination and output contains aggregate counts only. Do not call `/v1/activity/me` for this skill.
