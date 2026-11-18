# OpenClaw — Personal AI Assistant

**4Geeks Academy | AI Engineering Project**

A personal AI assistant deployed on a remote VPS using **OpenClaw**, integrated with **4Geeks Academy's LiteLLM gateway**, personalized through natural-language conversation, and version-controlled with Git and GitHub.

## Project Overview

This project demonstrates the installation, configuration, deployment, and personalization of an AI agent in a remote Linux environment.

The assistant, named **Kai 🤖**, runs through OpenClaw and communicates with an AI model using the LiteLLM API provided by 4Geeks Academy.

The project was developed using GitHub Codespaces as the development terminal, with the actual OpenClaw installation hosted separately on a VPS.

## Technology Stack

| Component | Technology |
|---|---|
| AI agent platform | OpenClaw 2026.10.10 |
| Operating system | Ubuntu 22.04.5 LTS |
| Hosting | 4Geeks-provided VPS |
| Development environment | GitHub Codespaces |
| AI provider | 4Geeks Academy LiteLLM gateway |
| AI model | GPT-6 Luna |
| Model API | OpenAI-compatible API |
| Version control | Git |
| Repository hosting | GitHub |
| Remote authentication | SSH with ED25519 key |

## System Architecture

```text
Developer
    |
    v
GitHub Codespaces
    |
    | SSH connection
    v
Ubuntu VPS
    |
    v
OpenClaw Gateway
    |
    v
OpenClaw Agent: Kai 🤖
    |
    | LiteLLM API
    v
4Geeks Academy AI Gateway
    |
    v
GPT-6 Luna
```

The OpenClaw Gateway runs on the VPS and is accessed locally through the terminal interface.

The project repository is synchronized with GitHub using SSH authentication from the VPS.

## Installation and Configuration

The deployment followed these principal stages:

1. Connect to the VPS using SSH from GitHub Codespaces.
2. Verify the Linux environment and available resources.
3. Configure swap memory to support the VPS's limited RAM.
4. Install OpenClaw using the official installation script.
5. Run the OpenClaw onboarding process.
6. Configure LiteLLM as the AI provider.
7. Select a model identifier supported by the 4Geeks LiteLLM gateway.
8. Configure and verify the OpenClaw Gateway service.
9. Test communication with the AI model using the OpenClaw terminal interface.
10. Personalize the assistant through natural-language conversation.
11. Verify the assistant's identity file and Git history.
12. Configure GitHub SSH authentication and upload the workspace.

### LiteLLM Configuration

The installation uses the following API endpoint:

```text
https://llm.4geeks.ai/v1
```

The model identifier successfully used during testing is:

```text
litellm/madrid-spain/opnerouter/openai/gpt-6-luna
```

The model identifier follows the exact naming returned by the provider's model catalog.

**Important:** The API key and other authentication credentials are stored outside this repository and are not included in the source files.

## Assistant Personalization

The assistant was personalized through a conversation in the OpenClaw terminal interface, rather than by manually editing its identity file.

| Attribute | Value |
|---|---|
| Name | Kai |
| Emoji | 🤖 |
| Type | AI assistant |
| Personality | Helpful and approachable |
| Language of greeting | Spanish |

**Greeting:**

> ¡Hola, soy Kai! ¿En qué puedo ayudarte hoy?

The resulting configuration is stored in [`IDENTITY.md`](./IDENTITY.md).

The personalization was recorded in Git commit `f554ad2`:

```text
Personalize assistant identity as Kai
```

This commit provides evidence of the identity configuration performed through the agent conversation.

## Functionality Verification

The OpenClaw installation was successfully tested from the VPS terminal.

Test message:

> Hola, ¿estás funcionando? Responde brevemente en español.

Assistant response:

> Sí, estoy funcionando. Soy tu nuevo asistente: ¿cómo te gustaría llamarme?

This confirmed successful communication between the OpenClaw terminal interface, Gateway, LiteLLM provider, and AI model.

## Hooks and Session Management

OpenClaw detected five bundled hooks as ready:

| Hook | Purpose |
|---|---|
| `boot-md` | Executes startup instructions |
| `bootstrap-extra-files` | Loads additional workspace context |
| `command-logger` | Records command events |
| `compaction-notifier` | Provides session-compaction notices |
| `session-memory` | Saves session context during resets |

The `session-memory` hook was verified as explicitly enabled in the OpenClaw configuration.

The other hooks were confirmed as ready, but were not individually verified as enabled.

## Repository Structure

```text
openclaw-luiscroes/
├── .gitignore
├── AGENTS.md
├── BOOTSTRAP.md
├── IDENTITY.md
├── README.md
├── SKILLS_DESIGN.md
├── SOUL.md
├── TOOLS.md
├── USER.md
├── openclaw-connection/
├── openclaw-skills/
└── skills/
    ├── learning-journal/SKILL.md
    └── study-session-scheduler/SKILL.md
```

### File Descriptions

- **AGENTS.md:** Instructions and operational context for the agent.
- **BOOTSTRAP.md:** Initial agent setup and onboarding instructions.
- **IDENTITY.md:** Assistant identity and greeting.
- **SOUL.md:** Assistant personality and behavior guidelines.
- **USER.md:** Structure for maintaining user preferences.
- **.gitignore:** Exclusions for sensitive and temporary files.
- **README.md:** Project documentation.

## Security Considerations

The project follows basic security practices for remote deployment and version control:

- SSH is used for remote VPS access.
- A dedicated ED25519 SSH key authenticates the VPS with GitHub.
- The SSH private key remains on the VPS.
- LiteLLM API credentials are not committed to GitHub.
- Authentication and environment files are excluded from version control.
- Workspace files were reviewed and scanned for common credential patterns before upload.
- GitHub history was merged and preserved without force-pushing.

The repository contains workspace configuration and documentation, **not** the full OpenClaw installation or its private runtime state.

## Useful Commands

Check OpenClaw installation:

```bash
openclaw --version
```

Inspect the Gateway:

```bash
openclaw gateway status --deep
```

Start the terminal interface:

```bash
openclaw tui
```

Check model configuration:

```bash
openclaw models status
```

Check available hooks:

```bash
openclaw hooks list
```

Inspect Git status:

```bash
git status
```

These commands are intended to run on a VPS with OpenClaw already installed and configured.

## GitHub Version Control

The OpenClaw workspace was initialized as a local Git repository on the VPS and connected to the project repository through SSH.

The histories were merged to preserve both the initial GitHub commit and the OpenClaw personalization commit.

Important commits:

| Commit | Description |
|---|---|
| `f554ad2` | Personalize assistant identity as Kai |
| `535bf28` | Add OpenClaw workspace files and security exclusions |
| `9ebba78` | Merge local workspace with GitHub repository |

The main project branch on GitHub is `main`.

## Project Outcome

The project successfully demonstrates:

- Remote installation and execution of OpenClaw.
- Integration with an external AI model using LiteLLM.
- Successful AI conversations through the terminal interface.
- Conversational personalization of an assistant.
- Persistent identity configuration.
- Verification of OpenClaw hooks.
- Secure SSH-based GitHub authentication.
- Version control and remote workspace backup.

The resulting assistant, **Kai 🤖**, is operational on the VPS and ready for further configuration and experimentation.


## Project 3: Teaching New Skills to Kai

**Project:** Mi Agente, A Mi Manera: Enseñando Nuevas Skills a Tu Asistente Personal

Kai went from a generic assistant to one configured for Luis, with two custom OpenClaw skills that remove weekly repetitive work. Only the services already connected were used (Telegram and two Zapier actions); no new API, OAuth flow or external service was added.

### The five configuration files

| File | What it now defines |
|---|---|
| [`IDENTITY.md`](./IDENTITY.md) | Kai 🤖, greeting and signature for longer outputs |
| [`SOUL.md`](./SOUL.md) | Acts first on clear, reversible requests; asks one question only when a detail would change the result; states uncertainty; Spanish, brief and direct |
| [`AGENTS.md`](./AGENTS.md) | Firm limits: privacy (no personal data outside the private chat, no secrets in files), stop-and-ask before sending to others, inviting, deleting or spending |
| [`USER.md`](./USER.md) | Luis's context: Madrid time zone, work at Novalta, 4Geeks bootcamp, TrackFlow, goals and study hours |
| [`TOOLS.md`](./TOOLS.md) | Telegram, Zapier *Create Document From Text* and *Create Detailed Event*, default calendar, naming conventions, reminders |

### Skills

Designed first in [`SKILLS_DESIGN.md`](./SKILLS_DESIGN.md) (committed before any implementation), then implemented as workspace skills:

| Skill | Trigger | Result |
|---|---|---|
| [`learning-journal`](./skills/learning-journal/SKILL.md) | `Diario: ...` on Telegram | Structured learning-journal entry saved as a new Google Doc |
| [`study-session-scheduler`](./skills/study-session-scheduler/SKILL.md) | `Agenda: ...` on Telegram | Complete study event in the `4Geeks OpenClaw Tests` calendar |

**Why these two:** both are tasks repeated several times a week during the bootcamp; one creates new content and the other sharpens an existing behaviour; and both visibly depend on the five files (tone, projects, hours and defaults).

### Verification

- `openclaw skills list`: both skills **ready**, source `openclaw-workspace`.
- `openclaw doctor --lint`: **0 errors** (3 non-blocking warnings, explained in the evidence notes).
- Real tests from Telegram produced a Google Doc and a Calendar event; evidence in [`openclaw-skills/`](./openclaw-skills/notes.md).

---

**Project:** Configurando tu Agente de IA Personal con OpenClaw  
**Institution:** 4Geeks Academy  
**GitHub:** [4GeeksAcademy/openclaw-luiscroes](https://github.com/4GeeksAcademy/openclaw-luiscroes)

---

## Mi Asistente 4Geeks — skills conectadas a la API de 4Geeks

Kai puede consultar mi progreso en el curso de 4Geeks directamente desde Telegram. Las seis skills se construyeron conversando con Kai, una pregunta a la vez; todo el proceso, con los prompts, las propuestas de Kai y las pruebas reales, está en **[SKILL_LOG.md](./SKILL_LOG.md)**.

| Skill | Pregunta | Endpoint |
|---|---|---|
| `authenticate-4geeks` | ¿Mi token es válido? | `GET /v1/admissions/user/me` |
| `get-my-projects` | ¿Cuáles son mis proyectos y en qué estado están? | `GET /v1/assignment/user/me/task?task_type=PROJECT` |
| `get-pending-work` | ¿Qué me falta por entregar? | `GET /v1/assignment/user/me/task?task_status=PENDING` |
| `get-progress-summary` | ¿Qué tan avanzado estoy? | `GET /v1/assignment/user/me/task` |
| `get-project-feedback` | ¿Qué feedback me dieron en X? | `GET /v1/assignment/task/{task_id}` |
| `get-my-cohort` | ¿En qué cohorte estoy y cuándo termina? | `GET /v1/admissions/user/me` |

**Seguridad:** el token de estudiante vive solo en `~/.openclaw/.env` del servidor (`TOKEN_4GEEKS`, permisos 600), fuera de este repositorio. Ninguna skill lo contiene, lo imprime ni lo guarda, y las respuestas de la API se procesan en memoria.
