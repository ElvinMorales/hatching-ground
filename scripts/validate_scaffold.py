#!/usr/bin/env python3
"""Validate the Hatching Ground documentation scaffold using the standard library."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md", "AGENTS.md", ".gitignore", ".github/workflows/validate.yml",
    "agent/identity.md", "agent/operating-style.md",
    "prompts/starter-prompts.md",
    "workflows/idea-discovery.md", "workflows/idea-intake.md",
    "workflows/incubation-scorecard.md", "workflows/hatching-workflow.md",
    "workflows/full-architecture.md",
    "templates/idea-card.md", "templates/architecture-brief.md",
    "templates/full-agent-architecture.md",
    "templates/codex-handoff.md", "schemas/idea-card.schema.json",
    "schemas/decision-record.schema.json", "guardrails/privacy-policy.md",
    "guardrails/public-private-boundary.md", "runtime/README.md",
    "runtime/.env.example", "runtime/config.example.yaml",
    "runtime/mock-runner.md", "runtime/provider-adapter-boundary.md",
    "runtime/schemas/run-request.schema.json",
    "runtime/schemas/runtime-result.schema.json",
    "runtime/examples/synthetic-run-request.json",
    "runtime/examples/synthetic-runtime-result.json",
    "local/README.md", "scripts/run_mock_runtime.py",
    "scripts/smoke_test_local_harness.py",
    "evals/rubric.md", "evals/cases.jsonl",
    "docs/setup.md", "docs/usage.md", "docs/maintenance.md",
    "docs/first-usable-product-plan.md",
    "scripts/validate_scaffold.py",
    # Synthetic end-to-end example pack
    "examples/README.md", "examples/synthetic-clutch.md",
    "examples/synthetic-idea-card.md", "examples/synthetic-scorecard.md",
    "examples/synthetic-decision-record.md",
    "examples/synthetic-architecture-brief.md",
    "examples/synthetic-full-architecture.md",
    "examples/synthetic-codex-handoff.md",
    # UI harness
    "ui-harness/README.md", "ui-harness/harness-contract.md",
    "ui-harness/session.schema.json", "ui-harness/artifact.schema.json",
    "ui-harness/workflow.schema.json", "ui-harness/events.schema.json",
    "ui-harness/agent-profile.schema.json", "ui-harness/run-status.schema.json",
    "ui-harness/approval.schema.json",
    "ui-harness/examples/synthetic-session.json",
    "ui-harness/examples/sanitized-event-stream.jsonl",
    "ui/hatching-ground.html", "docs/ui-harness.md",
    # Connected local mock harness
    "scripts/serve_local_harness.py", "ui/local-harness/index.html",
    "ui/local-harness/app.js", "ui/local-harness/styles.css",
    "ui/local-harness/README.md", "ui/local-harness/example-session-summary.json",
    "docs/local-web-harness.md",
]

EVAL_FIELDS = {
    "case_name", "user_input", "expected_behavior", "must_include",
    "must_avoid", "pass_fail_notes",
}

EVENT_FIELDS = {
    "event_id", "session_id", "agent_id", "timestamp", "type",
    "human_summary", "payload", "risk_level", "artifact_ids",
}

IGNORE_RULES = {
    ".env", ".env.*", "!.env.example", "local/*", "!local/README.md",
    "local/sessions/", "local/artifacts/", "local/runs/", ".tmp/", "private/",
    "data/private/", "data/local/", "memory/private/", "state/private/",
    "logs/", "runtime/private/", "runtime/logs/", "*.log",
    "ui/local/", "ui-harness/local/", "sessions/private/", "artifacts/private/",
    "local/harness/",
}

CONTENT_CHECKS = {
    "README.md": ["Hatching Ground", "Discover ideas", "Codex handoff", "Never commit", "UI Harness"],
    "AGENTS.md": ["artifact-first", "synthetic examples only", "runtime integrations"],
    "guardrails/public-private-boundary.md": ["Private-only", "Public-safe", "Potentially publishable later"],
    "workflows/hatching-workflow.md": ["Smallest useful version is clear", "No high-risk automation"],
    "runtime/README.md": ["local-first", "provider mode is not implemented", "least privilege"],
    "runtime/mock-runner.md": ["full_architecture", "events.jsonl", "ignored", "limitations"],
    "runtime/provider-adapter-boundary.md": ["not implemented", "cancellation", "usage", "approval"],
    "ui-harness/harness-contract.md": ["model API calls", "durable memory", "broad filesystem access"],
    "docs/ui-harness.md": ["local-first", "network calls", "artifacts/private/"],
    "docs/first-usable-product-plan.md": ["normal-use copy/paste relay", "Mock Mode", "Acceptance Criteria"],
    "docs/local-web-harness.md": ["127.0.0.1", "full_architecture", "local/harness/", "Provider mode remains deferred"],
    "ui/local-harness/README.md": ["standard-library", "/api/", "no external", "local/harness/"],
    "templates/full-agent-architecture.md": [
        "UI Harness Recommendation", "Taxonomy Artifact Map",
        "Codex Implementation Prompt", "Powering and Usage Plan",
        "First-Run Checklist",
    ],
}

RUNTIME_REQUEST_FIELDS = {
    "request_id", "session_id", "run_id", "agent_id", "workflow",
    "runtime_mode", "created_at", "context", "privacy_mode", "output_preferences",
}

RUNTIME_RESULT_FIELDS = {
    "request_id", "session_id", "run_id", "agent_id", "workflow",
    "runtime_mode", "status", "started_at", "completed_at", "event_stream_path",
    "run_status_path", "artifact_manifest_path", "artifact_paths", "summary", "warnings",
}

ARCHITECTURE_HEADINGS = [
    "# Agent Architecture: Garden Note Formatter",
    "## 1. Idea Restatement", "## 2. Recommended Pattern",
    "## 3. First Usable Product Scope", "## 4. Taxonomy Artifact Map",
    "## 5. Proposed Repo Structure", "## 6. UI Harness Recommendation",
    "## 7. Key Design Decisions", "## 8. Guardrails and Privacy Notes",
    "## 9. Codex Implementation Prompt", "## 10. Powering and Usage Plan",
    "## 11. First-Run Checklist", "## 12. Iteration Backlog",
]

EXAMPLE_FILES = [
    "examples/README.md",
    "examples/synthetic-clutch.md",
    "examples/synthetic-idea-card.md",
    "examples/synthetic-scorecard.md",
    "examples/synthetic-decision-record.md",
    "examples/synthetic-architecture-brief.md",
    "examples/synthetic-full-architecture.md",
    "examples/synthetic-codex-handoff.md",
]

EXAMPLE_LABEL = "Synthetic public-safe example"

EXAMPLE_TAXONOMY_BUCKETS = [
    "Identity", "Operating style", "Capability modules", "Tools",
    "Knowledge and resources", "Prompts and interfaces", "Memory", "State",
    "Planning and orchestration", "Guardrails and governance",
    "Outputs and schemas", "Evaluation and observability",
    "Runtime and deployment", "Learning and iteration",
]

EXAMPLE_READING_ORDER = [
    "synthetic-clutch.md", "synthetic-idea-card.md", "synthetic-scorecard.md",
    "synthetic-decision-record.md", "synthetic-architecture-brief.md",
    "synthetic-full-architecture.md", "synthetic-codex-handoff.md",
]


def validate_contract(instance: Any, schema: dict[str, Any], label: str) -> list[str]:
    """Validate the contract features used by this repository without dependencies."""
    failures: list[str] = []
    if not isinstance(instance, dict):
        return [f"{label}: expected a JSON object"]

    required = set(schema.get("required", []))
    missing = sorted(required - instance.keys())
    if missing:
        failures.append(f"{label}: missing fields: {', '.join(missing)}")

    properties = schema.get("properties", {})
    if schema.get("additionalProperties") is False:
        extra = sorted(instance.keys() - properties.keys())
        if extra:
            failures.append(f"{label}: unexpected fields: {', '.join(extra)}")

    for name, value in instance.items():
        spec = properties.get(name)
        if not isinstance(spec, dict):
            continue
        allowed_types = spec.get("type")
        if isinstance(allowed_types, str):
            allowed_types = [allowed_types]
        type_checks = {
            "object": lambda item: isinstance(item, dict),
            "array": lambda item: isinstance(item, list),
            "string": lambda item: isinstance(item, str),
            "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
            "boolean": lambda item: isinstance(item, bool),
            "null": lambda item: item is None,
        }
        if allowed_types and not any(type_checks[kind](value) for kind in allowed_types):
            failures.append(f"{label}.{name}: wrong type")
            continue
        if "enum" in spec and value not in spec["enum"]:
            failures.append(f"{label}.{name}: value is outside enum")
        if isinstance(value, str) and len(value) < spec.get("minLength", 0):
            failures.append(f"{label}.{name}: string is too short")
        if isinstance(value, str) and "pattern" in spec and not re.search(spec["pattern"], value):
            failures.append(f"{label}.{name}: string does not match pattern")
        if isinstance(value, str) and spec.get("format") == "date-time":
            try:
                parsed_time = datetime.fromisoformat(value.replace("Z", "+00:00"))
                if parsed_time.tzinfo is None:
                    failures.append(f"{label}.{name}: date-time needs a timezone")
            except ValueError:
                failures.append(f"{label}.{name}: invalid date-time")
        if isinstance(value, int) and not isinstance(value, bool):
            if value < spec.get("minimum", value):
                failures.append(f"{label}.{name}: value is below minimum")
            if value > spec.get("maximum", value):
                failures.append(f"{label}.{name}: value is above maximum")
        if isinstance(value, list):
            if len(value) < spec.get("minItems", 0):
                failures.append(f"{label}.{name}: array has too few items")
            if spec.get("uniqueItems") and len({json.dumps(item, sort_keys=True) for item in value}) != len(value):
                failures.append(f"{label}.{name}: array items are not unique")
            item_spec = spec.get("items", {})
            if isinstance(item_spec, dict):
                item_type = item_spec.get("type")
                for index, item in enumerate(value):
                    item_label = f"{label}.{name}[{index}]"
                    if item_type == "string" and not isinstance(item, str):
                        failures.append(f"{item_label}: expected a string")
                    elif item_type == "object":
                        failures.extend(validate_contract(item, item_spec, item_label))
                    elif isinstance(item, str) and len(item) < item_spec.get("minLength", 0):
                        failures.append(f"{item_label}: string is too short")
        if isinstance(value, dict):
            failures.extend(validate_contract(value, spec, f"{label}.{name}"))
    return failures


def main() -> int:
    failures: list[str] = []

    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    failures.extend(f"missing required file: {name}" for name in missing)

    workflow_name = ".github/workflows/validate.yml"
    try:
        workflow = (ROOT / workflow_name).read_text(encoding="utf-8")
        workflow_casefold = workflow.casefold()
        required_workflow_patterns = {
            "pull_request trigger": r"(?m)^\s*pull_request\s*:",
            "push trigger": r"(?m)^\s*push\s*:",
            "main branch": r"(?m)^\s*-\s*main\s*$",
            "read-only contents permission": r"(?m)^\s*contents\s*:\s*read\s*$",
            "checkout action": r"\bactions/checkout@",
            "Python setup action": r"\bactions/setup-python@",
            "scaffold validator command": r"\bpython\s+scripts/validate_scaffold\.py\b",
        }
        for description, pattern in required_workflow_patterns.items():
            if not re.search(pattern, workflow, flags=re.IGNORECASE):
                failures.append(f"{workflow_name}: missing {description}")

        prohibited_workflow_patterns = {
            "secret reference": r"\bsecrets\s*\.",
            "dependency installation": r"\bpip\s+install\b",
            "Poetry command": r"\bpoetry\b",
            "Pipenv command": r"\bpipenv\b",
            "npm command": r"\bnpm\b",
            "pnpm command": r"\bpnpm\b",
            "Yarn command": r"\byarn\b",
            "curl command": r"\bcurl\b",
            "wget command": r"\bwget\b",
            "Docker command": r"\bdocker\b",
            "deployment command": r"\bdeploy(?:ment)?\b",
            "OpenAI API key": r"\bopenai_api_key\b",
            "Anthropic API key": r"\banthropic_api_key\b",
            "write permission": r"(?m)^\s*(?:contents|actions|checks|deployments|issues|packages|pull-requests|statuses)\s*:\s*write\s*$",
            "write-all permission": r"(?m)^\s*permissions\s*:\s*write-all\s*$",
        }
        for description, pattern in prohibited_workflow_patterns.items():
            if re.search(pattern, workflow_casefold):
                failures.append(f"{workflow_name}: prohibited {description} found")
    except OSError as exc:
        if workflow_name not in missing:
            failures.append(f"{workflow_name}: unreadable: {exc}")

    example_contents: dict[str, str] = {}
    unsafe_example_patterns = {
        "machine-specific Windows path": re.compile(r"(?i)[a-z]:\\users\\[^\s\\]+"),
        "machine-specific Unix home path": re.compile(r"/(?:home|users)/[^/\s]+"),
        "private-data placeholder": re.compile(
            r"(?i)(?:<|\[)(?:real|your)[ _-]?(?:name|address|email|phone|employer|secret)(?:>|\])"
        ),
        "secret-like assignment": re.compile(
            r"(?i)(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*['\"]?[A-Za-z0-9+/=_-]{12,}"
        ),
    }
    for name in EXAMPLE_FILES:
        try:
            content = (ROOT / name).read_text(encoding="utf-8")
            example_contents[name] = content
            if EXAMPLE_LABEL not in content:
                failures.append(f"{name}: missing required synthetic public-safe label")
            for description, pattern in unsafe_example_patterns.items():
                if pattern.search(content):
                    failures.append(f"{name}: possible {description}")
        except OSError as exc:
            if name not in missing:
                failures.append(f"{name}: unreadable: {exc}")

    full_example = example_contents.get("examples/synthetic-full-architecture.md", "")
    for heading in ARCHITECTURE_HEADINGS:
        if heading not in full_example:
            failures.append(f"examples/synthetic-full-architecture.md: missing heading: {heading}")
    for bucket in EXAMPLE_TAXONOMY_BUCKETS:
        if not re.search(rf"(?m)^\|\s*{re.escape(bucket)}\s*\|", full_example):
            failures.append(
                "examples/synthetic-full-architecture.md: missing taxonomy bucket: " + bucket
            )

    handoff = example_contents.get("examples/synthetic-codex-handoff.md", "").casefold()
    for needle in ("codex", "validation commands", "acceptance criteria", "what not to build yet"):
        if needle.casefold() not in handoff:
            failures.append(f"examples/synthetic-codex-handoff.md: missing required content: {needle!r}")

    example_readme = example_contents.get("examples/README.md", "")
    positions = [example_readme.find(name) for name in EXAMPLE_READING_ORDER]
    for name, position in zip(EXAMPLE_READING_ORDER, positions):
        if position < 0:
            failures.append(f"examples/README.md: reading order missing {name}")
    if all(position >= 0 for position in positions) and positions != sorted(positions):
        failures.append("examples/README.md: example files are not in the required reading order")

    for name in ("schemas/idea-card.schema.json", "schemas/decision-record.schema.json"):
        try:
            data = json.loads((ROOT / name).read_text(encoding="utf-8"))
            if not isinstance(data, dict) or data.get("type") != "object":
                failures.append(f"{name}: expected an object schema")
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{name}: invalid JSON: {exc}")

    harness_schemas = [
        "ui-harness/session.schema.json",
        "ui-harness/artifact.schema.json",
        "ui-harness/workflow.schema.json",
        "ui-harness/events.schema.json",
        "ui-harness/agent-profile.schema.json",
        "ui-harness/run-status.schema.json",
        "ui-harness/approval.schema.json",
    ]
    for name in harness_schemas:
        try:
            data = json.loads((ROOT / name).read_text(encoding="utf-8"))
            if not isinstance(data, dict) or data.get("type") != "object":
                failures.append(f"{name}: expected an object schema")
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{name}: invalid JSON: {exc}")

    runtime_schemas: dict[str, dict[str, Any]] = {}
    for name in (
        "runtime/schemas/run-request.schema.json",
        "runtime/schemas/runtime-result.schema.json",
    ):
        try:
            data = json.loads((ROOT / name).read_text(encoding="utf-8"))
            if not isinstance(data, dict) or data.get("type") != "object":
                failures.append(f"{name}: expected an object schema")
            else:
                runtime_schemas[name] = data
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{name}: invalid JSON: {exc}")

    runtime_examples: dict[str, dict[str, Any]] = {}
    example_specs = (
        (
            "runtime/examples/synthetic-run-request.json",
            "runtime/schemas/run-request.schema.json",
            RUNTIME_REQUEST_FIELDS,
        ),
        (
            "runtime/examples/synthetic-runtime-result.json",
            "runtime/schemas/runtime-result.schema.json",
            RUNTIME_RESULT_FIELDS,
        ),
    )
    for name, schema_name, expected_fields in example_specs:
        try:
            data = json.loads((ROOT / name).read_text(encoding="utf-8"))
            runtime_examples[name] = data
            if not isinstance(data, dict):
                failures.append(f"{name}: expected a JSON object")
                continue
            missing_fields = expected_fields - data.keys()
            if missing_fields:
                failures.append(f"{name}: missing fields: {', '.join(sorted(missing_fields))}")
            if schema_name in runtime_schemas:
                failures.extend(validate_contract(data, runtime_schemas[schema_name], name))
            if name.endswith("synthetic-runtime-result.json") and isinstance(data, dict):
                result_paths = [
                    data.get("event_stream_path"), data.get("run_status_path"),
                    data.get("artifact_manifest_path"), *(data.get("artifact_paths") or []),
                ]
                for result_path in result_paths:
                    if not isinstance(result_path, str) or Path(result_path).is_absolute() or ".." in Path(result_path).parts:
                        failures.append(f"{name}: result paths must be relative and stay within the run directory")
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{name}: invalid JSON: {exc}")

    synthetic_path = ROOT / "ui-harness/examples/synthetic-session.json"
    try:
        data = json.loads(synthetic_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            failures.append("ui-harness/examples/synthetic-session.json: expected a JSON object")
        else:
            for field in ("session_id", "workflow", "generated_prompt", "artifacts"):
                if field not in data:
                    failures.append(f"ui-harness/examples/synthetic-session.json: missing field: {field}")
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"ui-harness/examples/synthetic-session.json: invalid JSON: {exc}")

    event_stream_path = ROOT / "ui-harness/examples/sanitized-event-stream.jsonl"
    event_count = 0
    try:
        for line_number, raw_line in enumerate(
            event_stream_path.read_text(encoding="utf-8").splitlines(), 1
        ):
            if not raw_line.strip():
                continue
            event_count += 1
            try:
                event = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                failures.append(
                    f"ui-harness/examples/sanitized-event-stream.jsonl:{line_number}: "
                    f"invalid JSON: {exc}"
                )
                continue
            if not isinstance(event, dict):
                failures.append(
                    f"ui-harness/examples/sanitized-event-stream.jsonl:{line_number}: "
                    "expected a JSON object"
                )
                continue
            missing_fields = EVENT_FIELDS - event.keys()
            if missing_fields:
                failures.append(
                    f"ui-harness/examples/sanitized-event-stream.jsonl:{line_number}: "
                    "missing fields: " + ", ".join(sorted(missing_fields))
                )
        if event_count == 0:
            failures.append("ui-harness/examples/sanitized-event-stream.jsonl: expected at least one event")
    except OSError as exc:
        failures.append(f"ui-harness/examples/sanitized-event-stream.jsonl: unreadable: {exc}")

    eval_path = ROOT / "evals/cases.jsonl"
    eval_count = 0
    try:
        for line_number, raw_line in enumerate(eval_path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw_line.strip():
                continue
            eval_count += 1
            try:
                record = json.loads(raw_line)
            except json.JSONDecodeError as exc:
                failures.append(f"evals/cases.jsonl:{line_number}: invalid JSON: {exc}")
                continue
            missing_fields = EVAL_FIELDS - record.keys()
            if missing_fields:
                failures.append(
                    f"evals/cases.jsonl:{line_number}: missing fields: "
                    + ", ".join(sorted(missing_fields))
                )
        if eval_count < 6:
            failures.append(f"evals/cases.jsonl: expected at least 6 cases, found {eval_count}")
    except OSError as exc:
        failures.append(f"evals/cases.jsonl: unreadable: {exc}")

    for name, needles in CONTENT_CHECKS.items():
        try:
            content = (ROOT / name).read_text(encoding="utf-8").casefold()
        except OSError as exc:
            failures.append(f"{name}: unreadable: {exc}")
            continue
        for needle in needles:
            if needle.casefold() not in content:
                failures.append(f"{name}: missing required content: {needle!r}")

    try:
        ignore_lines = {
            line.strip() for line in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        for rule in sorted(IGNORE_RULES - ignore_lines):
            failures.append(f".gitignore: missing rule: {rule}")
    except OSError as exc:
        failures.append(f".gitignore: unreadable: {exc}")

    frontend_files = (
        "ui/local-harness/index.html",
        "ui/local-harness/app.js",
        "ui/local-harness/styles.css",
    )
    external_resource = re.compile(
        r"(?i)(?:src|href)\s*=\s*['\"]\s*(?:https?:)?//|url\(\s*['\"]?(?:https?:)?//|@import"
    )
    for name in frontend_files:
        try:
            content = (ROOT / name).read_text(encoding="utf-8")
            if external_resource.search(content):
                failures.append(f"{name}: external script, stylesheet, font, or CDN resource found")
        except OSError as exc:
            failures.append(f"{name}: unreadable: {exc}")

    try:
        example_summary = json.loads(
            (ROOT / "ui/local-harness/example-session-summary.json").read_text(encoding="utf-8")
        )
        required_summary = {
            "session_id", "title", "workflow", "created_at", "updated_at",
            "latest_run_id", "artifact_count", "status",
        }
        if not isinstance(example_summary, dict) or required_summary - example_summary.keys():
            failures.append("ui/local-harness/example-session-summary.json: missing session summary fields")
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"ui/local-harness/example-session-summary.json: invalid JSON: {exc}")

    event_schema = json.loads((ROOT / "ui-harness/events.schema.json").read_text(encoding="utf-8"))
    status_schema = json.loads((ROOT / "ui-harness/run-status.schema.json").read_text(encoding="utf-8"))
    artifact_schema = json.loads((ROOT / "ui-harness/artifact.schema.json").read_text(encoding="utf-8"))
    result_schema = runtime_schemas.get("runtime/schemas/runtime-result.schema.json")
    run_parent = ROOT / "local" / "runs"
    run_parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix="scaffold-validation-", dir=run_parent) as temp_dir:
            command = [
                sys.executable,
                str(ROOT / "scripts/run_mock_runtime.py"),
                "--request", str(ROOT / "runtime/examples/synthetic-run-request.json"),
                "--out", temp_dir,
                "--quiet",
            ]
            completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
            if completed.returncode != 0:
                failures.append(
                    "mock runtime validation run failed: "
                    + (completed.stderr.strip() or completed.stdout.strip() or "unknown error")
                )
            else:
                output = Path(temp_dir)
                expected_output = {
                    "session.json", "events.jsonl", "run-status.json", "artifacts.json",
                    "runtime-result.json", "artifacts/full-agent-architecture.md",
                }
                for relative_path in sorted(expected_output):
                    if not (output / relative_path).is_file():
                        failures.append(f"mock runtime: missing output: {relative_path}")

                events_path = output / "events.jsonl"
                if events_path.is_file():
                    emitted_types: list[str] = []
                    for line_number, raw_line in enumerate(events_path.read_text(encoding="utf-8").splitlines(), 1):
                        event = json.loads(raw_line)
                        emitted_types.append(event.get("type", ""))
                        failures.extend(validate_contract(event, event_schema, f"mock events.jsonl:{line_number}"))
                    required_types = {
                        "session.started", "message.created", "plan.proposed",
                        "progress.updated", "artifact.created", "run.completed",
                    }
                    missing_types = required_types - set(emitted_types)
                    if missing_types:
                        failures.append("mock events.jsonl: missing event types: " + ", ".join(sorted(missing_types)))

                status_path = output / "run-status.json"
                if status_path.is_file():
                    status = json.loads(status_path.read_text(encoding="utf-8"))
                    failures.extend(validate_contract(status, status_schema, "mock run-status.json"))
                    if status.get("status") != "completed" or status.get("progress_percent") != 100:
                        failures.append("mock run-status.json: expected completed status at 100 percent")

                artifacts_path = output / "artifacts.json"
                if artifacts_path.is_file():
                    artifacts = json.loads(artifacts_path.read_text(encoding="utf-8"))
                    if not isinstance(artifacts, list) or not artifacts:
                        failures.append("mock artifacts.json: expected a non-empty array")
                    else:
                        for index, artifact in enumerate(artifacts):
                            failures.extend(validate_contract(artifact, artifact_schema, f"mock artifacts.json[{index}]"))

                result_path = output / "runtime-result.json"
                if result_path.is_file() and result_schema:
                    result = json.loads(result_path.read_text(encoding="utf-8"))
                    failures.extend(validate_contract(result, result_schema, "mock runtime-result.json"))
                    emitted_paths = [
                        result.get("event_stream_path"), result.get("run_status_path"),
                        result.get("artifact_manifest_path"), *(result.get("artifact_paths") or []),
                    ]
                    for emitted_path in emitted_paths:
                        if not isinstance(emitted_path, str) or Path(emitted_path).is_absolute() or ".." in Path(emitted_path).parts:
                            failures.append("mock runtime-result.json: paths must be relative and stay within the run directory")

                markdown_path = output / "artifacts/full-agent-architecture.md"
                if markdown_path.is_file():
                    markdown = markdown_path.read_text(encoding="utf-8")
                    for heading in ARCHITECTURE_HEADINGS:
                        if heading not in markdown:
                            failures.append(f"mock architecture: missing heading: {heading}")
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"mock runtime validation error: {exc}")

    smoke_command = [sys.executable, str(ROOT / "scripts/smoke_test_local_harness.py")]
    smoke = subprocess.run(
        smoke_command, cwd=ROOT, capture_output=True, text=True, check=False, timeout=30
    )
    if smoke.returncode != 0:
        failures.append(
            "local harness smoke test failed: "
            + (smoke.stderr.strip() or smoke.stdout.strip() or "unknown error")
        )

    obvious_secret = re.compile(
        r"(?i)(api[_-]?key|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9+/=_-]{16,}"
    )
    for name in REQUIRED_FILES:
        path = ROOT / name
        if not path.is_file() or path.suffix not in {
            ".md", ".json", ".jsonl", ".example", ".py", ".yaml", ".html", ".css", ".js",
        }:
            continue
        text = path.read_text(encoding="utf-8")
        if obvious_secret.search(text):
            failures.append(f"{name}: possible embedded secret; review manually")

    if failures:
        print(f"FAIL: {len(failures)} validation problem(s)")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"PASS: {len(REQUIRED_FILES)} required files present")
    print("PASS: 2 core JSON Schemas parse as JSON")
    print("PASS: 7 harness JSON Schemas parse as JSON")
    print("PASS: 2 runtime JSON Schemas and synthetic request/result examples validate")
    print("PASS: synthetic harness session parses as JSON with required fields")
    print(f"PASS: {event_count} sanitized event records parse and contain required fields")
    print(f"PASS: {eval_count} JSONL eval cases parse and contain required fields")
    print("PASS: deterministic mock run emits contract-compatible files and 12 headings")
    print("PASS: browserless local harness server/API smoke test")
    print("PASS: synthetic example pack labels, safety, reading order, architecture, and handoff")
    print("PASS: local harness frontend has no external resource dependencies")
    print("PASS: GitHub Actions validation workflow is minimal and read-only")
    print("PASS: required content and privacy-oriented ignore rules found")
    print("PASS: no obvious embedded secrets found (manual review still required)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
