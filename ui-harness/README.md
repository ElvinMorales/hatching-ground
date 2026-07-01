# UI Harness

Hatching Ground's UI harness is the artifact layer that connects the documentation scaffold to your interaction with Claude or GPT. It manages sessions, workflows, generated prompts, pasted model outputs, validation, and exported artifacts—without any backend, model API, persistence, or network calls.

## Why a harness, not just files

The documentation scaffold is the canonical source of truth. But using it repeatedly meant copying prompts, filling in context fields manually, and tracking which workflow applied. The harness makes that mechanical work easier without changing the underlying artifact-first approach.

## Session model

A session captures one round of Hatching Ground use: which workflow you selected, what context you provided, the prompt that was generated, the model output you pasted back, validation results, and any artifacts you exported. Sessions are ephemeral by default—nothing is stored between page loads. Export artifacts you want to keep to a local ignored folder.

See `session.schema.json` for the full field list.

## Workflow model

Each workflow is a named, structured interaction pattern:

- **first_clutch_brainstorm** — discover a small clutch of candidates
- **idea_card** — turn a rough idea into a structured idea card
- **score_clutch** — score a set of candidates against seven criteria
- **hatch_gate** — check whether an idea is ready for architecture work
- **architecture_brief** — produce a focused pre-architecture brief
- **full_architecture** — produce a twelve-section full architecture document
- **codex_handoff** — prepare an implementation prompt for a Codex or coding agent
- **public_private_boundary** — classify public vs. private content and surface risks

See `workflow.schema.json` for the full field list.

## Artifact model

An artifact is a named, typed output you export from a session: an idea card, a clutch score, an architecture brief, a Codex handoff, or a public/private checklist. Artifacts carry a privacy classification and a `should_commit` flag that defaults to false.

See `artifact.schema.json` for the full field list.

## Validation model

After pasting model output back into the harness, heuristic validation checks for required sections, privacy notes, bounded scope, and absence of prohibited patterns (cloud deployment, broad permissions, automatic actions). Validation is advisory—it flags missing structure but does not block export.

## Privacy model

The UI is local-first. The page does not send anything automatically. Content only leaves your machine if you copy it into Claude/GPT, download/share it, or commit it. No cookies, no localStorage, no sessionStorage, no network calls, no analytics. Private session data lives only in your browser's page memory until you close or reload the tab. Export artifacts to an ignored `local/` or `artifacts/private/` folder—never to tracked folders unless the content is synthetic and public-safe.

## Future runtime possibilities

A future runtime layer could add durable session storage (encrypted local file), a lightweight server for multi-session management, or integration with OpenClaw Gateway for controlled model API calls. Those capabilities are explicitly deferred from this MVP. See `harness-contract.md` for the boundary.

## Why model APIs and persistence are deferred

Adding model API calls now would require key management, error handling, cost controls, and a more complex trust model. Persistence would require a storage format, migration strategy, and backup plan. Neither is necessary for the core workflow. Manual copy/paste keeps the user in control and the harness inspectable.
