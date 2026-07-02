# Mock runtime runner

## Purpose

`scripts/run_mock_runtime.py` proves the local runtime contract before provider or UI work. It deterministically executes the synthetic `full_architecture` workflow without keys, network access, provider SDKs, private data, or external dependencies.

## Run it

```sh
python scripts/run_mock_runtime.py --request runtime/examples/synthetic-run-request.json --out local/runs/synthetic-demo --reset
```

`--reset` deletes only the selected directory below `local/` before recreating it. `--quiet` suppresses the success summary. The runner refuses an output path outside the repository's ignored `local/` tree.

## Output

- `session.json`: local session metadata and run/artifact references.
- `events.jsonl`: user-visible structured activity, not raw logs.
- `run-status.json`: completed run state compatible with the harness contract.
- `artifacts.json`: a manifest whose entries match the artifact contract.
- `artifacts/full-agent-architecture.md`: the 12-section synthetic artifact.
- `runtime-result.json`: portable relative paths and the final result.

## Safe data and cleanup

Use only fictional, public-safe context in the tracked request. Real local runs may still be private and must never be committed. Do not provide secrets, health or financial data, employer data, private memory/state, or raw logs.

To clean up, review the path and delete the specific run directory under `local/runs/`. Do not remove the tracked `local/README.md`.

## Limitations and future consumption

The runner supports only `runtime_mode: mock` and `workflow: full_architecture`. It does not call a model, validate general JSON Schema, persist across a service, expose an API server, or implement cancellation. A future local UI can invoke the same narrow command/API boundary, consume `events.jsonl` and `run-status.json`, and display the artifact manifest without exposing provider-specific details to the UI.
