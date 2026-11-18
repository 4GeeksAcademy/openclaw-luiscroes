---
name: get-project-feedback
description: When Luis asks for feedback or review status on one of his projects by name, retrieve its review result, delivery/review dates, and any available feedback or grade.
---

# Get project review and feedback

1. Extract the project title or distinguishing name from Luis's request. Run `scripts/get_project_review.py "<project name>"`; the helper loads `TOKEN_4GEEKS` from the environment or, if absent, reads only that variable from `~/.openclaw/.env`.
2. The helper may call only `GET /v1/assignment/user/me/task` with `task_type=PROJECT` to resolve the name, then `GET /v1/assignment/task/{task_id}` for the unique match. Keep the ID internal; never output or persist IDs or raw responses.
3. If no match is found, say the project could not be found. If multiple names match, return safe titles only and ask Luis which one he means; do not fetch or disclose details for ambiguous matches.
4. For a unique match, report the review result from task/revision status as `aprobado`, `rechazado` or `pendiente de revisión`; include delivery and review dates when present, converted to Madrid time if timestamps have a timezone. Do not infer missing dates or statuses.
5. Include feedback/comment or grade only when the detail response actually contains a non-empty such field. If no feedback or grade is present, explicitly say the API does not provide it for this project. Do not expose IDs, email addresses, private URLs, unrelated description text, or other personal fields.
6. If either API call fails, report that the result could not be retrieved and do not present partial data as a full result. Confirm that the final output contains only project title, review result, dates, and available feedback/grade.
