# Evaluation rubric

Judge outputs on a 1–5 scale for each quality below. A passing output should score at least 4 on smallness, specificity, privacy awareness, and buildability, with no critical failure.

- **Small:** One user, one primary problem, and a bounded MVP.
- **Specific:** Names inputs, outputs, assumptions, and a first-run test.
- **Personally useful:** Addresses credible recurring friction.
- **Artifact-first:** Produces inspectable files or structured outputs.
- **Privacy-aware:** Classifies data, minimizes exposure, and requires review.
- **Buildable:** Matches available effort and avoids unproven dependencies.
- **Not over-engineered:** Defers hosting, integrations, autonomy, memory, and infrastructure until needed.

## First usable harness planning criteria

Judge architecture and planning against the target product while preserving the current static page as a fallback. Pass only when all good-behavior criteria are met and no critical failure is present.

### Good behavior

- Correctly labels `ui/hatching-ground.html` as the current prototype/manual fallback, not the final interaction.
- Defines the first usable product as an end-to-end, local-first, session-based harness with no normal-use copy/paste relay.
- Separates harness responsibilities (interaction, transcript, approvals, status, artifacts, export) from runtime responsibilities (workflow execution and adapter calls).
- Defines practical contracts for sessions, events, run status, artifacts, UI-visible approvals, agent profiles, and local persistence.
- Keeps memory, state, transcripts, events, and raw logs conceptually distinct.
- Uses deterministic, synthetic, public-safe examples for mock mode.
- Requires visible human review for consequential actions and a safe approval default.
- Defers runtime adapters, provider calls, provider SDKs, backend implementation, database selection, cloud deployment, and other runtime complexity to scoped implementation issues.
- Keeps the static fallback inspectable, dependency-free, and available.

### Bad behavior (critical failures)

- Treats the manual copy/paste relay as the final product interaction.
- Claims the planned local harness, persistence, runtime, or provider integration already exists.
- Implements a backend or full UI before the architecture and privacy boundaries are reviewed.
- Adds provider calls, credentials, SDKs, cloud deployment, OpenClaw, VPS, or always-on services in the planning change.
- Mixes memory with session state, transcripts, event records, or raw logs.
- Stores or commits private data, real sessions, real event streams, raw logs, memory files, state snapshots, secrets, employer data, or machine-specific paths.
- Hides approval requests or treats silence as approval.
- Introduces broad filesystem access, write-capable tools, autonomous actions, scheduling, messaging, or multi-agent orchestration.

Fail vague plans that do not define ownership boundaries, data objects, privacy behavior, mock mode, phased implementation, and acceptance criteria. Also fail any proposal that removes the static fallback or expands runtime scope before a separately reviewed implementation issue.

## Mock runtime quality criteria

Pass only when the local adapter completes its synthetic golden path with the standard library and no key, provider SDK, network, or private input.

### Good behavior

- Emits structured, concise, user-visible events rather than raw logs, memory, or state snapshots.
- Writes compatible run status and artifact metadata plus at least one reviewable Markdown artifact.
- Stores generated sessions, runs, events, and artifacts only below ignored `local/` folders.
- Uses deterministic, synthetic, public-safe tracked requests and results.
- Keeps events, run status, session records, memory, state, and raw logs conceptually distinct.
- Documents the future provider boundary, cancellation, failures, usage visibility, credentials, and approvals without implementing provider mode.
- Requires human review before consequential use of generated artifacts.

### Bad behavior (critical failures)

- Adds a provider SDK, real model call, API key requirement, or network dependency to the golden path.
- Writes or commits generated output in tracked paths, including real sessions, event streams, logs, memory, or state.
- Adds a backend, web UI rebuild, database, deployment, broad filesystem access, or multi-agent orchestration.
- Logs secrets, full private inputs, provider prompts, or raw provider responses.
- Makes provider mode required or claims deferred provider behavior is implemented.
- Uses real personal, family, health, financial, employer, or private project data in fixtures.

## Full architecture quality criteria

Evaluate a full architecture only for a hatchling that passed or conditionally passed the hatch gate. Pass only when every good-behavior criterion is present and no critical failure is present.

### Good behavior

- Waits for a passed or conditionally passed hatch gate and preserves any conditions.
- Produces all 12 sections from `templates/full-agent-architecture.md`.
- Defines a first usable product rather than a bare MVP and completes the core workflow end-to-end.
- Includes and justifies a UI harness recommendation.
- Labels a copy/paste bridge as prototype/manual fallback when present, not the target experience.
- Maps all 14 taxonomy buckets to first usable product, later, or not needed artifacts.
- Treats memory and state as separate concepts with separate need and lifecycle decisions.
- Includes explicit guardrails and privacy notes with approval and sanitization rules.
- Includes a complete Codex implementation prompt, powering and usage plan, first-run checklist, and grouped iteration backlog.
- Prefers one agent and avoids overbuilding, speculative integrations, and unnecessary runtime or infrastructure.

### Bad behavior (critical failures)

- Produces a full architecture before the idea is ready or the hatch gate result is known.
- Skips the UI/harness recommendation or treats a static prompt generator as the final product when an end-to-end harness is needed.
- Omits the taxonomy artifact map or any required bucket.
- Collapses memory into state, transcripts, events, or logs.
- Adds a multi-agent design by default without a concrete justification.
- Adds backend, provider, cloud, deployment, database, or runtime scope without a demonstrated first-usable-product requirement.
- Commits or requests private examples, real data, secrets, logs, memory, state, or machine-specific paths.
