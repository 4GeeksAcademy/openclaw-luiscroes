---
name: study-session-scheduler
description: Creates a complete Google Calendar study-session event from a plain-language description (day, part of day, duration, topic), using Luis's Madrid time zone and calendar defaults. Use when a message starts with "Agenda:" or Luis asks to schedule or block time to study.
---

# Study session scheduler

Turn a plain-language request such as "el jueves por la tarde, dos horas, OpenClaw" into a correct Google Calendar event.

## When to use
- The message starts with `Agenda:`.
- Luis asks to "agendar / bloquear / reservar" time to study, review or work on a course topic.
- Do **not** use it for meetings with other people (they need invitations, which require his explicit approval).

## Prerequisites
- Read `TOOLS.md` (calendar `4Geeks OpenClaw Tests`, 2-hour default, 30-minute reminder, no guests) and `USER.md` (Europe/Madrid, study only between 09:00 and 22:00).
- Zapier MCP tools available: `inspect_zapier_actions` and `execute_zapier_write_action`.
- The Zapier action **Google Calendar: Create Detailed Event** is enabled.

## Procedure
1. **Extract** from the message: day, time or part of day, duration, topic.
2. **Resolve the day** against today's date in Europe/Madrid:
   - `hoy`, `mañana`, `pasado mañana`; weekday names mean the **next** occurrence of that day (if today is that weekday and the time has not passed, use today).
   - If no day can be determined, ask exactly one question ("¿Qué día?") and stop.
3. **Resolve the start time:** exact time if given; otherwise mañana 10:00, mediodía 13:00, tarde 16:00, noche 20:00.
4. **Duration:** as given ("dos horas", "90 min"); otherwise 2 hours.
5. **Check the limits** from `USER.md`: the session must start at or after 09:00 and end at or before 22:00. If it does not fit, move it to the closest valid slot the same day and say so.
6. **Time zone:** write start and end as ISO 8601 with the Madrid offset: `+01:00` in winter, `+02:00` from the last Sunday of March to the last Sunday of October.
7. **Build the event:**
   - Calendar: `4Geeks OpenClaw Tests`
   - Title: `Estudio · <Topic>` (topic in Spanish, capitalised; `Estudio · Bootcamp` if no topic)
   - Description: `Objetivo: <one sentence goal based on the topic and his current module in USER.md>` + `Creado por Kai 🤖`
   - Reminder: 30 minutes before (popup) if the action supports reminders; otherwise keep the calendar defaults and mention it.
   - No attendees, no video conference.
8. **Create the event:** call `inspect_zapier_actions` to confirm the parameters of *Google Calendar: Create Detailed Event*, then call `execute_zapier_write_action`.
9. **Confirm on Telegram** in one message:
   - `📅 <title>`
   - `<weekday> DD/MM/YYYY · HH:MM-HH:MM (Madrid)`
   - `Calendario: 4Geeks OpenClaw Tests`
   - the event link on its own line.

## Expected output
- One event in calendar `4Geeks OpenClaw Tests` at the exact resolved date and time (Europe/Madrid), correct duration, title `Estudio · <Topic>`, no guests.
- Luis receives one Telegram message with the details and a working event link.

## Special cases
- **Ambiguous day** (e.g. "el próximo fin de semana"): ask one short question with two options ("¿sábado o domingo?").
- **Request includes other people:** do not invite anyone; create the event only for Luis and ask whether he wants to invite them.
- **Zapier call fails:** retry once; if it fails again, tell Luis the event was **not** created and show the details so he can add it manually.
- **Time in the past:** do not create it; ask whether he meant the next occurrence.
