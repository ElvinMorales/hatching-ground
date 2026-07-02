# Local runtime storage

This directory is the ignored boundary for local Hatching Ground runtime output.

- `sessions/` may contain private local session records.
- `artifacts/` may contain generated Markdown artifacts.
- `runs/` contains complete per-run output directories from the mock runner.

Everything below `local/` is ignored except this README. Never commit generated runs, real sessions, raw logs, memory, state, secrets, employer data, or private input. Tracked fixtures belong under `runtime/examples/` and must remain synthetic and public-safe.

Delete a run by removing only its selected directory under `local/`. Review the resolved path before deletion.
