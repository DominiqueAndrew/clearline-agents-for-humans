from clearline.store import ClearlineStore
from clearline.worker import BackgroundWorker


def test_store_exposes_background_stats_and_audit():
    store = ClearlineStore(db_path=":memory:")
    BackgroundWorker(store).run_once()
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
    BackgroundWorker(store).run_once()
    store.decide("inv_1002", "approve")
    snapshot = store.snapshot()
    assert snapshot["stats"]["pending"] == 2
    assert snapshot["stats"]["filed"] == 6
    assert snapshot["invoices"][1]["decision"]["status"] == "approved"
    assert snapshot["audit"][0]["kind"] == "human"


def test_human_hold_does_not_count_as_filed():
    store = ClearlineStore(db_path=":memory:")
    BackgroundWorker(store).run_once()
    store.decide("inv_1007", "hold")
    snapshot = store.snapshot()
    assert snapshot["stats"]["pending"] == 2
    assert snapshot["stats"]["on_hold"] == 1
    assert snapshot["stats"]["filed"] == 5


def test_automatic_filing_cannot_receive_a_human_action():
    store = ClearlineStore(db_path=":memory:")
    BackgroundWorker(store).run_once()
    try:
        store.decide("inv_1001", "approve")
    except ValueError as exc:
        assert str(exc) == "only surfaced invoices can receive a human decision"
    else:
        raise AssertionError("automatic filing accepted a human action")


def test_human_decision_survives_a_store_restart(tmp_path):
    state_path = tmp_path / "clearline-state.json"
    first = ClearlineStore(db_path=state_path)
    BackgroundWorker(first).run_once()
    first.decide("inv_1002", "approve")
    second = ClearlineStore(db_path=state_path)
    BackgroundWorker(second).run_once()
    assert second.snapshot()["invoices"][1]["decision"]["status"] == "approved"
    assert second.snapshot()["stats"]["pending"] == 2


def test_repeated_background_sweeps_are_idempotent():
    store = ClearlineStore(db_path=":memory:")
    worker = BackgroundWorker(store)
    first = worker.run_once()
    second = worker.run_once()
    assert second["stats"] == first["stats"]
    assert len(second["audit"]) == 8
    assert second["sweep_count"] == 2
