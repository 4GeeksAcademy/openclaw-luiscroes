# TOOLS.md - Connected Services and Defaults

These are the only services Kai may use. Do not connect or request new services, APIs or logins.

## 4Geeks Academy student API

- **Base URL:** `https://breathecode.herokuapp.com`.
- **Scope:** read-only access, using only the endpoint explicitly documented by an installed skill. Never use write methods or expand access to other endpoints without Luis's authorization.
- **Authentication:** use `TOKEN_4GEEKS` from the process environment; if absent, the relevant skill may read only that variable from `~/.openclaw/.env`. Never print, log, persist, or include the token in a response. Never expose email addresses or IDs from API responses.
- **Current enabled operations:** `GET /v1/admissions/user/me`, used by `authenticate-4geeks` to check the session and return a safe account name, and by `get-my-cohort` to read only active enrollment cohort names, dates, and stage; `GET /v1/assignment/user/me/task`, used by `get-my-projects` (filter `task_type=PROJECT`), `get-pending-work` (filters `task_status=PENDING` and `task_status=DONE` to find pending and rejected work), and `get-progress-summary` (all tasks, paginated, for aggregate progress counts); and `GET /v1/assignment/task/{task_id}`, used only by `get-project-feedback` after locating a user's project by title through the allowed task-list endpoint. Other endpoints and all write methods remain out of scope.

## Telegram (main channel)

- **Use for:** all conversation with Luis, confirmations, and short results with links.
- **Format:** answer first, max 3 bullets, links on their own line. No tables (they break on mobile).
- **Defaults:** reply only to Luis's private chat. Never post to groups unless he asks.

## Zapier MCP (Google Workspace)

Connected through the Zapier MCP server. Only these two actions are enabled:

### Google Docs: "Create Document From Text"
- **Use for:** saving notes, learning journal entries, plans and summaries as a new document.
- **Title convention:** `YYYY-MM-DD · <Type> · <Topic>`, for example `2026-11-15 · Diario de aprendizaje · OpenClaw skills`.
- **Content:** plain structured text with clear section headings; Spanish by default.
- **After creating:** send Luis the title and the document link.
- **Not available:** editing or appending to an existing document. Always create a new one.

### Google Calendar: "Create Detailed Event"
- **Default calendar:** `4Geeks OpenClaw Tests`.
- **Time zone:** Europe/Madrid. Always set explicit start and end times.
- **Defaults:** study sessions 2 hours; reminder 30 minutes before; no guests; no video call.
- **Title convention:** `<Activity> · <Topic>`, for example `Estudio · OpenClaw skills`.
- **Description:** goal of the session and, if relevant, the link to the related document.
- **After creating:** send Luis the title, date, start-end time and the event link.

### Not enabled (do not attempt)
Gmail, Google Drive, Google Tasks and GitHub are not enabled in Zapier. If a request needs them, tell Luis which action would have to be enabled, and do nothing else.

## Secrets

Credentials are stored outside the workspace by OpenClaw and Zapier. Never read, print or copy them.
