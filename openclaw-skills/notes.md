# OpenClaw Skills - Evidencias de prueba

Pruebas reales hechas desde Telegram el 15/11/2026 con Kai, después de configurar los cinco archivos y de instalar las skills (`openclaw skills list` las muestra como **ready**, origen `openclaw-workspace`).

## 1. `learning-journal` → Google Docs
- **Input (Telegram):** `Diario: OpenClaw skills` + cuatro puntos reales de lo aprendido en este módulo.
- **Output:** documento nuevo `2026-11-15 · Diario de aprendizaje · OpenClaw skills` con las secciones *Resumen*, *Lo que aprendí*, *Por qué importa*, *Cómo lo aplicaré*, *Dudas abiertas* y la firma `— Kai 🤖`. Kai respondió en Telegram con el título y el enlace real.
- **Refleja la configuración:** español y tono directo (`SOUL.md`), relación con el bootcamp de 4Geeks y TrackFlow (`USER.md`), convención de título (`TOOLS.md`), firma (`IDENTITY.md`), sugerencias marcadas como tales y sin inventar datos (`AGENTS.md`).
- Capturas: `01-telegram-diario-aprendizaje.jpg`, `02-google-docs-diario-aprendizaje.jpg`.

## 2. `study-session-scheduler` → Google Calendar
- **Input (Telegram):** `Agenda: el jueves por la tarde, dos horas, repasar OpenClaw skills`.
- **Output:** evento `Estudio · OpenClaw skills`, jueves 19/11/2026, 16:00-18:00 (Europe/Madrid), en el calendario `4Geeks OpenClaw Tests`, con descripción del objetivo, recordatorio 30 minutos antes y sin invitados. Kai respondió con día, hora, calendario y enlace.
- **Refleja la configuración:** "tarde" → 16:00 y duración 2 h por defecto, calendario y recordatorio de `TOOLS.md`, horario permitido 09:00-22:00 y zona horaria de `USER.md`, sin invitar a nadie (`AGENTS.md`).
- Capturas: `03-telegram-agenda-estudio.jpg`, `04-google-calendar-evento-estudio.jpg`.

## Diagnóstico
`openclaw doctor --lint`: **0 errores**. Quedan 3 avisos que no bloquean: un alias de modelo no usado, la clave del proveedor guardada en `openclaw.json` (fuera del repositorio) y la recomendación de migrar `TOOLS.md` a `AGENTS.md`, que se mantiene porque el proyecto exige `TOOLS.md`.
