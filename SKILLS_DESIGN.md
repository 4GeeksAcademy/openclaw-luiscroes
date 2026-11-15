# SKILLS_DESIGN.md - Design of Kai's custom skills

Two skills for Kai, my OpenClaw assistant. Both remove a task I repeat every week during the 4Geeks AI Engineering bootcamp, and both use only the services already connected (Telegram and the two Zapier actions listed in `TOOLS.md`). No new API, OAuth flow or external service is needed.

| Skill | Trigger (Telegram) | Connected service | Result |
|---|---|---|---|
| `learning-journal` | "Diario: ..." + what I learned today | Google Docs - *Create Document From Text* | A structured journal entry as a new Google Doc |
| `study-session-scheduler` | "Agenda: ..." + a session in plain language | Google Calendar - *Create Detailed Event* | A complete event in the `4Geeks OpenClaw Tests` calendar |

---

## Skill 1 - `learning-journal`

### 1. What does this skill do?
It turns a few quick notes about what I learned today into a structured learning-journal entry and saves it as a new Google Doc.

### 2. What input does the agent need?
- **What I give it:** a Telegram message starting with `Diario:` followed by 2-6 short points, in Spanish or English, written fast from my phone. Optionally a topic after the colon (`Diario: OpenClaw skills`).
- **What it already knows from the five files:**
  - `USER.md`: who I am, that I am studying AI Engineering at 4Geeks, my current projects (bootcamp module, TrackFlow, Novalta) and my goal of turning lessons into reusable notes.
  - `SOUL.md`: write in Spanish, direct and brief, no filler, say when something I wrote looks wrong.
  - `TOOLS.md`: use *Create Document From Text*, the title convention `YYYY-MM-DD · Diario de aprendizaje · <Topic>`, and always send me the link.
  - `AGENTS.md`: never add secrets to documents; never claim it was saved without the tool's confirmation.
- **Why this input:** quick bullet points are what I actually have at the end of a class. Anything longer would stop me from using it.

### 3. What does a good output look like?
- **Format:** a new Google Doc with these sections, in Spanish:
  1. *Resumen* - one sentence.
  2. *Lo que aprendí* - my points, rewritten clearly, without inventing new facts.
  3. *Por qué importa* - how it connects to my current projects from `USER.md`.
  4. *Cómo lo aplicaré* - 1-3 concrete actions.
  5. *Dudas abiertas* - only if my notes leave something unclear.
  6. Signature `— Kai 🤖`.
- **Destination:** Google Docs (new document; the action cannot append).
- **How I know it worked:** Kai replies on Telegram with the document title and a real Google Docs link; the document opens, has the title convention and all sections, and contains nothing I did not say except the clearly labelled application ideas.
- **Why this format:** a fixed structure makes the entries easy to review before projects and interviews, and the "why it matters" section is what makes it personal instead of a generic summary.

---

## Skill 2 - `study-session-scheduler`

### 1. What does this skill do?
It turns a study session described in plain language ("el jueves por la tarde, dos horas, OpenClaw") into a complete Google Calendar event with the right date, time, duration and description.

### 2. What input does the agent need?
- **What I give it:** a Telegram message starting with `Agenda:` describing the session in natural language: day (absolute or relative, e.g. "mañana", "el jueves"), part of the day or exact time, optional duration and topic.
- **What it already knows from the five files:**
  - `USER.md`: time zone Europe/Madrid; never schedule study before 09:00 or after 22:00; always give the link.
  - `TOOLS.md`: calendar `4Geeks OpenClaw Tests`, default duration 2 hours, reminder 30 minutes before, no guests, title convention `Estudio · <Topic>`.
  - `SOUL.md`: act first with sensible defaults, ask only one question when a missing detail would change the result.
  - `AGENTS.md`: never invite other people without asking.
- **Why this input:** this is how I think about study time ("Thursday afternoon"), and resolving it into exact times is precisely the repetitive part I want Kai to do.

### 3. What does a good output look like?
- **Format:** one event with title `Estudio · <Topic>`, exact start and end time in Europe/Madrid, description with the goal of the session, reminder 30 minutes before, no guests.
- **Part-of-day defaults:** mañana 10:00, mediodía 13:00, tarde 16:00, noche 20:00 (always inside 09:00-22:00).
- **Destination:** Google Calendar, calendar `4Geeks OpenClaw Tests`.
- **How I know it worked:** Kai replies on Telegram with title, day (DD/MM/YYYY), start-end time, calendar name and the real event link; the event appears in Google Calendar at that exact time. If the day is missing or ambiguous, Kai asks one short question instead of guessing.
- **Why this format:** an event with an explicit time zone and a clear title avoids the most common errors (wrong hour, wrong calendar), and the confirmation lets me check it from my phone without opening the calendar.

---

## Why these two skills
- I use both several times a week, so they pass the "would I trigger it more than once?" test.
- They cover both kinds of skill in the brief: one that **creates new content** (journal) and one that **sharpens an existing behaviour** (calendar events).
- They show the five configuration files at work: the Spanish tone and signature from `SOUL.md`/`IDENTITY.md`, my projects and hours from `USER.md`, and the defaults from `TOOLS.md`.
