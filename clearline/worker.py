from __future__ import annotations

from typing import Any

from .store import ClearlineStore


class BackgroundWorker:
    """Own when a sweep runs; the store owns persistence and policy state."""

    def __init__(self, store: ClearlineStore) -> None:
        self.store = store

    def run_once(self) -> dict[str, Any]:
        """Run one idempotent background sweep without requiring the UI to be open."""
        return self.store.run_sweep()
