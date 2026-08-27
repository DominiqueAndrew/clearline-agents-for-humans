from __future__ import annotations

import json
import tempfile
from pathlib import Path

from .store import ClearlineStore
from .worker import BackgroundWorker


def run_smoke() -> dict[str, object]:
    """Exercise the credential-free demo contract without starting a server."""
    in_memory = ClearlineStore(db_path=":memory:")
    worker = BackgroundWorker(in_memory)
    first = worker.run_once()
    repeated = worker.run_once()
    assert first["stats"] == {
        "total": 8,
        "filed": 5,
        "pending": 3,
        "on_hold": 0,
        "processed_cents": 93_300,
    }
    assert repeated["stats"] == first["stats"]
    assert repeated["sweep_count"] == 2
    assert len(repeated["audit"]) == 8

    approved = in_memory.decide("inv_1002", "approve")
    assert approved["stats"]["pending"] == 2
    assert approved["invoices"][1]["decision"]["status"] == "approved"
    try:
        in_memory.decide("inv_1001", "approve")
    except ValueError as exc:
        assert str(exc) == "only surfaced invoices can receive a human decision"
    else:
        raise AssertionError("automatic filing accepted a human action")

    with tempfile.TemporaryDirectory(prefix="clearline-smoke-") as directory:
        state_path = Path(directory) / "state.json"
        persisted = ClearlineStore(db_path=state_path)
        BackgroundWorker(persisted).run_once()
        persisted.decide("inv_1002", "approve")
        restored = ClearlineStore(db_path=state_path)
        BackgroundWorker(restored).run_once()
        restored_snapshot = restored.snapshot()
        assert restored_snapshot["invoices"][1]["decision"]["status"] == "approved"
        assert restored_snapshot["stats"]["pending"] == 2

    return {
        "invoices": first["stats"]["total"],
        "filed": first["stats"]["filed"],
        "pending": first["stats"]["pending"],
        "repeat_sweep_audit": len(repeated["audit"]),
        "approval_persisted": True,
        "external_side_effects": False,
    }


def main() -> None:
    print(f"Clearline smoke passed: {json.dumps(run_smoke(), sort_keys=True)}")


if __name__ == "__main__":
    main()
