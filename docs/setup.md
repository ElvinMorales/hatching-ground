# Setup

## Create or clone

To start a new copy, create a folder named `hatching-ground` and place this scaffold inside it. To use an existing remote, clone it with your normal Git workflow, then review the repository before adding local material.

## Review the scaffold

Read `README.md`, both guardrail documents, and the workflows. Run:

```sh
python scripts/validate_scaffold.py
```

The script checks required files, JSON, JSONL shape, runtime examples and contracts, key content, `.gitignore`, and obvious sensitive placeholders. It uses only Python's standard library.

## Run the mock runtime

No environment variables, keys, packages, or network access are required:

```sh
python scripts/run_mock_runtime.py --request runtime/examples/synthetic-run-request.json --out local/runs/synthetic-demo --reset
```

The command writes only below ignored `local/` storage. Confirm with `git status --short --ignored`; never commit the generated session, events, status, or artifacts.

## Run the local web harness

No package install is required. Start the standard-library server:

```sh
python scripts/serve_local_harness.py --host 127.0.0.1 --port 8765
```

Open `http://127.0.0.1:8765/`. The connected harness runs only the synthetic `full_architecture` mock workflow and stores operational session/run output under ignored `local/harness/`. Provider mode remains deferred. See [the local web harness guide](local-web-harness.md).

## Secrets and private data

No secrets are needed for the mock runtime. Do not create a populated `.env` for this scaffold.

Create personal working cards only under an ignored folder such as `local/ideas/` or `private/`. Confirm with `git status --ignored` before relying on ignore behavior. Never commit real notes, logs, memory, state, exports, credentials, employer material, or machine-specific paths. Use invented examples in shared files.
