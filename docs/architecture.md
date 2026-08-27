# Clearline architecture

```mermaid
flowchart LR
    A[Invoice stream\nsynthetic demo fixture] --> B[Background sweep]
    B --> C[StrandsInvoiceAgent]
    C --> D[Policy tools\nparse · duplicate · policy]
    D --> E{Deterministic safety gate}
    E -->|safe| F[Local ledger\nauto-file]
    E -->|ambiguous| G[Human queue\nevidence + recommendation]
    G --> H[Approve or hold]
    H --> I[Append-only audit log]
    F --> I
    C -. optional model rationale .-> J[AWS Bedrock via Strands]
```

## Why this boundary matters

Strands is the agent runtime for the background work and optional model rationale. The final outcome is still decided by a small, deterministic policy gate. That makes the demo reproducible and prevents a language model from silently taking a financial action. The only write in this prototype is a local status change and audit entry; it never pays or messages a vendor.

## Runtime modes

- **Demo mode (default):** deterministic fixtures and policy evaluation; no credentials or network required.
- **Live rationale mode:** set `CLEARLINE_STRANDS_LIVE=1` after configuring AWS credentials and Bedrock model access. Strands supplies a concise rationale for surfaced items; policy status stays deterministic.

