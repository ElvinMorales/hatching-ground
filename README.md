# Hatching Ground

Hatching Ground is a private-first, file-first incubator for small personal agent ideas. It helps an individual builder turn rough inspiration into structured idea cards, compare a clutch of candidates, select a practical MVP, and prepare an architecture brief and Codex handoff.

This first version is an inspectable documentation scaffold. It contains prompts, workflows, templates, JSON Schemas, guardrails, and lightweight evaluations. It does not build, deploy, or operate agents.

## Who it is for

Use Hatching Ground if you want to discover boring-but-useful personal agents, control scope before architecture work, and keep private material outside version control.

## Smallest useful version

The MVP is a local folder you can use with a writing or coding assistant:

1. Discover ideas with a starter prompt.
2. Create one idea card per candidate.
3. Score the clutch using seven criteria.
4. Choose a hatchling or park, split, merge, or discard it.
5. Create a pre-architecture brief after it passes the hatch gate.
6. Prepare a Codex handoff for a separate implementation effort.

## Quick start

1. Review [the privacy policy](guardrails/privacy-policy.md) before adding content.
2. Copy a prompt from [starter prompts](prompts/starter-prompts.md).
3. Copy [the idea card](templates/idea-card.md) into an ignored `local/` folder.
4. Follow [idea discovery](workflows/idea-discovery.md), [idea intake](workflows/idea-intake.md), and [the scorecard](workflows/incubation-scorecard.md).
5. For the selected idea, follow [the hatching workflow](workflows/hatching-workflow.md).
6. Run `python scripts/validate_scaffold.py` to validate this shared scaffold.

> **Privacy warning:** Never commit real personal data, private notes, memory, state, logs, credentials, employer information, or machine-specific paths. Keep working material in ignored local/private folders. Repository examples must remain synthetic.

See [setup](docs/setup.md), [usage](docs/usage.md), and [maintenance](docs/maintenance.md) for details.

## UI Harness

Hatching Ground now includes an optional local UI harness. It is a self-contained static HTML page that assembles paste-ready prompts, accepts pasted model output, validates it heuristically, and exports Markdown artifacts. It runs from `file://` with no backend, no network calls, no persistence, and no model API keys.

- Open [`ui/hatching-ground.html`](ui/hatching-ground.html) in a browser to start using it.
- See [`ui-harness/README.md`](ui-harness/README.md) for the harness artifact model and contract.
- See [`docs/ui-harness.md`](docs/ui-harness.md) for usage instructions and design rationale.

> **Privacy warning:** The UI is local-first. Nothing leaves your machine. Save exported artifacts to an ignored `local/` or `artifacts/private/` folder—never to a tracked directory unless the content is synthetic and public-safe.
