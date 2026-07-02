"use strict";

const state = { sessions: [], selectedSession: null, selectedRun: null, artifactMarkdown: "" };
const byId = (id) => document.getElementById(id);

async function api(path, options = {}) {
  const response = await fetch(path, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = new Error(payload.error || `Request failed with status ${response.status}.`);
    error.action = payload.action || "complete request";
    error.retry = payload.retry || "Refresh and retry.";
    throw error;
  }
  return payload;
}

function showError(error) {
  const message = typeof error?.message === "string" && error.message.trim()
    ? error.message
    : "An unexpected local harness error occurred.";
  const action = typeof error?.action === "string" && error.action.trim()
    ? error.action
    : "complete the requested action";
  const retry = typeof error?.retry === "string" && error.retry.trim()
    ? error.retry
    : "Refresh and retry safely.";
  byId("errorTitle").textContent = `Could not ${action}.`;
  byId("errorMessage").textContent = message;
  byId("errorRetry").textContent = retry;
  byId("errorBanner").hidden = false;
}

function clearError() {
  byId("errorBanner").hidden = true;
  byId("errorMessage").textContent = "";
  byId("errorRetry").textContent = "";
}

function setBusy(busy) {
  byId("createSession").disabled = busy;
  byId("runWorkflow").disabled = busy || !state.selectedSession;
  byId("retryRun").disabled = busy || !state.selectedSession || !state.selectedSession.latest_run_id;
}

function formatTime(value) {
  if (!value) return "—";
  const date = new Date(value);
  return Number.isNaN(date.valueOf()) ? value : date.toLocaleString();
}

function renderSessions() {
  const list = byId("sessionList");
  list.replaceChildren();
  if (!state.sessions.length) {
    list.className = "session-list empty-state";
    list.textContent = "No local sessions yet.";
    return;
  }
  list.className = "session-list";
  for (const session of state.sessions) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `session-item${state.selectedSession?.session_id === session.session_id ? " selected" : ""}`;
    const title = document.createElement("strong");
    title.textContent = session.title;
    const detail = document.createElement("span");
    detail.textContent = `${session.status} · ${session.artifact_count || 0} artifact(s)`;
    const updated = document.createElement("span");
    updated.textContent = formatTime(session.updated_at);
    button.append(title, detail, updated);
    button.addEventListener("click", () => selectSession(session.session_id).catch(showError));
    list.append(button);
  }
}

function fillSessionForm(session) {
  byId("title").value = session.title || "";
  byId("ideaName").value = session.context.idea_name || "";
  byId("hatchGate").value = session.context.hatch_gate_result || "pass";
  byId("briefSummary").value = session.context.architecture_brief_summary || "";
  byId("constraints").value = (session.context.constraints || []).join("\n");
}

async function refreshSessions(preferredId = state.selectedSession?.session_id) {
  state.sessions = await api("/api/sessions");
  renderSessions();
  if (preferredId && state.sessions.some((item) => item.session_id === preferredId)) {
    await selectSession(preferredId);
  } else if (state.sessions.length) {
    await selectSession(state.sessions[0].session_id);
  } else {
    resetRunDisplay();
  }
  clearError();
}

async function selectSession(sessionId) {
  clearError();
  const session = await api(`/api/sessions/${encodeURIComponent(sessionId)}`);
  state.selectedSession = session;
  fillSessionForm(session);
  byId("selectedSessionStatus").textContent = session.status;
  setBusy(false);
  renderSessions();
  if (session.latest_run_id) {
    try {
      await loadRun(session.latest_run_id);
    } catch (error) {
      renderResumeError(error);
    }
  } else {
    resetRunDisplay();
  }
  clearError();
}

function resetRunDisplay() {
  state.selectedRun = null;
  state.artifactMarkdown = "";
  renderStatus(null);
  renderEvents([]);
  renderArtifacts([]);
  byId("exportRun").classList.add("disabled");
  byId("exportRun").removeAttribute("href");
}

function renderResumeError(error) {
  resetRunDisplay();
  const message = typeof error?.message === "string" && error.message.trim()
    ? error.message
    : "The latest run could not be loaded.";
  byId("runStatus").textContent = "Resume unavailable";
  byId("currentStep").textContent = "Load latest run";
  byId("runError").textContent = message;
  byId("eventTimeline").textContent = "The session is available, but its latest run is incomplete or missing. Refresh or retry the mock workflow.";
  byId("artifactList").textContent = "Artifacts from the latest run are unavailable. No local files were changed.";
}

function renderStatus(status) {
  const progress = status?.progress_percent || 0;
  byId("runStatus").textContent = status?.status || "Not started";
  byId("currentStep").textContent = status?.current_step || "—";
  byId("progressPercent").textContent = `${progress}%`;
  byId("progressBar").style.width = `${progress}%`;
  byId("pendingApproval").textContent = status?.pending_approval_id || "None";
  byId("runError").textContent = status?.error_summary || "None";
}

function renderEvents(events) {
  const timeline = byId("eventTimeline");
  byId("eventCount").textContent = `${events.length} event${events.length === 1 ? "" : "s"}`;
  timeline.replaceChildren();
  if (!events.length) {
    timeline.className = "timeline empty-state";
    timeline.textContent = "Run the mock workflow to see user-visible progress.";
    return;
  }
  timeline.className = "timeline";
  for (const event of events) {
    const card = document.createElement("article");
    card.className = "event-card";
    const meta = document.createElement("div");
    meta.className = "event-meta";
    const type = document.createElement("strong");
    type.textContent = event.type;
    const time = document.createElement("span");
    time.textContent = `${formatTime(event.timestamp)} · risk ${event.risk_level}`;
    meta.append(type, time);
    const summary = document.createElement("p");
    summary.textContent = event.human_summary;
    card.append(meta, summary);
    if (event.artifact_ids?.length) {
      const artifacts = document.createElement("div");
      artifacts.className = "event-artifacts";
      artifacts.textContent = `Artifacts: ${event.artifact_ids.join(", ")}`;
      card.append(artifacts);
    }
    timeline.append(card);
  }
}

function artifactUrl(artifactId, download = false) {
  const base = `/api/sessions/${encodeURIComponent(state.selectedSession.session_id)}/runs/${encodeURIComponent(state.selectedRun.runtime_result.run_id)}/artifacts/${encodeURIComponent(artifactId)}`;
  return download ? `${base}?download=1` : base;
}

function renderArtifacts(artifacts) {
  const list = byId("artifactList");
  list.replaceChildren();
  byId("artifactPreview").textContent = "Select an artifact to preview it.";
  byId("previewTitle").textContent = "Markdown preview";
  byId("copyArtifact").disabled = true;
  byId("downloadArtifact").classList.add("disabled");
  byId("downloadArtifact").removeAttribute("href");
  if (!artifacts.length) {
    list.className = "artifact-list empty-state";
    list.textContent = "Generated artifacts will appear here.";
    return;
  }
  list.className = "artifact-list";
  for (const artifact of artifacts) {
    const item = document.createElement("article");
    item.className = "artifact-item";
    const title = document.createElement("strong");
    title.textContent = artifact.title;
    const metadata = document.createElement("p");
    metadata.textContent = `${artifact.filename} · ${artifact.artifact_type}`;
    const privacy = document.createElement("p");
    privacy.textContent = `Privacy: ${artifact.privacy_classification} · Commit: ${artifact.should_commit ? "yes" : "no"}`;
    const actions = document.createElement("div");
    actions.className = "artifact-actions";
    const preview = document.createElement("button");
    preview.type = "button";
    preview.textContent = "Preview";
    preview.addEventListener("click", () => previewArtifact(artifact));
    const download = document.createElement("a");
    download.className = "button-link";
    download.textContent = "Download";
    download.href = artifactUrl(artifact.artifact_id, true);
    actions.append(preview, download);
    item.append(title, metadata, privacy, actions);
    list.append(item);
  }
}

async function previewArtifact(artifact) {
  try {
    const payload = await api(artifactUrl(artifact.artifact_id));
    state.artifactMarkdown = payload.markdown;
    byId("previewTitle").textContent = payload.metadata.title;
    byId("artifactPreview").textContent = payload.markdown;
    byId("copyArtifact").disabled = false;
    byId("downloadArtifact").href = artifactUrl(artifact.artifact_id, true);
    byId("downloadArtifact").classList.remove("disabled");
    clearError();
  } catch (error) { showError(error); }
}

async function loadRun(runId) {
  const run = await api(`/api/sessions/${encodeURIComponent(state.selectedSession.session_id)}/runs/${encodeURIComponent(runId)}`);
  state.selectedRun = run;
  renderStatus(run.run_status);
  renderEvents(run.events);
  renderArtifacts(run.artifacts);
  byId("exportRun").href = `/api/sessions/${encodeURIComponent(state.selectedSession.session_id)}/runs/${encodeURIComponent(runId)}/export`;
  byId("exportRun").classList.remove("disabled");
  clearError();
}

async function createSession(event) {
  event.preventDefault();
  clearError();
  setBusy(true);
  const constraints = byId("constraints").value.split(/\r?\n/).map((item) => item.trim()).filter(Boolean);
  const body = {
    title: byId("title").value,
    workflow: byId("workflow").value,
    idea_name: byId("ideaName").value,
    hatch_gate_result: byId("hatchGate").value,
    architecture_brief_summary: byId("briefSummary").value,
    constraints,
  };
  try {
    const session = await api("/api/sessions", { method: "POST", body: JSON.stringify(body) });
    await refreshSessions(session.session_id);
    clearError();
  } catch (error) {
    showError(error);
  } finally { setBusy(false); }
}

async function runWorkflow() {
  if (!state.selectedSession) return;
  clearError();
  setBusy(true);
  byId("runStatus").textContent = "Running";
  byId("currentStep").textContent = "Invoke mock runtime";
  try {
    const run = await api(`/api/sessions/${encodeURIComponent(state.selectedSession.session_id)}/runs`, { method: "POST", body: "{}" });
    state.selectedRun = run;
    renderStatus(run.run_status);
    renderEvents(run.events);
    renderArtifacts(run.artifacts);
    await refreshSessions(state.selectedSession.session_id);
    clearError();
  } catch (error) {
    showError(error);
    byId("runStatus").textContent = "Failed";
    byId("runError").textContent = error.message;
  } finally { setBusy(false); }
}

function clearForm() {
  state.selectedSession = null;
  byId("sessionForm").reset();
  byId("ideaName").value = "";
  byId("briefSummary").value = "";
  byId("constraints").value = "";
  byId("selectedSessionStatus").textContent = "No session";
  setBusy(false);
  renderSessions();
  resetRunDisplay();
}

async function checkHealth() {
  const badge = byId("healthBadge");
  try {
    const health = await api("/api/health");
    badge.textContent = health.ok ? "Server ready" : "Server unavailable";
    badge.className = `health ${health.ok ? "ok" : "bad"}`;
  } catch (error) {
    badge.textContent = "Server unavailable";
    badge.className = "health bad";
    throw error;
  }
}

byId("sessionForm").addEventListener("submit", createSession);
byId("runWorkflow").addEventListener("click", runWorkflow);
byId("retryRun").addEventListener("click", runWorkflow);
byId("clearForm").addEventListener("click", clearForm);
byId("newSession").addEventListener("click", clearForm);
byId("refreshSessions").addEventListener("click", () => refreshSessions().catch(showError));
byId("dismissError").addEventListener("click", clearError);
byId("copyArtifact").addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(state.artifactMarkdown);
    byId("copyArtifact").textContent = "Copied";
    window.setTimeout(() => { byId("copyArtifact").textContent = "Copy"; }, 1200);
  } catch (error) {
    showError(Object.assign(new Error("Clipboard access was unavailable."), { action: "copy artifact", retry: "Select the preview text and copy it manually." }));
  }
});

checkHealth().catch(showError);
refreshSessions().catch(showError);
