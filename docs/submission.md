# Agents for Humans submission readiness

This checklist is intentionally honest: Devpost account actions, AWS Builder ID, video publishing, and final submission remain human-only gates.

## Live requirements verified from Devpost on 2026-08-27

- [x] New agent targets a real repetitive professional task and handles it end to end.
- [x] Uses the Strands Agents SDK in the live rationale path.
- [x] Public repository URL: pending GitHub publish from this worktree.
- [x] MIT or Apache license file: `LICENSE` (Apache 2.0).
- [x] README with setup and testing instructions.
- [x] Architecture diagram: `docs/architecture.md` and `docs/architecture.svg`.
- [ ] Public demo video, maximum 5 minutes, with problem, user, why it matters, and working demo.
- [ ] AWS Builder ID: human account detail required.
- [ ] Devpost eligibility, registration, agreements, and final submission: human-only.

## Project description draft

Clearline is the invoice queue that only asks for a human when the invoice is genuinely ambiguous. A background Strands agent reads a synthetic invoice stream, checks vendor, duplicate, PO, and amount rules, and files routine invoices locally. It surfaces exceptions with the exact evidence behind them, then lets a person approve or hold the case. It never pays a vendor or sends a message, and every action lands in an audit feed.

## Video outline

Use `docs/demo-script.md`. The final public YouTube or Vimeo URL is intentionally not invented here.

