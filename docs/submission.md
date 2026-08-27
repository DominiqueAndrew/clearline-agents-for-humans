# Agents for Humans submission readiness

This checklist is intentionally honest: Devpost account actions, AWS Builder ID, video publishing, and final submission remain human-only gates. The evidence and rubric annex is [`docs/judge-brief.md`](judge-brief.md), with technical sources and reproducibility in [`SCIENCE_APPENDIX.md`](../SCIENCE_APPENDIX.md).

## Live requirements verified from Devpost on 2026-08-27

- [x] New agent targets a real repetitive professional task and handles it end to end.
- [x] Uses the Strands Agents SDK in the live rationale path.
- [x] Public repository URL: [DominiqueAndrew/clearline-agents-for-humans](https://github.com/DominiqueAndrew/clearline-agents-for-humans).
- [x] MIT or Apache license file: `LICENSE` (Apache 2.0).
- [x] README with setup and testing instructions.
- [x] Architecture diagram: `docs/architecture.md`, source `docs/architecture.svg`, and Devpost-uploadable `docs/architecture.png`.
- [ ] Participant must create the Devpost project during the submission period; the verified GitHub repository was created on 2026-08-27, and any pre-existing code or work and third-party integrations must be disclosed and authorized before submission.
- [ ] Public demo video, maximum 5 minutes, with problem, user, why it matters, and working demo.
- [ ] AWS Builder ID: human account detail required.
- [ ] Devpost eligibility, registration, agreements, and final submission: human-only.

## Project description draft

Clearline is the invoice queue that only asks for a human when the invoice is genuinely ambiguous. A background invoice agent reads a synthetic invoice stream, checks vendor, duplicate, PO, and amount rules, and files routine invoices locally. Its `StrandsInvoiceAgent` adapter can add a concise model rationale through the Strands Agents SDK and Amazon Bedrock without changing the deterministic outcome. It surfaces exceptions with the exact evidence behind them, then lets a person approve or hold the case. It never pays a vendor or sends a message, and every action lands in an audit feed.

## Video outline

Use `docs/demo-script.md`. The final public YouTube or Vimeo URL is intentionally not invented here.

## Official rubric and field notes

The Devpost Hackathons plugin snapshot on 2026-08-27 reports five criteria: Technological Implementation, Design, Potential Impact, Creativity & Originality, and Presentation. Clearline’s evidence for each is mapped in [`docs/judge-brief.md`](judge-brief.md). The required submission form also asks for submitter type, country of residence, track, public repo URL, architecture upload, AWS Builder ID, and a required public video; optional fields include a live demo, testing instructions, and an AWS Builder post. These account and agreement fields must be completed by the participant at submission time.

Use [`docs/devpost-form-packet.md`](devpost-form-packet.md) for draft answers, the exact human action pack, and the final participant-controlled checklist.
