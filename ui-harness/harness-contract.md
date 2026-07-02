# Hatching Ground UI Harness Contract

This contract distinguishes the current implemented page from the planned first usable local harness. The target section is an architecture boundary, not a claim of implementation.

## Layer 1: Current prototype/manual fallback contract

The static `ui/hatching-ground.html` page manages one ephemeral in-page interaction: workflow selection, user-entered context, generated prompt bundles, pasted model output, heuristic validation, and Markdown downloads.

It does not make model API calls, persist durable memory or session state, run background work, use a backend, have broad filesystem access, contact a network, integrate OpenClaw Gateway, or deploy to a VPS. The user manually transfers prompts and outputs. Closing or reloading the page discards its in-page data.

This layer remains supported for workflow testing and fallback use.

## Layer 2: Target first usable local harness contract

The planned local harness presents one end-to-end interface and removes the normal-use copy/paste relay. Its responsibilities are:

- **Sessions:** create, resume, list, export, and delete private local sessions with stable IDs.
- **Messages and transcript:** render user context, structured assistant summaries, approvals, and errors without exposing raw provider logs.
- **Context intake:** collect the minimum workflow inputs with privacy warnings and explicit review.
- **Event stream:** consume typed, user-visible events conforming to `events.schema.json`.
- **Run status:** show workflow step, progress, pending approval, artifacts, completion, cancellation, and bounded errors.
- **Artifact drawer:** list, preview, classify, and export typed Markdown artifacts.
- **Local session persistence:** retain resumable sessions in application-scoped local storage outside tracked repository paths, with deletion and migration behavior.
- **Mock mode:** execute deterministic, public-safe sample runs without network access, credentials, or private input.
- **Runtime adapter boundary:** send validated run requests to a narrow local adapter and receive events, status, approvals, and artifacts. Runtime implementation is deferred.
- **Provider configuration boundary:** offer explicit opt-in configuration while keeping credentials out of tracked files, sessions, transcripts, events, and exports. Provider implementation is deferred.

Approvals are UI-visible objects. The harness displays the requested action, reason, risk, data involved, choices, and safe default; it never treats silence as approval.

## Runtime boundary

The future Hatching Ground runtime, not the UI, executes workflows, invokes a mock or configured provider adapter, enforces workflow gates, emits typed events and status, and returns artifacts. Provider transport, retries, credentials, and usage controls remain behind that adapter.

This planning issue does not add the runtime adapter, backend, local server, provider calls, SDKs, database, model configuration, or persistent session files.

## Privacy and scope boundary

Local data is private by default and must remain in ignored, application-scoped storage. Events are structured activity records rather than raw logs, memory, or state snapshots. Memory and state remain distinct concepts. Consequential actions require human review.

OpenClaw integration, VPS deployment, cloud sync, full authentication, multi-agent orchestration, scheduling, messaging, monitoring, live memory/state, and broad filesystem or write-capable tool access are deferred until separately specified and reviewed.
