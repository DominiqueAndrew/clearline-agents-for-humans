from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from threading import RLock
from typing import Any

from .agent import StrandsInvoiceAgent
from .domain import Decision, Invoice, Policy, Reason, decision_to_dict, invoice_to_dict, money, utc_now
from .fixtures import demo_invoices


@dataclass
class AuditEvent:
    timestamp: str
    message: str
    kind: str


class ClearlineStore:
    def __init__(self, agent: StrandsInvoiceAgent | None = None, db_path: str | Path | None = None) -> None:
        self._lock = RLock()
        self.policy = Policy()
        self.agent = agent or StrandsInvoiceAgent()
        self.invoices: dict[str, Invoice] = {invoice.id: invoice for invoice in demo_invoices()}
        self.decisions: dict[str, Decision] = {}
        self.audit: list[AuditEvent] = []
        self.last_sweep: str | None = None
        self.sweep_count = 0
        configured_path = db_path if db_path is not None else os.getenv("CLEARLINE_STATE_FILE", "data/clearline-state.json")
        self._state_path = None if str(configured_path) == ":memory:" else Path(configured_path)
        self._load()
        self.run_sweep()

    def run_sweep(self) -> dict[str, Any]:
        with self._lock:
            timestamp = utc_now()
            decisions = self.agent.sweep(self.invoices.values(), self.policy, decided_at=timestamp)
            for decision in decisions:
                previous = self.decisions.get(decision.invoice_id)
                if previous and previous.status in {"approved", "on_hold"}:
                    continue
                self.decisions[decision.invoice_id] = decision
                if previous is None:
                    self.audit.append(
                        AuditEvent(
                            timestamp=timestamp,
                            message=self._automated_message(decision),
                            kind="agent",
                        )
                    )
            self.last_sweep = timestamp
            self.sweep_count += 1
            self._persist()
            return self.snapshot()

    def decide(self, invoice_id: str, action: str) -> dict[str, Any]:
        with self._lock:
            if action not in {"approve", "hold"}:
                raise ValueError("action must be approve or hold")
            if invoice_id not in self.invoices:
                raise KeyError(invoice_id)
            current = self.decisions[invoice_id]
            if current.status != "needs_review":
                raise ValueError("only surfaced invoices can receive a human decision")
            timestamp = utc_now()
            status = "approved" if action == "approve" else "on_hold"
            message = (
                f"You approved {self.invoices[invoice_id].invoice_number} for local filing"
                if action == "approve"
                else f"You placed {self.invoices[invoice_id].invoice_number} on hold for more context"
            )
            self.decisions[invoice_id] = Decision(
                invoice_id=current.invoice_id,
                status=status,
                recommendation=current.recommendation,
                reasons=current.reasons,
                evidence=current.evidence,
                confidence=current.confidence,
                decided_at=timestamp,
                decided_by="You",
                rationale=current.rationale,
            )
            self.audit.append(AuditEvent(timestamp=timestamp, message=message, kind="human"))
            self._persist()
            return self.snapshot()

    def _load(self) -> None:
        if self._state_path is None or not self._state_path.is_file():
            return
        try:
            payload = json.loads(self._state_path.read_text(encoding="utf-8"))
            self.last_sweep = payload.get("last_sweep")
            self.sweep_count = int(payload.get("sweep_count", 0))
            self.audit = [AuditEvent(**event) for event in payload.get("audit", [])]
            self.decisions = {}
            for invoice_id, raw in payload.get("decisions", {}).items():
                reasons = tuple(Reason(**reason) for reason in raw.get("reasons", []))
                self.decisions[invoice_id] = Decision(
                    invoice_id=raw["invoice_id"],
                    status=raw["status"],
                    recommendation=raw["recommendation"],
                    reasons=reasons,
                    evidence=tuple(raw.get("evidence", [])),
                    confidence=int(raw["confidence"]),
                    decided_at=raw["decided_at"],
                    decided_by=raw["decided_by"],
                    rationale=raw.get("rationale"),
                )
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError):
            self.decisions = {}
            self.audit = []
            self.last_sweep = None
            self.sweep_count = 0

    def _persist(self) -> None:
        if self._state_path is None:
            return
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "last_sweep": self.last_sweep,
            "sweep_count": self.sweep_count,
            "decisions": {key: decision_to_dict(value) for key, value in self.decisions.items()},
            "audit": [
                {"timestamp": event.timestamp, "message": event.message, "kind": event.kind}
                for event in self.audit
            ],
        }
        temporary = self._state_path.with_suffix(self._state_path.suffix + ".tmp")
        temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        temporary.replace(self._state_path)

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            decisions = [self.decisions[key] for key in self.invoices]
            filed = [decision for decision in decisions if decision.status in {"auto_filed", "approved"}]
            pending = [decision for decision in decisions if decision.status == "needs_review"]
            on_hold = [decision for decision in decisions if decision.status == "on_hold"]
            processed_cents = sum(self.invoices[item.invoice_id].amount_cents for item in filed)
            return {
                "product": "Clearline",
                "mode": "live rationale" if self.agent.live else "demo mode",
                "sdk": self.agent.sdk_name,
                "model": self.agent.model_name,
                "last_live_error": self.agent.last_live_error,
                "policy": {
                    "version": self.policy.version,
                    "auto_file_limit": money(self.policy.auto_file_limit_cents),
                    "po_required_over": money(self.policy.po_required_over_cents),
                },
                "last_sweep": self.last_sweep,
                "sweep_count": self.sweep_count,
                "stats": {
                    "total": len(decisions),
                    "filed": len(filed),
                    "pending": len(pending),
                    "on_hold": len(on_hold),
                    "processed_cents": processed_cents,
                },
                "invoices": [
                    {
                        **invoice_to_dict(self.invoices[item.id]),
                        "decision": decision_to_dict(self.decisions[item.id]),
                    }
                    for item, decision in zip(self.invoices.values(), decisions)
                ],
                "audit": [
                    {"timestamp": event.timestamp, "message": event.message, "kind": event.kind}
                    for event in reversed(self.audit[-12:])
                ],
            }

    def _automated_message(self, decision: Decision) -> str:
        invoice = self.invoices[decision.invoice_id]
        if decision.status == "auto_filed":
            return f"Filed {invoice.invoice_number} from {invoice.vendor} automatically · {money(invoice.amount_cents)}"
        reason = decision.reasons[0].label.lower()
        return f"Surfaced {invoice.invoice_number} · {reason}"
