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
