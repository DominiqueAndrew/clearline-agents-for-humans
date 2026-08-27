# Clearline science and engineering appendix

Status: 2026-08-27. This appendix separates evidence from product intent. The demo uses synthetic invoices and proves software behavior; it does not claim accounting accuracy, reduced workload in the field, or production readiness.

## Evidence-backed claims

| Product or architecture claim | Evidence | Design consequence |
| --- | --- | --- |
| A professional agent should handle a concrete repetitive workflow and surface only genuine decisions. | [Official Agents for Humans overview](https://agentsforhumans.devpost.com/) and the [official Devpost submission brief](https://agentsforhumans.devpost.com/details) describe background work, real tasks, and human decisions as the target. | Clearline owns one narrow workflow: invoice triage for a small operations or finance team. |
| Human-AI systems should keep people informed and in control, especially when the system can be wrong. | [Amershi et al., “Guidelines for Human-AI Interaction,” CHI 2019](https://doi.org/10.1145/3290605.3300233) proposes 18 guidelines and reports validation with 49 design practitioners across 20 AI products. | Ambiguous invoices remain visible with evidence and an explicit `Approve & file` or `Hold & request info` action. |
| Trustworthiness requires more than an accuracy number; transparency, safety, reliability, and accountability are part of the system. | [NIST AI RMF 1.0](https://doi.org/10.6028/NIST.AI.100-1) identifies valid/reliable, safe, secure/resilient, explainable/interpretable, privacy-enhanced, fair, and accountable/transparent characteristics. | The final gate is deterministic, policy version is shown, writes are local, and the audit feed records automated and human events. |
| Retries must not multiply side effects. | AWS Builders’ Library, [“Making retries safe with idempotent APIs”](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/). | A repeated background sweep recomputes the same policy outcome, preserves human decisions, and does not append duplicate audit events. |
| Agent tools execute with host-process permissions and require an explicit threat model. | Official Strands [Tools Overview](https://strandsagents.com/docs/user-guide/concepts/tools/) documents custom tools and warns that tool code executes with the host process permissions. | The only demo write is a local state/audit update; no payment, email, shell, or vendor tool is exposed. |
| Strands supports a Python agent, custom function tools, and optional Amazon Bedrock providers. | Official Strands [Python quickstart](https://strandsagents.com/docs/user-guide/quickstart/python/) and [quickstart overview](https://strandsagents.com/docs/user-guide/quickstart/overview/). | `StrandsInvoiceAgent` is the agent seam; the default path is credential-free and the live path adds rationale without changing policy status. |

## Policy model

For invoice (i), let `amount_i` be the parsed integer amount in cents, `vendor_i` the normalized vendor, `po_i` the purchase-order value, and `duplicate_i` the duplicate indicator. With policy limits (L = $500) and (P = $250):

```text
safe_i = known_vendor_i
         AND (amount_i <= L)
         AND (amount_i < P OR po_i is present)
         AND (duplicate_i = false)

auto_file_i = 1[safe_i]
needs_review_i = 1 - auto_file_i
```

The model is deliberately a hard gate, not a probability threshold. “Rule coverage” in the UI is a deterministic rule-result indicator; it is not calibrated model confidence. Any missing, conflicting, or suspicious condition fails closed into the human queue.

For a batch of (N) invoices:

```text
auto_file_rate = sum(auto_file_i) / N
processed_value = sum(amount_i * auto_file_i)
```

If future real usage supplies a surfaced-arrival rate (lambda_R) and a median human handling time (t_H), the operational decision-load proxy is:

```text
decision_load = lambda_R * t_H
```

If `W_pending` is the average time a surfaced item waits, Little’s law gives the queue-size relation `N_pending = lambda_R * W_pending` under its usual steady-state assumptions. Clearline does not currently observe these production variables; they are measurement plans, not claimed outcomes.

The error-cost framing is:

```text
expected_cost = c_silent_exception * false_negative
                + c_extra_review * false_positive
```

For this workflow, a silent exception is intentionally treated as more costly than an extra review. The implementation therefore has no probabilistic auto-approval path: only an invoice with zero policy reasons can be filed automatically.

## Reproducible experiments and current results

The tests use eight fixed synthetic invoices: five satisfy every encoded safe condition and three intentionally surface for over-limit, missing-PO, or duplicate evidence. The current local run of `.venv/bin/python -m pytest -q` completed with `15 passed`; runtime duration is intentionally omitted because it varies by host.

| Experiment | Expected invariant | Result recorded by the test suite |
| --- | --- | --- |
| Deterministic policy sweep | 8 total, 5 filed, 3 pending, `$933.00` processed | `tests/test_domain.py` and `tests/test_store.py` |
| Background-worker seam | A store can be constructed without side effects; `BackgroundWorker.run_once()` performs the sweep | `tests/test_store.py` |
| Repeated sweep | Two sweeps keep the same statuses and eight audit events; only the sweep counter advances | `test_repeated_background_sweeps_are_idempotent` |
| Human gate | Approving `inv_1002` produces six filed/two pending; holding `inv_1007` leaves five filed and records one hold | `tests/test_store.py`, `tests/test_server.py` |
| Safety boundary | An automatically filed invoice rejects a human action | `test_automatic_filing_cannot_receive_a_human_action` |
| Restart persistence | A human approval remains after a new store loads the state file and runs a new sweep | `test_human_decision_survives_a_store_restart` |
| Strands fallback | A live-path failure leaves deterministic status intact and records the error | `tests/test_agent.py` |

The latest responsive review also captured and visually inspected the six required viewport artifacts under `/Users/dominique/.codex/visualizations/2026/08/27/01a04367-649a-7441-80cd-018ddd3048c1/clearline/`: `mobile-390x844-v6.png`, `tablet-768x1024-v6.png`, `laptop-1366x768-v6.png`, `desktop-1440x900-v6.png`, `large-desktop-1920x1080-v6.png`, and `wide-desktop-2560x1440-v6.png`. The review found no visible horizontal overflow; the desktop action stayed within the captured frame after the compact-height rule was adjusted.

A fresh loopback HTTP run also verified `/health` = `200`, initial `pending=3/filed=5/sweep_count=1`, approval of `inv_1002` = `pending=2`, a repeated `/api/run` = `pending=2/sweep_count=2/audit_count=9`, and a new server instance restored `approved/pending=2/sweep_count=3/audit_count=9`.

The fixture arithmetic is `5 / 8 = 62.5%` auto-filed and `$933 / $2,087 = 44.7%` of the eight-invoice batch value filed automatically. These are demo-batch descriptors, not accuracy or ROI measurements.

## Limitations and next measurements

- The inbox, fields, vendor policy, and duplicate labels are synthetic; extraction quality against real PDFs or email is unmeasured.
- No causal or user study demonstrates that Clearline reduces time, interruption, or error rate. A useful pilot would compare baseline review time and surfaced decision time against the same invoice sample, with human-labeled exception outcomes and separate train/test periods.
- The current integer rule coverage score is not uncertainty quantification. A production system would need calibrated extraction confidence, provenance for each field, threshold review, and error-cost approval from the customer.
- The optional Bedrock rationale path is construction-tested and fallback-tested, but this repository does not claim a live AWS invocation without the participant’s credentials and model access.
- The demo uses a local JSON state file rather than a multi-user accounting ledger. Concurrency, access control, retention, encryption, and provider SLA behavior remain out of scope.

## Reproduce

From the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pytest -q
.venv/bin/python -m clearline.smoke
node --check clearline/static/app.js
python3 -m compileall -q clearline tests
git diff --check
```

The smoke command returned `Clearline smoke passed` with `8` invoices, `5` filed, `3` pending, `repeat_sweep_audit=8`, `approval_persisted=true`, and `external_side_effects=false`.

The published distribution was also checked separately from the checkout on 2026-08-27. A PEP 517 wheel build produced `clearline-0.1.0-py3-none-any.whl`; that wheel was installed into a fresh virtual environment from a temporary working directory, where `pip check`, the installed `clearline --help` and `python -m clearline --help` entry points, and `python -m clearline.smoke` all passed. The import resolved from temporary `site-packages`, which guards against accidentally testing the editable source tree. The packaged smoke result matched the source result: `8` invoices, `5` filed, `3` pending, `repeat_sweep_audit=8`, `approval_persisted=true`, and `external_side_effects=false`. The wheel manifest includes `clearline/static/index.html`, `styles.css`, and `app.js`; an installed-server `GET /` returned `200` and the Clearline UI, closing the source-versus-distribution gap.

The default server is credential-free:

```bash
CLEARLINE_STATE_FILE=/tmp/clearline-science-demo.json .venv/bin/python -m clearline --port 8787
```

For the optional model rationale path, configure AWS through the normal SDK credential chain and set `CLEARLINE_STRANDS_LIVE=1`. Do not place credentials in the repository. The deterministic safety gate remains authoritative.

## Official hackathon snapshot

The [Devpost Hackathons plugin](https://agentsforhumans.devpost.com/) was queried on 2026-08-27. It returned `submissions_open`, submissions ending at `2026-09-15T00:00:00Z`, a `$40,000` total prize value, solo participation as an available registration choice, and the Professional Agents track. The [official rules](https://agentsforhumans.devpost.com/rules) and [submission requirements](https://agentsforhumans.devpost.com/details) remain the authority for eligibility, agreements, required fields, and final submission. Clearline has not registered, supplied an AWS Builder ID, published a video, or submitted a project through this workstream.

The requirements response accepts `png`, `jpg`, `jpeg`, `pdf`, `ppt`, or `pptx` for the required architecture upload. `docs/architecture.png` is a 2800×940 RGBA PNG rendered from the committed SVG source and visually inspected before this milestone.
