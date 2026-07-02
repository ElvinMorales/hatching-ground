# Hatching Ground

Hatching Ground is a private-first, file-first incubator for small personal agent ideas. It helps an individual builder turn rough inspiration into structured idea cards, compare a clutch of candidates, select a practical first usable product, and prepare an architecture brief, full architecture, and Codex handoff.

This version is an inspectable documentation scaffold with a deterministic local mock runtime adapter and a mock-connected local web harness. It contains prompts, workflows, templates, JSON Schemas, guardrails, lightweight evaluations, and the static UI prototype/manual fallback. It does not call providers, deploy, or operate real agents.

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
7. Review the [synthetic public-safe example pack](examples/README.md) to see one fictional idea traverse the full workflow.
8. Run `python scripts/validate_scaffold.py` to validate this shared scaffold.
9. Optionally run `python scripts/run_mock_runtime.py --request runtime/examples/synthetic-run-request.json --out local/runs/synthetic-demo --reset` to exercise the synthetic runtime contract.
10. Run `python scripts/serve_local_harness.py --host 127.0.0.1 --port 8765` and open `http://127.0.0.1:8765/` for the connected mock workflow.

> **Privacy warning:** Never commit real personal data, private notes, memory, state, logs, credentials, employer information, or machine-specific paths. Keep working material in ignored local/private folders. Repository examples must remain synthetic.

See [setup](docs/setup.md), [usage](docs/usage.md), and [maintenance](docs/maintenance.md) for details.

## Synthetic examples

The [`examples/`](examples/README.md) directory shows the fictional **Garden Note Formatter** moving from a clutch through idea selection, scoring, decision, architecture, and Codex handoff. These public-safe artifacts are structural references, not real personal data, private memory, state, or implementation output.

## Local mock harness

The standard-library server and dependency-free frontend support session create/resume, synthetic context intake, mock execution, events, run status, an artifact drawer, Markdown preview/download, and JSON export for `full_architecture`. Outputs stay in ignored `local/harness/` storage. Provider mode remains visibly deferred. See [the local web harness guide](docs/local-web-harness.md).

## UI Harness

Hatching Ground also preserves a self-contained static UI prototype/manual fallback. It assembles paste-ready prompts, accepts pasted model output, validates it heuristically, and exports Markdown artifacts. It runs from `file://` with no server, network calls, persistence, or model API keys.

The full architecture template is a design output after the hatch gate, not an implemented runtime or UI. It records the first usable product, artifact map, interface decision, privacy boundaries, and implementation handoff.

The first mock-connected step of the target local, session-based product is implemented for one synthetic workflow. Broader workflows, provider execution, approvals, and production/private support remain deferred. See [the first usable product plan](docs/first-usable-product-plan.md).

- Open [`ui/hatching-ground.html`](ui/hatching-ground.html) in a browser to use the current prototype/manual fallback.
- Start `scripts/serve_local_harness.py` to use [`ui/local-harness/`](ui/local-harness/) with the mock runtime.
- See [`ui-harness/README.md`](ui-harness/README.md) for the expanded harness artifact set.
- See [`docs/ui-harness.md`](docs/ui-harness.md) for current fallback instructions and the target distinction.

> **Privacy warning:** The current static UI is local-first. The page does not send anything automatically. Content only leaves your machine if you copy it into Claude/GPT, download/share it, or commit it. Save exported artifacts to an ignored `local/` or `artifacts/private/` folder—never to a tracked directory unless the content is synthetic and public-safe.
