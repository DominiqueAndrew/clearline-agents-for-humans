from clearline.store import ClearlineStore


def test_store_exposes_background_stats_and_audit():
    store = ClearlineStore(db_path=":memory:")
    snapshot = store.snapshot()
    assert snapshot["stats"] == {
        "total": 8,
        "filed": 5,
        "pending": 3,
        "on_hold": 0,
        "processed_cents": 93300,
    }
    assert snapshot["sdk"] == "AWS Strands Agents SDK"
    assert len(snapshot["audit"]) == 8


def test_human_approve_decreases_pending_and_adds_audit_event():
    store = ClearlineStore(db_path=":memory:")
    store.decide("inv_1002", "approve")
    snapshot = store.snapshot()
    assert snapshot["stats"]["pending"] == 2
    assert snapshot["stats"]["filed"] == 6
    assert snapshot["invoices"][1]["decision"]["status"] == "approved"
    assert snapshot["audit"][0]["kind"] == "human"


def test_human_hold_does_not_count_as_filed():
    store = ClearlineStore(db_path=":memory:")
    store.decide("inv_1007", "hold")
    snapshot = store.snapshot()
    assert snapshot["stats"]["pending"] == 2
    assert snapshot["stats"]["on_hold"] == 1
    assert snapshot["stats"]["filed"] == 5


def test_human_decision_survives_a_store_restart(tmp_path):
    state_path = tmp_path / "clearline-state.json"
    first = ClearlineStore(db_path=state_path)
    first.decide("inv_1002", "approve")
    second = ClearlineStore(db_path=state_path)
    assert second.snapshot()["invoices"][1]["decision"]["status"] == "approved"
    assert second.snapshot()["stats"]["pending"] == 2
