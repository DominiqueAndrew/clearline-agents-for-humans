# Clearline judge brief

## One sentence

Clearline is a quiet invoice-approval queue for small professional teams: a background Strands agent files routine invoices locally and surfaces only the exceptions that require a human decision.

## Why Professional Agents

The user is an operations or finance lead who is capable of judging an invoice but should not have to inspect every routine item. Clearline removes the repetitive scan while preserving the judgment boundary. The demo is intentionally one complete workflow, not a collection of half-built integrations.

## Rubric mapping from the official Devpost snapshot

| Criterion | What the judge can verify in Clearline |
| --- | --- |
| Technological Implementation | `StrandsInvoiceAgent` is a real Python SDK adapter; the top bar names `Strands Agents SDK` in both demo and live-rationale modes; `BackgroundWorker` separates scheduling from policy state; policy tools produce structured evidence; tests exercise deterministic, live-rationale, fallback, persistence, and repeat-sweep behavior. |
| Design | The screen opens on a queue, not a chat. It shows the three-way operational state—filed, needs your call, on hold—and a focused evidence panel with a human action. Responsive review covers mobile, tablet, laptop, desktop, large desktop, and wide desktop. |
| Potential Impact | The audience and repetitive task are specific. The demo shows five routine invoices disappear into a local ledger while three meaningful exceptions remain. It does not claim production savings from synthetic data. |
| Creativity & Originality | The wedge is decision-budget protection: automation is measured by the quality of interruptions it removes, not by making approval invisible. The hard safety boundary is part of the product, not an afterthought. |
| Presentation | `docs/demo-script.md` follows problem → user → why it matters → working end-to-end flow. The recorded path should show background sweep, exact exception evidence, one approval, one hold, refresh/restart persistence, and the Strands seam. |

## Submission readiness

Completed in this repository:

- Public GitHub repo: [DominiqueAndrew/clearline-agents-for-humans](https://github.com/DominiqueAndrew/clearline-agents-for-humans)
- Apache 2.0 license, README, source, tests, architecture Markdown, SVG source, and the Devpost-uploadable PNG diagram.
- Science/evidence appendix: [`SCIENCE_APPENDIX.md`](../SCIENCE_APPENDIX.md).
- Testing instructions for a judge: [`README.md`](../README.md) and the appendix reproduction section.
- One-command demo smoke check: `python -m clearline.smoke`.
- Verified public-code receipt (2026-08-27, tested at commit `a84346ae9c2788bbd87e01cc71f93b2de9bdb58b`; later documentation-only commits preserve that tested code): fresh clone install passed `pip check`, `15 passed`, and the smoke invariants (`8` total, `5` filed, `3` pending, no external side effects); the loopback HTTP rehearsal also verified approval, repeat-sweep idempotency, and restart persistence.

Human-only gates still open:

- Confirm personal eligibility and complete any Devpost agreements.
- Supply the participant’s AWS Builder ID.
- Record and publish a truthful public demo video of no more than five minutes.
- Upload the architecture diagram and answer the required submission fields.
- Perform the final Devpost submission confirmation.

No Devpost submission is claimed here.
