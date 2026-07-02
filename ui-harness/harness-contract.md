# Hatching Ground UI Harness Contract

This contract distinguishes the static fallback, the implemented mock-connected local harness, and later provider/hardening boundaries.

## Layer 1: Current prototype/manual fallback contract

The static `ui/hatching-ground.html` page manages one ephemeral in-page interaction: workflow selection, user-entered context, generated prompt bundles, pasted model output, heuristic validation, and Markdown downloads.

It does not make model API calls, persist durable memory or session state, run background work, use a backend, have broad filesystem access, contact a network, integrate OpenClaw Gateway, or deploy to a VPS. The user manually transfers prompts and outputs. Closing or reloading the page discards its in-page data.

This layer remains supported for workflow testing and fallback use.

## Layer 2: Implemented local mock harness contract

The local harness presents one end-to-end interface for the synthetic `full_architecture` mock workflow and removes the normal-use copy/paste relay for that flow. Its current responsibilities are:

- **Sessions:** create, resume, and list synthetic local operational sessions with stable IDs; export applies to run bundles, and UI deletion remains deferred.
- **Messages and transcript:** render user context, structured assistant summaries, approvals, and errors without exposing raw provider logs.
- **Context intake:** collect the minimum workflow inputs with privacy warnings and explicit review.
- **Event stream:** consume typed, user-visible events conforming to `events.schema.json`.
- **Run status:** show workflow step, progress, pending approval reference, artifacts, completion, and bounded errors. Cancellation remains deferred.
- **Artifact drawer:** list, preview, classify, and export typed Markdown artifacts.
- **Local session persistence:** retain resumable operational sessions below ignored `local/harness/`; manual deletion is documented, while UI deletion and migrations remain deferred.
- **Mock mode:** execute deterministic, public-safe sample runs without network access, credentials, or private input.
- **Runtime adapter boundary:** send schema-compatible run requests to the local mock adapter and receive events, status, and artifacts.
- **Provider configuration boundary:** provider configuration and implementation are deferred; the UI exposes no API-key or provider fields.

The mock workflow emits no consequential approval request. Future approvals must be UI-visible objects that expose action, reason, risk, data involved, choices, and safe default; silence is never approval.

## Runtime boundary

The Hatching Ground mock runtime, not the UI, executes the supported workflow, enforces its input boundary, emits typed events and status, and returns artifacts. Future provider transport, retries, credentials, and usage controls remain behind the adapter boundary.

The connected harness adds only a loopback Python standard-library server and ignored operational session files. It adds no provider calls, SDKs, database, model configuration, production platform, or tracked session output.

## Privacy and scope boundary

Local data is private by default and must remain in ignored, application-scoped storage. Events are structured activity records rather than raw logs, memory, or state snapshots. Memory and state remain distinct concepts. Consequential actions require human review.

OpenClaw integration, VPS deployment, cloud sync, full authentication, multi-agent orchestration, scheduling, messaging, monitoring, live memory/state, and broad filesystem or write-capable tool access are deferred until separately specified and reviewed.
