from clearline.domain import Policy, classify_invoice, classify_invoices
from clearline.fixtures import demo_invoices


def test_demo_stream_has_five_automatic_and_three_surfaced_decisions():
    decisions = classify_invoices(demo_invoices(), Policy(), decided_at="2026-08-26T12:00:00+00:00")
    assert [decision.status for decision in decisions].count("auto_filed") == 5
    assert [decision.status for decision in decisions].count("needs_review") == 3


def test_over_limit_invoice_surfaces_exact_policy_evidence():
    decision = classify_invoices(demo_invoices(), Policy(), decided_at="2026-08-26T12:00:00+00:00")[1]
    assert decision.status == "needs_review"
    assert decision.reasons[0].code == "over_limit"
    assert "$742.00" in decision.reasons[0].detail
    assert "$500.00" in decision.reasons[0].detail


def test_duplicate_is_a_human_hold_recommendation():
    decision = classify_invoices(demo_invoices(), Policy(), decided_at="2026-08-26T12:00:00+00:00")[6]
    assert decision.reasons[0].code == "duplicate"
    assert decision.recommendation == "Hold and request context"


def test_missing_po_only_matters_above_threshold():
    low = demo_invoices()[3]
    high = demo_invoices()[2]
    low_decision = classify_invoice(low, Policy(), {})
    high_decision = classify_invoice(high, Policy(), {})
    assert low_decision.status == "auto_filed"
    assert high_decision.status == "needs_review"
    assert any(reason.code == "missing_po" for reason in high_decision.reasons)

