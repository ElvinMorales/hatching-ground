# Runtime boundary

Hatching Ground now has a small local-first, mock-only runtime adapter. It accepts one `full_architecture` request, emits structured user-visible records, and writes a synthetic Markdown artifact. It uses the Python standard library, requires no key or network, and is a development/testing boundary rather than the final web harness.

## Current mock adapter

```sh
python scripts/run_mock_runtime.py --request runtime/examples/synthetic-run-request.json --out local/runs/synthetic-demo --reset
```

The selected directory below `local/` receives `session.json`, `events.jsonl`, `run-status.json`, `artifacts.json`, `runtime-result.json`, and `artifacts/full-agent-architecture.md`. The runner reads only the request path and refuses to write outside this repository's ignored `local/` folder.

Validate contracts and tracked examples with `python scripts/validate_scaffold.py`. See [mock-runner.md](mock-runner.md) for usage and limitations.

## Future provider adapter

Provider mode is not implemented. Credentials, provider calls, SDKs, retries, cancellation, and usage reporting remain behind the documented boundary in [provider-adapter-boundary.md](provider-adapter-boundary.md). Provider runtime integrations, backend services, databases, deployment, and OpenClaw are not part of this MVP.

## Storage and safety

Generated runtime data belongs only under ignored `local/sessions/`, `local/artifacts/`, or `local/runs/`. Tracked examples must be synthetic and public-safe. Events are not raw logs, transcripts are not memory, and run status is not durable memory. Never grant broad filesystem access. Apply least privilege and require human review for consequential actions.

Do not build provider calls, a backend, a web UI, a database, live memory/state, monitoring, messaging, or multi-agent orchestration in this runtime foundation.
