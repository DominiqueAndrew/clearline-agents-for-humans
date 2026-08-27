from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Iterable


@dataclass(frozen=True)
class Invoice:
    id: str
    vendor: str
    invoice_number: str
    amount_cents: int
    currency: str
    received_at: str
    po_number: str | None
    description: str
    due_date: str
    category: str
    duplicate_of: str | None = None


@dataclass(frozen=True)
class Policy:
    version: str = "v3.2"
    auto_file_limit_cents: int = 50_000
    po_required_over_cents: int = 25_000
    known_vendors: frozenset[str] = field(
        default_factory=lambda: frozenset(
            {
                "LumaStack Cloud",
                "Northstar Courier",
                "Field & Finch",
                "Cedar & Co",
                "Atlas Design",
                "Parcel Hive",
                "Morrow Studio",
            }
        )
    )


@dataclass(frozen=True)
class Reason:
    code: str
    label: str
    detail: str
    severity: str = "warning"


@dataclass(frozen=True)
class Decision:
    invoice_id: str
    status: str
    recommendation: str
    reasons: tuple[Reason, ...]
    evidence: tuple[str, ...]
    confidence: int
    decided_at: str
    decided_by: str
    rationale: str | None = None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def money(cents: int, currency: str = "USD") -> str:
    return f"{currency} ${cents / 100:,.2f}"


def classify_invoice(
    invoice: Invoice,
    policy: Policy,
    seen_keys: dict[tuple[str, str], str],
    decided_at: str | None = None,
) -> Decision:
    reasons: list[Reason] = []
    duplicate_id = invoice.duplicate_of or seen_keys.get((invoice.vendor, invoice.invoice_number))
    if duplicate_id and duplicate_id != invoice.id:
        reasons.append(
            Reason(
                code="duplicate",
                label="Possible duplicate",
                detail=f"Matches invoice {duplicate_id} from {invoice.vendor}",
                severity="high",
            )
        )
    if invoice.amount_cents > policy.auto_file_limit_cents:
        reasons.append(
            Reason(
                code="over_limit",
                label="Above auto-file limit",
                detail=(
                    f"{money(invoice.amount_cents)} is above the "
                    f"{money(policy.auto_file_limit_cents)} policy cap"
                ),
                severity="high",
            )
        )
    if invoice.amount_cents >= policy.po_required_over_cents and not invoice.po_number:
        reasons.append(
            Reason(
                code="missing_po",
                label="Purchase order missing",
                detail=f"Invoices at or above {money(policy.po_required_over_cents)} need a PO",
                severity="high",
            )
        )
    if invoice.vendor not in policy.known_vendors:
        reasons.append(
            Reason(
                code="unknown_vendor",
                label="Vendor not recognized",
                detail="No matching vendor exists in the team policy",
                severity="warning",
            )
        )

    if reasons:
        recommendation = "Hold and request context" if any(r.code == "duplicate" for r in reasons) else "Approve manually if the work is verified"
        status = "needs_review"
        confidence = max(72, 96 - len(reasons) * 8)
        decided_by = "Clearline policy agent"
    else:
        recommendation = "File to the local ledger"
        status = "auto_filed"
        confidence = 99
        decided_by = "Clearline policy agent"

    evidence = (
        f"Invoice total: {money(invoice.amount_cents, invoice.currency)}",
        f"Auto-file limit: {money(policy.auto_file_limit_cents, invoice.currency)}",
        f"Purchase order: {invoice.po_number or 'not provided'}",
        f"Vendor: {invoice.vendor}",
    )
    return Decision(
        invoice_id=invoice.id,
        status=status,
        recommendation=recommendation,
        reasons=tuple(reasons),
        evidence=evidence,
        confidence=confidence,
        decided_at=decided_at or utc_now(),
        decided_by=decided_by,
    )


def classify_invoices(invoices: Iterable[Invoice], policy: Policy, decided_at: str | None = None) -> list[Decision]:
    seen_keys: dict[tuple[str, str], str] = {}
    decisions: list[Decision] = []
    for invoice in invoices:
        decision = classify_invoice(invoice, policy, seen_keys, decided_at)
        decisions.append(decision)
        seen_keys.setdefault((invoice.vendor, invoice.invoice_number), invoice.id)
    return decisions


def invoice_to_dict(invoice: Invoice) -> dict[str, Any]:
    return asdict(invoice)


def decision_to_dict(decision: Decision) -> dict[str, Any]:
    payload = asdict(decision)
    payload["reasons"] = [asdict(reason) for reason in decision.reasons]
    payload["evidence"] = list(decision.evidence)
    return payload

