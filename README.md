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
├── SOUL.md
└── USER.md
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

---

**Project:** Configurando tu Agente de IA Personal con OpenClaw  
**Institution:** 4Geeks Academy  
**GitHub:** [4GeeksAcademy/openclaw-luiscroes](https://github.com/4GeeksAcademy/openclaw-luiscroes)
