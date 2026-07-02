# Architecture brief: Garden Note Formatter

> Synthetic public-safe example. Do not treat this as real personal data, memory, state, or implementation output.

## Idea restatement

A fictional home gardener needs one unstructured synthetic note turned into a dated Markdown checklist whose tasks remain reviewable and traceable to the note.

## Recommended pattern

A single, local/file-first workflow agent. One bounded transformation keeps the behavior inspectable and requires no integration, autonomy, or persistent profile.

## First usable product scope

The first usable product accepts one pasted or typed synthetic note and a date, extracts only explicit actions, displays a reviewable checklist, and exports Markdown. It does not monitor weather, buy supplies, send reminders, control devices, diagnose plants, or scan folders.

## User workflow

1. The fictional user opens a local command or local harness.
2. They enter one synthetic note and choose a date.
3. The formatter produces a draft checklist and flags ambiguity instead of inventing work.
4. The user reviews the draft and explicitly exports it.

## Data sources

User-supplied synthetic text and a chosen date only. The first product does not read arbitrary files or external sources.

## Tool needs

Local text processing and writing one user-selected Markdown output. No network or provider tool is required.

## Privacy classification

Public-safe for this synthetic fixture. Any later real notes are private-only, must remain in ignored local locations, and must not appear in tracked examples, logs, memory, or state.

## Memory needs

None. The first usable product does not need cross-run preferences or learned facts.

## State needs

Temporary in-process input, draft, and validation result may exist for one run, then be cleared. No durable operational state is required.

## Likely artifacts

- Formatter instructions and local entry point.
- Checklist output contract.
- Synthetic input/output fixtures.
- Faithfulness and boundary eval cases.
- Local usage and privacy documentation.

## UI/harness note

A simple local command is sufficient if it supports input, review, and explicit export. A small direct local web harness is appropriate if review benefits from form fields and preview. Static prompt relay is only a prototype/manual fallback, not the repeated-use target when a harness is needed.

## Runtime note

Local execution is enough. The existing Hatching Ground mock runtime can demonstrate the artifact path but is not Garden Note Formatter. No provider call, backend, database, or cloud deployment is needed.

## Guardrails

Use synthetic fixtures, minimize file access, never invent tasks, flag uncertain source text, require review before export, and keep consequential or external actions unavailable.

## Deferred features

Weather monitoring, purchasing, reminders, messaging, scheduling, device control, plant disease diagnosis, provider execution, backend services, databases, cloud deployment, memory, durable state, and broad filesystem access.

## First-run scenario

Input: “On the sample plot, tie the fictional tomato stems and add mulch beside the labeled herb row.” Date: `2026-04-18` (fictional). Success: the output contains exactly those two tasks, identifies the date, adds no diagnosis or recommendation, and exports valid Markdown after review.

## Open questions

None that changes architecture or safety. The implementation issue may choose CLI or direct local harness while preserving the same workflow.

## Hatch recommendation

Proceed to full architecture. The hatch gate passed, scope is bounded, and human review is required before implementation.

## Next implementation handoff

After a human approves the full architecture, create a separate Codex task for the bounded local formatter and require synthetic fixture validation before any real use.
