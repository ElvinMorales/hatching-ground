#!/usr/bin/env python3
"""Validate the Hatching Ground documentation scaffold using the standard library."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md", "AGENTS.md", ".gitignore",
    "agent/identity.md", "agent/operating-style.md",
    "prompts/starter-prompts.md",
    "workflows/idea-discovery.md", "workflows/idea-intake.md",
    "workflows/incubation-scorecard.md", "workflows/hatching-workflow.md",
    "templates/idea-card.md", "templates/architecture-brief.md",
    "templates/codex-handoff.md", "schemas/idea-card.schema.json",
    "schemas/decision-record.schema.json", "guardrails/privacy-policy.md",
    "guardrails/public-private-boundary.md", "runtime/README.md",
    "runtime/.env.example", "evals/rubric.md", "evals/cases.jsonl",
    "docs/setup.md", "docs/usage.md", "docs/maintenance.md",
    "scripts/validate_scaffold.py",
]

EVAL_FIELDS = {
    "case_name", "user_input", "expected_behavior", "must_include",
    "must_avoid", "pass_fail_notes",
}

IGNORE_RULES = {
    ".env", ".env.*", "!.env.example", "local/", "private/",
    "data/private/", "data/local/", "memory/private/", "state/private/",
    "logs/", "runtime/private/", "runtime/logs/", "*.log",
}

CONTENT_CHECKS = {
    "README.md": ["Hatching Ground", "Discover ideas", "Codex handoff", "Never commit"],
    "AGENTS.md": ["artifact-first", "synthetic examples only", "runtime integrations"],
    "guardrails/public-private-boundary.md": ["Private-only", "Public-safe", "Potentially publishable later"],
    "workflows/hatching-workflow.md": ["Smallest useful version is clear", "No high-risk automation"],
    "runtime/README.md": ["local-first", "not part of this MVP", "least privilege"],
}


def main() -> int:
    failures: list[str] = []

    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    failures.extend(f"missing required file: {name}" for name in missing)

    for name in ("schemas/idea-card.schema.json", "schemas/decision-record.schema.json"):
        try:
            data = json.loads((ROOT / name).read_text(encoding="utf-8"))
            if not isinstance(data, dict) or data.get("type") != "object":
                failures.append(f"{name}: expected an object schema")
        except (OSError, json.JSONDecodeError) as exc:
            failures.append(f"{name}: invalid JSON: {exc}")

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

    obvious_secret = re.compile(
        r"(?i)(api[_-]?key|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9+/=_-]{16,}"
    )
    for name in REQUIRED_FILES:
        path = ROOT / name
        if not path.is_file() or path.suffix not in {".md", ".json", ".jsonl", ".example"}:
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
    print("PASS: 2 JSON Schemas parse as JSON")
    print(f"PASS: {eval_count} JSONL eval cases parse and contain required fields")
    print("PASS: required content and privacy-oriented ignore rules found")
    print("PASS: no obvious embedded secrets found (manual review still required)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
