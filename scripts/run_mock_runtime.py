#!/usr/bin/env python3
"""Run one deterministic, standard-library-only Hatching Ground mock workflow."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = (ROOT / "local").resolve()
REQUIRED_REQUEST_FIELDS = {
    "request_id", "session_id", "run_id", "agent_id", "workflow",
    "runtime_mode", "created_at", "context", "privacy_mode", "output_preferences",
}
REQUIRED_CONTEXT_FIELDS = {
    "idea_name", "hatch_gate_result", "architecture_brief_summary",
    "constraints", "desired_artifact_type",
}
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", required=True, type=Path, help="Runtime request JSON file")
    parser.add_argument("--out", required=True, type=Path, help="Output directory below local/")
    parser.add_argument("--reset", action="store_true", help="Clear the selected output directory first")
    parser.add_argument("--quiet", action="store_true", help="Suppress the success summary")
    return parser.parse_args()


def require_local_output(path: Path) -> Path:
    resolved = (ROOT / path).resolve() if not path.is_absolute() else path.resolve()
    if resolved == LOCAL_ROOT or LOCAL_ROOT not in resolved.parents:
        raise ValueError("--out must select a directory below the repository's ignored local/ folder")
    return resolved


def read_request(path: Path) -> dict[str, Any]:
    with path.resolve().open(encoding="utf-8") as handle:
        request = json.load(handle)
    if not isinstance(request, dict):
        raise ValueError("request must be a JSON object")
    missing = sorted(REQUIRED_REQUEST_FIELDS - request.keys())
    if missing:
        raise ValueError("request is missing fields: " + ", ".join(missing))
    if request["runtime_mode"] != "mock":
        raise ValueError("only runtime_mode 'mock' is implemented")
    if request["workflow"] != "full_architecture":
        raise ValueError("only workflow 'full_architecture' is implemented")
    if request["privacy_mode"] != "synthetic-public-safe":
        raise ValueError("mock runs require privacy_mode 'synthetic-public-safe'")
    context = request["context"]
    if not isinstance(context, dict):
        raise ValueError("context must be an object")
    missing_context = sorted(REQUIRED_CONTEXT_FIELDS - context.keys())
    if missing_context:
        raise ValueError("context is missing fields: " + ", ".join(missing_context))
    if context["hatch_gate_result"] not in {"pass", "conditional-pass"}:
        raise ValueError("full_architecture requires a pass or conditional-pass hatch gate")
    if not isinstance(context["constraints"], list) or not context["constraints"] or not all(
        isinstance(item, str) and item.strip() for item in context["constraints"]
    ):
        raise ValueError("context.constraints must be an array of non-empty strings")
    preferences = request["output_preferences"]
    if not isinstance(preferences, dict) or preferences.get("format") != "markdown":
        raise ValueError("output_preferences.format must be 'markdown'")
    filename = preferences.get("filename")
    if not isinstance(filename, str) or Path(filename).name != filename or not filename.endswith(".md"):
        raise ValueError("output_preferences.filename must be a simple Markdown filename")
    for field in REQUIRED_REQUEST_FIELDS - {"context", "output_preferences"}:
        if not isinstance(request[field], str) or not request[field].strip():
            raise ValueError(f"{field} must be a non-empty string")
    try:
        created_at = datetime.fromisoformat(request["created_at"].replace("Z", "+00:00"))
        if created_at.tzinfo is None:
            raise ValueError
    except ValueError as exc:
        raise ValueError("created_at must be an ISO 8601 date-time with a timezone") from exc
    return request


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def architecture_markdown(context: dict[str, Any]) -> str:
    constraints = "; ".join(context["constraints"])
    return f"""# Agent Architecture: {context['idea_name']}

> Synthetic public-safe mock artifact. Human review is required before implementation.

## 1. Idea Restatement

{context['architecture_brief_summary']} The hatch gate result is `{context['hatch_gate_result']}`. Do not access files broadly or act on the notes.

## 2. Recommended Pattern

Use one local, file-first formatter with deterministic mock execution.

## 3. First Usable Product Scope

Accept reviewed synthetic context and export one reviewable architecture artifact. Provider calls and automation are out of scope.

## 4. Taxonomy Artifact Map

Identity, workflow, guardrails, outputs, and evaluation are first-use artifacts. Memory, live state, hosting, and integrations are not needed.

## 5. Proposed Repo Structure

Keep contracts in tracked Markdown and JSON; keep generated runs under ignored `local/` storage.

## 6. UI Harness Recommendation

A future local web harness may consume the event, status, and artifact files. This mock runner is a command boundary, not the final UI.

## 7. Key Design Decisions

Use one agent, no memory, no provider SDK, and no network dependency. The result stays inspectable and reproducible.

## 8. Guardrails and Privacy Notes

Use synthetic input only for tracked fixtures. Constraints: {constraints}. Never export secrets, private prompts, raw logs, memory, or state. Consequential use requires human review.

## 9. Codex Implementation Prompt

```text
Inspect the repository, preserve artifact-first contracts, and implement only the reviewed bounded formatter using synthetic tests and human review.
```

## 10. Powering and Usage Plan

Run locally with standard-library Python. No account, API, key, database, or external service is required.

## 11. First-Run Checklist

- [ ] Confirm the input is synthetic and public-safe.
- [ ] Run the validator and mock command.
- [ ] Review emitted events, status, metadata, and Markdown.
- [ ] Confirm generated output remains ignored.

## 12. Iteration Backlog

- Fix contract defects found in review.
- Improve the mock only when a consumer demonstrates a need.
- Consider a provider adapter in a separately reviewed issue.
"""


def build_events(
    request: dict[str, Any], artifact_id: str, filename: str, started: datetime
) -> list[dict[str, Any]]:
    base = {
        "session_id": request["session_id"],
        "agent_id": request["agent_id"],
        "risk_level": "low",
    }
    specs = [
        ("001", 0, "session.started", "Started a synthetic full-architecture session.", {"workflow": "full_architecture", "runtime_mode": "mock"}, []),
        ("002", 4, "message.created", "Accepted public-safe fictional garden formatter context.", {"role": "user", "context_summary": "Create a reviewable architecture for a fictional garden-note formatter."}, []),
        ("003", 8, "plan.proposed", "Proposed a bounded mock architecture plan.", {"steps": ["Check hatch readiness", "Draft 12 sections", "Export artifact"]}, []),
        ("004", 14, "progress.updated", "Completed the synthetic architecture draft.", {"current_step": "Export artifact", "progress_percent": 75}, []),
        ("005", 18, "artifact.created", "Created a synthetic public-safe full architecture.", {"artifact_type": "full_architecture", "filename": filename}, [artifact_id]),
        ("006", 20, "run.completed", "Completed the deterministic mock run.", {"run_id": request["run_id"], "status": "completed", "progress_percent": 100}, [artifact_id]),
    ]
    return [
        {
            "event_id": f"evt-{request['run_id']}-{number}",
            **base,
            "timestamp": format_timestamp(started + timedelta(seconds=offset)),
            "type": event_type,
            "human_summary": summary,
            "payload": payload,
            "artifact_ids": artifact_ids,
        }
        for number, offset, event_type, summary, payload, artifact_ids in specs
    ]


def run(request: dict[str, Any], output: Path, reset: bool) -> dict[str, Any]:
    if reset and output.exists():
        shutil.rmtree(output)
    artifacts_dir = output / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    artifact_id = f"artifact-{request['run_id']}-full-architecture"
    filename = request["output_preferences"]["filename"]
    artifact_relative = f"artifacts/{filename}"
    started = datetime.fromisoformat(request["created_at"].replace("Z", "+00:00"))
    started_at = format_timestamp(started)
    artifact_created_at = format_timestamp(started + timedelta(seconds=18))
    completed_at = format_timestamp(started + timedelta(seconds=20))
    (artifacts_dir / filename).write_text(
        architecture_markdown(request["context"]), encoding="utf-8"
    )

    artifact = {
        "artifact_id": artifact_id,
        "artifact_type": "full_architecture",
        "title": f"Agent Architecture: {request['context']['idea_name']}",
        "filename": filename,
        "created_at": artifact_created_at,
        "privacy_classification": "public-safe",
        "source_workflow": "full_architecture",
        "content_summary": "Synthetic mock architecture proving the local runtime artifact contract.",
        "should_commit": False,
    }
    session = {
        "session_id": request["session_id"],
        "agent_id": request["agent_id"],
        "workflow": request["workflow"],
        "created_at": started_at,
        "updated_at": completed_at,
        "privacy_mode": request["privacy_mode"],
        "run_ids": [request["run_id"]],
        "artifact_ids": [artifact_id],
        "summary": f"Synthetic local session for the {request['context']['idea_name']} mock workflow.",
    }
    run_status = {
        "run_id": request["run_id"],
        "session_id": request["session_id"],
        "workflow": request["workflow"],
        "status": "completed",
        "current_step": "Export artifact",
        "started_at": started_at,
        "updated_at": completed_at,
        "completed_at": completed_at,
        "progress_percent": 100,
        "pending_approval_id": None,
        "artifact_ids": [artifact_id],
        "error_summary": None,
    }
    result = {
        "request_id": request["request_id"],
        "session_id": request["session_id"],
        "run_id": request["run_id"],
        "agent_id": request["agent_id"],
        "workflow": request["workflow"],
        "runtime_mode": request["runtime_mode"],
        "status": "completed",
        "started_at": started_at,
        "completed_at": completed_at,
        "event_stream_path": "events.jsonl",
        "run_status_path": "run-status.json",
        "artifact_manifest_path": "artifacts.json",
        "artifact_paths": [artifact_relative],
        "summary": "Created one synthetic public-safe full architecture artifact in deterministic mock mode.",
        "warnings": ["Mock content proves the contract only and requires human review before implementation."],
    }

    write_json(output / "session.json", session)
    events = build_events(request, artifact_id, filename, started)
    (output / "events.jsonl").write_text(
        "".join(json.dumps(event, separators=(",", ":")) + "\n" for event in events),
        encoding="utf-8",
    )
    write_json(output / "run-status.json", run_status)
    write_json(output / "artifacts.json", [artifact])
    write_json(output / "runtime-result.json", result)
    return result


def main() -> int:
    args = parse_args()
    try:
        output = require_local_output(args.out)
        request = read_request(args.request)
        result = run(request, output, args.reset)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if not args.quiet:
        relative_output = output.relative_to(ROOT).as_posix()
        print(f"Completed mock run {result['run_id']}")
        print(f"Output: {relative_output}")
        print(f"Events: {relative_output}/{result['event_stream_path']}")
        print(f"Artifact: {relative_output}/{result['artifact_paths'][0]}")
        print(f"Result: {relative_output}/runtime-result.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
