# UI Harness Artifacts

This directory contains versioned contracts shared by the static prototype/manual fallback and the mock-connected local harness. The implemented frontend lives in `../ui/local-harness/`; the broader target architecture is described in [the first usable product plan](../docs/first-usable-product-plan.md). See [the harness contract](harness-contract.md) for the layers and remaining boundaries.

## Current interface

`../ui/hatching-ground.html` remains the implemented static page. It runs from `file://`, creates paste-ready prompts, accepts manually pasted model output, validates heuristically, and downloads Markdown. It uses no backend, persistence, network calls, model APIs, or external dependencies.

## Expanded artifact set

- `session.schema.json`: baseline session context and artifact references. A future implementation must version its persistence model.
- `artifact.schema.json`: typed, privacy-classified exported outputs.
- `workflow.schema.json`: supported workflow definitions, inputs, outputs, and checks.
- `events.schema.json`: user-visible activity events that drive transcript and progress views.
- `run-status.schema.json`: current status, step, progress, approval, artifact, and error references.
- `approval.schema.json`: visible human-review requests, choices, safe defaults, and decisions.
- `agent-profile.schema.json`: harness-visible capabilities, workflows, permissions, runtime mode, memory behavior, and state behavior.
- `examples/synthetic-session.json`: existing synthetic example for the static/manual workflow.
- `examples/sanitized-event-stream.jsonl`: public-safe mock event sequence for the planned harness.

These schemas are practical contract baselines, not frozen runtime protocols. The local harness consumes the compatible event, run-status, and artifact records emitted by the mock adapter; its simple operational session record is documented separately.

## Implemented mock interaction

The local harness supports resumable operational sessions, synthetic context intake, an event timeline, run status, an artifact drawer, ignored local persistence, deterministic mock execution, and Markdown/JSON export for `full_architecture`. Normal use of this supported workflow does not require copying prompts and outputs between interfaces. Approvals, private production support, additional workflows, and providers remain deferred.

## Privacy

Tracked examples are synthetic and public-safe. Real sessions, transcripts, events, approvals, artifacts, memory, state, logs, credentials, and provider configuration must remain outside version control in ignored local storage. Export does not imply that an artifact is safe to commit.
