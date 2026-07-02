# Usage

The canonical artifact path is:

`idea discovery -> idea intake -> incubation scorecard -> hatching workflow -> architecture brief -> full architecture -> Codex handoff`

1. Start with a prompt from `prompts/starter-prompts.md` and follow `workflows/idea-discovery.md`.
2. Create one idea card per candidate in an ignored local folder using `workflows/idea-intake.md`.
3. Score the clutch with `workflows/incubation-scorecard.md`.
4. Pick one hatchling or explicitly park, split, merge, or discard each candidate.
5. Follow `workflows/hatching-workflow.md`, apply the hatch gate, and create a pre-architecture brief.
6. After a pass or conditional pass and human review, follow `workflows/full-architecture.md` and complete `templates/full-agent-architecture.md`.
7. Review the full architecture, then use its Codex implementation prompt as a handoff for a separately authorized implementation issue.

The full architecture is a design artifact, not a runtime. It must define an end-to-end first usable product and make an explicit UI harness decision. Any normal-use copy/paste relay is a prototype/manual fallback, not the target experience. Keep private instances in ignored local folders and use only synthetic examples in tracked files.

## Synthetic example

Suppose a fictional user repeatedly writes unstructured garden-task notes. A narrow candidate is a **Garden Task Note Formatter**: it converts a pasted synthetic note into a dated checklist saved for review. It needs no integration, memory, or hosting. Its first-run test is whether three synthetic notes produce accurate checklists without inventing tasks. This is public-safe because both the scenario and test data are invented.

The “universal garden manager” version—weather monitoring, purchases, reminders, and device control—should be split and deferred. The formatter can be useful before any automation exists.

## Exercise the runtime contract

After reviewing the synthetic request, run:

```sh
python scripts/run_mock_runtime.py --request runtime/examples/synthetic-run-request.json --out local/runs/synthetic-demo --reset
```

Review `session.json`, `events.jsonl`, `run-status.json`, `artifacts.json`, `runtime-result.json`, and the Markdown file below `local/runs/synthetic-demo/`. These files are ignored local output and must not be committed. The runner is the mock execution layer a future local web harness can consume; it is not the web harness or a model provider.

Delete only the reviewed `local/runs/synthetic-demo/` directory when finished. Mock fixtures must be synthetic and public-safe; real private context, secrets, memory, state, and raw logs do not belong in tracked files.

## Use the local web harness

For the supported mock workflow, start the local server and keep the full interaction in one browser interface:

`open local harness -> create session -> provide context once -> run mock workflow -> inspect events and status -> preview artifact -> export artifact`

Run `python scripts/serve_local_harness.py --host 127.0.0.1 --port 8765`, open `http://127.0.0.1:8765/`, and use only synthetic public-safe context. Refreshing the browser reloads sessions from ignored local server files. Normal use of this supported flow has no prompt/output copy/paste relay. See [the detailed guide](local-web-harness.md).
