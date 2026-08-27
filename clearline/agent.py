from __future__ import annotations

import os
from dataclasses import replace
from typing import Iterable

from .domain import Decision, Invoice, Policy, classify_invoices


class StrandsInvoiceAgent:
    """Background worker with a deterministic safety gate and optional Strands rationale."""

    sdk_name = "AWS Strands Agents SDK"
    model_name = "Amazon Bedrock · optional live rationale"

    def __init__(self, live: bool | None = None) -> None:
        self.live = live if live is not None else os.getenv("CLEARLINE_STRANDS_LIVE", "0") == "1"
        self.last_live_error: str | None = None

    def sweep(self, invoices: Iterable[Invoice], policy: Policy, decided_at: str) -> list[Decision]:
        items = list(invoices)
        decisions = classify_invoices(items, policy, decided_at=decided_at)
        if not self.live:
            return decisions

        try:
            live_agent = self._build_strands_agent()
            enriched: list[Decision] = []
            for decision in decisions:
                if decision.status != "needs_review":
                    enriched.append(decision)
                    continue
                invoice = next(item for item in items if item.id == decision.invoice_id)
                prompt = self._rationale_prompt(invoice, decision, policy)
                response = live_agent(prompt)
                rationale = str(response).strip()
                enriched.append(replace(decision, rationale=rationale[:600] or None))
            return enriched
        except Exception as exc:  # pragma: no cover - depends on external AWS credentials
            self.last_live_error = f"{type(exc).__name__}: {exc}"
            return decisions

    @staticmethod
    def _build_strands_agent():
        from strands import Agent, tool

        @tool
        def clearline_safety_boundary() -> str:
            """Return the non-negotiable boundary for invoice decisions."""
            return "Never pay, approve, or contact a vendor; explain evidence and leave the decision to the user."

        return Agent(
            system_prompt=(
                "You are Clearline's invoice review explainer. "
                "Explain the supplied policy evidence in two concise sentences. "
                "Never approve, pay, or contact anyone."
            ),
            tools=[clearline_safety_boundary],
        )

    @staticmethod
    def _rationale_prompt(invoice: Invoice, decision: Decision, policy: Policy) -> str:
        reasons = "; ".join(reason.detail for reason in decision.reasons)
        return (
            f"Invoice {invoice.invoice_number} from {invoice.vendor} is {invoice.amount_cents / 100:.2f} "
            f"{invoice.currency}. Policy cap is {policy.auto_file_limit_cents / 100:.2f}. "
            f"Deterministic reasons: {reasons}. Recommendation: {decision.recommendation}."
        )
