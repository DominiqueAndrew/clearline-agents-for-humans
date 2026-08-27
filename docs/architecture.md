# Clearline architecture

```mermaid
flowchart LR
    A[Invoice stream\nsynthetic demo fixture] --> B[Background sweep]
    B --> C[BackgroundWorker\nrun once or on schedule]
    C --> D[StrandsInvoiceAgent]
    D --> E[Policy tools\nparse · duplicate · policy]
    E --> F{Deterministic safety gate}
    F -->|safe| G[Local ledger\nauto-file]
    F -->|ambiguous| H[Human queue\nevidence + recommendation]
    H --> I[Approve or hold]
    I --> J[Append-only audit log]
    G --> J
    D -. optional model rationale .-> K[AWS Bedrock via Strands]
```

## Why this boundary matters

The background worker owns when a sweep runs; the Strands agent owns the agent/tool seam and optional model rationale; the final outcome is still decided by a small, deterministic policy gate. That makes the demo reproducible and prevents a language model from silently taking a financial action. The only write in this prototype is a local status change and audit entry; it never pays or messages a vendor.

## Runtime modes

- **Demo mode (default):** deterministic fixtures and policy evaluation; no credentials or network required.
- **Live rationale mode:** set `CLEARLINE_STRANDS_LIVE=1` after configuring AWS credentials and Bedrock model access. Strands supplies a concise rationale for surfaced items; policy status stays deterministic.
