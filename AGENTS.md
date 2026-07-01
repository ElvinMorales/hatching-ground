# Instructions for coding agents

Preserve this repository's artifact-first structure: behavior and decisions should remain visible in versioned Markdown, templates, schemas, and evals.

## Required behavior

- Keep changes small, inspectable, local-first, and compatible with the documented workflows.
- Use synthetic examples only.
- State assumptions when missing information does not materially change a recommendation.
- Ask questions only when an answer materially changes architecture, safety, or the recommendation.
- Validate schemas and JSONL after relevant changes.
- Require human review for consequential actions.

## Prohibited content

Do not add real personal or family data, health or financial data, employer data, secrets, tokens, machine-specific paths, raw logs, private memory, or private state. Do not copy content from ignored working folders into tracked examples.

## Scope boundary

Do not add runtime integrations, broad filesystem access, write-capable tools, a database, API server, VPS deployment, OpenClaw Gateway, multi-agent orchestration, live memory/state, monitoring, messaging, or automated commits unless explicitly requested in a later scoped change.

**Allowed in this MVP:** A self-contained static HTML UI harness (`ui/hatching-ground.html`) with no external dependencies, no network calls, no persistent browser storage, no model API calls, and no backend. This harness assembles prompts, accepts pasted model output, validates heuristically, and exports Markdown artifacts. It does not extend permitted scope beyond these constraints.

The following remain prohibited even with the UI harness present: model API keys or calls, backend servers, databases, OpenClaw Gateway, VPS deployment, always-on services, broad filesystem access, real private data in tracked files, secrets, employer data, and machine-specific paths.
