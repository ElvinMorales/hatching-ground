# Synthetic example pack

> Synthetic public-safe example. Do not treat this as real personal data, memory, state, or implementation output.

This pack follows one fictional, low-risk idea—**Garden Note Formatter**—through the Hatching Ground artifact workflow. It exists so a new user can copy the structure of a complete hatch without needing real personal content. Every person, note, decision, and proposed file is invented.

## Recommended reading order

1. [`synthetic-clutch.md`](synthetic-clutch.md) — compare three candidate ideas.
2. [`synthetic-idea-card.md`](synthetic-idea-card.md) — define the selected idea.
3. [`synthetic-scorecard.md`](synthetic-scorecard.md) — score it against the seven incubation criteria.
4. [`synthetic-decision-record.md`](synthetic-decision-record.md) — record the hatch decision and gate result.
5. [`synthetic-architecture-brief.md`](synthetic-architecture-brief.md) — establish the pre-architecture boundary.
6. [`synthetic-full-architecture.md`](synthetic-full-architecture.md) — design the reviewed first usable product.
7. [`synthetic-codex-handoff.md`](synthetic-codex-handoff.md) — hand a separately authorized implementation to Codex.

This order maps to discovery, intake, scoring, selection and hatch review, architecture briefing, full architecture, and implementation handoff. Human review remains required at the hatch decision, architecture approval, and before any implementation.

## Intentional exclusions

The example does not monitor weather, purchase supplies, send reminders, control devices, diagnose plant disease, call a model provider, use broad filesystem access, or require a backend, database, cloud deployment, memory, or durable state. A local file workflow or direct local harness is enough. Generated runs belong only in ignored local folders.

The existing deterministic mock runtime and mock-connected local web harness demonstrate Hatching Ground's artifact path; they do not implement Garden Note Formatter. The static prompt relay remains a prototype/manual fallback, not the target for repeated use when a direct harness is needed.

## Validation

From the repository root, run:

```sh
python scripts/validate_scaffold.py
python scripts/smoke_test_local_harness.py
python scripts/run_mock_runtime.py --request runtime/examples/synthetic-run-request.json --out local/runs/synthetic-demo --reset
git diff --check
```

Confirm the generated `local/runs/synthetic-demo/` output remains ignored and unstaged.
