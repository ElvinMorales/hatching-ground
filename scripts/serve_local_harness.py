#!/usr/bin/env python3
"""Serve the standard-library-only Hatching Ground local mock harness."""

from __future__ import annotations

import argparse
import json
import mimetypes
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
STATIC_ROOT = (ROOT / "ui" / "local-harness").resolve()
HARNESS_ROOT = (ROOT / "local" / "harness").resolve()
SESSIONS_ROOT = HARNESS_ROOT / "sessions"
RUNS_ROOT = HARNESS_ROOT / "runs"
EXPORTS_ROOT = HARNESS_ROOT / "exports"
MOCK_RUNNER = ROOT / "scripts" / "run_mock_runtime.py"
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}$")
MAX_BODY_BYTES = 64 * 1024

WORKFLOWS = [
    {
        "workflow": "full_architecture",
        "display_name": "Full Architecture",
        "description": "Create a synthetic 12-section full architecture artifact through the mock runtime.",
        "runtime_mode": "mock",
    }
]


class ApiError(Exception):
    def __init__(self, status: HTTPStatus, message: str, action: str, retry: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message
        self.action = action
        self.retry = retry


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require_id(value: str, label: str) -> str:
    if not ID_PATTERN.fullmatch(value):
        raise ApiError(
            HTTPStatus.BAD_REQUEST,
            f"Invalid {label}.",
            f"read {label}",
            "Refresh the session list and try again.",
        )
    return value


def session_path(session_id: str) -> Path:
    return SESSIONS_ROOT / f"{require_id(session_id, 'session ID')}.json"


def load_session(session_id: str) -> dict[str, Any]:
    path = session_path(session_id)
    if not path.is_file():
        raise ApiError(
            HTTPStatus.NOT_FOUND,
            "Session not found.",
            "load session",
            "Refresh the session list or create a new session.",
        )
    value = read_json(path)
    if not isinstance(value, dict):
        raise ApiError(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            "The local session record is invalid.",
            "load session",
            "Remove the affected local session file and create a new session.",
        )
    return value


def run_paths(session_id: str, run_id: str) -> tuple[Path, Path]:
    require_id(session_id, "session ID")
    require_id(run_id, "run ID")
    run_root = RUNS_ROOT / session_id / run_id
    return run_root, run_root / "output"


def session_summary(session: dict[str, Any]) -> dict[str, Any]:
    return {
        key: session.get(key)
        for key in (
            "session_id", "title", "workflow", "created_at", "updated_at",
            "latest_run_id", "artifact_count", "status",
        )
    }


def load_events(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if raw_line.strip():
            value = json.loads(raw_line)
            if isinstance(value, dict):
                events.append(value)
    return events


def load_run(session: dict[str, Any], run_id: str) -> dict[str, Any]:
    run_root, output = run_paths(session["session_id"], run_id)
    known_runs = {item.get("run_id") for item in session.get("runs", []) if isinstance(item, dict)}
    required = [
        run_root / "runtime-request.json", output / "runtime-result.json",
        output / "events.jsonl", output / "run-status.json", output / "artifacts.json",
    ]
    if run_id not in known_runs or not all(path.is_file() for path in required):
        raise ApiError(
            HTTPStatus.NOT_FOUND,
            "Run not found or its output is incomplete.",
            "load run",
            "Refresh the session and run the mock workflow again.",
        )
    artifacts = read_json(output / "artifacts.json")
    previews = [
        {
            "artifact_id": item.get("artifact_id"),
            "title": item.get("title"),
            "content_summary": item.get("content_summary"),
        }
        for item in artifacts
        if isinstance(item, dict)
    ]
    return {
        "session": session_summary(session),
        "runtime_result": read_json(output / "runtime-result.json"),
        "events": load_events(output / "events.jsonl"),
        "run_status": read_json(output / "run-status.json"),
        "artifacts": artifacts,
        "artifact_previews": previews,
    }


def find_artifact(session: dict[str, Any], run_id: str, artifact_id: str) -> tuple[dict[str, Any], Path]:
    require_id(artifact_id, "artifact ID")
    run = load_run(session, run_id)
    _, output = run_paths(session["session_id"], run_id)
    for artifact in run["artifacts"]:
        if not isinstance(artifact, dict) or artifact.get("artifact_id") != artifact_id:
            continue
        filename = artifact.get("filename")
        if not isinstance(filename, str) or Path(filename).name != filename:
            break
        content_path = (output / "artifacts" / filename).resolve()
        artifacts_root = (output / "artifacts").resolve()
        if artifacts_root not in content_path.parents or not content_path.is_file():
            break
        return artifact, content_path
    raise ApiError(
        HTTPStatus.NOT_FOUND,
        "Artifact not found.",
        "load artifact",
        "Refresh the run details and select an artifact from the drawer.",
    )


def validate_session_input(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("Request body must be a JSON object.")
    allowed = {"title", "idea_name", "hatch_gate_result", "architecture_brief_summary", "constraints", "workflow"}
    if set(value) - allowed:
        raise ValueError("Request contains unsupported fields.")
    workflow = value.get("workflow", "full_architecture")
    idea_name = value.get("idea_name")
    gate = value.get("hatch_gate_result")
    summary = value.get("architecture_brief_summary")
    constraints = value.get("constraints")
    if workflow != "full_architecture":
        raise ValueError("Only the full_architecture workflow is supported.")
    if not isinstance(idea_name, str) or not idea_name.strip():
        raise ValueError("Idea name is required.")
    if gate not in {"pass", "conditional-pass"}:
        raise ValueError("Hatch gate result must be pass or conditional-pass.")
    if not isinstance(summary, str) or not summary.strip():
        raise ValueError("Architecture brief summary is required.")
    if not isinstance(constraints, list) or not constraints or not all(
        isinstance(item, str) and item.strip() for item in constraints
    ):
        raise ValueError("Provide at least one non-empty constraint.")
    title = value.get("title")
    if title is not None and (not isinstance(title, str) or len(title.strip()) > 120):
        raise ValueError("Title must be at most 120 characters.")
    for field, text in (("idea name", idea_name), ("architecture summary", summary)):
        if len(text.strip()) > 4000:
            raise ValueError(f"The {field} is too long.")
    if len(constraints) > 50 or any(len(item.strip()) > 1000 for item in constraints):
        raise ValueError("Constraints are too large.")
    return {
        "title": title.strip() if isinstance(title, str) and title.strip() else idea_name.strip(),
        "workflow": workflow,
        "context": {
            "idea_name": idea_name.strip(),
            "hatch_gate_result": gate,
            "architecture_brief_summary": summary.strip(),
            "constraints": [item.strip() for item in constraints],
        },
    }


def create_session(value: Any) -> dict[str, Any]:
    data = validate_session_input(value)
    now = utc_now()
    session_id = f"session-{uuid.uuid4().hex}"
    session = {
        "session_id": session_id,
        "title": data["title"],
        "workflow": data["workflow"],
        "runtime_mode": "mock",
        "created_at": now,
        "updated_at": now,
        "context": data["context"],
        "runs": [],
        "latest_run_id": None,
        "artifact_ids": [],
        "artifact_count": 0,
        "status": "ready",
    }
    write_json(session_path(session_id), session)
    return session_summary(session)


def execute_run(session: dict[str, Any]) -> dict[str, Any]:
    run_id = f"run-{uuid.uuid4().hex}"
    request_id = f"request-{uuid.uuid4().hex}"
    created_at = utc_now()
    run_root, output = run_paths(session["session_id"], run_id)
    request = {
        "request_id": request_id,
        "session_id": session["session_id"],
        "run_id": run_id,
        "agent_id": "hatching-ground-mock",
        "workflow": "full_architecture",
        "runtime_mode": "mock",
        "created_at": created_at,
        "context": {
            **session["context"],
            "desired_artifact_type": "full_architecture",
        },
        "privacy_mode": "synthetic-public-safe",
        "output_preferences": {"format": "markdown", "filename": "full-agent-architecture.md"},
    }
    run_root.mkdir(parents=True, exist_ok=False)
    request_path = run_root / "runtime-request.json"
    write_json(request_path, request)
    command = [
        sys.executable, str(MOCK_RUNNER), "--request", str(request_path),
        "--out", str(output), "--reset", "--quiet",
    ]
    completed = subprocess.run(
        command, cwd=ROOT, capture_output=True, text=True, check=False, timeout=60
    )
    if completed.returncode != 0:
        session["updated_at"] = utc_now()
        session["latest_run_id"] = run_id
        session["status"] = "failed"
        session["runs"].append({"run_id": run_id, "created_at": created_at, "status": "failed", "artifact_ids": []})
        write_json(session_path(session["session_id"]), session)
        raise ApiError(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            "The mock runtime did not complete.",
            "run mock workflow",
            "Review the concise server diagnostic, then retry the run.",
        )
    artifacts = read_json(output / "artifacts.json")
    artifact_ids = [item["artifact_id"] for item in artifacts if isinstance(item, dict) and isinstance(item.get("artifact_id"), str)]
    session["updated_at"] = utc_now()
    session["latest_run_id"] = run_id
    session["artifact_ids"] = list(dict.fromkeys([*session.get("artifact_ids", []), *artifact_ids]))
    session["artifact_count"] = len(session["artifact_ids"])
    session["status"] = "completed"
    session["runs"].append({"run_id": run_id, "created_at": created_at, "status": "completed", "artifact_ids": artifact_ids})
    write_json(session_path(session["session_id"]), session)
    return load_run(session, run_id)


class HarnessHandler(BaseHTTPRequestHandler):
    server_version = "HatchingGroundLocal/1.0"

    def log_message(self, format_string: str, *args: Any) -> None:
        # Request paths and status only; request bodies and session context are never logged.
        sys.stderr.write("local harness: " + format_string % args + "\n")

    def send_bytes(
        self,
        body: bytes,
        content_type: str,
        status: HTTPStatus = HTTPStatus.OK,
        disposition: str | None = None,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'")
        if disposition:
            self.send_header("Content-Disposition", disposition)
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, value: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        self.send_bytes((json.dumps(value, indent=2) + "\n").encode(), "application/json; charset=utf-8", status)

    def send_error_json(self, error: ApiError) -> None:
        self.send_json(
            {"ok": False, "error": error.message, "action": error.action, "retry": error.retry},
            error.status,
        )

    def read_body(self) -> Any:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "Invalid request length.", "read request", "Retry with valid JSON.") from exc
        if length <= 0 or length > MAX_BODY_BYTES:
            raise ApiError(HTTPStatus.BAD_REQUEST, "Request body is empty or too large.", "read request", "Use the form with concise synthetic context and retry.")
        try:
            return json.loads(self.rfile.read(length))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "Request body is not valid JSON.", "read request", "Correct the form data and retry.") from exc

    def route_parts(self) -> tuple[list[str], dict[str, list[str]]]:
        parsed = urlparse(self.path)
        return [unquote(part) for part in parsed.path.split("/") if part], parse_qs(parsed.query)

    def do_GET(self) -> None:  # noqa: N802
        try:
            parts, query = self.route_parts()
            if parts and parts[0] == "api":
                self.handle_api_get(parts[1:], query)
            else:
                self.serve_static(parts)
        except ApiError as exc:
            self.send_error_json(exc)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"local harness diagnostic: {type(exc).__name__}", file=sys.stderr)
            self.send_error_json(ApiError(HTTPStatus.INTERNAL_SERVER_ERROR, "A local harness file could not be read.", "read local harness data", "Refresh and retry. If the problem persists, remove the affected local session."))

    def do_POST(self) -> None:  # noqa: N802
        try:
            parts, _ = self.route_parts()
            if parts == ["api", "sessions"]:
                try:
                    session = create_session(self.read_body())
                except ValueError as exc:
                    raise ApiError(HTTPStatus.BAD_REQUEST, str(exc), "create session", "Correct the synthetic context and retry.") from exc
                self.send_json(session, HTTPStatus.CREATED)
                return
            if len(parts) == 4 and parts[:2] == ["api", "sessions"] and parts[3] == "runs":
                session = load_session(parts[2])
                self.send_json(execute_run(session), HTTPStatus.CREATED)
                return
            raise ApiError(HTTPStatus.NOT_FOUND, "API endpoint not found.", "route request", "Refresh the page and retry.")
        except ApiError as exc:
            self.send_error_json(exc)
        except subprocess.TimeoutExpired:
            self.send_error_json(ApiError(HTTPStatus.GATEWAY_TIMEOUT, "The mock runtime timed out.", "run mock workflow", "Retry once; if it repeats, run the mock runtime validation command."))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"local harness diagnostic: {type(exc).__name__}", file=sys.stderr)
            self.send_error_json(ApiError(HTTPStatus.INTERNAL_SERVER_ERROR, "The local operation failed.", "update local harness data", "Refresh and retry safely."))

    def handle_api_get(self, parts: list[str], query: dict[str, list[str]]) -> None:
        if parts == ["health"]:
            self.send_json({"ok": True, "runtime_mode": "mock", "provider_mode": "deferred"})
            return
        if parts == ["workflows"]:
            self.send_json(WORKFLOWS)
            return
        if parts == ["sessions"]:
            SESSIONS_ROOT.mkdir(parents=True, exist_ok=True)
            sessions = []
            for path in sorted(SESSIONS_ROOT.glob("session-*.json")):
                value = read_json(path)
                if isinstance(value, dict):
                    sessions.append(session_summary(value))
            sessions.sort(key=lambda item: item.get("updated_at") or "", reverse=True)
            self.send_json(sessions)
            return
        if len(parts) >= 2 and parts[0] == "sessions":
            session = load_session(parts[1])
            if len(parts) == 2:
                self.send_json(session)
                return
            if len(parts) >= 4 and parts[2] == "runs":
                run_id = parts[3]
                if len(parts) == 4:
                    self.send_json(load_run(session, run_id))
                    return
                if len(parts) == 6 and parts[4] == "artifacts":
                    artifact, content_path = find_artifact(session, run_id, parts[5])
                    payload = {"metadata": artifact, "markdown": content_path.read_text(encoding="utf-8")}
                    if query.get("download") == ["1"]:
                        self.send_bytes(content_path.read_bytes(), "text/markdown; charset=utf-8", disposition=f'attachment; filename="{artifact["filename"]}"')
                    else:
                        self.send_json(payload)
                    return
                if len(parts) == 5 and parts[4] == "export":
                    run = load_run(session, run_id)
                    bundle = {**run, "artifact_markdown": {}}
                    for artifact in run["artifacts"]:
                        if isinstance(artifact, dict):
                            _, content_path = find_artifact(session, run_id, artifact["artifact_id"])
                            bundle["artifact_markdown"][artifact["artifact_id"]] = content_path.read_text(encoding="utf-8")
                    export_path = EXPORTS_ROOT / session["session_id"] / f"{run_id}.json"
                    write_json(export_path, bundle)
                    body = (json.dumps(bundle, indent=2) + "\n").encode()
                    self.send_bytes(body, "application/json; charset=utf-8", disposition=f'attachment; filename="{run_id}-export.json"')
                    return
        raise ApiError(HTTPStatus.NOT_FOUND, "API endpoint not found.", "route request", "Refresh the page and retry.")

    def serve_static(self, parts: list[str]) -> None:
        if parts == ["favicon.ico"]:
            self.send_bytes(b"", "image/x-icon", HTTPStatus.NO_CONTENT)
            return
        relative = Path("index.html") if not parts else Path(*parts)
        candidate = (STATIC_ROOT / relative).resolve()
        if STATIC_ROOT not in candidate.parents or not candidate.is_file():
            raise ApiError(HTTPStatus.NOT_FOUND, "Page not found.", "load interface", "Return to the local harness home page.")
        content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        if content_type.startswith("text/") or content_type in {"application/javascript", "application/json"}:
            content_type += "; charset=utf-8"
        self.send_bytes(candidate.read_bytes(), content_type)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1)")
    parser.add_argument("--port", default=8765, type=int, help="Bind port (default: 8765)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not STATIC_ROOT.is_dir():
        print("ERROR: ui/local-harness/ is missing", file=sys.stderr)
        return 1
    SESSIONS_ROOT.mkdir(parents=True, exist_ok=True)
    RUNS_ROOT.mkdir(parents=True, exist_ok=True)
    EXPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    try:
        server = ThreadingHTTPServer((args.host, args.port), HarnessHandler)
    except OSError as exc:
        print(f"ERROR: could not start local harness: {exc}", file=sys.stderr)
        return 1
    print(f"Hatching Ground local harness: http://{args.host}:{args.port}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
