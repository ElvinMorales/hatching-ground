# Local Web Harness

## Purpose and boundary

The local web harness is the first usable, mock-connected Hatching Ground interface. It lets one user create or resume a local session, run the synthetic `full_architecture` workflow, inspect structured events and status, preview its Markdown artifact, and export the artifact or a JSON run bundle without relaying a prompt through another chat tool.

It is separate from `ui/hatching-ground.html`, which remains the self-contained static prototype/manual fallback. The fallback opens directly from `file://` and supports manual prompt/output relay. The connected harness lives in `ui/local-harness/` and requires the local standard-library server.

The server accepts a narrow JSON request, stores operational session state under ignored `local/harness/`, invokes `scripts/run_mock_runtime.py`, and presents the adapter's existing event, status, manifest, result, and artifact files. A harness session is operational state, not memory.

Provider mode remains deferred. The harness has no provider settings, API keys, model calls, network integrations, external frontend dependencies, database, authentication, or deployment support.

## Start the server

From the repository root, run:

```sh
python scripts/serve_local_harness.py --host 127.0.0.1 --port 8765
```

No package installation is required. The server prints:

```text
Hatching Ground local harness: http://127.0.0.1:8765/
```

Open that URL in a browser. The default bind address is loopback-only `127.0.0.1`; do not expose this development harness as a remote service.

## Golden path

1. Select **New session**.
2. Keep the `full_architecture` workflow selected.
3. Enter only invented, public-safe context. The prefilled Garden Note Formatter context is synthetic.
4. Select a `pass` or `conditional-pass` hatch gate result and create the session.
5. Select **Run mock workflow**.
6. Confirm the status is `completed`, progress is 100%, and six user-visible events appear.
7. Select the full architecture in the artifact drawer and preview its 12-section Markdown.
8. Copy or download the Markdown, or select **Export run JSON**.
9. Refresh the browser and confirm the local session and latest run resume from server-side files.

No prompt relay to a model interface is part of this flow.

For a browserless golden-path check, run:

```sh
python scripts/smoke_test_local_harness.py
```

The standard-library smoke test starts the server on a temporary loopback port, exercises health, workflow, session, run, artifact, export, and static-file endpoints, checks dependency and storage boundaries, and terminates the server cleanly.

## Local output layout

Generated data stays under ignored paths:

```text
local/harness/
  sessions/                  operational session records
  runs/<session>/<run>/      generated request and mock adapter output
  exports/<session>/         JSON run bundles requested from the UI
```

Each run retains `runtime-request.json` beside an `output/` folder containing `session.json`, `events.jsonl`, `run-status.json`, `artifacts.json`, `runtime-result.json`, and generated Markdown. Inspect these files locally when diagnosing the harness. Never stage generated sessions, requests, events, status, exports, or artifacts.

## Delete local data safely

Stop the server first. Review the target with `git status --short --ignored`, then delete only the generated `local/harness/` directory using the normal file manager or a path you have verified is inside this repository. Preserve tracked `local/README.md`. Restarting the server recreates the empty harness folders.

## Privacy and safety

The implemented demo path permits only `privacy_mode: synthetic-public-safe`. Do not claim private production support. Do not enter secrets, real personal or family data, health or financial data, employer data, raw logs, memory, or state. The server does not log request bodies, and API errors do not return stack traces, but this is a development harness rather than a hardened private-data system.

Generated artifacts require human review before consequential use. Export does not mean an artifact is safe to commit.

## Troubleshooting

- **Page cannot reach the API:** start the server and open its HTTP URL; do not open `index.html` directly.
- **Port already in use:** stop the other local process or choose another local port with `--port`.
- **Session or run not found:** refresh the session list. Create a new session if its ignored local files were removed.
- **Mock run fails:** run `python scripts/validate_scaffold.py`, then exercise `scripts/run_mock_runtime.py` with the documented synthetic request.
- **Browser clipboard is unavailable:** select and copy the Markdown preview manually or use the download link.

## Deferred work

Provider adapters and model calls, additional workflows, approval interactions, cancellation, private-data hardening, deletion controls in the UI, migrations, auth, deployment, messaging, scheduling, memory/state systems, broad filesystem tools, and production monitoring remain later separately reviewed work.
