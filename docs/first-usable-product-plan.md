# First Usable Product Plan

## 1. Current State

Hatching Ground is an artifact-first documentation scaffold with prompts, workflows, templates, JSON Schemas, guardrails, evals, a self-contained static HTML interface, and a standard-library mock runtime adapter. The adapter executes one deterministic synthetic `full_architecture` workflow through a local command boundary and writes contracts to ignored storage. The static page remains a manual fallback and is not connected to the adapter. Neither component has backend, network, provider, or persistent browser integration.

## 2. Why the Static UI Is a Prototype / Manual Fallback

The static UI proves the workflow and remains useful for testing, offline inspection, and fallback use. However, its prompt-copy/model-run/output-paste relay makes the user coordinate the system manually and prevents resumable sessions, a coherent transcript, and reliable progress reporting. It is therefore a prototype/manual fallback, not the target interaction.

The target product removes the normal-use copy/paste relay. Manual copy/paste remains available only as a transparent fallback.

## 3. Target First Usable Product

The first usable product is a local-first, session-based web harness in which one user can complete the Hatching Ground workflow in one local interface. It supports session creation and resume, workflow selection, context intake, a model run through a local runtime adapter or deterministic mock adapter, a transcript, progress and status updates, an artifact drawer, Markdown export, and local session persistence.

This document defines the target architecture. Only the mock command boundary and local output records are implemented; session resume, the connected web UI, and provider mode remain future work.

## 4. Core User Workflow

1. Create or resume a local session.
2. Select a workflow and enter minimal, privacy-reviewed context.
3. Turn a rough idea into an idea card.
4. Score a clutch of candidates and apply the hatch gate.
5. Produce a pre-architecture brief only after the gate passes or conditionally passes.
6. Produce a full architecture artifact using `workflows/full-architecture.md` after human review.
7. Produce a reviewed Codex handoff from that architecture.
8. Inspect the transcript, progress, status, and artifact drawer.
9. Export selected artifacts as Markdown.

Normal use stays inside the harness from rough idea through export. Consequential actions and sensitive-data disclosures always require explicit human review.

## 5. Harness Responsibilities

The harness owns presentation and local interaction: session create/resume, workflow selection, context forms, transcript rendering, event consumption, run-status display, approval surfaces, the artifact drawer, privacy warnings, provider-configuration UI, and Markdown export. It presents approval requests as visible objects and never silently approves them.

## 6. Hatching Ground Runtime Responsibilities

The runtime owns workflow execution behind a narrow adapter: accepting a validated run request, invoking an adapter, emitting events and run status, returning typed artifacts, and reporting failures. The current implementation supports deterministic mock execution for `full_architecture`. Provider-specific credentials, transport, retries, and cost controls stay behind the future provider adapter and never enter exported artifacts or tracked session examples.

Provider SDKs, a backend server, and provider calls are deferred to later implementation issues.

## 7. Session Model

A session is the durable local container for one incubation effort. It has a stable ID, timestamps, selected workflow, privacy-reviewed context, transcript references, run references, events, approvals, and artifact references. A session may be resumed after restart. Session data is private by default and must support explicit deletion and export. The existing `session.schema.json` is a baseline and will need a versioned migration before implementation.

## 8. Event Model

The event stream is an ordered, append-oriented record of user-visible activity. Each event identifies its session and agent, has a timestamp and type, provides a concise human summary, carries a practical payload, declares risk, and references affected artifacts. Events drive the transcript, progress UI, approval surfaces, and diagnostic summaries; they are not raw provider logs or hidden memory. The baseline is `ui-harness/events.schema.json`.

## 9. Artifact Model

Artifacts are typed, inspectable outputs such as idea cards, clutch scores, architecture briefs, full architectures, Codex handoffs, and public/private checklists. Every artifact has an ID, source workflow, creation time, privacy classification, and export name. The artifact drawer lists artifacts by session and run, previews content, and exports selected content as Markdown. Artifacts do not become safe to commit merely because they were exported.

## 10. Local Storage and Privacy Model

Sessions, events, approvals, status, and artifacts are stored locally in an implementation-defined application data directory, not in tracked repository paths. Data is private by default, scoped to the application, and unavailable to network services unless a user explicitly configures and runs a provider. The implementation must provide deletion, avoid broad filesystem access, redact secrets from user-visible records, and never treat transcripts as memory or state snapshots. Repository examples remain synthetic and public-safe.

An implementation issue must choose and threat-model the local storage mechanism. A database, encryption scheme, sync, backup, and multi-device storage are deferred until justified.

## 11. Mock Mode

Mock mode is the default development and acceptance-test path. A deterministic local adapter consumes synthetic context and emits a fixed sequence of realistic events, status changes, an optional approval, and public-safe Markdown artifacts. It requires no key, network, provider SDK, or private input. `ui-harness/examples/sanitized-event-stream.jsonl` illustrates the event shape, not a real session.

## 12. Real Provider Mode

Real provider mode is a later opt-in capability behind the same runtime adapter contract. The user explicitly chooses and configures a provider locally. Credentials remain outside repository artifacts, transcripts, events, and exports. The adapter must expose cancellation, bounded errors, cost/usage visibility where available, and approval boundaries. Normal use does not require manually relaying prompts or outputs.

## 13. Deferred Capabilities

- Provider adapter implementation
- Provider SDK selection and model calls
- Database selection or cloud synchronization
- Full authentication and multi-user access
- OpenClaw Gateway and VPS deployment
- Multi-agent orchestration, scheduling, and messaging
- Memory proposal inbox, live memory, and state snapshots
- Monitoring and always-on services
- Broad filesystem or write-capable tool access

## 14. Implementation Phases

1. **Architecture contract:** version the schemas, event vocabulary, privacy boundaries, mock fixtures, and acceptance tests. Complete for the initial contracts.
2. **Mock runtime adapter:** implement the narrow local command boundary, ignored output records, structured events/status, and Markdown export. Complete for one synthetic `full_architecture` workflow.
3. **Local mock harness:** build session create/resume, transcript, status, approvals, artifact drawer, persistence, and Markdown export against the deterministic mock adapter.
4. **Opt-in provider adapter:** add one provider only after credential handling, privacy review, usage visibility, and failure behavior are specified and tested.
5. **Hardening:** test migration, deletion, recovery, accessibility, and safe fallback to the static page.

Each phase should remain independently reviewable and preserve the static page as a manual fallback.

## 15. Acceptance Criteria

The first usable product is accepted when:

- One local interface supports rough idea -> idea card -> clutch score -> hatch gate -> architecture brief -> full architecture -> Codex handoff -> Markdown export.
- A user can create, close, resume, and delete a local session.
- Normal use has no prompt/output copy/paste relay.
- The transcript, current step, progress, errors, approvals, and artifacts are visible and consistent with emitted events.
- Mock mode completes a synthetic end-to-end run without network access or secrets.
- Provider mode, when implemented, is explicit and isolated behind the runtime adapter.
- Consequential actions require visible human approval and have a safe default.
- Private runtime data stays in ignored local storage; tracked fixtures are synthetic and public-safe.
- No cloud deployment, multi-agent orchestration, live memory/state, or broad filesystem access is required.
- The static HTML page still works and is documented as the prototype/manual fallback.
