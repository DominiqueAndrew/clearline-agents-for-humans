# Clearline product spec

## Problem

Small professional teams receive enough invoices to create a daily second job. Most are routine, but the few that are over policy, missing context, or suspiciously duplicated deserve a person’s attention. A conventional inbox forces the operator to open every message.

## Product promise

Clearline watches a synthetic invoice stream in the background. It extracts the useful fields, checks a visible company policy, files safe invoices automatically, and shows only the invoices where a human must decide. It never pays a vendor, sends an email, or silently approves an exception.

Primary user: an operations or finance lead at a small professional team.

Track: Professional Agents.

## In scope

- A reproducible eight-invoice synthetic shared inbox.
- Policy checks for auto-file limit, purchase-order requirement, known vendor, and duplicate invoice number.
- A queue split into “Filed automatically” and “Needs your call”.
- Evidence for every surfaced decision.
- Explicit `Approve & file` and `Hold & request info` actions.
- An append-only local audit feed.
- A live Strands adapter that adds a model-generated rationale when AWS credentials are present; the deterministic policy gate remains authoritative.

## Out of scope

- Paying invoices or moving money.
- Sending email or contacting vendors.
- Connecting to real inboxes, accounting systems, or personal data.
- Automatically approving ambiguous invoices.
- A general-purpose chat interface.

## Acceptance criteria

### Background triage

Given a clean demo start, when the background worker starts without a decision screen open, then all eight synthetic inbox items receive a decision and the UI shows the counts for filed, surfaced, and value processed.

### Policy evidence

Given an invoice above the `$500` auto-file limit, when it is inspected, then the queue shows the exact amount, policy limit, and reason it was surfaced.

Given a duplicate invoice number, when it is inspected, then the queue identifies the earlier invoice and recommends holding it.

### Human gate

Given a surfaced invoice, when a user chooses `Approve & file`, then its status changes to `Approved by you`, the pending count decreases, and an audit event records the action.

Given a surfaced invoice, when a user chooses `Hold & request info`, then its status changes to `On hold`, no external action is performed, and an audit event records the hold.

Given a human decision has been recorded, when the worker or UI is restarted, then the final status and audit event remain visible from the local state file.

Given the worker runs twice for the same inbox snapshot, when the second sweep completes, then no duplicate decision or audit events are created and human decisions remain unchanged.

### Safety and reproducibility

Given no AWS credentials, when a user starts the demo, then the local deterministic path still works without network access or an API key.

Given `CLEARLINE_STRANDS_LIVE=1` and valid Bedrock access, when a sweep runs, then the Strands adapter can enrich the surfaced decisions without changing the deterministic policy gate.
