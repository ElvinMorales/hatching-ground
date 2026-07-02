# Full architecture workflow

## Purpose

Turn a hatch-gate-ready idea and its pre-architecture brief into one complete, buildable design artifact. The output defines the first usable product, its artifact and interface boundaries, and a reviewed handoff for a later Codex implementation pass. This workflow produces architecture only; it does not authorize implementation.

## When to use this workflow

Use this workflow only after:

- an idea card exists;
- the idea has passed or conditionally passed the hatch gate; and
- the user has enough context to define a first usable product.

A conditional pass must name its unresolved conditions, and the architecture must preserve them as explicit assumptions, decisions, or pre-implementation checks.

## When not to use it

Do not use this workflow when:

- the idea is still vague;
- the idea should be parked, split, merged, or discarded;
- the user only needs a seed prompt;
- a pre-architecture brief is enough; or
- the workflow would force premature implementation.

Return to the idea card, scorecard, or hatch gate instead of inventing missing decisions.

## Required inputs

- The selected idea card.
- Hatch gate result: passed or conditionally passed, with evidence and conditions.
- The architecture brief.
- A privacy-reviewed description of the user, problem, desired outcome, and exclusions.
- Enough workflow detail to describe an end-to-end first usable product.
- Known constraints, available tools, and any material interface preferences.

Use synthetic or abstracted inputs in tracked or public-safe artifacts. Keep private working context in ignored local folders.

## Step-by-step process

1. Verify the required inputs and record the hatch gate result.
2. Restate the idea, intended user, problem, outcome, and non-goals.
3. Select one primary agent pattern. Use a single agent by default and justify any exception.
4. Define the first usable product as a complete input-to-output workflow, not a bare MVP or disconnected demo.
5. Map all 14 taxonomy buckets to first usable product, later, or not needed artifacts.
6. Propose only the repository files the agent actually needs.
7. Make the UI harness decision using the rules below.
8. Record the material design decisions, including memory and state as separate concerns.
9. Define privacy boundaries, approval points, refusals, sanitization, and data lifecycles.
10. Write a copy-paste-ready Codex implementation prompt for a later, explicitly authorized implementation pass.
11. Specify powering, configuration, first-run setup, normal usage, and a synthetic safe test.
12. Complete the first-run checklist and a deliberately bounded iteration backlog.
13. Validate the artifact and obtain human review before implementation.

## Hatch gate dependency

Do not generate a full architecture unless the hatch gate passed or conditionally passed. A conditional pass is acceptable only when its conditions do not prevent a coherent first usable product; carry every condition into the architecture and Codex acceptance criteria. If readiness cannot be established, stop and recommend the smallest next idea-card, scorecard, or hatch-gate action.

## Architecture generation rules

- Use the exact 12-section structure in `templates/full-agent-architecture.md`.
- Design the smallest product that supports the core workflow end-to-end.
- Prefer one agent, local-first operation, inspectable artifacts, least privilege, and human review.
- Separate memory from temporary or durable operational state. Include neither without a demonstrated need and lifecycle.
- State assumptions when missing information does not materially change architecture or safety.
- Ask only questions whose answers materially change architecture, safety, or the recommendation.
- Defer speculative integrations, hosting, automation, and infrastructure.
- Do not turn architecture generation into runtime implementation.

## UI harness decision rules

Every full architecture must recommend an interaction surface and explain whether ChatGPT, Claude, Codex, a CLI, a local web harness, an existing self-hosted UI, or a gateway-backed harness fits the workflow.

- Use an existing conversational or CLI surface when it completes the workflow cleanly and exposes the necessary review points and artifacts.
- Recommend a local web harness when normal use needs a coherent session, structured intake, progress/events, approvals, artifact review, or direct end-to-end execution.
- Consider an existing self-hosted UI before proposing a custom harness.
- Justify a gateway-backed harness only for a proven runtime or access requirement and after threat-model review.
- Describe visible interface content, session state, progress/events, approvals, artifact drawer contents, memory review, and state inspection or clearing as applicable.
- If normal use requires copying a prompt into another system and pasting the result back, classify that interaction as a **prototype/manual fallback**, never the target product experience.

## Public/private boundary rules

- Treat real personal content, credentials, memory, state, sessions, event streams, raw logs, employer data, and machine-specific paths as private and untracked.
- Use only synthetic examples in versioned artifacts and tests.
- Identify public-safe schemas, templates, prompts, and fictional fixtures separately from private runtime data.
- Put secrets in an appropriate ignored secret store or environment mechanism; never include secret values in architecture artifacts.
- Require explicit human approval for consequential, external, destructive, or write-capable actions.
- Sanitize exported artifacts and UI-visible logs or events before sharing or committing them.

## Output requirements

Produce one Markdown artifact based on `templates/full-agent-architecture.md`. It must contain all 12 sections, the complete 14-bucket taxonomy table, an explicit UI harness recommendation, a complete Codex implementation prompt, a powering and usage plan, a first-run checklist, and a grouped iteration backlog. Save private instances only in an ignored local location.

## Validation checklist

- [ ] Idea card and architecture brief are identified.
- [ ] Hatch gate is recorded as passed or conditionally passed.
- [ ] Every conditional-pass requirement remains visible.
- [ ] All 12 required sections are complete.
- [ ] The first usable product supports the core workflow end-to-end.
- [ ] Any copy/paste relay is labeled prototype/manual fallback.
- [ ] All 14 taxonomy buckets are mapped.
- [ ] Memory and state are evaluated separately.
- [ ] The UI harness decision covers interface, sessions, events, approvals, artifacts, memory, and state as applicable.
- [ ] Public/private boundaries and approval requirements are explicit.
- [ ] The Codex prompt includes files, steps, tests, acceptance criteria, exclusions, and final response requirements.
- [ ] The first-run scenario is synthetic and safe.
- [ ] Speculative integrations and unnecessary infrastructure are deferred.
- [ ] A human has reviewed the architecture before implementation.

## Recommended next step

After human review, use the architecture's Codex implementation prompt to open a separately scoped implementation issue. Recheck privacy, permissions, and acceptance criteria before authorizing code or runtime changes.
