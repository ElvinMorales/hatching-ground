# Codex handoff: Garden Note Formatter

> Synthetic public-safe example. Do not treat this as real personal data, memory, state, or implementation output.

This is an example handoff artifact for a fictional project. It does not instruct Codex to modify Hatching Ground.

## Project name

Garden Note Formatter

## Goal

Implement a local/file-first tool that accepts one synthetic garden note and a date, produces a faithful checklist for review, and exports dated Markdown only after confirmation.

## Context

The fictional home gardener has messy notes that obscure next steps. The idea passed the hatch gate and has a reviewed architecture. The first product is one bounded transformation; tracked data remains synthetic and public-safe.

## Architecture summary

- One local workflow agent performs input, format, review, and export.
- The checklist contains only tasks supported by the source and flags ambiguity.
- Memory is not needed. Current input, draft, and validation result are temporary run state that can be cleared.
- External and consequential actions are unavailable.

## UI/harness summary

Use the smallest complete direct local interaction: a simple CLI or an existing dependency-free local harness. Keep intake, status, preview, confirmation, and export in one flow. If a direct harness is needed, avoid a normal-use copy/paste relay to another model; static relay is only a prototype/manual fallback.

## Assumptions

- Existing repository instructions and conventions take precedence.
- All committed fixtures are fictional.
- Deterministic local behavior can satisfy the first product without a provider.

## Files to create or modify

Inspect the repository first, then select only repository-native equivalents of:

- `README.md` — usage, privacy, and validation.
- Identity and operating-style artifacts — formatter role and faithful behavior.
- A formatting capability and direct interaction contract.
- A minimal local entry point for the chosen CLI or harness.
- A checklist output schema.
- Synthetic note and expected-checklist fixtures.
- JSONL eval cases and validation coverage.

Preserve useful existing files and do not replace working artifacts without evidence.

## Implementation steps

1. Inspect repository instructions, status, workflows, schemas, tests, ignore rules, and existing interface before editing.
2. Confirm the smallest repository-native file set and state assumptions that do not change safety or architecture.
3. Define the checklist contract and synthetic expected output.
4. Implement the note/date intake, faithful task extraction, ambiguity display, review, confirmation, and Markdown export path.
5. Limit writes to an explicit user-selected output and provide clear/reset for temporary state.
6. Add synthetic evals for exact extraction, ambiguity, empty input, diagnosis refusal, and prohibited integration scope.
7. Validate schemas and JSONL, run the synthetic end-to-end scenario, and inspect the diff and ignored files.

## Guardrails

- Use synthetic fixtures only; avoid secrets, private data, real logs, memory, durable state, and machine-specific paths.
- Never infer unsupported tasks or diagnose plant disease.
- Require human review before export and before any consequential action.
- Do not scan directories or request broad filesystem access.
- Do not add provider SDKs, model calls, backend services, databases, deployment, auth, scheduling, messaging, monitoring, purchases, device control, or multi-agent orchestration unless a later issue explicitly scopes and reviews them.

## Validation commands

Use the repository's exact documented commands after inspection. At minimum run its scaffold/schema validator, JSONL validation, focused tests, a synthetic end-to-end fixture, diff whitespace checks, and status/ignored-file checks. Record every exact command and result.

## Acceptance criteria

- One synthetic note and date produce one dated Markdown checklist.
- Each task is traceable to explicit source text; ambiguity is visible and unsupported advice is absent.
- The user reviews and confirms before export.
- No network, provider credential, backend, database, deployment, memory, or durable state is required.
- The supported direct local flow does not rely on normal-use prompt/output copy/paste.
- Schemas, JSONL, fixtures, tests, and privacy checks pass.
- Generated or private working files remain ignored and unstaged.

## What not to build yet

Weather monitoring, purchasing, reminders, scheduling, messaging, device control, plant disease diagnosis, provider execution, API-key handling, backend frameworks, databases, cloud deployment, authentication, persistent profiles, memory, durable state, broad filesystem access, or automatic commits.

## Final response requirements

Report files created and modified, implementation choices and assumptions, exact validation commands and outcomes, any skipped checks, ignored/generated-output status, and whether private data, secrets, machine-specific paths, dependencies, or prohibited runtime scope were added.
