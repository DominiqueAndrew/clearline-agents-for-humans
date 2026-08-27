# Devpost form packet (human-gated)

Prepared from the official [Agents for Humans Devpost overview](https://agentsforhumans.devpost.com/), [rules](https://agentsforhumans.devpost.com/rules), and [submission requirements](https://agentsforhumans.devpost.com/details) queried on 2026-08-27. This is a drafting aid, not a registration or submission. Do not paste participant facts that have not been confirmed.

## Project fields

| Devpost field | Draft answer or artifact | State |
| --- | --- | --- |
| Project name | `Clearline` | Ready |
| Tagline | `A background invoice agent that files routine work and surfaces only the decisions that need a person.` | Ready |
| Description | Use [`docs/submission.md`](submission.md) project description, with [`SCIENCE_APPENDIX.md`](../SCIENCE_APPENDIX.md) linked for evidence and limitations. | Ready |
| Built with | `Python`, `Strands Agents SDK`, `Amazon Bedrock` (optional live rationale), `AWS` | Ready |
| Public code repo | `https://github.com/DominiqueAndrew/clearline-agents-for-humans` | Ready |
| Architecture diagram | Upload [`architecture.png`](architecture.png) | Ready |
| Track | `Professional Agents` | Draft selection |
| Demo video | **Participant must supply a public YouTube or Vimeo URL, maximum 5 minutes.** | Human gate |
| Live demo link | Optional; leave blank unless a public deployment is actually verified. | Optional |
| Testing instructions | `python3 -m venv .venv && .venv/bin/python -m pip install -e '.[dev]' && .venv/bin/python -m clearline.smoke && .venv/bin/python -m pytest -q` | Ready |
| Optional bonus blog post | Leave blank unless a public Builder post titled with `Agents for Humans` is actually published. | Optional |

## Participant fields

These are required by the current form but cannot be inferred safely:

- Submitter type: **participant must choose** `Individual`, `Team of Individuals`, or `Organization`.
- Country of residence: **participant must provide and verify** the current country/territory.
- AWS Builder ID: **participant must provide** their AWS Builder ID.
- Organization name: leave blank unless submitting on behalf of an organization.

## Registration and submission gates

- Registration form says team preference and several experience questions are required; the participant must answer them.
- The rules page states the participant must be above the legal age of majority in their country of residence and observes the listed geographic exclusions; the participant must verify eligibility.
- The rules require a new project created during the submission period. This repository was created during the current submission period; the participant must disclose any pre-existing code or work and confirm that every third-party integration is authorized.
- Devpost requires explicit agreement to the official rules and Devpost terms. No agreement is recorded by this file.
- The final submission must be performed and confirmed by the participant. This workstream has not registered or submitted Clearline.

## Final pre-submit verification

1. Pull the intended public repo and verify its HEAD is `d186e43773607d9a925726884a98150cc8813613` or a later participant-approved commit.
2. Run `python -m clearline.smoke` and `python -m pytest -q` from that exact checkout.
3. Open the live video URL in a logged-out/private browser and confirm it is public, working, and no longer than five minutes.
4. Upload `docs/architecture.png`; do not substitute an unverified screenshot or a private file.
5. Fill participant fields, review eligibility and agreements, then submit only after the participant’s final confirmation.
