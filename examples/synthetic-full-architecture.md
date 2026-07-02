# Agent Architecture: Garden Note Formatter

> Synthetic public-safe example. Do not treat this as real personal data, memory, state, or implementation output.

## 1. Idea Restatement

Garden Note Formatter serves a fictional home gardener whose unstructured notes obscure next steps. It turns one synthetic note and selected date into one reviewable Markdown checklist without inventing tasks. The hatch gate passed after a 31/35 score. This architecture does not authorize implementation and requires human review.

Non-goals are weather monitoring, purchasing, reminders, messaging, device control, plant disease diagnosis, broad filesystem access, provider calls, backend services, databases, cloud deployment, and autonomous decisions.

## 2. Recommended Pattern

Use one local/file-first workflow agent. A deterministic local transformation boundary, explicit review, and artifact output fit the single input-to-output loop. Multi-agent orchestration would add coordination without improving the result.

## 3. First Usable Product Scope

The user enters one synthetic note and date in a local command or direct local harness, requests formatting, reviews tasks and ambiguity flags, and explicitly exports a dated Markdown checklist. The product must preserve source meaning, omit unsupported work, and finish the workflow end to end.

No provider call is required for this synthetic example. No backend, database, cloud deployment, memory, or persistent profile is needed. A static prompt relay may support prototyping, but it is a **prototype/manual fallback**, not the target if repeated use needs a harness.

## 4. Taxonomy Artifact Map

| Bucket | First Usable Product / Later / Not Needed | Artifact | Notes |
| --- | --- | --- | --- |
| Identity | First Usable Product | `agent/identity.md` | Defines a narrow checklist formatter, not an adviser or operator. |
| Operating style | First Usable Product | `agent/operating-style.md` | Requires faithful extraction, explicit uncertainty, and concise output. |
| Capability modules | First Usable Product | `capabilities/format-note.md` | One parse, draft, review, and export capability. |
| Tools | First Usable Product | `tools/local-output-boundary.md` | Accepts direct input and writes only a user-selected output; no broad file access. |
| Knowledge and resources | Not Needed | None | No reference corpus, weather feed, or horticultural knowledge is required. |
| Prompts and interfaces | First Usable Product | `interfaces/checklist-workflow.md` | Defines note/date intake, preview, review, and export. |
| Memory | Not Needed | None | Cross-run facts and preferences provide no first-product value; nothing is retained or proposed. |
| State | First Usable Product | In-process run object only | Temporary note, draft, and validation result are inspectable during the run and cleared on exit; no durable state. |
| Planning and orchestration | Not Needed | None | A fixed single-agent sequence needs no planner or orchestration layer. |
| Guardrails and governance | First Usable Product | `guardrails/privacy-and-faithfulness.md` | Synthetic fixtures, no invention, no diagnosis, explicit review, minimal file access. |
| Outputs and schemas | First Usable Product | `schemas/checklist-output.schema.json` | Defines date, source summary, tasks, ambiguity notes, and Markdown rendering. |
| Evaluation and observability | First Usable Product | `evals/cases.jsonl` | Synthetic fidelity, ambiguity, empty-input, and prohibited-scope cases; no raw logs. |
| Runtime and deployment | First Usable Product | `README.md` local usage section | Local command or dependency-free local harness only; no service or deployment. |
| Learning and iteration | Later | `docs/iteration.md` | Human-reviewed issues from demonstrated gaps; no automatic learning. |

## 5. Proposed Repo Structure

```text
garden-note-formatter/
├── README.md
├── agent/
│   ├── identity.md
│   └── operating-style.md
├── capabilities/
│   └── format-note.md
├── interfaces/
│   └── checklist-workflow.md
├── tools/
│   └── local-output-boundary.md
├── guardrails/
│   └── privacy-and-faithfulness.md
├── schemas/
│   └── checklist-output.schema.json
├── evals/
│   └── cases.jsonl
├── examples/
│   ├── synthetic-note.txt
│   └── synthetic-checklist.md
└── docs/
    └── iteration.md
```

An implementation should omit any path not needed by the chosen local interface. Generated output and any real input belong in an ignored local folder.

## 6. UI Harness Recommendation

A CLI is sufficient when it can collect the note and date, show a preview, accept confirmation, and export directly. A small dependency-free local web harness is preferable if the user needs a form and side-by-side Markdown preview. ChatGPT, Claude, or Codex can demonstrate the prompt as a manual fallback, but repeated use must not require a copy/paste relay. An existing self-hosted UI or gateway-backed harness is unjustified.

The interface shows note input, selected date, formatting status, ambiguity warnings, checklist preview, and an explicit export action. Temporary session state contains only the current input, draft, and validation result. Visible events are limited to input accepted, draft ready, review required, and export complete. Export requires human confirmation. The artifact drawer, if a web harness is chosen, contains only the draft and exported Markdown checklist. There are no memory controls because memory is absent; a clear/reset control removes temporary state.

## 7. Key Design Decisions

- A single agent matches the fixed sequence and minimizes coordination and risk.
- Memory is not needed for the first usable product because each note is self-contained.
- Temporary run state may exist only long enough to review and export, then is cleared.
- The local interface owns review and explicit export; it does not automate external actions.
- No provider calls are required for the synthetic example; deterministic behavior is preferable.
- Integrations and infrastructure are deferred until observed use establishes a need.

## 8. Guardrails and Privacy Notes

Tracked files contain only fictional notes and synthetic outputs. Real addresses, household routines, family details, photos, health, financial, employer, private-project, logs, memory, state, credentials, and machine-specific paths must never be committed. The formatter refuses diagnosis and redirects monitoring, purchasing, reminders, messaging, and device control outside its scope.

The user reviews every checklist before export. File writing is limited to an explicit user-selected destination; broad discovery or scanning is prohibited. Temporary state is cleared after the run. Events describe milestones without copying full inputs. Exports contain only reviewed checklist content and should be sanitized before sharing.

## 9. Codex Implementation Prompt

```text
Project name: Garden Note Formatter

Goal:
Build a small local/file-first formatter that accepts one synthetic garden note and a date, produces a faithful reviewable checklist, and exports dated Markdown after explicit user confirmation.

Context:
This is a fictional public-safe project. The approved pattern is a single workflow agent with no memory and only temporary run state. Human review is required before export.

First inspect the current repository, its instructions, status, existing files, tests, schemas, and documented workflows. Preserve useful existing files and keep changes small and inspectable.

Architecture summary:
- One input-to-output loop: note plus date -> draft -> review -> Markdown export.
- Extract only explicit tasks; flag ambiguity and never invent advice.
- Use a local command or dependency-free direct local harness.
- Clear temporary run state after completion; add no memory.

UI/harness summary:
The interface must keep intake, status, preview, review, and export together. Do not make normal use depend on copying a prompt to another service and pasting output back; that is only a prototype/manual fallback.

Assumptions:
- All tracked fixtures are synthetic.
- A local command is acceptable unless an existing direct local harness is already the smaller complete path.
- No network or model execution is needed.

Files to create or modify:
- README.md for local usage and privacy boundaries.
- Narrow identity, operating-style, capability, interface, tool-boundary, and guardrail artifacts.
- A checklist output schema.
- Synthetic input/output fixtures and JSONL eval cases.
- The smallest local entry point required by the selected interface.

Implementation steps:
1. Inspect the repository and preserve useful existing artifacts.
2. Confirm the exact files against repository conventions.
3. Define the checklist output contract and synthetic fixtures.
4. Implement the local input, formatting, preview, confirmation, and export loop.
5. Enforce no-invention, no-diagnosis, minimal-file-access, and clear/reset behavior.
6. Add standard-library or existing-tool validation without new dependencies unless separately approved.
7. Run schema, JSONL, fixture, privacy, and end-to-end checks.
8. Review the diff for generated output, secrets, private content, and machine-specific paths.

Guardrails:
Avoid secrets, private data, real logs, memory, durable state, and machine-specific paths. Use synthetic fixtures only. Require human review before export or any consequential action. Do not add broad filesystem access.

Testing and validation:
Run the repository's documented validators, JSON/JSONL checks, fixture tests, and a synthetic end-to-end test. Confirm the output contains exactly supported tasks, flags ambiguity, writes only to an explicit location, and leaves generated/private files ignored.

Acceptance criteria:
- One synthetic note and date produce a reviewable dated Markdown checklist.
- Unsupported tasks and diagnoses are not invented.
- Review is explicit before export.
- Fixtures are synthetic and schemas/evals validate.
- Memory is absent and temporary state can be cleared.
- The complete supported flow uses no normal-use copy/paste relay.

What not to build yet:
Provider SDKs, model calls, backend services, databases, cloud deployment, auth, scheduling, messaging, weather monitoring, purchases, device integrations, plant disease diagnosis, memory, durable state, broad filesystem access, or multi-agent orchestration.

Final response requirements:
List files changed, assumptions, exact validation commands and results, failures or skips, generated-output status, and an explicit statement that no sensitive data, secrets, machine paths, or prohibited runtime scope was added.
```

## 10. Powering and Usage Plan

The product needs a local machine, the repository's existing language/runtime, and a user-controlled input/output location. It needs no account, API, provider credential, external data, backend, database, or cloud service. Any local configuration is non-secret and repository-relative; real notes remain outside tracked fixtures.

Memory plan: none. State plan: a temporary run object is inspectable in the interface and cleared on reset or exit. First-run setup is to review the guardrails, run validators, and use the synthetic fixture. Normal usage is open the local interface, enter a note and date, format, review, and export. Success means every output task is supported by the input, ambiguous text is flagged, no external action occurs, and the workflow completes without prompt relay.

## 11. First-Run Checklist

- [ ] Review the approved architecture and implementation diff.
- [ ] Confirm the first usable product remains one note and one checklist.
- [ ] Confirm the local command or harness completes intake through export.
- [ ] Confirm ignored paths cover real inputs, generated output, logs, memory, and state.
- [ ] Use only the fictional fixture in the first run.
- [ ] Validate the output schema and JSONL evals.
- [ ] Run the synthetic safe test and compare supported tasks.
- [ ] Confirm ambiguity is visible and no diagnosis or extra recommendation appears.
- [ ] Confirm temporary state clears and memory does not exist.
- [ ] Human-review the checklist before export.
- [ ] Record only demonstrated gaps as follow-up issues.

## 12. Iteration Backlog

### Fix Next

- Correct any task omission, invention, or Markdown contract failure found by the synthetic first run.

### Improve Later

- Improve ambiguity wording if users cannot distinguish extracted tasks from review notes.
- Add another synthetic fixture only when it covers a demonstrated edge case.

### Consider Only If First Usable Product Proves Useful

- Choose a direct local web harness if CLI review becomes cumbersome.
- Consider a fixed, user-authored formatting preference file; do not add memory automatically.
- Evaluate integrations only in separate issues with new privacy and approval review.
