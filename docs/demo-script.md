# Clearline demo script (2 minutes)

## Clean start

Run this from the repository root before recording. It proves the local contract without AWS credentials or a browser:

```bash
.venv/bin/python -m clearline.smoke
```

Then launch a clean browser session using a temporary state file so previous clicks never change the recording:

```bash
CLEARLINE_STATE_FILE="$(mktemp -d)/state.json" .venv/bin/python -m clearline --port 8787
```

1. **Open the product (0:00–0:15).** “Clearline is for the person who approves every invoice at a small company. It runs in the background, so the inbox is not their job.” Point to the top-right `Strands Agents SDK · demo mode` badge, `Quiet mode on`, `8 invoices`, and the `5 filed / 3 need you` split. “Strands runs the agent seam; the visible policy gate still owns the decision.”
2. **Show the quiet work (0:15–0:40).** Select `LumaStack Cloud`. “This one is known, under the $500 cap, and has no exception. Clearline filed it without asking me.” Point to the policy checks and audit event.
3. **Show a real decision (0:40–1:10).** Select `Northstar Courier`. “This is $742, above the $500 auto-file limit. Clearline does not guess; it brings me the amount, policy, PO, and a recommendation.” Click `Approve & file` to show the explicit human gate.
4. **Show the other kind of ambiguity (1:10–1:35).** Select the duplicate `LumaStack Cloud`. “This is not an amount problem. It matches an invoice already filed. I can hold it and ask for information, but Clearline never sends the request on its own.” Click `Hold & request info`.
5. **Close on the boundary (1:35–2:00).** Point to the audit feed, then refresh the page once. “Every automated or human decision is visible, and the approval and hold remain after refresh because Clearline persists its local state.” Call out that the hero sentence follows the remaining queue (`3` → `2` → `1`), so the request for human attention cannot go stale after a decision. “The model can help explain a case in live mode, but the policy gate and human approval are the control plane.”

The recording must show the working interface, not only this script. Keep the final video public and at most five minutes for Devpost; do not claim a video URL until it is actually published.

## Optional Strands proof shot

If the participant has Bedrock access, run a separate clean recording state with `CLEARLINE_STRANDS_LIVE=1` as described in the README. Open one pending invoice and briefly point to the `STRANDS RATIONALE` block: “This is where the Strands adapter adds explanation. It does not own the policy result or the human action.” If live access is unavailable, keep the credential-free recording; do not imply that a live AWS invocation was performed. The committed adapter, tool seam, fallback test, and architecture remain the evidence for the implementation criterion.
