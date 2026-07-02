#!/usr/bin/env python3
"""Exercise the local web harness golden path without a graphical browser."""

from __future__ import annotations

import ast
import json
import re
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "scripts" / "serve_local_harness.py"
HARNESS_ROOT = ROOT / "local" / "harness"
FRONTEND_ROOT = ROOT / "ui" / "local-harness"
ARCHITECTURE_HEADINGS = [
    "## 1. Idea Restatement",
    "## 2. Recommended Pattern",
    "## 3. First Usable Product Scope",
    "## 4. Taxonomy Artifact Map",
    "## 5. Proposed Repo Structure",
    "## 6. UI Harness Recommendation",
    "## 7. Key Design Decisions",
    "## 8. Guardrails and Privacy Notes",
    "## 9. Codex Implementation Prompt",
    "## 10. Powering and Usage Plan",
    "## 11. First-Run Checklist",
    "## 12. Iteration Backlog",
]
ALLOWED_SERVER_IMPORTS = {
    "__future__", "argparse", "datetime", "http", "json", "mimetypes",
    "pathlib", "re", "subprocess", "sys", "typing", "urllib", "uuid",
}


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(("127.0.0.1", 0))
        return int(listener.getsockname()[1])


def request_json(
    base_url: str,
    path: str,
    method: str = "GET",
    body: dict[str, Any] | None = None,
) -> Any:
    payload = None if body is None else json.dumps(body).encode("utf-8")
    request = Request(
        base_url + path,
        data=payload,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    with urlopen(request, timeout=10) as response:
        if response.status not in {200, 201}:
            raise AssertionError(f"{method} {path} returned {response.status}")
        return json.loads(response.read().decode("utf-8"))


def request_text(base_url: str, path: str) -> tuple[int, str, str]:
    with urlopen(base_url + path, timeout=10) as response:
        return (
            response.status,
            response.headers.get_content_type(),
            response.read().decode("utf-8"),
        )


def request_error(base_url: str, path: str) -> tuple[int, dict[str, Any]]:
    try:
        request_json(base_url, path)
    except HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))
    raise AssertionError(f"GET {path} unexpectedly succeeded")


def wait_until_ready(base_url: str, process: subprocess.Popen[str]) -> dict[str, Any]:
    deadline = time.monotonic() + 10
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        if process.poll() is not None:
            break
        try:
            health = request_json(base_url, "/api/health")
            if isinstance(health, dict):
                return health
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
        time.sleep(0.1)
    detail = f": {last_error}" if last_error else ""
    raise AssertionError(f"local harness server did not become ready{detail}")


def assert_dependency_boundary() -> None:
    external_resource = re.compile(
        r"(?i)(?:src|href)\s*=\s*['\"]\s*(?:https?:)?//"
        r"|url\(\s*['\"]?(?:https?:)?//|@import|analytics"
    )
    for name in ("index.html", "app.js", "styles.css"):
        content = (FRONTEND_ROOT / name).read_text(encoding="utf-8")
        if external_resource.search(content):
            raise AssertionError(f"{name} contains an external resource or analytics reference")

    tree = ast.parse(SERVER.read_text(encoding="utf-8"), filename=str(SERVER))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.update(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module.split(".", 1)[0])
    unexpected = sorted(imports - ALLOWED_SERVER_IMPORTS)
    if unexpected:
        raise AssertionError("server has unexpected imports: " + ", ".join(unexpected))


def main() -> int:
    port = free_port()
    base_url = f"http://127.0.0.1:{port}"
    command = [
        sys.executable,
        str(SERVER),
        "--host",
        "127.0.0.1",
        "--port",
        str(port),
    ]
    process = subprocess.Popen(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    session_id: str | None = None
    run_id: str | None = None
    try:
        health = wait_until_ready(base_url, process)
        assert health == {
            "ok": True,
            "runtime_mode": "mock",
            "provider_mode": "deferred",
        }

        workflows = request_json(base_url, "/api/workflows")
        assert isinstance(workflows, list)
        assert any(item.get("workflow") == "full_architecture" for item in workflows)

        missing_status, missing_payload = request_error(
            base_url, "/api/sessions/session-missing-smoke-test"
        )
        assert missing_status == 404
        assert all(missing_payload.get(field) for field in ("error", "action", "retry"))
        assert request_json(base_url, "/api/health")["ok"] is True
        assert isinstance(request_json(base_url, "/api/sessions"), list)

        session = request_json(
            base_url,
            "/api/sessions",
            method="POST",
            body={
                "title": "Garden Note Formatter Smoke Test",
                "idea_name": "Garden Note Formatter",
                "hatch_gate_result": "pass",
                "architecture_brief_summary": (
                    "A fictional local tool formats synthetic garden notes into a reviewable structure."
                ),
                "constraints": [
                    "No network access",
                    "Synthetic public-safe data only",
                    "Human review before consequential use",
                ],
                "workflow": "full_architecture",
            },
        )
        session_id = session["session_id"]

        sessions = request_json(base_url, "/api/sessions")
        assert any(item.get("session_id") == session_id for item in sessions)

        created_run = request_json(
            base_url,
            f"/api/sessions/{session_id}/runs",
            method="POST",
            body={},
        )
        run_id = created_run["runtime_result"]["run_id"]
        run = request_json(base_url, f"/api/sessions/{session_id}/runs/{run_id}")
        assert run["run_status"]["status"] == "completed"
        assert run["run_status"]["progress_percent"] == 100
        assert len(run["events"]) == 6
        assert run["runtime_result"]["runtime_mode"] == "mock"
        assert run["runtime_result"]["workflow"] == "full_architecture"
        assert len(run["artifacts"]) == 1
        artifact = run["artifacts"][0]
        assert artifact["artifact_type"] == "full_architecture"
        assert artifact["should_commit"] is False

        preview = request_json(
            base_url,
            f"/api/sessions/{session_id}/runs/{run_id}/artifacts/{artifact['artifact_id']}",
        )
        markdown = preview["markdown"]
        for heading in ARCHITECTURE_HEADINGS:
            if heading not in markdown:
                raise AssertionError(f"artifact preview is missing heading: {heading}")

        exported = request_json(
            base_url,
            f"/api/sessions/{session_id}/runs/{run_id}/export",
        )
        assert artifact["artifact_id"] in exported["artifact_markdown"]

        static_expectations = {
            "/": ("text/html", "Artifact drawer"),
            "/index.html": ("text/html", "Event timeline"),
            "/app.js": ("text/javascript", "/api/sessions"),
            "/styles.css": ("text/css", ".artifact-layout"),
        }
        for path, (expected_type, marker) in static_expectations.items():
            status, content_type, content = request_text(base_url, path)
            assert status == 200
            assert content_type == expected_type
            assert marker in content

        favicon_status, favicon_type, favicon_content = request_text(base_url, "/favicon.ico")
        assert favicon_status == 204
        assert favicon_type == "image/x-icon"
        assert favicon_content == ""

        app_script = (FRONTEND_ROOT / "app.js").read_text(encoding="utf-8")
        index_markup = (FRONTEND_ROOT / "index.html").read_text(encoding="utf-8")
        styles = (FRONTEND_ROOT / "styles.css").read_text(encoding="utf-8")
        banner_tag = re.search(r'<div\b[^>]*\bid="errorBanner"[^>]*>', index_markup)
        assert banner_tag and re.search(r"\bhidden(?:\s|=|>)", banner_tag.group(0))
        assert re.search(
            r"\[hidden\]\s*\{[^}]*display\s*:\s*none\s*!important\s*;?[^}]*\}",
            styles,
            re.IGNORECASE,
        )
        fragile_startup = "Promise.all([checkHealth(), refreshSessions()]).catch(showError)"
        assert fragile_startup not in app_script
        assert "checkHealth().catch(showError);" in app_script
        assert "refreshSessions().catch(showError);" in app_script
        assert "renderResumeError(error);" in app_script
        assert 'byId("errorBanner").hidden = false;' in app_script
        assert "showError(error);" in app_script
        assert app_script.count("clearError();") >= 8

        assert_dependency_boundary()
        assert (ROOT / "ui" / "hatching-ground.html").is_file()
        ignore_rules = {
            line.strip()
            for line in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        assert "local/harness/" in ignore_rules

        run_root = HARNESS_ROOT / "runs" / session_id / run_id
        assert (HARNESS_ROOT / "sessions" / f"{session_id}.json").is_file()
        assert (run_root / "runtime-request.json").is_file()
        assert (run_root / "output" / "events.jsonl").is_file()
        assert (run_root / "output" / "artifacts" / "full-agent-architecture.md").is_file()

        print("PASS: local harness server started on loopback")
        print("PASS: health, workflows, sessions, mock run, resume, and export endpoints")
        print("PASS: run returned six events, completed status, artifact metadata, and runtime result")
        print("PASS: artifact preview contains all 12 full architecture headings")
        print("PASS: index.html, app.js, and styles.css are served locally")
        print("PASS: hidden error banner stays hidden until real errors invoke showError")
        print("PASS: startup is resilient, favicon is harmless, and API errors stay structured")
        print("PASS: frontend external-resource and server import boundaries")
        print("PASS: generated output stayed below ignored local/harness/")
        print("PASS: static ui/hatching-ground.html fallback remains available")
        return 0
    except (AssertionError, HTTPError, URLError, KeyError, OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    finally:
        process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate(timeout=5)
        if process.returncode not in {0, -15, 1} and stderr:
            print("Server diagnostic: " + stderr.strip().splitlines()[-1], file=sys.stderr)
        if session_id:
            (HARNESS_ROOT / "sessions" / f"{session_id}.json").unlink(missing_ok=True)
            shutil.rmtree(HARNESS_ROOT / "runs" / session_id, ignore_errors=True)
            shutil.rmtree(HARNESS_ROOT / "exports" / session_id, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
