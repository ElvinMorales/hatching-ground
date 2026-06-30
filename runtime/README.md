# Runtime boundary

The MVP is local-first and file-first. It requires no runtime integration: Markdown, JSON, a text editor, and optional assistant conversations are sufficient. The repository contains no agent runner and should not receive broad filesystem or write permissions.

## Possible later runtime options

- **Local folder only:** The current default and lowest-complexity option.
- **ChatGPT project:** A possible reviewed workspace for safe artifacts.
- **Codex handoff:** A bounded implementation prompt after an idea passes the hatch gate.
- **VPS:** Optional later hosting only when a proven workflow requires it.
- **OpenClaw Gateway:** Optional later integration only after a separate threat model and architecture review.

VPS and OpenClaw Gateway are not part of this MVP.

## Later hardening requirements

- Start read-only and apply least privilege.
- Never grant broad filesystem access.
- Store secrets in ignored `.env` files or an appropriate secret manager.
- Require human approval for writes, sends, commits, deletes, spending, contacting people, and consequential changes.
- Define data retention, auditability, failure behavior, and a kill switch before enabling automation.
