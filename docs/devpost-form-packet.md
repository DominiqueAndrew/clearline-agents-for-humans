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
- Current required submission field mapping: `27729` submitter type, `27730` country of residence, `27732` track, `27733` public repository URL, `27734` architecture upload, and `27735` AWS Builder ID. The public video is a required deliverable; it is not represented as one of these custom field IDs.

## Registration and submission gates

- Registration team preference is required: choose exactly one of `Working solo`, `Looking for teammates`, or `Already have a team`.
- The current registration form requires these exact custom answers; use the live form’s options and do not invent participant facts:
  - `3985` AWS experience: `New to AWS` / `Some experience (used a few services)` / `Comfortable (build on AWS regularly)` / `Expert (AWS in production daily)`.
  - `4158` Bedrock AgentCore or Strands experience: `Never use either` / `Used Bedrock AgentCore only` / `Used Strands SDK only` / `Used both` / `Heard of them but haven't built with either`.
  - `4159` AI-agent experience: `None yet` / `Tinkered with LLM apps / prompt` / `Built a basic agent (tool calling, RAG)` / `Built production agent systems`.
  - `4160` participation: `Solo` / `I have a team already` / `Looking to join a team` / `Not sure yet`.
  - `4161` help desired (multi-select): `Live mentorship / office hours`, `Starter templates and sample code`, `Workshops and tutorials`, `A sandbox environment to experiment in`, and/or `Clear dos and reference architectures`.
- The rules page states the participant must be above the legal age of majority in their country of residence and observes the listed geographic exclusions; the participant must verify eligibility.
- The rules require a new project created during the submission period. This repository was created during the current submission period; the participant must disclose any pre-existing code or work and confirm that every third-party integration is authorized.
- Before submission, the participant must confirm the project is original and solely owned, all submission materials are in English or have English translations, and judges can install and run it free of charge and without restriction through the judging period.
- Devpost requires explicit agreement to the official rules and Devpost terms. No agreement is recorded by this file.
- The final submission must be performed and confirmed by the participant. This workstream has not registered or submitted Clearline.

## Smallest human action pack

Each row is intentionally a human gate. The evidence column is what to retain after the action; an unavailable credential or account must leave the gate open rather than be guessed.

**Current timing receipt (queried 2026-08-27):** Devpost reports submissions open until `2026-09-15T00:00:00Z`, which is September 14, 2026 at 5:00 PM PT. Recheck the [official event page](https://agentsforhumans.devpost.com/) immediately before uploading or submitting; its live date is authoritative.

| Gate | Required input | One click or command path | Expected evidence | Fallback if unavailable |
| --- | --- | --- | --- | --- |
| Register | Participant eligibility, country, one team preference, five required registration answers, and explicit agreement to the [rules](https://agentsforhumans.devpost.com/rules) and [Devpost terms](https://info.devpost.com/terms). | Open [Agents for Humans](https://agentsforhumans.devpost.com/) → **Register** → choose `Working solo` (or the participant’s true choice) → answer the live form → review both agreements → confirm. | Devpost registration confirmation/status for the participant. | Keep registration unchecked; Clearline remains runnable and the project must not be submitted. |
| Create project | Project name, tagline, description, built-with list, and the public repository URL. | Devpost → **Projects** → **Create project** → enter the prepared answers from this packet → save. | A public Devpost project URL whose text and repository link are readable while logged out. | Keep the packet as a draft; do not invent a project URL. |
| AWS Builder ID | The participant’s own AWS Builder ID. | In the Devpost submission form, paste it into required field `27735` **AWS Builder ID**. | The saved field value is visible in the participant’s draft/review screen. | Leave the field blank; do not substitute an AWS account number, email, or guessed ID. |
| Record video | Screen recorder and a public YouTube or Vimeo account; final URL must be public and ≤5 minutes. | From the repo: `CLEARLINE_STATE_FILE="$(mktemp -d)/state.json" .venv/bin/python -m clearline --port 8787` → record the two-minute flow in [`demo-script.md`](demo-script.md) → publish the video publicly → test logged out. | The URL plays without login, is ≤5 minutes, shows the working interface, problem, user, why it matters, and the human gate. | Use the credential-free local demo and keep the video field unchecked; never claim a URL that was not published and tested. |
| Upload architecture | The committed `docs/architecture.png` file. | In the Devpost submission form, upload `docs/architecture.png` to required field `27734`. | Devpost accepts the PNG and the review page shows the attached architecture diagram. | Leave the upload pending; do not replace it with an unverified screenshot. |
| Scan public repo | No AWS keys, private keys, or hard-coded API secrets. | From the repo root run `! rg -n -I 'AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|-----BEGIN (RSA|EC|OPENSSH|PRIVATE) KEY-----|aws_secret_access_key[[:space:]]*[:=]|api[_-]?key[[:space:]]*[:=]' .` (or use an installed secret scanner). | Zero output and a zero exit status from the negated scan; inspect any match before publishing. | If no scanner is available, use the shown high-confidence scan plus manual review; do not publish while a match is unexplained. |
| Optional live AWS rationale | AWS credentials with Bedrock access and approval to incur any applicable free-tier usage. | `CLEARLINE_STRANDS_LIVE=1 CLEARLINE_STATE_FILE="$(mktemp -d)/state.json" .venv/bin/python -m clearline` → open one surfaced invoice. | The UI reports live rationale mode and shows rationale while the deterministic policy result is unchanged; no credentials enter the repo. | Run the default credential-free command and say only that the Strands seam is implemented, not that a live AWS call was made. |
| Final submit | Participant confirmation of eligibility, originality/ownership, third-party authorization, English/translation, public judge access, all required fields, and the exact public-main test receipt. | Run `git ls-remote https://github.com/DominiqueAndrew/clearline-agents-for-humans.git refs/heads/main`, run the tests from that checkout, open the Devpost review page, verify every required field and agreement, then click **Submit**. | Devpost submitted status, submission URL, timestamp, and the recorded Git SHA. | Stop at review; this workstream must report “not submitted” rather than infer success. |

## Final pre-submit verification

1. Create the Devpost project and join/register for the hackathon; confirm the project was created during the Submission Period.
2. Pull the intended public repo and record the exact SHA returned by `git ls-remote https://github.com/DominiqueAndrew/clearline-agents-for-humans.git refs/heads/main`; run the checks below from that exact checkout.
3. Run `python -m clearline.smoke` and `python -m pytest -q` from that exact checkout.
4. Open the live video URL in a logged-out/private browser and confirm it is public and accessible (not private or an unshared unlisted video), no longer than five minutes, and shows the app working—not only slides or a mockup—while explaining the problem, solution, and Strands use.
5. Upload `docs/architecture.png`; do not substitute an unverified screenshot or a private file.
6. Run the public-repo secret scan above and resolve every match before publishing.
7. Fill participant fields, review eligibility and agreements, then submit only after the participant’s final confirmation.

**Deadline freeze:** The current Devpost instructions say that after the deadline, the project, submission form, code repository, and video must not be edited—even for a typo—until after the winners are announced. Capture the final public-main SHA, form review, architecture upload, and video check before `2026-09-15T00:00:00Z`, then leave those artifacts unchanged through judging.
