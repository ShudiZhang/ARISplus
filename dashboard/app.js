(function () {
  const RUBRIC_LABELS = {
    originality: "Originality",
    importance: "Importance",
    claims_supported: "Claims Supported",
    experiment_soundness: "Experiment Soundness",
    writing_clarity: "Writing Clarity",
    community_value: "Community Value",
    prior_work_context: "Prior Work Context"
  };

  function text(value, fallback) {
    if (value === undefined || value === null || value === "") return fallback || "not available";
    return String(value);
  }

  function byId(id) {
    return document.getElementById(id);
  }

  function loadData() {
    const script = byId("dashboard-data");
    if (!script) return {};
    try {
      return JSON.parse(script.textContent || "{}");
    } catch (error) {
      return { project: { name: "Dashboard data error", summary: String(error) } };
    }
  }

  function score(value) {
    const number = Number(value);
    if (!Number.isFinite(number)) return "unknown";
    return Number.isInteger(number) ? String(number) : number.toFixed(1);
  }

  function renderWorkflow(data) {
    const target = byId("workflow-list");
    if (!target) return;
    const phases = data.workflow && Array.isArray(data.workflow.phases)
      ? data.workflow.phases
      : [];
    if (!phases.length) {
      target.innerHTML = "<p class=\"muted\">No workflow state available.</p>";
      return;
    }
    target.innerHTML = phases.map((phase) => {
      const status = text(phase.status, "unknown");
      return `
        <div class="phase ${status}">
          <span class="dot"></span>
          <div>
            <strong>${text(phase.label || phase.name, "unknown phase")}</strong>
            <p>${text(phase.summary, "not available")}</p>
          </div>
          <span class="tag">${status}</span>
        </div>
      `;
    }).join("");
  }

  function renderQuality(data) {
    const quality = data.paper_quality || {};
    byId("quality-score").textContent = score(quality.overall_score);
    byId("quality-verdict").textContent =
      `${text(quality.overall_verdict, "unknown")} | confidence: ${text(quality.overall_confidence, "unknown")}`;

    const rubricTarget = byId("rubric-grid");
    const rubric = quality.rubric_scores || {};
    rubricTarget.innerHTML = Object.keys(RUBRIC_LABELS).map((key) => {
      const item = rubric[key] || {};
      return `
        <div class="rubric-item">
          <span>${RUBRIC_LABELS[key]}</span>
          <strong>${score(item.score)}</strong>
          <small>${text(item.minimum_fix, "not available")}</small>
        </div>
      `;
    }).join("");
  }

  function renderSubmission(data) {
    const submission = data.submission || {};
    const status = text(submission.status || submission.overall_status, "unknown");
    const statusEl = byId("submission-status");
    statusEl.textContent = status;
    statusEl.className = `status-pill ${status}`;

    const audits = Array.isArray(submission.audits) ? submission.audits : [];
    byId("audit-list").innerHTML = audits.length ? audits.map((audit) => `
      <div class="list-row">
        <span>${text(audit.name || audit.audit, "audit")}</span>
        <strong>${text(audit.verdict || audit.status, "unknown")}</strong>
      </div>
    `).join("") : "<p class=\"muted\">No audit summary available.</p>";
  }

  function renderArtifacts(data) {
    const artifacts = Array.isArray(data.artifacts) ? data.artifacts : [];
    byId("artifact-list").innerHTML = artifacts.length ? artifacts.slice(0, 8).map((artifact) => `
      <div class="list-row">
        <span>${text(artifact.path || artifact.file, "unknown")}</span>
        <strong>${text(artifact.stage, "artifact")}</strong>
      </div>
    `).join("") : "<p class=\"muted\">No artifacts listed.</p>";
  }

  function renderExperiments(data) {
    const experiments = data.experiments || {};
    const counts = experiments.counts || experiments;
    const keys = ["queued", "running", "completed", "failed", "unknown"];
    byId("experiment-summary").innerHTML = keys.map((key) => `
      <div class="metric">
        <strong>${text(counts[key], "0")}</strong>
        <span>${key}</span>
      </div>
    `).join("");
  }

  function render() {
    const data = loadData();
    const project = data.project || {};
    byId("project-title").textContent = text(project.name, "ARIS Research Dashboard");
    byId("project-summary").textContent = text(project.summary, "Static view of ARIS workflow state.");
    renderWorkflow(data);
    renderQuality(data);
    renderSubmission(data);
    renderArtifacts(data);
    renderExperiments(data);
  }

  render();
})();

