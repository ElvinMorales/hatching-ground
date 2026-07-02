# Local harness frontend

This folder contains the dependency-free browser interface for the local mock harness:

- `index.html` defines session intake, status, events, and artifact views.
- `styles.css` provides local responsive styling with system fonts.
- `app.js` calls same-origin `/api/` endpoints exposed by `scripts/serve_local_harness.py`.
- `example-session-summary.json` documents a synthetic session-list response.

Start the required Python standard-library server from the repository root:

```powershell
python scripts/serve_local_harness.py --host 127.0.0.1 --port 8765
```

Then open `http://127.0.0.1:8765/`. Opening `index.html` directly does not provide the API.

The frontend loads no external scripts, styles, fonts, or analytics. It does not use browser persistent storage. Durable operational session state and generated output stay under ignored `local/harness/` paths. Use only synthetic public-safe demo input; do not put secrets or real private data in tracked examples.

Provider mode, API keys, model calls, and network integrations are deferred.

Run `python scripts/smoke_test_local_harness.py` from the repository root for a browserless server/API golden-path check.
