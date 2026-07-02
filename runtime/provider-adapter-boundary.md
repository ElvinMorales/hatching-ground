# Future provider adapter boundary

Provider mode is not implemented in this issue. Mock mode remains the only executable path and does not require provider configuration.

## Eventual ownership

A future provider adapter may translate a validated runtime request into one bounded provider call, normalize provider output into typed artifacts, emit sanitized user-visible events and status, handle bounded retries and cancellation, and report provider usage/cost when available. It must preserve the same runtime result boundary used by mock mode.

Credentials must live in ignored local environment configuration or an appropriate operating-system secret store. They must never appear in tracked files, requests, prompts, transcripts, events, raw logs, status files, artifacts, errors, or exports. Full private prompts and provider responses must not be logged or included in event payloads.

## Failure, cancellation, and usage

- Cancellation must stop new work promptly and produce a terminal `cancelled` run status without claiming completion.
- Failures must be bounded, user-visible, sanitized, and actionable; retries must have explicit limits.
- Token, request, and estimated cost information should be visible before or immediately after a call when the provider exposes it.
- Partial artifacts must be labeled incomplete and must not silently replace reviewed output.

## Approval boundaries

Selecting provider mode and disclosing reviewed context require explicit user action. Consequential writes, sends, spending, external contact, deletion, or publication require separate UI-visible human approval with a safe deny/cancel default. A provider adapter must never expand filesystem or tool permissions.

## Why deferred

The deterministic mock establishes contracts, storage boundaries, privacy behavior, and consumer expectations without introducing credential risk, network behavior, dependency selection, or provider lock-in. Provider implementation should be a separate reviewed issue after the local consumer proves the boundary is sufficient.
