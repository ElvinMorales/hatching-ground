# UI Harness Artifacts

This directory contains the versioned contracts for the current static prototype/manual fallback and the planned first usable local harness. The target architecture is described in [the first usable product plan](../docs/first-usable-product-plan.md); it is not implemented yet. See [the harness contract](harness-contract.md) for the two-layer boundary.

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

These schemas are practical planning baselines, not frozen runtime protocols.

## Target interaction

The planned local harness will support resumable sessions, context intake, a transcript, an event stream, run status, approvals, an artifact drawer, local private persistence, deterministic mock mode, and an adapter boundary for later provider use. Normal use will not require copying prompts and outputs between interfaces.

## Privacy

Tracked examples are synthetic and public-safe. Real sessions, transcripts, events, approvals, artifacts, memory, state, logs, credentials, and provider configuration must remain outside version control in ignored local storage. Export does not imply that an artifact is safe to commit.
