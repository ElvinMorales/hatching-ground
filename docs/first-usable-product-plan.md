# First Usable Product Plan

## 1. Current State

Hatching Ground is an artifact-first documentation scaffold with prompts, workflows, templates, JSON Schemas, guardrails, evals, a self-contained static HTML fallback, a standard-library mock runtime adapter, and a local mock-connected web harness. The harness executes one deterministic synthetic `full_architecture` workflow through the adapter, renders its events/status/artifact, and resumes operational sessions from ignored storage. It has no external network, provider, database, or persistent browser-storage integration.

## 2. Why the Static UI Is a Prototype / Manual Fallback

The static UI proves the workflow and remains useful for testing, offline inspection, and fallback use. However, its prompt-copy/model-run/output-paste relay makes the user coordinate the system manually and prevents resumable sessions, a coherent transcript, and reliable progress reporting. It is therefore a prototype/manual fallback, not the target interaction.

The target product removes the normal-use copy/paste relay. Manual copy/paste remains available only as a transparent fallback.

## 3. Target First Usable Product

The first usable product is a local-first, session-based web harness in which one user can complete the Hatching Ground workflow in one local interface. It supports session creation and resume, workflow selection, context intake, a model run through a local runtime adapter or deterministic mock adapter, a transcript, progress and status updates, an artifact drawer, Markdown export, and local session persistence.

The first connected UI step is implemented for `full_architecture` in mock mode. The full multi-workflow incubation path, interactive approvals, deletion/recovery controls, provider mode, and hardening remain future work.

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

The harness owns presentation and local interaction: session create/resume, workflow selection, context forms, transcript rendering, event consumption, run-status display, the artifact drawer, privacy warnings, and Markdown export. Approval surfaces and provider configuration remain later work; there is no provider configuration UI in mock mode. Future approval requests must be visible objects and never silently approved.

## 6. Hatching Ground Runtime Responsibilities

The runtime owns workflow execution behind a narrow adapter: accepting a validated run request, invoking an adapter, emitting events and run status, returning typed artifacts, and reporting failures. The current implementation supports deterministic mock execution for `full_architecture`. Provider-specific credentials, transport, retries, and cost controls stay behind the future provider adapter and never enter exported artifacts or tracked session examples.

Provider SDKs, provider calls, and production backend frameworks are deferred. The implemented development server uses only Python's standard library and exposes a narrow loopback API.

## 7. Session Model

A session is the local operational container for one incubation effort. The implemented mock record has a stable ID, timestamps, selected workflow, synthetic context, run references, artifact references, and status, and may be resumed after restart. It is not durable memory. Explicit UI deletion, migrations, approvals, and private production storage remain later hardening work.

## 8. Event Model

The event stream is an ordered, append-oriented record of user-visible activity. Each event identifies its session and agent, has a timestamp and type, provides a concise human summary, carries a practical payload, declares risk, and references affected artifacts. Events drive the transcript, progress UI, approval surfaces, and diagnostic summaries; they are not raw provider logs or hidden memory. The baseline is `ui-harness/events.schema.json`.

## 9. Artifact Model

Artifacts are typed, inspectable outputs such as idea cards, clutch scores, architecture briefs, full architectures, Codex handoffs, and public/private checklists. Every artifact has an ID, source workflow, creation time, privacy classification, and export name. The artifact drawer lists artifacts by session and run, previews content, and exports selected content as Markdown. Artifacts do not become safe to commit merely because they were exported.

## 10. Local Storage and Privacy Model

The current mock harness stores sessions, generated requests, events, status, artifacts, and exports below ignored `local/harness/`. It writes nowhere else and reads runtime output only from expected run directories. The supported UI path is synthetic/public-safe only. It never treats transcripts as memory or state snapshots. Repository examples remain synthetic and public-safe.

A database, encryption scheme, sync, backup, multi-device storage, private-data support, and UI deletion controls are deferred until justified and threat-modeled.

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
3. **Local mock harness:** session create/resume, event transcript, status, artifact drawer, ignored file persistence, Markdown export, and JSON export against the deterministic mock adapter. Complete for synthetic `full_architecture`; approvals and broader workflows remain later.
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
