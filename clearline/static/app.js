const app = {
  state: null,
  selectedId: "inv_1002",
  filter: "all",
};

const $ = (selector) => document.querySelector(selector);
const money = (cents, currency = "USD") => `${currency === "USD" ? "$" : currency + " "}${(cents / 100).toLocaleString("en-US", { minimumFractionDigits: 0, maximumFractionDigits: 2 })}`;
const escapeHtml = (value) => String(value).replace(/[&<>'"]/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[char]));
const initials = (name) => name.split(/\s+/).map((part) => part[0]).slice(0, 2).join("").toUpperCase();

function statusMeta(status) {
  return {
    auto_filed: ["Filed automatically", "auto"],
    needs_review: ["Needs your call", "review"],
    approved: ["Approved by you", "resolved"],
    on_hold: ["On hold", "hold"],
  }[status] || [status, "review"];
}

function relativeTime(timestamp) {
  if (!timestamp) return "waiting for first sweep";
  const date = new Date(timestamp);
  if (Number.isNaN(date.getTime())) return timestamp;
  return `at ${date.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" })}`;
}

async function request(path, options = {}) {
  const response = await fetch(path, { headers: { "Content-Type": "application/json" }, ...options });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || "Request failed");
  return payload;
}

function render() {
  const { state } = app;
  if (!state) return;
  const stats = state.stats;
  $("#mode-label").textContent = `${state.sdk.replace(/^AWS /, "")} · ${state.mode}`;
  const decisionLabel = stats.pending === 1 ? "decision needs" : "decisions need";
  $("#hero-subtitle").textContent = `Your invoice stream is clear. ${stats.pending} ${decisionLabel} a human eye.`;
  $("#nav-pending").textContent = stats.pending;
  $("#stat-pending").textContent = stats.pending;
  $("#stat-filed").textContent = stats.filed;
  $("#stat-value").textContent = money(stats.processed_cents);
  $("#policy-version").textContent = state.policy.version;
  $("#policy-limit").textContent = state.policy.auto_file_limit.replace("USD ", "");
  $("#po-limit").textContent = state.policy.po_required_over.replace("USD ", "");
  $("#footer-policy").textContent = state.policy.version;
  $("#last-sweep").textContent = state.last_sweep ? `Last checked ${relativeTime(state.last_sweep)}` : "Starting background worker";
  $("#sweep-status").textContent = state.last_sweep ? "Complete" : "Starting";
  $("#queue-count").textContent = `${stats.total} invoices`;
  $("#all-count").textContent = stats.total;
  $("#needs-count").textContent = stats.pending;
  $("#filed-count").textContent = stats.filed;
  renderQueue();
  renderDetail();
  renderAudit();
}

function renderQueue() {
  const invoices = app.state.invoices.filter((invoice) => app.filter === "all" || invoice.decision.status === app.filter);
  $("#invoice-list").innerHTML = invoices.length ? invoices.map((invoice) => {
    const [label, tone] = statusMeta(invoice.decision.status);
    const selected = invoice.id === app.selectedId ? " selected" : "";
    return `<article class="invoice-row${selected}" data-id="${escapeHtml(invoice.id)}" tabindex="0" role="button" aria-label="Open ${escapeHtml(invoice.vendor)} invoice">
      <div class="vendor-icon ${tone === "review" ? "review" : ""}">${escapeHtml(initials(invoice.vendor))}</div>
      <div class="row-main"><div class="vendor-line"><strong>${escapeHtml(invoice.vendor)}</strong><span class="invoice-number">${escapeHtml(invoice.invoice_number)}</span></div><div class="invoice-description">${escapeHtml(invoice.description)}</div></div>
      <div class="row-right"><strong>${money(invoice.amount_cents, invoice.currency)}</strong><small class="status-text ${tone}">${escapeHtml(label)}</small></div>
    </article>`;
  }).join("") : `<div class="empty-audit">Nothing in this view. Clearline is keeping the rest quiet.</div>`;
  document.querySelectorAll(".invoice-row").forEach((row) => {
    row.addEventListener("click", () => { app.selectedId = row.dataset.id; renderQueue(); renderDetail(); });
    row.addEventListener("keydown", (event) => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); app.selectedId = row.dataset.id; renderQueue(); renderDetail(); } });
  });
}

function renderDetail() {
  const invoice = app.state.invoices.find((item) => item.id === app.selectedId) || app.state.invoices[0];
  if (!invoice) return;
  app.selectedId = invoice.id;
  const decision = invoice.decision;
  const [label, tone] = statusMeta(decision.status);
  const isPending = decision.status === "needs_review";
  const calloutClass = isPending ? "" : tone === "hold" ? " hold" : " resolved";
  const reasons = decision.reasons.length ? `<div class="reason-block"><div class="evidence-heading">WHY IT SURFACED</div>${decision.reasons.map((reason) => `<div class="reason-item"><span class="reason-symbol">!</span><div><strong>${escapeHtml(reason.label)}</strong><span>${escapeHtml(reason.detail)}</span></div></div>`).join("")}</div>` : "";
  const actions = isPending ? `<div class="action-row"><button class="action-button primary" data-action="approve">Approve &amp; file</button><button class="action-button secondary" data-action="hold">Hold &amp; request info</button></div>` : `<div class="resolved-note"><strong>${escapeHtml(label)}</strong> · recorded by ${escapeHtml(decision.decided_by)} ${relativeTime(decision.decided_at)}. No external action was taken.</div>`;
  $("#detail-panel").innerHTML = `<div class="detail-header"><div><span class="badge badge-${tone === "review" ? "review" : tone === "hold" ? "hold" : tone === "resolved" ? "approved" : "auto"}">${escapeHtml(label)}</span><h3>${escapeHtml(invoice.vendor)}</h3><p class="detail-number">${escapeHtml(invoice.invoice_number)} · due ${escapeHtml(invoice.due_date)}</p></div><strong class="detail-amount">${money(invoice.amount_cents, invoice.currency)}</strong></div>
    <p class="detail-description">${escapeHtml(invoice.description)}</p>
    <div class="decision-callout${calloutClass}"><span class="callout-label">${isPending ? "CLEARLINE RECOMMENDS" : "DECISION RECORDED"}</span><strong>${escapeHtml(decision.recommendation)}</strong><p>${isPending ? "The policy gate kept this out of the ledger until you decide." : "This case is now out of the pending queue."}</p><span class="provenance-note">Decision source · policy ${escapeHtml(app.state.policy.version)}</span></div>
    <div class="evidence-heading"><span>EVIDENCE COLLECTED</span><span class="confidence">${decision.confidence}% rule coverage</span></div>
    <ul class="evidence-list">${decision.evidence.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}</ul>${reasons}${decision.rationale ? `<div class="reason-block"><div class="evidence-heading">STRANDS RATIONALE</div><p class="detail-description">${escapeHtml(decision.rationale)}</p></div>` : ""}${actions}`;
  document.querySelectorAll("[data-action]").forEach((button) => button.addEventListener("click", () => decide(button.dataset.action)));
}

function renderAudit() {
  const events = app.state.audit || [];
  $("#audit-list").innerHTML = events.length ? events.slice(0, 6).map((event) => `<div class="audit-event ${escapeHtml(event.kind)}"><span class="event-mark">${event.kind === "human" ? "✓" : "✦"}</span><div><p>${escapeHtml(event.message)}</p><time>${relativeTime(event.timestamp)}</time></div></div>`).join("") : `<div class="empty-audit">The audit trail will appear after the first background sweep.</div>`;
}

async function decide(action) {
  const button = document.querySelector(`[data-action="${action}"]`);
  if (button) { button.disabled = true; button.textContent = "Saving…"; }
  try {
    app.state = await request(`/api/invoices/${encodeURIComponent(app.selectedId)}/decision`, { method: "POST", body: JSON.stringify({ action }) });
    render();
  } catch (error) {
    if (button) { button.disabled = false; button.textContent = action === "approve" ? "Approve & file" : "Hold & request info"; }
    window.alert(error.message);
  }
}

async function runSweep() {
  const button = $("#run-sweep");
  button.classList.add("spinning"); button.disabled = true;
  try { app.state = await request("/api/run", { method: "POST" }); render(); }
  finally { button.classList.remove("spinning"); button.disabled = false; }
}

document.querySelectorAll("[data-filter]").forEach((button) => button.addEventListener("click", () => {
  app.filter = button.dataset.filter;
  document.querySelectorAll("[data-filter]").forEach((item) => item.classList.toggle("active", item === button));
  renderQueue();
}));
$("#run-sweep").addEventListener("click", runSweep);
request("/api/state").then((state) => { app.state = state; render(); }).catch((error) => { $("#invoice-list").innerHTML = `<div class="empty-audit">Could not connect to Clearline: ${escapeHtml(error.message)}</div>`; });
