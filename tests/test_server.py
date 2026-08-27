import json
from threading import Thread
from urllib.request import Request, urlopen

from clearline.server import create_server
from clearline.store import ClearlineStore


def test_http_demo_serves_state_and_human_action():
    server = create_server("127.0.0.1", 0, ClearlineStore(db_path=":memory:"))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        with urlopen(f"{base}/api/state") as response:
            state = json.load(response)
        assert state["stats"]["pending"] == 3

        request = Request(
            f"{base}/api/invoices/inv_1002/decision",
            data=json.dumps({"action": "approve"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request) as response:
            updated = json.load(response)
        assert updated["invoices"][1]["decision"]["status"] == "approved"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
