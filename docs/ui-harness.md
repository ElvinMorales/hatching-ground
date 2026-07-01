# UI Harness

## What the UI harness is

The UI harness is a local, self-contained HTML interface for Hatching Ground. It assembles paste-ready prompts from your context and the selected workflow template, accepts pasted model output, validates it heuristically, and exports Markdown artifacts. It is part of the artifact system, not a replacement for it.

## Why Hatching Ground needs an interface

Using Hatching Ground repeatedly means filling in the same context fields, selecting the right prompt template, and tracking which workflow applies. Without an interface, that mechanical work is manual every time. The harness eliminates the friction without adding a backend, persistence layer, or model API.

## What the MVP UI does

- Lets you select one of eight Hatching Ground workflows.
- Collects context: project area, goal, friction, constraints, privacy notes, build style.
- Accepts a rough idea and/or clutch of candidates.
- Generates a complete, paste-ready prompt for Claude or GPT.
- Lets you copy or download the prompt as `hatching-ground-prompt.txt`.
- Accepts pasted model output.
- Runs heuristic validation (checks for required sections, privacy notes, bounded scope).
- Exports the validated output as a Markdown file with a recommended filename.
- Shows safety warnings throughout.

## What the MVP UI does not do

- It does not call any model API.
- It does not store data between sessions.
- It does not use cookies, localStorage, sessionStorage, or any browser persistence.
- It does not make network calls.
- It does not use external scripts, stylesheets, or fonts.
- It does not send analytics.
- It does not log user input to the console.
- It does not deploy or operate any agent.

## How to open `ui/hatching-ground.html`

Open the file directly in a web browser:

```
# macOS
open ui/hatching-ground.html

# Windows
start ui/hatching-ground.html

# Linux
xdg-open ui/hatching-ground.html
```

No server required. Works from `file://`.

## How to use it with Claude or GPT

1. Open `ui/hatching-ground.html` in a browser.
2. Select a workflow.
3. Fill in the context fields.
4. Click **Generate Prompt**.
5. Click **Copy Prompt** or **Download Prompt**.
6. Paste the prompt into Claude, GPT, or another assistant.
7. Copy the model's response.
8. Paste it into the **Model Output** area in the UI.
9. Click a **Validate** button for the relevant workflow.
10. Review any warnings.
11. Click **Download Output as Markdown** to save the artifact.

## How to export artifacts

Use the download controls at the bottom of the page. Each workflow has a recommended filename:

| Workflow | Recommended filename |
|---|---|
| Idea Card | `idea-card.md` |
| Clutch Score | `clutch-score.md` |
| Architecture Brief | `architecture-brief.md` |
| Full Architecture | `full-agent-architecture.md` |
| Codex Handoff | `codex-handoff.md` |
| Public/Private Checklist | `public-private-checklist.md` |

## Where private outputs should live

Save downloaded artifacts to an ignored local folder:

- `local/` (gitignored at repo root)
- `artifacts/private/` (gitignored)
- Any folder not tracked by git

Never save private outputs to a tracked folder. Never commit real personal data, private notes, credentials, employer information, or machine-specific paths.

## Why the harness is local-first

Keeping the harness local-first preserves the core Hatching Ground principle: the user is always in control, nothing leaves their machine without explicit action, and the system is inspectable at every step. Model API calls, cloud storage, and background agents are deferred until a proven use case justifies the additional complexity and trust surface.

## What should wait for v2

- Durable encrypted session storage.
- Controlled model API calls with user-managed keys.
- OpenClaw Gateway integration.
- Multi-session management.
- Server-side rendering or a lightweight backend.
- Automated artifact organization.

These are explicitly out of scope for the MVP. See `ui-harness/harness-contract.md` for the full boundary definition.
