---
name: learning-journal
description: Turns Luis's quick notes about what he learned today into a structured learning-journal entry saved as a new Google Doc. Use when a message starts with "Diario:" or Luis asks to log, save or note what he learned today.
---

# Learning journal

Turn 2-6 quick notes from Luis into a clear, personal learning-journal entry and save it as a new Google Doc.

## When to use
- The message starts with `Diario:` (optionally followed by a topic, e.g. `Diario: OpenClaw skills`).
- Luis asks to "guardar / apuntar lo que aprendí hoy", "log what I learned" or similar.
- Do **not** use it for meeting notes, plans or general documents.

## Prerequisites
- Read `USER.md` (his course, projects and goals) and `SOUL.md` (tone, Spanish by default).
- Zapier MCP tools available: `inspect_zapier_actions` and `execute_zapier_write_action`.
- The Zapier action **Google Docs: Create Document From Text** is enabled (see `TOOLS.md`).
- At least one real learning point in the message. If there is none, ask one short question: "¿Qué aprendiste hoy?" and stop.

## Procedure
1. **Collect the input.** Take the points after `Diario:`. Detect the topic: use the text right after `Diario:` if given, otherwise infer a 2-4 word topic from the points.
2. **Date.** Use today's date in Europe/Madrid, formatted `YYYY-MM-DD` for the title and `DD/MM/YYYY` in the body.
3. **Write the entry in Spanish** with exactly these sections:
   - `Resumen` - one sentence that captures the main idea.
   - `Lo que aprendí` - each of Luis's points rewritten as a clear bullet. Do not add facts he did not mention.
   - `Por qué importa` - 1-2 bullets linking the lesson to his current projects from `USER.md` (4Geeks bootcamp, TrackFlow, Novalta). Be specific, not generic.
   - `Cómo lo aplicaré` - 1-3 concrete next actions, labelled as suggestions.
   - `Dudas abiertas` - only if something in his notes is unclear or looks wrong; otherwise omit the section.
   - Last line: `— Kai 🤖`
4. **Title:** `YYYY-MM-DD · Diario de aprendizaje · <Topic>`.
5. **Create the document.** Call `inspect_zapier_actions` to confirm the parameters of *Google Docs: Create Document From Text*, then call `execute_zapier_write_action` with the title and the full text.
6. **Confirm on Telegram** in one message:
   - `📓 Entrada guardada: <title>`
   - the document link on its own line
   - one line with the main takeaway.

## Expected output
- A new Google Doc exists with the exact title convention and all required sections.
- The content reflects only Luis's points plus clearly labelled suggestions.
- Luis receives one Telegram message with the title and a working Google Docs link.

## Special cases
- **Zapier call fails:** retry once. If it fails again, tell Luis it was not saved, paste the formatted entry in the chat so nothing is lost, and do not claim success.
- **No link returned:** say the document was created but the link was not returned; never invent a link.
- **Notes contain a password, key or token:** leave it out of the document and remind Luis to rotate it.
- **Very long input (more than 10 points):** keep the 6 most important in `Lo que aprendí` and mention the rest were summarised.
