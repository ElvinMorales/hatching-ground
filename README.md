# Hatching Ground

Hatching Ground is a private-first, file-first incubator for small personal agent ideas. It helps an individual builder turn rough inspiration into structured idea cards, compare a clutch of candidates, select a practical first usable product, and prepare an architecture brief, full architecture, and Codex handoff.

This version is an inspectable documentation scaffold. It contains prompts, workflows, templates, JSON Schemas, guardrails, lightweight evaluations, and a static UI prototype. It does not build, deploy, or operate agents.

## Who it is for

Use Hatching Ground if you want to discover boring-but-useful personal agents, control scope before architecture work, and keep private material outside version control.

## Smallest useful version

The smallest useful version is a local folder you can use with a writing or coding assistant:

1. Discover ideas with a starter prompt.
2. Create one idea card per candidate.
3. Score the clutch using seven criteria.
4. Choose a hatchling or park, split, merge, or discard it.
5. Create a pre-architecture brief after it passes the hatch gate.
6. Use the reviewed brief to create a 12-section full architecture artifact.
7. Prepare a Codex handoff for a separate implementation effort.

## Quick start

1. Review [the privacy policy](guardrails/privacy-policy.md) before adding content.
2. Copy a prompt from [starter prompts](prompts/starter-prompts.md).
3. Copy [the idea card](templates/idea-card.md) into an ignored `local/` folder.
4. Follow [idea discovery](workflows/idea-discovery.md), [idea intake](workflows/idea-intake.md), and [the scorecard](workflows/incubation-scorecard.md).
5. For the selected idea, follow [the hatching workflow](workflows/hatching-workflow.md).
6. After the hatch gate and brief, follow [the full architecture workflow](workflows/full-architecture.md).
7. Run `python scripts/validate_scaffold.py` to validate this shared scaffold.

> **Privacy warning:** Never commit real personal data, private notes, memory, state, logs, credentials, employer information, or machine-specific paths. Keep working material in ignored local/private folders. Repository examples must remain synthetic.

See [setup](docs/setup.md), [usage](docs/usage.md), and [maintenance](docs/maintenance.md) for details.

## UI Harness

Hatching Ground currently includes a self-contained static UI prototype/manual fallback. It assembles paste-ready prompts, accepts pasted model output, validates it heuristically, and exports Markdown artifacts. It runs from `file://` with no backend, network calls, persistence, or model API keys. This page is useful for workflow testing and fallback use, but its manual copy/paste relay is not the final target interaction.

The full architecture template is a design output after the hatch gate, not an implemented runtime or UI. It records the first usable product, artifact map, interface decision, privacy boundaries, and implementation handoff.

The target first usable product is a local-first, session-based web harness. It will support resumable local sessions, context intake, adapter-backed model runs, a transcript, progress and status, approvals, an artifact drawer, and Markdown export in one interface, without a normal-use copy/paste relay. This is a planned architecture, not an implemented web app. See [the first usable product plan](docs/first-usable-product-plan.md).

- Open [`ui/hatching-ground.html`](ui/hatching-ground.html) in a browser to use the current prototype/manual fallback.
- See [`ui-harness/README.md`](ui-harness/README.md) for the expanded harness artifact set.
- See [`docs/ui-harness.md`](docs/ui-harness.md) for current fallback instructions and the target distinction.

> **Privacy warning:** The current static UI is local-first. The page does not send anything automatically. Content only leaves your machine if you copy it into Claude/GPT, download/share it, or commit it. Save exported artifacts to an ignored `local/` or `artifacts/private/` folder—never to a tracked directory unless the content is synthetic and public-safe.
