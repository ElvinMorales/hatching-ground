# UI Harness Taxonomy Notes

> Public-safe handoff note. This document summarizes Hatching Ground design lessons for a future taxonomy update. It does not modify the taxonomy repo and does not contain private data, memory, state, logs, or implementation output.

## 1. Purpose

This note captures lessons from the Hatching Ground UI harness for a future, separate update to `agentic-ai-artifact-taxonomy`. This repository is producing only a handoff note; this change does not update the taxonomy repo. All descriptions are public-safe, use synthetic framing, and refer only to versioned repository artifacts.

## 2. Core Lesson

A UI harness is an inspectable artifact bundle, not just frontend code. It defines and constrains how people supply context, assemble a prompt or request, validate results, review work, resume a session, and reach approval checkpoints. It also determines what runtime and tool activity is visible, how state can be inspected, how artifacts are handled, and what export or save behavior is available.

When memory exists, the harness may also provide memory review without making temporary UI or session state into durable memory. Together, these surfaces express safety boundaries and influence how an agent is used and evaluated. They should therefore be reviewable alongside prompts, schemas, guardrails, evals, and runtime contracts.

## 3. UI Harness as Artifact Bundle

A harness can combine several artifact types:

- an interface contract;
- session, artifact, event stream, run status, approval, and agent profile schemas;
- a frontend shell and local server;
- a runtime adapter boundary;
- a static prototype or manual fallback;
- a mock event stream and deterministic mock runner;
- an export contract;
- validation and smoke tests; and
- usage, setup, and maintenance documentation.

Each item is inspectable and versioned. Together they constrain accepted inputs, observable progress, human review, output structure, and failure behavior. Treating only the frontend shell as the harness would hide the contracts that make its workflow understandable and testable.

## 4. Static Prompt Bridge vs Local Web Harness vs Runtime

### Static prompt bridge

A static prompt bridge is a useful prototype and manual fallback. It can validate layout, prompt structure, artifact export, and assumptions about the user workflow. It is not the target product when normal use requires repeated copy/paste relay between tools.

### Local web harness

A local web harness provides one local interface for context intake, progress, approvals, artifacts, and export. It may remain mock-first. It can be the first usable product when it completes the workflow without a normal-use copy/paste relay, even if provider integrations remain deferred.

### Runtime

The runtime executes the workflow through deterministic or mock adapters and, only in later explicit scope, provider or tool calls. Its execution concerns should remain separated from the UI contract. Provider mode, real tool integrations, and consequential actions require explicit scope and human review rather than being implied by the presence of an interface.

## 5. Mapping to Taxonomy Buckets

| Taxonomy bucket | Harness contribution | Hatching Ground examples | Taxonomy clarification to consider |
| --- | --- | --- | --- |
| Prompts and interfaces | Defines context intake, interaction flow, prompt assembly, and the manual or connected interface contract. | `ui/hatching-ground.html`, `ui/local-harness/index.html`, `ui-harness/harness-contract.md` | Interfaces can be first-class artifacts rather than only wrappers around prompts. |
| State | Defines inspectable session continuity, run status, event progression, and the boundary between temporary state and durable memory. | `ui-harness/session.schema.json`, `ui-harness/run-status.schema.json`, `ui-harness/events.schema.json` | Temporary UI and session state should not be classified automatically as memory. |
| Outputs and schemas | Defines artifact metadata, Markdown handling, manifests, previews, downloads, and export behavior. | `ui-harness/artifact.schema.json`, `ui/local-harness/app.js`, `runtime/schemas/runtime-result.schema.json` | Artifact handling and export contracts belong with output definitions, not only UI implementation. |
| Guardrails and governance | Makes approval checkpoints, privacy boundaries, runtime modes, and review expectations visible. | `ui-harness/approval.schema.json`, `ui-harness/harness-contract.md`, `runtime/provider-adapter-boundary.md` | Approval surfaces are governance artifacts and should identify which actions require human review. |
| Evaluation and observability | Exposes events, progress, status, and artifacts that validators and smoke tests can inspect. | `ui-harness/examples/sanitized-event-stream.jsonl`, `scripts/smoke_test_local_harness.py`, `scripts/validate_scaffold.py` | Harness observability should cover human-readable timelines and machine-checkable contracts. |
| Runtime and deployment | Separates the local interface from execution adapters and records the boundary around deferred provider mode. | `scripts/serve_local_harness.py`, `runtime/mock-runner.md`, `runtime/provider-adapter-boundary.md` | A local harness, runtime adapter, and deployed application are distinct artifact and maturity levels. |

The bundle also relates to other taxonomy areas. **Tools** are surfaced through runtime visibility and future permission boundaries. **Memory** is relevant when a harness supports review of durable memory, but is distinct from temporary session state. **Planning and orchestration** appears in progress events, workflow selection, and approval sequencing. **Learning and iteration** is supported when validation findings and synthetic failures lead to versioned contract improvements rather than hidden behavior changes.

## 6. Hatching Ground Artifact Examples

- `ui/hatching-ground.html` is the dependency-free static prompt bridge and manual fallback.
- `ui/local-harness/index.html` and `ui/local-harness/app.js` provide the connected local interface and client-side workflow behavior.
- `ui/local-harness/README.md` and `docs/local-web-harness.md` document setup, use, limitations, and deferred provider scope.
- `ui-harness/harness-contract.md` states the interface contract and scope boundaries.
- `ui-harness/events.schema.json`, `ui-harness/run-status.schema.json`, `ui-harness/approval.schema.json`, and `ui-harness/agent-profile.schema.json` make events, status, approvals, and agent presentation inspectable.
- `ui-harness/examples/sanitized-event-stream.jsonl` is a synthetic, public-safe observability fixture.
- `runtime/provider-adapter-boundary.md` separates mock execution from any later provider integration.
- `runtime/mock-runner.md` documents deterministic local execution and its outputs.
- `scripts/serve_local_harness.py` connects the local interface to the mock-first workflow without external dependencies.
- `scripts/smoke_test_local_harness.py` checks the local server, API surface, session flow, run flow, and artifact retrieval.

These files have different formats and responsibilities, but together they define the usable and reviewable harness.

## 7. What This Suggests for the Taxonomy Repo

A future taxonomy issue or pull request could propose the following changes without copying Hatching Ground implementation details:

1. Clarify that **Prompts and interfaces** includes UI and harness contracts, context-intake shapes, and interaction surfaces.
2. Explain that a UI harness can span interface, state, outputs, guardrails, evaluation, observability, and runtime boundaries.
3. Add examples that distinguish a static prototype, local harness, runtime adapter, and deployed application.
4. Add artifact handling under outputs and approval checkpoint examples under guardrails.
5. Clarify that temporary UI or session state differs from durable memory.
6. Note that a harness may be necessary for a first usable product even when agent logic is simple.
7. Define a copy/paste prompt bridge as an acceptable prototype or manual fallback, not necessarily a complete normal-use workflow.

These are proposals for later review in the taxonomy repo. They are not taxonomy changes made by this repository.

## 8. What Should Remain Deferred

Hatching Ground intentionally deferred model provider APIs, persistence beyond ignored local files, OpenClaw, VPS or cloud deployment, backend and database services, authentication and multi-user support, production monitoring, email/Slack/calendar integrations, and autonomous actions.

Those deferrals kept the first usable product small while preserving its core path: collect context, execute a mock-first workflow, inspect progress, review artifacts, and export a result. Adding an interface did not grant permission to expand the runtime or integration boundary.

## 9. Public/Private Boundary

Tracked documentation and examples must remain public-safe. Local generated runs remain ignored. Real personal content, raw logs, memory, state, secrets, employer data, and machine-specific paths stay out of the repository. Any future taxonomy example should use synthetic fixtures only. Consequential actions continue to require human review.

## 10. Follow-Up Proposal Packet

## Proposed taxonomy update packet

### Proposed change

Recognize a UI harness as an inspectable artifact bundle spanning interface contracts, state, outputs, guardrails, observability, and runtime boundaries.

### Rationale from Hatching Ground

The first usable local workflow depended on versioned contracts, schemas, mock execution, validation, and documentation in addition to frontend files. Those artifacts shaped use and review as directly as the prompt did.

### Candidate taxonomy buckets affected

Prompts and interfaces; State; Outputs and schemas; Guardrails and governance; Evaluation and observability; Runtime and deployment. Related examples may reference Tools, Memory, Planning and orchestration, and Learning and iteration.

### Example language to add

“A UI harness may be a first-class artifact bundle that defines context intake, interaction, state visibility, approvals, artifact handling, and runtime boundaries. Classify its component contracts in the relevant buckets rather than treating the harness only as frontend code.”

### Non-goals

Do not prescribe a frontend framework, require deployment, merge temporary state with memory, or imply provider and tool permissions.

### Validation questions

- Can a reviewer identify the interface, state, output, approval, observability, and runtime contracts?
- Is a static prototype distinguished from a complete local workflow and from its runtime?
- Are synthetic examples, privacy boundaries, deferred integrations, and human approval explicit?
