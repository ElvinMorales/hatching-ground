# Agent Architecture: [Agent Name]

> Complete this artifact only after the idea has passed or conditionally passed the hatch gate. Use concise, implementation-relevant detail, synthetic examples in anything tracked, and human review before consequential actions or implementation.

## 1. Idea Restatement

Restate the agent idea, intended user, problem, desired outcome, and what the agent should not do. Name assumptions and the hatch gate result, including any conditional-pass requirements.

## 2. Recommended Pattern

Choose and justify one primary pattern, such as prompt-only assistant, file-first mirror agent, personal operations agent, research-to-action agent, maintenance agent, workflow agent, tool-using agent, memory-enabled personal agent, state-tracking agent, local runtime scaffold, local web harness agent, or gateway-backed agent. Prefer a single agent; avoid multi-agent systems unless a concrete requirement clearly justifies their added coordination and risk.

## 3. First Usable Product Scope

Define a first usable product, not a bare MVP. State what it does, what it does not do, how the user completes the core workflow end-to-end, what can wait, and what would make the product more work than the task itself. Identify whether the interaction depends on a copy/paste relay. If normal use requires copying prompts into another chat tool and pasting results back, classify that as a **prototype/manual fallback**, not the target product experience.

## 4. Taxonomy Artifact Map

Map every bucket below. For each one, choose `First Usable Product`, `Later`, or `Not Needed`; name the concrete artifact or `None`; and explain the boundary briefly.

| Bucket | First Usable Product / Later / Not Needed | Artifact | Notes |
| --- | --- | --- | --- |
| Identity | [Classification] | [Artifact or None] | [Notes] |
| Operating style | [Classification] | [Artifact or None] | [Notes] |
| Capability modules | [Classification] | [Artifact or None] | [Notes] |
| Tools | [Classification] | [Artifact or None] | [Notes] |
| Knowledge and resources | [Classification] | [Artifact or None] | [Notes] |
| Prompts and interfaces | [Classification] | [Artifact or None] | [Notes] |
| Memory | [Classification] | [Artifact or None] | [Need, retention, review, and deletion; do not merge with state] |
| State | [Classification] | [Artifact or None] | [Lifecycle, inspection, clearing, and archive; do not merge with memory] |
| Planning and orchestration | [Classification] | [Artifact or None] | [Notes] |
| Guardrails and governance | [Classification] | [Artifact or None] | [Notes] |
| Outputs and schemas | [Classification] | [Artifact or None] | [Notes] |
| Evaluation and observability | [Classification] | [Artifact or None] | [Notes] |
| Runtime and deployment | [Classification] | [Artifact or None] | [Notes] |
| Learning and iteration | [Classification] | [Artifact or None] | [Notes] |

## 5. Proposed Repo Structure

Provide a practical file tree or bullet list with each file's purpose. Include only files the agent actually needs; use Markdown, YAML, JSON Schema, and JSONL when useful; avoid adding every possible folder by default; and keep real private data out of public repositories.

## 6. UI Harness Recommendation

Decide and justify the recommended interaction surface for every architecture. State whether a UI harness is needed; whether ChatGPT, Claude, Codex, or a CLI is sufficient; whether a local web harness is needed; whether an existing self-hosted UI is sufficient; and whether a gateway-backed harness is justified.

Define what the first usable interface must show, what session state exists, what progress or events are visible, which actions require approval, and which artifacts appear in the artifact drawer. If memory exists, explain how proposals are reviewed and deleted. If state exists, explain how temporary state is inspected, cleared, or archived. State whether the workflow requires manual copy/paste between systems. Classify manual copy/paste in normal use as a **prototype/manual fallback**, not the target interaction.

## 7. Key Design Decisions

Explain concisely why this pattern fits, why the design is single-agent by default, why memory is or is not needed, why state is or is not needed, why the chosen interface fits, and what is deliberately deferred.

## 8. Guardrails and Privacy Notes

Specify what data stays private, what must never be committed, what examples and fixtures must be synthetic, what actions require explicit approval, what the agent should refuse or redirect, and what it should never automate. If memory exists, define review and deletion. If state exists, define clearing and archiving. Explain how UI logs, event streams, and exported artifacts are minimized and sanitized.

## 9. Codex Implementation Prompt

Write a complete, copy-paste-ready prompt inside a fenced text block. It must contain: project name; goal; context; an instruction to inspect the current repository first and preserve useful files; architecture summary; UI harness summary when relevant; assumptions; files to create or modify; ordered implementation steps; guardrails; testing and validation instructions; acceptance criteria; what not to build yet; and final response requirements.

Tell Codex to avoid secrets, private data, real logs, memory, state, and machine-specific paths; use synthetic examples; retain human review for consequential actions; and avoid turning a copy/paste round trip into the final user workflow when a direct harness is needed.

```text
[Complete Codex implementation prompt]
```

## 10. Powering and Usage Plan

Define required tools, accounts, APIs (if any), local folders, configuration, where secrets live, required data, and data the agent must not access. Specify separate memory and state plans, the interaction/harness plan, first-run setup, normal usage workflow and cadence, a synthetic safe test scenario, and measurable success criteria.

## 11. First-Run Checklist

- [ ] Clone or create the repository.
- [ ] Review generated files before use.
- [ ] Confirm the first usable product scope.
- [ ] Confirm the interaction surface and any fallback path.
- [ ] Confirm `.gitignore` covers private data, secrets, logs, memory, state, sessions, and generated local artifacts as applicable.
- [ ] Add only synthetic sample data to tracked files.
- [ ] Validate schemas.
- [ ] Validate evals and JSONL.
- [ ] Run the safe sample workflow.
- [ ] Review generated artifacts and privacy classifications.
- [ ] Review memory proposals, if any.
- [ ] Create focused v2 issues from demonstrated gaps.

## 12. Iteration Backlog

Group only evidence-based follow-up work. Avoid bloat and defer speculative integrations.

### Fix Next

- [Defect or blocker found in first use]

### Improve Later

- [Bounded improvement supported by usage evidence]

### Consider Only If First Usable Product Proves Useful

- [Speculative integration, automation, hosting, or expansion]
