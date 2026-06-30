# Setup

## Create or clone

To start a new copy, create a folder named `hatching-ground` and place this scaffold inside it. To use an existing remote, clone it with your normal Git workflow, then review the repository before adding local material.

## Review the scaffold

Read `README.md`, both guardrail documents, and the workflows. Run:

```sh
python scripts/validate_scaffold.py
```

The script checks required files, JSON, JSONL shape, key content, `.gitignore`, and obvious sensitive placeholders. It uses only Python's standard library. You can perform the equivalent manually by checking the required paths, parsing both schema files and each JSONL line, and reviewing the content and ignore rules listed in the acceptance criteria.

## Secrets and private data

No secrets are needed for the MVP. Do not create a populated `.env` for this scaffold.

Create personal working cards only under an ignored folder such as `local/ideas/` or `private/`. Confirm with `git status --ignored` before relying on ignore behavior. Never commit real notes, logs, memory, state, exports, credentials, employer material, or machine-specific paths. Use invented examples in shared files.
