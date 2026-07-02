# UI Harness

## Connected local mock harness

`ui/local-harness/` is the implemented first mock-connected interface. Start it through `python scripts/serve_local_harness.py --host 127.0.0.1 --port 8765` and open `http://127.0.0.1:8765/`.

For the synthetic `full_architecture` workflow, one local interface creates/resumes operational sessions, collects context, invokes the mock runtime adapter, renders user-visible events and run status, lists artifacts, previews Markdown, and offers Markdown/JSON export. Normal use of this supported flow no longer requires a copy/paste relay. Data stays in ignored `local/harness/`; it is operational state, not memory.

The harness is local-first and makes no external network calls. It uses browser-native HTML/CSS/JavaScript and a Python standard-library server. Provider mode is deferred and there are no provider settings, API-key fields, SDKs, or model calls.

## Static prototype/manual fallback

`ui/hatching-ground.html` remains available as a self-contained `file://` page. It assembles prompts, accepts manually pasted model output, validates heuristically, and exports Markdown without a server or persistence. Use it for workflow testing or when the connected harness is unavailable.

The static page's prompt/output relay is a fallback, not the target normal interaction. It has no backend, network calls, external dependencies, model API calls, or broad filesystem access.

## Current and deferred capability

The connected harness currently supports only one synthetic, public-safe mock `full_architecture` workflow. The broader first usable product still needs additional incubation workflows, UI-visible approval resolution, cancellation, explicit deletion controls, migration and recovery behavior, and private-data hardening.

Provider adapters, real model runs, database/cloud sync, OpenClaw Gateway, deployment, auth, multi-agent orchestration, scheduling, messaging, monitoring, live memory/state, and broad filesystem or write-capable tools remain deferred.

## Artifact export and privacy

The artifact drawer shows title, filename, type, privacy classification, and commit recommendation. It can preview/copy/download Markdown and export a run bundle as JSON. Export does not make content safe to commit.

Use only synthetic public-safe data in the implemented demo path. Never commit real personal, health, financial, employer, credential, memory, state, transcript, event-stream, or generated session data. Private outputs must remain in ignored `local/` or `artifacts/private/` paths. See [the local web harness guide](local-web-harness.md) for operation and troubleshooting.
