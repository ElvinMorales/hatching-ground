# Hatching Ground UI Harness Contract

This document defines the responsibilities and explicit limits of the Hatching Ground UI harness MVP.

## What the harness manages

The MVP harness is responsible for:

- **Sessions** — holding the current workflow, context fields, rough idea, and clutch input in page memory for the duration of a single browser session.
- **Selected workflow** — surfacing the correct context fields and prompt template for the chosen workflow.
- **User-provided context** — collecting project area, goal, friction, constraints, privacy notes, and build style.
- **Generated prompt bundle** — assembling a paste-ready prompt from the workflow template and user context.
- **Pasted model output** — accepting model output that the user copies back from Claude or GPT.
- **Validation results** — running heuristic checks against pasted output and reporting warnings.
- **Exported artifacts** — packaging validated output as a downloadable Markdown file with a recommended filename.

## What the harness does not manage

The MVP harness explicitly does **not** manage:

- **Model API calls** — no calls to Claude, GPT, or any model API. The user copies the prompt and pastes the output manually.
- **Background runs** — no scheduled tasks, queued jobs, or background agents.
- **Autonomous actions** — no actions taken without explicit user initiation.
- **Durable memory** — no localStorage, sessionStorage, cookies, IndexedDB, or file writes. State is lost when the tab closes.
- **Live state** — no polling, no WebSockets, no server-sent events.
- **Cloud storage** — no cloud file systems, databases, or object stores.
- **OpenClaw Gateway** — not integrated in this MVP.
- **VPS deployment** — not deployed anywhere; runs from `file://` only.
- **Broad filesystem access** — reads nothing from disk except the HTML file itself.

## Upgrade path

A future harness version (v2+) may add:

- Encrypted local session persistence via a local server or OPFS.
- Controlled model API calls with explicit user-managed keys.
- OpenClaw Gateway integration for authenticated, logged model calls.
- Multi-session management.

None of these may be added without an explicit scoped change request. The boundary in this contract must be updated before scope expands.
