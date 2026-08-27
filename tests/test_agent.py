from clearline.agent import StrandsInvoiceAgent
from clearline.domain import Policy
from clearline.fixtures import demo_invoices


def test_live_strands_rationale_enriches_but_does_not_change_gate():
    agent = StrandsInvoiceAgent(live=True)

    class FakeStrandsAgent:
        def __call__(self, prompt):
            assert "NS-9041" in prompt
            return "The amount is above policy, so a person must verify receipt."

    agent._build_strands_agent = lambda: FakeStrandsAgent()
    decision = agent.sweep([demo_invoices()[1]], Policy(), "2026-08-26T12:00:00+00:00")[0]
    assert decision.status == "needs_review"
    assert decision.rationale.startswith("The amount is above policy")


def test_live_failure_falls_back_to_deterministic_gate():
    agent = StrandsInvoiceAgent(live=True)
    agent._build_strands_agent = lambda: (_ for _ in ()).throw(RuntimeError("no model access"))
    decision = agent.sweep([demo_invoices()[1]], Policy(), "2026-08-26T12:00:00+00:00")[0]
    assert decision.status == "needs_review"
    assert decision.rationale is None
    assert "no model access" in agent.last_live_error

