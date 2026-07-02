# UI Harness

## Current static prototype/manual bridge

`ui/hatching-ground.html` is the currently implemented interface. It is a self-contained `file://` page that assembles prompts, accepts pasted model output, validates output heuristically, and exports Markdown. It has no backend, persistence, network calls, external dependencies, model API calls, or broad filesystem access.

The page is useful for testing the artifact workflow and as a transparent manual fallback. Because the user must relay prompts and model output, it is not the target first usable product.

## Target local web harness

The planned first usable product is a local-first, session-based web harness. In one local interface, a user should be able to create or resume a session, select a workflow, provide privacy-reviewed context, run through a mock or local runtime adapter, inspect the transcript and status, resolve visible approvals, manage generated artifacts, and export Markdown.

Normal use will not require copying a prompt to another interface and pasting output back. The architecture and phased boundaries are defined in [the first usable product plan](first-usable-product-plan.md). These capabilities are planned, not currently implemented.

## What changes in the first usable product

- Durable local session creation, resume, and deletion
- Workflow and context intake inside a session
- Mock-adapter and runtime-adapter execution boundary
- User-visible transcript and structured event stream
- Current run status, progress, errors, and cancellation
- Visible approval objects with safe defaults
- Artifact drawer with previews and Markdown export
- Local private persistence outside tracked repository paths
- Provider configuration isolated behind a future adapter boundary

The harness owns presentation, local interaction, and export. The future runtime owns workflow execution and structured event/status emission. Neither layer silently approves consequential actions.

## What stays deferred

- Runtime adapter and provider implementation
- Provider SDKs and model calls
- Database choice, cloud sync, and multi-device storage
- OpenClaw Gateway and VPS deployment
- Multi-agent orchestration, scheduling, messaging, and monitoring
- Full authentication or multi-user access
- Live memory, memory proposal inboxes, and state snapshots
- Broad filesystem access and write-capable tools

## Manual fallback instructions

Use the current page when testing workflows or when the future local harness is unavailable:

1. Open `ui/hatching-ground.html` directly in a browser.
2. Select a workflow and enter only public-safe or appropriately local context.
3. Generate and copy the prompt.
4. Paste it into the model interface you chose.
5. Paste the model response into the page.
6. Run the relevant heuristic validation and review warnings.
7. Download the Markdown artifact.

The fallback page does not send or retain content automatically. Opening it requires no server.

## Artifact export and privacy

Recommended exports include `idea-card.md`, `clutch-score.md`, `architecture-brief.md`, `full-agent-architecture.md`, `codex-handoff.md`, and `public-private-checklist.md`.

Save private outputs in an ignored `local/` or `artifacts/private/` directory. Never commit real personal, health, financial, employer, credential, memory, state, transcript, or event-stream data. Tracked examples must stay synthetic and public-safe.
